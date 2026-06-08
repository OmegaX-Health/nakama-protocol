// SPDX-License-Identifier: AGPL-3.0-or-later

// Shared-devnet bootstrap for the trimmed base protocol.
//
// The base program no longer owns DAO governance, membership seats, oracle
// registries, liquidity pools, LP positions, allocation ledgers, or claim
// attestation accounts. This live bootstrap intentionally materializes only the
// current on-chain primitives: reserve domains, domain asset vaults, health
// plans, policy series, supported funding lines, and a proof-fingerprinted
// claim case used as a smoke anchor.

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  Connection,
  Keypair,
  PublicKey,
  SystemProgram,
  Transaction,
  TransactionInstruction,
} from "@solana/web3.js";
import { TOKEN_PROGRAM_ID } from "@solana/spl-token";

import { loadEnvFile } from "./support/load_env_file.ts";
import { wrapConnectionWithRpcRetry } from "./support/rpc_retry.ts";
import { keypairFromFile } from "./support/script_helpers.ts";

type ProtocolModule = typeof import("../frontend/lib/protocol.ts");
type FixturesModule = typeof import("../frontend/lib/devnet-fixtures.ts");

type ModuleWithDefault<T> = T & { default?: T };

type ProtocolInstructionAccountInput = {
  pubkey?: PublicKey | string | null;
  isSigner?: boolean;
  isWritable?: boolean;
};

type BootstrapCounters = {
  created: number;
  skippedExisting: number;
  skippedUnsupported: number;
};

const FRONTEND_ENV_PATH = resolve(process.cwd(), "frontend/.env.local");
const DEVNET_MANIFEST_ENV_PATH = resolve(process.cwd(), "devnet/health-capital-markets.env");
const PROTOCOL_CONTRACT_PATH = resolve(process.cwd(), "shared/protocol_contract.json");
const DEFAULT_OPERATOR_KEYPAIR_PATH = resolve(homedir(), ".config/solana/id.json");
const DEFAULT_RPC_URL = "https://api.devnet.solana.com";
const ZERO_PUBKEY = "11111111111111111111111111111111";
const PROOF_CLAIM_ID = "devnet-proof-fingerprint";

function expandHome(path: string): string {
  return path.replace(/^~(?=\/|$)/, homedir());
}

function configuredOperatorKeypairPath(): string {
  return expandHome(
    process.env.OMEGAX_DEVNET_PROTOCOL_GOVERNANCE_KEYPAIR_PATH?.trim()
      || process.env.OMEGAX_DEVNET_OPERATOR_KEYPAIR_PATH?.trim()
      || process.env.SOLANA_KEYPAIR?.trim()
      || DEFAULT_OPERATOR_KEYPAIR_PATH,
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
    process.env[key] = value;
  }

  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(
    path,
    `${[...existing.entries()].map(([key, value]) => `${key}=${value}`).join("\n")}\n`,
  );
}

function run(cmd: string, args: string[]): void {
  const result = spawnSync(cmd, args, {
    cwd: resolve(process.cwd()),
    encoding: "utf8",
    env: process.env,
  });
  const output = `${result.stdout ?? ""}${result.stderr ?? ""}`;
  if (result.status !== 0) {
    throw new Error(`${cmd} ${args.join(" ")} failed:\n${output}`);
  }
  process.stdout.write(output);
}

function checkedInProgramId(): string {
  const contract = JSON.parse(readFileSync(PROTOCOL_CONTRACT_PATH, "utf8")) as { programId?: string };
  if (!contract.programId) {
    throw new Error("shared/protocol_contract.json is missing programId.");
  }
  return new PublicKey(contract.programId).toBase58();
}

async function importFresh<T>(path: string): Promise<T> {
  const url = `${pathToFileURL(resolve(process.cwd(), path)).href}?v=${Date.now()}`;
  const module = await import(url) as ModuleWithDefault<T>;
  return (module.default ?? module) as T;
}

