// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import { useEffect, useMemo, useState } from "react";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
import { PublicKey, type Transaction } from "@solana/web3.js";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";

import { useProtocolTransactionReviewPrompt } from "@/components/protocol-transaction-review";
import { WizardDetailSheet, type WizardDetailMetaItem } from "@/components/wizard-detail-sheet";
import { executeProtocolTransactionWithToast } from "@/lib/protocol-action-toast";
import {
  buildDepositIntoCapitalClassTx,
  buildRequestRedemptionTx,
  CAPITAL_CLASS_RESTRICTION_OPEN,
  type CapitalClassSnapshot,
  type DomainAssetVaultSnapshot,
  type LiquidityPoolSnapshot,
  type LPPositionSnapshot,
} from "@/lib/protocol";
import { formatAmount } from "@/lib/canonical-ui";

type Status = {
  tone: "ok" | "error";
  message: string;
} | null;

type LpSelfServiceAction = "deposit" | "redemption";

type CapitalLpSelfServicePanelProps = {
  selectedPool: LiquidityPoolSnapshot | null;
  selectedClass: CapitalClassSnapshot | null;
  domainAssetVaults: DomainAssetVaultSnapshot[];
  lpPositions: LPPositionSnapshot[];
  onRefresh?: () => Promise<void> | void;
};

function parseBigIntInput(value: string): bigint {
  const normalized = value.trim().replace(/[_ ,]/g, "");
  if (!normalized) return 0n;
  try {
    return BigInt(normalized);
  } catch {
    return 0n;
  }
}

function deriveOwnerAta(owner: PublicKey | null, mint: string | null): string {
  if (!owner || !mint) return "";
  try {
    return getAssociatedTokenAddressSync(new PublicKey(mint), owner, false).toBase58();
  } catch {
    return "";
  }
}

function shortenAddress(value: string | null | undefined): string {
  if (!value) return "None";
  if (value.length <= 14) return value;
  return `${value.slice(0, 6)}...${value.slice(-6)}`;
}

function ReviewRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="plans-wizard-review-row">
      <span className="plans-wizard-review-label">{label}</span>
      <span className="plans-wizard-review-value">{value}</span>
    </div>
  );
}

