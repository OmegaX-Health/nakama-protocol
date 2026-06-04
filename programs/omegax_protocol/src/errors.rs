// SPDX-License-Identifier: AGPL-3.0-or-later

//! Protocol error codes.

use crate::platform::*;

#[cfg(not(feature = "quasar"))]
#[error_code]
pub enum OmegaXProtocolError {
    #[msg("Caller is not authorized for this scope")]
    Unauthorized,
    #[msg("Reserve domain is inactive")]
    ReserveDomainInactive,
    #[msg("Domain asset vault token account is missing or invalid")]
    VaultTokenAccountInvalid,
    #[msg("Health plan is paused")]
    HealthPlanPaused,
    #[msg("Claim intake is paused")]
    ClaimIntakePaused,
    #[msg("Invalid basis points value")]
    InvalidBps,
    #[msg("Identifier length exceeds the canonical maximum")]
    IdentifierTooLong,
    #[msg("Health plan mismatch")]
    HealthPlanMismatch,
    #[msg("Policy series mismatch")]
    PolicySeriesMismatch,
    #[msg("Policy series is missing where one is required")]
    PolicySeriesMissing,
    #[msg("Unexpected series ledger was provided")]
    SeriesLedgerUnexpected,
    #[msg("Asset mint mismatch")]
    AssetMintMismatch,
    #[msg("Source token account owner does not match the signer")]
    TokenAccountOwnerMismatch,
    #[msg("Source and vault token accounts must be different accounts")]
    TokenAccountSelfTransferInvalid,
    #[msg("Vault token account does not match the domain asset vault")]
    VaultTokenAccountMismatch,
    #[msg("Token-2022 custody rails are not supported by this protocol version")]
    Token2022NotSupported,
    #[msg("Funding line mismatch")]
    FundingLineMismatch,
    #[msg("Funding line type mismatch")]
    FundingLineTypeMismatch,
    #[msg("Obligation account mismatch")]
    ObligationMismatch,
    #[msg("Invalid obligation state transition")]
    InvalidObligationStateTransition,
    #[msg("Amount exceeds outstanding obligation")]
    AmountExceedsOutstandingObligation,
    #[msg("Amount exceeds reserved balance")]
    AmountExceedsReservedBalance,
    #[msg("Amount exceeds approved claim")]
    AmountExceedsApprovedClaim,
    #[msg("Amount must be greater than zero")]
    AmountMustBePositive,
    #[msg("Claim case linkage mismatch")]
    ClaimCaseLinkMismatch,
    #[msg("Linked claims must settle through the obligation path")]
    LinkedClaimMustSettleThroughObligation,
    #[msg("Insufficient free reserve capacity")]
    InsufficientFreeReserveCapacity,
    #[msg("Arithmetic overflow or underflow")]
    ArithmeticError,
    #[msg("Membership gate configuration is invalid")]
    MembershipGateConfigurationInvalid,
    #[msg("Membership proof mode does not match the configured plan posture")]
    MembershipProofModeMismatch,
    #[msg("Invite authority is missing or invalid for this plan")]
    MembershipInviteAuthorityInvalid,
    #[msg("Invite permit is expired")]
    MembershipInvitePermitExpired,
    #[msg("Bounded string field exceeds the canonical maximum")]
    StringTooLong,
    #[msg("Claim attestation decision is not a recognized value")]
    InvalidClaimAttestationDecision,
    #[msg("Claim attestation requires a locked evidence reference")]
    ClaimEvidenceRequired,
    #[msg("Claim attestation evidence reference does not match the claim case")]
    ClaimEvidenceMismatch,
    #[msg("Claim evidence cannot be changed after attestations begin")]
    ClaimEvidenceLocked,
    #[msg("Claim settlement recipient is locked after approval or payout")]
    ClaimRecipientLocked,
    #[msg("Health plan has paused oracle finality")]
    OracleFinalityHeld,
    #[msg("Fee vault initialization requires the matching domain asset vault to exist")]
    DomainAssetVaultRequired,
    #[msg("Linked claim settlement requires the member, mint, vault token, recipient token, and token program accounts")]
    SettlementOutflowAccountsRequired,
    #[msg("Stable coverage capacity is insufficient")]
    InsufficientStableCoverageCapacity,
    #[msg("Reserve asset role is invalid")]
    InvalidReserveAssetRole,
    #[msg("Reserve asset oracle source is invalid")]
    InvalidReserveOracleSource,
    #[msg("Reserve asset rail mismatch")]
    ReserveAssetRailMismatch,
    #[msg("Reserve domain mismatch")]
    ReserveDomainMismatch,
    #[msg("Reserve asset rail is inactive")]
    ReserveAssetRailInactive,
    #[msg("Reserve asset rail does not allow claims payout")]
    ReserveAssetRailPayoutDisabled,
    #[msg("Reserve asset rail cannot count toward claims capacity")]
    ReserveAssetRailCapacityDisabled,
    #[msg("Reserve asset oracle price is stale or missing")]
    ReserveAssetPriceStale,
    #[msg("Reserve asset oracle price is invalid")]
    ReserveAssetPriceInvalid,
    #[msg("Reserve asset oracle price confidence exceeds rail threshold")]
    ReserveAssetPriceConfidenceTooWide,
    #[msg("Partial obligation lifecycle transitions are not supported")]
    PartialObligationTransitionUnsupported,
    #[msg("Invalid obligation delivery mode")]
    InvalidObligationDeliveryMode,
    #[msg("Claim adjudication is locked after payout or terminal state")]
    ClaimAdjudicationLocked,
    #[msg("Health plan is inactive")]
    HealthPlanInactive,
    #[msg("Direct claim reserves require linked obligation settlement")]
    DirectClaimReserveUnsupported,
}

