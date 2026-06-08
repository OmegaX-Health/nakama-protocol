// SPDX-License-Identifier: AGPL-3.0-or-later

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { loadEnvFile } from "./support/load_env_file.ts";

function fail(message: string): never {
  throw new Error(message);
}

const FRONTEND_ENV_PATH = resolve(process.cwd(), "frontend/.env.local");
const DEVNET_MANIFEST_ENV_PATH = resolve(process.cwd(), "devnet/health-capital-markets.env");
const PROTOCOL_CONTRACT_PATH = resolve(process.cwd(), "shared/protocol_contract.json");

function checkedInProgramId(): string {
  const contract = JSON.parse(readFileSync(PROTOCOL_CONTRACT_PATH, "utf8")) as { programId?: string };
  if (!contract.programId) {
    throw new Error("shared/protocol_contract.json is missing programId.");
  }
  return contract.programId;
}

async function main() {
  loadEnvFile(DEVNET_MANIFEST_ENV_PATH);
  loadEnvFile(FRONTEND_ENV_PATH);
  const canonicalProgramId = checkedInProgramId();
  process.env.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID = canonicalProgramId;
  process.env.PROTOCOL_PROGRAM_ID = canonicalProgramId;
  const fixturesModule = await import("../frontend/lib/devnet-fixtures.ts");
  const {
    DEVNET_PROTOCOL_FIXTURE_STATE,
    configuredDevnetPaymentRails,
    configuredDevnetWallets,
  } = fixturesModule;
  const strict = process.env.DEVNET_FIXTURE_STRICT === "1";

  console.log(strict ? "Frontend devnet parity signoff" : "Frontend devnet smoke");
  console.log(`Reserve domains: ${DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains.length}`);
  console.log(`Health plans: ${DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans.length}`);
  console.log(`Policy series: ${DEVNET_PROTOCOL_FIXTURE_STATE.policySeries.length}`);
  console.log(`Funding lines: ${DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines.length}`);
  console.log(`Claim cases: ${DEVNET_PROTOCOL_FIXTURE_STATE.claimCases.length}`);
  console.log(`Capital contributions: ${DEVNET_PROTOCOL_FIXTURE_STATE.capitalContributions.length}`);
  console.log(`Configured wallets: ${configuredDevnetWallets().length}`);
  console.log(`Configured payment rails: ${configuredDevnetPaymentRails().length}`);

  console.log("\nRole matrix:");
  for (const row of DEVNET_PROTOCOL_FIXTURE_STATE.roleMatrix) {
    console.log(`- ${row.role}: ${row.actions.join(", ")}`);
  }

  if (strict) {
    const missing = [];
    if (configuredDevnetWallets().length < 6) {
      missing.push("at least 6 non-zero devnet wallet roles");
    }
    if (configuredDevnetPaymentRails().length < 2) {
      missing.push("at least 2 configured devnet payment rails");
    }
    if (DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans.length < 2) {
      missing.push("two canonical health plan fixtures");
    }
    if (DEVNET_PROTOCOL_FIXTURE_STATE.policySeries.length < 2) {
      missing.push("two canonical policy series fixtures");
    }
    if (DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines.length < 2) {
      missing.push("two canonical funding line fixtures");
    }
    if (DEVNET_PROTOCOL_FIXTURE_STATE.claimCases.length < 1) {
      missing.push("one canonical claim case fixture");
    }
    if (missing.length > 0) {
      fail(`Strict frontend signoff failed:\n- ${missing.join("\n- ")}`);
    }
  }
}

await main();
