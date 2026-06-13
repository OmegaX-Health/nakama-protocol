// SPDX-License-Identifier: AGPL-3.0-or-later

import {
  GENESIS_PROTECT_ACUTE_JUNIOR_CLASS_DISPLAY_NAME,
  GENESIS_PROTECT_ACUTE_JUNIOR_CLASS_ID,
  GENESIS_PROTECT_ACUTE_POOL_DISPLAY_NAME,
  GENESIS_PROTECT_ACUTE_POOL_ID,
  GENESIS_PROTECT_ACUTE_POOL_STRATEGY_THESIS,
  GENESIS_PROTECT_ACUTE_SENIOR_CLASS_DISPLAY_NAME,
  GENESIS_PROTECT_ACUTE_SENIOR_CLASS_ID,
} from "@/lib/genesis-protect-acute";

export type NetworkSchoolAcuteAssistSkuKey = "core" | "longTermer" | "familyGuarded";

export type NetworkSchoolAcuteAssistSublimit = {
  label: string;
  amountUsd: number;
};

export type NetworkSchoolAcuteAssistEvidenceSchemaBinding = {
  schemaKey: string;
  schemaVersion: number;
  schemaAuthority: "shared_public_contract";
};

export type NetworkSchoolAcuteAssistFundingLane = {
  lineId: string;
  reserveRole: string;
};

export type NetworkSchoolAcuteAssistIssuanceControls = {
  reserveAttribution: string;
  publicStatusRule: string;
  issueWhen: string[];
  pauseWhen: string[];
};

export type NetworkSchoolAcuteAssistLaunchTruth = {
  publicStatus: "network_school_verification_pending";
  primaryLaunchSku: NetworkSchoolAcuteAssistSkuKey;
  claimsTrustPhase: "operator_backed_oracle_phase0";
  broadlyLiveInsurance: false;
  networkSchoolOfficialBenefit: false;
  superteamEligible: false;
  discordVerificationRequired: true;
  rawHealthEvidenceOnchain: false;
};

export type NetworkSchoolAcuteAssistSkuDefinition = {
  key: NetworkSchoolAcuteAssistSkuKey;
  seriesId: string;
  displayName: string;
  metadataUri: string;
  comparabilityKey: string;
  coverWindowDays: number;
  defaultSelection: boolean;
  cohort0Launch: boolean;
  familyPlan: boolean;
  pricing: {
    retailUsd: number;
    termRolBps: number;
    expectedLossUsd: number;
    baseLossRatioPct: number;
    stressLossRatioPct: number;
  };
  supportLimitUsd: number;
  fastLaneUsd: number;
  manualReviewAboveUsd: number;
  reimbursement: {
    excessUsd: number;
    reimbursementPctAfterExcess: number;
    formula: string;
  };
  sublimits: NetworkSchoolAcuteAssistSublimit[];
  householdRules?: {
    baseHouseholdUsd?: number;
    adultUsd?: number;
    childUsd?: number;
    referenceAdults?: number;
    referenceChildren?: number;
    maxAdults?: number;
    maxChildren?: number;
    adultPerPersonMaxUsd?: number;
    childPerPersonMaxUsd?: number;
    includedAdults?: number;
    includedChildren?: number;
    perPersonMaxUsd?: number;
    perEventMaxUsd: number;
    outpatientFamilySublimitUsd: number;
    maxPaidClaimsPerWindow: number;
  };
  termRules?: {
    quoteBasis: "per_started_30_day_period" | "household_size_and_term";
    formula: string;
    minCoveredDays: number;
    maxCoveredDays: number;
    upfrontPaymentRequired: boolean;
    aggregateCapDoesNotReset: boolean;
    exampleQuotes: string[];
  };
  waitingPeriods: {
    illnessHours: number;
    accidentHours: number;
    knownSymptomsExcluded: boolean;
  };
  evidenceSchema: NetworkSchoolAcuteAssistEvidenceSchemaBinding;
  fundingLineIds: {
    premium: string;
    liquidity: string;
  };
  fundingLanes: {
    premium: NetworkSchoolAcuteAssistFundingLane;
    liquidity: NetworkSchoolAcuteAssistFundingLane;
  };
  issuanceControls: NetworkSchoolAcuteAssistIssuanceControls;
  launchTruth: NetworkSchoolAcuteAssistLaunchTruth;
};

