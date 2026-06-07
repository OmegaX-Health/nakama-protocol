// SPDX-License-Identifier: AGPL-3.0-or-later

//! Funding and premium inflow instruction handlers and account validation contexts.

use super::*;

#[cfg(not(feature = "quasar"))]
pub(crate) fn fund_sponsor_budget(
    ctx: Context<FundSponsorBudget>,
    args: FundSponsorBudgetArgs,
) -> Result<()> {
    require_plan_control(&ctx.accounts.authority.key(), &ctx.accounts.health_plan)?;
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
    let amount = args.amount;
    let funding_line = &mut ctx.accounts.funding_line;
    funding_line.funded_amount = checked_add(funding_line.funded_amount, amount)?;
    book_inflow(&mut ctx.accounts.domain_asset_vault.total_assets, amount)?;
    book_inflow_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;

    emit!(FundingFlowRecordedEvent {
        funding_line: funding_line.key(),
        amount,
        flow_kind: FundingFlowKind::SponsorBudgetFunded as u8,
        reference_hash: [0u8; 32],
    });

    Ok(())
}
#[cfg(not(feature = "quasar"))]
pub(crate) fn record_premium_payment(
    ctx: Context<RecordPremiumPayment>,
    args: RecordPremiumPaymentArgs,
) -> Result<()> {
    require_plan_control(&ctx.accounts.authority.key(), &ctx.accounts.health_plan)?;
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
    let amount = args.amount;
    let funding_line_key = ctx.accounts.funding_line.key();

    let funding_line = &mut ctx.accounts.funding_line;
    funding_line.funded_amount = checked_add(funding_line.funded_amount, amount)?;
    book_inflow(&mut ctx.accounts.domain_asset_vault.total_assets, amount)?;
    book_inflow_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_inflow_sheet(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;

    emit!(FundingFlowRecordedEvent {
        funding_line: funding_line_key,
        amount,
        flow_kind: FundingFlowKind::PremiumRecorded as u8,
        reference_hash: [0u8; 32],
    });

    Ok(())
}

#[cfg(not(feature = "quasar"))]
fn require_reserve_capital_line(funding_line: &FundingLine) -> Result<()> {
    require!(
        funding_line.line_type == FUNDING_LINE_TYPE_BACKSTOP,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    require!(
        funding_line.status == FUNDING_LINE_STATUS_OPEN,
        OmegaXProtocolError::FundingLineMismatch
    );
    Ok(())
}

#[cfg(not(feature = "quasar"))]
fn require_reserve_earnings_line(funding_line: &FundingLine) -> Result<()> {
    require!(
        funding_line.line_type == FUNDING_LINE_TYPE_BACKSTOP
            || funding_line.line_type == FUNDING_LINE_TYPE_SUBSIDY,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    require!(
        funding_line.status == FUNDING_LINE_STATUS_OPEN,
        OmegaXProtocolError::FundingLineMismatch
    );
    Ok(())
}

#[cfg(not(feature = "quasar"))]
fn require_nonzero_hash(hash: &[u8; 32], error: OmegaXProtocolError) -> Result<()> {
    if hash.iter().any(|byte| *byte != 0) {
        Ok(())
    } else {
        Err(error.into())
    }
}

#[cfg(not(feature = "quasar"))]
fn book_return_sheet(sheet: &mut ReserveBalanceSheet, amount: u64) -> Result<()> {
    require_free_reserve_capacity(sheet, amount)?;
    sheet.funded = checked_sub(sheet.funded, amount)?;
    recompute_sheet(sheet)
}

#[cfg(not(feature = "quasar"))]
fn apply_inflow_books(
    amount: u64,
    domain_asset_vault: &mut DomainAssetVault,
    domain_asset_ledger: &mut DomainAssetLedger,
    plan_reserve_ledger: &mut PlanReserveLedger,
    funding_line_ledger: &mut FundingLineLedger,
) -> Result<()> {
    book_inflow(&mut domain_asset_vault.total_assets, amount)?;
    book_inflow_sheet(&mut domain_asset_ledger.sheet, amount)?;
    book_inflow_sheet(&mut plan_reserve_ledger.sheet, amount)?;
    book_inflow_sheet(&mut funding_line_ledger.sheet, amount)?;
    Ok(())
}

#[cfg(not(feature = "quasar"))]
pub(crate) fn deposit_reserve_capital(
    ctx: Context<DepositReserveCapital>,
    args: DepositReserveCapitalArgs,
) -> Result<()> {
    require_positive_amount(args.amount)?;
    require_reserve_capital_line(&ctx.accounts.funding_line)?;
    transfer_to_domain_vault(
        args.amount,
        &ctx.accounts.contributor,
        &ctx.accounts.source_token_account,
        &ctx.accounts.asset_mint,
        &ctx.accounts.vault_token_account,
        &ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;

    let contribution = &mut ctx.accounts.capital_contribution;
    if contribution.contributor == ZERO_PUBKEY {
        contribution.reserve_domain = ctx.accounts.health_plan.reserve_domain;
        contribution.health_plan = ctx.accounts.health_plan.key();
        contribution.funding_line = ctx.accounts.funding_line.key();
        contribution.contributor = ctx.accounts.contributor.key();
        contribution.asset_mint = ctx.accounts.funding_line.asset_mint;
        contribution.contributed_amount = 0;
        contribution.returned_amount = 0;
        contribution.terms_hash = args.terms_hash;
        contribution.bump = ctx.bumps.capital_contribution;
    } else {
        require_keys_eq!(
            contribution.contributor,
            ctx.accounts.contributor.key(),
            OmegaXProtocolError::Unauthorized
        );
        require_keys_eq!(
            contribution.funding_line,
            ctx.accounts.funding_line.key(),
            OmegaXProtocolError::FundingLineMismatch
        );
        require_keys_eq!(
            contribution.asset_mint,
            ctx.accounts.funding_line.asset_mint,
            OmegaXProtocolError::AssetMintMismatch
        );
        if contribution.contributed_amount > contribution.returned_amount {
            require!(
                contribution.terms_hash == args.terms_hash,
                OmegaXProtocolError::CapitalContributionTermsMismatch
            );
        } else {
            contribution.terms_hash = args.terms_hash;
        }
    }

    let amount = args.amount;
    contribution.contributed_amount = checked_add(contribution.contributed_amount, amount)?;
    ctx.accounts.funding_line.funded_amount =
        checked_add(ctx.accounts.funding_line.funded_amount, amount)?;
    apply_inflow_books(
        amount,
        &mut ctx.accounts.domain_asset_vault,
        &mut ctx.accounts.domain_asset_ledger,
        &mut ctx.accounts.plan_reserve_ledger,
        &mut ctx.accounts.funding_line_ledger,
    )?;

    emit!(FundingFlowRecordedEvent {
        funding_line: ctx.accounts.funding_line.key(),
        amount,
        flow_kind: FundingFlowKind::ReserveCapitalContributed as u8,
        reference_hash: args.terms_hash,
    });

    Ok(())
}

#[cfg(not(feature = "quasar"))]
pub(crate) fn return_reserve_capital(
    ctx: Context<ReturnReserveCapital>,
    args: ReturnReserveCapitalArgs,
) -> Result<()> {
    require_plan_control(&ctx.accounts.authority.key(), &ctx.accounts.health_plan)?;
    require_positive_amount(args.amount)?;
    require_reserve_capital_line(&ctx.accounts.funding_line)?;
    let contribution_available = checked_sub(
        ctx.accounts.capital_contribution.contributed_amount,
        ctx.accounts.capital_contribution.returned_amount,
    )?;
    require!(
        contribution_available >= args.amount,
        OmegaXProtocolError::CapitalContributionAmountExceedsAvailable
    );
    require_keys_eq!(
        ctx.accounts.recipient_token_account.owner,
        ctx.accounts.capital_contribution.contributor,
        OmegaXProtocolError::TokenAccountOwnerMismatch
    );

    let amount = args.amount;
    book_return_sheet(&mut ctx.accounts.domain_asset_ledger.sheet, amount)?;
    book_return_sheet(&mut ctx.accounts.plan_reserve_ledger.sheet, amount)?;
    book_return_sheet(&mut ctx.accounts.funding_line_ledger.sheet, amount)?;
    ctx.accounts.domain_asset_vault.total_assets =
        checked_sub(ctx.accounts.domain_asset_vault.total_assets, amount)?;
    ctx.accounts.funding_line.funded_amount =
        checked_sub(ctx.accounts.funding_line.funded_amount, amount)?;
    ctx.accounts.funding_line.returned_amount =
        checked_add(ctx.accounts.funding_line.returned_amount, amount)?;
    ctx.accounts.capital_contribution.returned_amount =
        checked_add(ctx.accounts.capital_contribution.returned_amount, amount)?;

    transfer_from_domain_vault(
        amount,
        &ctx.accounts.domain_asset_vault,
        &ctx.accounts.vault_token_account,
        &ctx.accounts.recipient_token_account,
        &ctx.accounts.asset_mint,
        &ctx.accounts.token_program,
    )?;

    emit!(FundingFlowRecordedEvent {
        funding_line: ctx.accounts.funding_line.key(),
        amount,
        flow_kind: FundingFlowKind::ReserveCapitalReturned as u8,
        reference_hash: args.reason_hash,
    });

    Ok(())
}

#[cfg(not(feature = "quasar"))]
pub(crate) fn record_reserve_earnings(
    ctx: Context<RecordReserveEarnings>,
    args: RecordReserveEarningsArgs,
) -> Result<()> {
    require_plan_control(&ctx.accounts.authority.key(), &ctx.accounts.health_plan)?;
    require_positive_amount(args.amount)?;
    require_nonzero_hash(
        &args.earnings_ref_hash,
        OmegaXProtocolError::ReserveEarningsReferenceRequired,
    )?;
    require_reserve_earnings_line(&ctx.accounts.funding_line)?;
    transfer_to_domain_vault(
        args.amount,
        &ctx.accounts.authority,
        &ctx.accounts.source_token_account,
        &ctx.accounts.asset_mint,
        &ctx.accounts.vault_token_account,
        &ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;

    let amount = args.amount;
    ctx.accounts.funding_line.funded_amount =
        checked_add(ctx.accounts.funding_line.funded_amount, amount)?;
    apply_inflow_books(
        amount,
        &mut ctx.accounts.domain_asset_vault,
        &mut ctx.accounts.domain_asset_ledger,
        &mut ctx.accounts.plan_reserve_ledger,
        &mut ctx.accounts.funding_line_ledger,
    )?;

    emit!(FundingFlowRecordedEvent {
        funding_line: ctx.accounts.funding_line.key(),
        amount,
        flow_kind: FundingFlowKind::ReserveEarningsRecorded as u8,
        reference_hash: args.earnings_ref_hash,
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
fn require_quasar_positive_amount(amount: u64) -> Result<()> {
    require!(amount > 0, OmegaXProtocolError::AmountMustBePositive);
    Ok(())
}

#[cfg(feature = "quasar")]
#[inline(always)]
fn require_quasar_plan_control(authority: &Pubkey, plan: &HealthPlanAccountData<'_>) -> Result<()> {
    if *authority == plan.plan_admin || *authority == plan.sponsor_operator {
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
fn quasar_require_free_reserve_capacity(sheet: &ReserveBalanceSheet, amount: u64) -> Result<()> {
    require!(
        sheet.free >= amount,
        OmegaXProtocolError::InsufficientFreeReserveCapacity
    );
    Ok(())
}

#[cfg(feature = "quasar")]
fn quasar_book_return_sheet(sheet: &mut ReserveBalanceSheet, amount: u64) -> Result<()> {
    quasar_require_free_reserve_capacity(sheet, amount)?;
    sheet.funded = quasar_checked_sub(sheet.funded, amount)?;
    quasar_recompute_sheet(sheet)
}

#[cfg(feature = "quasar")]
fn require_quasar_reserve_capital_line(funding_line: &FundingLineAccountData<'_>) -> Result<()> {
    require!(
        funding_line.line_type == FUNDING_LINE_TYPE_BACKSTOP,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    require!(
        funding_line.status == FUNDING_LINE_STATUS_OPEN,
        OmegaXProtocolError::FundingLineMismatch
    );
    Ok(())
}

#[cfg(feature = "quasar")]
fn require_quasar_reserve_earnings_line(funding_line: &FundingLineAccountData<'_>) -> Result<()> {
    require!(
        funding_line.line_type == FUNDING_LINE_TYPE_BACKSTOP
            || funding_line.line_type == FUNDING_LINE_TYPE_SUBSIDY,
        OmegaXProtocolError::FundingLineTypeMismatch
    );
    require!(
        funding_line.status == FUNDING_LINE_STATUS_OPEN,
        OmegaXProtocolError::FundingLineMismatch
    );
    Ok(())
}

#[cfg(feature = "quasar")]
fn require_quasar_nonzero_hash(hash: &[u8; 32], error: OmegaXProtocolError) -> Result<()> {
    if hash.iter().any(|byte| *byte != 0) {
        Ok(())
    } else {
        Err(error.into())
    }
}

#[cfg(feature = "quasar")]
pub(crate) fn fund_sponsor_budget<'info>(
    ctx: &mut Ctx<'info, FundSponsorBudget<'info>>,
    amount: u64,
) -> Result<()> {
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(&authority, &ctx.accounts.health_plan)?;
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

    Ok(())
}

#[cfg(feature = "quasar")]
pub(crate) fn record_premium_payment<'info>(
    ctx: &mut Ctx<'info, RecordPremiumPayment<'info>>,
    amount: u64,
) -> Result<()> {
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(&authority, &ctx.accounts.health_plan)?;
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

    Ok(())
}

#[cfg(feature = "quasar")]
pub(crate) fn deposit_reserve_capital<'info>(
    ctx: &mut Ctx<'info, DepositReserveCapital<'info>>,
    amount: u64,
    terms_hash: [u8; 32],
) -> Result<()> {
    require_quasar_positive_amount(amount)?;
    require_quasar_reserve_capital_line(&ctx.accounts.funding_line)?;
    transfer_to_domain_vault(
        amount,
        ctx.accounts.contributor,
        ctx.accounts.source_token_account,
        ctx.accounts.asset_mint,
        ctx.accounts.vault_token_account,
        ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
    )?;

    let contributor = *ctx.accounts.contributor.address();
    let health_plan_key = *ctx.accounts.health_plan.address();
    let funding_line_key = *ctx.accounts.funding_line.address();
    let contribution = &mut ctx.accounts.capital_contribution;
    let existing_contributed = contribution.contributed_amount.get();
    let existing_returned = contribution.returned_amount.get();
    if contribution.contributor == ZERO_PUBKEY {
        let bump = contribution.bump;
        contribution.set_inner(
            ctx.accounts.health_plan.reserve_domain,
            health_plan_key,
            funding_line_key,
            contributor,
            ctx.accounts.funding_line.asset_mint,
            0,
            0,
            terms_hash,
            bump,
        );
    } else {
        require_keys_eq!(
            contribution.contributor,
            contributor,
            OmegaXProtocolError::Unauthorized
        );
        require_keys_eq!(
            contribution.funding_line,
            funding_line_key,
            OmegaXProtocolError::FundingLineMismatch
        );
        require_keys_eq!(
            contribution.asset_mint,
            ctx.accounts.funding_line.asset_mint,
            OmegaXProtocolError::AssetMintMismatch
        );
        if existing_contributed > existing_returned {
            require!(
                contribution.terms_hash == terms_hash,
                OmegaXProtocolError::CapitalContributionTermsMismatch
            );
        }
    }

    let new_contributed = quasar_checked_add(
        ctx.accounts.capital_contribution.contributed_amount.get(),
        amount,
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
        ctx.accounts.contributor.to_account_view(),
        None,
    )?;

    let contribution = &mut ctx.accounts.capital_contribution;
    let reserve_domain = contribution.reserve_domain;
    let health_plan = contribution.health_plan;
    let funding_line = contribution.funding_line;
    let contributor = contribution.contributor;
    let asset_mint = contribution.asset_mint;
    let returned_amount = contribution.returned_amount.get();
    let bump = contribution.bump;
    contribution.set_inner(
        reserve_domain,
        health_plan,
        funding_line,
        contributor,
        asset_mint,
        new_contributed,
        returned_amount,
        terms_hash,
        bump,
    );

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

    Ok(())
}

#[cfg(feature = "quasar")]
pub(crate) fn return_reserve_capital<'info>(
    ctx: &mut Ctx<'info, ReturnReserveCapital<'info>>,
    amount: u64,
    _reason_hash: [u8; 32],
) -> Result<()> {
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(&authority, &ctx.accounts.health_plan)?;
    require_quasar_positive_amount(amount)?;
    require_quasar_reserve_capital_line(&ctx.accounts.funding_line)?;
    let contribution_available = quasar_checked_sub(
        ctx.accounts.capital_contribution.contributed_amount.get(),
        ctx.accounts.capital_contribution.returned_amount.get(),
    )?;
    require!(
        contribution_available >= amount,
        OmegaXProtocolError::CapitalContributionAmountExceedsAvailable
    );
    require_keys_eq!(
        *ctx.accounts.recipient_token_account.owner(),
        ctx.accounts.capital_contribution.contributor,
        OmegaXProtocolError::TokenAccountOwnerMismatch
    );

    let mut domain_sheet = ctx.accounts.domain_asset_ledger.sheet;
    let mut plan_sheet = ctx.accounts.plan_reserve_ledger.sheet;
    let mut funding_line_sheet = ctx.accounts.funding_line_ledger.sheet;
    quasar_book_return_sheet(&mut domain_sheet, amount)?;
    quasar_book_return_sheet(&mut plan_sheet, amount)?;
    quasar_book_return_sheet(&mut funding_line_sheet, amount)?;
    let new_total_assets =
        quasar_checked_sub(ctx.accounts.domain_asset_vault.total_assets.get(), amount)?;
    let new_funded_amount =
        quasar_checked_sub(ctx.accounts.funding_line.funded_amount.get(), amount)?;
    let new_line_returned =
        quasar_checked_add(ctx.accounts.funding_line.returned_amount.get(), amount)?;
    let new_contribution_returned = quasar_checked_add(
        ctx.accounts.capital_contribution.returned_amount.get(),
        amount,
    )?;

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
        new_line_returned,
        status,
        caps_hash,
        bump,
        &line_id,
        ctx.accounts.authority.to_account_view(),
        None,
    )?;

    let contribution = &mut ctx.accounts.capital_contribution;
    let reserve_domain = contribution.reserve_domain;
    let health_plan = contribution.health_plan;
    let funding_line = contribution.funding_line;
    let contributor = contribution.contributor;
    let asset_mint = contribution.asset_mint;
    let contributed_amount = contribution.contributed_amount.get();
    let terms_hash = contribution.terms_hash;
    let bump = contribution.bump;
    contribution.set_inner(
        reserve_domain,
        health_plan,
        funding_line,
        contributor,
        asset_mint,
        contributed_amount,
        new_contribution_returned,
        terms_hash,
        bump,
    );

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

    transfer_from_domain_vault(
        amount,
        &ctx.accounts.domain_asset_vault,
        ctx.accounts.vault_token_account,
        ctx.accounts.recipient_token_account,
        ctx.accounts.asset_mint,
        ctx.accounts.token_program,
    )
}

#[cfg(feature = "quasar")]
pub(crate) fn record_reserve_earnings<'info>(
    ctx: &mut Ctx<'info, RecordReserveEarnings<'info>>,
    amount: u64,
    earnings_ref_hash: [u8; 32],
) -> Result<()> {
    let authority = *ctx.accounts.authority.address();
    require_quasar_plan_control(&authority, &ctx.accounts.health_plan)?;
    require_quasar_positive_amount(amount)?;
    require_quasar_nonzero_hash(
        &earnings_ref_hash,
        OmegaXProtocolError::ReserveEarningsReferenceRequired,
    )?;
    require_quasar_reserve_earnings_line(&ctx.accounts.funding_line)?;
    transfer_to_domain_vault(
        amount,
        ctx.accounts.authority,
        ctx.accounts.source_token_account,
        ctx.accounts.asset_mint,
        ctx.accounts.vault_token_account,
        ctx.accounts.token_program,
        &ctx.accounts.domain_asset_vault,
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

    Ok(())
}

#[derive(Accounts)]
pub struct FundSponsorBudget<'info> {
    #[cfg(not(feature = "quasar"))]
    pub authority: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub authority: &'info Signer,
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
    pub source_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: Account<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Program<'info, TokenInterface>,
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
    pub source_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: Account<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Program<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
}

#[derive(Accounts)]
#[cfg_attr(not(feature = "quasar"), instruction(args: DepositReserveCapitalArgs))]
#[cfg_attr(feature = "quasar", instruction(_amount: u64, _terms_hash: [u8; 32]))]
pub struct DepositReserveCapital<'info> {
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub contributor: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub contributor: &'info Signer,
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
    #[cfg_attr(
        not(feature = "quasar"),
        account(
            init_if_needed,
            payer = contributor,
            space = 8 + CapitalContribution::INIT_SPACE,
            seeds = [SEED_CAPITAL_CONTRIBUTION, funding_line.key().as_ref(), contributor.key().as_ref()],
            bump
        )
    )]
    #[cfg(not(feature = "quasar"))]
    pub capital_contribution: Box<Account<'info, CapitalContribution>>,
    #[cfg_attr(
        feature = "quasar",
        account(
            mut,
            constraint = quasar_pda_matches(
                capital_contribution.address(),
                &crate::ID,
                &[SEED_CAPITAL_CONTRIBUTION, funding_line.address().as_ref(), contributor.address().as_ref()],
                capital_contribution.bump,
            ) @ OmegaXProtocolError::FundingLineMismatch
        )
    )]
    #[cfg(feature = "quasar")]
    pub capital_contribution: &'info mut Account<CapitalContribution>,
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
    pub source_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: Account<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Program<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
    #[cfg(not(feature = "quasar"))]
    pub system_program: Program<'info, System>,
    #[cfg(feature = "quasar")]
    pub system_program: &'info Program<System>,
}

