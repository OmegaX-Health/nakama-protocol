// SPDX-License-Identifier: AGPL-3.0-or-later

//! Authorization, authority, and bounded-field validation helpers.

use crate::platform::*;

use crate::constants::*;
use crate::errors::*;
use crate::state::*;

pub(crate) fn require_id(value: &str) -> Result<()> {
    require!(
        value.len() <= MAX_ID_LEN,
        OmegaXProtocolError::IdentifierTooLong
    );
    Ok(())
}

pub(crate) fn require_health_plan_active(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require!(plan.active, OmegaXProtocolError::HealthPlanInactive);
    Ok(())
}

pub(crate) fn require_plan_pause_flags_clear(
    plan: &HealthPlanAccountData<'_>,
    flags: u32,
    error: OmegaXProtocolError,
) -> Result<()> {
    if plan.pause_flags & flags == 0 {
        Ok(())
    } else {
        Err(error.into())
    }
}

pub(crate) fn require_plan_operations_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_health_plan_active(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_PROTOCOL_EMERGENCY | PAUSE_FLAG_PLAN_OPERATIONS,
        OmegaXProtocolError::HealthPlanPaused,
    )
}

pub(crate) fn require_reserve_rails_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_plan_operations_open(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_DOMAIN_RAILS | PAUSE_FLAG_ALLOCATION_FREEZE,
        OmegaXProtocolError::HealthPlanPaused,
    )
}

pub(crate) fn require_capital_subscriptions_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_reserve_rails_open(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_CAPITAL_SUBSCRIPTIONS,
        OmegaXProtocolError::HealthPlanPaused,
    )
}

pub(crate) fn require_reserve_redemptions_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_reserve_rails_open(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_REDEMPTION_QUEUE_ONLY,
        OmegaXProtocolError::HealthPlanPaused,
    )
}

pub(crate) fn require_claim_intake_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_plan_operations_open(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_CLAIM_INTAKE,
        OmegaXProtocolError::ClaimIntakePaused,
    )
}

pub(crate) fn require_claim_finality_open(plan: &HealthPlanAccountData<'_>) -> Result<()> {
    require_reserve_rails_open(plan)?;
    require_plan_pause_flags_clear(
        plan,
        PAUSE_FLAG_ORACLE_FINALITY_HOLD,
        OmegaXProtocolError::OracleFinalityHeld,
    )
}

pub(crate) fn require_positive_amount(amount: u64) -> Result<()> {
    require!(amount > 0, OmegaXProtocolError::AmountMustBePositive);
    Ok(())
}

pub(crate) fn require_domain_control(
    authority: &Pubkey,
    domain: &ReserveDomainAccountData<'_>,
) -> Result<()> {
    if *authority == domain.domain_admin {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn require_plan_control(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.plan_admin || *authority == plan.sponsor_operator {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn obligation_has_linked_claim_case(obligation: &ObligationAccountData<'_>) -> bool {
    obligation.claim_case != ZERO_PUBKEY
}

pub(crate) fn require_linked_claim_reserve_operator(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.oracle_authority
        || *authority == plan.claims_operator
        || *authority == plan.plan_admin
    {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn require_linked_claim_settlement_operator(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.claims_operator || *authority == plan.plan_admin {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn require_obligation_reserve_control(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
    obligation: &ObligationAccountData<'_>,
) -> Result<()> {
    if obligation_has_linked_claim_case(obligation) {
        require_linked_claim_reserve_operator(authority, plan)
    } else {
        require_plan_control(authority, plan)
    }
}

pub(crate) fn require_obligation_settlement_control(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
    obligation: &ObligationAccountData<'_>,
) -> Result<()> {
    if obligation_has_linked_claim_case(obligation) {
        require_linked_claim_settlement_operator(authority, plan)
    } else {
        require_plan_control(authority, plan)
    }
}

// Resolve the SPL recipient for a claim settlement. The claimant is now the
// on-chain settlement default; a claimant-authorized delegate may override it.
pub(crate) fn resolve_claim_settlement_recipient(claim_case: &ClaimCaseAccountData<'_>) -> Pubkey {
    if claim_case.delegate_recipient != ZERO_PUBKEY {
        claim_case.delegate_recipient
    } else {
        claim_case.claimant
    }
}

pub(crate) fn require_claim_intake_submitter(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
    claimant: Pubkey,
) -> Result<()> {
    let claimant_present = claimant != ZERO_PUBKEY;
    let claimant_self_submit = *authority == claimant && claimant_present;
    let operator_submit =
        (*authority == plan.claims_operator || *authority == plan.plan_admin) && claimant_present;

    if claimant_self_submit || operator_submit {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn require_claim_operator(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.claims_operator || *authority == plan.plan_admin {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

pub(crate) fn require_direct_claim_settlement_control(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.plan_admin {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}
