// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

export function OracleRegistryVerificationPanel() {
  return (
    <section className="plans-shell-section">
      <div className="plans-card heavy-glass">
        <div className="plans-card-head">
          <div>
            <p className="plans-card-eyebrow">Oracle archive</p>
            <h2 className="plans-card-title plans-card-title-display">
              Registry transactions <em>retired</em>
            </h2>
          </div>
          <span className="plans-card-meta">Read-only</span>
        </div>
        <div className="plans-notice liquid-glass" role="status">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
          <p>
            The base protocol no longer creates or claims standalone oracle profiles. Operators use
            plan oracle authority plus claim evidence and decision-support fingerprints for audit
            traceability.
          </p>
        </div>
      </div>
    </section>
  );
}
