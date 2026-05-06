// SPDX-License-Identifier: AGPL-3.0-or-later

//! Certora CVLR rules compiled only for manual formal-verification runs.

use cvlr::prelude::*;

use crate::constants::{BASIS_POINTS_DENOMINATOR, MAX_SELECTED_ASSET_PAYOUT_OVERPAY_BPS};

const CERTORA_SCALE_1E6: u64 = 1_000_000;
const CERTORA_MAX_AMOUNT: u64 = 1_000_000_000;
const CERTORA_MAX_PRICE_1E8: u64 = 1_000_000;

fn certora_value_1e8(amount: u64, price_1e8: u64) -> u64 {
    (amount * price_1e8) / CERTORA_SCALE_1E6
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

    let claim_value = certora_value_1e8(claim_credit_amount, claim_price_1e8);
    let payout_value = certora_value_1e8(payout_amount, payout_price_1e8);
    let max_value = (claim_value * ((BASIS_POINTS_DENOMINATOR as u64) + (max_overpay_bps as u64)))
        / (BASIS_POINTS_DENOMINATOR as u64);

    let accepted = payout_value >= claim_value && payout_value <= max_value;

    if accepted {
        cvlr_assert!(payout_value >= claim_value);
        cvlr_assert!(payout_value <= max_value);
    }

    cvlr_satisfy!(accepted);
}