export const NETWORK_SCHOOL_ACUTE_ASSIST_PLAN_ID = "network-school-acute-assist-v1";
export const NETWORK_SCHOOL_ACUTE_ASSIST_PLAN_DISPLAY_NAME = "Network School Acute Assist";
export const NETWORK_SCHOOL_ACUTE_ASSIST_PLAN_METADATA_URI = "/metadata/plans/network-school-acute-assist-v1.json";
export const NETWORK_SCHOOL_ACUTE_ASSIST_SPONSOR_LABEL = "Network School Verified Members";
export const NETWORK_SCHOOL_ACUTE_ASSIST_TERMS_VERSION = "ns-acute-assist-v1";
export const NETWORK_SCHOOL_ACUTE_ASSIST_PUBLIC_DISCLOSURE_BASE_URL = "https://protocol.omegax.health";
export const NETWORK_SCHOOL_ACUTE_ASSIST_TECHNICAL_TERMS_PATH =
  "/coverage/network-school-acute-assist/technical-terms";
export const NETWORK_SCHOOL_ACUTE_ASSIST_RISK_DISCLOSURE_PATH =
  "/coverage/network-school-acute-assist/risk-disclosures";
export const NETWORK_SCHOOL_ACUTE_ASSIST_TECHNICAL_TERMS_URL =
  `${NETWORK_SCHOOL_ACUTE_ASSIST_PUBLIC_DISCLOSURE_BASE_URL}${NETWORK_SCHOOL_ACUTE_ASSIST_TECHNICAL_TERMS_PATH}`;
export const NETWORK_SCHOOL_ACUTE_ASSIST_RISK_DISCLOSURE_URL =
  `${NETWORK_SCHOOL_ACUTE_ASSIST_PUBLIC_DISCLOSURE_BASE_URL}${NETWORK_SCHOOL_ACUTE_ASSIST_RISK_DISCLOSURE_PATH}`;
export const NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA_KEY = "network-school-acute-assist-claim";
export const NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA_VERSION = 1;
export const NETWORK_SCHOOL_ACUTE_ASSIST_POOL_ID = GENESIS_PROTECT_ACUTE_POOL_ID;
export const NETWORK_SCHOOL_ACUTE_ASSIST_POOL_DISPLAY_NAME = GENESIS_PROTECT_ACUTE_POOL_DISPLAY_NAME;
export const NETWORK_SCHOOL_ACUTE_ASSIST_POOL_STRATEGY_THESIS = GENESIS_PROTECT_ACUTE_POOL_STRATEGY_THESIS;
export const NETWORK_SCHOOL_ACUTE_ASSIST_SENIOR_CLASS_ID = GENESIS_PROTECT_ACUTE_SENIOR_CLASS_ID;
export const NETWORK_SCHOOL_ACUTE_ASSIST_SENIOR_CLASS_DISPLAY_NAME =
  GENESIS_PROTECT_ACUTE_SENIOR_CLASS_DISPLAY_NAME;
export const NETWORK_SCHOOL_ACUTE_ASSIST_JUNIOR_CLASS_ID = GENESIS_PROTECT_ACUTE_JUNIOR_CLASS_ID;
export const NETWORK_SCHOOL_ACUTE_ASSIST_JUNIOR_CLASS_DISPLAY_NAME =
  GENESIS_PROTECT_ACUTE_JUNIOR_CLASS_DISPLAY_NAME;
export const NETWORK_SCHOOL_ACUTE_ASSIST_VISIBLE_RESERVE_USD = 5_000;
export const NETWORK_SCHOOL_ACUTE_ASSIST_COHORT0_POLICY_CAP = 25;
export const NETWORK_SCHOOL_ACUTE_ASSIST_COHORT0_HARD_PAYOUT_CAP_USD = 3_000;

export const NETWORK_SCHOOL_ACUTE_ASSIST_METADATA_URIS = {
  core: "/metadata/protection/ns-acute-assist-core-30-v1.json",
  longTermer: "/metadata/protection/ns-acute-assist-long-termer-v1.json",
  familyGuarded: "/metadata/protection/ns-acute-assist-family-guarded-v1.json",
} as const satisfies Record<NetworkSchoolAcuteAssistSkuKey, string>;

