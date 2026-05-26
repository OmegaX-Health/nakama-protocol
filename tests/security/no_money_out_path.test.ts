// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Pre-mainnet pen-test defense regression — findings PT-2026-04-27-01 / 02.
// Original severity: CRITICAL.
//
// Historical hypothesis: the on-chain program accepted SPL token deposits but
// had no instruction that released tokens back out. All "settle / process /
// release" instructions updated ledger state but called no `transfer_checked`
// CPI.
//
// Current role of this file: pin the remediation. It now asserts that real
// money-out handlers call `transfer_from_domain_vault`, and that fee withdrawal
// instructions remain present in the IDL.
//
// `release_reserve` remains accounting-only by design: it releases reserved
// capacity back to free reserve and does not move SPL tokens.

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  extractRustFunctionBody,
  findEnclosingRustFunctionName,
  programSource,
} from "./program_source.ts";

const idl = JSON.parse(
  readFileSync(new URL("../../idl/omegax_protocol.json", import.meta.url), "utf8"),
) as { instructions: Array<{ name: string }> };

const extractInstructionBody = extractRustFunctionBody;

test("[PT-01 defense regression] IDL exposes the 6 expected fee-vault withdrawal instructions", () => {
  // Phase 1.7 (PR2) shipped 6 withdraw_*_fee_* instructions, fully closing
  // PT-01 on the protocol-fee / pool-treasury / pool-oracle rails. This
  // assertion was flipped from VULN_CONFIRMED to a defense regression: if
  // any of the six are removed, the original "no money-out path" finding
  // would re-emerge for that rail.
  const drainPatterns = /^(withdraw|sweep|collect_fee|reclaim|payout)/i;
  const matches = idl.instructions
    .map((ix) => ix.name)
    .filter((name) => drainPatterns.test(name))
    .sort();

  const expected = [
    "withdraw_pool_oracle_fee_sol",
    "withdraw_pool_oracle_fee_spl",
    "withdraw_pool_treasury_sol",
    "withdraw_pool_treasury_spl",
    "withdraw_protocol_fee_sol",
    "withdraw_protocol_fee_spl",
  ];
  assert.deepEqual(
    matches,
    expected,
    "[PT-01 defense] expected exactly the 6 Phase 1.7 fee-vault withdraw instructions; removal or addition would change the protocol's outflow surface and warrants security review.",
  );
});

test("[PT-02 defense] settle_claim_case + process_redemption_queue + settle_obligation call transfer_from_domain_vault", () => {
  // All three money-out instruction handlers are wired. settle_obligation
  // does the CPI conditionally (only when claim_case is linked AND outflow
  // accounts are supplied) — the body still contains the helper call site,
  // so the source-pattern test is satisfied either way.
  //
  // Note: release_reserve is NOT a money-out path despite its name. It is a
  // pure accounting operation that returns reserved capital to the free pool
  // (status becomes CANCELED if reserved hits zero). It is intentionally
  // excluded from this defense test.
  const wired = [
    "settle_claim_case",
    "settle_claim_case_selected_asset",
    "process_redemption_queue",
    "settle_obligation",
  ];
  for (const handler of wired) {
    const body = extractInstructionBody(handler);
    assert.ok(
      /transfer_from_domain_vault\s*\(/.test(body),
      `[PT-02 regression] ${handler} must call transfer_from_domain_vault`,
    );
  }
});

test("[PT-02] The only token CPI lives in transfer_to_domain_vault and is inflow-only", () => {
  // Locate the helper.
  assert.ok(
    /fn\s+transfer_to_domain_vault\s*</.test(programSource),
    "transfer_to_domain_vault helper must exist",
  );

  // Locate every callsite of transfer_to_domain_vault. Expect they live only in
  // remaining protocol inflow handlers.
  const callsiteLines = programSource
    .split("\n")
    .map((line, idx) => ({ line, lineno: idx + 1 }))
    .filter(({ line }) => /transfer_to_domain_vault\s*\(/.test(line))
    // Filter out the function definition itself.
    .filter(({ line }) => !/fn\s+transfer_to_domain_vault/.test(line));

  // Group callsites by enclosing handler by walking back to the nearest `pub fn ...`.
  const expectedInflowHandlers = new Set([
    "fund_sponsor_budget",
    "record_premium_payment",
    "deposit_into_capital_class",
  ]);
  const lines = programSource.split("\n");
  const violations: Array<{ lineno: number; handler: string }> = [];
  for (const callsite of callsiteLines) {
    const handler = findEnclosingRustFunctionName(lines, callsite.lineno) ?? "<unknown>";
    if (!expectedInflowHandlers.has(handler)) {
      violations.push({ lineno: callsite.lineno, handler });
    }
  }

  assert.deepEqual(
    violations,
    [],
    `Token CPI must only appear in inflow handlers; finding PT-02 would change if otherwise. Got: ${JSON.stringify(violations, null, 2)}`,
  );

  // Sanity: all three expected inflow handlers must in fact use the helper.
  const handlersWithCpi = new Set(
    callsiteLines.map(({ lineno }) => {
      return findEnclosingRustFunctionName(lines, lineno) ?? "<unknown>";
    }),
  );
  for (const h of expectedInflowHandlers) {
    assert.ok(
      handlersWithCpi.has(h),
      `Expected inflow handler ${h} to call transfer_to_domain_vault`,
    );
  }
});
