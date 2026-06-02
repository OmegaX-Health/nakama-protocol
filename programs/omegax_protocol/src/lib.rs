// SPDX-License-Identifier: AGPL-3.0-or-later

//! Canonical OmegaX health capital markets program surface.

pub mod platform;

use crate::platform::*;

declare_id!("Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B");

pub mod args;
pub mod capital;
#[cfg(feature = "certora")]
pub mod certora;
pub mod claims;
pub mod constants;
pub mod errors;
pub mod events;
pub mod fees;
pub mod funding_obligations;
pub mod governance;
pub mod kernel;
pub mod oracle_schema;
pub mod plans_membership;
pub mod quasar_discriminators;
pub mod reserve_custody;
pub mod reserve_waterfall;
pub mod state;
pub mod types;

pub use args::*;
pub use capital::*;
pub use claims::*;
pub use constants::*;
pub use errors::*;
pub use events::*;
pub use fees::*;
pub use funding_obligations::*;
pub use governance::*;
#[cfg(test)]
pub(crate) use kernel::*;
pub use oracle_schema::*;
pub use plans_membership::*;
pub use reserve_custody::*;
pub use reserve_waterfall::*;
pub use state::*;
pub use types::*;

// Anchor derives these hidden client-account modules next to each `Accounts`
// context. Re-export them at crate root so Anchor `#[program]` sees the same
// names after moving the contexts into child modules.
#[cfg(not(feature = "quasar"))]
pub(crate) use capital::{
    __client_accounts_allocate_capital, __client_accounts_create_allocation_position,
    __client_accounts_create_capital_class, __client_accounts_create_liquidity_pool,
    __client_accounts_deallocate_capital, __client_accounts_deposit_into_capital_class,
    __client_accounts_mark_impairment, __client_accounts_process_redemption_queue,
    __client_accounts_request_redemption, __client_accounts_update_allocation_caps,
    __client_accounts_update_capital_class_controls,
    __client_accounts_update_lp_position_credentialing,
};
#[cfg(not(feature = "quasar"))]
pub(crate) use claims::__client_accounts_settle_claim_case_selected_asset;
#[cfg(not(feature = "quasar"))]
pub(crate) use funding_obligations::{
    __client_accounts_create_obligation, __client_accounts_fund_sponsor_budget,
    __client_accounts_open_funding_line, __client_accounts_record_premium_payment,
    __client_accounts_release_reserve, __client_accounts_reserve_obligation,
    __client_accounts_settle_obligation,
};
#[cfg(not(feature = "quasar"))]
pub(crate) use reserve_waterfall::{
    __client_accounts_configure_reserve_asset_rail,
    __client_accounts_publish_reserve_asset_rail_price,
};

#[cfg(not(feature = "quasar"))]
#[program]
pub mod omegax_protocol {
    use super::*;

    pub fn initialize_protocol_governance(
        ctx: Context<InitializeProtocolGovernance>,
        args: InitializeProtocolGovernanceArgs,
    ) -> Result<()> {
        crate::governance::initialize_protocol_governance(ctx, args)
    }

    pub fn set_protocol_emergency_pause(
        ctx: Context<SetProtocolEmergencyPause>,
        args: SetProtocolEmergencyPauseArgs,
    ) -> Result<()> {
        crate::governance::set_protocol_emergency_pause(ctx, args)
    }

    pub fn rotate_protocol_governance_authority(
        ctx: Context<RotateProtocolGovernanceAuthority>,
        args: RotateProtocolGovernanceAuthorityArgs,
    ) -> Result<()> {
        crate::governance::rotate_protocol_governance_authority(ctx, args)
    }

    pub fn accept_protocol_governance_authority(
        ctx: Context<AcceptProtocolGovernanceAuthority>,
    ) -> Result<()> {
        crate::governance::accept_protocol_governance_authority(ctx)
    }

    pub fn cancel_protocol_governance_authority_transfer(
        ctx: Context<CancelProtocolGovernanceAuthorityTransfer>,
    ) -> Result<()> {
        crate::governance::cancel_protocol_governance_authority_transfer(ctx)
    }

