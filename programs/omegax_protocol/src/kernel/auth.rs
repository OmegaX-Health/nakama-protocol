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

pub(crate) fn require_valid_attestation_decision(decision: u8) -> Result<()> {
    match decision {
        CLAIM_ATTESTATION_DECISION_SUPPORT_APPROVE
        | CLAIM_ATTESTATION_DECISION_SUPPORT_DENY
        | CLAIM_ATTESTATION_DECISION_REQUEST_REVIEW
        | CLAIM_ATTESTATION_DECISION_ABSTAIN => Ok(()),
        _ => err!(OmegaXProtocolError::InvalidClaimAttestationDecision),
    }
}

pub(crate) fn is_zero_hash(value: &[u8; 32]) -> bool {
    *value == [0; 32]
}

pub(crate) fn require_claim_attestation_oracle_authority(
    health_plan: &HealthPlanAccountData<'_>,
    _funding_line: &FundingLineAccountData<'_>,
    oracle: Pubkey,
) -> Result<()> {
    require_keys_eq!(
        oracle,
        health_plan.oracle_authority,
        OmegaXProtocolError::Unauthorized
    );
    Ok(())
}
