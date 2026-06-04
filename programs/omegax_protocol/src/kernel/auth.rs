// SPDX-License-Identifier: AGPL-3.0-or-later

//! Authorization, authority, and bounded-field validation helpers.

use crate::platform::*;

use crate::args::*;
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

// Resolve the SPL recipient for a claim settlement. Routing is exclusively
// controlled by the member-set delegate_recipient field on ClaimCase: if it
// is the ZERO_PUBKEY, payouts go to member_position.wallet. The `claimant`
// field on ClaimCase is informational metadata only — it is constrained at
// intake to equal member_position.wallet (PT-2026-04-27-04 fix).
pub(crate) fn resolve_claim_settlement_recipient(
    claim_case: &ClaimCaseAccountData<'_>,
    member_position: &MemberPosition,
) -> Pubkey {
    if claim_case.delegate_recipient != ZERO_PUBKEY {
        claim_case.delegate_recipient
    } else {
        member_position.wallet
    }
}

pub(crate) fn require_claim_intake_submitter(
    authority: &Pubkey,
    plan: &HealthPlanAccountData<'_>,
    member_position: &MemberPosition,
    args: &OpenClaimCaseArgs,
) -> Result<()> {
    // Both branches require args.claimant == member_position.wallet so the
    // claimant field cannot be used to divert funds when settlement transfers
    // ship. Recipient routing is handled separately via ClaimCase.delegate_recipient
    // (set by the member via `authorize_claim_recipient`).
    let claimant_is_member = args.claimant == member_position.wallet;
    let member_self_submit = *authority == member_position.wallet && claimant_is_member;
    let operator_submit =
        (*authority == plan.claims_operator || *authority == plan.plan_admin) && claimant_is_member;

    if member_self_submit || operator_submit {
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
