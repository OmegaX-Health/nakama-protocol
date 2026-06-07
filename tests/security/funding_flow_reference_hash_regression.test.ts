// SPDX-License-Identifier: AGPL-3.0-or-later

import test from "node:test";
import assert from "node:assert/strict";

import { extractRustFunctionBody, programSource } from "./program_source.ts";

test("[audit] funding flow events carry off-chain reference hashes", () => {
  assert.match(
    programSource,
    /pub struct FundingFlowRecordedEvent\s*\{[^}]*reference_hash:\s*\[u8;\s*32\]/s,
    "FundingFlowRecordedEvent must expose a 32-byte reference_hash in the public IDL surface",
  );

  const depositBody = extractRustFunctionBody("deposit_reserve_capital");
  assert.match(
    depositBody,
    /reference_hash:\s*args\.terms_hash/,
    "reserve-capital deposits must emit the contribution terms hash",
  );

  const returnBody = extractRustFunctionBody("return_reserve_capital");
  assert.doesNotMatch(
    returnBody,
    /let\s+_\s*=\s*args\.reason_hash/,
    "capital-return reason_hash must not be silently discarded",
  );
  assert.match(
    returnBody,
    /reference_hash:\s*args\.reason_hash/,
    "reserve-capital returns must emit the supplied reason hash",
  );

  const earningsBody = extractRustFunctionBody("record_reserve_earnings");
  assert.match(
    earningsBody,
    /require_nonzero_hash\(\s*&args\.earnings_ref_hash/s,
    "reserve earnings must keep requiring a nonzero off-chain reference hash",
  );
  assert.match(
    earningsBody,
    /reference_hash:\s*args\.earnings_ref_hash/,
    "reserve earnings must emit the supplied earnings reference hash",
  );
});
