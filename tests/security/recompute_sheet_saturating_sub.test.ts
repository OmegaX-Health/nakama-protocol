// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Pre-mainnet pen-test PoC — finding PT-2026-04-27-12 (INFO).
// Severity: INFO (cosmetic only).
//
// Hypothesis: `recompute_sheet` (lib.rs:5678-5693) computes derived display
// fields `free` and `redeemable` with `saturating_sub`. Earlier static-analysis
// claimed this could mask insolvency. In fact, every place that mutates the
// underlying `funded`, `allocated`, `reserved`, etc. uses `checked_add` /
// `checked_sub`, so insolvency cannot be silently introduced through the
// money paths. The saturation only affects how `free`/`redeemable` are
// displayed when the protocol is already in a state where encumbered
// exceeds funded — at which point the system is already wrong, but not via
// this function.
//
// This test verifies BOTH halves of that nuance, so an audit reader can
// confirm the finding's exact scope.

import test from "node:test";
import assert from "node:assert/strict";
import { extractRustFunctionBody } from "./program_source.ts";

function extractFunctionBody(signaturePrefix: string): string {
  const match = /(?:pub\s+)?fn\s+(\w+)\s*\(/.exec(signaturePrefix);
  assert.ok(match, `signature ${signaturePrefix} should include a function name`);
  return extractRustFunctionBody(match[1]!);
}

test("[PT-12] recompute_sheet uses saturating_sub but only on derived display fields", () => {
  const body = extractFunctionBody("fn recompute_sheet(");

  // Confirm derived field computation uses saturating_sub against `funded`.
  const saturatingFreeMatch =
    /sheet\.free\s*=\s*sheet\.funded\.saturating_sub\(/.test(body);
  const saturatingRedeemableMatch =
    /sheet\.redeemable\s*=\s*sheet\.funded\.saturating_sub\(/.test(body);
  assert.ok(saturatingFreeMatch, "PT-12 base condition: free is saturating_sub against funded");
  assert.ok(
    saturatingRedeemableMatch,
    "PT-12 base condition: redeemable is saturating_sub against funded",
  );

  // Confirm encumbered itself is `checked_add`, not saturating — so any
  // overflow propagates as ArithmeticError and aborts the tx.
  assert.ok(
    /\.checked_add\(sheet\.claimable\)/.test(body) ||
      /\.checked_add\(sheet\.payable\)/.test(body) ||
      /\.checked_add\(sheet\.impaired\)/.test(body),
    "PT-12 mitigation: encumbered is computed via checked_add (overflow surfaces ArithmeticError)",
  );
});

test("[PT-12] book_inflow_sheet uses checked_add on the load-bearing `funded` field", () => {
  const body = extractFunctionBody("fn book_inflow_sheet(");
  assert.ok(
    /sheet\.funded\s*=\s*checked_add\(sheet\.funded,\s*amount\)/.test(body),
    "PT-12 mitigation: book_inflow_sheet uses checked_add on funded — saturation is display-only",
  );
});

test("[PT-12] money-out paths decrement vault.total_assets via checked_sub, not saturating_sub", () => {
  // Settlement and claim payout helpers must still use checked_sub directly
  // on the reserve asset totals after the fee-vault rail cleanup.
  const settleDelivery = extractFunctionBody("pub(crate) fn settle_delivery(");
  assert.ok(
    /\*domain_assets\s*=\s*checked_sub\(\*domain_assets,\s*amount\)\?/.test(settleDelivery),
    "PT-12 mitigation: settle_delivery must checked_sub domain_assets",
  );

  const directClaimPayout = extractFunctionBody("pub(crate) fn book_direct_claim_payout(");
  assert.ok(
    /\*domain_assets\s*=\s*checked_sub\(\*domain_assets,\s*amount\)\?/.test(directClaimPayout),
    "PT-12 mitigation: direct claim payout must checked_sub domain_assets",
  );
});
