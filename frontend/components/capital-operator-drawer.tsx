// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import { WizardDetailSheet } from "@/components/wizard-detail-sheet";
import {
  type AllocationPositionSnapshot,
  type CapitalClassSnapshot,
  type DomainAssetVaultSnapshot,
  type FundingLineSnapshot,
  type HealthPlanSnapshot,
  type LiquidityPoolSnapshot,
  type LPPositionSnapshot,
  type ReserveDomainSnapshot,
} from "@/lib/protocol";

export type CapitalOperatorSection = "provision" | "controls" | "allocate" | "queue";

type CapitalOperatorDrawerProps = {
  open: boolean;
  initialSection?: CapitalOperatorSection;
  onOpenChange: (open: boolean) => void;
  onRefresh?: () => Promise<void> | void;
  reserveDomains: ReserveDomainSnapshot[];
  selectedPool: LiquidityPoolSnapshot | null;
  selectedClass: CapitalClassSnapshot | null;
  lpPositions: LPPositionSnapshot[];
  allocations: AllocationPositionSnapshot[];
  plans: HealthPlanSnapshot[];
  fundingLines: FundingLineSnapshot[];
  domainAssetVaults: DomainAssetVaultSnapshot[];
};

function StatRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="plans-settings-row">
      <div>
        <span className="plans-settings-label">{label}</span>
        <span className="plans-settings-lane">Read-only archive context</span>
      </div>
      <span className="plans-settings-address">{value}</span>
    </div>
  );
}

export function CapitalOperatorDrawer(props: CapitalOperatorDrawerProps) {
  const meta = [
    props.selectedPool ? { label: props.selectedPool.displayName, tone: "muted" as const } : null,
    props.selectedClass ? { label: props.selectedClass.displayName, tone: "accent" as const } : null,
  ].filter(Boolean) as Array<{ label: string; tone?: "default" | "accent" | "muted" }>;

  return (
    <WizardDetailSheet
      open={props.open}
      onOpenChange={props.onOpenChange}
      title="Capital actions retired"
      summary="Liquidity pools, capital classes, allocations, LP credentialing, and redemption queues are not part of the trimmed base protocol."
      meta={meta}
      size="wide"
    >
      <div className="operator-drawer">
        <div className="operator-drawer-body">
          <fieldset className="operator-drawer-fieldset">
            <legend className="operator-drawer-legend">Current capital model</legend>
            <p className="operator-drawer-hint">
              Operators now use plan funding lines for sponsor money, premiums, reserve-capital
              deposits, capital returns, and reserve earnings. Historical pool/class/allocation
              snapshots can remain visible for analysis, but this drawer does not build retired
              capital-market transactions.
            </p>
          </fieldset>

          <div className="plans-settings-grid">
            <StatRow label="Reserve domains" value={String(props.reserveDomains.length)} />
            <StatRow label="Plans" value={String(props.plans.length)} />
            <StatRow label="Funding lines" value={String(props.fundingLines.length)} />
            <StatRow label="Visible vaults" value={String(props.domainAssetVaults.length)} />
            <StatRow label="Archived pools" value={props.selectedPool?.displayName ?? "None selected"} />
            <StatRow label="Archived classes" value={props.selectedClass?.displayName ?? "None selected"} />
            <StatRow label="Archived allocations" value={String(props.allocations.length)} />
            <StatRow label="Archived LP positions" value={String(props.lpPositions.length)} />
          </div>
        </div>
      </div>
    </WizardDetailSheet>
  );
}
