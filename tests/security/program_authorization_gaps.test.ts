// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Defense regression tests for PT-2026-04-27-04 and PT-2026-04-27-07.
//
// Both findings shipped fixes in the on-chain program:
//   PT-04 — after the membership-account trim, `require_claim_intake_submitter`
//           allows claimant self-submit or plan operators for a nonzero
//           claimant. Recipient routing is handled by ClaimCase.delegate_recipient.
//   PT-07 — the standalone OracleProfile registry has been removed. The base
//           program no longer stores claim attestations, so there is no profile
//           metadata or on-chain claim-attestation surface for an attacker to squat.
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

test("[PT-04 defense] require_claim_intake_submitter operator branch requires a nonzero claimant", () => {
  const body = extractFunctionBody("fn require_claim_intake_submitter(");

  assert.ok(
    /claimant_present\s*=\s*claimant\s*!=\s*ZERO_PUBKEY/.test(body),
    "[PT-04 regression] gate must reject zero claimant",
  );
  assert.ok(
    /claimant_self_submit/.test(body),
    "[PT-04 regression] gate must preserve claimant self-submit",
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
    /claimant_present/.test(operatorExpr),
    `[PT-04 regression] operator_submit must require claimant_present. Got: ${operatorExpr.trim()}`,
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

test("[PT-07 defense] claim attestation surface stays removed from the base program", () => {
  assert.ok(
    !/\bpub\s+fn\s+attest_claim_case\s*\(/.test(programSrc),
    "[PT-07 regression] attest_claim_case should not be part of the live base program",
  );
  assert.ok(
    !/\bClaimAttestation\b/.test(programSrc),
    "[PT-07 regression] ClaimAttestation state should stay removed",
  );
  assert.ok(
    !/\brequire_claim_attestation_oracle_authority\b/.test(programSrc),
    "[PT-07 regression] attestation-specific oracle gate should stay removed",
  );
});
