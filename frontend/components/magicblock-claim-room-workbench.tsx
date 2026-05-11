// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import { type FormEvent, type ReactNode, useState } from "react";
import {
  CheckCircle2,
  EyeOff,
  Fingerprint,
  Info,
  LockKeyhole,
  Network,
  ReceiptText,
  Search,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import { useConnection } from "@solana/wallet-adapter-react";

import { useNetworkContext } from "@/components/network-context";
import {
  derivePrivateClaimReviewSessionPda,
  loadPrivateClaimReviewReceipt,
  PRIVATE_CLAIM_REVIEW_PROGRAM_ID,
  type PrivateClaimReviewLookupResult,
  type PrivateClaimReviewReceipt,
} from "@/lib/private-claim-review";
import { toExplorerAddressLink } from "@/lib/protocol";

const DEVNET_REVIEW_PROGRAM_ID = PRIVATE_CLAIM_REVIEW_PROGRAM_ID.toBase58();

const devnetProofSignals = [
  {
    icon: <EyeOff className="h-4 w-4" strokeWidth={1.9} />,
    label: "Evidence privacy",
    value: "Private docs",
    meta: "Raw files stay off-chain",
  },
  {
    icon: <Network className="h-4 w-4" strokeWidth={1.9} />,
    label: "Review lane",
    value: "Devnet ER",
    meta: "Session PDA only",
  },
  {
    icon: <CheckCircle2 className="h-4 w-4" strokeWidth={1.9} />,
    label: "Public output",
    value: "Hash receipt",
    meta: "No clinical content",
  },
  {
    icon: <ReceiptText className="h-4 w-4" strokeWidth={1.9} />,
    label: "Settlement",
    value: "Solana kernel",
    meta: "Standard reserve path",
  },
] as const;

const mainnetProofSignals = [
  {
    icon: <EyeOff className="h-4 w-4" strokeWidth={1.9} />,
    label: "Evidence privacy",
    value: "Private docs",
    meta: "Raw files stay off-chain",
  },
  {
    icon: <LockKeyhole className="h-4 w-4" strokeWidth={1.9} />,
    label: "Review lane",
    value: "Not configured",
    meta: "No mainnet ER",
  },
  {
    icon: <CheckCircle2 className="h-4 w-4" strokeWidth={1.9} />,
    label: "Public output",
    value: "No demo receipt",
    meta: "Fail-closed",
  },
  {
    icon: <ReceiptText className="h-4 w-4" strokeWidth={1.9} />,
    label: "Settlement",
    value: "Solana kernel",
    meta: "Standard reserve path",
  },
] as const;

const devnetProofSteps = [
  {
    label: "Prepare",
    title: "Evidence packet",
    detail:
      "Medical documents stay inside the review workspace. The public trail keeps safe metadata and a checksum.",
  },
  {
    label: "Open",
    title: "Base-layer session",
    detail:
      "Solana anchors the review-session PDA, schema hash, and evidence checksum without exposing source documents.",
  },
  {
    label: "Delegate",
    title: "Devnet review lane",
    detail:
      "Only the review-session PDA is delegated to MagicBlock. Claim cases, reserves, vaults, and obligations stay on the standard protocol.",
  },
  {
    label: "Review",
    title: "Reviewer result",
    detail:
      "The reviewer checks completeness and emits result hashes plus artifact references. Raw PHI is never published here.",
  },
  {
    label: "Reference",
    title: "Payment ref preview",
    detail:
      "Payment-reference storage is devnet demo evidence only. Production reimbursement still uses the normal reserve and claim-settlement kernel.",
  },
  {
    label: "Commit",
    title: "Public receipt out",
    detail:
      "The session commits a review receipt that claim operators can verify before using the normal attestation path.",
  },
] as const;

const mainnetProofSteps = [
  {
    label: "Prepare",
    title: "Private evidence remains off-chain",
    detail:
      "Medical documents still belong inside the private review workspace. This page never asks for or stores claim documents.",
  },
  {
    label: "Open",
    title: "No mainnet review session",
    detail:
      "No MagicBlock review-session PDA is configured for mainnet. Production claim cases use the standard base-layer protocol surface.",
  },
  {
    label: "Delegate",
    title: "No mainnet delegation",
    detail:
      "MagicBlock delegation is disabled here. Claim cases, reserves, vaults, and obligations remain on the standard protocol.",
  },
  {
    label: "Review",
    title: "Operator review stays private",
    detail:
      "Any real review workflow must be approved separately before a public mainnet receipt can be shown.",
  },
  {
    label: "Reference",
    title: "No payment-reference preview",
    detail:
      "Payment-reference storage is devnet demo evidence only. Production reimbursement still uses the normal reserve and claim-settlement kernel.",
  },
  {
    label: "Commit",
    title: "Fail-closed public posture",
    detail:
      "The public page shows that no MagicBlock receipt is live on mainnet instead of implying a production review lane exists.",
  },
] as const;

const visibleRecords = [
  {
    label: "Devnet review program",
    value: DEVNET_REVIEW_PROGRAM_ID,
    detail: "Public devnet program anchoring the demo review receipt.",
  },
  {
    label: "Private intake",
    value: "Evidence checksum",
    detail: "Medical records remain off-chain and private to the review workspace.",
  },
  {
    label: "Public attestation input",
    value: "Review receipt",
    detail: "The public record receives the final review hash receipt, not the raw packet.",
  },
] as const;

export function MagicBlockClaimRoomWorkbench() {
  const { connection } = useConnection();
  const { selectedNetwork } = useNetworkContext();
  const isMainnet = selectedNetwork === "mainnet-beta";
  const networkLabel = isMainnet ? "Mainnet" : "Devnet";
  const postureLabel = isMainnet ? "Mainnet unavailable" : "Devnet verifier";
  const proofSignals = isMainnet ? mainnetProofSignals : devnetProofSignals;
  const proofSteps = isMainnet ? mainnetProofSteps : devnetProofSteps;
  const postureCopy = isMainnet
    ? "Receipt verification is unavailable on mainnet because no MagicBlock private-review program is configured. Production claims stay on the standard Solana claim, oracle, and reserve-settlement path."
    : "Paste or derive a MagicBlock private-review session PDA to verify the public hash receipt on devnet. No claim documents, signatures, or payment movement are requested here.";
  const flowTitle = isMainnet ? "Closed review posture" : "How the receipt is produced";
  const flowCopy = isMainnet
    ? "This public page is a fail-closed receipt posture for mainnet. It does not create claims, upload documents, delegate sessions, or move reimbursement funds."
    : "The verifier reads the public review-session account and checks that it belongs to the MagicBlock private-review adjunct before showing safe receipt metadata.";
  const railTitle = isMainnet ? "No live review trail" : "Claim review trail";
  const railCopy = isMainnet
    ? "Mainnet has no MagicBlock receipt program configured. Settlement stays on Solana."
    : "Private evidence in. Public receipt out. Settlement stays on Solana.";
  const [sessionAddress, setSessionAddress] = useState("");
  const [sessionAuthority, setSessionAuthority] = useState("");
  const [claimCase, setClaimCase] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [lookupResult, setLookupResult] = useState<PrivateClaimReviewLookupResult | null>(null);
  const [lookupPending, setLookupPending] = useState(false);
  const [deriveMessage, setDeriveMessage] = useState<string | null>(null);
  const canLookup = !isMainnet && sessionAddress.trim().length > 0 && !lookupPending;

  async function runLookup(address: string, options: { keepDeriveMessage?: boolean } = {}) {
    if (isMainnet) return;
    setLookupPending(true);
    if (!options.keepDeriveMessage) setDeriveMessage(null);
    try {
      const result = await loadPrivateClaimReviewReceipt(connection, address);
      setLookupResult(result);
    } finally {
      setLookupPending(false);
    }
  }

  async function handleLookupSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canLookup) return;
    await runLookup(sessionAddress.trim());
  }

  async function handleDeriveSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (isMainnet || lookupPending) return;
    try {
      const derived = derivePrivateClaimReviewSessionPda({
        sessionAuthority,
        claimCase,
        sessionId,
      });
      const derivedAddress = derived.toBase58();
      setSessionAddress(derivedAddress);
      setDeriveMessage("Derived review-session PDA from the public seeds.");
      await runLookup(derivedAddress, { keepDeriveMessage: true });
    } catch (cause) {
      setLookupResult({
        kind: "invalid-address",
        message: cause instanceof Error && cause.message
          ? cause.message
          : "Enter valid session authority, claim case, and session ID values.",
      });
      setDeriveMessage(null);
    }
  }

  const auditRows = isMainnet
    ? [
        {
          label: "Mainnet status",
          value: "Not configured",
          detail: "This route intentionally fails closed on mainnet until a separate production review program is approved.",
        },
        ...visibleRecords.slice(1),
      ]
    : visibleRecords;
  const verifiedReceipt = lookupResult?.kind === "found" ? lookupResult.receipt : null;

  return (
    <div className="plans-shell claim-room-shell">
      <div className="plans-scroll">
        <header className="plans-hero">
          <div className="plans-hero-glow" aria-hidden="true" />
          <div className="plans-hero-head">
            <div className="plans-hero-copy">
              <span className="plans-hero-eyebrow">Public receipt verifier</span>
              <h1 className="plans-hero-title">
                MagicBlock receipt <em>verifier</em>
              </h1>
              <p className="plans-hero-subtitle">
                {postureCopy}
              </p>
            </div>
            <div className="plans-hero-actions">
              <span
                className={`claim-room-posture-badge${isMainnet ? " claim-room-posture-badge-closed" : ""}`}
                role="status"
              >
                <LockKeyhole className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />
                {postureLabel}
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
            <article className="plans-card heavy-glass claim-room-verifier-card">
              <VerifierPanel
                isMainnet={isMainnet}
                sessionAddress={sessionAddress}
                sessionAuthority={sessionAuthority}
                claimCase={claimCase}
                sessionId={sessionId}
                lookupPending={lookupPending}
                lookupResult={lookupResult}
                deriveMessage={deriveMessage}
                canLookup={canLookup}
                selectedNetwork={selectedNetwork}
                onSessionAddressChange={setSessionAddress}
                onSessionAuthorityChange={setSessionAuthority}
                onClaimCaseChange={setClaimCase}
                onSessionIdChange={setSessionId}
                onLookupSubmit={handleLookupSubmit}
                onDeriveSubmit={handleDeriveSubmit}
              />
            </article>

            <article className="plans-card heavy-glass">
              <div className="plans-card-head">
                <div>
                  <p className="plans-card-eyebrow">Receipt path</p>
                  <h2 className="plans-card-title plans-card-title-display">
                    {isMainnet ? (
                      <>
                        Closed review <em>posture</em>
                      </>
                    ) : (
                      <>
                        Private review, <em>public receipt</em>
                      </>
                    )}
                  </h2>
                </div>
                <span className="plans-card-meta">
                  <span className="plans-live-dot" aria-hidden="true" />
                  {networkLabel}
                </span>
              </div>
              <p className="plans-card-body">
                {flowCopy}
              </p>

              <ol className="claim-room-flow-list" aria-label={flowTitle}>
                {proofSteps.map((step, index) => (
                  <ProofStep
                    key={step.label}
                    step={step}
                    index={index}
                    isLast={index === proofSteps.length - 1}
                  />
                ))}
              </ol>
            </article>
          </section>

          <aside className="plans-rail">
            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">Audit anchor</span>
                <span className="plans-rail-subtag">{postureLabel}</span>
              </div>
              <div className="plans-rail-hero">
                <span className="plans-rail-hero-val">{railTitle}</span>
                <span className="plans-rail-hero-sub">
                  {railCopy}
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
                <span className="plans-rail-tag">What this proves</span>
                <ShieldCheck
                  className="h-5 w-5 text-[color:var(--accent)]"
                  strokeWidth={1.8}
                  aria-hidden="true"
                />
              </div>
              <ul className="claim-room-proof-list">
                <li>{verifiedReceipt ? "The account is owned by the devnet private-review adjunct." : "A matching receipt must be owned by the devnet private-review adjunct."}</li>
                <li>{verifiedReceipt ? "The account decodes as a PrivateClaimReviewSession." : "Only PrivateClaimReviewSession accounts can pass verification."}</li>
                <li>Only public hashes, authorities, lifecycle state, and linked protocol addresses are exposed.</li>
              </ul>
            </section>

            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">What it does not prove</span>
                <Info
                  className="h-5 w-5 text-[color:var(--muted-foreground)]"
                  strokeWidth={1.8}
                  aria-hidden="true"
                />
              </div>
              <ul className="claim-room-proof-list">
                <li>It does not prove the raw medical evidence is valid.</li>
                <li>It does not create active cover, settle a claim, or move reimbursement funds.</li>
                <li>Claim operators must still verify registry binding, expected hashes, and normal protocol attestation rules.</li>
              </ul>
            </section>

            <section className="plans-rail-card heavy-glass">
              <div className="plans-rail-head">
                <span className="plans-rail-tag">Boundary</span>
                <Fingerprint
                  className="h-5 w-5 text-[color:var(--accent)]"
                  strokeWidth={1.8}
                  aria-hidden="true"
                />
              </div>
              <p className="plans-rail-empty-copy">
                Operator APIs remain private; this public view shows only receipt posture and safe audit metadata.
              </p>
            </section>
          </aside>
        </div>
      </div>
    </div>
  );
}

