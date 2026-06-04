// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

type PoolTreasuryPanelProps = {
  poolAddress: string;
};

function shortAddress(value: string): string {
  if (!value || value.length < 12) return value || "n/a";
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
}

export function PoolTreasuryPanel({ poolAddress }: PoolTreasuryPanelProps) {
  return (
    <section className="surface-card-soft space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="metric-label">Treasury status</p>
          <p className="field-help">
            Pool custody now settles through claim, redemption, and linked-obligation payout paths.
          </p>
        </div>
        <span className="status-pill status-ok">Fee rails removed</span>
      </div>
      <dl className="operator-summary-list">
        <div>
          <dt>Pool</dt>
          <dd className="break-all font-mono">{shortAddress(poolAddress)}</dd>
        </div>
        <div>
          <dt>Withdraw controls</dt>
          <dd>Not exposed on the current program surface</dd>
        </div>
      </dl>
    </section>
  );
}