export const NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA: NetworkSchoolAcuteAssistEvidenceSchemaBinding = {
  schemaKey: NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA_KEY,
  schemaVersion: NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA_VERSION,
  schemaAuthority: "shared_public_contract",
};

export const NETWORK_SCHOOL_ACUTE_ASSIST_LAUNCH_TRUTH: NetworkSchoolAcuteAssistLaunchTruth = {
  publicStatus: "network_school_verification_pending",
  primaryLaunchSku: "core",
  claimsTrustPhase: "operator_backed_oracle_phase0",
  broadlyLiveInsurance: false,
  networkSchoolOfficialBenefit: false,
  superteamEligible: false,
  discordVerificationRequired: true,
  rawHealthEvidenceOnchain: false,
};

const NETWORK_SCHOOL_ACUTE_ASSIST_REIMBURSEMENT = {
  excessUsd: 50,
  reimbursementPctAfterExcess: 80,
  formula: "min(plan_limit, sublimit, remaining_member_limit, remaining_pool_cap, max(0, (eligible_bill - 50) * 0.80))",
} as const;

const NETWORK_SCHOOL_ACUTE_ASSIST_WAITING_PERIODS = {
  illnessHours: 24,
  accidentHours: 0,
  knownSymptomsExcluded: true,
} as const;

function fundingLanesFor(linePrefix: string, displayName: string) {
  const premium = `${linePrefix}-premiums`;
  const liquidity = `${linePrefix}-liquidity`;
  return {
    fundingLineIds: {
      premium,
      liquidity,
    },
    fundingLanes: {
      premium: {
        lineId: premium,
        reserveRole: `Collected 30-day member premiums attributed to ${displayName}.`,
      },
      liquidity: {
        lineId: liquidity,
        reserveRole: `Posted acute-pool capital allocated to approved ${displayName} obligations.`,
      },
    },
  } as const;
}

function cohort0IssuanceControls(displayName: string, fastLaneUsd: number): NetworkSchoolAcuteAssistIssuanceControls {
  return {
    reserveAttribution:
      "Only posted acute-pool capital and collected premiums count as claims-paying reserve; token treasury marks do not count without a disclosed haircut.",
    publicStatusRule:
      "Keep this as a Network School-only limited pilot. Do not present it as official Network School coverage, Superteam coverage, broad public insurance, or guaranteed payout insurance.",
    issueWhen: [
      "Network School membership verification has succeeded through the off-chain Discord/member verifier.",
      "The member activates the 30-day window before symptoms, injury, or the acute event.",
      "Usable claim-paying reserve supports the active Cohort 0 product ladder and aggregate payout cap.",
      "Claims operators can review evidence manually above the fast-lane threshold.",
    ],
    pauseWhen: [
      "Discord or Network School membership verification is unavailable, unconfigured, or stale.",
      "Paid claims exceed 50% of the Cohort 0 hard aggregate payout cap or hit the hard aggregate cap.",
      `Any ${displayName} claim exceeds the fast-lane threshold of ${fastLaneUsd} USD without manual review.`,
      `Claims-paying reserve falls below ${NETWORK_SCHOOL_ACUTE_ASSIST_VISIBLE_RESERVE_USD} USD before collecting the next premium batch.`,
      "Provider evidence, pricing, reserve controls, or public terms drift from the published metadata.",
    ],
  };
}

const coreLanes = fundingLanesFor("ns-acute-core30", "NS Acute Assist Core 30");
const longTermerLanes = fundingLanesFor("ns-acute-long-termer", "NS Acute Assist Long-Termer Guarded");
const familyGuardedLanes = fundingLanesFor("ns-family-guarded", "NS Acute Assist Family Guarded");

export const NETWORK_SCHOOL_ACUTE_ASSIST_SKUS: Record<
  NetworkSchoolAcuteAssistSkuKey,
  NetworkSchoolAcuteAssistSkuDefinition
