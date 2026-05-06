// SPDX-License-Identifier: AGPL-3.0-or-later
//
// CSO-2026-05-04 regression: LP-allocation obligations must not be able to
// mutate global reserve state while omitting the pool/allocation scoped
// accounts. Otherwise reserve, release, settlement, or impairment flows could
// bypass allocation-level encumbrance and realized-PnL ledgers.

import test from "node:test";
import assert from "node:assert/strict";

import { extractRustFunctionBody } from "./program_source.ts";

test("[CSO-2026-05-04] treasury mutation bindings require allocation scope accounts", () => {
  const body = extractRustFunctionBody("validate_treasury_mutation_bindings");

  assert.match(body, /let allocation_scoped = obligation\.liquidity_pool != ZERO_PUBKEY/);
  assert.match(body, /obligation\.capital_class != ZERO_PUBKEY/);
  assert.match(body, /obligation\.allocation_position != ZERO_PUBKEY/);
  assert.match(body, /pool_class_ledger\.is_some\(\)[\s\S]+CapitalClassMismatch/);
  assert.match(body, /allocation_position\.is_some\(\) && allocation_ledger\.is_some\(\)[\s\S]+AllocationPositionMismatch/);
  assert.match(body, /position\.liquidity_pool[\s\S]+obligation\.liquidity_pool[\s\S]+LiquidityPoolMismatch/);
  assert.match(body, /position\.capital_class[\s\S]+obligation\.capital_class[\s\S]+CapitalClassMismatch/);
  assert.match(body, /position\.health_plan[\s\S]+obligation\.health_plan[\s\S]+HealthPlanMismatch/);
});

test("[CSO-2026-05-06] optional reserve and allocation accounts must be canonical PDAs", () => {
  const seriesBody = extractRustFunctionBody("validate_optional_series_ledger");
  assert.match(seriesBody, /Pubkey::find_program_address/);
  assert.match(seriesBody, /SEED_SERIES_RESERVE_LEDGER/);
  assert.match(seriesBody, /ledger\.key\(\)[\s\S]+expected_ledger/);
  assert.match(seriesBody, /ledger\.bump == expected_bump/);

  const poolClassBody = extractRustFunctionBody("validate_optional_pool_class_ledger");
  assert.match(poolClassBody, /Pubkey::find_program_address/);
  assert.match(poolClassBody, /SEED_POOL_CLASS_LEDGER/);
  assert.match(poolClassBody, /ledger\.key\(\)[\s\S]+expected_ledger/);
  assert.match(poolClassBody, /ledger\.bump == expected_bump/);

  const allocationPositionBody = extractRustFunctionBody("validate_optional_allocation_position");
  assert.match(allocationPositionBody, /Pubkey::find_program_address/);
  assert.match(allocationPositionBody, /SEED_ALLOCATION_POSITION/);
  assert.match(allocationPositionBody, /position\.key\(\)[\s\S]+expected_position/);
  assert.match(allocationPositionBody, /position\.bump == expected_bump/);

  const allocationLedgerBody = extractRustFunctionBody("validate_optional_allocation_ledger");
  assert.match(allocationLedgerBody, /Pubkey::find_program_address/);
  assert.match(allocationLedgerBody, /SEED_ALLOCATION_LEDGER/);
  assert.match(allocationLedgerBody, /ledger\.key\(\)[\s\S]+expected_ledger/);
  assert.match(allocationLedgerBody, /ledger\.bump == expected_bump/);
});

test("[CSO-2026-05-04] reserve, release, and settlement share the strict binding gate", () => {
  assert.match(extractRustFunctionBody("reserve_obligation"), /validate_treasury_mutation_bindings\(/);
  assert.match(extractRustFunctionBody("release_reserve"), /validate_treasury_mutation_bindings\(/);
  assert.match(extractRustFunctionBody("settle_obligation"), /validate_treasury_mutation_bindings\(/);
});

test("[CSO-2026-05-04] allocation-scoped settlement does not debit capacity ledgers as funded custody", () => {
  const body = extractRustFunctionBody("settle_delivery");

  assert.match(body, /let allocation_scoped = allocation_position\.is_some\(\) \|\| allocation_sheet\.is_some\(\)/);
  assert.match(body, /settle_from_allocation_sheet\(plan_sheet/);
  assert.match(body, /settle_from_allocation_sheet\(line_sheet/);
  assert.match(body, /settle_from_allocation_sheet\(&mut series\.sheet/);
  assert.match(body, /settle_from_allocation_sheet\(&mut ledger\.sheet/);
});

test("[CSO-2026-05-04] standalone LP-allocation impairments require scoped accounts", () => {
  const body = extractRustFunctionBody("validate_impairment_bindings");

  assert.match(body, /funding_line\.line_type == FUNDING_LINE_TYPE_LIQUIDITY_POOL_ALLOCATION/);
  assert.match(body, /pool_class_ledger\.is_some\(\)[\s\S]+CapitalClassMismatch/);
  assert.match(body, /allocation_position\.is_some\(\) && allocation_ledger\.is_some\(\)[\s\S]+AllocationPositionMismatch/);
  assert.match(body, /position\.reserve_domain[\s\S]+funding_line\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(body, /position\.health_plan[\s\S]+funding_line\.health_plan[\s\S]+HealthPlanMismatch/);
  assert.match(body, /position\.policy_series[\s\S]+funding_line\.policy_series[\s\S]+PolicySeriesMismatch/);
  assert.match(body, /position\.active[\s\S]+AllocationPositionMismatch/);
});
