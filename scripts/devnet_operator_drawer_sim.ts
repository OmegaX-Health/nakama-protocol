// SPDX-License-Identifier: AGPL-3.0-or-later

// Devnet simulate-only smoke harness for the live operator builders.
//
// Replicates the current trimmed reserve, plan, funding, obligation, and claim
// builder shapes, then signs each tx with the local operator keypair and runs
// connection.simulateTransaction against devnet. Does NOT submit. No state is
// mutated.
//
// Usage:
//   npm run devnet:operator:drawer:sim
//
// Keypair is read from OMEGAX_DEVNET_PROTOCOL_GOVERNANCE_KEYPAIR_PATH
// (falling back to SOLANA_KEYPAIR, then ~/.config/solana/id.json). When
// NEXT_PUBLIC_DEVNET_PROTOCOL_GOVERNANCE_WALLET is configured, the pubkey must
// match it before any RPC work begins.

import { Buffer } from "node:buffer";
import { createHash, randomBytes } from "node:crypto";
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { resolve } from "node:path";

import { keypairFromFile } from "./support/script_helpers.ts";

import {
  Connection,
  Keypair,
  PublicKey,
  Transaction,
  TransactionInstruction,
} from "@solana/web3.js";

import { loadEnvFile } from "./support/load_env_file.ts";

type ProtocolModule = typeof import("../frontend/lib/protocol.ts");
type FixturesModule = typeof import("../frontend/lib/devnet-fixtures.ts");
type ModuleWithDefault<T> = T & { default?: T };

const FRONTEND_ENV_PATH = resolve(process.cwd(), "frontend/.env.local");
const DEVNET_MANIFEST_ENV_PATH = resolve(process.cwd(), "devnet/health-capital-markets.env");
const PROTOCOL_CONTRACT_PATH = resolve(process.cwd(), "shared/protocol_contract.json");
const DEFAULT_KEYPAIR_PATH = resolve(homedir(), ".config/solana/id.json");
const DEFAULT_RPC_URL = "https://api.devnet.solana.com";

function expandHome(path: string): string {
  return path.replace(/^~(?=\/|$)/, homedir());
}

function configuredGovernanceKeypairPath(): string {
  return expandHome(
    process.env.OMEGAX_DEVNET_PROTOCOL_GOVERNANCE_KEYPAIR_PATH?.trim()
      || process.env.SOLANA_KEYPAIR?.trim()
      || DEFAULT_KEYPAIR_PATH,
  );
}

type FlowResult = {
  name: string;
  section: "reserve" | "plan";
  // PASS               — simulate succeeded cleanly
  // EXPECTED_COLLISION — account already bootstrapped (idempotent collision)
  // BUILDER_OK         — instruction decoded + accounts loaded + reached
  //                      the program, but live state / authority rejected it.
  // FAIL               — actual builder or wiring bug (runtime rejected tx
  //                      before it reached the program or hit known UI inputs)
  // SKIP               — required fixture missing
  status: "PASS" | "EXPECTED_COLLISION" | "BUILDER_OK" | "FAIL" | "SKIP";
  note?: string;
};

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