function VerifierPanel({
  isMainnet,
  sessionAddress,
  sessionAuthority,
  claimCase,
  sessionId,
  lookupPending,
  lookupResult,
  deriveMessage,
  canLookup,
  selectedNetwork,
  onSessionAddressChange,
  onSessionAuthorityChange,
  onClaimCaseChange,
  onSessionIdChange,
  onLookupSubmit,
  onDeriveSubmit,
}: {
  isMainnet: boolean;
  sessionAddress: string;
  sessionAuthority: string;
  claimCase: string;
  sessionId: string;
  lookupPending: boolean;
  lookupResult: PrivateClaimReviewLookupResult | null;
  deriveMessage: string | null;
  canLookup: boolean;
  selectedNetwork: string;
  onSessionAddressChange: (value: string) => void;
  onSessionAuthorityChange: (value: string) => void;
  onClaimCaseChange: (value: string) => void;
  onSessionIdChange: (value: string) => void;
  onLookupSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onDeriveSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <div className="claim-room-verifier-grid">
      <div className="claim-room-verifier-controls">
        <div className="plans-card-head">
          <div>
            <p className="plans-card-eyebrow">On-chain lookup</p>
            <h2 className="plans-card-title plans-card-title-display">
              Verify a review-session <em>receipt</em>
            </h2>
          </div>
          <span className={`claim-room-posture-badge${isMainnet ? " claim-room-posture-badge-closed" : ""}`}>
            <LockKeyhole className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />
            {isMainnet ? "Unavailable" : "Read-only"}
          </span>
        </div>
        <p className="plans-card-body">
          {isMainnet
            ? "No MagicBlock private-review verifier is configured for mainnet. This page will not query a mainnet adjunct program until one is explicitly approved."
            : "Enter a review-session PDA, or derive it from the public session seeds. The verifier only reads public-safe account data from the selected RPC connection."}
        </p>

        <form className="claim-room-lookup-form" onSubmit={onLookupSubmit}>
          <label className="claim-room-field">
            <span className="plans-hero-select-eyebrow">Review session PDA</span>
            <input
              type="text"
              className="plans-wizard-input claim-room-input"
              value={sessionAddress}
              onChange={(event) => onSessionAddressChange(event.target.value)}
              disabled={isMainnet || lookupPending}
              placeholder="Paste PrivateClaimReviewSession account address"
              autoComplete="off"
              spellCheck={false}
            />
          </label>
          <button
            type="submit"
            className="plans-primary-cta claim-room-lookup-button"
            disabled={!canLookup}
          >
            <Search className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />
            {lookupPending ? "Checking" : "Verify receipt"}
          </button>
        </form>

        <details className="claim-room-derive-panel">
          <summary>Seed-derived lookup</summary>
          <form className="claim-room-derive-form" onSubmit={onDeriveSubmit}>
            <label className="claim-room-field">
              <span className="plans-hero-select-eyebrow">Session authority</span>
              <input
                type="text"
                className="plans-wizard-input claim-room-input"
                value={sessionAuthority}
                onChange={(event) => onSessionAuthorityChange(event.target.value)}
                disabled={isMainnet || lookupPending}
                placeholder="Authority that opened the private review"
                autoComplete="off"
                spellCheck={false}
              />
            </label>
            <label className="claim-room-field">
              <span className="plans-hero-select-eyebrow">Claim case</span>
              <input
                type="text"
                className="plans-wizard-input claim-room-input"
                value={claimCase}
                onChange={(event) => onClaimCaseChange(event.target.value)}
                disabled={isMainnet || lookupPending}
                placeholder="Linked ClaimCase PDA"
                autoComplete="off"
                spellCheck={false}
              />
            </label>
            <label className="claim-room-field claim-room-field-wide">
              <span className="plans-hero-select-eyebrow">Session ID</span>
              <input
                type="text"
                className="plans-wizard-input claim-room-input"
                value={sessionId}
                onChange={(event) => onSessionIdChange(event.target.value)}
                disabled={isMainnet || lookupPending}
                placeholder="Session ID used by open_review_session"
                autoComplete="off"
                spellCheck={false}
              />
            </label>
            <button
              type="submit"
              className="plans-secondary-cta claim-room-derive-button"
              disabled={isMainnet || lookupPending}
            >
              Derive and verify
            </button>
          </form>
          {deriveMessage ? <p className="claim-room-helper-copy">{deriveMessage}</p> : null}
        </details>
      </div>

      <ReceiptLookupResult
        isMainnet={isMainnet}
        lookupPending={lookupPending}
        lookupResult={lookupResult}
        selectedNetwork={selectedNetwork}
      />
    </div>
  );
}