#[cfg(feature = "quasar")]
#[error_code]
pub enum OmegaXProtocolError {
    Unauthorized,
    ReserveDomainInactive,
    VaultTokenAccountInvalid,
    HealthPlanPaused,
    ClaimIntakePaused,
    InvalidBps,
    IdentifierTooLong,
    HealthPlanMismatch,
    PolicySeriesMismatch,
    PolicySeriesMissing,
    SeriesLedgerUnexpected,
    AssetMintMismatch,
    TokenAccountOwnerMismatch,
    TokenAccountSelfTransferInvalid,
    VaultTokenAccountMismatch,
    Token2022NotSupported,
    FundingLineMismatch,
    FundingLineTypeMismatch,
    ObligationMismatch,
    InvalidObligationStateTransition,
    AmountExceedsOutstandingObligation,
    AmountExceedsReservedBalance,
    AmountExceedsApprovedClaim,
    AmountMustBePositive,
    ClaimCaseLinkMismatch,
    LinkedClaimMustSettleThroughObligation,
    InsufficientFreeReserveCapacity,
    ArithmeticError,
    MembershipGateConfigurationInvalid,
    MembershipProofModeMismatch,
    MembershipInviteAuthorityInvalid,
    MembershipInvitePermitExpired,
    StringTooLong,
    InvalidClaimAttestationDecision,
    ClaimEvidenceRequired,
    ClaimEvidenceMismatch,
    ClaimEvidenceLocked,
    ClaimRecipientLocked,
    OracleFinalityHeld,
    DomainAssetVaultRequired,
    SettlementOutflowAccountsRequired,
    InsufficientStableCoverageCapacity,
    InvalidReserveAssetRole,
    InvalidReserveOracleSource,
    ReserveAssetRailMismatch,
    ReserveDomainMismatch,
    ReserveAssetRailInactive,
    ReserveAssetRailPayoutDisabled,
    ReserveAssetRailCapacityDisabled,
    ReserveAssetPriceStale,
    ReserveAssetPriceInvalid,
    ReserveAssetPriceConfidenceTooWide,
    PartialObligationTransitionUnsupported,
    InvalidObligationDeliveryMode,
    ClaimAdjudicationLocked,
    HealthPlanInactive,
    DirectClaimReserveUnsupported,
}
