// SPDX-License-Identifier: AGPL-3.0-or-later

//! Raw-account layout migrations for accounts whose serialized state grew.
//!
//! These handlers intentionally avoid `Account<T>` for the migrated account so
//! legacy, shorter account data can be reallocated and rewritten before Anchor
//! attempts to deserialize the current account layout in ordinary handlers.

use anchor_lang::prelude::*;
use anchor_lang::solana_program::{program::invoke, system_instruction};

use crate::args::*;
use crate::constants::*;
use crate::errors::*;
use crate::program::OmegaxProtocol;
use crate::state::*;

#[derive(AnchorSerialize, AnchorDeserialize)]
struct LegacyProtocolGovernance {
    governance_authority: Pubkey,
    protocol_fee_bps: u16,
    emergency_pause: bool,
    audit_nonce: u64,
    bump: u8,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
struct LegacyCapitalClass {
    reserve_domain: Pubkey,
    liquidity_pool: Pubkey,
    share_mint: Pubkey,
    class_id: String,
    display_name: String,
    priority: u8,
    impairment_rank: u8,
    restriction_mode: u8,
    redemption_terms_mode: u8,
    wrapper_metadata_hash: [u8; 32],
    permissioning_hash: [u8; 32],
    fee_bps: u16,
    min_lockup_seconds: i64,
    pause_flags: u32,
    queue_only_redemptions: bool,
    total_shares: u64,
    nav_assets: u64,
    allocated_assets: u64,
    reserved_assets: u64,
    impaired_assets: u64,
    pending_redemptions: u64,
    active: bool,
    bump: u8,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
struct LegacyLPPosition {
    capital_class: Pubkey,
    owner: Pubkey,
    shares: u64,
    subscription_basis: u64,
    pending_redemption_shares: u64,
    pending_redemption_assets: u64,
    realized_distributions: u64,
    impaired_principal: u64,
    lockup_ends_at: i64,
    credentialed: bool,
    queue_status: u8,
    bump: u8,
}

pub(crate) fn migrate_protocol_governance_layout(
    ctx: Context<MigrateProtocolGovernanceLayout>,
) -> Result<()> {
    migrate_account_layout(
        &ctx.accounts.protocol_governance.to_account_info(),
        &ctx.accounts.authority.to_account_info(),
        &ctx.accounts.system_program.to_account_info(),
        ProtocolGovernance::INIT_SPACE,
        ProtocolGovernance::DISCRIMINATOR,
        |body| {
            let legacy = LegacyProtocolGovernance::deserialize(&mut &body[..])?;
            Ok(ProtocolGovernance {
                governance_authority: legacy.governance_authority,
                pending_governance_authority: ZERO_PUBKEY,
                pending_governance_proposed_at: 0,
                pending_governance_expires_at: 0,
                protocol_fee_bps: legacy.protocol_fee_bps,
                emergency_pause: legacy.emergency_pause,
                audit_nonce: legacy.audit_nonce,
                bump: legacy.bump,
            })
        },
    )
}

pub(crate) fn migrate_capital_class_layout(
    ctx: Context<MigrateCapitalClassLayout>,
    args: MigrateCapitalClassLayoutArgs,
) -> Result<()> {
    let (expected_key, _) = Pubkey::find_program_address(
        &[
            SEED_CAPITAL_CLASS,
            ctx.accounts.liquidity_pool.key().as_ref(),
            args.class_id.as_bytes(),
        ],
        ctx.program_id,
    );
    require_keys_eq!(
        expected_key,
        ctx.accounts.capital_class.key(),
        OmegaXProtocolError::CapitalClassMismatch
    );

    migrate_account_layout(
        &ctx.accounts.capital_class.to_account_info(),
        &ctx.accounts.authority.to_account_info(),
        &ctx.accounts.system_program.to_account_info(),
        CapitalClass::INIT_SPACE,
        CapitalClass::DISCRIMINATOR,
        |body| {
            let legacy = LegacyCapitalClass::deserialize(&mut &body[..])?;
            require_keys_eq!(
                legacy.liquidity_pool,
                ctx.accounts.liquidity_pool.key(),
                OmegaXProtocolError::LiquidityPoolMismatch
            );
            require!(
                legacy.class_id == args.class_id,
                OmegaXProtocolError::CapitalClassMismatch
            );
            Ok(CapitalClass {
                reserve_domain: legacy.reserve_domain,
                liquidity_pool: legacy.liquidity_pool,
                share_mint: legacy.share_mint,
                class_id: legacy.class_id,
                display_name: legacy.display_name,
                priority: legacy.priority,
                impairment_rank: legacy.impairment_rank,
                restriction_mode: legacy.restriction_mode,
                redemption_terms_mode: legacy.redemption_terms_mode,
                wrapper_metadata_hash: legacy.wrapper_metadata_hash,
                permissioning_hash: legacy.permissioning_hash,
                fee_bps: legacy.fee_bps,
                min_lockup_seconds: legacy.min_lockup_seconds,
                pause_flags: legacy.pause_flags,
                queue_only_redemptions: legacy.queue_only_redemptions,
                total_shares: legacy.total_shares,
                nav_assets: legacy.nav_assets,
                allocated_assets: legacy.allocated_assets,
                reserved_assets: legacy.reserved_assets,
                impaired_assets: legacy.impaired_assets,
                pending_redemptions: legacy.pending_redemptions,
                next_redemption_sequence: 0,
                next_redemption_to_process: 0,
                active: legacy.active,
                bump: legacy.bump,
            })
        },
    )
}

pub(crate) fn migrate_lp_position_layout(
    ctx: Context<MigrateLPPositionLayout>,
    args: MigrateLPPositionLayoutArgs,
) -> Result<()> {
    let (expected_key, _) = Pubkey::find_program_address(
        &[
            SEED_LP_POSITION,
            ctx.accounts.capital_class.key().as_ref(),
            args.owner.as_ref(),
        ],
        ctx.program_id,
    );
    require_keys_eq!(
        expected_key,
        ctx.accounts.lp_position.key(),
        OmegaXProtocolError::CapitalClassMismatch
    );

    migrate_account_layout(
        &ctx.accounts.lp_position.to_account_info(),
        &ctx.accounts.authority.to_account_info(),
        &ctx.accounts.system_program.to_account_info(),
        LPPosition::INIT_SPACE,
        LPPosition::DISCRIMINATOR,
        |body| {
            let legacy = LegacyLPPosition::deserialize(&mut &body[..])?;
            require_keys_eq!(
                legacy.capital_class,
                ctx.accounts.capital_class.key(),
                OmegaXProtocolError::CapitalClassMismatch
            );
            require_keys_eq!(legacy.owner, args.owner, OmegaXProtocolError::Unauthorized);
            Ok(LPPosition {
                capital_class: legacy.capital_class,
                owner: legacy.owner,
                shares: legacy.shares,
                subscription_basis: legacy.subscription_basis,
                pending_redemption_shares: legacy.pending_redemption_shares,
                pending_redemption_assets: legacy.pending_redemption_assets,
                realized_distributions: legacy.realized_distributions,
                impaired_principal: legacy.impaired_principal,
                lockup_ends_at: legacy.lockup_ends_at,
                credentialed: legacy.credentialed,
                queue_status: legacy.queue_status,
                redemption_sequence: 0,
                redemption_requested_at: 0,
                bump: legacy.bump,
            })
        },
    )
}

fn migrate_account_layout<'info, T, F>(
    account: &AccountInfo<'info>,
    payer: &AccountInfo<'info>,
    system_program: &AccountInfo<'info>,
    current_body_space: usize,
    discriminator: &[u8],
    legacy_to_current: F,
) -> Result<()>
where
    T: AnchorSerialize + AnchorDeserialize,
    F: FnOnce(&[u8]) -> Result<T>,
{
    require_keys_eq!(*account.owner, crate::ID, OmegaXProtocolError::Unauthorized);

    let current_len = 8usize
        .checked_add(current_body_space)
        .ok_or(OmegaXProtocolError::ArithmeticError)?;
    let account_len = account.data_len();
    require!(account_len >= 8, OmegaXProtocolError::Unauthorized);

    {
        let data = account.try_borrow_data()?;
        require!(
            &data[..discriminator.len()] == discriminator,
            OmegaXProtocolError::Unauthorized
        );
        if account_len >= current_len {
            let _ = T::deserialize(&mut &data[8..])?;
            return Ok(());
        }
    }

    let current = {
        let data = account.try_borrow_data()?;
        legacy_to_current(&data[8..])?
    };

    fund_realloc(account, payer, system_program, current_len)?;

    let mut data = account.try_borrow_mut_data()?;
    data[..discriminator.len()].copy_from_slice(discriminator);
    let mut body = &mut data[8..];
    current.serialize(&mut body)?;

    Ok(())
}

fn fund_realloc<'info>(
    account: &AccountInfo<'info>,
    payer: &AccountInfo<'info>,
    system_program: &AccountInfo<'info>,
    new_len: usize,
) -> Result<()> {
    let rent = Rent::get()?;
    let required_lamports = rent.minimum_balance(new_len);
    let current_lamports = account.lamports();

    if current_lamports < required_lamports {
        let top_up = required_lamports
            .checked_sub(current_lamports)
            .ok_or(OmegaXProtocolError::ArithmeticError)?;
        invoke(
            &system_instruction::transfer(payer.key, account.key, top_up),
            &[payer.clone(), account.clone(), system_program.clone()],
        )?;
    }

    account.resize(new_len)?;
    Ok(())
}

