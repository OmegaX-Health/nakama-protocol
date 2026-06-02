// SPDX-License-Identifier: AGPL-3.0-or-later

//! Impairment instruction handlers and account validation contexts.

use super::*;

#[cfg(not(feature = "quasar"))]
pub(crate) fn mark_impairment(
    ctx: Context<MarkImpairment>,
    args: MarkImpairmentArgs,
) -> Result<()> {
    require_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    require_claim_operator(
        &ctx.accounts.authority.key(),
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require_positive_amount(args.amount)?;
    validate_impairment_bindings(
        ctx.accounts.series_reserve_ledger.as_deref(),
        ctx.accounts.pool_class_ledger.as_deref(),
        ctx.accounts.allocation_position.as_deref(),
        ctx.accounts.allocation_ledger.as_deref(),
        ctx.accounts.obligation.as_deref(),
        ctx.accounts.funding_line.key(),
        &ctx.accounts.funding_line,
    )?;

    let amount = args.amount;
    book_impairment(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_impairment(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_impairment(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_deref_mut() {
        book_impairment(&mut series_ledger.sheet, amount)?;
    }
    if let Some(pool_class_ledger) = ctx.accounts.pool_class_ledger.as_deref_mut() {
        book_impairment(&mut pool_class_ledger.sheet, amount)?;
        pool_class_ledger.realized_loss_amount =
            checked_add(pool_class_ledger.realized_loss_amount, amount)?;
    }
    if let Some(allocation_position) = ctx.accounts.allocation_position.as_deref_mut() {
        allocation_position.impaired_amount =
            checked_add(allocation_position.impaired_amount, amount)?;
        allocation_position.realized_pnl =
            debit_realized_pnl_for_loss(allocation_position.realized_pnl, amount)?;
    }
    if let Some(allocation_ledger) = ctx.accounts.allocation_ledger.as_deref_mut() {
        book_impairment(&mut allocation_ledger.sheet, amount)?;
        allocation_ledger.realized_pnl =
            debit_realized_pnl_for_loss(allocation_ledger.realized_pnl, amount)?;
    }
    if let Some(obligation) = ctx.accounts.obligation.as_deref_mut() {
        obligation.status = OBLIGATION_STATUS_IMPAIRED;
        obligation.impaired_amount = checked_add(obligation.impaired_amount, amount)?;
        obligation.updated_at = Clock::get()?.unix_timestamp;
    }

    ctx.accounts.funding_line.released_amount =
        checked_add(ctx.accounts.funding_line.released_amount, amount)?;

    emit!(ImpairmentRecordedEvent {
        funding_line: ctx.accounts.funding_line.key(),
        obligation: ctx
            .accounts
            .obligation
            .as_ref()
            .map(|obligation| obligation.key())
            .unwrap_or(ZERO_PUBKEY),
        amount,
        reason_hash: args.reason_hash,
    });

    Ok(())
}

#[derive(Accounts)]
pub struct MarkImpairment<'info> {
    #[cfg(not(feature = "quasar"))]
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
    #[account(mut, seeds = [SEED_DOMAIN_ASSET_LEDGER, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()], bump = domain_asset_ledger.bump)]
    pub domain_asset_ledger: Box<Account<'info, DomainAssetLedger>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            domain_asset_ledger.address(),
            &crate::ID,
            &[SEED_DOMAIN_ASSET_LEDGER, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()],
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
    #[account(mut, seeds = [SEED_PLAN_RESERVE_LEDGER, health_plan.key().as_ref(), funding_line.asset_mint.as_ref()], bump = plan_reserve_ledger.bump)]
    pub plan_reserve_ledger: Box<Account<'info, PlanReserveLedger>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            plan_reserve_ledger.address(),
            &crate::ID,
            &[SEED_PLAN_RESERVE_LEDGER, health_plan.address().as_ref(), funding_line.asset_mint.as_ref()],
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
    #[account(mut)]
    pub pool_class_ledger: Option<Box<Account<'info, PoolClassLedger>>>,
    #[cfg(feature = "quasar")]
    pub pool_class_ledger: Option<&'info mut Account<PoolClassLedger>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub allocation_position: Option<Box<Account<'info, AllocationPosition>>>,
    #[cfg(feature = "quasar")]
    pub allocation_position: Option<&'info mut Account<AllocationPosition>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub allocation_ledger: Option<Box<Account<'info, AllocationLedger>>>,
    #[cfg(feature = "quasar")]
    pub allocation_ledger: Option<&'info mut Account<AllocationLedger>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub obligation: Option<Box<Account<'info, Obligation>>>,
    #[cfg(feature = "quasar")]
    pub obligation: Option<Account<ObligationAccountData<'info>>>,
}