function ReceiptLookupResult({
  isMainnet,
  lookupPending,
  lookupResult,
  selectedNetwork,
}: {
  isMainnet: boolean;
  lookupPending: boolean;
  lookupResult: PrivateClaimReviewLookupResult | null;
  selectedNetwork: string;
}) {
  if (isMainnet) {
    return (
      <div className="claim-room-result-panel claim-room-result-panel-muted">
        <ResultPanelHeader
          icon={<LockKeyhole className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />}
          eyebrow="Mainnet"
          title="Verification unavailable"
        />
        <p>
          No mainnet MagicBlock receipt program is configured. Production claim review and settlement stay on the standard protocol path.
        </p>
      </div>
    );
  }

  if (lookupPending) {
    return (
      <div className="claim-room-result-panel claim-room-result-panel-muted">
        <ResultPanelHeader
          icon={<Search className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />}
          eyebrow="Lookup"
          title="Checking on-chain receipt"
        />
        <p>Reading the selected RPC endpoint and decoding the account as a PrivateClaimReviewSession.</p>
      </div>
    );
  }

  if (!lookupResult) {
    return (
      <div className="claim-room-result-panel claim-room-result-panel-muted">
        <ResultPanelHeader
          icon={<ReceiptText className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />}
          eyebrow="Ready"
          title="Paste a receipt account"
        />
        <p>
          The verifier checks account ownership, account type, and public-safe receipt fields before showing any claim-review metadata.
        </p>
      </div>
    );
  }

  if (lookupResult.kind !== "found") {
    return <ReceiptLookupError result={lookupResult} />;
  }

  return <ReceiptDetails receipt={lookupResult.receipt} selectedNetwork={selectedNetwork} />;
}