    pub fn create_reserve_domain(
        ctx: Context<CreateReserveDomain>,
        args: CreateReserveDomainArgs,
    ) -> Result<()> {
        crate::reserve_custody::create_reserve_domain(ctx, args)
    }

    pub fn update_reserve_domain_controls(
        ctx: Context<UpdateReserveDomainControls>,
        args: UpdateReserveDomainControlsArgs,
    ) -> Result<()> {
        crate::reserve_custody::update_reserve_domain_controls(ctx, args)
    }

    pub fn create_domain_asset_vault(
        ctx: Context<CreateDomainAssetVault>,
        args: CreateDomainAssetVaultArgs,
    ) -> Result<()> {
        crate::reserve_custody::create_domain_asset_vault(ctx, args)
    }

    pub fn configure_reserve_asset_rail(
        ctx: Context<ConfigureReserveAssetRail>,
        args: ConfigureReserveAssetRailArgs,
    ) -> Result<()> {
        crate::reserve_waterfall::configure_reserve_asset_rail(ctx, args)
    }

    pub fn publish_reserve_asset_rail_price(
        ctx: Context<PublishReserveAssetRailPrice>,
        args: PublishReserveAssetRailPriceArgs,
    ) -> Result<()> {
        crate::reserve_waterfall::publish_reserve_asset_rail_price(ctx, args)
    }

    /// Phase 1.6 — Initialize the protocol-fee vault for a (reserve_domain, asset_mint)
    /// rail. Governance-only; binds the rail to the asset mint at the program edge.
    /// Withdrawal authority is governance (PR2). Accrual is wired in PR1 hooks.
    pub fn init_protocol_fee_vault(
        ctx: Context<InitProtocolFeeVault>,
        args: InitProtocolFeeVaultArgs,
    ) -> Result<()> {
        crate::fees::init_protocol_fee_vault(ctx, args)
    }

    /// Phase 1.6 — Initialize the pool-treasury vault for a (liquidity_pool, asset_mint)
    /// rail. Governance-only init; pool-admin signs withdrawals (PR2).
    pub fn init_pool_treasury_vault(
        ctx: Context<InitPoolTreasuryVault>,
        args: InitPoolTreasuryVaultArgs,
    ) -> Result<()> {
        crate::fees::init_pool_treasury_vault(ctx, args)
    }

    /// Phase 1.6 — Initialize the pool-oracle fee vault for a (liquidity_pool,
    /// oracle, asset_mint) rail. Governance-only init; the registered oracle
    /// wallet (or oracle profile admin) signs withdrawals (PR2).
    pub fn init_pool_oracle_fee_vault(
        ctx: Context<InitPoolOracleFeeVault>,
        args: InitPoolOracleFeeVaultArgs,
    ) -> Result<()> {
        crate::fees::init_pool_oracle_fee_vault(ctx, args)
    }

    pub fn create_health_plan(
        ctx: Context<CreateHealthPlan>,
        args: CreateHealthPlanArgs,
    ) -> Result<()> {
        crate::plans_membership::create_health_plan(ctx, args)
    }

    pub fn update_health_plan_controls(
        ctx: Context<UpdateHealthPlanControls>,
        args: UpdateHealthPlanControlsArgs,
    ) -> Result<()> {
        crate::plans_membership::update_health_plan_controls(ctx, args)
    }

    pub fn create_policy_series(
        ctx: Context<CreatePolicySeries>,
        args: CreatePolicySeriesArgs,
    ) -> Result<()> {
        crate::plans_membership::create_policy_series(ctx, args)
    }

    pub fn initialize_series_reserve_ledger(
        ctx: Context<InitializeSeriesReserveLedger>,
        args: InitializeSeriesReserveLedgerArgs,
    ) -> Result<()> {
        crate::plans_membership::initialize_series_reserve_ledger(ctx, args)
    }

    pub fn version_policy_series(
        ctx: Context<VersionPolicySeries>,
        args: VersionPolicySeriesArgs,
    ) -> Result<()> {
        crate::plans_membership::version_policy_series(ctx, args)
    }

