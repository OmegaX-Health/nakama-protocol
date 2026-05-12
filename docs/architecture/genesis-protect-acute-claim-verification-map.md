# Genesis Protect Acute v1 — Claim Verification Map

> **Version**: 1.0
> **Author**: Manuel Soldatini — Protocol Verification & Claims
> **Status**: Pre-Mainnet Review | May 2026
> **Audience**: Investors · LPs · Sponsors · External Auditors
> **Classification**: Internal — Pre-Mainnet
> **KR**: 1.4 — Onchain/Offchain Boundary Map
> **Program ID**: `Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B`
> **Companion docs**:
> [`genesis-protect-claim-trace.md`](./genesis-protect-claim-trace.md) (step-by-step truth chain narrative),
> [`genesis-protect-acute-claims-processing-spec.md`](./genesis-protect-acute-claims-processing-spec.md) (operational spec — KR 1.2),
> [`genesis-protect-acute-full-protect-flow.md`](./genesis-protect-acute-full-protect-flow.md) (full operational flow — KR 1.1),
> [`magicblock-private-claim-room.md`](./magicblock-private-claim-room.md) (private review adjunct)

---

## Executive Summary

Genesis Protect Acute v1 processes health insurance claims through a cryptographically verifiable truth chain anchored on Solana. This document is the authoritative map of that chain — intended for investors, LPs, sponsors, and independent auditors who want to understand what the protocol guarantees and how to verify those guarantees from public on-chain data.

**Three properties are enforced at the protocol level — without trusting any operator:**

| # | Property | How it is enforced |
|---|----------|--------------------|
| 1 | **Reserve capital cannot leave the vault on an unauthorized claim** | The only outflow path is a PDA-signed SPL transfer gated on `ClaimCase.intake_status = SETTLED (4)` and a valid oracle attestation chain |
| 2 | **Claim evidence is tamper-evident — retrospective forgery is impossible** | Each evidence packet is SHA-256 hashed and anchored on Solana before any oracle attests; once attested, the hash is permanently immutable |
| 3 | **Raw patient data never appears on Solana in any form** | Only 32-byte cryptographic fingerprints of medical documents are written on-chain; the underlying PHI stays encrypted on the off-chain oracle portal |

**What LPs and sponsors can verify independently**, using only public Solana explorer data:
- Every claim opened, every evidence hash committed, every oracle attestation, every adjudication decision, and every payout — each with timestamp and signing authority
- That vault balances decrease only on settled, attested claims
- That oracle attestations reference exactly the evidence packet that was reviewed (hash equality enforced on-chain)
- That protocol fees were correctly carved out at settlement

**Current posture (Phase 0 — Pre-Mainnet):** operator-backed oracle review with all material state transitions anchored on-chain. The roadmap toward fully decentralized adjudication is documented in §10.

---

## Purpose

Two categories of data exist in this protocol:

- **Raw PHI** (Protected Health Information): medical records, invoices, discharge summaries — stored exclusively off-chain, never written to Solana
- **Proof anchors**: SHA-256 cryptographic hashes of that evidence — the only representation of PHI that appears on-chain, sufficient for independent verification without exposing private medical data

This is the authoritative reference for sponsors, LPs, auditors, and protocol reviewers who want to verify the claim truth chain without reading the full Anchor source.

**Legend used throughout this document:**

```
⛓  Solana instruction (on-chain transaction)
🔒 On-chain proof anchor (hash or state written to Solana)
📁 Off-chain only (raw PHI, operator workflow, AI logs)
🔐 TEE only (MagicBlock private review path — hash exits, plaintext never does)
```

---

## 1. Pre-Claim Foundation: Policy Hashes Anchored on Solana

Before any claim opens, the protocol anchors the policy terms, pricing, and evidence requirements on-chain as immutable hash commitments inside the `PolicySeries` account. These are the root of the verification chain — every claim is evaluated against these anchored parameters.

**`PolicySeries` account** — set by protocol governance, locked before the series goes live:

