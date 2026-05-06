// SPDX-License-Identifier: AGPL-3.0-or-later

//! Certora CVLR rules compiled only for manual formal-verification runs.

use anchor_lang::prelude::Pubkey;
use cvlr::prelude::*;

use crate::constants::{BASIS_POINTS_DENOMINATOR, MAX_SELECTED_ASSET_PAYOUT_OVERPAY_BPS};
use crate::reserve_waterfall::require_selected_asset_payout_value_at;
use crate::state::ReserveAssetRail;

const CERTORA_MINT_DECIMALS: u8 = 6;
const CERTORA_SCALE_1E6: u128 = 1_000_000;
const CERTORA_NOW_TS: i64 = 1;
const CERTORA_MAX_AMOUNT: u64 = 1_000_000_000_000;
const CERTORA_MAX_PRICE_1E8: u64 = 10_000_000_000;

fn certora_price_rail(price_1e8: u64) -> ReserveAssetRail {
    ReserveAssetRail {
        reserve_domain: Pubkey::default(),
        asset_mint: Pubkey::default(),
        oracle_authority: Pubkey::default(),
        asset_symbol: String::new(),
        role: 0,
        payout_priority: 0,
        oracle_source: 0,
        oracle_feed_id: [0u8; 32],
        max_staleness_seconds: CERTORA_NOW_TS,
        haircut_bps: 0,
        max_exposure_bps: 0,
        deposit_enabled: true,
        payout_enabled: true,
        capacity_enabled: true,
        active: true,
        last_price_usd_1e8: price_1e8,
        last_price_confidence_bps: 0,
        last_price_published_at_ts: CERTORA_NOW_TS,
        last_price_slot: 0,
        last_price_proof_hash: [0u8; 32],
        audit_nonce: 0,
        bump: 0,
    }
}

fn certora_value_1e8(amount: u64, price_1e8: u64) -> u128 {
    ((amount as u128) * (price_1e8 as u128)) / CERTORA_SCALE_1E6
}

#[rule]
pub fn rule_selected_asset_payout_bounds() {
    let claim_credit_amount: u64 = nondet();
    let payout_amount: u64 = nondet();
    let max_overpay_bps: u16 = nondet();
    let claim_price_1e8: u64 = nondet();
    let payout_price_1e8: u64 = nondet();

    cvlr_assume!(claim_credit_amount > 0);
    cvlr_assume!(payout_amount > 0);
    cvlr_assume!(claim_credit_amount <= CERTORA_MAX_AMOUNT);
    cvlr_assume!(payout_amount <= CERTORA_MAX_AMOUNT);
    cvlr_assume!(claim_price_1e8 > 0);
    cvlr_assume!(payout_price_1e8 > 0);
    cvlr_assume!(claim_price_1e8 <= CERTORA_MAX_PRICE_1E8);
    cvlr_assume!(payout_price_1e8 <= CERTORA_MAX_PRICE_1E8);
    cvlr_assume!(max_overpay_bps <= MAX_SELECTED_ASSET_PAYOUT_OVERPAY_BPS);

    let claim_rail = certora_price_rail(claim_price_1e8);
    let payout_rail = certora_price_rail(payout_price_1e8);
    let result = require_selected_asset_payout_value_at(
        claim_credit_amount,
        CERTORA_MINT_DECIMALS,
        &claim_rail,
        payout_amount,
        CERTORA_MINT_DECIMALS,
        &payout_rail,
        max_overpay_bps,
        CERTORA_NOW_TS,
    );

    if result.is_ok() {
        let claim_value = certora_value_1e8(claim_credit_amount, claim_price_1e8);
        let payout_value = certora_value_1e8(payout_amount, payout_price_1e8);
        let max_value = (claim_value
            * ((BASIS_POINTS_DENOMINATOR as u128) + (max_overpay_bps as u128)))
            / (BASIS_POINTS_DENOMINATOR as u128);

        cvlr_assert!(payout_value >= claim_value);
        cvlr_assert!(payout_value <= max_value);
    }

    cvlr_satisfy!(result.is_ok());
}
