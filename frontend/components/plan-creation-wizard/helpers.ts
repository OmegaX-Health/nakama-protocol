// SPDX-License-Identifier: AGPL-3.0-or-later

import { PublicKey } from "@solana/web3.js";

import type { MultiOracleOption } from "@/components/multi-oracle-picker";
import { GENESIS_PROTECT_ACUTE_TEMPLATE_KEY } from "@/lib/genesis-protect-acute-operator";
import {
  requiresProtectionLane,
  requiresRewardLane,
  type CoveragePathway,
  type LaunchIntent,
  type PayoutAssetMode,
} from "@/lib/plan-launch";
import { parseUiAmountToBaseUnits } from "@/lib/spl";

export type StepId =
  | "basics"
  | "membership"
  | "verification"
  | "reward-lane"
  | "protection-lane"
  | "review";

export type StepDescriptor = {
  id: StepId;
  number: string;
  label: string;
};

export type StepCopy = {
  headline: string;
  emphasis: string;
  body: string;
  tip: string;
};

export type ActionLog = {
  id: string;
  action: string;
  message: string;
  explorerUrl?: string;
  signature?: string;
};

export type CreatedArtifacts = {
  healthPlanAddress: string;
  rewardSeriesAddress: string | null;
  protectionSeriesAddress: string | null;
  rewardFundingLineAddress: string | null;
  protectionFundingLineAddress: string | null;
  poolAddress?: string | null;
  capitalClassAddresses?: string[];
  allocationAddresses?: string[];
  extraSeriesAddresses?: string[];
  extraFundingLineAddresses?: string[];
};

export type RulePreview = {
  derivedRuleHashHex: string;
  derivedPayoutHashHex: string;
};

export type WizardDetailState =
  | { key: "launch-preview" }
  | { key: "rule-commitments"; outcomeId: string }
  | { key: "protection-posture" };

export const ZERO_HASH = "0".repeat(64);
export const SOL_DECIMALS = 9;

const DEFAULT_PROTECTION_METADATA_URIS = {
  defi_native: "/metadata/protection/default-defi-v1.json",
  rwa_policy: "/metadata/protection/default-rwa-v1.json",
} as const;

export function defaultProtectionMetadataUri(pathway: Exclude<CoveragePathway, "">): string {
  return DEFAULT_PROTECTION_METADATA_URIS[pathway];
}

export function isGenesisProtectAcuteTemplate(value: string | null): boolean {
  return (value ?? "").trim() === GENESIS_PROTECT_ACUTE_TEMPLATE_KEY;
}

export const STEP_COPY: Record<StepId, StepCopy> = {
  basics: {
    headline: "Set up your",
    emphasis: "plan.",
    body: "Start with the basics. You’ll pick rewards and coverage in the next steps.",
    tip: "Pick a name, identifier, and public link you’re comfortable keeping long term.",
  },
  membership: {
    headline: "Choose who can",
    emphasis: "join.",
    body: "Enrollment rules apply before members participate in any reward or coverage lane.",
    tip: "Keep it simple at launch. You can tighten enrollment rules later.",
  },
  verification: {
    headline: "Choose who verifies",
    emphasis: "outcomes.",
    body: "The verifiers you pick define who may attest outcomes; quorum is recorded for the future finality layer.",
    tip: "Pick enough verifiers to avoid single-operator risk, but keep the launch quorum simple.",
  },
  "reward-lane": {
    headline: "Set up your",
    emphasis: "rewards.",
    body: "Pick the outcomes that should trigger a reward, name each rule, and connect the budget that will fund payouts.",
    tip: "Start narrow. One crisp reward is better than many muddy ones.",
  },
  "protection-lane": {
    headline: "Set up your",
    emphasis: "coverage.",
    body: "Define the protection terms, premium schedule, and public policy details members can inspect.",
    tip: "Link to terms and disclosures real people can read.",
  },
  review: {
    headline: "Review and",
    emphasis: "create.",
    body: "Final check before the plan, series, and funding lines are created on-chain.",
    tip: "If creation partially succeeds, rerunning is safe — existing accounts are skipped.",
  },
};