#[derive(Accounts)]
pub struct ReturnReserveCapital<'info> {
    #[cfg(not(feature = "quasar"))]
    pub authority: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub authority: &'info Signer,
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
    #[account(mut, seeds = [SEED_CAPITAL_CONTRIBUTION, funding_line.key().as_ref(), capital_contribution.contributor.as_ref()], bump = capital_contribution.bump)]
    pub capital_contribution: Box<Account<'info, CapitalContribution>>,
    #[cfg(feature = "quasar")]
    #[account(
        mut,
        constraint = quasar_pda_matches(
            capital_contribution.address(),
            &crate::ID,
            &[SEED_CAPITAL_CONTRIBUTION, funding_line.address().as_ref(), capital_contribution.contributor.as_ref()],
            capital_contribution.bump,
        ) @ OmegaXProtocolError::FundingLineMismatch
    )]
    pub capital_contribution: &'info mut Account<CapitalContribution>,
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
    pub asset_mint: Account<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub recipient_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub recipient_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Program<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
}

#[derive(Accounts)]
pub struct RecordReserveEarnings<'info> {
    #[cfg(not(feature = "quasar"))]
    pub authority: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub authority: &'info Signer,
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
    pub source_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub source_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub asset_mint: Account<'info, Mint>,
    #[cfg(feature = "quasar")]
    pub asset_mint: &'info InterfaceAccount<Mint>,
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub vault_token_account: Account<'info, TokenAccount>,
    #[cfg(feature = "quasar")]
    #[account(mut)]
    pub vault_token_account: &'info mut InterfaceAccount<TokenAccount>,
    #[cfg(not(feature = "quasar"))]
    pub token_program: Program<'info, TokenInterface>,
    #[cfg(feature = "quasar")]
    pub token_program: &'info Interface<TokenInterface>,
}

