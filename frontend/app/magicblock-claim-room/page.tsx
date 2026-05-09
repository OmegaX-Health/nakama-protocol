// SPDX-License-Identifier: AGPL-3.0-or-later

import type { Metadata } from "next";
import {
  CheckCircle2,
  EyeOff,
  FileCheck2,
  Fingerprint,
  LockKeyhole,
  Network,
  ReceiptText,
} from "lucide-react";

const REVIEW_PROGRAM_ID = "FADqaRcJHERauzMo3BRzXZVY2qvrpPqg1ie2FGqACCVn";

const proofSteps = [
  {
    label: "Prepare",
    title: "Evidence packet",
    detail:
      "Medical documents stay inside the review workspace. The public trail keeps safe metadata and a checksum.",
  },
  {
    label: "Open",
    title: "On-chain case",
    detail:
      "Solana anchors the claim case, schema hash, and evidence checksum without exposing source documents.",
  },
  {
    label: "Delegate",
    title: "Fast review lane",
    detail:
      "MagicBlock handles the review session so reviewer output can be prepared quickly.",
  },
  {
    label: "Review",
    title: "Reviewer result",
    detail:
      "The reviewer checks completeness and emits result hashes plus artifact references.",
  },
  {
    label: "Pay",
    title: "Payment preview",
    detail:
      "A devnet reimbursement preview confirms that the payment rail was invoked.",
  },
  {
    label: "Commit",
    title: "Public receipt out",
    detail:
      "The review surface commits a public receipt that claim operators can verify before attestation.",
  },
] as const;

const proofSignals = [
  {
    icon: <EyeOff className="h-4 w-4" strokeWidth={1.9} />,
    label: "Evidence privacy",
    value: "Private docs",
    meta: "Raw files stay off-chain",
  },
  {
    icon: <Network className="h-4 w-4" strokeWidth={1.9} />,
    label: "Review session",
    value: "Fast review",
    meta: "Reviewer output is hashed",
  },
  {
    icon: <CheckCircle2 className="h-4 w-4" strokeWidth={1.9} />,
    label: "Public output",
    value: "Hash receipt",
    meta: "Only hashes are published",
  },
  {
    icon: <ReceiptText className="h-4 w-4" strokeWidth={1.9} />,
    label: "Settlement",
    value: "Receipt linked",
    meta: "Operators verify before settlement",
  },
] as const;

const auditRows = [
  {
    label: "Review program",
    value: REVIEW_PROGRAM_ID,
    detail: "Public program anchoring the demo review receipt.",
  },
  {
    label: "Private intake",
    value: "Evidence checksum",
    detail: "Medical records remain off-chain and private to the review workspace.",
  },
  {
    label: "Public attestation",
    value: "Review receipt",
    detail: "The public record receives the final review hash receipt, not the raw packet.",
  },
] as const;

export const metadata: Metadata = {
  title: "MagicBlock Claim Room | OmegaX Protocol",
  description:
    "A MagicBlock-powered claim review surface for OmegaX Protect medical claims.",
};

