// SPDX-License-Identifier: AGPL-3.0-or-later

//! Liquidity-pool instruction handlers and account validation contexts.

use super::*;

#[cfg(not(feature = "quasar"))]
pub(crate) fn create_liquidity_pool(
    ctx: Context<CreateLiquidityPool>,
    args: CreateLiquidityPoolArgs,
) -> Result<()> {
    require_id(&args.pool_id)?;
    require_domain_control(
        &ctx.accounts.authority.key(),
        &ctx.accounts.protocol_governance,
        &ctx.accounts.reserve_domain,
    )?;
    require!(
        ctx.accounts.domain_asset_vault.asset_mint == args.deposit_asset_mint,
        OmegaXProtocolError::AssetMintMismatch
    );
    require!(
        args.fee_bps <= MAX_CONFIGURED_FEE_BPS,
        OmegaXProtocolError::InvalidBps
    );

    let pool = &mut ctx.accounts.liquidity_pool;
    pool.reserve_domain = ctx.accounts.reserve_domain.key();
    pool.curator = args.curator;
    pool.allocator = args.allocator;
    pool.sentinel = args.sentinel;
    pool.pool_id = args.pool_id;
    pool.display_name = args.display_name;
    pool.deposit_asset_mint = args.deposit_asset_mint;
    pool.strategy_hash = args.strategy_hash;
    pool.allowed_exposure_hash = args.allowed_exposure_hash;
    pool.external_yield_adapter_hash = args.external_yield_adapter_hash;
    pool.fee_bps = args.fee_bps;
    pool.redemption_policy = args.redemption_policy;
    pool.pause_flags = args.pause_flags;
    pool.total_value_locked = 0;
    pool.total_allocated = 0;
    pool.total_reserved = 0;
    pool.total_impaired = 0;
    pool.total_pending_redemptions = 0;
    pool.active = true;
    pool.audit_nonce = 0;
    pool.bump = ctx.bumps.liquidity_pool;

    emit!(LiquidityPoolCreatedEvent {
        reserve_domain: pool.reserve_domain,
        liquidity_pool: pool.key(),
        asset_mint: pool.deposit_asset_mint,
    });

    Ok(())
}

#[derive(Accounts)]
#[instruction(args: CreateLiquidityPoolArgs)]
pub struct CreateLiquidityPool<'info> {
    #[cfg(not(feature = "quasar"))]
    #[account(mut)]
    pub authority: Signer<'info>,
    #[cfg(feature = "quasar")]
    pub authority: &'info mut Signer,
    #[cfg(not(feature = "quasar"))]
    #[account(seeds = [SEED_PROTOCOL_GOVERNANCE], bump = protocol_governance.bump)]
    pub protocol_governance: Account<'info, ProtocolGovernance>,
    #[cfg(feature = "quasar")]
    #[account(seeds = [SEED_PROTOCOL_GOVERNANCE], bump = protocol_governance.bump)]
    pub protocol_governance: &'info Account<ProtocolGovernance>,
    #[cfg(not(feature = "quasar"))]
    #[account(seeds = [SEED_RESERVE_DOMAIN, reserve_domain.domain_id.as_bytes()], bump = reserve_domain.bump)]
    pub reserve_domain: Account<'info, ReserveDomain>,
    #[cfg(feature = "quasar")]
    #[account(
        constraint = quasar_pda_matches(
            reserve_domain.address(),
            &crate::ID,
            &[SEED_RESERVE_DOMAIN, reserve_domain.domain_id().as_bytes()],
            reserve_domain.bump,
        ) @ OmegaXProtocolError::ReserveDomainMismatch
    )]
    pub reserve_domain: &'info Account<ReserveDomainAccountData<'info>>,
    #[cfg(not(feature = "quasar"))]
    #[account(seeds = [SEED_DOMAIN_ASSET_VAULT, reserve_domain.key().as_ref(), args.deposit_asset_mint.as_ref()], bump = domain_asset_vault.bump)]
    pub domain_asset_vault: Account<'info, DomainAssetVault>,
    #[cfg(feature = "quasar")]
    #[account(
        constraint = quasar_pda_matches(
            domain_asset_vault.address(),
            &crate::ID,
            &[SEED_DOMAIN_ASSET_VAULT, reserve_domain.address().as_ref(), domain_asset_vault.asset_mint.as_ref()],
            domain_asset_vault.bump,
        ) @ OmegaXProtocolError::ReserveDomainMismatch
    )]
    pub domain_asset_vault: &'info Account<DomainAssetVault>,
    #[cfg_attr(
        not(feature = "quasar"),
        account(
            init,
            payer = authority,
            space = 8 + LiquidityPool::INIT_SPACE,
            seeds = [SEED_LIQUIDITY_POOL, reserve_domain.key().as_ref(), args.pool_id.as_bytes()],
            bump
        )
    )]
    #[cfg(not(feature = "quasar"))]
    pub liquidity_pool: Account<'info, LiquidityPool>,
    #[cfg_attr(
        feature = "quasar",
        account(
            mut,
            constraint = quasar_pda_matches(
                liquidity_pool.address(),
                &crate::ID,
                &[SEED_LIQUIDITY_POOL, reserve_domain.address().as_ref(), liquidity_pool.pool_id().as_bytes()],
                liquidity_pool.bump,
            ) @ OmegaXProtocolError::LiquidityPoolMismatch
        )
    )]
    #[cfg(feature = "quasar")]
    pub liquidity_pool: &'info mut Account<LiquidityPool<'info>>,
    #[cfg(not(feature = "quasar"))]
    pub system_program: Program<'info, System>,
    #[cfg(feature = "quasar")]
    pub system_program: &'info Program<System>,
}