#[cfg(all(test, not(feature = "quasar")))]
mod tests {
    use super::*;

    fn sample_line(line_type: u8, status: u8) -> FundingLine {
        FundingLine {
            reserve_domain: Pubkey::new_unique(),
            health_plan: Pubkey::new_unique(),
            policy_series: Pubkey::new_unique(),
            asset_mint: Pubkey::new_unique(),
            line_id: "line".to_string(),
            line_type,
            funding_priority: 0,
            committed_amount: 0,
            funded_amount: 0,
            reserved_amount: 0,
            spent_amount: 0,
            released_amount: 0,
            returned_amount: 0,
            status,
            caps_hash: [0; 32],
            bump: 0,
        }
    }

    #[test]
    fn reserve_capital_deposits_only_use_open_backstop_lines() {
        assert!(require_reserve_capital_line(&sample_line(
            FUNDING_LINE_TYPE_BACKSTOP,
            FUNDING_LINE_STATUS_OPEN,
        ))
        .is_ok());
        assert!(require_reserve_capital_line(&sample_line(
            FUNDING_LINE_TYPE_PREMIUM_INCOME,
            FUNDING_LINE_STATUS_OPEN,
        ))
        .is_err());
        assert!(require_reserve_capital_line(&sample_line(
            FUNDING_LINE_TYPE_BACKSTOP,
            FUNDING_LINE_STATUS_CLOSED,
        ))
        .is_err());
    }

