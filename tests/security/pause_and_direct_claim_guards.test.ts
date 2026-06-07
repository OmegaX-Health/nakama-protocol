// SPDX-License-Identifier: AGPL-3.0-or-later

import assert from "node:assert/strict";
import { test } from "node:test";

import { extractRustFunctionBody, programSource } from "./program_source.ts";

test("[AUDIT-2026-06-07] money-state handlers enforce plan pause gates", () => {
  const expectedCalls: Array<[string, RegExp]> = [
    ["fund_sponsor_budget", /require_reserve_rails_open\(&ctx\.accounts\.health_plan\)\?/],
    ["record_premium_payment", /require_reserve_rails_open\(&ctx\.accounts\.health_plan\)\?/],
    ["deposit_reserve_capital", /require_capital_subscriptions_open\(&ctx\.accounts\.health_plan\)\?/],
    ["return_reserve_capital", /require_reserve_redemptions_open\(&ctx\.accounts\.health_plan\)\?/],
    ["record_reserve_earnings", /require_reserve_rails_open\(&ctx\.accounts\.health_plan\)\?/],
    ["create_obligation", /require_plan_operations_open\(&ctx\.accounts\.health_plan\)\?/],
    ["reserve_obligation", /require_claim_finality_open\(&ctx\.accounts\.health_plan\)\?/],
    ["release_reserve", /require_reserve_rails_open\(&ctx\.accounts\.health_plan\)\?/],
    ["settle_obligation", /require_claim_finality_open\(&ctx\.accounts\.health_plan\)\?/],
    ["open_claim_case", /require_claim_intake_open\(&ctx\.accounts\.health_plan\)\?/],
    ["adjudicate_claim_case", /require_claim_finality_open\(&ctx\.accounts\.health_plan\)\?/],
    ["settle_claim_case", /require_claim_finality_open\(&ctx\.accounts\.health_plan\)\?/],
  ];

  for (const [handler, pattern] of expectedCalls) {
    assert.match(
      extractRustFunctionBody(handler),
      pattern,
      `${handler} should call its plan pause guard before money or claim-finality state moves`,
    );
  }
});

test("[AUDIT-2026-06-07] direct free-reserve claim settlement is not claims-operator-only", () => {
  assert.match(programSource, /fn require_direct_claim_settlement_control\(/);
  assert.match(extractRustFunctionBody("settle_claim_case"), /require_direct_claim_settlement_control\(/);

  const directControlBody = extractRustFunctionBody("require_direct_claim_settlement_control");
  assert.match(directControlBody, /\*authority\s*==\s*plan\.plan_admin/);
  assert.doesNotMatch(directControlBody, /plan\.claims_operator/);
});
