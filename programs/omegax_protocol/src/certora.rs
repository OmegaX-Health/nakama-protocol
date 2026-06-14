// SPDX-License-Identifier: AGPL-3.0-or-later

//! Certora CVLR rules compiled only for manual formal-verification runs.

use cvlr::prelude::*;

const CERTORA_MAX_BALANCE_COMPONENT: u64 = 1_000_000_000_000;

#[rule]
pub fn rule_reserve_capacity_non_overflow() {
    let funded: u64 = nondet();
    let allocated: u64 = nondet();
    let reserved: u64 = nondet();
    let claimable: u64 = nondet();
    let payable: u64 = nondet();
    let impaired: u64 = nondet();
    let pending_redemption: u64 = nondet();
    let restricted: u64 = nondet();

    cvlr_assume!(funded <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(allocated <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(reserved <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(claimable <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(payable <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(impaired <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(pending_redemption <= CERTORA_MAX_BALANCE_COMPONENT);
    cvlr_assume!(restricted <= CERTORA_MAX_BALANCE_COMPONENT);

    cvlr_assert!(reserved <= u64::MAX - claimable);
    let encumbered = reserved + claimable;
    cvlr_assert!(encumbered <= u64::MAX - payable);
    let encumbered = encumbered + payable;
    cvlr_assert!(encumbered <= u64::MAX - impaired);
    let encumbered = encumbered + impaired;
    cvlr_assert!(encumbered <= u64::MAX - pending_redemption);
    let encumbered = encumbered + pending_redemption;
    cvlr_assert!(encumbered <= u64::MAX - restricted);
    let encumbered = encumbered + restricted;

    cvlr_assert!(encumbered <= u64::MAX - allocated);
    let redeemable_encumbered = encumbered + allocated;

    let free = if funded >= encumbered {
        funded - encumbered
    } else {
        0
    };
    let redeemable = if funded >= redeemable_encumbered {
        funded - redeemable_encumbered
    } else {
        0
    };

    cvlr_assert!(free <= funded);
    cvlr_assert!(redeemable <= funded);
    cvlr_assert!(redeemable <= free);

    cvlr_satisfy!(funded >= redeemable_encumbered);
}
