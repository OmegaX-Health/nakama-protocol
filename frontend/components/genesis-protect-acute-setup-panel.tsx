// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import Link from "next/link";

import { formatAmount, formatSettlementUnits, rawAmountTitle } from "@/lib/canonical-ui";
import type { GenesisProtectAcuteSkuKey } from "@/lib/genesis-protect-acute";
import {
  GENESIS_PROTECT_ACUTE_FAST_DEMO_SKU,
  GENESIS_PROTECT_ACUTE_PRIMARY_SKU,
  GENESIS_PROTECT_ACUTE_TEMPLATE_KEY,
  type GenesisProtectAcuteSetupModel,
} from "@/lib/genesis-protect-acute-operator";

type GenesisProtectAcuteSetupPanelProps = {
  model: GenesisProtectAcuteSetupModel;
  planAddress: string | null;
  treasuryHref: string;
  capitalClassesHref: string;
  capitalAllocationsHref: string;
  bootstrapHref: string;
  oracleBindingsHref: string;
  claimsHref: string;
  adminActionsEnabled?: boolean;
  founderCommitmentHref?: string;
  skuConsoleHrefs: Record<GenesisProtectAcuteSkuKey, {
    claims: string;
    treasury: string;
  }>;
};

function posturePillClass(state: GenesisProtectAcuteSetupModel["posture"]["state"]): string {
  switch (state) {
    case "healthy":
      return "status-ok";
    case "paused":
      return "status-error";
    default:
      return "status-off";
  }
}

function readinessPillClass(phase: GenesisProtectAcuteSetupModel["readinessPhase"]): string {
  switch (phase) {
    case "issuance_ready":
      return "status-ok";
    case "paused":
      return "status-error";
    default:
      return "status-off";
  }
}

function utilizationLabel(bps: bigint | null): string {
  if (bps === null) return "N/A";
  return `${Number(bps) / 100}%`;
}

function commitmentModeLabel(mode: number): string {
  switch (mode) {
    case 0:
      return "Direct premium";
    case 1:
      return "Treasury credit";
    case 2:
      return "Waterfall reserve";
    default:
      return `Mode ${mode}`;
  }
}

function shortHash(value: string | null | undefined): string {
  const normalized = value?.trim() ?? "";
  if (!normalized) return "None";
  if (normalized.length <= 16) return normalized;
  return `${normalized.slice(0, 8)}…${normalized.slice(-8)}`;
}

