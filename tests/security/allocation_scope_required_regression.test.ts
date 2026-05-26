// SPDX-License-Identifier: AGPL-3.0-or-later
//
// CSO-2026-05-04 regression: LP-allocation obligations must not be able to
// mutate global reserve state while omitting the pool/allocation scoped
// accounts. Otherwise reserve, release, settlement, or impairment flows could
// bypass allocation-level encumbrance and realized-PnL ledgers.

import test from "node:test";
import assert from "node:assert/strict";

import { extractRustFunctionBody, programSource } from "./program_source.ts";

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

test("[CSO-2026-05-07] obligation creation validates allocation scope before owed booking", () => {
  const body = extractRustFunctionBody("create_obligation");
  const scopeIndex = body.indexOf("validate_obligation_creation_scope(");
  const persistIndex = body.indexOf("let obligation = &mut ctx.accounts.obligation");
  const bookIndex = body.indexOf("book_owed(");

  assert(scopeIndex > 0, "create_obligation should call the LP scope validator");
  assert(persistIndex > scopeIndex, "scope should be validated before obligation persistence");
  assert(bookIndex > scopeIndex, "scope should be validated before any owed ledger mutation");
});

test("[CSO-2026-05-07] obligation creation scope rejects partial or stray LP accounts", () => {
  const body = extractRustFunctionBody("validate_obligation_creation_scope");

  assert.match(body, /let scope_requested = expected_liquidity_pool != ZERO_PUBKEY/);
  assert.match(body, /liquidity_pool\.is_some\(\)/);
  assert.match(body, /capital_class\.is_some\(\)/);
  assert.match(body, /allocation_position\.is_some\(\)/);
  assert.match(body, /pool_class_ledger\.is_some\(\)/);
  assert.match(body, /allocation_ledger\.is_some\(\)/);
  assert.match(body, /funding_line\.line_type != FUNDING_LINE_TYPE_LIQUIDITY_POOL_ALLOCATION/);
  assert.match(body, /!scope_requested[\s\S]+FundingLineTypeMismatch/);
  assert.match(body, /expected_liquidity_pool != ZERO_PUBKEY[\s\S]+expected_capital_class != ZERO_PUBKEY[\s\S]+expected_allocation_position != ZERO_PUBKEY/);
  assert.match(body, /liquidity_pool\.ok_or\(OmegaXProtocolError::LiquidityPoolMismatch\)/);
  assert.match(body, /capital_class\.ok_or\(OmegaXProtocolError::CapitalClassMismatch\)/);
  assert.match(body, /allocation_position\.ok_or\(OmegaXProtocolError::AllocationPositionMismatch\)/);
  assert.match(body, /pool_class_ledger\.is_some\(\)[\s\S]+CapitalClassMismatch/);
  assert.match(body, /allocation_ledger\.is_some\(\)[\s\S]+AllocationPositionMismatch/);
});