    pub fn open_member_position(
        ctx: Context<OpenMemberPosition>,
        args: OpenMemberPositionArgs,
    ) -> Result<()> {
        crate::plans_membership::open_member_position(ctx, args)
    }

    pub fn update_member_eligibility(
        ctx: Context<UpdateMemberEligibility>,
        args: UpdateMemberEligibilityArgs,
    ) -> Result<()> {
        crate::plans_membership::update_member_eligibility(ctx, args)
    }

    pub fn open_funding_line(
        ctx: Context<OpenFundingLine>,
        args: OpenFundingLineArgs,
    ) -> Result<()> {
        crate::funding_obligations::open_funding_line(ctx, args)
    }

    pub fn fund_sponsor_budget(
        ctx: Context<FundSponsorBudget>,
        args: FundSponsorBudgetArgs,
    ) -> Result<()> {
        crate::funding_obligations::fund_sponsor_budget(ctx, args)
    }

    pub fn record_premium_payment(
        ctx: Context<RecordPremiumPayment>,
        args: RecordPremiumPaymentArgs,
    ) -> Result<()> {
        crate::funding_obligations::record_premium_payment(ctx, args)
    }

    pub fn create_obligation(
        ctx: Context<CreateObligation>,
        args: CreateObligationArgs,
    ) -> Result<()> {
        crate::funding_obligations::create_obligation(ctx, args)
    }

    pub fn reserve_obligation(
        ctx: Context<ReserveObligation>,
        args: ReserveObligationArgs,
    ) -> Result<()> {
        crate::funding_obligations::reserve_obligation(ctx, args)
    }

    pub fn settle_obligation(
        ctx: Context<SettleObligation>,
        args: SettleObligationArgs,
    ) -> Result<()> {
        crate::funding_obligations::settle_obligation(ctx, args)
    }

    pub fn release_reserve(ctx: Context<ReleaseReserve>, args: ReleaseReserveArgs) -> Result<()> {
        crate::funding_obligations::release_reserve(ctx, args)
    }

    pub fn open_claim_case(ctx: Context<OpenClaimCase>, args: OpenClaimCaseArgs) -> Result<()> {
        crate::claims::open_claim_case(ctx, args)
    }

    pub fn authorize_claim_recipient(
        ctx: Context<AuthorizeClaimRecipient>,
        args: AuthorizeClaimRecipientArgs,
    ) -> Result<()> {
        crate::claims::authorize_claim_recipient(ctx, args)
    }

    pub fn attach_claim_evidence_ref(
        ctx: Context<AttachClaimEvidenceRef>,
        args: AttachClaimEvidenceRefArgs,
    ) -> Result<()> {
        crate::claims::attach_claim_evidence_ref(ctx, args)
    }

    pub fn adjudicate_claim_case(
        ctx: Context<AdjudicateClaimCase>,
        args: AdjudicateClaimCaseArgs,
    ) -> Result<()> {
        crate::claims::adjudicate_claim_case(ctx, args)
    }

    pub fn settle_claim_case(
        ctx: Context<SettleClaimCase>,
        args: SettleClaimCaseArgs,
    ) -> Result<()> {
        crate::claims::settle_claim_case(ctx, args)
    }

    pub fn settle_claim_case_selected_asset(
        ctx: Context<SettleClaimCaseSelectedAsset>,
        args: SettleClaimCaseSelectedAssetArgs,
    ) -> Result<()> {
        crate::claims::settle_claim_case_selected_asset(ctx, args)
    }

    pub fn create_liquidity_pool(
        ctx: Context<CreateLiquidityPool>,
        args: CreateLiquidityPoolArgs,
    ) -> Result<()> {
        crate::capital::create_liquidity_pool(ctx, args)
    }

    pub fn create_capital_class(
        ctx: Context<CreateCapitalClass>,
        args: CreateCapitalClassArgs,
    ) -> Result<()> {
        crate::capital::create_capital_class(ctx, args)
    }