| Field | What it commits to |
|-------|--------------------|
| `terms_hash` | Full coverage terms and exclusion schedule |
| `pricing_hash` | Premium structure and benefit tiers |
| `payout_hash` | Benefit amounts per tier (T1/T2/T3) and reimbursement cap |
| `reserve_model_hash` | Reserve methodology and VaR parameters |
| `evidence_requirements_hash` | Required document types per claim tier |

**`HealthPlan` account** — set by plan admin:

| Field | What it commits to |
|-------|--------------------|
| `schema_binding_hash` | Binding to the verified `OutcomeSchema` for this plan |

> **OutcomeSchema** (`genesis-protect-acute-claim` v1) is separately registered on-chain and must be marked `verified = true` by governance before any oracle can attest against it. Its `schema_key_hash` and `schema_hash` are snapshotted into every `ClaimAttestation`.

All policy material is locked (`material_locked = true`) before the series goes live. No claim can be adjudicated against a different set of terms than what was hashed at policy issuance.

---

## 2. Claim State Machine

The `ClaimCase` account (`intake_status` field) drives the complete claim lifecycle. Each state is set by a specific on-chain instruction; no state can be skipped or forged without a valid signed Solana transaction from the authorized role.

```
                    ┌─────────────────────────────────────────────────────┐
                    │               CLAIM STATE MACHINE                   │
                    │                                                     │
                    │   ⛓ open_claim_case                                │
                    │        │                                            │
                    │        ▼                                            │
                    │   [0] OPEN ─────────────────────────────────┐      │
                    │        │                                     │      │
                    │        │  (operator workflow, off-chain)     │      │
                    │        ▼                                     │      │
                    │   [1] UNDER_REVIEW                           │      │
                    │        │                                     │      │
                    │        │  ⛓ adjudicate_claim_case           │      │
                    │        ├──────────────────────┐             │      │
                    │        ▼                      ▼             │      │
                    │   [2] APPROVED          [3] DENIED ─────────┘      │
                    │        │                                            │
                    │        │  ⛓ settle_claim_case                      │
                    │        │  ⛓ settle_claim_case_selected_asset       │
                    │        ▼                                            │
                    │   [4] SETTLED                                       │
                    │        │                                            │
                    │        ▼                                            │
                    │   [5] CLOSED  (reserved for future use)             │
                    └─────────────────────────────────────────────────────┘
```

> The `DENIED → OPEN` arrow in the diagram represents a **new** `ClaimCase` PDA being opened for an appeal — it is not an in-claim state rollback. The original `ClaimCase` remains permanently at `DENIED (3)`.

| State | `intake_status` | On-chain trigger | Who signs | Money moves? |
|-------|----------------|-----------------|-----------|--------------|
| **OPEN** | `0` | `open_claim_case` | Member **or** claims_operator **or** plan_admin | No |
| **UNDER_REVIEW** | `1` | Operator workflow (off-chain queue pickup) | — | No |
| **APPROVED** | `2` | `adjudicate_claim_case` (`approved_amount > 0`) | claims_operator | No — reserve booked |
| **DENIED** | `3` | `adjudicate_claim_case` (`approved_amount == 0`) | claims_operator | No — obligation void |
| **SETTLED** | `4` | `settle_claim_case` or `settle_claim_case_selected_asset` (`paid_amount ≥ approved_amount`) | claims_operator | **Yes** — USDC leaves vault |
| **CLOSED** | `5` | Reserved for Phase 1 dispute-case state | — | — |

---

## 3. Instruction-to-Verification Map

Every step that produces an on-chain proof is listed below with the exact account it writes to, the hash field it anchors, and the event it emits. Steps that are purely off-chain (📁) are shown for completeness with explicit confirmation that they leave no on-chain footprint at that point.

