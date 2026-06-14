// SPDX-License-Identifier: AGPL-3.0-or-later

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

import { loadEnvFile } from "./support/load_env_file.ts";

type ProtocolModule = typeof import("../frontend/lib/protocol.ts");
type FixturesModule = typeof import("../frontend/lib/devnet-fixtures.ts");
type ModuleWithDefault<T> = T & { default?: T };

const FRONTEND_ENV_PATH = resolve(process.cwd(), "frontend/.env.local");
const OUTPUT_DIR = resolve(process.cwd(), "devnet");
const MANIFEST_PATH = resolve(OUTPUT_DIR, "health-capital-markets-manifest.json");
const ENV_PATH = resolve(OUTPUT_DIR, "health-capital-markets.env");
const PROTOCOL_CONTRACT_PATH = resolve(process.cwd(), "shared/protocol_contract.json");

let protocolModule: ProtocolModule;
let fixturesModule: FixturesModule;

function writeFile(path: string, content: string): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content);
}

function stringify(value: unknown): string {
  return JSON.stringify(
    value,
    (_key, currentValue) => (typeof currentValue === "bigint" ? currentValue.toString() : currentValue),
    2,
  );
}

function checkedInProgramId(): string {
  const contract = JSON.parse(readFileSync(PROTOCOL_CONTRACT_PATH, "utf8")) as { programId?: string };
  if (!contract.programId) {
    throw new Error("shared/protocol_contract.json is missing programId.");
  }
  return contract.programId;
}

async function importRuntimeModule<T>(path: string): Promise<T> {
  const module = await import(path) as ModuleWithDefault<T>;
  return (module.default ?? module) as T;
}

function envLines(): string[] {
  const { DEVNET_PROTOCOL_FIXTURE_STATE, DEFAULT_HEALTH_PLAN_ADDRESS } = fixturesModule;
  const { getProgramId } = protocolModule;
  const primaryPlan = DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans[0]!;
  return [
    `NEXT_PUBLIC_PROTOCOL_PROGRAM_ID=${getProgramId().toBase58()}`,
    `NEXT_PUBLIC_DEVNET_SETTLEMENT_MINT=${DEVNET_PROTOCOL_FIXTURE_STATE.settlementMint}`,
    `NEXT_PUBLIC_DEVNET_REWARD_MINT=${DEVNET_PROTOCOL_FIXTURE_STATE.rewardMint}`,
    `NEXT_PUBLIC_DEVNET_WRAPPER_SETTLEMENT_MINT=${DEVNET_PROTOCOL_FIXTURE_STATE.wrapperSettlementMint}`,
    `NEXT_PUBLIC_DEFAULT_HEALTH_PLAN_ADDRESS=${DEFAULT_HEALTH_PLAN_ADDRESS}`,
    `NEXT_PUBLIC_PRIMARY_RESERVE_DOMAIN=${DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains[0]!.address}`,
    `NEXT_PUBLIC_PRIMARY_HEALTH_PLAN_ID=${primaryPlan.planId}`,
  ];
}

function derivedDomainAssetScopes() {
  const { DEVNET_PROTOCOL_FIXTURE_STATE } = fixturesModule;
  const { deriveDomainAssetVaultPda } = protocolModule;
  const keyedScopes = new Map<string, {
    address: string;
    assetMint: string;
    reserveDomain: string;
  }>();

  const addScope = (reserveDomain: string, assetMint: string) => {
    const key = `${reserveDomain}:${assetMint}`;
    if (keyedScopes.has(key)) return;
    keyedScopes.set(key, {
      reserveDomain,
      assetMint,
      address: deriveDomainAssetVaultPda({ reserveDomain, assetMint }).toBase58(),
    });
  };

  for (const scope of DEVNET_PROTOCOL_FIXTURE_STATE.domainAssetVaults) {
    addScope(scope.reserveDomain, scope.assetMint);
  }
  for (const line of DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines) {
    addScope(line.reserveDomain, line.assetMint);
  }

  return [...keyedScopes.values()].sort((left, right) =>
    `${left.reserveDomain}:${left.assetMint}`.localeCompare(`${right.reserveDomain}:${right.assetMint}`),
  );
}