function hashStringTo32HexLocal(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

function hashReason(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  const normalized = trimmed.toLowerCase().replace(/^0x/, "");
  if (/^[0-9a-f]{64}$/.test(normalized)) return normalized;
  return hashStringTo32HexLocal(trimmed);
}

function publicKeyOrFallback(value: string | null | undefined, fallback: PublicKey | string): PublicKey | string {
  const trimmed = String(value ?? "").trim();
  return trimmed || fallback;
}

function classifyError(
  logs: string[],
  isBootstrap: boolean,
): "EXPECTED_COLLISION" | "BUILDER_OK" | "FAIL" {
  const joined = logs.join(" ").toLowerCase();
  if (
    joined.includes("already in use") ||
    joined.includes("already initialized") ||
    // 0x0 on an init-constrained account path with bootstrap flows means the
    // SystemProgram Allocate rejected because the PDA is already materialized.
    (isBootstrap && joined.includes("custom program error: 0x0"))
  ) {
    return "EXPECTED_COLLISION";
  }
  const anchorCode = logs
    .find((l) => l.includes("Error Code: "))
    ?.replace(/.*Error Code: /, "")
    .split(".")[0]
    ?.trim();
  if (anchorCode === "ConstraintSeeds") {
    return "FAIL";
  }
  // If the program emitted an AnchorError, the builder reached the program
  // cleanly (instruction decoded, accounts loaded). That is a builder-level
  // success for state / auth / lifecycle rejections that depend on live data.
  if (logs.some((l) => l.includes("AnchorError"))) return "BUILDER_OK";
  return "FAIL";
}

// The protocol module resolves @solana/web3.js from frontend/node_modules,
// while this script resolves it from root/node_modules. Even when both are
// the same version, the Transaction class prototypes differ and cross-instance
// signing fails in Message.serialize. Rebuild each tx in our local class.
function localizeTx(foreignTx: { instructions: readonly unknown[] }, blockhash: string, feePayer: PublicKey): Transaction {
  const instructions = foreignTx.instructions.map((ix) => {
    const typed = ix as {
      keys: Array<{ pubkey: { toBase58?: () => string; toString?: () => string } | string; isSigner: boolean; isWritable: boolean }>;
      programId: { toBase58?: () => string; toString?: () => string } | string;
      data: Uint8Array | Buffer;
    };
    return new TransactionInstruction({
      keys: typed.keys.map((k) => ({
        pubkey: new PublicKey(
          typeof k.pubkey === "string" ? k.pubkey : (k.pubkey.toBase58?.() ?? k.pubkey.toString!()),
        ),
        isSigner: k.isSigner,
        isWritable: k.isWritable,
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

async function simulate(
  connection: Connection,
  signer: Keypair,
  blockhash: string,
  foreignTx: { instructions: readonly unknown[] },
  name: string,
  section: "reserve" | "plan",
  isBootstrap = false,
): Promise<FlowResult> {
  try {
    const tx = localizeTx(foreignTx, blockhash, signer.publicKey);
    tx.sign(signer);
    const sim = await connection.simulateTransaction(tx, undefined, false);
    if (sim.value.err) {
      const logs = sim.value.logs ?? [];
      const anchorLine = logs.find((l) => l.includes("AnchorError")) ?? "";
      const errCodeLine = logs.find((l) => /Error Code: [A-Z]/.test(l)) ?? "";
      const composed = `${JSON.stringify(sim.value.err)} ${anchorLine} ${errCodeLine}`;
      const verdict = classifyError(logs, isBootstrap);
      return {
        name,
        section,
        status: verdict,
        note:
          verdict === "EXPECTED_COLLISION"
            ? "fixture already bootstrapped (idempotent collision)"
            : verdict === "BUILDER_OK"
              ? `program rejected: ${errCodeLine.replace(/.*Error Code: /, "").trim() || anchorLine}`
              : composed.trim().slice(0, 240),
      };
    }
    return { name, section, status: "PASS" };
  } catch (err) {
    return {
      name,
      section,
      status: "FAIL",
      note: err instanceof Error ? err.message.slice(0, 240) : String(err).slice(0, 240),
    };
  }
}

async function main(): Promise<void> {
  loadEnvFile(DEVNET_MANIFEST_ENV_PATH);
  loadEnvFile(FRONTEND_ENV_PATH);
  const canonicalProgramId = checkedInProgramId();
  process.env.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID = canonicalProgramId;
  process.env.PROTOCOL_PROGRAM_ID = canonicalProgramId;

  const keypairPath = configuredGovernanceKeypairPath();
  const signer = keypairFromFile(keypairPath);
  const signerAddress = signer.publicKey.toBase58();

  const expectedGov = (process.env.NEXT_PUBLIC_DEVNET_PROTOCOL_GOVERNANCE_WALLET || "").trim();
  if (expectedGov && signerAddress !== expectedGov) {
    throw new Error(
      `Signer pubkey ${signerAddress} does not match NEXT_PUBLIC_DEVNET_PROTOCOL_GOVERNANCE_WALLET=${expectedGov}. Aborting.`,
    );
  }

  const rpcUrl = (process.env.NEXT_PUBLIC_SOLANA_RPC_URL || DEFAULT_RPC_URL).trim();
  const connection = new Connection(rpcUrl, "confirmed");
  const { blockhash } = await connection.getLatestBlockhash("confirmed");

  console.log("Devnet operator drawer simulate-only smoke");
  console.log(`RPC: ${rpcUrl}`);
  console.log(`Signer: ${signerAddress}`);
  console.log(`Blockhash: ${blockhash}`);
  console.log("");

  const protocol = await importRuntimeModule<ProtocolModule>("../frontend/lib/protocol.ts");
  const fixturesModule = await importRuntimeModule<FixturesModule>("../frontend/lib/devnet-fixtures.ts");
  const fixtures = fixturesModule.DEVNET_PROTOCOL_FIXTURE_STATE;

  const plan =
    fixtures.healthPlans.find((candidate) =>
      fixtures.claimCases.some((entry) => entry.healthPlan === candidate.address) &&
      fixtures.fundingLines.some(
        (entry) =>
          entry.healthPlan === candidate.address &&
          entry.lineType === protocol.FUNDING_LINE_TYPE_PREMIUM_INCOME,
      ),
    ) ??
    fixtures.healthPlans.find((candidate) =>
      fixtures.fundingLines.some((entry) => entry.healthPlan === candidate.address),
    ) ??
    fixtures.healthPlans[0] ??
    null;
  const reserveDomain =
    (plan ? fixtures.reserveDomains.find((domain) => domain.address === plan.reserveDomain) : null) ??
    fixtures.reserveDomains[0] ??
    null;
  const planSeries = plan
    ? fixtures.policySeries.filter((entry) => entry.healthPlan === plan.address)
    : [];
  const planFundingLines = plan
    ? fixtures.fundingLines.filter((entry) => entry.healthPlan === plan.address)
    : [];
  const planClaims = plan
    ? fixtures.claimCases.filter((entry) => entry.healthPlan === plan.address)
    : [];
  const planObligations = plan
    ? fixtures.obligations.filter((entry) => entry.healthPlan === plan.address)
    : [];
  const series = planSeries[0] ?? null;
  const sponsorLine =
    planFundingLines.find((l) => l.lineType === protocol.FUNDING_LINE_TYPE_SPONSOR_BUDGET) ?? null;
  const premiumLine =
    planFundingLines.find((l) => l.lineType === protocol.FUNDING_LINE_TYPE_PREMIUM_INCOME) ?? null;
  const capitalLine =
    planFundingLines.find((l) => l.lineType === protocol.FUNDING_LINE_TYPE_BACKSTOP) ??
    planFundingLines[0] ??
    null;
  const earningsLine =
    planFundingLines.find(
      (l) => l.lineType === protocol.FUNDING_LINE_TYPE_BACKSTOP || l.lineType === protocol.FUNDING_LINE_TYPE_SUBSIDY,
    ) ??
    capitalLine;
  const operatorSourceTokenAccount =
    process.env.NEXT_PUBLIC_DEVNET_OPERATOR_SOURCE_TOKEN_ACCOUNT ||
    process.env.OMEGAX_DEVNET_OPERATOR_SOURCE_TOKEN_ACCOUNT ||
    "";
  const vaultTokenForLine = (line: { assetMint: string } | null): string => {
    if (!line) return "";
    const fixtureVault = fixtures.domainAssetVaults.find(
      (vault) => vault.reserveDomain === plan?.reserveDomain && vault.assetMint === line.assetMint,
    ) as { vaultTokenAccount?: string } | undefined;
    if (fixtureVault?.vaultTokenAccount) return fixtureVault.vaultTokenAccount;
    const envName = line.assetMint === fixtures.rewardMint
      ? "OMEGAX_DEVNET_OPEN_REWARD_VAULT_TOKEN_ACCOUNT"
      : "OMEGAX_DEVNET_OPEN_SETTLEMENT_VAULT_TOKEN_ACCOUNT";
    return process.env[envName] ?? "";
  };
  const firstLine = planFundingLines[0] ?? null;
  const claim = planClaims[0] ?? null;
  const obligation =
    planObligations.find((entry) => entry.address === claim?.linkedObligation) ??
    planObligations.find((entry) => entry.claimCase === claim?.address) ??
    planObligations[0] ??
    null;

  const results: FlowResult[] = [];

  const skip = (name: string, section: "reserve" | "plan", reason: string): FlowResult => ({
    name,
    section,
    status: "SKIP",
    note: reason,
  });

  // ── RESERVE SETUP ─────────────────────────────────────────────────────────

  results.push(
    await simulate(
      connection,
      signer,
      blockhash,
      protocol.buildCreateReserveDomainTx({
        authority: signer.publicKey,
        recentBlockhash: blockhash,
        // Use a random-suffixed id to avoid colliding with bootstrapped domains
        // (we want a *builder-shape* check, not an idempotency probe).
        domainId: `sim-domain-${randomBytes(4).toString("hex")}`,
        displayName: "Simulated domain",
        domainAdmin: signer.publicKey,
        settlementMode: 0,
        legalStructureHashHex: hashReason("simulated-legal"),
        complianceBaselineHashHex: hashReason("simulated-baseline"),
        allowedRailMask: 65535,
        pauseFlags: 0,
      }),
      "Create reserve domain",
      "reserve",
    ),
  );

  if (!reserveDomain) {
    results.push(skip("Create domain asset vault", "reserve", "no reserve domain fixture"));
  } else {
    // Use the protocol's own settlement mint; simulation will collide if the
    // vault is already bootstrapped for this (domain, mint) pair — that is the
    // expected classification.
    const assetMint =
      process.env.NEXT_PUBLIC_DEVNET_SETTLEMENT_MINT ||
      process.env.NEXT_PUBLIC_DEFAULT_INSURANCE_PAYOUT_MINT ||
      "";
    if (!assetMint) {
      results.push(skip("Create domain asset vault", "reserve", "no settlement mint configured"));
    } else {
      // PT-2026-04-27-01/02 fix: vault token account is now PDA-owned and
      // initialized by the program inline, so the OMEGAX_DEVNET_OPEN_SETTLEMENT_VAULT_TOKEN_ACCOUNT
      // env var is no longer required. The token account address is derivable
      // via deriveDomainAssetVaultTokenAccountPda for downstream inflow calls.
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildCreateDomainAssetVaultTx({
            authority: signer.publicKey,
            reserveDomainAddress: reserveDomain.address,
            assetMint,
            recentBlockhash: blockhash,
          }),
          "Create domain asset vault",
          "reserve",
          true,
        ),
      );
    }
  }

  // ── PLAN OPERATIONS ───────────────────────────────────────────────────────

  if (plan) {
    // Fund sponsor budget
    const sponsorVaultTokenAccount = vaultTokenForLine(sponsorLine);
    if (sponsorLine && operatorSourceTokenAccount && sponsorVaultTokenAccount) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildFundSponsorBudgetTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: sponsorLine.address,
            assetMint: sponsorLine.assetMint,
            sourceTokenAccountAddress: operatorSourceTokenAccount,
            vaultTokenAccountAddress: sponsorVaultTokenAccount,
            recentBlockhash: blockhash,
            amount: 100_000n,
            policySeriesAddress: sponsorLine.policySeries ?? null,
          }),
          "Fund sponsor budget",
          "plan",
        ),
      );
    } else {
      results.push(
        skip(
          "Fund sponsor budget",
          "plan",
          sponsorLine
            ? "operator source token account or vault token account missing"
            : "no SPONSOR_BUDGET funding line",
        ),
      );
    }

    // Record premium payment
    const premiumVaultTokenAccount = vaultTokenForLine(premiumLine);
    if (premiumLine && operatorSourceTokenAccount && premiumVaultTokenAccount) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildRecordPremiumPaymentTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: premiumLine.address,
            assetMint: premiumLine.assetMint,
            sourceTokenAccountAddress: operatorSourceTokenAccount,
            vaultTokenAccountAddress: premiumVaultTokenAccount,
            recentBlockhash: blockhash,
            amount: 100_000n,
            policySeriesAddress: premiumLine.policySeries ?? null,
          }),
          "Record premium payment",
          "plan",
        ),
      );
    } else {
      results.push(
        skip(
          "Record premium payment",
          "plan",
          premiumLine
            ? "operator source token account or vault token account missing"
            : "no PREMIUM_INCOME funding line",
        ),
      );
    }

    // Deposit reserve capital. If the fixture line is not BACKSTOP, the
    // program should reject semantically after the builder reaches it.
    const capitalVaultTokenAccount = vaultTokenForLine(capitalLine);
    if (capitalLine && operatorSourceTokenAccount && capitalVaultTokenAccount) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildDepositReserveCapitalTx({
            contributor: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: capitalLine.address,
            assetMint: capitalLine.assetMint,
            sourceTokenAccountAddress: operatorSourceTokenAccount,
            vaultTokenAccountAddress: capitalVaultTokenAccount,
            recentBlockhash: blockhash,
            amount: 1n,
            termsHashHex: hashReason("sim-capital-terms"),
          }),
          "Deposit reserve capital",
          "plan",
        ),
      );
    } else {
      results.push(
        skip(
          "Deposit reserve capital",
          "plan",
          capitalLine
            ? "operator source token account or vault token account missing"
            : "no funding line fixture",
        ),
      );
    }

    if (capitalLine && operatorSourceTokenAccount && capitalVaultTokenAccount) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildReturnReserveCapitalTx({
            authority: signer.publicKey,
            contributorAddress: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: capitalLine.address,
            assetMint: capitalLine.assetMint,
            vaultTokenAccountAddress: capitalVaultTokenAccount,
            recipientTokenAccountAddress: operatorSourceTokenAccount,
            recentBlockhash: blockhash,
            amount: 1n,
            reasonHashHex: hashReason("sim-capital-return"),
          }),
          "Return reserve capital",
          "plan",
        ),
      );
    } else {
      results.push(
        skip(
          "Return reserve capital",
          "plan",
          capitalLine
            ? "operator token account or vault token account missing"
            : "no funding line fixture",
        ),
      );
    }

    const earningsVaultTokenAccount = vaultTokenForLine(earningsLine);
    if (earningsLine && operatorSourceTokenAccount && earningsVaultTokenAccount) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildRecordReserveEarningsTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: earningsLine.address,
            assetMint: earningsLine.assetMint,
            sourceTokenAccountAddress: operatorSourceTokenAccount,
            vaultTokenAccountAddress: earningsVaultTokenAccount,
            recentBlockhash: blockhash,
            amount: 1n,
            earningsRefHashHex: hashReason("sim-reserve-earnings"),
          }),
          "Record reserve earnings",
          "plan",
        ),
      );
    } else {
      results.push(
        skip(
          "Record reserve earnings",
          "plan",
          earningsLine
            ? "operator source token account or vault token account missing"
            : "no funding line fixture",
        ),
      );
    }

    // Open claim case (use random claim id to probe builder shape)
    if (firstLine) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildOpenClaimCaseTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            fundingLineAddress: firstLine.address,
            recentBlockhash: blockhash,
            claimId: `sim-${randomBytes(4).toString("hex")}`,
            policySeriesAddress: series?.address ?? firstLine.policySeries ?? null,
            claimantAddress: signer.publicKey,
            evidenceRefHashHex: hashReason("sim-evidence-bundle"),
          }),
          "Open claim case",
          "plan",
        ),
      );
    } else {
      results.push(skip("Open claim case", "plan", "no funding line"));
    }

    // Adjudicate claim case
    if (claim) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildAdjudicateClaimCaseTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            claimCaseAddress: claim.address,
            recentBlockhash: blockhash,
            reviewState: protocol.CLAIM_INTAKE_UNDER_REVIEW,
            approvedAmount: 0n,
            deniedAmount: 0n,
            reserveAmount: 0n,
            evidenceRefHashHex: hashReason("sim-evidence-bundle"),
            decisionSupportHashHex: hashReason("sim-decision-support"),
            obligationAddress: obligation?.address ?? null,
          }),
          "Adjudicate claim case",
          "plan",
        ),
      );
    } else {
      results.push(skip("Adjudicate claim case", "plan", "no claim case fixture"));
    }

    // Create obligation
    if (firstLine) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildCreateObligationTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: firstLine.address,
            assetMint: firstLine.assetMint,
            recentBlockhash: blockhash,
            obligationId: `sim-${randomBytes(4).toString("hex")}`,
            policySeriesAddress: series?.address ?? firstLine.policySeries ?? null,
            memberWalletAddress: signer.publicKey,
            beneficiaryAddress: signer.publicKey,
            claimCaseAddress: claim?.address ?? null,
            deliveryMode: protocol.OBLIGATION_DELIVERY_MODE_CLAIMABLE,
            amount: 10_000n,
            creationReasonHashHex: hashReason("sim-reason"),
          }),
          "Create obligation",
          "plan",
        ),
      );
    } else {
      results.push(skip("Create obligation", "plan", "no funding line"));
    }

    // Reserve obligation
    if (obligation && firstLine) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildReserveObligationTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: firstLine.address,
            assetMint: obligation.assetMint,
            obligationAddress: obligation.address,
            recentBlockhash: blockhash,
            amount: 1_000n,
            claimCaseAddress: obligation.claimCase ?? null,
            policySeriesAddress: obligation.policySeries ?? null,
          }),
          "Reserve obligation",
          "plan",
        ),
      );

      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildReleaseReserveTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: firstLine.address,
            assetMint: obligation.assetMint,
            obligationAddress: obligation.address,
            recentBlockhash: blockhash,
            amount: 0n,
            claimCaseAddress: obligation.claimCase ?? null,
            policySeriesAddress: obligation.policySeries ?? null,
          }),
          "Release reserve",
          "plan",
        ),
      );

      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildSettleObligationTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: firstLine.address,
            assetMint: obligation.assetMint,
            obligationAddress: obligation.address,
            recentBlockhash: blockhash,
            nextStatus: protocol.OBLIGATION_STATUS_CLAIMABLE_PAYABLE,
            amount: 0n,
            settlementReasonHashHex: hashReason("sim-settlement"),
            claimCaseAddress: obligation.claimCase ?? null,
            policySeriesAddress: obligation.policySeries ?? null,
          }),
          "Settle obligation",
          "plan",
        ),
      );
    } else {
      results.push(skip("Reserve obligation", "plan", "no obligation or funding line"));
      results.push(skip("Release reserve", "plan", "no obligation or funding line"));
      results.push(skip("Settle obligation", "plan", "no obligation or funding line"));
    }

    // Settle claim
    if (claim && firstLine) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildSettleClaimCaseTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            reserveDomainAddress: plan.reserveDomain,
            fundingLineAddress: firstLine.address,
            assetMint: firstLine.assetMint,
            claimCaseAddress: claim.address,
            recentBlockhash: blockhash,
            amount: 0n,
            policySeriesAddress: claim.policySeries ?? null,
            obligationAddress: obligation?.address ?? null,
          }),
          "Settle claim case",
          "plan",
        ),
      );
    } else {
      results.push(skip("Settle claim case", "plan", "no claim case or funding line"));
    }

    // Update plan controls
    results.push(
      await simulate(
        connection,
        signer,
        blockhash,
        protocol.buildUpdateHealthPlanControlsTx({
          authority: signer.publicKey,
          healthPlanAddress: plan.address,
          recentBlockhash: blockhash,
          sponsorOperator: publicKeyOrFallback(plan.sponsorOperator, signer.publicKey),
          claimsOperator: publicKeyOrFallback(plan.claimsOperator, signer.publicKey),
          oracleAuthority: publicKeyOrFallback(plan.oracleAuthority, protocol.ZERO_PUBKEY),
          allowedRailMask: 65535,
          defaultFundingPriority: fixtures.fundingLines[0]?.fundingPriority ?? 0,
          pauseFlags: 0,
          active: true,
        }),
        "Update plan controls",
        "plan",
      ),
    );

    // Update reserve domain controls
    if (reserveDomain) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildUpdateReserveDomainControlsTx({
            authority: signer.publicKey,
            reserveDomainAddress: reserveDomain.address,
            recentBlockhash: blockhash,
            allowedRailMask: 65535,
            pauseFlags: 0,
            active: true,
          }),
          "Update reserve domain controls",
          "plan",
        ),
      );
    } else {
      results.push(skip("Update reserve domain controls", "plan", "no reserve domain"));
    }

    // Create policy series (random seriesId avoids bootstrapped collision,
    // exercises arg-shape correctness against the program constraints).
    {
      const seriesAssetMint =
        process.env.NEXT_PUBLIC_DEVNET_SETTLEMENT_MINT ||
        process.env.NEXT_PUBLIC_DEFAULT_INSURANCE_PAYOUT_MINT ||
        "";
      if (!seriesAssetMint) {
        results.push(skip("Create policy series", "plan", "no settlement mint configured"));
      } else {
        results.push(
          await simulate(
            connection,
            signer,
            blockhash,
            protocol.buildCreatePolicySeriesTx({
              authority: signer.publicKey,
              healthPlanAddress: plan.address,
              assetMint: seriesAssetMint,
              recentBlockhash: blockhash,
              seriesId: `sim-${randomBytes(4).toString("hex")}`,
              displayName: "Simulated series",
              metadataUri: "ipfs://sim",
              mode: protocol.SERIES_MODE_OTHER,
              status: protocol.SERIES_STATUS_DRAFT,
              adjudicationMode: 0,
              cycleSeconds: 0n,
              termsVersion: 1,
            }),
            "Create policy series",
            "plan",
          ),
        );
      }
    }

    // Version policy series — must use an existing series
    if (series) {
      results.push(
        await simulate(
          connection,
          signer,
          blockhash,
          protocol.buildVersionPolicySeriesTx({
            authority: signer.publicKey,
            healthPlanAddress: plan.address,
            currentPolicySeriesAddress: series.address,
            assetMint: series.assetMint,
            recentBlockhash: blockhash,
            seriesId: `sim-v-${randomBytes(4).toString("hex")}`,
            displayName: "Simulated next series",
            metadataUri: "ipfs://sim-v",
            status: series.status,
            adjudicationMode: 0,
            cycleSeconds: 0n,
          }),
          "Version policy series",
          "plan",
        ),
      );
    } else {
      results.push(skip("Version policy series", "plan", "no policy series fixture"));
    }

    // Open funding line (random id)
    {
      const lineAssetMint =
        process.env.NEXT_PUBLIC_DEVNET_SETTLEMENT_MINT ||
        process.env.NEXT_PUBLIC_DEFAULT_INSURANCE_PAYOUT_MINT ||
        "";
      if (!lineAssetMint) {
        results.push(skip("Open funding line", "plan", "no settlement mint configured"));
      } else {
        results.push(
          await simulate(
            connection,
            signer,
            blockhash,
            protocol.buildOpenFundingLineTx({
              authority: signer.publicKey,
              healthPlanAddress: plan.address,
              reserveDomainAddress: plan.reserveDomain,
              assetMint: lineAssetMint,
              recentBlockhash: blockhash,
              lineId: `sim-${randomBytes(4).toString("hex")}`,
              policySeriesAddress: series?.address ?? null,
              lineType: protocol.FUNDING_LINE_TYPE_SPONSOR_BUDGET,
              fundingPriority: 0,
              committedAmount: 0n,
            }),
            "Open funding line",
            "plan",
          ),
        );
      }
    }
  } else {
    const allPlanFlows = [
      "Fund sponsor budget",
      "Record premium payment",
      "Deposit reserve capital",
      "Return reserve capital",
      "Record reserve earnings",
      "Open claim case",
      "Adjudicate claim case",
      "Create obligation",
      "Reserve obligation",
      "Release reserve",
      "Settle obligation",
      "Settle claim case",
      "Update plan controls",
      "Update reserve domain controls",
      "Create policy series",
      "Version policy series",
      "Open funding line",
    ];
    for (const name of allPlanFlows) {
      results.push(skip(name, "plan", "no health plan fixture"));
    }
  }

  // ── REPORT ────────────────────────────────────────────────────────────────

  const pad = (s: string, n: number) => String(s ?? "") + " ".repeat(Math.max(0, n - String(s ?? "").length));
  const cleanNote = (s?: string) =>
    (s ?? "").replace(/\s+/g, " ").slice(0, 180);
  console.log(pad("Flow", 34) + pad("Section", 12) + pad("Status", 22) + "Note");
  console.log("-".repeat(140));
  for (const r of results) {
    console.log(
      pad(r.name, 34) + pad(r.section, 12) + pad(r.status, 22) + cleanNote(r.note),
    );
  }
  console.log("");

  const counts = results.reduce<Record<string, number>>((acc, r) => {
    acc[r.status] = (acc[r.status] ?? 0) + 1;
    return acc;
  }, {});
  const builderOk =
    (counts.PASS ?? 0) + (counts.EXPECTED_COLLISION ?? 0) + (counts.BUILDER_OK ?? 0);
  const attempted = builderOk + (counts.FAIL ?? 0);
  console.log(
    `Summary: PASS=${counts.PASS ?? 0}  EXPECTED_COLLISION=${counts.EXPECTED_COLLISION ?? 0}  BUILDER_OK=${counts.BUILDER_OK ?? 0}  SKIP=${counts.SKIP ?? 0}  FAIL=${counts.FAIL ?? 0}`,
  );
  console.log(
    `Builder health: ${builderOk}/${attempted} attempted flows reached the program cleanly.`,
  );
  console.log(
    "  PASS               — sim succeeded; tx would submit cleanly",
  );
  console.log(
    "  EXPECTED_COLLISION — fixture already bootstrapped (idempotent)",
  );
  console.log(
    "  BUILDER_OK         — program accepted & rejected semantically (state/auth/lifecycle)",
  );
  console.log(
    "  FAIL               — real builder or wiring bug",
  );

  if ((counts.FAIL ?? 0) > 0) {
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.stack || err.message : err);
  process.exit(1);
});