### Step 1 — `open_claim_case` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | Member wallet **or** `health_plan.claims_operator` **or** `health_plan.plan_admin` |
| PDA created | `ClaimCase` — seeds: `["claim_case", health_plan.key(), claim_id]` |
| State transition | → `CLAIM_INTAKE_OPEN` (0) |
| 🔒 On-chain writes | `claim_case.claimant`, `claim_case.policy_series`, `claim_case.funding_line`, `claim_case.evidence_ref_hash` (initial, may be zeroed), `claim_case.opened_at` |
| Event emitted | `ClaimCaseStateChangedEvent { claim_case, intake_status: 0, approved_amount: 0 }` |
| 📁 Off-chain at this point | Raw incident report, member identity docs — not yet submitted |
| PHI on-chain? | **No** |

> **Security note (PT-04)**: `claimant` is constrained to equal `member_position.wallet` — operators cannot open a claim attributing it to a different member.

---

### Step 2 — `authorize_claim_recipient` ⛓ *(optional)*

| Attribute | Value |
|-----------|-------|
| Authorized signers | Member wallet **only** — operators cannot set this |
| State transition | None — no `intake_status` change |
| 🔒 On-chain writes | `claim_case.delegate_recipient` (wallet address of delegated payout recipient) |
| Event emitted | None |
| PHI on-chain? | **No** |

> The delegate recipient is the sole routing address for settlement. If not set, payout goes to `member_position.wallet`. Operators have no unilateral authority over this field.

---

### Step 3 — Evidence upload and review 📁

| Attribute | Value |
|-----------|-------|
| Where | OmegaX Health oracle portal (off-chain) |
| 📁 What happens | Member uploads: discharge summary, itemized invoice, location proof, doctor note |
| 📁 AI pre-screening | Document completeness check, anomaly flags → operator queue |
| 📁 Human review | Claims operator reviews raw PHI against `evidence_requirements_hash` |
| PHI on-chain? | **No** — raw documents never touch Solana |

---

### Step 4 — `attach_claim_evidence_ref` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | `health_plan.claims_operator` |
| Precondition | `claim_case.attestation_count == 0` (evidence mutable only before first attestation) |
| State transition | None — no `intake_status` change |
| 🔒 On-chain writes | `claim_case.evidence_ref_hash` (SHA-256 of the full evidence packet) |
| | `claim_case.decision_support_hash` (SHA-256 of the operator review bundle) |
| Event emitted | None |
| PHI on-chain? | **No** — only 32-byte hashes |

> **Evidence lock**: once `attest_claim_case` is executed (`attestation_count` increments to ≥ 1), `evidence_ref_hash` becomes permanently immutable. A materially revised evidence packet must open a new `ClaimCase` PDA — there is no silent overwrite path under an existing attestation.

---

### Step 5 — `attest_claim_case` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | `oracle_profile.oracle` (the configured oracle authority for this health plan) |
| Preconditions | `outcome_schema.verified == true`; oracle supports the schema; `args.attestation_ref_hash == claim_case.evidence_ref_hash` (hash match enforced on-chain); oracle finality hold clear; protocol not paused |
| PDA created | `ClaimAttestation` — seeds: `["claim_attestation", claim_case.key(), oracle.key()]` |
| State transition | `claim_case.attestation_count++` |
| 🔒 On-chain writes | Full `ClaimAttestation` account — see hash breakdown below |
| Event emitted | `ClaimCaseAttestedEvent { claim_attestation, claim_case, oracle_profile, oracle, decision, attestation_hash }` |
| PHI on-chain? | **No** — only hash fields |

**`ClaimAttestation` — complete on-chain fields:**

