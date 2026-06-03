// SPDX-License-Identifier: AGPL-3.0-or-later

//! Funding and premium inflow instruction handlers and account validation contexts.

use super::*;

#[cfg(not(feature = "quasar"))]
pub(crate) fn fund_sponsor_budget(
    ctx: Context<FundSponsorBudget>,
    args: FundSponsorBudgetArgs,
) -> Result<()> {
    require_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    require_plan_control(
        &ctx.accounts.authority.key(),
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require_positive_amount(args.amount)?;
    require!(
        ctx.accounts.funding_line.line_type == FUNDING_LINE_TYPE_SPONSOR_BUDGET,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    transfer_to_domain_vault(
        args.amount,
        &ctx.accounts.authority,
        &ctx.accounts.source_token_account,
        &ctx.accounts.asset_mint,
        &ctx.accounts.vault_token_account,
        &ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;
    validate_optional_series_ledger(
        ctx.accounts.series_reserve_ledger.as_deref(),
        ctx.accounts.funding_line.policy_series,
        ctx.accounts.funding_line.asset_mint,
    )?;

    let amount = args.amount;
    let funding_line = &mut ctx.accounts.funding_line;
    funding_line.funded_amount = checked_add(funding_line.funded_amount, amount)?;
    book_inflow(&mut ctx.accounts.domain_asset_vault.total_assets, amount)?;
    book_inflow_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_deref_mut() {
        book_inflow_sheet(&mut series_ledger.sheet, amount)?;
    }

    emit!(FundingFlowRecordedEvent {
        funding_line: funding_line.key(),
        amount,
        flow_kind: FundingFlowKind::SponsorBudgetFunded as u8,
    });

    Ok(())
}
#[cfg(not(feature = "quasar"))]
pub(crate) fn record_premium_payment(
    ctx: Context<RecordPremiumPayment>,
    args: RecordPremiumPaymentArgs,
) -> Result<()> {
    require_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    require_plan_control(
        &ctx.accounts.authority.key(),
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require_positive_amount(args.amount)?;
    require!(
        ctx.accounts.funding_line.line_type == FUNDING_LINE_TYPE_PREMIUM_INCOME,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    transfer_to_domain_vault(
        args.amount,
        &ctx.accounts.authority,
        &ctx.accounts.source_token_account,
        &ctx.accounts.asset_mint,
        &ctx.accounts.vault_token_account,
        &ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;
    validate_optional_series_ledger(
        ctx.accounts.series_reserve_ledger.as_deref(),
        ctx.accounts.funding_line.policy_series,
        ctx.accounts.funding_line.asset_mint,
    )?;

    let amount = args.amount;
    // Capture immutable values needed after the mutable borrow on funding_line
    // and during the protocol_fee_vault accrual block below.
    let funding_line_key = ctx.accounts.funding_line.key();
    let funding_line_asset_mint = ctx.accounts.funding_line.asset_mint;
    let health_plan_reserve_domain = ctx.accounts.health_plan.reserve_domain;
    let protocol_fee_bps = ctx.accounts.protocol_governance.protocol_fee_bps;
    let fee = fee_share_from_bps(amount, protocol_fee_bps)?;

    let funding_line = &mut ctx.accounts.funding_line;
    funding_line.funded_amount = checked_add(funding_line.funded_amount, amount)?;
    book_inflow(&mut ctx.accounts.domain_asset_vault.total_assets, amount)?;
    book_inflow_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_deref_mut() {
        book_inflow_sheet(&mut series_ledger.sheet, amount)?;
    }

    if fee > 0 {
        book_fee_accrual_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, fee)?;
        book_fee_accrual_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, fee)?;
        book_fee_accrual_sheet(&mut ctx.accounts.funding_line_ledger.sheet, fee)?;
        if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_deref_mut() {
            book_fee_accrual_sheet(&mut series_ledger.sheet, fee)?;
        }
    }

    // Phase 1.6 — Protocol fee accrual on premium income.
    // The full premium amount stays physically in the vault until withdrawal,
    // but the fee carve-out leaves reserve capacity at accrual time.
    let vault = &mut ctx.accounts.protocol_fee_vault;
    require_keys_eq!(
        vault.reserve_domain,
        health_plan_reserve_domain,
        OmegaXProtocolError::FeeVaultMismatch
    );
    require_keys_eq!(
        vault.asset_mint,
        funding_line_asset_mint,
        OmegaXProtocolError::FeeVaultMismatch
    );
    if fee > 0 {
        let vault_key = vault.key();
        let vault_mint = vault.asset_mint;
        let accrued_total = accrue_fee(&mut vault.accrued_fees, fee)?;
        emit!(FeeAccruedEvent {
            vault: vault_key,
            asset_mint: vault_mint,
            amount: fee,
            accrued_total,
        });
    }

    emit!(FundingFlowRecordedEvent {
        funding_line: funding_line_key,
        amount,
        flow_kind: FundingFlowKind::PremiumRecorded as u8,
    });

    Ok(())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn quasar_checked_add(lhs: u64, rhs: u64) -> Result<u64> {
    lhs.checked_add(rhs)
        .ok_or(OmegaXProtocolError::ArithmeticError.into())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn quasar_checked_sub(lhs: u64, rhs: u64) -> Result<u64> {
    lhs.checked_sub(rhs)
        .ok_or(OmegaXProtocolError::ArithmeticError.into())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn require_quasar_protocol_not_paused(governance: &ProtocolGovernance) -> Result<()> {
    require!(
        !governance.emergency_pause.get(),
        OmegaXProtocolError::ProtocolEmergencyPaused
    );
    Ok(())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn require_quasar_positive_amount(amount: u64) -> Result<()> {
    require!(amount > 0, OmegaXProtocolError::AmountMustBePositive);
    Ok(())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn require_quasar_plan_control(
    authority: &Pubkey,
    governance: &ProtocolGovernance,
    plan: &HealthPlanAccountData<'_>,
) -> Result<()> {
    if *authority == plan.plan_admin
        || *authority == plan.sponsor_operator
        || *authority == governance.governance_authority
    {
        Ok(())
    } else {
        err!(OmegaXProtocolError::Unauthorized)
    }
}

#[cfg(feature = "quasar")]
fn quasar_recompute_sheet(sheet: &mut ReserveBalanceSheet) -> Result<()> {
    let encumbered = sheet
        .reserved
        .checked_add(sheet.claimable)
        .and_then(|value| value.checked_add(sheet.payable))
        .and_then(|value| value.checked_add(sheet.impaired))
        .and_then(|value| value.checked_add(sheet.pending_redemption))
        .and_then(|value| value.checked_add(sheet.restricted))
        .ok_or(OmegaXProtocolError::ArithmeticError)?;
    sheet.free = sheet.funded.saturating_sub(encumbered);
    let redeemable_encumbered = encumbered
        .checked_add(sheet.allocated)
        .ok_or(OmegaXProtocolError::ArithmeticError)?;
    sheet.redeemable = sheet.funded.saturating_sub(redeemable_encumbered);
    Ok(())
}

#[cfg(feature = "quasar")]
fn quasar_book_inflow_sheet(sheet: &mut ReserveBalanceSheet, amount: u64) -> Result<()> {
    sheet.funded = quasar_checked_add(sheet.funded, amount)?;
    quasar_recompute_sheet(sheet)
}

#[cfg(feature = "quasar")]
fn quasar_book_fee_accrual_sheet(sheet: &mut ReserveBalanceSheet, amount: u64) -> Result<()> {
    if amount == 0 {
        return Ok(());
    }
    sheet.funded = quasar_checked_sub(sheet.funded, amount)?;
    quasar_recompute_sheet(sheet)
}

#[cfg(feature = "quasar")]
fn quasar_fee_share_from_bps(amount: u64, bps: u16) -> Result<u64> {
    if bps == 0 || amount == 0 {
        return Ok(0);
    }
    require!(
        bps <= BASIS_POINTS_DENOMINATOR,
        OmegaXProtocolError::FeeVaultBpsMisconfigured
    );
    let scaled = (amount as u128)
        .checked_mul(bps as u128)
        .ok_or(OmegaXProtocolError::ArithmeticError)?
        .checked_div(BASIS_POINTS_DENOMINATOR as u128)
        .ok_or(OmegaXProtocolError::ArithmeticError)?;
    let fee = u64::try_from(scaled).map_err(|_| OmegaXProtocolError::ArithmeticError)?;
    require!(fee <= amount, OmegaXProtocolError::ArithmeticError);
    Ok(fee)
}

#[cfg(feature = "quasar")]
fn quasar_accrue_fee(accrued: u64, amount: u64) -> Result<u64> {
    if amount == 0 {
        return Ok(accrued);
    }
    quasar_checked_add(accrued, amount)
}

#[cfg(feature = "quasar")]
fn validate_quasar_optional_series_ledger(
    series_ledger: Option<&Account<SeriesReserveLedger>>,
    expected_policy_series: Pubkey,
    expected_asset_mint: Pubkey,
) -> Result<()> {
    if let Some(ledger) = series_ledger {
        require!(
            expected_policy_series != ZERO_PUBKEY,
            OmegaXProtocolError::PolicySeriesMissing
        );
        require_keys_eq!(
            ledger.policy_series,
            expected_policy_series,
            OmegaXProtocolError::PolicySeriesMismatch
        );
        require_keys_eq!(
            ledger.asset_mint,
            expected_asset_mint,
            OmegaXProtocolError::AssetMintMismatch
        );
        require!(
            quasar_pda_matches(
                ledger.address(),
                &crate::ID,
                &[
                    SEED_SERIES_RESERVE_LEDGER,
                    expected_policy_series.as_ref(),
                    expected_asset_mint.as_ref(),
                ],
                ledger.bump,
            ),
            OmegaXProtocolError::PolicySeriesMismatch
        );
    }
    Ok(())
}

#[cfg(feature = "quasar")]
pub(crate) fn fund_sponsor_budget<'info>(
    ctx: &mut Ctx<'info, FundSponsorBudget<'info>>,
    amount: u64,
) -> Result<()> {
    require_quasar_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(
        &authority,
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require_quasar_positive_amount(amount)?;
    require!(
        ctx.accounts.funding_line.line_type == FUNDING_LINE_TYPE_SPONSOR_BUDGET,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    transfer_to_domain_vault(
        amount,
        ctx.accounts.authority,
        ctx.accounts.source_token_account,
        ctx.accounts.asset_mint,
        ctx.accounts.vault_token_account,
        ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;
    validate_quasar_optional_series_ledger(
        ctx.accounts
            .series_reserve_ledger
            .as_ref()
            .map(|ledger| &**ledger),
        ctx.accounts.funding_line.policy_series,
        ctx.accounts.funding_line.asset_mint,
    )?;

    let new_funded_amount =
        quasar_checked_add(ctx.accounts.funding_line.funded_amount.get(), amount)?;
    let new_total_assets =
        quasar_checked_add(ctx.accounts.domain_asset_vault.total_assets.get(), amount)?;
    let mut domain_sheet = ctx.accounts.domain_asset_ledger.sheet;
    let mut plan_sheet = ctx.accounts.plan_reserve_ledger.sheet;
    let mut funding_line_sheet = ctx.accounts.funding_line_ledger.sheet;
    quasar_book_inflow_sheet(&mut domain_sheet, amount)?;
    quasar_book_inflow_sheet(&mut plan_sheet, amount)?;
    quasar_book_inflow_sheet(&mut funding_line_sheet, amount)?;

    let vault = &mut ctx.accounts.domain_asset_vault;
    let reserve_domain = vault.reserve_domain;
    let asset_mint = vault.asset_mint;
    let vault_token_account = vault.vault_token_account;
    let bump = vault.bump;
    vault.set_inner(
        reserve_domain,
        asset_mint,
        vault_token_account,
        new_total_assets,
        bump,
    );

    let funding_line = &mut ctx.accounts.funding_line;
    let reserve_domain = funding_line.reserve_domain;
    let health_plan = funding_line.health_plan;
    let policy_series = funding_line.policy_series;
    let asset_mint = funding_line.asset_mint;
    let line_type = funding_line.line_type;
    let funding_priority = funding_line.funding_priority;
    let committed_amount = funding_line.committed_amount.get();
    let reserved_amount = funding_line.reserved_amount.get();
    let spent_amount = funding_line.spent_amount.get();
    let released_amount = funding_line.released_amount.get();
    let returned_amount = funding_line.returned_amount.get();
    let status = funding_line.status;
    let caps_hash = funding_line.caps_hash;
    let bump = funding_line.bump;
    let line_id = funding_line.line_id().to_owned();
    funding_line.set_inner(
        reserve_domain,
        health_plan,
        policy_series,
        asset_mint,
        line_type,
        funding_priority,
        committed_amount,
        new_funded_amount,
        reserved_amount,
        spent_amount,
        released_amount,
        returned_amount,
        status,
        caps_hash,
        bump,
        &line_id,
        ctx.accounts.authority.to_account_view(),
        None,
    )?;

    let domain_ledger = &mut ctx.accounts.domain_asset_ledger;
    let reserve_domain = domain_ledger.reserve_domain;
    let asset_mint = domain_ledger.asset_mint;
    let bump = domain_ledger.bump;
    domain_ledger.set_inner(reserve_domain, asset_mint, domain_sheet, bump);

    let plan_ledger = &mut ctx.accounts.plan_reserve_ledger;
    let health_plan = plan_ledger.health_plan;
    let asset_mint = plan_ledger.asset_mint;
    let bump = plan_ledger.bump;
    plan_ledger.set_inner(health_plan, asset_mint, plan_sheet, bump);

    let line_ledger = &mut ctx.accounts.funding_line_ledger;
    let funding_line = line_ledger.funding_line;
    let asset_mint = line_ledger.asset_mint;
    let bump = line_ledger.bump;
    line_ledger.set_inner(funding_line, asset_mint, funding_line_sheet, bump);

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_mut() {
        let series_ledger = &mut **series_ledger;
        let mut sheet = series_ledger.sheet;
        quasar_book_inflow_sheet(&mut sheet, amount)?;
        let policy_series = series_ledger.policy_series;
        let asset_mint = series_ledger.asset_mint;
        let bump = series_ledger.bump;
        series_ledger.set_inner(policy_series, asset_mint, sheet, bump);
    }

    Ok(())
}

#[cfg(feature = "quasar")]
pub(crate) fn record_premium_payment<'info>(
    ctx: &mut Ctx<'info, RecordPremiumPayment<'info>>,
    amount: u64,
) -> Result<()> {
    require_quasar_protocol_not_paused(&ctx.accounts.protocol_governance)?;
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(
        &authority,
        &ctx.accounts.protocol_governance,
        &ctx.accounts.health_plan,
    )?;
    require_quasar_positive_amount(amount)?;
    require!(
        ctx.accounts.funding_line.line_type == FUNDING_LINE_TYPE_PREMIUM_INCOME,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    transfer_to_domain_vault(
        amount,
        ctx.accounts.authority,
        ctx.accounts.source_token_account,
        ctx.accounts.asset_mint,
        ctx.accounts.vault_token_account,
        ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;
    validate_quasar_optional_series_ledger(
        ctx.accounts
            .series_reserve_ledger
            .as_ref()
            .map(|ledger| &**ledger),
        ctx.accounts.funding_line.policy_series,
        ctx.accounts.funding_line.asset_mint,
    )?;

    let funding_line_asset_mint = ctx.accounts.funding_line.asset_mint;
    let health_plan_reserve_domain = ctx.accounts.health_plan.reserve_domain;
    let fee = quasar_fee_share_from_bps(
        amount,
        ctx.accounts.protocol_governance.protocol_fee_bps.get(),
    )?;
    let new_funded_amount =
        quasar_checked_add(ctx.accounts.funding_line.funded_amount.get(), amount)?;
    let new_total_assets =
        quasar_checked_add(ctx.accounts.domain_asset_vault.total_assets.get(), amount)?;
    let mut domain_sheet = ctx.accounts.domain_asset_ledger.sheet;
    let mut plan_sheet = ctx.accounts.plan_reserve_ledger.sheet;
    let mut funding_line_sheet = ctx.accounts.funding_line_ledger.sheet;
    quasar_book_inflow_sheet(&mut domain_sheet, amount)?;
    quasar_book_inflow_sheet(&mut plan_sheet, amount)?;
    quasar_book_inflow_sheet(&mut funding_line_sheet, amount)?;
    if fee > 0 {
        quasar_book_fee_accrual_sheet(&mut domain_sheet, fee)?;
        quasar_book_fee_accrual_sheet(&mut plan_sheet, fee)?;
        quasar_book_fee_accrual_sheet(&mut funding_line_sheet, fee)?;
    }

    require_keys_eq!(
        ctx.accounts.protocol_fee_vault.reserve_domain,
        health_plan_reserve_domain,
        OmegaXProtocolError::FeeVaultMismatch
    );
    require_keys_eq!(
        ctx.accounts.protocol_fee_vault.asset_mint,
        funding_line_asset_mint,
        OmegaXProtocolError::FeeVaultMismatch
    );
    let new_accrued_fees =
        quasar_accrue_fee(ctx.accounts.protocol_fee_vault.accrued_fees.get(), fee)?;

    let domain_vault = &mut ctx.accounts.domain_asset_vault;
    let reserve_domain = domain_vault.reserve_domain;
    let asset_mint = domain_vault.asset_mint;
    let vault_token_account = domain_vault.vault_token_account;
    let bump = domain_vault.bump;
    domain_vault.set_inner(
        reserve_domain,
        asset_mint,
        vault_token_account,
        new_total_assets,
        bump,
    );

    let funding_line = &mut ctx.accounts.funding_line;
    let reserve_domain = funding_line.reserve_domain;
    let health_plan = funding_line.health_plan;
    let policy_series = funding_line.policy_series;
    let asset_mint = funding_line.asset_mint;
    let line_type = funding_line.line_type;
    let funding_priority = funding_line.funding_priority;
    let committed_amount = funding_line.committed_amount.get();
    let reserved_amount = funding_line.reserved_amount.get();
    let spent_amount = funding_line.spent_amount.get();
    let released_amount = funding_line.released_amount.get();
    let returned_amount = funding_line.returned_amount.get();
    let status = funding_line.status;
    let caps_hash = funding_line.caps_hash;
    let bump = funding_line.bump;
    let line_id = funding_line.line_id().to_owned();
    funding_line.set_inner(
        reserve_domain,
        health_plan,
        policy_series,
        asset_mint,
        line_type,
        funding_priority,
        committed_amount,
        new_funded_amount,
        reserved_amount,
        spent_amount,
        released_amount,
        returned_amount,
        status,
        caps_hash,
        bump,
        &line_id,
        ctx.accounts.authority.to_account_view(),
        None,
    )?;

    let domain_ledger = &mut ctx.accounts.domain_asset_ledger;
    let reserve_domain = domain_ledger.reserve_domain;
    let asset_mint = domain_ledger.asset_mint;
    let bump = domain_ledger.bump;
    domain_ledger.set_inner(reserve_domain, asset_mint, domain_sheet, bump);

    let plan_ledger = &mut ctx.accounts.plan_reserve_ledger;
    let health_plan = plan_ledger.health_plan;
    let asset_mint = plan_ledger.asset_mint;
    let bump = plan_ledger.bump;
    plan_ledger.set_inner(health_plan, asset_mint, plan_sheet, bump);

    let line_ledger = &mut ctx.accounts.funding_line_ledger;
    let funding_line = line_ledger.funding_line;
    let asset_mint = line_ledger.asset_mint;
    let bump = line_ledger.bump;
    line_ledger.set_inner(funding_line, asset_mint, funding_line_sheet, bump);

    if let Some(series_ledger) = ctx.accounts.series_reserve_ledger.as_mut() {
        let series_ledger = &mut **series_ledger;
        let mut sheet = series_ledger.sheet;
        quasar_book_inflow_sheet(&mut sheet, amount)?;
        if fee > 0 {
            quasar_book_fee_accrual_sheet(&mut sheet, fee)?;
        }
        let policy_series = series_ledger.policy_series;
        let asset_mint = series_ledger.asset_mint;
        let bump = series_ledger.bump;
        series_ledger.set_inner(policy_series, asset_mint, sheet, bump);
    }

    if fee > 0 {
        let fee_vault = &mut ctx.accounts.protocol_fee_vault;
        let reserve_domain = fee_vault.reserve_domain;
        let asset_mint = fee_vault.asset_mint;
        let fee_recipient = fee_vault.fee_recipient;
        let withdrawn_fees = fee_vault.withdrawn_fees.get();
        let bump = fee_vault.bump;
        fee_vault.set_inner(
            reserve_domain,
            asset_mint,
            fee_recipient,
            new_accrued_fees,
            withdrawn_fees,
            bump,
        );
    }

    Ok(())
}

#[derive(Accounts)]
pub struct FundSponsorBudget<'info> {
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
    #[account(mut, seeds = [SEED_DOMAIN_ASSET_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()], bump = domain_asset_vault.bump)]
    pub domain_asset_vault: Box<Account<'info, DomainAssetVault>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            domain_asset_vault.address(),
            &crate::ID,
            &[SEED_DOMAIN_ASSET_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()],
            domain_asset_vault.bump,
        ) @ OmegaXProtocolError::DomainAssetVaultRequired
    )]
    pub domain_asset_vault: &'info mut Account<DomainAssetVault>,
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
    pub domain_asset_ledger: &'info mut Account<DomainAssetLedger>,
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
    pub funding_line_ledger: &'info mut Account<FundingLineLedger>,
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
    pub plan_reserve_ledger: &'info mut Account<PlanReserveLedger>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub series_reserve_ledger: Option<Box<Account<'info, SeriesReserveLedger>>>,
    #[cfg(feature = "quasar")]
    pub series_reserve_ledger: Option<&'info mut Account<SeriesReserveLedger>>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub source_token_account: InterfaceAccount<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: InterfaceAccount<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: InterfaceAccount<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Interface<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
}
#[derive(Accounts)]
pub struct RecordPremiumPayment<'info> {
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
    #[account(mut, seeds = [SEED_DOMAIN_ASSET_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()], bump = domain_asset_vault.bump)]
    pub domain_asset_vault: Box<Account<'info, DomainAssetVault>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            domain_asset_vault.address(),
            &crate::ID,
            &[SEED_DOMAIN_ASSET_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()],
            domain_asset_vault.bump,
        ) @ OmegaXProtocolError::DomainAssetVaultRequired
    )]
    pub domain_asset_vault: &'info mut Account<DomainAssetVault>,
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
    pub domain_asset_ledger: &'info mut Account<DomainAssetLedger>,
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
    pub funding_line_ledger: &'info mut Account<FundingLineLedger>,
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
    pub plan_reserve_ledger: &'info mut Account<PlanReserveLedger>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub series_reserve_ledger: Option<Box<Account<'info, SeriesReserveLedger>>>,
    #[cfg(feature = "quasar")]
    pub series_reserve_ledger: Option<&'info mut Account<SeriesReserveLedger>>,
    #[cfg(not(feature = "quasar"))]
    #[account(
        mut,
        seeds = [SEED_PROTOCOL_FEE_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()],
        bump = protocol_fee_vault.bump,
        constraint = protocol_fee_vault.reserve_domain == health_plan.reserve_domain @ OmegaXProtocolError::FeeVaultMismatch,
        constraint = protocol_fee_vault.asset_mint == funding_line.asset_mint @ OmegaXProtocolError::FeeVaultMismatch,
    )]
    pub protocol_fee_vault: Box<Account<'info, ProtocolFeeVault>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            protocol_fee_vault.address(),
            &crate::ID,
            &[SEED_PROTOCOL_FEE_VAULT, health_plan.reserve_domain.as_ref(), funding_line.asset_mint.as_ref()],
            protocol_fee_vault.bump,
        ) @ OmegaXProtocolError::FeeVaultMismatch,
        constraint = protocol_fee_vault.reserve_domain == health_plan.reserve_domain @ OmegaXProtocolError::FeeVaultMismatch,
        constraint = protocol_fee_vault.asset_mint == funding_line.asset_mint @ OmegaXProtocolError::FeeVaultMismatch,
    )]
    pub protocol_fee_vault: &'info mut Account<ProtocolFeeVault>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub source_token_account: InterfaceAccount<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: InterfaceAccount<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: InterfaceAccount<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Interface<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
}