function ReceiptLookupError({ result }: { result: Exclude<PrivateClaimReviewLookupResult, { kind: "found" }> }) {
  const detailRows =
    result.kind === "wrong-owner"
      ? [
          { label: "Owner", value: result.owner },
          { label: "Expected", value: result.expectedOwner },
        ]
      : result.kind === "wrong-account-type"
        ? [{ label: "Discriminator", value: result.discriminator || "Unavailable" }]
        : "address" in result && result.address
          ? [{ label: "Address", value: result.address }]
          : [];

  return (
    <div className="claim-room-result-panel claim-room-result-panel-error">
      <ResultPanelHeader
        icon={<XCircle className="h-4 w-4" strokeWidth={1.9} aria-hidden="true" />}
        eyebrow="Not verified"
        title={lookupErrorTitle(result.kind)}
      />
      <p>{result.message}</p>
      {detailRows.length > 0 ? (
        <div className="claim-room-result-minirows">
          {detailRows.map((row) => (
            <div key={row.label} className="claim-room-minirow">
              <span>{row.label}</span>
              <strong title={row.value}>{shortenMiddle(row.value, 9)}</strong>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function ReceiptDetails({
  receipt,
  selectedNetwork,
}: {
  receipt: PrivateClaimReviewReceipt;
  selectedNetwork: string;
}) {
  const addressRows = [
    { label: "Session PDA", value: receipt.sessionAddress },
    { label: "Claim case", value: receipt.claimCase },
    { label: "Health plan", value: receipt.healthPlan },
    { label: "Policy series", value: receipt.policySeries },
    { label: "Session authority", value: receipt.sessionAuthority },
    { label: "Reviewer", value: receipt.reviewerAuthority },
    { label: "Payment attestor", value: receipt.paymentAttestor },
    { label: "Review operator", value: receipt.reviewOperator },
  ];
  const hashRows = [
    { label: "Evidence ref", value: receipt.evidenceRefHash },
    { label: "Schema key", value: receipt.schemaKeyHash },
    { label: "Schema hash", value: receipt.schemaHash },
    { label: "Review result", value: receipt.reviewResultHash },
    { label: "Review artifact", value: receipt.reviewArtifactHash },
    { label: "Review binary", value: receipt.reviewBinaryHash },
    { label: "TEE attestation", value: receipt.teeAttestationDigest },
    { label: "Payment ref", value: receipt.privatePaymentRefHash },
  ];
  const timestampRows = [
    { label: "Opened", value: receipt.openedAt },
    { label: "Delegated", value: receipt.delegatedAt },
    { label: "Reviewed", value: receipt.reviewedAt },
    { label: "Payment recorded", value: receipt.paymentRecordedAt },
    { label: "Committed", value: receipt.committedAt },
    { label: "Failed", value: receipt.failedAt },
  ].filter((row) => row.value > 0);

  return (
    <div className="claim-room-result-panel claim-room-result-panel-found">
      <div className="claim-room-result-head">
        <div>
          <p className="plans-card-eyebrow">Verified receipt</p>
          <h3 className="claim-room-result-title">{receipt.sessionId || "Private review session"}</h3>
        </div>
        <span className={`claim-room-status-badge claim-room-status-${receipt.status}`}>
          {receipt.statusLabel}
        </span>
      </div>

      <a
        href={toExplorerAddressLink(receipt.sessionAddress, selectedNetwork)}
        target="_blank"
        rel="noreferrer"
        className="claim-room-explorer-link"
      >
        View account on Solana Explorer
      </a>

      <ReceiptRows title="Linked accounts" rows={addressRows} />
      <ReceiptRows title="Receipt hashes" rows={hashRows.map((row) => ({
        ...row,
        value: isZeroHash(row.value) ? "Not recorded" : row.value,
      }))} />
      {timestampRows.length > 0 ? (
        <ReceiptRows
          title="Timestamps"
          rows={timestampRows.map((row) => ({ label: row.label, value: formatUnixSeconds(row.value) }))}
        />
      ) : null}
    </div>
  );
}

function ReceiptRows({
  title,
  rows,
}: {
  title: string;
  rows: Array<{ label: string; value: string }>;
}) {
  return (
    <div className="claim-room-result-section">
      <h4>{title}</h4>
      <div className="claim-room-result-rows">
        {rows.map((row) => (
          <div key={row.label} className="claim-room-result-row">
            <span>{row.label}</span>
            <strong title={row.value}>{shortenMiddle(row.value, 12)}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}

function ResultPanelHeader({
  icon,
  eyebrow,
  title,
}: {
  icon: ReactNode;
  eyebrow: string;
  title: string;
}) {
  return (
    <div className="claim-room-result-head">
      <div>
        <p className="plans-card-eyebrow">{eyebrow}</p>
        <h3 className="claim-room-result-title">{title}</h3>
      </div>
      <span className="claim-room-result-icon">{icon}</span>
    </div>
  );
}

function lookupErrorTitle(kind: PrivateClaimReviewLookupResult["kind"]): string {
  switch (kind) {
    case "invalid-address":
      return "Invalid address";
    case "not-found":
      return "Receipt not found";
    case "wrong-owner":
      return "Wrong program owner";
    case "wrong-account-type":
      return "Wrong account type";
    case "decode-error":
      return "Decode failed";
    case "rpc-error":
      return "RPC lookup failed";
    case "found":
      return "Verified";
  }
}

function shortenMiddle(value: string, size: number): string {
  if (!value) return "—";
  if (value === "Not recorded") return value;
  if (value.length <= size * 2 + 3) return value;
  return `${value.slice(0, size)}...${value.slice(-size)}`;
}

function isZeroHash(value: string): boolean {
  return /^0+$/.test(value);
}

function formatUnixSeconds(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "Not recorded";
  return new Date(value * 1000).toISOString().replace("T", " ").replace(".000Z", " UTC");
}

function ProofStep({
  step,
  index,
  isLast,
}: {
  step: (typeof devnetProofSteps)[number] | (typeof mainnetProofSteps)[number];
  index: number;
  isLast: boolean;
}) {
  return (
    <li className="claim-room-flow-item">
      <div className="claim-room-flow-topline">
        <span className="workbench-card-meta">{String(index + 1).padStart(2, "0")}</span>
        {isLast ? (
          <ReceiptText
            className="h-4 w-4 text-[color:var(--accent)]"
            strokeWidth={1.8}
            aria-hidden="true"
          />
        ) : (
          <span className="claim-room-step-rule" aria-hidden="true" />
        )}
      </div>
      <p className="workbench-panel-eyebrow">{step.label}</p>
      <h3 className="claim-room-flow-title">{step.title}</h3>
      <p className="claim-room-flow-copy">
        {step.detail}
      </p>
    </li>
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
        </div>
        <p className="plans-rail-event-detail">{detail}</p>
        <p className="mt-1 break-all font-mono text-[0.66rem] leading-5 text-[color:var(--foreground)]">
          {value}
        </p>
      </div>
    </div>
  );
}