export function normalize(value: string): string {
  return value.trim();
}

export function shortAddress(value: string): string {
  if (!value || value.length < 12) return value || "n/a";
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
}

export function randomId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function firstError(errors: string[]): string | null {
  return errors[0] ?? null;
}

export function toPositiveInt(value: string): number {
  const parsed = Number.parseInt(normalize(value), 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

export function protocolToken(value: string): string {
  const normalized = normalize(value)
    .replace(/[^a-z0-9]+/gi, "_")
    .replace(/^_+|_+$/g, "")
    .toUpperCase();
  return normalized || "PENDING";
}

export function humanizeChoice(value: string): string {
  const normalized = normalize(value).replace(/[_-]+/g, " ").trim();
  if (!normalized) return "Pending";
  if (normalized === "defi native") return "DeFi native";
  if (normalized === "rwa policy") return "RWA policy";
  if (normalized === "spl") return "SPL";
  if (normalized === "sol") return "SOL";
  if (normalized === "nft anchor") return "NFT anchor";
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
}

export function seedDefault(value: string, fallback: string): string {
  const normalized = normalize(value)
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return (normalized || fallback).slice(0, 32);
}

export function seriesDisplayDefault(planDisplayName: string, suffix: string): string {
  const normalized = normalize(planDisplayName);
  return normalized ? `${normalized} ${suffix}` : `OmegaX ${suffix}`;
}

export function toAssetPublicKey(value: string): PublicKey | null {
  try {
    return new PublicKey(normalize(value));
  } catch {
    return null;
  }
}

export function toUiAmountBaseUnits(value: string, mode: PayoutAssetMode, splDecimals: number | null): bigint {
  if (mode === "sol") {
    return parseUiAmountToBaseUnits(value, SOL_DECIMALS);
  }
  if (splDecimals === null) {
    throw new Error("Token decimals are not loaded yet.");
  }
  return parseUiAmountToBaseUnits(value, splDecimals);
}

export function baseUnitsPreview(value: string, mode: PayoutAssetMode, splDecimals: number | null): string {
  try {
    return `${toUiAmountBaseUnits(value, mode, splDecimals).toLocaleString()} base units`;
  } catch {
    return "n/a";
  }
}

export function buildWorkflowSteps(intent: LaunchIntent, genesisTemplateMode = false): StepDescriptor[] {
  const steps: StepDescriptor[] = [
    { id: "basics", number: "01", label: "Basics" },
    { id: "membership", number: "02", label: "Membership" },
    { id: "verification", number: "03", label: "Verification" },
  ];
  if (genesisTemplateMode) {
    steps.push({ id: "review", number: String(steps.length + 1).padStart(2, "0"), label: "Review" });
    return steps;
  }
  if (requiresRewardLane(intent)) {
    steps.push({ id: "reward-lane", number: String(steps.length + 1).padStart(2, "0"), label: "Reward Lane" });
  }
  if (requiresProtectionLane(intent)) {
    steps.push({ id: "protection-lane", number: String(steps.length + 1).padStart(2, "0"), label: "Protection Lane" });
  }
  steps.push({ id: "review", number: String(steps.length + 1).padStart(2, "0"), label: "Review" });
  return steps;
}

export function buildLaunchOracleOptions(
  liveProfiles: Array<{ oracle: string; active: boolean; metadataUri: string }>,
  selectedOracles: string[],
): MultiOracleOption[] {
  const options = new Map<string, MultiOracleOption>();

  for (const profile of liveProfiles) {
    options.set(profile.oracle, {
      oracle: profile.oracle,
      active: profile.active,
      metadataUri: profile.metadataUri,
    });
  }

  for (const oracle of selectedOracles) {
    if (!options.has(oracle)) {
      options.set(oracle, {
        oracle,
        active: true,
        metadataUri: "Manual oracle entry",
      });
    }
  }

  return [...options.values()];
}

export function wizardDetailKey(detail: WizardDetailState): string {
  return detail.key === "rule-commitments" ? `rule-commitments:${detail.outcomeId}` : detail.key;
}
