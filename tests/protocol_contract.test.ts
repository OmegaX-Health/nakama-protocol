import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import contractModule from "../frontend/lib/generated/protocol-contract.ts";

const {
  PROTOCOL_INSTRUCTION_ARGS,
  PROTOCOL_ACCOUNT_DISCRIMINATORS,
  PROTOCOL_INSTRUCTION_ACCOUNTS,
  PROTOCOL_INSTRUCTION_DISCRIMINATORS,
} = contractModule as typeof import("../frontend/lib/generated/protocol-contract.ts");

test("canonical contract exposes the reserve-accounting surface", () => {
  const instructionNames = Object.keys(PROTOCOL_INSTRUCTION_DISCRIMINATORS);
  const accountNames = Object.keys(PROTOCOL_ACCOUNT_DISCRIMINATORS);
  const serializedAccounts = JSON.stringify(PROTOCOL_INSTRUCTION_ACCOUNTS);
  const idl = JSON.parse(readFileSync(new URL("../idl/omegax_protocol.json", import.meta.url), "utf8")) as {
    instructions: Array<{ name: string }>;
    types: Array<{ name: string; type: { kind: string; fields?: Array<{ name: string }> } }>;
  };
  const configureReserveAssetRailArgs = idl.types.find((entry) => entry.name === "ConfigureReserveAssetRailArgs");
  const reserveAssetRailAccount = idl.types.find((entry) => entry.name === "ReserveAssetRail");
  const selectedAssetPayoutArgs = idl.types.find((entry) => entry.name === "SettleClaimCaseSelectedAssetArgs");
  const claimCaseAccount = idl.types.find((entry) => entry.name === "ClaimCase");
  const claimAttestationAccount = idl.types.find((entry) => entry.name === "ClaimAttestation");

  assert(!instructionNames.includes("initialize_protocol_governance"));
  assert(!instructionNames.includes("set_protocol_emergency_pause"));
  assert(!instructionNames.includes("rotate_protocol_governance_authority"));
  assert(!instructionNames.includes("accept_protocol_governance_authority"));
  assert(!instructionNames.includes("cancel_protocol_governance_authority_transfer"));
  assert(instructionNames.includes("create_reserve_domain"));
  assert(instructionNames.includes("create_health_plan"));
  assert(instructionNames.includes("create_policy_series"));
  assert(instructionNames.includes("initialize_series_reserve_ledger"));
  assert(instructionNames.includes("open_funding_line"));
  assert(!instructionNames.includes("register_oracle"));
  assert(!instructionNames.includes("claim_oracle"));
  assert(!instructionNames.includes("update_oracle_profile"));
  assert(!instructionNames.includes("set_pool_oracle"));
  assert(!instructionNames.includes("set_pool_oracle_permissions"));
  assert(!instructionNames.includes("set_pool_oracle_policy"));
  assert(!instructionNames.includes("register_outcome_schema"));
  assert(!instructionNames.includes("verify_outcome_schema"));
  assert(!instructionNames.includes("backfill_schema_dependency_ledger"));
  assert(!instructionNames.includes("close_outcome_schema"));
  assert(instructionNames.includes("attest_claim_case"));
  assert(!instructionNames.includes("settle_claim_case_selected_asset"));

  for (const removedInstruction of [
    "init_protocol_fee_vault",
    "init_pool_treasury_vault",
    "init_pool_oracle_fee_vault",
    "withdraw_protocol_fee_sol",
    "withdraw_protocol_fee_spl",
    "withdraw_pool_treasury_sol",
    "withdraw_pool_treasury_spl",
    "withdraw_pool_oracle_fee_sol",
    "withdraw_pool_oracle_fee_spl",
    "create_liquidity_pool",
    "create_capital_class",
    "update_capital_class_controls",
    "deposit_into_capital_class",
    "update_lp_position_credentialing",
    "request_redemption",
    "process_redemption_queue",
    "create_allocation_position",
    "update_allocation_caps",
    "allocate_capital",
    "deallocate_capital",
    "mark_impairment",
    "register_oracle",
    "claim_oracle",
    "update_oracle_profile",
  ]) {
    assert(!instructionNames.includes(removedInstruction), `${removedInstruction} should be removed`);
  }

  assert(accountNames.includes("ReserveDomain"));
  assert(accountNames.includes("HealthPlan"));
  assert(accountNames.includes("PolicySeries"));
  assert(accountNames.includes("FundingLine"));
  assert(accountNames.includes("Obligation"));
  assert(!accountNames.includes("OracleProfile"));
  assert(!accountNames.includes("PoolOracleApproval"));
  assert(!accountNames.includes("PoolOraclePolicy"));
  assert(!accountNames.includes("PoolOraclePermissionSet"));
  assert(!accountNames.includes("OutcomeSchema"));
  assert(!accountNames.includes("SchemaDependencyLedger"));
  assert(accountNames.includes("ClaimAttestation"));

  for (const removedAccount of [
    "ProtocolGovernance",
    "ProtocolFeeVault",
    "PoolTreasuryVault",
    "PoolOracleFeeVault",
    "LiquidityPool",
    "CapitalClass",
    "LPPosition",
    "PoolClassLedger",
    "AllocationPosition",
    "AllocationLedger",
    "OracleProfile",
  ]) {
    assert(!accountNames.includes(removedAccount), `${removedAccount} should be removed`);
  }
  assert(!serializedAccounts.includes("protocol_governance"));
  assert(!serializedAccounts.includes("protocol_fee_vault"));
  assert(!serializedAccounts.includes("pool_treasury_vault"));
  assert(!serializedAccounts.includes("pool_oracle_fee_vault"));
  for (const accountName of [
    "oracle",
    "health_plan",
    "claim_case",
    "funding_line",
    "claim_attestation",
  ]) {
    assert(
      PROTOCOL_INSTRUCTION_ACCOUNTS.attest_claim_case.some((account) => account.name === accountName),
      `attest_claim_case missing ${accountName}`,
    );
  }
  for (const removedAccount of [
    "liquidity_pool",
    "capital_class",
    "allocation_position",
    "pool_oracle_approval",
    "pool_oracle_permission_set",
    "pool_oracle_policy",
    "oracle_profile",
  ]) {
    assert(
      !PROTOCOL_INSTRUCTION_ACCOUNTS.attest_claim_case.some((account) => account.name === removedAccount),
      `attest_claim_case should not carry ${removedAccount}`,
    );
  }

  assert(!instructionNames.includes("create_pool"));
  assert(!instructionNames.includes("set_pool_status"));
  assert(!serializedAccounts.includes("pool_type"));
  assert(!serializedAccounts.includes("membership_anchor_seat"));
  assert(!accountNames.includes("MembershipAnchorSeat"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.reserve_obligation.some((account) => account.name === "claim_case"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.release_reserve.some((account) => account.name === "claim_case"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.settle_obligation.some((account) => account.name === "claim_case"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.settle_obligation.some((account) => account.name === "reserve_asset_rail"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.settle_claim_case.some((account) => account.name === "reserve_asset_rail"));
  assert(!Object.prototype.hasOwnProperty.call(PROTOCOL_INSTRUCTION_ACCOUNTS, "settle_claim_case_selected_asset"));
  for (const accountName of [
    "liquidity_pool",
    "capital_class",
    "pool_class_ledger",
    "allocation_position",
    "allocation_ledger",
  ]) {
    assert(
      !PROTOCOL_INSTRUCTION_ACCOUNTS.create_obligation.some((account) => account.name === accountName),
      `create_obligation should not carry ${accountName}`,
    );
  }
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.reserve_obligation.find((account) => account.name === "claim_case")?.pdaSeeds);
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.release_reserve.find((account) => account.name === "claim_case")?.pdaSeeds);
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.settle_obligation.find((account) => account.name === "claim_case")?.pdaSeeds);
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.fund_sponsor_budget.some((account) => account.name === "source_token_account"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.fund_sponsor_budget.some((account) => account.name === "vault_token_account"));
  assert(PROTOCOL_INSTRUCTION_ACCOUNTS.record_premium_payment.some((account) => account.name === "token_program"));
  assert(configureReserveAssetRailArgs?.type.fields?.some((field) => field.name === "max_confidence_bps"));
  assert(reserveAssetRailAccount?.type.fields?.some((field) => field.name === "max_confidence_bps"));
  assert(!selectedAssetPayoutArgs);
  assert(claimCaseAccount?.type.fields?.some((field) => field.name === "attestation_count"));
  for (const fieldName of [
    "evidence_ref_hash",
    "decision_support_hash",
  ]) {
    assert(
      claimAttestationAccount?.type.fields?.some((field) => field.name === fieldName),
      `ClaimAttestation missing ${fieldName}`,
    );
  }
  for (const removedFieldName of [
    "oracle_profile",
    "schema_key_hash",
    "schema_hash",
    "schema_version",
  ]) {
    assert(
      !claimAttestationAccount?.type.fields?.some((field) => field.name === removedFieldName),
      `ClaimAttestation should not carry ${removedFieldName}`,
    );
  }
  assert(!claimAttestationAccount?.type.fields?.some((field) => field.name === "liquidity_pool"));
  assert(!claimAttestationAccount?.type.fields?.some((field) => field.name === "allocation_position"));
});