test("[CSO-2026-05-07] obligation creation scope binds pool class and allocation position", () => {
  const body = extractRustFunctionBody("validate_obligation_creation_scope");

  assert.match(body, /funding_line\.reserve_domain[\s\S]+health_plan\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(body, /funding_line\.health_plan[\s\S]+health_plan\.key\(\)[\s\S]+HealthPlanMismatch/);
  assert.match(body, /pool\.reserve_domain[\s\S]+health_plan\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(body, /pool\.deposit_asset_mint[\s\S]+funding_line\.asset_mint[\s\S]+AssetMintMismatch/);
  assert.match(body, /SEED_LIQUIDITY_POOL/);
  assert.match(body, /pool\.bump == expected_pool_bump/);
  assert.match(body, /class\.reserve_domain[\s\S]+health_plan\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(body, /class\.liquidity_pool[\s\S]+pool\.key\(\)[\s\S]+LiquidityPoolMismatch/);
  assert.match(body, /SEED_CAPITAL_CLASS/);
  assert.match(body, /class\.bump == expected_class_bump/);
  assert.match(body, /validate_optional_pool_class_ledger\([\s\S]+expected_capital_class[\s\S]+funding_line\.asset_mint/);
  assert.match(body, /validate_optional_allocation_position\([\s\S]+Some\(position\)[\s\S]+funding_line_key/);
  assert.match(body, /position\.reserve_domain[\s\S]+health_plan\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(body, /position\.health_plan[\s\S]+funding_line\.health_plan[\s\S]+HealthPlanMismatch/);
  assert.match(body, /position\.policy_series[\s\S]+funding_line\.policy_series[\s\S]+PolicySeriesMismatch/);
  assert.match(body, /position\.liquidity_pool[\s\S]+pool\.key\(\)[\s\S]+LiquidityPoolMismatch/);
  assert.match(body, /position\.capital_class[\s\S]+class\.key\(\)[\s\S]+CapitalClassMismatch/);
  assert.match(body, /require_liquidity_pool_active\(pool\)\?/);
  assert.match(body, /require_capital_class_active\(class\)\?/);
  assert.match(body, /require_allocation_position_allocatable\(position\)\?/);
  assert.match(body, /validate_optional_allocation_ledger\([\s\S]+expected_allocation_position[\s\S]+funding_line\.asset_mint/);
});

test("[CSO-2026-05-24] obligation creation scope blocks inactive or deallocation-only LP surfaces", () => {
  const body = extractRustFunctionBody("validate_obligation_creation_scope");
  const poolGuardIndex = body.indexOf("require_liquidity_pool_active(pool)?");
  const classGuardIndex = body.indexOf("require_capital_class_active(class)?");
  const positionGuardIndex = body.indexOf("require_allocation_position_allocatable(position)?");
  const ledgerValidationIndex = body.indexOf("validate_optional_allocation_ledger(");

  assert(poolGuardIndex > 0, "liquidity pool must be active for fresh LP obligation intake");
  assert(classGuardIndex > 0, "capital class must be active for fresh LP obligation intake");
  assert(
    positionGuardIndex > 0,
    "allocation position must be active and not deallocation-only for fresh LP obligation intake",
  );
  assert(
    poolGuardIndex < ledgerValidationIndex
      && classGuardIndex < ledgerValidationIndex
      && positionGuardIndex < ledgerValidationIndex,
    "lifecycle guards should run before allocation-ledger validation returns success",
  );
});

test("[CSO-2026-05-07] create obligation account context carries LP scope accounts", () => {
  assert.match(programSource, /pub struct CreateObligation<'info>[\s\S]+pub liquidity_pool: Option<Box<Account<'info, LiquidityPool>>>/);
  assert.match(programSource, /pub struct CreateObligation<'info>[\s\S]+pub capital_class: Option<Box<Account<'info, CapitalClass>>>/);
  assert.match(programSource, /pub struct CreateObligation<'info>[\s\S]+pub pool_class_ledger: Option<Box<Account<'info, PoolClassLedger>>>/);
  assert.match(programSource, /pub struct CreateObligation<'info>[\s\S]+pub allocation_position: Option<Box<Account<'info, AllocationPosition>>>/);
  assert.match(programSource, /pub struct CreateObligation<'info>[\s\S]+pub allocation_ledger: Option<Box<Account<'info, AllocationLedger>>>/);
});

test("[ALMANAX-059d57e3] impairment obligation accounts must be canonical and coherent", () => {
  const helperBody = extractRustFunctionBody("validate_obligation_binding");

  assert.match(helperBody, /Pubkey::find_program_address/);
  assert.match(helperBody, /SEED_OBLIGATION/);
  assert.match(helperBody, /expected_funding_line\.as_ref\(\)/);
  assert.match(helperBody, /obligation\.obligation_id\.as_bytes\(\)/);
  assert.match(helperBody, /obligation\.key\(\)[\s\S]+expected_obligation/);
  assert.match(helperBody, /obligation\.bump == expected_bump/);
  assert.match(helperBody, /obligation\.funding_line[\s\S]+expected_funding_line[\s\S]+FundingLineMismatch/);
  assert.match(helperBody, /obligation\.asset_mint[\s\S]+funding_line\.asset_mint[\s\S]+AssetMintMismatch/);
  assert.match(helperBody, /obligation\.reserve_domain[\s\S]+funding_line\.reserve_domain[\s\S]+ReserveDomainMismatch/);
  assert.match(helperBody, /obligation\.health_plan[\s\S]+funding_line\.health_plan[\s\S]+HealthPlanMismatch/);
  assert.match(helperBody, /obligation\.policy_series[\s\S]+funding_line\.policy_series[\s\S]+PolicySeriesMismatch/);
  assert.match(
    extractRustFunctionBody("validate_impairment_bindings"),
    /validate_obligation_binding\(obligation,\s*funding_line_key,\s*funding_line\)\?/,
  );
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
