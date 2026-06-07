// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

type WizardMode = "register" | "update";

type OracleProfileWizardProps = {
  mode: WizardMode;
  oracleAddress?: string;
};

export function OracleProfileWizard({ mode, oracleAddress = "" }: OracleProfileWizardProps) {
  return (
    <section className="plans-shell-section">
      <div className="plans-card heavy-glass">
        <div className="plans-card-head">
          <div>
            <p className="plans-card-eyebrow">Oracle archive</p>
            <h1 className="plans-card-title plans-card-title-display">
              Oracle profile <em>{mode === "register" ? "registration" : "updates"} retired</em>
            </h1>
          </div>
          <span className="plans-card-meta">Read-only</span>
        </div>
        <div className="plans-notice liquid-glass" role="status">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
          <p>
            On-chain oracle profile registration and claim transactions are no longer part of the
            trimmed base protocol. Plan-level oracle authority and claim proof fingerprints carry
            the current audit path.
          </p>
        </div>
        <div className="plans-settings-grid">
          <div className="plans-settings-row">
            <div>
              <span className="plans-settings-label">Requested oracle</span>
              <span className="plans-settings-lane">Historical context only</span>
            </div>
            <span className="plans-settings-address">{oracleAddress || "None"}</span>
          </div>
        </div>
      </div>
    </section>
  );
}
