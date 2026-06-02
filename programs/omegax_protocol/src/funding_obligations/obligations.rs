// SPDX-License-Identifier: AGPL-3.0-or-later

//! Obligation creation instruction handlers and account validation contexts.

use super::*;

#[cfg(not(feature = "quasar"))]
pub(crate) fn create_obligation(
    ctx: Context<CreateObligation>,
    args: CreateObligationArgs,
) -> Result<()> {
    require_id(&args.obligation_id)?;
    require_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    require_plan_control(
        &ctx.accounts.authority.key(),
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require!(
        ctx.accounts.funding_line.health_plan == ctx.accounts.health_plan.key(),
        OmegaXProtocolError::HealthPlanMismatch
    );
    require!(
        ctx.accounts.funding_line.asset_mint == args.asset_mint,
        OmegaXProtocolError::AssetMintMismatch
    );
    require_keys_eq!(
        ctx.accounts.funding_line.policy_series,
        args.policy_series,
        OmegaXProtocolError::PolicySeriesMismatch
    );
    require_positive_amount(args.amount)?;
    validate_optional_series_ledger(
        ctx.accounts.series_reserve_ledger.as_deref(),
        args.policy_series,
        args.asset_mint,
    )?;
    validate_obligation_creation_scope(
        ctx.accounts.liquidity_pool.as_deref(),
        ctx.accounts.capital_class.as_deref(),
        ctx.accounts.allocation_position.as_deref(),
        ctx.accounts.pool_class_ledger.as_deref(),
        ctx.accounts.allocation_ledger.as_deref(),
        &ctx.accounts.health_plan,
        ctx.accounts.funding_line.key(),
        &ctx.accounts.funding_line,
        args.liquidity_pool,
        args.capital_class,
        args.allocation_position,
    )?;
    require_supported_obligation_delivery_mode(args.delivery_mode)?;

    let obligation = &mut ctx.accounts.obligation;
    obligation.reserve_domain = ctx.accounts.health_plan.reserve_domain;
    obligation.asset_mint = args.asset_mint;
    obligation.health_plan = ctx.accounts.health_plan.key();
    obligation.policy_series = args.policy_series;
    obligation.member_wallet = args.member_wallet;
    obligation.beneficiary = args.beneficiary;
    obligation.funding_line = ctx.accounts.funding_line.key();
    obligation.claim_case = args.claim_case;
    obligation.liquidity_pool = args.liquidity_pool;
    obligation.capital_class = args.capital_class;
    obligation.allocation_position = args.allocation_position;
    obligation.obligation_id = args.obligation_id;
    obligation.creation_reason_hash = args.creation_reason_hash;
    obligation.settlement_reason_hash = [0u8; 32];
    obligation.status = OBLIGATION_STATUS_PROPOSED;
    obligation.delivery_mode = args.delivery_mode;
    obligation.principal_amount = args.amount;
    obligation.outstanding_amount = args.amount;
    obligation.reserved_amount = 0;
    obligation.claimable_amount = 0;
    obligation.payable_amount = 0;
    obligation.settled_amount = 0;
    obligation.impaired_amount = 0;
    obligation.recovered_amount = 0;
    obligation.created_at = Clock::get()?.unix_timestamp;
    obligation.updated_at = obligation.created_at;
    obligation.bump = ctx.bumps.obligation;

    book_owed(&mut ctx.accounts.domain_asset_ledger.sheet, args.amount)?;
    book_owed(&mut ctx.accounts.plan_reserve_ledger.sheet, args.amount)?;
    book_owed(&mut ctx.accounts.funding_line_ledger.sheet, args.amount)?;

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_deref_mut() {
        book_owed(&mut series_ledger.sheet, args.amount)?;
    }

    if let Some(pool_class_ledger) = ctx.accounts.pool_class_ledger.as_deref_mut() {
        book_owed(&mut pool_class_ledger.sheet, args.amount)?;
    }

    if let Some(allocation_ledger) = ctx.accounts.allocation_ledger.as_deref_mut() {
        book_owed(&mut allocation_ledger.sheet, args.amount)?;
    }

    emit!(ObligationStatusChangedEvent {
        obligation: obligation.key(),
        funding_line: obligation.funding_line,
        status: obligation.status,
        amount: obligation.principal_amount,
    });

    Ok(())
}

#[derive(Accounts)]
#[cfg_attr(not(feature = "quasar"), instruction(args: CreateObligationArgs))]
#[cfg_attr(
    feature = "quasar",
    instruction(
        asset_mint: Pubkey,
        _policy_series_arg: Pubkey,
        _member_wallet: Pubkey,
        _beneficiary: Pubkey,
        _claim_case: Pubkey,
        _liquidity_pool_arg: Pubkey,
        _capital_class_arg: Pubkey,
        _allocation_position_arg: Pubkey,
        _delivery_mode: u8,
        _amount: u64,
        _creation_reason_hash: [u8; 32],
        obligation_id: String<u32, 32>
    )
)]
pub struct CreateObligation<'info> {
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub authority: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub authority: &'info Signer,
    #[cfg(not(feature = "quasar"))]
    #[account(seeds = [SEED_PROTOCOL_GOVERNANCE], bump = protocol_governance.bump)]
    pub protocol_governance: Box<Account<'info, ProtocolGovernance>>,
    #[cfg(feature = "quasar")]
    #[account(seeds = [SEED_PROTOCOL_GOVERNANCE], bump = protocol_governance.bump)]
    pub protocol_governance: &'info Account<ProtocolGovernance>,
    #[cfg(not(feature = "quasar"))]
    #[account(seeds = [SEED_HEALTH_PLAN, health_plan.reserve_domain.as_ref(), health_plan.health_plan_id.as_bytes()], bump = health_plan.bump)]
    pub health_plan: Box<Account<'info, HealthPlan>>,
    #[cfg(feature = "quasar")]
    #[account(
        constraint = quasar_pda_matches(
            health_plan.address(),
            &crate::ID,
            &[SEED_HEALTH_PLAN, health_plan.reserve_domain.as_ref(), health_plan.health_plan_id().as_bytes()],
            health_plan.bump,
        ) @ OmegaXProtocolError::HealthPlanMismatch
    )]
    pub health_plan: Account<HealthPlanAccountData<'info>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut, seeds = [SEED_DOMAIN_ASSET_LEDGER, health_plan.reserve_domain.as_ref(), args.asset_mint.as_ref()], bump = domain_asset_ledger.bump)]
    pub domain_asset_ledger: Box<Account<'info, DomainAssetLedger>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
            constraint = quasar_pda_matches(
                domain_asset_ledger.address(),
                &crate::ID,
                &[SEED_DOMAIN_ASSET_LEDGER, health_plan.reserve_domain.as_ref(), asset_mint.as_ref()],
                domain_asset_ledger.bump,
            ) @ OmegaXProtocolError::ReserveDomainMismatch
        )]
    pub domain_asset_ledger: &'info Account<DomainAssetLedger>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut, seeds = [SEED_FUNDING_LINE, health_plan.key().as_ref(), funding_line.line_id.as_bytes()], bump = funding_line.bump)]
    pub funding_line: Box<Account<'info, FundingLine>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            funding_line.address(),
            &crate::ID,
            &[SEED_FUNDING_LINE, health_plan.address().as_ref(), funding_line.line_id().as_bytes()],
            funding_line.bump,
        ) @ OmegaXProtocolError::FundingLineMismatch
    )]
    pub funding_line: Account<FundingLineAccountData<'info>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut, seeds = [SEED_FUNDING_LINE_LEDGER, funding_line.key().as_ref(), funding_line.asset_mint.as_ref()], bump = funding_line_ledger.bump)]
    pub funding_line_ledger: Box<Account<'info, FundingLineLedger>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            funding_line_ledger.address(),
            &crate::ID,
            &[SEED_FUNDING_LINE_LEDGER, funding_line.address().as_ref(), funding_line.asset_mint.as_ref()],
            funding_line_ledger.bump,
        ) @ OmegaXProtocolError::FundingLineMismatch
    )]
    pub funding_line_ledger: &'info Account<FundingLineLedger>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut, seeds = [SEED_PLAN_RESERVE_LEDGER, health_plan.key().as_ref(), args.asset_mint.as_ref()], bump = plan_reserve_ledger.bump)]
    pub plan_reserve_ledger: Box<Account<'info, PlanReserveLedger>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
            constraint = quasar_pda_matches(
                plan_reserve_ledger.address(),
                &crate::ID,
                &[SEED_PLAN_RESERVE_LEDGER, health_plan.address().as_ref(), asset_mint.as_ref()],
                plan_reserve_ledger.bump,
            ) @ OmegaXProtocolError::HealthPlanMismatch
        )]
    pub plan_reserve_ledger: &'info Account<PlanReserveLedger>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub series_reserve_ledger: Option<Box<Account<'info, SeriesReserveLedger>>>,
    #[cfg(feature = "quasar")]
    pub series_reserve_ledger: Option<&'info mut Account<SeriesReserveLedger>>,
    #[cfg(not(feature = "quasar"))]
    pub liquidity_pool: Option<Box<Account<'info, LiquidityPool>>>,
    #[cfg(feature = "quasar")]
    pub liquidity_pool: Option<Account<LiquidityPoolAccountData<'info>>>,
    #[cfg(not(feature = "quasar"))]
    pub capital_class: Option<Box<Account<'info, CapitalClass>>>,
    #[cfg(feature = "quasar")]
    pub capital_class: Option<Account<CapitalClassAccountData<'info>>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub pool_class_ledger: Option<Box<Account<'info, PoolClassLedger>>>,
    #[cfg(feature = "quasar")]
    pub pool_class_ledger: Option<&'info mut Account<PoolClassLedger>>,
    #[cfg(not(feature = "quasar"))]
    pub allocation_position: Option<Box<Account<'info, AllocationPosition>>>,
    #[cfg(feature = "quasar")]
    pub allocation_position: Option<&'info Account<AllocationPosition>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub allocation_ledger: Option<Box<Account<'info, AllocationLedger>>>,
    #[cfg(feature = "quasar")]
    pub allocation_ledger: Option<&'info mut Account<AllocationLedger>>,
    #[cfg_attr(
        not(feature = "quasar"),
        account(
            init,
            payer = authority,
            space = 8 + Obligation::INIT_SPACE,
            seeds = [SEED_OBLIGATION, funding_line.key().as_ref(), args.obligation_id.as_bytes()],
            bump
        )
    )]
    #[cfg(not(feature = "quasar"))]
    pub obligation: Box<Account<'info, Obligation>>,
    #[cfg_attr(
        feature = "quasar",
        account(
            mut,
            constraint = quasar_pda_matches(
                obligation.address(),
                &crate::ID,
                &[SEED_OBLIGATION, funding_line.address().as_ref(), obligation_id],
                obligation.bump,
            ) @ OmegaXProtocolError::ObligationMismatch
        )
    )]
    #[cfg(feature = "quasar")]
    pub obligation: Account<ObligationAccountData<'info>>,
    #[cfg(not(feature = "quasar"))]
    pub system_program: Program<'info, System>,
    #[cfg(feature = "quasar")]
    pub system_program: &'info Program<System>,
}