function checklistRows(props: GenesisProtectAcuteSetupPanelProps) {
  return [
    {
      key: "planShellReady",
      title: "Plan shell exists",
      detail: "Genesis Protect Acute is present with the canonical plan id and sponsor label.",
      ready: props.model.checklist.planShellReady,
      href: props.bootstrapHref,
      action: "Rerun template bootstrap",
    },
    {
      key: "event7SeriesReady",
      title: "Event 7 coverage product exists",
      detail: "The fast demo SKU stays wired to the canonical PolicySeries metadata URI and protection mode.",
      ready: props.model.checklist.event7SeriesReady,
      href: props.bootstrapHref,
      action: "Restore launch SKU",
    },
    {
      key: "travel30SeriesReady",
      title: "Travel 30 coverage product exists",
      detail: "The primary launch SKU stays wired to the canonical PolicySeries metadata URI and protection mode.",
      ready: props.model.checklist.travel30SeriesReady,
      href: props.bootstrapHref,
      action: "Restore launch SKU",
    },
    {
      key: "fundingLinesReady",
      title: "Canonical reserve lanes exist",
      detail: "Event 7 keeps premium, sponsor, and liquidity FundingLine lanes while Travel 30 keeps premium and liquidity.",
      ready: props.model.checklist.fundingLinesReady,
      href: props.bootstrapHref,
      action: "Restore reserve lanes",
    },
    {
      key: "poolReady",
      title: "Pool shell exists",
      detail: "The Genesis reserve pool is present with the canonical display name and strategy thesis.",
      ready: props.model.checklist.poolReady,
      href: props.bootstrapHref,
      action: "Restore pool shell",
    },
    {
      key: "capitalClassesReady",
      title: "Senior and junior classes exist",
      detail: "Both capital sleeves are present so Travel 30 and Event 7 can keep distinct reserve attribution.",
      ready: props.model.checklist.capitalClassesReady,
      href: props.capitalClassesHref,
      action: "Open capital classes",
    },
    {
      key: "allocationsReady",
      title: "Launch allocation positions exist",
      detail: "The canonical junior Event 7 lane plus senior/junior Travel 30 lanes are registered.",
      ready: props.model.checklist.allocationsReady,
      href: props.capitalAllocationsHref,
      action: "Open allocations",
    },
    {
      key: "planAuthoritiesReady",
      title: "Sponsor, claims, and oracle authorities are configured",
      detail: "The plan root must already expose real operator wallets before the launch window opens.",
      ready: props.model.checklist.planAuthoritiesReady,
      href: props.treasuryHref,
      action: "Open treasury controls",
    },
    {
      key: "reserveTargetReviewReady",
      title: "Reserve target review is live",
      detail: "Pool terms are present and at least one claims-paying reserve lane is funded for operator review.",
      ready: props.model.checklist.reserveTargetReviewReady,
      href: props.treasuryHref,
      action: "Open reserve settings",
    },
    {
      key: "poolTermsReady",
      title: "Pool terms are configured",
      detail: "Terms and payout metadata must be present before reserve-target review can be considered complete.",
      ready: props.model.checklist.poolTermsReady,
      href: props.treasuryHref,
      action: "Open pool settings",
    },
    {
      key: "poolOraclePolicyReady",
      title: "Pool oracle policy is configured",
      detail: "The pool-facing oracle policy must be bound before the Genesis posture can move out of setup mode.",
      ready: props.model.checklist.poolOraclePolicyReady,
      href: props.oracleBindingsHref,
      action: "Open oracle bindings",
    },
  ] as const;
}