    pub fn update_capital_class_controls(
        ctx: Context<UpdateCapitalClassControls>,
        args: UpdateCapitalClassControlsArgs,
    ) -> Result<()> {
        crate::capital::update_capital_class_controls(ctx, args)
    }

    pub fn update_lp_position_credentialing(
        ctx: Context<UpdateLpPositionCredentialing>,
        args: UpdateLpPositionCredentialingArgs,
    ) -> Result<()> {
        crate::capital::update_lp_position_credentialing(ctx, args)
    }

    pub fn deposit_into_capital_class(
        ctx: Context<DepositIntoCapitalClass>,
        args: DepositIntoCapitalClassArgs,
    ) -> Result<()> {
        crate::capital::deposit_into_capital_class(ctx, args)
    }

    pub fn request_redemption(
        ctx: Context<RequestRedemption>,
        args: RequestRedemptionArgs,
    ) -> Result<()> {
        crate::capital::request_redemption(ctx, args)
    }

    pub fn process_redemption_queue(
        ctx: Context<ProcessRedemptionQueue>,
        args: ProcessRedemptionQueueArgs,
    ) -> Result<()> {
        crate::capital::process_redemption_queue(ctx, args)
    }

    /// Sweep accrued protocol fees (SPL rail) to a recipient ATA.
    /// Authority: governance only. Fees physically reside in the matching
    /// DomainAssetVault.vault_token_account; the CPI is PDA-signed via
    /// transfer_from_domain_vault.
    pub fn withdraw_protocol_fee_spl(
        ctx: Context<WithdrawProtocolFeeSpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_protocol_fee_spl(ctx, args)
    }

    /// Sweep accrued protocol fees (SOL rail) to a recipient system account.
    /// Authority: governance only. Lamports come straight off the fee-vault
    /// PDA; rent-exempt minimum is preserved.
    pub fn withdraw_protocol_fee_sol(
        ctx: Context<WithdrawProtocolFeeSol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_protocol_fee_sol(ctx, args)
    }

    /// Sweep accrued pool-treasury fees (SPL rail).
    /// Authority: pool curator OR governance.
    pub fn withdraw_pool_treasury_spl(
        ctx: Context<WithdrawPoolTreasurySpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_pool_treasury_spl(ctx, args)
    }

    /// Sweep accrued pool-treasury fees (SOL rail).
    /// Authority: pool curator OR governance.
    pub fn withdraw_pool_treasury_sol(
        ctx: Context<WithdrawPoolTreasurySol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_pool_treasury_sol(ctx, args)
    }

    /// Sweep accrued pool-oracle fees (SPL rail) to a recipient ATA.
    /// Authority: registered oracle wallet OR oracle profile admin OR governance.
    pub fn withdraw_pool_oracle_fee_spl(
        ctx: Context<WithdrawPoolOracleFeeSpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_pool_oracle_fee_spl(ctx, args)
    }

    /// Sweep accrued pool-oracle fees (SOL rail) to a recipient system account.
    /// Authority: registered oracle wallet OR oracle profile admin OR governance.
    pub fn withdraw_pool_oracle_fee_sol(
        ctx: Context<WithdrawPoolOracleFeeSol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        crate::fees::withdraw_pool_oracle_fee_sol(ctx, args)
    }

    pub fn create_allocation_position(
        ctx: Context<CreateAllocationPosition>,
        args: CreateAllocationPositionArgs,
    ) -> Result<()> {
        crate::capital::create_allocation_position(ctx, args)
    }

    pub fn update_allocation_caps(
        ctx: Context<UpdateAllocationCaps>,
        args: UpdateAllocationCapsArgs,
    ) -> Result<()> {
        crate::capital::update_allocation_caps(ctx, args)
    }

    pub fn allocate_capital(
        ctx: Context<AllocateCapital>,
        args: AllocateCapitalArgs,
    ) -> Result<()> {
        crate::capital::allocate_capital(ctx, args)
    }