| Field | Size | What it represents |
|-------|------|--------------------|
| `oracle` | Pubkey | Oracle authority public key |
| `oracle_profile` | Pubkey | OracleProfile PDA reference |
| `claim_case` | Pubkey | Parent ClaimCase reference |
| `health_plan` | Pubkey | HealthPlan reference |
| `policy_series` | Pubkey | PolicySeries reference |
| `decision` | u8 | 0=approve / 1=deny / 2=request_review / 3=abstain |
| `attestation_hash` | 32 bytes | Oracle's own hash commitment (off-chain signed artifact) |
| `attestation_ref_hash` | 32 bytes | Must equal `claim_case.evidence_ref_hash` — enforced on-chain |
| `evidence_ref_hash` | 32 bytes | Snapshot of evidence hash at attestation time |
| `decision_support_hash` | 32 bytes | Snapshot of operator review bundle hash |
| `schema_key_hash` | 32 bytes | Hash of the OutcomeSchema key (`genesis-protect-acute-claim`) |
| `schema_hash` | 32 bytes | Hash of the schema content |
| `schema_version` | u16 | Schema version at attestation time |
| `liquidity_pool` | Pubkey | LP pool reference (LP-backed claims only; zero otherwise) |
| `allocation_position` | Pubkey | LP allocation reference (LP-backed claims only; zero otherwise) |
| `created_at_ts` | i64 | Unix timestamp of attestation |

> **Security note (PT-07)**: oracle registration requires `signer == args.oracle` — no third party can register an oracle profile on behalf of another key. The schema must be governance-verified before it can be used.

---

### Step 6 — `adjudicate_claim_case` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | `health_plan.claims_operator` |
| State transition | → `CLAIM_INTAKE_APPROVED` (2) if `approved_amount > 0` **or** → `CLAIM_INTAKE_DENIED` (3) if `approved_amount == 0` |
| 🔒 On-chain writes | `claim_case.intake_status`, `claim_case.adjudicator` (operator pubkey), `claim_case.approved_amount`, `claim_case.denied_amount`, `claim_case.decision_support_hash` (updated at adjudication) |
| Event emitted | `ClaimCaseStateChangedEvent { claim_case, intake_status, approved_amount }` |
| PHI on-chain? | **No** — only amounts and pubkeys |

> Denial path: no `Obligation` PDA is created. The claim lifecycle ends here. The denial reason is anchored via `decision_support_hash` — the full rationale stays off-chain but is hash-committed on-chain.

---

### Step 7 — `reserve_obligation` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | `health_plan.claims_operator` |
| State transition | `Obligation.status` → `OBLIGATION_STATUS_RESERVED` (1) |
| 🔒 On-chain writes | `obligation.reserved_amount`, `funding_line.reserved_amount` ↑, `claim_case.linked_obligation` |
| Event emitted | `ObligationStatusChangedEvent { obligation, funding_line, status: 1, amount }` |
| PHI on-chain? | **No** |

> The encumbered reserve number visible on the public protocol console increases at this step. LP and sponsor reserve impact is visible in real time.

---

### Step 8 — `settle_claim_case` / `settle_claim_case_selected_asset` ⛓

| Attribute | Value |
|-----------|-------|
| Authorized signers | `health_plan.claims_operator` |
| Preconditions | `reserve_asset_rail.payout_enabled == true`; price freshness and confidence within rail bounds; recipient token account owner matches resolved recipient |
| State transition | → `CLAIM_INTAKE_SETTLED` (4) when `paid_amount ≥ approved_amount` |
| 🔒 On-chain writes | `claim_case.paid_amount` ↑, `claim_case.intake_status` → SETTLED, `claim_case.closed_at`, `domain_asset_vault.total_assets` ↓ |
| SPL transfer | `transfer_from_domain_vault` (PDA-signed CPI) — the **only** authorized path for funds to leave the reserve vault |
| Events emitted | `ClaimCaseStateChangedEvent` + `FeeAccruedEvent` (protocol fee) + optionally `FeeAccruedEvent` (oracle revshare if LP-backed) |
| Multi-asset variant | `settle_claim_case_selected_asset` — payout in an approved alternate asset rail (e.g. PUSD, SOL); emits `ClaimCaseSelectedAssetPayoutEvent { claim_asset_mint, payout_asset_mint, claim_credit_amount, payout_amount, settlement_reason_hash }` |
| PHI on-chain? | **No** |