function sha256Hex(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function hashBytes(value: string): number[] {
  return [...Buffer.from(sha256Hex(value), "hex")];
}

function fixedHashHex(value: unknown, fallbackLabel: string): string {
  const normalized = String(value ?? "").trim().toLowerCase().replace(/^0x/, "");
  if (/^[0-9a-f]{64}$/.test(normalized)) return normalized;
  return sha256Hex(normalized || fallbackLabel);
}

function hashBytesFromValue(value: unknown, fallbackLabel: string): number[] {
  return [...Buffer.from(fixedHashHex(value, fallbackLabel), "hex")];
}

function toBigIntAmount(value: unknown): bigint {
  if (typeof value === "bigint") return value;
  if (typeof value === "number") return BigInt(Math.trunc(value));
  if (typeof value === "string" && value.trim()) return BigInt(value.trim());
  return 0n;
}

function toPublicKey(value: PublicKey | string): PublicKey {
  return value instanceof PublicKey ? value : new PublicKey(value);
}

function isZeroAddress(value: unknown): boolean {
  return !String(value ?? "").trim() || String(value).trim() === ZERO_PUBKEY;
}

function localizeTx(foreignTx: { instructions: readonly unknown[] }, blockhash: string, feePayer: PublicKey): Transaction {
  const instructions = foreignTx.instructions.map((ix) => {
    const typed = ix as {
      keys: Array<{
        pubkey: { toBase58?: () => string; toString?: () => string } | string;
        isSigner: boolean;
        isWritable: boolean;
      }>;
      programId: { toBase58?: () => string; toString?: () => string } | string;
      data: Uint8Array | Buffer;
    };
    return new TransactionInstruction({
      keys: typed.keys.map((key) => ({
        pubkey: new PublicKey(
          typeof key.pubkey === "string"
            ? key.pubkey
            : (key.pubkey.toBase58?.() ?? key.pubkey.toString!()),
        ),
        isSigner: key.isSigner,
        isWritable: key.isWritable,
      })),
      programId: new PublicKey(
        typeof typed.programId === "string"
          ? typed.programId
          : (typed.programId.toBase58?.() ?? typed.programId.toString!()),
      ),
      data: Buffer.from(typed.data),
    });
  });
  return new Transaction({ feePayer, recentBlockhash: blockhash }).add(...instructions);
}

async function accountExists(connection: Connection, address: PublicKey | string): Promise<boolean> {
  return await connection.getAccountInfo(toPublicKey(address), "confirmed") !== null;
}

async function sendProtocolInstruction(params: {
  accounts: ProtocolInstructionAccountInput[];
  args: Record<string, unknown>;
  connection: Connection;
  instructionName: string;
  label: string;
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<string> {
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const { blockhash, lastValidBlockHeight } = await params.connection.getLatestBlockhash("confirmed");
      const foreignTx = params.protocol.buildProtocolTransactionFromInstruction({
        feePayer: params.signer.publicKey,
        recentBlockhash: blockhash,
        instructionName: params.instructionName,
        args: params.args,
        accounts: params.accounts,
      });
      const tx = localizeTx(foreignTx, blockhash, params.signer.publicKey);
      tx.sign(params.signer);
      const signature = await params.connection.sendRawTransaction(tx.serialize(), {
        maxRetries: 5,
        skipPreflight: false,
      });
      const confirmation = await params.connection.confirmTransaction(
        { blockhash, lastValidBlockHeight, signature },
        "confirmed",
      );
      if (confirmation.value.err) {
        throw new Error(`${params.label} failed during confirmation.`);
      }
      console.log(`[live-bootstrap] ${params.label}: ${signature}`);
      return signature;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (attempt === 4 || !/429|Too Many|blockhash|timeout|fetch failed/i.test(message)) {
        throw error;
      }
      await new Promise((resolve) => setTimeout(resolve, 1200 * attempt));
    }
  }
  throw new Error(`${params.label} failed before send.`);
}

async function createReserveDomains(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<void> {
  for (const domain of params.fixtureState.reserveDomains) {
    if (await accountExists(params.connection, domain.address)) {
      params.counters.skippedExisting += 1;
      continue;
    }
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `create_reserve_domain:${domain.domainId}`,
      instructionName: "create_reserve_domain",
      args: {
        domain_id: domain.domainId,
        display_name: domain.displayName,
        domain_admin: params.signer.publicKey,
        settlement_mode: domain.settlementMode ?? 0,
        legal_structure_hash: hashBytes(`reserve-domain:${domain.domainId}:legal`),
        compliance_baseline_hash: hashBytes(`reserve-domain:${domain.domainId}:compliance`),
        allowed_rail_mask: 0xffff,
        pause_flags: domain.pauseFlags ?? 0,
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: domain.address, isWritable: true },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  }
}

async function createDomainAssetVaults(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<void> {
  const scopes = new Map<string, { reserveDomain: string; assetMint: string }>();
  for (const vault of params.fixtureState.domainAssetVaults) {
    scopes.set(`${vault.reserveDomain}:${vault.assetMint}`, {
      reserveDomain: vault.reserveDomain,
      assetMint: vault.assetMint,
    });
  }
  for (const line of params.fixtureState.fundingLines) {
    scopes.set(`${line.reserveDomain}:${line.assetMint}`, {
      reserveDomain: line.reserveDomain,
      assetMint: line.assetMint,
    });
  }

  for (const scope of scopes.values()) {
    if (isZeroAddress(scope.assetMint)) {
      params.counters.skippedUnsupported += 1;
      console.log(`[live-bootstrap] skip vault:${scope.reserveDomain}: unset asset mint`);
      continue;
    }
    const vault = params.protocol.deriveDomainAssetVaultPda({
      reserveDomain: scope.reserveDomain,
      assetMint: scope.assetMint,
    });
    const ledger = params.protocol.deriveDomainAssetLedgerPda({
      reserveDomain: scope.reserveDomain,
      assetMint: scope.assetMint,
    });
    if (await accountExists(params.connection, vault) && await accountExists(params.connection, ledger)) {
      params.counters.skippedExisting += 1;
      continue;
    }
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `create_domain_asset_vault:${scope.reserveDomain}:${scope.assetMint}`,
      instructionName: "create_domain_asset_vault",
      args: {
        asset_mint: new PublicKey(scope.assetMint),
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: scope.reserveDomain, isWritable: true },
        { pubkey: vault, isWritable: true },
        { pubkey: ledger, isWritable: true },
        { pubkey: scope.assetMint },
        {
          pubkey: params.protocol.deriveDomainAssetVaultTokenAccountPda({
            reserveDomain: scope.reserveDomain,
            assetMint: scope.assetMint,
          }),
          isWritable: true,
        },
        { pubkey: TOKEN_PROGRAM_ID },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  }
}

async function createHealthPlans(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<void> {
  for (const plan of params.fixtureState.healthPlans) {
    if (await accountExists(params.connection, plan.address)) {
      params.counters.skippedExisting += 1;
      continue;
    }
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `create_health_plan:${plan.planId}`,
      instructionName: "create_health_plan",
      args: {
        plan_id: plan.planId,
        display_name: plan.displayName,
        organization_ref: plan.sponsorLabel || plan.planId,
        metadata_uri: `https://protocol.omegax.health/plans/${plan.planId}`,
        sponsor: params.signer.publicKey,
        sponsor_operator: params.signer.publicKey,
        claims_operator: params.signer.publicKey,
        oracle_authority: params.signer.publicKey,
        allowed_rail_mask: 0xffff,
        default_funding_priority: 1,
        oracle_policy_hash: hashBytes(`health-plan:${plan.planId}:oracle`),
        schema_binding_hash: hashBytes(`health-plan:${plan.planId}:schema`),
        compliance_baseline_hash: hashBytes(`health-plan:${plan.planId}:compliance`),
        pause_flags: plan.pauseFlags ?? 0,
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: plan.reserveDomain },
        { pubkey: plan.address, isWritable: true },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  }
}

async function createPolicySeries(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<void> {
  for (const series of params.fixtureState.policySeries) {
    if (isZeroAddress(series.assetMint)) {
      params.counters.skippedUnsupported += 1;
      console.log(`[live-bootstrap] skip policy_series:${series.seriesId}: unset asset mint`);
      continue;
    }
    if (await accountExists(params.connection, series.address)) {
      params.counters.skippedExisting += 1;
      continue;
    }
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `create_policy_series:${series.seriesId}`,
      instructionName: "create_policy_series",
      args: {
        series_id: series.seriesId,
        display_name: series.displayName,
        metadata_uri: series.metadataUri ?? `https://protocol.omegax.health/series/${series.seriesId}`,
        asset_mint: new PublicKey(series.assetMint),
        mode: series.mode,
        status: series.status,
        adjudication_mode: 0,
        terms_hash: hashBytes(`policy-series:${series.seriesId}:terms`),
        pricing_hash: hashBytes(`policy-series:${series.seriesId}:pricing`),
        payout_hash: hashBytes(`policy-series:${series.seriesId}:payout`),
        reserve_model_hash: hashBytes(`policy-series:${series.seriesId}:reserve`),
        comparability_hash: hashBytesFromValue(series.comparabilityHashHex ?? series.comparabilityKey, `policy-series:${series.seriesId}:comparability`),
        policy_overrides_hash: hashBytes(`policy-series:${series.seriesId}:overrides`),
        cycle_seconds: BigInt(series.cycleSeconds ?? 0),
        terms_version: Number.parseInt(String(series.termsVersion ?? "1"), 10) || 1,
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: series.healthPlan },
        { pubkey: series.address, isWritable: true },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  }
}

function supportedFundingLineTypes(protocol: ProtocolModule): Set<number> {
  return new Set([
    protocol.FUNDING_LINE_TYPE_SPONSOR_BUDGET,
    protocol.FUNDING_LINE_TYPE_PREMIUM_INCOME,
    protocol.FUNDING_LINE_TYPE_BACKSTOP,
    protocol.FUNDING_LINE_TYPE_SUBSIDY,
  ]);
}

async function createFundingLines(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<void> {
  const supportedTypes = supportedFundingLineTypes(params.protocol);
  for (const line of params.fixtureState.fundingLines) {
    if (!supportedTypes.has(line.lineType)) {
      params.counters.skippedUnsupported += 1;
      console.log(`[live-bootstrap] skip funding_line:${line.lineId}: removed line type ${line.lineType}`);
      continue;
    }
    if (isZeroAddress(line.assetMint)) {
      params.counters.skippedUnsupported += 1;
      console.log(`[live-bootstrap] skip funding_line:${line.lineId}: unset asset mint`);
      continue;
    }
    if (await accountExists(params.connection, line.address)) {
      params.counters.skippedExisting += 1;
      continue;
    }
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `open_funding_line:${line.lineId}`,
      instructionName: "open_funding_line",
      args: {
        line_id: line.lineId,
        policy_series: isZeroAddress(line.policySeries) ? new PublicKey(ZERO_PUBKEY) : new PublicKey(line.policySeries!),
        asset_mint: new PublicKey(line.assetMint),
        line_type: line.lineType,
        funding_priority: line.fundingPriority,
        committed_amount: toBigIntAmount(line.fundedAmount),
        caps_hash: hashBytes(`funding-line:${line.lineId}:caps`),
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: line.healthPlan },
        {
          pubkey: params.protocol.deriveDomainAssetVaultPda({
            reserveDomain: line.reserveDomain,
            assetMint: line.assetMint,
          }),
        },
        {
          pubkey: params.protocol.deriveDomainAssetLedgerPda({
            reserveDomain: line.reserveDomain,
            assetMint: line.assetMint,
          }),
          isWritable: true,
        },
        { pubkey: line.address, isWritable: true },
        {
          pubkey: params.protocol.deriveFundingLineLedgerPda({
            fundingLine: line.address,
            assetMint: line.assetMint,
          }),
          isWritable: true,
        },
        {
          pubkey: params.protocol.derivePlanReserveLedgerPda({
            healthPlan: line.healthPlan,
            assetMint: line.assetMint,
          }),
          isWritable: true,
        },
        { pubkey: isZeroAddress(line.policySeries) ? null : line.policySeries },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  }
}

async function seedProofClaim(params: {
  connection: Connection;
  counters: BootstrapCounters;
  fixtureState: FixturesModule["DEVNET_PROTOCOL_FIXTURE_STATE"];
  protocol: ProtocolModule;
  signer: Keypair;
}): Promise<string | null> {
  const supportedTypes = supportedFundingLineTypes(params.protocol);
  const line = params.fixtureState.fundingLines.find((candidate) =>
    supportedTypes.has(candidate.lineType)
      && !isZeroAddress(candidate.assetMint)
      && !isZeroAddress(candidate.policySeries)
      && candidate.lineType === params.protocol.FUNDING_LINE_TYPE_PREMIUM_INCOME,
  ) ?? params.fixtureState.fundingLines.find((candidate) =>
    supportedTypes.has(candidate.lineType)
      && !isZeroAddress(candidate.assetMint)
      && !isZeroAddress(candidate.policySeries),
  );
  if (!line) {
    params.counters.skippedUnsupported += 1;
    console.log("[live-bootstrap] skip proof claim: no supported funding line with policy series");
    return null;
  }

  const claimCase = params.protocol.deriveClaimCasePda({
    healthPlan: line.healthPlan,
    claimId: PROOF_CLAIM_ID,
  });
  const claimCaseAddress = claimCase.toBase58();
  const evidenceHashHex = sha256Hex(`devnet-live:${params.protocol.getProgramId().toBase58()}:${PROOF_CLAIM_ID}:evidence`);
  const decisionHashHex = sha256Hex(`devnet-live:${params.protocol.getProgramId().toBase58()}:${PROOF_CLAIM_ID}:decision`);

  if (!await accountExists(params.connection, claimCase)) {
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `open_claim_case:${PROOF_CLAIM_ID}`,
      instructionName: "open_claim_case",
      args: {
        claim_id: PROOF_CLAIM_ID,
        policy_series: new PublicKey(line.policySeries!),
        claimant: params.signer.publicKey,
        evidence_ref_hash: [...Buffer.from(evidenceHashHex, "hex")],
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true, isWritable: true },
        { pubkey: line.healthPlan },
        { pubkey: line.address },
        { pubkey: claimCase, isWritable: true },
        { pubkey: SystemProgram.programId },
      ],
    });
    params.counters.created += 1;
  } else {
    params.counters.skippedExisting += 1;
  }

  const snapshot = await params.protocol.loadProtocolConsoleSnapshot(params.connection);
  const liveClaim = snapshot.claimCases.find((claim) => claim.address === claimCaseAddress);
  const hasDecisionHash = Boolean(liveClaim?.decisionSupportHashHex && !/^0+$/.test(liveClaim.decisionSupportHashHex));
  if (!hasDecisionHash) {
    await sendProtocolInstruction({
      protocol: params.protocol,
      connection: params.connection,
      signer: params.signer,
      label: `adjudicate_claim_case:${PROOF_CLAIM_ID}`,
      instructionName: "adjudicate_claim_case",
      args: {
        review_state: params.protocol.CLAIM_INTAKE_DENIED,
        approved_amount: 0n,
        denied_amount: 1n,
        reserve_amount: 0n,
        evidence_ref_hash: [...Buffer.from(evidenceHashHex, "hex")],
        decision_support_hash: [...Buffer.from(decisionHashHex, "hex")],
      },
      accounts: [
        { pubkey: params.signer.publicKey, isSigner: true },
        { pubkey: line.healthPlan },
        { pubkey: claimCase, isWritable: true },
        { pubkey: null, isWritable: true },
      ],
    });
    params.counters.created += 1;
  }
  return claimCaseAddress;
}

async function main(): Promise<void> {
  loadEnvFile(DEVNET_MANIFEST_ENV_PATH);
  loadEnvFile(FRONTEND_ENV_PATH);

  const canonicalProgramId = checkedInProgramId();
  process.env.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID = canonicalProgramId;
  process.env.PROTOCOL_PROGRAM_ID = canonicalProgramId;

  const signer = keypairFromFile(configuredOperatorKeypairPath());
  const operatorAddress = signer.publicKey.toBase58();

  upsertEnvFile(FRONTEND_ENV_PATH, {
    NEXT_PUBLIC_PROTOCOL_PROGRAM_ID: canonicalProgramId,
    PROTOCOL_PROGRAM_ID: canonicalProgramId,
    NEXT_PUBLIC_DEVNET_PROTOCOL_GOVERNANCE_WALLET: operatorAddress,
    NEXT_PUBLIC_DEVNET_DOMAIN_ADMIN_WALLET: operatorAddress,
    NEXT_PUBLIC_DEVNET_PLAN_ADMIN_WALLET: operatorAddress,
    NEXT_PUBLIC_DEVNET_SPONSOR_OPERATOR_WALLET: operatorAddress,
    NEXT_PUBLIC_DEVNET_CLAIMS_OPERATOR_WALLET: operatorAddress,
    NEXT_PUBLIC_DEVNET_ORACLE_OPERATOR_WALLET: operatorAddress,
  });
  loadEnvFile(FRONTEND_ENV_PATH);

  const protocol = await importFresh<ProtocolModule>("frontend/lib/protocol.ts");
  const fixtures = await importFresh<FixturesModule>("frontend/lib/devnet-fixtures.ts");
  const fixtureState = fixtures.DEVNET_PROTOCOL_FIXTURE_STATE;
  const rpcUrl =
    process.env.SOLANA_RPC_URL
    || process.env.NEXT_PUBLIC_SOLANA_RPC_URL
    || process.env.NEXT_PUBLIC_SOLANA_DEVNET_RPC_URL
    || DEFAULT_RPC_URL;
  const connection = wrapConnectionWithRpcRetry(new Connection(rpcUrl, "confirmed"), {
    labelPrefix: "live-bootstrap",
    logPrefix: "live-bootstrap",
  });
  const counters: BootstrapCounters = {
    created: 0,
    skippedExisting: 0,
    skippedUnsupported: 0,
  };

  console.log(`[live-bootstrap] rpc=${rpcUrl.includes("?") ? `${rpcUrl.slice(0, rpcUrl.indexOf("?"))}?...` : rpcUrl}`);
  console.log(`[live-bootstrap] program=${protocol.getProgramId().toBase58()}`);
  console.log(`[live-bootstrap] operator=${operatorAddress}`);

  await createReserveDomains({ connection, counters, fixtureState, protocol, signer });
  await createDomainAssetVaults({ connection, counters, fixtureState, protocol, signer });
  await createHealthPlans({ connection, counters, fixtureState, protocol, signer });
  await createPolicySeries({ connection, counters, fixtureState, protocol, signer });
  await createFundingLines({ connection, counters, fixtureState, protocol, signer });
  const proofClaim = await seedProofClaim({ connection, counters, fixtureState, protocol, signer });

  run("npm", ["run", "protocol:bootstrap"]);
  run("npm", ["run", "devnet:frontend:bootstrap"]);

  const finalSnapshot = await protocol.loadProtocolConsoleSnapshot(connection);
  console.log(
    JSON.stringify(
      {
        programId: protocol.getProgramId().toBase58(),
        operator: operatorAddress,
        proofClaim,
        created: counters.created,
        skippedExisting: counters.skippedExisting,
        skippedUnsupported: counters.skippedUnsupported,
        reserveDomains: finalSnapshot.reserveDomains.length,
        domainAssetVaults: finalSnapshot.domainAssetVaults.length,
        healthPlans: finalSnapshot.healthPlans.length,
        policySeries: finalSnapshot.policySeries.length,
        fundingLines: finalSnapshot.fundingLines.length,
        claimCases: finalSnapshot.claimCases.length,
        capitalContributions: finalSnapshot.capitalContributions.length,
        obligations: finalSnapshot.obligations.length,
      },
      null,
      2,
    ),
  );
}

await main();
