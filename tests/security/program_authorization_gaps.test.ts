// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Defense regression tests for PT-2026-04-27-04 and PT-2026-04-27-07.
//
// Both findings shipped fixes in the on-chain program:
//   PT-04 — `require_claim_intake_submitter` (lib.rs:5166-) now requires
//           `args.claimant == member_position.wallet` in BOTH the member
//           self-submit and operator-submit branches. Recipient routing is
//           handled by the new ClaimCase.delegate_recipient field.
//   PT-07 — the standalone OracleProfile registry has been removed. Claim
//           attestations are authorized directly against HealthPlan.oracle_authority,
//           so there is no profile metadata surface for an attacker to squat.
//
// These tests now act as defense regressions: each one PASSES while the
// defense remains in place and FAILS if the constraint is removed or
// regressed. Originally these were "vulnerability present" tests; flipped
// post-fix per the remediation plan.

import test from "node:test";
import assert from "node:assert/strict";
import { extractRustFunctionBody, programSource as programSrc } from "./program_source.ts";

function extractFunctionBody(signaturePrefix: string): string {
  const match = /(?:pub\s+)?fn\s+(\w+)\s*\(/.exec(signaturePrefix);
  assert.ok(match, `signature ${signaturePrefix} should include a function name`);
  return extractRustFunctionBody(match[1]!);
}

test("[PT-04 defense] require_claim_intake_submitter operator branch constrains args.claimant", () => {
  const body = extractFunctionBody("fn require_claim_intake_submitter(");

  // Both branches must compare args.claimant to member_position.wallet so
  // operator-routed claim diversion is impossible by construction.
  assert.ok(
    /args\.claimant\s*==\s*member_position\.wallet/.test(body),
    "[PT-04 regression] gate must compare args.claimant to member_position.wallet",
  );

  assert.ok(
    /plan\.claims_operator/.test(body) && /plan\.plan_admin/.test(body),
    "[PT-04 regression] operator branch must reference claims_operator and plan_admin",
  );

  // Defense: the operator_submit boolean must reference the claimant
  // constraint either inline or via an extracted local. If a future change
  // removes claimant reference from the operator branch, this fails.
  const operatorLineMatch =
    /let\s+operator_submit\s*=\s*([\s\S]+?);/.exec(body);
  assert.ok(
    operatorLineMatch,
    "[PT-04 regression] operator_submit boolean must be defined",
  );
  const operatorExpr = operatorLineMatch[1];
  assert.ok(
    /claimant/.test(operatorExpr),
    `[PT-04 regression] operator_submit must reference claimant constraint. Got: ${operatorExpr.trim()}`,
  );
});

test("[PT-04] open_claim_case persists args.claimant verbatim onto claim_case state", () => {
  // From lib.rs:1251 — `claim_case.claimant = args.claimant;`
  // This is the data path that primes the diversion when settlement transfers
  // are added: a claims_operator submits with attacker `args.claimant`, the
  // ClaimCase records that pubkey, and any future SPL CPI keyed off that
  // field would route funds to the attacker.
  const body = extractFunctionBody("pub fn open_claim_case(");
  assert.ok(
    /claim_case\.claimant\s*=\s*args\.claimant\s*;/.test(body),
    "PT-04 evidence: open_claim_case must assign claim_case.claimant = args.claimant",
  );
});

test("[PT-07 defense] oracle profile registry surface stays removed", () => {
  assert.ok(
    !/\bpub\s+fn\s+register_oracle\s*\(/.test(programSrc),
    "[PT-07 regression] register_oracle should not be part of the live program",
  );
  assert.ok(
    !/\bpub\s+fn\s+claim_oracle\s*\(/.test(programSrc),
    "[PT-07 regression] claim_oracle should not be part of the live program",
  );
  assert.ok(
    !/\bOracleProfile\b/.test(programSrc),
    "[PT-07 regression] OracleProfile state should stay removed",
  );
});

test("[PT-07 defense] claim attestations are gated by the plan oracle authority", () => {
  const body = extractFunctionBody("fn require_claim_attestation_oracle_authority(");
  assert.ok(
    /require_keys_eq!\([\s\S]*?oracle[\s\S]*?health_plan\.oracle_authority/s.test(body),
    "[PT-07 regression] attestation gate must require oracle == health_plan.oracle_authority",
  );
});