    #[test]
    fn reserve_earnings_can_land_on_backstop_or_subsidy_lines() {
        assert!(require_reserve_earnings_line(&sample_line(
            FUNDING_LINE_TYPE_BACKSTOP,
            FUNDING_LINE_STATUS_OPEN,
        ))
        .is_ok());
        assert!(require_reserve_earnings_line(&sample_line(
            FUNDING_LINE_TYPE_SUBSIDY,
            FUNDING_LINE_STATUS_OPEN,
        ))
        .is_ok());
        assert!(require_reserve_earnings_line(&sample_line(
            FUNDING_LINE_TYPE_PREMIUM_INCOME,
            FUNDING_LINE_STATUS_OPEN,
        ))
        .is_err());
    }

    #[test]
    fn reserve_capital_returns_cannot_withdraw_encumbered_reserve() {
        let mut sheet = ReserveBalanceSheet {
            funded: 100,
            reserved: 90,
            free: 10,
            redeemable: 10,
            ..ReserveBalanceSheet::default()
        };

        assert!(book_return_sheet(&mut sheet, 11).is_err());
        assert_eq!(sheet.funded, 100);
        book_return_sheet(&mut sheet, 10).unwrap();
        assert_eq!(sheet.funded, 90);
        assert_eq!(sheet.free, 0);
    }
}