export function GenesisProtectAcuteSetupPanel(props: GenesisProtectAcuteSetupPanelProps) {
  const primarySku = props.model.perSkuPosture.find((entry) => entry.skuKey === GENESIS_PROTECT_ACUTE_PRIMARY_SKU.key) ?? null;
  const demoSku = props.model.perSkuPosture.find((entry) => entry.skuKey === GENESIS_PROTECT_ACUTE_FAST_DEMO_SKU.key) ?? null;
  const rows = checklistRows(props);

  return (
    <section className="plans-stack">
      <article className="plans-card heavy-glass">
        <div className="plans-card-head">
          <div>
            <p className="plans-card-eyebrow">Genesis market setup</p>
            <h2 className="plans-card-title plans-card-title-display">
              Launch-readiness <em>checklist</em>
            </h2>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className={`status-pill ${readinessPillClass(props.model.readinessPhase)}`}>
              {props.model.readinessPhaseCopy.label}
            </span>
            <span className={`status-pill ${posturePillClass(props.model.posture.state)}`}>
              {props.model.posture.state.toUpperCase()}
            </span>
            <span className="status-pill status-off">
              {props.model.checklistCompleted}/{props.model.checklistTotal} items ready
            </span>
            <span className="status-pill status-ok">
              {GENESIS_PROTECT_ACUTE_PRIMARY_SKU.displayName}
            </span>
            <span className="status-pill status-off">
              {GENESIS_PROTECT_ACUTE_FAST_DEMO_SKU.displayName}
            </span>
          </div>
        </div>

        <div className="plans-notice liquid-glass" role="status">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">flag</span>
          <p>
            <strong>{props.model.readinessPhaseCopy.title}.</strong>{" "}
            {props.model.readinessPhaseCopy.detail}
          </p>
        </div>

        <p className="plans-card-body">
          The Genesis template creates the canonical two-SKU shell in place.
          Current public posture: bounded end-of-month mainnet target, not broadly live insurance today, with Phase 0 operator-backed claim review while reserve, oracle, and pool controls finish operator sign-off.
        </p>

        <div className="plans-settings-grid">
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Claims</span>
              <span className="plans-settings-lane">ClaimCase records currently linked to the Genesis plan</span>
            </div>
            <span className="plans-settings-address">{formatAmount(props.model.claimCount)}</span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Reserved amount</span>
              <span className="plans-settings-lane">Current reserve already encumbered across Genesis FundingLine lanes</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.reservedAmount)}>
              {formatSettlementUnits(props.model.reservedAmount)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Payout/liability pending</span>
              <span className="plans-settings-lane">Claimable or payable Obligation exposure visible on the live reserve lanes</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.pendingPayoutAmount)}>
              {formatSettlementUnits(props.model.pendingPayoutAmount)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Reserve utilization</span>
              <span className="plans-settings-lane">Reserved plus pending payout as a share of currently posted claims-paying capital</span>
            </div>
            <span className="plans-settings-address">{utilizationLabel(props.model.reserveUtilizationBps)}</span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Claims-paying capital</span>
              <span className="plans-settings-lane">Premium, sponsor, and LP-backed capital currently posted to Genesis reserve lanes</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.claimsPayingCapital)}>
              {formatSettlementUnits(props.model.claimsPayingCapital)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Live stress flags</span>
              <span className="plans-settings-lane">Queue-only capital sleeves and impairment stay visible while the bounded launch window remains under operator review</span>
            </div>
            <span className="plans-settings-address">
              {props.model.impairmentActive ? "Impairment active" : props.model.queueOnlyRedemptionsActive ? "Queue-only exits" : "Clear"}
            </span>
          </div>
        </div>

        <div className="plans-notice liquid-glass" role="status">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">lock</span>
          <p>
            <strong>Founder commitments are read-only here.</strong>{" "}
            Pending deposits are refundable holds, not active cover, not LP deposits, and not claims-paying reserve until activation or posting rules are satisfied.
          </p>
        </div>

        {props.founderCommitmentHref ? (
          <div className="plans-wizard-support-actions">
            <Link href={props.founderCommitmentHref} className="secondary-button inline-flex w-fit" target="_blank" rel="noreferrer">
              Open consumer Founder flow
            </Link>
          </div>
        ) : null}

        <div className="plans-settings-grid">
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Founder campaigns</span>
              <span className="plans-settings-lane">Read-only campaign status linked to this plan and policy series</span>
            </div>
            <span className="plans-settings-address">
              {props.model.founderCommitments.activeCampaignCount}/{props.model.founderCommitments.campaignCount} active
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Payment rails</span>
              <span className="plans-settings-lane">Accepted assets under the same Founder campaign, not split treasury campaigns</span>
            </div>
            <span className="plans-settings-address">
              {props.model.founderCommitments.waterfallRailCount}/{props.model.founderCommitments.paymentRailCount} waterfall
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Pending commitments</span>
              <span className="plans-settings-lane">Commitment positions still waiting for activation or refund</span>
            </div>
            <span className="plans-settings-address">{formatAmount(props.model.founderCommitments.pendingPositionCount)}</span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Custody pending</span>
              <span className="plans-settings-lane">Deposited token amount still held in the DomainAssetVault commitment lane</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.founderCommitments.pendingCustodyAmount)}>
              {formatSettlementUnits(props.model.founderCommitments.pendingCustodyAmount)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Coverage pending</span>
              <span className="plans-settings-lane">Coverage amount represented by pending commitments, not active coverage</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.founderCommitments.pendingCoverageAmount)}>
              {formatSettlementUnits(props.model.founderCommitments.pendingCoverageAmount)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Treasury inventory</span>
              <span className="plans-settings-lane">Legacy treasury-credit amount locked as inventory after activation</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.founderCommitments.treasuryInventoryAmount)}>
              {formatSettlementUnits(props.model.founderCommitments.treasuryInventoryAmount)}
            </span>
          </div>
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Pending reserve impact</span>
              <span className="plans-settings-lane">Claims-paying reserve impact from pending commitments</span>
            </div>
            <span className="plans-settings-address" title={rawAmountTitle(props.model.founderCommitments.claimsPayingReserveImpact)}>
              {formatSettlementUnits(props.model.founderCommitments.claimsPayingReserveImpact)}
            </span>
          </div>
        </div>

        {props.model.founderCommitments.rows.length > 0 ? (
          <div className="grid gap-3 lg:grid-cols-2">
            {props.model.founderCommitments.rows.map((row) => (
              <article key={row.address} className="operator-summary-card">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-sm font-semibold text-[var(--foreground)]">{row.displayName}</p>
                    <p className="field-help">
                      {row.campaignId} · {commitmentModeLabel(row.mode)} · {row.paymentRailCount} rail{row.paymentRailCount === 1 ? "" : "s"}
                    </p>
                  </div>
                  <span className={`status-pill ${row.status === 1 ? "status-ok" : "status-off"}`}>
                    {row.status === 1 ? "Active" : "Inactive"}
                  </span>
                </div>
                <div className="plans-settings-grid">
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Pending</span>
                    <span className="plans-settings-address" title={rawAmountTitle(row.pendingAmount)}>
                      {formatSettlementUnits(row.pendingAmount)}
                    </span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Policy series</span>
                    <span className="plans-settings-address">{row.policySeries ? shortHash(row.policySeries) : "Unlinked"}</span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Funding line</span>
                    <span className="plans-settings-address">{shortHash(row.coverageFundingLine)}</span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Terms hash</span>
                    <span className="plans-settings-address">{shortHash(row.termsHashHex)}</span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Activated</span>
                    <span className="plans-settings-address" title={rawAmountTitle(row.activatedAmount)}>
                      {formatSettlementUnits(row.activatedAmount)}
                    </span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Treasury locked</span>
                    <span className="plans-settings-address" title={rawAmountTitle(row.treasuryLockedAmount)}>
                      {formatSettlementUnits(row.treasuryLockedAmount)}
                    </span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Waterfall rails</span>
                    <span className="plans-settings-address">{formatAmount(row.waterfallRailCount)}</span>
                  </div>
                  <div className="plans-settings-row">
                    <span className="plans-settings-label">Refunded</span>
                    <span className="plans-settings-address" title={rawAmountTitle(row.refundedAmount)}>
                      {formatSettlementUnits(row.refundedAmount)}
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        ) : null}

        {props.model.founderCommitments.warnings.length > 0 ? (
          <div className="space-y-2">
            {props.model.founderCommitments.warnings.map((warning) => (
              <div key={warning} className="plans-notice liquid-glass" role="status">
                <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
                <p>{warning}</p>
              </div>
            ))}
          </div>
        ) : null}

        {props.model.posture.reasons.length > 0 ? (
          <div className="space-y-2">
            {props.model.posture.reasons.map((reason) => (
              <div key={reason} className="plans-notice liquid-glass" role="status">
                <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
                <p>{reason}</p>
              </div>
            ))}
          </div>
        ) : null}

        <div className="plans-wizard-support-grid">
          {[primarySku, demoSku].filter((entry): entry is NonNullable<typeof entry> => Boolean(entry)).map((sku) => (
            <section key={sku.skuKey} className="plans-wizard-support-card">
              <div className="space-y-1">
                <h3 className="plans-wizard-support-title">{sku.displayName}</h3>
                <p className="plans-wizard-support-copy">
                  {sku.publicStatusRule}
                </p>
              </div>
              <div className="plans-settings-grid">
                <div className="plans-settings-row">
                  <div>
                    <span className="plans-settings-label">Cover window</span>
                    <span className="plans-settings-lane">Published launch posture</span>
                  </div>
                  <span className="plans-settings-address">{sku.coverWindowDays} days</span>
                </div>
                <div className="plans-settings-row">
                  <div>
                    <span className="plans-settings-label">Reimbursement mode</span>
                    <span className="plans-settings-lane">Member-facing claims posture</span>
                  </div>
                  <span className="plans-settings-address">{sku.reimbursementMode}</span>
                </div>
                <div className="plans-settings-row">
                  <div>
                    <span className="plans-settings-label">Claims-paying capital</span>
                    <span className="plans-settings-lane">Posted capital currently attributed to this SKU</span>
                  </div>
                  <span className="plans-settings-address" title={rawAmountTitle(sku.claimsPayingCapital)}>
                    {formatSettlementUnits(sku.claimsPayingCapital)}
                  </span>
                </div>
                <div className="plans-settings-row">
                  <div>
                    <span className="plans-settings-label">Pending payout</span>
                    <span className="plans-settings-lane">Claimable or payable exposure for this SKU</span>
                  </div>
                  <span className="plans-settings-address" title={rawAmountTitle(sku.pendingPayoutAmount)}>
                    {formatSettlementUnits(sku.pendingPayoutAmount)}
                  </span>
                </div>
              </div>
              <div className="space-y-2">
                <div>
                  <p className="plans-card-eyebrow">Issue when</p>
                  <ul className="list-disc pl-5 text-sm text-[var(--muted)]">
                    {sku.issueWhen.map((row) => (
                      <li key={row}>{row}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="plans-card-eyebrow">Pause when</p>
                  <ul className="list-disc pl-5 text-sm text-[var(--muted)]">
                    {sku.pauseWhen.map((row) => (
                      <li key={row}>{row}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="plans-wizard-support-actions">
                <Link href={props.skuConsoleHrefs[sku.skuKey].claims} className="secondary-button inline-flex w-fit">
                  Open claim console
                </Link>
                <Link href={props.skuConsoleHrefs[sku.skuKey].treasury} className="secondary-button inline-flex w-fit">
                  Open reserve console
                </Link>
              </div>
            </section>
          ))}
        </div>

        <div className="plans-wizard-support-actions">
          {props.adminActionsEnabled ? (
            <Link href={props.bootstrapHref} className="secondary-button inline-flex w-fit">
              Rerun Genesis template
            </Link>
          ) : null}
          {props.planAddress ? (
            <Link href={props.claimsHref} className="secondary-button inline-flex w-fit">
              Open claim console
            </Link>
          ) : null}
          {props.planAddress ? (
            <Link href={props.treasuryHref} className="secondary-button inline-flex w-fit">
              Open Genesis treasury
            </Link>
          ) : null}
        </div>
      </article>

      <article className="plans-card heavy-glass">
        <div className="plans-card-head">
          <div>
            <p className="plans-card-eyebrow">Readiness checklist</p>
            <h2 className="plans-card-title plans-card-title-display">
              Bounded launch <em>items</em>
            </h2>
          </div>
          <span className="plans-card-meta">
            Template {GENESIS_PROTECT_ACUTE_TEMPLATE_KEY}
          </span>
        </div>
        <div className="grid gap-3 lg:grid-cols-2">
          {rows.map((row) => (
            <article key={row.key} className="operator-summary-card">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-[var(--foreground)]">{row.title}</p>
                  <p className="field-help">{row.detail}</p>
                </div>
              <span className={`status-pill ${row.ready ? "status-ok" : "status-off"}`}>
                {row.ready ? "Ready" : "Action needed"}
              </span>
            </div>
              {props.adminActionsEnabled ? (
                <Link href={row.href} className="secondary-button inline-flex w-fit">
                  {row.action}
                </Link>
              ) : null}
            </article>
          ))}
        </div>
      </article>
    </section>
  );
}