    pub fn deallocate_capital(
        ctx: Context<DeallocateCapital>,
        args: DeallocateCapitalArgs,
    ) -> Result<()> {
        crate::capital::deallocate_capital(ctx, args)
    }

    pub fn mark_impairment(ctx: Context<MarkImpairment>, args: MarkImpairmentArgs) -> Result<()> {
        crate::capital::mark_impairment(ctx, args)
    }

    pub fn register_oracle(ctx: Context<RegisterOracle>, args: RegisterOracleArgs) -> Result<()> {
        crate::oracle_schema::register_oracle(ctx, args)
    }

    pub fn claim_oracle(ctx: Context<ClaimOracle>) -> Result<()> {
        crate::oracle_schema::claim_oracle(ctx)
    }

    pub fn update_oracle_profile(
        ctx: Context<UpdateOracleProfile>,
        args: UpdateOracleProfileArgs,
    ) -> Result<()> {
        crate::oracle_schema::update_oracle_profile(ctx, args)
    }

    pub fn set_pool_oracle(ctx: Context<SetPoolOracle>, args: SetPoolOracleArgs) -> Result<()> {
        crate::oracle_schema::set_pool_oracle(ctx, args)
    }

    pub fn set_pool_oracle_permissions(
        ctx: Context<SetPoolOraclePermissions>,
        args: SetPoolOraclePermissionsArgs,
    ) -> Result<()> {
        crate::oracle_schema::set_pool_oracle_permissions(ctx, args)
    }

    pub fn set_pool_oracle_policy(
        ctx: Context<SetPoolOraclePolicy>,
        args: SetPoolOraclePolicyArgs,
    ) -> Result<()> {
        crate::oracle_schema::set_pool_oracle_policy(ctx, args)
    }

    pub fn register_outcome_schema(
        ctx: Context<RegisterOutcomeSchema>,
        args: RegisterOutcomeSchemaArgs,
    ) -> Result<()> {
        crate::oracle_schema::register_outcome_schema(ctx, args)
    }

    pub fn verify_outcome_schema(
        ctx: Context<VerifyOutcomeSchema>,
        args: VerifyOutcomeSchemaArgs,
    ) -> Result<()> {
        crate::oracle_schema::verify_outcome_schema(ctx, args)
    }

    pub fn backfill_schema_dependency_ledger(
        ctx: Context<BackfillSchemaDependencyLedger>,
        args: BackfillSchemaDependencyLedgerArgs,
    ) -> Result<()> {
        crate::oracle_schema::backfill_schema_dependency_ledger(ctx, args)
    }

    pub fn close_outcome_schema(ctx: Context<CloseOutcomeSchema>) -> Result<()> {
        crate::oracle_schema::close_outcome_schema(ctx)
    }

    pub fn attest_claim_case(
        ctx: Context<AttestClaimCase>,
        args: AttestClaimCaseArgs,
    ) -> Result<()> {
        crate::claims::attest_claim_case(ctx, args)
    }
}

#[cfg(feature = "quasar")]
#[program]
pub mod omegax_protocol {
    use super::*;
    #[inline(always)]
    fn quasar_handler_port_pending() -> Result<()> {
        Err(ProgramError::InvalidInstructionData)
    }

