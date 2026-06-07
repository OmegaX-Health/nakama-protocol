// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import {
  type CapitalClassSnapshot,
  type DomainAssetVaultSnapshot,
  type LiquidityPoolSnapshot,
  type LPPositionSnapshot,
} from "@/lib/protocol";
import { formatAmount } from "@/lib/canonical-ui";

type CapitalLpSelfServicePanelProps = {
  selectedPool: LiquidityPoolSnapshot | null;
  selectedClass: CapitalClassSnapshot | null;
  domainAssetVaults: DomainAssetVaultSnapshot[];
  lpPositions: LPPositionSnapshot[];
  onRefresh?: () => Promise<void> | void;
};

function shortenAddress(value: string | null | undefined): string {
  if (!value) return "None";
  if (value.length <= 14) return value;
  return `${value.slice(0, 6)}...${value.slice(-6)}`;
}

function toBigInt(value: LPPositionSnapshot["shares"]): bigint {
  if (typeof value === "bigint") return value;
  return BigInt(String(value));
}

export function CapitalLpSelfServicePanel(props: CapitalLpSelfServicePanelProps) {
  const vault = props.domainAssetVaults.find(
    (entry) =>
      entry.reserveDomain === props.selectedPool?.reserveDomain &&
      entry.assetMint === props.selectedPool?.depositAssetMint,
  ) ?? null;
  const classPositions = props.lpPositions.filter(
    (entry) => entry.capitalClass === props.selectedClass?.address,
  );
  const totalShares = classPositions.reduce((sum, entry) => sum + toBigInt(entry.shares), 0n);

  return (
    <article className="plans-card heavy-glass">
      <div className="plans-card-head">
        <div>
          <p className="plans-card-eyebrow">Capital archive</p>
          <h2 className="plans-card-title plans-card-title-display">
            LP self-service <em>retired</em>
          </h2>
        </div>
        <span className="plans-card-meta">Read-only</span>
      </div>

      <div className="plans-notice liquid-glass" role="status">
        <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
        <p>
          Public LP deposits and redemption queues are no longer part of the base protocol.
          Reserve capital now enters through plan funding lines and contribution records.
        </p>
      </div>

      <div className="plans-settings-grid">
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Selected pool</span>
            <span className="plans-settings-lane">Historical context from fixture or decoded state</span>
          </div>
          <span className="plans-settings-address">{props.selectedPool?.displayName ?? "None"}</span>
        </div>
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Selected class</span>
            <span className="plans-settings-lane">Historical context from fixture or decoded state</span>
          </div>
          <span className="plans-settings-address">{props.selectedClass?.displayName ?? "None"}</span>
        </div>
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Visible vault</span>
            <span className="plans-settings-lane">No LP transaction is built from this panel</span>
          </div>
          <span className="plans-settings-address">{shortenAddress(vault?.vaultTokenAccount)}</span>
        </div>
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Archived LP shares</span>
            <span className="plans-settings-lane">Read-only aggregate for the selected class</span>
          </div>
          <span className="plans-settings-address">{formatAmount(totalShares)}</span>
        </div>
      </div>
    </article>
  );
}