> = {
  core: {
    key: "core",
    seriesId: "ns-acute-core-30-v1",
    displayName: "NS Acute Assist - Core 30",
    metadataUri: NETWORK_SCHOOL_ACUTE_ASSIST_METADATA_URIS.core,
    comparabilityKey: "ns-acute-assist-core-30",
    coverWindowDays: 30,
    defaultSelection: true,
    cohort0Launch: true,
    familyPlan: false,
    pricing: {
      retailUsd: 19,
      termRolBps: 190,
      expectedLossUsd: 7.5,
      baseLossRatioPct: 39,
      stressLossRatioPct: 118,
    },
    supportLimitUsd: 1_000,
    fastLaneUsd: 250,
    manualReviewAboveUsd: 250,
    reimbursement: NETWORK_SCHOOL_ACUTE_ASSIST_REIMBURSEMENT,
    sublimits: [
      { label: "Clinic, urgent care, diagnostics, prescribed medication, and initial stabilization", amountUsd: 1_000 },
    ],
    waitingPeriods: NETWORK_SCHOOL_ACUTE_ASSIST_WAITING_PERIODS,
    evidenceSchema: NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA,
    fundingLineIds: coreLanes.fundingLineIds,
    fundingLanes: coreLanes.fundingLanes,
    issuanceControls: cohort0IssuanceControls("Core 30", 250),
    launchTruth: NETWORK_SCHOOL_ACUTE_ASSIST_LAUNCH_TRUTH,
  },
  longTermer: {
    key: "longTermer",
    seriesId: "ns-acute-long-termer-v1",
    displayName: "NS Acute Assist - Long-Termer Guarded",
    metadataUri: NETWORK_SCHOOL_ACUTE_ASSIST_METADATA_URIS.longTermer,
    comparabilityKey: "ns-acute-assist-long-termer",
    coverWindowDays: 365,
    defaultSelection: false,
    cohort0Launch: true,
    familyPlan: false,
    pricing: {
      retailUsd: 19,
      termRolBps: 190,
      expectedLossUsd: 7.5,
      baseLossRatioPct: 39,
      stressLossRatioPct: 118,
    },
    supportLimitUsd: 1_000,
    fastLaneUsd: 200,
    manualReviewAboveUsd: 200,
    reimbursement: NETWORK_SCHOOL_ACUTE_ASSIST_REIMBURSEMENT,
    sublimits: [
      { label: "Remaining-contract aggregate", amountUsd: 1_000 },
      { label: "Per-event maximum", amountUsd: 600 },
      { label: "Outpatient and clinic sublimit", amountUsd: 400 },
    ],
    termRules: {
      quoteBasis: "per_started_30_day_period",
      formula:
        "quote_usd = ceil(remaining_contract_days / 30) * 19; one 1000 USD aggregate cap applies until the Network School contract end date and does not reset monthly.",
      minCoveredDays: 31,
      maxCoveredDays: 365,
      upfrontPaymentRequired: true,
      aggregateCapDoesNotReset: true,
      exampleQuotes: [
        "7 months remaining -> 133 USD upfront, 1000 USD aggregate cap",
        "10 months remaining -> 190 USD upfront, 1000 USD aggregate cap",
        "12 months remaining -> 228 USD upfront, 1000 USD aggregate cap",
      ],
    },
    waitingPeriods: NETWORK_SCHOOL_ACUTE_ASSIST_WAITING_PERIODS,
    evidenceSchema: NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA,
    fundingLineIds: longTermerLanes.fundingLineIds,
    fundingLanes: longTermerLanes.fundingLanes,
    issuanceControls: cohort0IssuanceControls("Long-Termer Guarded", 200),
    launchTruth: NETWORK_SCHOOL_ACUTE_ASSIST_LAUNCH_TRUTH,
  },
  familyGuarded: {
    key: "familyGuarded",
    seriesId: "ns-acute-family-guarded-v1",
    displayName: "NS Acute Assist - Family Guarded",
    metadataUri: NETWORK_SCHOOL_ACUTE_ASSIST_METADATA_URIS.familyGuarded,
    comparabilityKey: "ns-acute-assist-family-guarded",
    coverWindowDays: 30,
    defaultSelection: false,
    cohort0Launch: true,
    familyPlan: true,
    pricing: {
      retailUsd: 89,
      termRolBps: 593,
      expectedLossUsd: 24,
      baseLossRatioPct: 27,
      stressLossRatioPct: 81,
    },
    supportLimitUsd: 1_500,
    fastLaneUsd: 250,
    manualReviewAboveUsd: 250,
    reimbursement: NETWORK_SCHOOL_ACUTE_ASSIST_REIMBURSEMENT,
    sublimits: [
      { label: "Shared family aggregate", amountUsd: 1_500 },
      { label: "Adult per-person maximum", amountUsd: 600 },
      { label: "Child per-person maximum", amountUsd: 350 },
      { label: "Per-event maximum", amountUsd: 750 },
      { label: "Outpatient and clinic family sublimit", amountUsd: 500 },
    ],
    householdRules: {
      baseHouseholdUsd: 39,
      adultUsd: 15,
      childUsd: 10,
      referenceAdults: 2,
      referenceChildren: 2,
      maxAdults: 2,
      maxChildren: 3,
      adultPerPersonMaxUsd: 600,
      childPerPersonMaxUsd: 350,
      perEventMaxUsd: 750,
      outpatientFamilySublimitUsd: 500,
      maxPaidClaimsPerWindow: 2,
    },
    termRules: {
      quoteBasis: "household_size_and_term",
      formula:
        "quote_usd_per_30_days = 39 + (15 * covered_adults) + (10 * covered_children); renewals require reserve review and the 1500 USD household aggregate does not reset until the next approved renewal.",
      minCoveredDays: 1,
      maxCoveredDays: 30,
      upfrontPaymentRequired: true,
      aggregateCapDoesNotReset: true,
      exampleQuotes: [
        "2 adults + 2 children -> 89 USD for 30 days, 1500 USD shared aggregate cap",
        "2 adults + 3 children -> 99 USD for 30 days, 1500 USD shared aggregate cap",
      ],
    },
    waitingPeriods: NETWORK_SCHOOL_ACUTE_ASSIST_WAITING_PERIODS,
    evidenceSchema: NETWORK_SCHOOL_ACUTE_ASSIST_EVIDENCE_SCHEMA,
    fundingLineIds: familyGuardedLanes.fundingLineIds,
    fundingLanes: familyGuardedLanes.fundingLanes,
    issuanceControls: cohort0IssuanceControls("Family Guarded", 250),
    launchTruth: NETWORK_SCHOOL_ACUTE_ASSIST_LAUNCH_TRUTH,
  },
};