function derivedDomainAssetLedgers() {
  const { DEVNET_PROTOCOL_FIXTURE_STATE } = fixturesModule;
  const { deriveDomainAssetLedgerPda } = protocolModule;
  return derivedDomainAssetScopes().map((scope) => {
    const existing = DEVNET_PROTOCOL_FIXTURE_STATE.domainAssetLedgers.find((row) =>
      row.reserveDomain === scope.reserveDomain && row.assetMint === scope.assetMint
    );
    return {
      address: deriveDomainAssetLedgerPda({
        reserveDomain: scope.reserveDomain,
        assetMint: scope.assetMint,
      }).toBase58(),
      reserveDomain: scope.reserveDomain,
      assetMint: scope.assetMint,
      ...(existing?.sheet ? { sheet: existing.sheet } : {}),
    };
  });
}

function manifest() {
  const { DEVNET_PROTOCOL_FIXTURE_STATE } = fixturesModule;
  const { getProgramId } = protocolModule;
  return {
    generatedAt: new Date().toISOString(),
    programId: getProgramId().toBase58(),
    migrationMode: "hard_break_devnet",
    liveBootstrapSurface: [
      "reserve_domains",
      "domain_asset_vaults",
      "health_plans",
      "policy_series",
      "funding_lines",
      "capital_contributions",
      "claim_cases",
      "obligations",
    ],
    retiredLegacySeedsToIgnore: [
      "pool",
      "pool_terms",
      "pool_liquidity_config",
      "pool_capital_class",
      "pool_treasury_reserve",
      "pool_oracle_policy",
      "pool_control_authority",
      "pool_automation_policy",
    ],
    steps: [
      "Ignore or archive retired pre-rearchitecture devnet accounts by retired seed prefix.",
      "Create reserve domains before any plan or liability state.",
      "Create domain asset vaults and ledgers per [reserve_domain, asset_mint].",
      "Create health plans and policy series with immutable live economic semantics.",
      "Open funding lines for sponsor budgets, premiums, backstop capital, and subsidies.",
      "Seed proof-fingerprinted claim anchors for audit and frontend smoke coverage.",
      "Keep retired LP, capital-class, allocation, member-seat, oracle-registry, and schema-registry data as fixture-only historical context.",
    ],
    reserveDomains: DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains,
    domainAssetVaults: derivedDomainAssetScopes(),
    domainAssetLedgers: derivedDomainAssetLedgers(),
    healthPlans: DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans,
    policySeries: DEVNET_PROTOCOL_FIXTURE_STATE.policySeries,
    fundingLines: DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines,
    obligations: DEVNET_PROTOCOL_FIXTURE_STATE.obligations,
    claimCases: DEVNET_PROTOCOL_FIXTURE_STATE.claimCases,
    capitalContributions: DEVNET_PROTOCOL_FIXTURE_STATE.capitalContributions,
    retiredFixtureOnly: {
      memberPositions: DEVNET_PROTOCOL_FIXTURE_STATE.memberPositions,
      liquidityPools: DEVNET_PROTOCOL_FIXTURE_STATE.liquidityPools,
      capitalClasses: DEVNET_PROTOCOL_FIXTURE_STATE.capitalClasses,
      lpPositions: DEVNET_PROTOCOL_FIXTURE_STATE.lpPositions,
      allocationPositions: DEVNET_PROTOCOL_FIXTURE_STATE.allocationPositions,
    },
    legacyArtifactsRetired: DEVNET_PROTOCOL_FIXTURE_STATE.legacyArtifactsRetired,
  };
}

async function main() {
  loadEnvFile(ENV_PATH);
  loadEnvFile(FRONTEND_ENV_PATH);
  const canonicalProgramId = checkedInProgramId();
  process.env.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID = canonicalProgramId;
  process.env.PROTOCOL_PROGRAM_ID = canonicalProgramId;
  fixturesModule = await importRuntimeModule<FixturesModule>("../frontend/lib/devnet-fixtures.ts");
  protocolModule = await importRuntimeModule<ProtocolModule>("../frontend/lib/protocol.ts");

  const { DEFAULT_HEALTH_PLAN_ADDRESS } = fixturesModule;

  writeFile(MANIFEST_PATH, `${stringify(manifest())}\n`);
  writeFile(ENV_PATH, `${envLines().join("\n")}\n`);

  console.log(`[bootstrap] manifest=${MANIFEST_PATH}`);
  console.log(`[bootstrap] env=${ENV_PATH}`);
  console.log(`[bootstrap] default_health_plan=${DEFAULT_HEALTH_PLAN_ADDRESS}`);
}

await main();