> **Security note (PT-01/02)**: `transfer_from_domain_vault` is the only SPL transfer path out of the custody vault. It requires the vault PDA to sign via seeds — no unsigned outflow is possible.

---

## 4. PHI vs. Proof Anchoring — Complete Separation Table

This table is the canonical reference for what lives where. Nothing in the left column ever appears on Solana in any form. The right column is what external parties can read and verify.

| Category | Data | 📁 Off-chain location | 🔒 On-chain proof anchor |
|----------|------|----------------------|--------------------------|
| **Member identity** | Passport, ID document, KYC data | Oracle portal — private | `member_position.subject_commitment` (identity commitment hash) |
| **Medical evidence** | Discharge summary, doctor notes, clinical records | Oracle portal — private, encrypted | `claim_case.evidence_ref_hash` (SHA-256 of evidence packet) |
| **Billing documents** | Itemized invoice, proof of payment, receipts | Oracle portal — private | `claim_case.evidence_ref_hash` (included in evidence packet hash) |
| **Operator review** | Review checklist, internal recommendation, AI flag log | Claims management system | `claim_case.decision_support_hash` (SHA-256 of review bundle) |
| **Oracle decision** | Full oracle assessment document | Oracle service — private | `claim_attestation.attestation_hash` (oracle's own 32-byte commitment) |
| **Policy terms** | Full coverage terms text (PDF/doc) | OmegaX Health portal | `policy_series.terms_hash` (SHA-256 of terms document) |
| **Evidence requirements** | Required document checklist per tier | OmegaX Health portal | `policy_series.evidence_requirements_hash` |
| **Fraud notes** | Investigation notes, referral details | Secure internal system | Not anchored on-chain in Phase 0 |
| **AI screening logs** | Pre-screening output, anomaly scores | Claims management system | Not anchored on-chain in Phase 0 |
| **TEE evidence packet** | Plaintext PHI inside MagicBlock TEE | TEE enclave — never exits | `private_review_session.review_artifact_hash` (exits TEE as hash only) |

**Summary**: every byte of raw PHI stays off-chain. What Solana records are the **SHA-256 fingerprints** of that data — sufficient for a third party to verify that the reviewed evidence matches what was attested, without accessing the underlying medical content.

---

## 5. Complete On-Chain Hash Chain

The following diagram shows how each hash links to the next, forming a tamper-evident chain from raw PHI to final settlement.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     RAW PHI (off-chain only)                            │
│                                                                         │
│   Medical records + invoices + location proof + doctor note             │
│   (stored encrypted on OmegaX Health oracle portal)                     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ SHA-256  (operator, after human review)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🔒 ClaimCase.evidence_ref_hash          [32 bytes — Solana]            │
│  🔒 ClaimCase.decision_support_hash      [32 bytes — Solana]            │
│                                                                         │
│  Set by: attach_claim_evidence_ref (claims_operator)                    │
│  Immutable after: first attest_claim_case (attestation_count ≥ 1)      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ Oracle verifies: attestation_ref_hash == evidence_ref_hash
                             │ (enforced on-chain — transaction reverts if mismatch)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🔒 ClaimAttestation PDA                 [Solana — permanent]           │
│                                                                         │
│  attestation_hash        [32 bytes] — oracle's signed commitment        │
│  attestation_ref_hash    [32 bytes] — snapshot of evidence_ref_hash     │
│  evidence_ref_hash       [32 bytes] — snapshot at attestation time      │
│  decision_support_hash   [32 bytes] — snapshot of review bundle hash    │
│  schema_key_hash         [32 bytes] — verified OutcomeSchema key        │
│  schema_hash             [32 bytes] — verified OutcomeSchema content    │
│  decision                [u8]       — approve / deny / review / abstain │
│  oracle                  [Pubkey]   — signing oracle public key         │
│                                                                         │
│  Set by: attest_claim_case (oracle_authority)                           │
│  Schema must be: outcome_schema.verified == true (governance gate)      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ adjudicate_claim_case (claims_operator)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🔒 ClaimCase — adjudication record      [Solana — permanent]           │
│                                                                         │
│  intake_status           APPROVED (2) or DENIED (3)                     │
│  adjudicator             [Pubkey]   — signing claims_operator key       │
│  approved_amount         [u64]      — USDC amount approved              │
│  denied_amount           [u64]      — USDC amount denied                │
│  decision_support_hash   [32 bytes] — updated at adjudication           │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ reserve_obligation → settle_claim_case
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🔒 Settlement — SPL token transfer      [Solana — permanent]           │
│                                                                         │
│  intake_status           SETTLED (4)                                    │
│  paid_amount             [u64]      — actual USDC disbursed             │
│  closed_at               [i64]      — Unix timestamp of settlement      │
│  recipient               member_position.wallet or delegate_recipient   │
│  tx signature            immutable Solana transaction record            │
│  vault delta             domain_asset_vault.total_assets ↓              │
└─────────────────────────────────────────────────────────────────────────┘
```

**Verification property**: a third party who knows the original evidence packet can SHA-256 hash it and compare against `claim_case.evidence_ref_hash`. If they match, the evidence anchored on Solana is the same evidence that was reviewed — and the oracle's attestation applies to exactly that packet.

---

## 6. MagicBlock Private Review Path

For claims requiring TEE-private handling (Phase 0 demo, high-sensitivity cases), an adjunct program `omegax_private_claim_review` runs on MagicBlock Ephemeral Rollups. This path integrates with the standard claim lifecycle at steps 4–5, replacing the standard operator attachment + oracle attestation with a TEE-bounded variant.

```
Standard path:                          MagicBlock private path:
                                        
📁 Evidence upload (off-chain)          📁 Evidence upload (off-chain)
         │                                       │
         │                              🔐 TEE receives private packet
         ▼                                       │
⛓ attach_claim_evidence_ref            ⛓ open_review_session
         │                                       │
         ▼                              ⛓ delegate_review_session
⛓ attest_claim_case                    (→ MagicBlock ER)
                                                │
                                       🔐 Private review inside TEE
                                        (plaintext never leaves enclave)
                                                │
                                       ⛓ record_private_review
                                        (review_artifact_hash only)
                                                │
                                       ⛓ record_private_payment_ref
                                        (payment_reference_hash only)
                                                │
                                       ⛓ commit_and_close_review_session
                                        (→ back to Solana base)
                                                │
                                                ▼
                                       ⛓ attest_claim_case (main program)
                                        consumes committed artifact hash
```

**PHI boundary in the MagicBlock path:**

| What | Where |
|------|-------|
| Private evidence packet (plaintext) | 🔐 TEE enclave only — never on Solana, never on MagicBlock ER |
| `review_artifact_hash` | 🔒 MagicBlock ER → committed to Solana base |
| `private_payment_reference_hash` | 🔒 MagicBlock ER → committed to Solana base |
| Oracle attestation hash | 🔒 Standard `ClaimAttestation` PDA on Solana base |

The main `omegax_protocol` program, its vaults, funding lines, obligations, and payout accounts are **never delegated to MagicBlock** — the reserve kernel remains exclusively on Solana base.

---

## 7. Unhappy Paths — Verification Map

| Scenario | On-chain state | Off-chain state | What's verifiable |
|----------|---------------|-----------------|-------------------|
| **Incomplete evidence** | `ClaimCase.intake_status = OPEN` (0) — no `evidence_ref_hash` set yet | Operator review queue pending | Chain shows claim opened but no evidence attached |
| **Evidence resubmission** (pre-attestation) | New `attach_claim_evidence_ref` call updates `evidence_ref_hash` | New evidence packet uploaded | Each update is a distinct Solana transaction; full update history recoverable from transaction logs |
| **Evidence revision** (post-attestation) | New `ClaimCase` PDA opened | Original attested claim visible alongside new claim case | Both cases publicly visible; correlation via off-chain claim manifest |
| **Partial approval** (Travel 30 top-up) | `approved_amount` = fixed tier cap; top-up requires separate adjudication round | UCR itemization review off-chain | `ClaimCaseStateChangedEvent` shows tier approval; second adjudication for top-up produces separate event |
| **Denial** | `intake_status = DENIED` (3); `decision_support_hash` updated | Full denial rationale off-chain | Hash-committed reason; no obligation created; no funds reserved |
| **Settlement deferred** | `obligation.status = CLAIMABLE_PAYABLE` (2) | Waiting on multisig settlement signer | Encumbered reserve visible; vault balance unchanged |
| **Impairment** | `mark_impairment` → `obligation.status = IMPAIRED` (5) | LP loss absorbed by junior class | `ImpairmentRecordedEvent { funding_line, obligation, amount, reason_hash }` visible on-chain |
| **Appeal (Phase 0)** | New `ClaimCase` PDA opened with appeal evidence | Correlated to original via off-chain claim manifest | New claim case on-chain; original denial chain intact and immutable |

---

## 8. Obligation State Lifecycle (parallel to ClaimCase)

```
⛓ adjudicate_claim_case (approved)
        │
        ▼
[0] PROPOSED ──► [1] RESERVED ──────────────────────────────► [3] SETTLED
                 (reserve_obligation)    ⛓ settle_claim_case   (settle_claim_case)
                       │
                       ├──────────────────────────────────────► [4] CANCELED
                       │                                         (denial / void path;
                       │                                          no funds reserved)
                       │
                       ▼
                 [2] CLAIMABLE_PAYABLE
                       │
                       ├──────────────────────────────────────► [5] IMPAIRED
                       │                                         (mark_impairment;
                       │                                          LP junior class absorbs loss)
                       │
                       └──────────────────────────────────────► [6] RECOVERED
                                                                 (post-impairment recovery)
```

Every `Obligation` state transition emits `ObligationStatusChangedEvent { obligation, funding_line, status, amount }`.

---

## 9. Auditor Verification Checklist

For any Genesis Protect Acute claim, an independent auditor can verify the following from public on-chain data alone. No access to raw PHI is required.

| Question | Where to look on-chain |
|----------|----------------------|
| Who opened the claim and when? | `claim_case.claimant`, `claim_case.opened_at`, opening tx signature |
| Was the claimant an active policy member? | `member_position.active == true`, `member_position.eligibility_status == ELIGIBLE` at claim time |
| What evidence hash was committed? | `claim_case.evidence_ref_hash` |
| Was the evidence locked before attestation? | `claim_case.attestation_count ≥ 1` → hash is immutable |
| Who attested and with what decision? | `ClaimAttestation.oracle`, `.decision`, `.attestation_hash` |
| Was the schema governance-verified? | `outcome_schema.verified == true` at attestation time |
| Does the attestation match the evidence? | `claim_attestation.attestation_ref_hash == claim_case.evidence_ref_hash` (enforced on-chain) |
| Who adjudicated and what was the outcome? | `claim_case.adjudicator`, `claim_case.intake_status`, `claim_case.approved_amount` |
| What funding line was reserved? | `claim_case.funding_line`, `obligation.reserved_amount` |
| Was the payout made and to whom? | `claim_case.paid_amount`, `claim_case.closed_at`, settlement tx; recipient = `delegate_recipient` if set, else `member_position.wallet` |
| Were fees correctly carved out? | `FeeAccruedEvent` on settlement tx; `protocol_fee_vault.accrued_fees` |
| Was the policy material unchanged at claim time? | `policy_series.material_locked == true`, `terms_hash` unchanged since issuance |

---

## 10. Phased Decentralization Roadmap

The protocol launches in a deliberately phased approach: Phase 0 achieves on-chain anchoring of all material claim state (evidence hashes, attestations, adjudication, settlement) while retaining operator-supervised workflows for review queuing and oracle key management. The table below is an honest accounting of what each phase adds.

| Item | Phase 0 posture | Phase 1 target |
|------|----------------|----------------|
| **`UNDER_REVIEW` state** | Off-chain queue pickup — not a distinct on-chain `intake_status` transition | Explicit on-chain `set_claim_under_review` instruction |
| **Appeal linkage** | New `ClaimCase` PDA opened for appeals; correlated off-chain | On-chain dispute-case linkage between original denial and appeal PDA |
| **Fraud referral record** | Internal notes; hash not yet committed on-chain | `fraud_referral_hash` field or dedicated instruction in `protocol-oracle-service` |
| **Oracle key custody** | Claims operator hot wallet signs oracle transactions | HSM / KMS boundary enforced before mainnet (see claims-processing-spec §13) |
| **Provider direct settlement** | Payout goes to member wallet or delegated recipient | Provider KYB + `delegate_recipient` = verified provider wallet |

> **Phase 0 communication standard**: any external claim communication — to members, partners, or press — must describe the current posture as **operator-backed oracle review**, not fully decentralized adjudication. The on-chain record is authoritative; the governance of who writes to it is progressively decentralizing.

---

## 11. LP Capital Protection — Summary

For LPs deploying capital into the OmegaX Protocol liquidity pools, the claim architecture provides the following hard guarantees:

| Concern | Protocol guarantee |
|---------|--------------------|
| **Can an operator drain the vault without a real claim?** | No — funds leave only via `transfer_from_domain_vault` PDA-signed CPI, requiring a `ClaimCase` with `intake_status = SETTLED (4)` and a valid attested oracle decision |
| **Can a fraudulent claim override a valid attestation?** | No — `adjudicate_claim_case` is gated on the oracle attestation chain; the adjudicator pubkey is permanently recorded |
| **Can evidence be altered after oracle review?** | No — `evidence_ref_hash` is immutable once `attestation_count ≥ 1`; any change requires a new `ClaimCase` PDA |
| **Can LP losses be hidden?** | No — `ImpairmentRecordedEvent { funding_line, obligation, amount, reason_hash }` is emitted on-chain; `ObligationStatusChangedEvent` at each obligation state transition |
| **Can payout routing be changed by the operator?** | Partially — operator cannot override a member-set `delegate_recipient`; `authorize_claim_recipient` is member-only |
| **Is the oracle's schema governance-controlled?** | Yes — `outcome_schema.verified == true` is enforced on-chain at attestation time; schema changes require governance authority |

---

## 12. References

| Document | Path |
|----------|------|
| Step-by-step claim truth chain narrative | [`genesis-protect-claim-trace.md`](./genesis-protect-claim-trace.md) |
| Claims processing specification (KR 1.2) | [`genesis-protect-acute-claims-processing-spec.md`](./genesis-protect-acute-claims-processing-spec.md) |
| Full operational protect flow (KR 1.1) | [`genesis-protect-acute-full-protect-flow.md`](./genesis-protect-acute-full-protect-flow.md) |
| MagicBlock private claim room | [`magicblock-private-claim-room.md`](./magicblock-private-claim-room.md) |
| Evidence schema (JSON) | [`../../frontend/public/schemas/genesis-protect-acute-claim-v1.json`](../../frontend/public/schemas/genesis-protect-acute-claim-v1.json) |
| Phase 0 mainnet surface gating | [`../operations/phase0-mainnet-surface-gating.md`](../operations/phase0-mainnet-surface-gating.md) |
| Anchor source — claim instructions | [`../../programs/omegax_protocol/src/claims.rs`](../../programs/omegax_protocol/src/claims.rs) |
| Anchor source — account states | [`../../programs/omegax_protocol/src/state.rs`](../../programs/omegax_protocol/src/state.rs) |
| Anchor source — protocol events | [`../../programs/omegax_protocol/src/events.rs`](../../programs/omegax_protocol/src/events.rs) |
| Anchor source — constants and seeds | [`../../programs/omegax_protocol/src/constants.rs`](../../programs/omegax_protocol/src/constants.rs) |