#[derive(Accounts)]
pub struct MigrateProtocolGovernanceLayout<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    #[account(mut, seeds = [SEED_PROTOCOL_GOVERNANCE], bump)]
    /// CHECK: This handler must accept legacy shorter bytes before Anchor can
    /// deserialize the current ProtocolGovernance layout. The PDA seed, owner,
    /// discriminator, and upgrade authority are verified explicitly.
    pub protocol_governance: UncheckedAccount<'info>,
    #[account(
        constraint = program.programdata_address()? == Some(program_data.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program: Program<'info, OmegaxProtocol>,
    #[account(
        constraint = program_data.upgrade_authority_address == Some(authority.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program_data: Account<'info, ProgramData>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct MigrateCapitalClassLayout<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    pub liquidity_pool: Account<'info, LiquidityPool>,
    #[account(mut)]
    /// CHECK: The account may still contain the legacy shorter CapitalClass
    /// layout. The handler verifies the PDA key, owner, discriminator, and
    /// parsed liquidity-pool/class-id binding before rewriting it.
    pub capital_class: UncheckedAccount<'info>,
    #[account(
        constraint = program.programdata_address()? == Some(program_data.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program: Program<'info, OmegaxProtocol>,
    #[account(
        constraint = program_data.upgrade_authority_address == Some(authority.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program_data: Account<'info, ProgramData>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct MigrateLPPositionLayout<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    /// CHECK: CapitalClass may be legacy-sized during batched migrations. The
    /// LP PDA key and parsed account body are both checked against this key.
    pub capital_class: UncheckedAccount<'info>,
    #[account(mut)]
    /// CHECK: The account may still contain the legacy shorter LPPosition
    /// layout. The handler verifies the PDA key, owner, discriminator, and
    /// parsed capital-class/owner binding before rewriting it.
    pub lp_position: UncheckedAccount<'info>,
    #[account(
        constraint = program.programdata_address()? == Some(program_data.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program: Program<'info, OmegaxProtocol>,
    #[account(
        constraint = program_data.upgrade_authority_address == Some(authority.key()) @ OmegaXProtocolError::Unauthorized
    )]
    pub program_data: Account<'info, ProgramData>,
    pub system_program: Program<'info, System>,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn legacy_protocol_governance() -> LegacyProtocolGovernance {
        LegacyProtocolGovernance {
            governance_authority: Pubkey::new_unique(),
            protocol_fee_bps: 25,
            emergency_pause: true,
            audit_nonce: 9,
            bump: 254,
        }
    }

    #[test]
    fn legacy_protocol_governance_maps_inserted_fields_to_defaults() {
        let legacy = legacy_protocol_governance();
        let mut bytes = Vec::new();
        legacy.serialize(&mut bytes).unwrap();

        let current = {
            let legacy = LegacyProtocolGovernance::deserialize(&mut &bytes[..]).unwrap();
            ProtocolGovernance {
                governance_authority: legacy.governance_authority,
                pending_governance_authority: ZERO_PUBKEY,
                pending_governance_proposed_at: 0,
                pending_governance_expires_at: 0,
                protocol_fee_bps: legacy.protocol_fee_bps,
                emergency_pause: legacy.emergency_pause,
                audit_nonce: legacy.audit_nonce,
                bump: legacy.bump,
            }
        };

        assert_eq!(current.protocol_fee_bps, 25);
        assert_eq!(current.pending_governance_authority, ZERO_PUBKEY);
        assert_eq!(current.pending_governance_proposed_at, 0);
        assert_eq!(current.pending_governance_expires_at, 0);
        assert!(current.emergency_pause);
        assert_eq!(current.audit_nonce, 9);
        assert_eq!(current.bump, 254);
    }
}
