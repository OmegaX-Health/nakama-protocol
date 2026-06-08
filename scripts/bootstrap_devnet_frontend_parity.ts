// SPDX-License-Identifier: AGPL-3.0-or-later

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

import { loadEnvFile } from "./support/load_env_file.ts";

const FRONTEND_ENV_PATH = resolve(process.cwd(), "frontend/.env.local");
const FRONTEND_FIXTURE_JSON_PATH = resolve(process.cwd(), "frontend/public/devnet-fixtures.json");
const DEVNET_MANIFEST_ENV_PATH = resolve(process.cwd(), "devnet/health-capital-markets.env");
const PROTOCOL_CONTRACT_PATH = resolve(process.cwd(), "shared/protocol_contract.json");

function upsertEnvFile(path: string, updates: Record<string, string>): void {
  const existing = new Map<string, string>();
  if (readable(path)) {
    for (const line of readFileSync(path, "utf8").split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
      const separator = trimmed.indexOf("=");
      existing.set(trimmed.slice(0, separator), trimmed.slice(separator + 1));
    }
  }

  for (const [key, value] of Object.entries(updates)) {
    existing.set(key, value);
  }

  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(
    path,
    `${[...existing.entries()].map(([key, value]) => `${key}=${value}`).join("\n")}\n`,
  );
}

function readable(path: string): boolean {
  try {
    readFileSync(path, "utf8");
    return true;
  } catch {
    return false;
  }
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

function updates(): Record<string, string> {
  const {
    DEVNET_PROTOCOL_FIXTURE_STATE,
    DEFAULT_HEALTH_PLAN_ADDRESS,
  } = fixturesModule;
  const primaryPlan = DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans[0]!;
  return {
    NEXT_PUBLIC_PROTOCOL_PROGRAM_ID: protocolModule.getProgramId().toBase58(),
    NEXT_PUBLIC_DEFAULT_HEALTH_PLAN_ADDRESS: DEFAULT_HEALTH_PLAN_ADDRESS,
    NEXT_PUBLIC_DEVNET_SETTLEMENT_MINT: DEVNET_PROTOCOL_FIXTURE_STATE.settlementMint,
    NEXT_PUBLIC_DEVNET_REWARD_MINT: DEVNET_PROTOCOL_FIXTURE_STATE.rewardMint,
    NEXT_PUBLIC_DEVNET_WRAPPER_SETTLEMENT_MINT: DEVNET_PROTOCOL_FIXTURE_STATE.wrapperSettlementMint,
    NEXT_PUBLIC_PRIMARY_RESERVE_DOMAIN: DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains[0]!.address,
    NEXT_PUBLIC_PRIMARY_HEALTH_PLAN_ID: primaryPlan.planId,
  };
}

let fixturesModule: typeof import("../frontend/lib/devnet-fixtures.ts");
let protocolModule: typeof import("../frontend/lib/protocol.ts");

async function main() {
  loadEnvFile(DEVNET_MANIFEST_ENV_PATH);
  loadEnvFile(FRONTEND_ENV_PATH);
  const canonicalProgramId = checkedInProgramId();
  process.env.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID = canonicalProgramId;
  process.env.PROTOCOL_PROGRAM_ID = canonicalProgramId;
  fixturesModule = await import("../frontend/lib/devnet-fixtures.ts");
  protocolModule = await import("../frontend/lib/protocol.ts");

  upsertEnvFile(FRONTEND_ENV_PATH, updates());
  mkdirSync(dirname(FRONTEND_FIXTURE_JSON_PATH), { recursive: true });
  writeFileSync(FRONTEND_FIXTURE_JSON_PATH, `${stringify(fixturesModule.DEVNET_PROTOCOL_FIXTURE_STATE)}\n`);

  console.log(`[frontend-bootstrap] env=${FRONTEND_ENV_PATH}`);
  console.log(`[frontend-bootstrap] fixtures=${FRONTEND_FIXTURE_JSON_PATH}`);
}

await main();