    #[instruction(discriminator = [220, 188, 231, 198, 20, 71, 42, 123])]
    pub fn initialize_protocol_governance(
        ctx: Ctx<InitializeProtocolGovernance>,
        args: InitializeProtocolGovernanceArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [180, 209, 92, 144, 227, 14, 97, 94])]
    pub fn set_protocol_emergency_pause(
        ctx: Ctx<SetProtocolEmergencyPause>,
        args: SetProtocolEmergencyPauseArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [173, 25, 179, 236, 198, 190, 207, 98])]
    pub fn rotate_protocol_governance_authority(
        ctx: Ctx<RotateProtocolGovernanceAuthority>,
        args: RotateProtocolGovernanceAuthorityArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [202, 235, 28, 119, 167, 24, 81, 85])]
    pub fn accept_protocol_governance_authority(
        ctx: Ctx<AcceptProtocolGovernanceAuthority>,
    ) -> Result<()> {
        let _ = &ctx;
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [113, 25, 246, 12, 38, 35, 223, 114])]
    pub fn cancel_protocol_governance_authority_transfer(
        ctx: Ctx<CancelProtocolGovernanceAuthorityTransfer>,
    ) -> Result<()> {
        let _ = &ctx;
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [222, 2, 8, 218, 45, 157, 193, 246])]
    pub fn create_reserve_domain(
        ctx: Ctx<CreateReserveDomain>,
        args: CreateReserveDomainArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [3, 60, 38, 233, 198, 167, 116, 197])]
    pub fn update_reserve_domain_controls(
        ctx: Ctx<UpdateReserveDomainControls>,
        args: UpdateReserveDomainControlsArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [31, 13, 112, 128, 23, 164, 26, 108])]
    pub fn create_domain_asset_vault(
        ctx: Ctx<CreateDomainAssetVault>,
        args: CreateDomainAssetVaultArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [78, 48, 108, 190, 181, 203, 194, 176])]
    pub fn configure_reserve_asset_rail(
        ctx: Ctx<ConfigureReserveAssetRail>,
        args: ConfigureReserveAssetRailArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [132, 35, 143, 147, 59, 80, 162, 117])]
    pub fn publish_reserve_asset_rail_price(
        ctx: Ctx<PublishReserveAssetRailPrice>,
        args: PublishReserveAssetRailPriceArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [212, 235, 61, 42, 96, 183, 225, 57])]
    pub fn init_protocol_fee_vault(
        ctx: Ctx<InitProtocolFeeVault>,
        args: InitProtocolFeeVaultArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [96, 169, 51, 224, 0, 207, 141, 47])]
    pub fn init_pool_treasury_vault(
        ctx: Ctx<InitPoolTreasuryVault>,
        args: InitPoolTreasuryVaultArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [68, 122, 148, 84, 91, 98, 198, 167])]
    pub fn init_pool_oracle_fee_vault(
        ctx: Ctx<InitPoolOracleFeeVault>,
        args: InitPoolOracleFeeVaultArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [136, 7, 197, 134, 241, 206, 83, 171])]
    pub fn create_health_plan(
        ctx: Ctx<CreateHealthPlan>,
        args: CreateHealthPlanArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [108, 11, 28, 140, 226, 164, 239, 113])]
    pub fn update_health_plan_controls(
        ctx: Ctx<UpdateHealthPlanControls>,
        args: UpdateHealthPlanControlsArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [70, 162, 231, 218, 211, 136, 110, 176])]
    pub fn create_policy_series(
        ctx: Ctx<CreatePolicySeries>,
        args: CreatePolicySeriesArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [113, 155, 191, 126, 81, 152, 220, 249])]
    pub fn initialize_series_reserve_ledger(
        ctx: Ctx<InitializeSeriesReserveLedger>,
        args: InitializeSeriesReserveLedgerArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [64, 76, 132, 253, 41, 220, 169, 146])]
    pub fn version_policy_series(
        ctx: Ctx<VersionPolicySeries>,
        args: VersionPolicySeriesArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [161, 42, 115, 196, 30, 87, 104, 236])]
    pub fn open_member_position(
        ctx: Ctx<OpenMemberPosition>,
        args: OpenMemberPositionArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [254, 66, 68, 244, 98, 157, 111, 191])]
    pub fn update_member_eligibility(
        ctx: Ctx<UpdateMemberEligibility>,
        args: UpdateMemberEligibilityArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [231, 140, 66, 127, 163, 1, 197, 9])]
    pub fn open_funding_line(ctx: Ctx<OpenFundingLine>, args: OpenFundingLineArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [150, 210, 161, 31, 50, 12, 224, 32])]
    pub fn fund_sponsor_budget(
        ctx: Ctx<FundSponsorBudget>,
        args: FundSponsorBudgetArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [196, 182, 182, 56, 146, 87, 170, 29])]
    pub fn record_premium_payment(
        ctx: Ctx<RecordPremiumPayment>,
        args: RecordPremiumPaymentArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [216, 144, 172, 223, 19, 106, 220, 54])]
    pub fn create_obligation(ctx: Ctx<CreateObligation>, args: CreateObligationArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [48, 113, 133, 225, 40, 36, 197, 86])]
    pub fn reserve_obligation(
        ctx: Ctx<ReserveObligation>,
        args: ReserveObligationArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [209, 166, 218, 35, 147, 139, 238, 208])]
    pub fn settle_obligation(ctx: Ctx<SettleObligation>, args: SettleObligationArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [170, 102, 52, 144, 33, 176, 41, 60])]
    pub fn release_reserve(ctx: Ctx<ReleaseReserve>, args: ReleaseReserveArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [151, 125, 231, 211, 63, 132, 248, 184])]
    pub fn open_claim_case(ctx: Ctx<OpenClaimCase>, args: OpenClaimCaseArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [112, 97, 129, 42, 125, 165, 226, 163])]
    pub fn authorize_claim_recipient(
        ctx: Ctx<AuthorizeClaimRecipient>,
        args: AuthorizeClaimRecipientArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [52, 246, 203, 87, 244, 143, 132, 131])]
    pub fn attach_claim_evidence_ref(
        ctx: Ctx<AttachClaimEvidenceRef>,
        args: AttachClaimEvidenceRefArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [146, 99, 255, 26, 223, 88, 235, 114])]
    pub fn adjudicate_claim_case(
        ctx: Ctx<AdjudicateClaimCase>,
        args: AdjudicateClaimCaseArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [178, 123, 229, 204, 50, 204, 91, 71])]
    pub fn settle_claim_case(ctx: Ctx<SettleClaimCase>, args: SettleClaimCaseArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [21, 218, 248, 73, 41, 97, 47, 212])]
    pub fn settle_claim_case_selected_asset(
        ctx: Ctx<SettleClaimCaseSelectedAsset>,
        args: SettleClaimCaseSelectedAssetArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [175, 75, 181, 165, 224, 254, 6, 131])]
    pub fn create_liquidity_pool(
        ctx: Ctx<CreateLiquidityPool>,
        args: CreateLiquidityPoolArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [0, 161, 244, 112, 151, 137, 35, 221])]
    pub fn create_capital_class(
        ctx: Ctx<CreateCapitalClass>,
        args: CreateCapitalClassArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [34, 4, 113, 70, 79, 197, 244, 109])]
    pub fn update_capital_class_controls(
        ctx: Ctx<UpdateCapitalClassControls>,
        args: UpdateCapitalClassControlsArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [54, 194, 211, 94, 197, 61, 228, 202])]
    pub fn update_lp_position_credentialing(
        ctx: Ctx<UpdateLpPositionCredentialing>,
        args: UpdateLpPositionCredentialingArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [40, 215, 33, 115, 185, 101, 196, 167])]
    pub fn deposit_into_capital_class(
        ctx: Ctx<DepositIntoCapitalClass>,
        args: DepositIntoCapitalClassArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [14, 62, 182, 237, 59, 79, 149, 22])]
    pub fn request_redemption(
        ctx: Ctx<RequestRedemption>,
        args: RequestRedemptionArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [244, 120, 208, 73, 216, 200, 158, 93])]
    pub fn process_redemption_queue(
        ctx: Ctx<ProcessRedemptionQueue>,
        args: ProcessRedemptionQueueArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [120, 62, 236, 14, 227, 240, 52, 253])]
    pub fn withdraw_protocol_fee_spl(
        ctx: Ctx<WithdrawProtocolFeeSpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [193, 33, 140, 185, 45, 190, 112, 7])]
    pub fn withdraw_protocol_fee_sol(
        ctx: Ctx<WithdrawProtocolFeeSol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [43, 146, 116, 123, 106, 69, 242, 104])]
    pub fn withdraw_pool_treasury_spl(
        ctx: Ctx<WithdrawPoolTreasurySpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [50, 115, 51, 120, 221, 37, 200, 169])]
    pub fn withdraw_pool_treasury_sol(
        ctx: Ctx<WithdrawPoolTreasurySol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [242, 75, 247, 122, 255, 183, 48, 189])]
    pub fn withdraw_pool_oracle_fee_spl(
        ctx: Ctx<WithdrawPoolOracleFeeSpl>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [208, 223, 250, 62, 199, 8, 221, 185])]
    pub fn withdraw_pool_oracle_fee_sol(
        ctx: Ctx<WithdrawPoolOracleFeeSol>,
        args: WithdrawArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [165, 80, 76, 13, 12, 202, 112, 31])]
    pub fn create_allocation_position(
        ctx: Ctx<CreateAllocationPosition>,
        args: CreateAllocationPositionArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [224, 101, 103, 146, 78, 5, 48, 132])]
    pub fn update_allocation_caps(
        ctx: Ctx<UpdateAllocationCaps>,
        args: UpdateAllocationCapsArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [146, 129, 60, 205, 88, 225, 60, 183])]
    pub fn allocate_capital(ctx: Ctx<AllocateCapital>, args: AllocateCapitalArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [10, 97, 97, 189, 60, 170, 102, 29])]
    pub fn deallocate_capital(
        ctx: Ctx<DeallocateCapital>,
        args: DeallocateCapitalArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [58, 97, 30, 157, 211, 45, 174, 238])]
    pub fn mark_impairment(ctx: Ctx<MarkImpairment>, args: MarkImpairmentArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [176, 200, 234, 37, 199, 129, 164, 111])]
    pub fn register_oracle(ctx: Ctx<RegisterOracle>, args: RegisterOracleArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [1, 252, 166, 132, 45, 24, 23, 233])]
    pub fn claim_oracle(ctx: Ctx<ClaimOracle>) -> Result<()> {
        let _ = &ctx;
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [175, 66, 157, 51, 96, 190, 163, 98])]
    pub fn update_oracle_profile(
        ctx: Ctx<UpdateOracleProfile>,
        args: UpdateOracleProfileArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [140, 225, 146, 45, 210, 81, 225, 223])]
    pub fn set_pool_oracle(ctx: Ctx<SetPoolOracle>, args: SetPoolOracleArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [168, 14, 22, 106, 118, 145, 105, 44])]
    pub fn set_pool_oracle_permissions(
        ctx: Ctx<SetPoolOraclePermissions>,
        args: SetPoolOraclePermissionsArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [190, 13, 51, 113, 230, 140, 103, 82])]
    pub fn set_pool_oracle_policy(
        ctx: Ctx<SetPoolOraclePolicy>,
        args: SetPoolOraclePolicyArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [187, 68, 109, 211, 168, 181, 105, 32])]
    pub fn register_outcome_schema(
        ctx: Ctx<RegisterOutcomeSchema>,
        args: RegisterOutcomeSchemaArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [221, 10, 144, 137, 106, 214, 205, 170])]
    pub fn verify_outcome_schema(
        ctx: Ctx<VerifyOutcomeSchema>,
        args: VerifyOutcomeSchemaArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [109, 109, 247, 151, 229, 78, 52, 167])]
    pub fn backfill_schema_dependency_ledger(
        ctx: Ctx<BackfillSchemaDependencyLedger>,
        args: BackfillSchemaDependencyLedgerArgs,
    ) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [196, 81, 8, 61, 95, 145, 225, 2])]
    pub fn close_outcome_schema(ctx: Ctx<CloseOutcomeSchema>) -> Result<()> {
        let _ = &ctx;
        quasar_handler_port_pending()
    }

    #[instruction(discriminator = [111, 40, 46, 51, 76, 157, 214, 136])]
    pub fn attest_claim_case(ctx: Ctx<AttestClaimCase>, args: AttestClaimCaseArgs) -> Result<()> {
        let _ = (&ctx, &args);
        quasar_handler_port_pending()
    }
}

#[cfg(test)]
mod tests;