export default function MagicBlockClaimRoomPage() {
  return (
    <div className="plans-shell">
      <div className="plans-scroll">
        <header className="plans-hero">
          <div className="plans-hero-glow" aria-hidden="true" />
          <div className="plans-hero-head">
            <div className="plans-hero-copy">
              <span className="plans-hero-eyebrow">Private claim review</span>
              <h1 className="plans-hero-title">
                OmegaX claim <em>privacy</em>
              </h1>
              <p className="plans-hero-subtitle">
                Medical evidence stays inside the review workspace while Solana receives a review receipt operators can verify before settlement.
              </p>
            </div>
            <div className="plans-hero-actions">
              <span className="plans-secondary-cta plans-action-disabled" aria-disabled="true">
                <LockKeyhole className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />
                Demo surface
              </span>
            </div>
          </div>
        </header>

        <section className="plans-kpi-strip" aria-label="Claim privacy audit signals">
          {proofSignals.map((signal) => (
            <div key={signal.label} className="plans-kpi-metric">
              <span className="plans-kpi-label">{signal.label}</span>
              <span className="plans-kpi-value">
                {signal.icon}
                {signal.value}
              </span>
              <span className="plans-kpi-meta">{signal.meta}</span>
            </div>
          ))}
        </section>

        <div className="plans-body">
          <section className="plans-main">
            <article className="plans-card heavy-glass">
              <div className="plans-card-head">
                <div>
                  <p className="plans-card-eyebrow">Review flow</p>
                  <h2 className="plans-card-title plans-card-title-display">
                    Private review, <em>public receipt</em>
                  </h2>
                </div>
                <span className="plans-card-meta">
                  <span className="plans-live-dot" aria-hidden="true" />
                  Demo
                </span>
              </div>
              <p className="plans-card-body">
                The review surface separates medical evidence from settlement evidence. Operators can verify the review record without publishing the source documents.
              </p>

              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                {proofSteps.map((step, index) => (
                  <ProofStep key={step.label} step={step} index={index} />
                ))}
              </div>
            </article>
          </section>

          <aside className="plans-rail">
            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">Audit anchor</span>
                <span className="plans-rail-subtag">Public receipt</span>
              </div>
              <div className="plans-rail-hero">
                <span className="plans-rail-hero-val">Claim review trail</span>
                <span className="plans-rail-hero-sub">
                  Private evidence in. Public receipt out. Settlement stays on Solana.
                </span>
              </div>
            </section>

            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">Visible records</span>
                <span className="plans-rail-subtag">No documents</span>
              </div>
              <div className="plans-rail-trail">
                {auditRows.map((row) => (
                  <ProofRow key={row.label} {...row} />
                ))}
              </div>
            </section>

            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">Demo posture</span>
                <Fingerprint
                  className="h-5 w-5 text-[color:var(--accent)]"
                  strokeWidth={1.8}
                  aria-hidden="true"
                />
              </div>
              <p className="plans-rail-empty-copy">
                Operator APIs remain private; this public view shows the review receipt only.
              </p>
            </section>
          </aside>
        </div>
      </div>
    </div>
  );
}

function ProofStep({
  step,
  index,
}: {
  step: (typeof proofSteps)[number];
  index: number;
}) {
  return (
    <div className="workbench-inline-card">
      <div className="flex items-center justify-between gap-3">
        <span className="workbench-card-meta">{String(index + 1).padStart(2, "0")}</span>
        {index < proofSteps.length - 1 ? (
          <span className="claim-room-step-rule" aria-hidden="true" />
        ) : (
          <ReceiptText
            className="h-4 w-4 text-[color:var(--accent)]"
            strokeWidth={1.8}
            aria-hidden="true"
          />
        )}
      </div>
      <p className="mt-4 workbench-panel-eyebrow">{step.label}</p>
      <h3 className="mt-1 text-base font-semibold">{step.title}</h3>
      <p className="mt-2 text-sm leading-6 text-[color:var(--muted-foreground)]">
        {step.detail}
      </p>
    </div>
  );
}

function ProofRow({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <div className="plans-rail-event plans-rail-event-verified">
      <span className="plans-rail-event-dot" aria-hidden="true" />
      <div className="plans-rail-event-copy">
        <div className="plans-rail-event-row">
          <strong className="plans-rail-event-label">{label}</strong>
          <FileCheck2 className="h-3.5 w-3.5 text-[color:var(--accent)]" strokeWidth={1.8} aria-hidden="true" />
        </div>
        <p className="plans-rail-event-detail">{detail}</p>
        <p className="mt-1 break-all font-mono text-[0.66rem] leading-5 text-[color:var(--foreground)]">
          {value}
        </p>
      </div>
    </div>
  );
}
