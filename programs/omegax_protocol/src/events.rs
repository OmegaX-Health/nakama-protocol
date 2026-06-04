// SPDX-License-Identifier: AGPL-3.0-or-later

//! Public event types emitted by the protocol.

use crate::platform::*;

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ReserveDomainCreatedEvent {
    pub reserve_domain: Pubkey,
    pub domain_admin: Pubkey,
    pub settlement_mode: u8,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [138, 101, 116, 228, 188, 195, 89, 37]))]
pub struct ReserveDomainCreatedEvent {
    pub reserve_domain: Address,
    pub domain_admin: Address,
    pub settlement_mode: u8,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct HealthPlanCreatedEvent {
    pub reserve_domain: Pubkey,
    pub health_plan: Pubkey,
    pub sponsor: Pubkey,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [160, 200, 242, 77, 168, 222, 253, 22]))]
pub struct HealthPlanCreatedEvent {
    pub reserve_domain: Address,
    pub health_plan: Address,
    pub sponsor: Address,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct PolicySeriesCreatedEvent {
    pub health_plan: Pubkey,
    pub policy_series: Pubkey,
    pub asset_mint: Pubkey,
    pub mode: u8,
    pub terms_version: u16,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [106, 212, 178, 224, 202, 185, 17, 157]))]
pub struct PolicySeriesCreatedEvent {
    pub health_plan: Address,
    pub policy_series: Address,
    pub asset_mint: Address,
    pub mode: u8,
    pub terms_version: u16,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct PolicySeriesVersionedEvent {
    pub prior_series: Pubkey,
    pub next_series: Pubkey,
    pub new_terms_version: u16,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [37, 154, 96, 209, 46, 91, 162, 255]))]
pub struct PolicySeriesVersionedEvent {
    pub prior_series: Address,
    pub next_series: Address,
    pub new_terms_version: u16,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct FundingLineOpenedEvent {
    pub health_plan: Pubkey,
    pub funding_line: Pubkey,
    pub asset_mint: Pubkey,
    pub line_type: u8,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [47, 172, 14, 218, 139, 94, 10, 145]))]
pub struct FundingLineOpenedEvent {
    pub health_plan: Address,
    pub funding_line: Address,
    pub asset_mint: Address,
    pub line_type: u8,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct FundingFlowRecordedEvent {
    pub funding_line: Pubkey,
    pub amount: u64,
    pub flow_kind: u8,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [207, 159, 154, 43, 193, 239, 239, 163]))]
pub struct FundingFlowRecordedEvent {
    pub funding_line: Address,
    pub amount: u64,
    pub flow_kind: u8,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ReserveAssetRailConfiguredEvent {
    pub reserve_domain: Pubkey,
    pub reserve_asset_rail: Pubkey,
    pub asset_mint: Pubkey,
    pub role: u8,
    pub payout_priority: u8,
    pub oracle_source: u8,
    pub active: bool,
    pub reason_hash: [u8; 32],
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [33, 112, 220, 210, 144, 2, 40, 234]))]
pub struct ReserveAssetRailConfiguredEvent {
    pub reserve_domain: Address,
    pub reserve_asset_rail: Address,
    pub asset_mint: Address,
    pub role: u8,
    pub payout_priority: u8,
    pub oracle_source: u8,
    pub active: bool,
    pub reason_hash: Address,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ReserveAssetRailPricePublishedEvent {
    pub reserve_asset_rail: Pubkey,
    pub asset_mint: Pubkey,
    pub oracle_authority: Pubkey,
    pub price_usd_1e8: u64,
    pub confidence_bps: u16,
    pub published_at_ts: i64,
    pub proof_hash: [u8; 32],
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [161, 207, 64, 197, 138, 47, 213, 44]))]
pub struct ReserveAssetRailPricePublishedEvent {
    pub reserve_asset_rail: Address,
    pub asset_mint: Address,
    pub oracle_authority: Address,
    pub price_usd_1e8: u64,
    pub confidence_bps: u16,
    pub published_at_ts: i64,
    pub proof_hash: Address,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ObligationStatusChangedEvent {
    pub obligation: Pubkey,
    pub funding_line: Pubkey,
    pub status: u8,
    pub amount: u64,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [173, 116, 84, 221, 225, 109, 198, 74]))]
pub struct ObligationStatusChangedEvent {
    pub obligation: Address,
    pub funding_line: Address,
    pub status: u8,
    pub amount: u64,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ClaimCaseStateChangedEvent {
    pub claim_case: Pubkey,
    pub intake_status: u8,
    pub approved_amount: u64,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [162, 195, 160, 236, 219, 18, 240, 208]))]
pub struct ClaimCaseStateChangedEvent {
    pub claim_case: Address,
    pub intake_status: u8,
    pub approved_amount: u64,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ClaimCaseAttestedEvent {
    pub claim_attestation: Pubkey,
    pub claim_case: Pubkey,
    pub oracle: Pubkey,
    pub decision: u8,
    pub attestation_hash: [u8; 32],
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [27, 131, 74, 180, 134, 39, 214, 103]))]
pub struct ClaimCaseAttestedEvent {
    pub claim_attestation: Address,
    pub claim_case: Address,
    pub oracle: Address,
    pub decision: u8,
    pub attestation_hash: Address,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct ScopedControlChangedEvent {
    pub scope_kind: u8,
    pub scope: Pubkey,
    pub authority: Pubkey,
    pub pause_flags: u32,
    pub reason_hash: [u8; 32],
    pub audit_nonce: u64,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [103, 133, 3, 156, 72, 49, 119, 157]))]
pub struct ScopedControlChangedEvent {
    pub scope_kind: u8,
    pub scope: Address,
    pub authority: Address,
    pub pause_flags: u32,
    pub reason_hash: Address,
    pub audit_nonce: u64,
}

#[cfg(not(feature = "quasar"))]
#[event]
pub struct LedgerInitializedEvent {
    pub scope_kind: u8,
    pub scope: Pubkey,
    pub asset_mint: Pubkey,
}

#[cfg(feature = "quasar")]
#[cfg_attr(any(), event(discriminator = [155, 186, 165, 141, 70, 86, 207, 246]))]
pub struct LedgerInitializedEvent {
    pub scope_kind: u8,
    pub scope: Address,
    pub asset_mint: Address,
}