export function CapitalLpSelfServicePanel(props: CapitalLpSelfServicePanelProps) {
  const { connection } = useConnection();
  const { publicKey, sendTransaction } = useWallet();
  const { confirmReview, reviewPrompt } = useProtocolTransactionReviewPrompt();
  const [depositAmount, setDepositAmount] = useState("");
  const [minimumShares, setMinimumShares] = useState("0");
  const [sourceTokenAccount, setSourceTokenAccount] = useState("");
  const [redemptionShares, setRedemptionShares] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>(null);
  const [activeAction, setActiveAction] = useState<LpSelfServiceAction | null>(null);
  const [advancedOpen, setAdvancedOpen] = useState(false);

  const selectedVault = useMemo(
    () =>
      props.domainAssetVaults.find(
        (vault) =>
          vault.reserveDomain === props.selectedPool?.reserveDomain &&
          vault.assetMint === props.selectedPool?.depositAssetMint,
      ) ?? null,
    [props.domainAssetVaults, props.selectedPool?.depositAssetMint, props.selectedPool?.reserveDomain],
  );
  const ownerPosition = useMemo(
    () =>
      props.lpPositions.find(
        (position) =>
          position.capitalClass === props.selectedClass?.address &&
          position.owner === publicKey?.toBase58(),
      ) ?? null,
    [props.lpPositions, props.selectedClass?.address, publicKey],
  );

  useEffect(() => {
    const derived = deriveOwnerAta(publicKey ?? null, props.selectedPool?.depositAssetMint ?? null);
    if (derived) setSourceTokenAccount(derived);
  }, [props.selectedPool?.depositAssetMint, publicKey]);

  useEffect(() => {
    setActiveAction(null);
    setAdvancedOpen(false);
  }, [props.selectedClass?.address, props.selectedPool?.address]);

  async function run(label: string, factory: () => Promise<Transaction>) {
    if (!publicKey || !sendTransaction) return;
    setBusy(label);
    setStatus(null);
    try {
      const tx = await factory();
      const result = await executeProtocolTransactionWithToast({
        connection,
        sendTransaction,
        tx,
        label,
        confirmReview,
        review: {
          authority: publicKey.toBase58(),
          feePayer: publicKey.toBase58(),
          affectedObject: props.selectedClass
            ? `${props.selectedClass.displayName} (${props.selectedClass.address})`
            : "LP self-service",
          economicEffect:
            label === "Deposit LP capital"
              ? "Deposits SPL assets into the selected capital class and mints LP shares under the pool accounting rules."
              : "Queues LP shares for operator-processed redemption; it does not withdraw assets immediately.",
          warnings: [
            "Phase 0 LP exits are queue-only; redemption processing remains operator-reviewed.",
            "Use the token account for the pool deposit mint only.",
          ],
        },
        onConfirmed: async () => {
          await props.onRefresh?.();
        },
        onRetry: () => {
          void run(label, factory);
        },
      });
      setStatus({
        tone: result.ok ? "ok" : "error",
        message: result.ok ? result.message : result.error,
      });
    } catch (cause) {
      setStatus({
        tone: "error",
        message: cause instanceof Error ? cause.message : `${label} failed.`,
      });
    } finally {
      setBusy(null);
    }
  }

  const canSubmit =
    Boolean(publicKey)
    && Boolean(props.selectedPool)
    && Boolean(props.selectedClass)
    && props.selectedClass?.restrictionMode === CAPITAL_CLASS_RESTRICTION_OPEN
    && Boolean(selectedVault?.vaultTokenAccount);
  const actionPrerequisite = !publicKey
    ? "Connect a wallet to enable LP deposits and redemption requests."
    : !props.selectedPool
      ? "Choose a pool before LP actions are available."
      : !props.selectedClass
        ? "Choose a capital class before LP actions are available."
        : props.selectedClass.restrictionMode !== CAPITAL_CLASS_RESTRICTION_OPEN
          ? "This capital class is restricted, so public LP self-service is unavailable for it."
          : !selectedVault?.vaultTokenAccount
            ? "The selected pool is missing a visible vault token account."
            : null;
  const depositDisabled = !canSubmit || !sourceTokenAccount.trim() || !depositAmount.trim() || busy === "Deposit LP capital";
  const redemptionDisabled = !canSubmit || !redemptionShares.trim() || busy === "Request LP redemption";
  const actionMeta = useMemo<WizardDetailMetaItem[]>(() => {
    const meta: WizardDetailMetaItem[] = [];
    if (props.selectedPool) meta.push({ label: props.selectedPool.displayName, tone: "muted" });
    if (props.selectedClass) meta.push({ label: props.selectedClass.displayName, tone: "accent" });
    if (activeAction === "redemption") meta.push({ label: "Queue-only exit", tone: "muted" });
    return meta;
  }, [activeAction, props.selectedClass, props.selectedPool]);
  const activeActionTitle = activeAction === "deposit" ? "Deposit LP capital" : "Queue LP redemption";
  const activeActionSummary = activeAction === "deposit"
    ? "Configure the amount, review the selected class and token route, then sign the deposit transaction."
    : "Choose the LP shares to queue, review the class exit rules, then sign the redemption request.";

  const closeActionSheet = () => {
    setActiveAction(null);
    setAdvancedOpen(false);
  };

  return (
    <article className="plans-card heavy-glass">
      {reviewPrompt}
      <div className="plans-card-head">
        <div>
          <p className="plans-card-eyebrow">LP self-service</p>
          <h2 className="plans-card-title plans-card-title-display">
            Capital class <em>actions</em>
          </h2>
        </div>
        <span className="plans-card-meta">Queue-only exit</span>
      </div>

      <div className="plans-notice liquid-glass" role="status">
        <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">info</span>
        <p>
          {props.selectedClass?.restrictionMode === CAPITAL_CLASS_RESTRICTION_OPEN
            ? "Public LP deposits and redemption requests are available for this open class. Redemption processing stays operator-reviewed and pays the LP owner route enforced on-chain."
            : "This selected class is visible for audit, but public LP deposits and redemption requests are not available from this class."}
        </p>
      </div>

      {status ? (
        <div className="plans-notice liquid-glass" role="status">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">
            {status.tone === "ok" ? "verified" : "error"}
          </span>
          <p>{status.message}</p>
        </div>
      ) : null}

      {actionPrerequisite ? (
        <div className="plans-notice liquid-glass" role="status" id="capital-lp-action-help">
          <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">lock</span>
          <p>{actionPrerequisite}</p>
        </div>
      ) : null}

      <div className="plans-settings-grid">
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Selected class</span>
            <span className="plans-settings-lane">
              {props.selectedClass ? "Selected from the capital context bar" : "Choose the pool and class in the context bar above"}
            </span>
          </div>
          <span className="plans-settings-address">{props.selectedClass?.displayName ?? "None"}</span>
        </div>
        <div className="plans-settings-row">
          <div>
            <span className="plans-settings-label">Your LP shares</span>
            <span className="plans-settings-lane">Connected wallet position in this class</span>
          </div>
          <span className="plans-settings-address">{formatAmount(ownerPosition?.shares ?? 0n)}</span>
        </div>
      </div>

      <div className="capital-lp-action-grid" aria-label="LP transaction actions">
        <button
          type="button"
          className="capital-lp-action-card"
          disabled={!canSubmit}
          aria-describedby={actionPrerequisite ? "capital-lp-action-help" : undefined}
          aria-haspopup="dialog"
          onClick={() => setActiveAction("deposit")}
        >
          <span className="material-symbols-outlined capital-lp-action-icon" aria-hidden="true">account_balance_wallet</span>
          <span className="capital-lp-action-copy">
            <span className="capital-lp-action-title">Deposit LP capital</span>
            <span className="capital-lp-action-summary">Amount, minimum shares, review, sign.</span>
          </span>
          <span className="capital-lp-action-open">{canSubmit ? "Open" : "Locked"}</span>
        </button>
        <button
          type="button"
          className="capital-lp-action-card"
          disabled={!canSubmit}
          aria-describedby={actionPrerequisite ? "capital-lp-action-help" : undefined}
          aria-haspopup="dialog"
          onClick={() => setActiveAction("redemption")}
        >
          <span className="material-symbols-outlined capital-lp-action-icon" aria-hidden="true">low_priority</span>
          <span className="capital-lp-action-copy">
            <span className="capital-lp-action-title">Queue redemption</span>
            <span className="capital-lp-action-summary">Shares enter operator-reviewed exit queue.</span>
          </span>
          <span className="capital-lp-action-open">{canSubmit ? "Open" : "Locked"}</span>
        </button>
      </div>

      <WizardDetailSheet
        open={activeAction !== null}
        onOpenChange={(open) => {
          if (!open) closeActionSheet();
        }}
        title={activeActionTitle}
        summary={activeActionSummary}
        meta={actionMeta}
      >
        <div className="operator-drawer">
          <div className="capital-lp-step-list" aria-label="Transaction steps">
            <span className="capital-lp-step capital-lp-step-active">Configure</span>
            <span className="capital-lp-step capital-lp-step-active">Review</span>
            <span className="capital-lp-step">Sign</span>
          </div>

          {status ? (
            <div className="plans-notice liquid-glass" role="status">
              <span className="material-symbols-outlined plans-notice-icon" aria-hidden="true">
                {status.tone === "ok" ? "verified" : "error"}
              </span>
              <p>{status.message}</p>
            </div>
          ) : null}

          {activeAction === "deposit" ? (
            <fieldset className="operator-drawer-fieldset">
              <legend className="operator-drawer-legend">Deposit details</legend>
              <div className="plans-wizard-row">
                <label className="plans-wizard-field-group">
                  <span className="plans-wizard-field-label">Deposit amount</span>
                  <span className="plans-wizard-field-bar">
                    <input
                      type="text"
                      inputMode="numeric"
                      className="plans-wizard-input"
                      value={depositAmount}
                      onChange={(event) => setDepositAmount(event.target.value)}
                      placeholder="0"
                    />
                  </span>
                  <span className="field-help">Pool deposit asset amount in raw protocol units.</span>
                </label>
                <label className="plans-wizard-field-group">
                  <span className="plans-wizard-field-label">Minimum LP shares</span>
                  <span className="plans-wizard-field-bar">
                    <input
                      type="text"
                      inputMode="numeric"
                      className="plans-wizard-input"
                      value={minimumShares}
                      onChange={(event) => setMinimumShares(event.target.value)}
                      placeholder="0"
                    />
                  </span>
                  <span className="field-help">Slippage floor before signing.</span>
                </label>
              </div>
              <button
                type="button"
                className="operator-drawer-advanced-toggle"
                onClick={() => setAdvancedOpen((open) => !open)}
                aria-expanded={advancedOpen}
              >
                {advancedOpen ? "Hide advanced route" : "Advanced token route"}
              </button>
              {advancedOpen ? (
                <label className="plans-wizard-field-group">
                  <span className="plans-wizard-field-label">Funding token account</span>
                  <span className="plans-wizard-field-bar">
                    <input
                      type="text"
                      className="plans-wizard-input"
                      value={sourceTokenAccount}
                      onChange={(event) => setSourceTokenAccount(event.target.value)}
                      placeholder="Auto-filled from the connected wallet when available"
                    />
                  </span>
                  <span className="field-help">Usually the associated token account for the pool deposit asset.</span>
                </label>
              ) : null}
            </fieldset>
          ) : null}

          {activeAction === "redemption" ? (
            <fieldset className="operator-drawer-fieldset">
              <legend className="operator-drawer-legend">Redemption request</legend>
              <label className="plans-wizard-field-group">
                <span className="plans-wizard-field-label">Shares to queue</span>
                <span className="plans-wizard-field-bar">
                  <input
                    type="text"
                    inputMode="numeric"
                    className="plans-wizard-input"
                    value={redemptionShares}
                    onChange={(event) => setRedemptionShares(event.target.value)}
                    placeholder="0"
                  />
                </span>
                <span className="field-help">Queued shares remain operator-reviewed; this does not withdraw assets immediately.</span>
              </label>
            </fieldset>
          ) : null}

          <div className="plans-wizard-review-section">
            <div className="plans-wizard-review-section-head">
              <h3>Transaction review</h3>
              <p>Confirm the selected pool, class, and route before the wallet prompt opens.</p>
            </div>
            <div className="plans-wizard-review-section-rows">
              <ReviewRow label="Pool" value={props.selectedPool?.displayName ?? "None"} />
              <ReviewRow label="Class" value={props.selectedClass?.displayName ?? "None"} />
              <ReviewRow label="Deposit mint" value={shortenAddress(props.selectedPool?.depositAssetMint)} />
              {activeAction === "deposit" ? (
                <>
                  <ReviewRow label="Amount" value={depositAmount.trim() || "0"} />
                  <ReviewRow label="Min shares" value={minimumShares.trim() || "0"} />
                  <ReviewRow label="Funding account" value={shortenAddress(sourceTokenAccount)} />
                  <ReviewRow label="Vault" value={shortenAddress(selectedVault?.vaultTokenAccount)} />
                </>
              ) : (
                <>
                  <ReviewRow label="Shares" value={redemptionShares.trim() || "0"} />
                  <ReviewRow label="Current position" value={formatAmount(ownerPosition?.shares ?? 0n)} />
                  <ReviewRow label="Exit mode" value="Queue-only, operator-reviewed" />
                </>
              )}
            </div>
          </div>

          <div className="plans-wizard-footer">
            <button type="button" className="plans-wizard-back" onClick={closeActionSheet}>
              <span className="material-symbols-outlined" aria-hidden="true">close</span>
              Cancel
            </button>
            {activeAction === "deposit" ? (
              <button
                type="button"
                className="plans-wizard-next"
                disabled={depositDisabled}
                aria-describedby={actionPrerequisite ? "capital-lp-action-help" : undefined}
                onClick={() =>
                  run("Deposit LP capital", async () => {
                    const { blockhash } = await connection.getLatestBlockhash("confirmed");
                    return buildDepositIntoCapitalClassTx({
                      owner: publicKey!,
                      reserveDomainAddress: props.selectedPool!.reserveDomain,
                      poolAddress: props.selectedPool!.address,
                      poolDepositAssetMint: props.selectedPool!.depositAssetMint,
                      capitalClassAddress: props.selectedClass!.address,
                      sourceTokenAccountAddress: sourceTokenAccount.trim(),
                      vaultTokenAccountAddress: selectedVault!.vaultTokenAccount,
                      recentBlockhash: blockhash,
                      amount: parseBigIntInput(depositAmount),
                      shares: parseBigIntInput(minimumShares),
                    });
                  })
                }
              >
                <span className="plans-wizard-next-label">
                  {busy === "Deposit LP capital" ? "Submitting" : "Review deposit"}
                </span>
                <span className="material-symbols-outlined" aria-hidden="true">arrow_forward</span>
              </button>
            ) : (
              <button
                type="button"
                className="plans-wizard-next"
                disabled={redemptionDisabled}
                aria-describedby={actionPrerequisite ? "capital-lp-action-help" : undefined}
                onClick={() =>
                  run("Request LP redemption", async () => {
                    const { blockhash } = await connection.getLatestBlockhash("confirmed");
                    return buildRequestRedemptionTx({
                      owner: publicKey!,
                      reserveDomainAddress: props.selectedPool!.reserveDomain,
                      poolAddress: props.selectedPool!.address,
                      poolDepositAssetMint: props.selectedPool!.depositAssetMint,
                      capitalClassAddress: props.selectedClass!.address,
                      recentBlockhash: blockhash,
                      shares: parseBigIntInput(redemptionShares),
                    });
                  })
                }
              >
                <span className="plans-wizard-next-label">
                  {busy === "Request LP redemption" ? "Submitting" : "Review request"}
                </span>
                <span className="material-symbols-outlined" aria-hidden="true">arrow_forward</span>
              </button>
            )}
          </div>
        </div>
      </WizardDetailSheet>
    </article>
  );
}