export const NETWORK_SCHOOL_ACUTE_ASSIST_DEFAULT_SKU = NETWORK_SCHOOL_ACUTE_ASSIST_SKUS.core;

export const NETWORK_SCHOOL_ACUTE_ASSIST_SKU_LIST = [
  NETWORK_SCHOOL_ACUTE_ASSIST_SKUS.core,
  NETWORK_SCHOOL_ACUTE_ASSIST_SKUS.longTermer,
  NETWORK_SCHOOL_ACUTE_ASSIST_SKUS.familyGuarded,
] as const;

export const NETWORK_SCHOOL_ACUTE_ASSIST_COMMON_EXCLUSIONS = [
  "chronic and pre-existing conditions",
  "known symptoms before activation",
  "routine checkups, preventive care, and elective or planned treatment",
  "dental, vision, maternity, fertility, mental health, cosmetic care, and long-term rehabilitation",
  "ongoing medication refills",
  "intoxication-related events, illegal activity, and fraud",
  "high-risk or professional sports unless a later explicit add-on is published",
  "treatment in USA or Canada at launch",
  "evacuation, repatriation, trip cancellation, baggage, delay, and liability",
] as const;

export const NETWORK_SCHOOL_ACUTE_ASSIST_COVERED_EVENTS = [
  "urgent clinic visit",
  "urgent doctor consult",
  "emergency room consult",
  "hospital stabilization within cap",
  "food poisoning or gastroenteritis requiring care",
  "dengue fever evaluation and treatment within cap",
  "fever or infection requiring clinic, labs, or prescribed medication",
  "minor injury, wound care, sprain, or fracture evaluation",
  "doctor-prescribed medication tied to an eligible acute event",
  "basic diagnostics tied directly to an eligible acute event",
] as const;
