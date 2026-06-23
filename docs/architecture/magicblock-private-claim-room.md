# MagicBlock Private Claim Room

Nakama Private Claim Room is a hackathon adjunct for private Genesis Protect Acute claim review. It uses MagicBlock Ephemeral Rollups for delegated review-session state while the main `nakama_coverage_protocol` program remains the Solana claim, reserve, and settlement kernel.

The adjunct program is `nakama_private_claim_review`. It stores only public-safe hashes and session state:

- registry/session authority
- registered review operator
- linked claim case
- health plan and policy series
- evidence and schema hashes
- review result and artifact hashes
- review binary and TEE attestation digests
- reviewer/operator key
- private payment reference hash
- lifecycle status and timestamps

Raw medical evidence, encrypted evidence payloads, OCR text, storage paths, and private payment details never belong in this program.

## Demo Flow

1. `omegax-health` prepares a redacted Genesis Protect Acute claim packet and hashes the private evidence bundle.
2. The private-review program upgrade authority initializes `PrivateReviewRegistry` and registers an active `PrivateReviewOperator` with the expected review binary hash.
3. `nakama_private_claim_review::open_review_session` creates a public review-session PDA on base Solana. The PDA is seeded by session authority, claim case, and session id to prevent third-party squatting.
4. `delegate_review_session` verifies the session authority, marks the session delegated, and delegates that session PDA to MagicBlock ER.
5. A TEE/private reviewer checks the private packet and emits a hash-bounded review artifact.
6. `record_private_review` records only review hashes and status on the delegated session. Only the active registered reviewer can write the result, and the submitted review binary hash must match the operator registry entry.
7. The MagicBlock Private Payments API builds a devnet reimbursement preview; `record_private_payment_ref` stores only its reference hash and is limited to the configured payment attestor.
8. `commit_and_close_review_session` schedules the MagicBlock commit and undelegates the review session back to Solana. Approved sessions require a private payment reference before commit. This instruction deliberately leaves account data unchanged and only invokes the MagicBlock commit CPI.
9. After the session PDA is owned by `nakama_private_claim_review` on base Solana again, `finalize_committed_review_session` stamps `committed_at` on the base-layer receipt.
10. Off-chain consumers or operator tooling refetch and verify the committed adjunct account, then use the review artifact as support for the base program's `adjudicate_claim_case` / reserve / settlement path.

## Boundaries

- The main `nakama_coverage_protocol` program is not delegated to MagicBlock.
- `ClaimCase`, reserves, vaults, funding lines, obligations, and payout accounts are not delegated.
- The private reviewer may inspect plaintext inside the TEE path, but public Solana only receives hashes and status.
- The hackathon reimbursement preview demonstrates MagicBlock private payments; it does not replace the production reserve kernel.
- The adjunct is not authoritative by itself. Consumers must verify registry binding, reviewer binding, expected hashes, payment reference, and committed ownership before treating it as claim-decision input.
- The registry is a singleton PDA, so first initialization is deliberately restricted to the private-review program upgrade authority via the program `ProgramData` account. This prevents public first-writer takeover of the canonical review registry.

## Devnet Smoke Runner

Use `npm run devnet:magicblock:claim-review -- --fixtures <hash-only-fixtures.json> --count 5` to exercise the full devnet path: base Solana registry/open/delegate, authenticated MagicBlock TEE review/payment/commit, and base Solana finalization. The fixture file must contain public-safe hashes and public keys only. `protocol-oracle-service` can generate that shape from the Genesis Protect claim simulation lab with `npm run claims:magicblock-fixtures`.

The runner intentionally uses the public devnet RPC, `https://devnet-tee.magicblock.app`, and a local signer supplied through `ANCHOR_WALLET`, `SOLANA_KEYPAIR`, or `--keypair`. It does not write raw medical evidence, local key paths, or TEE auth tokens to tracked files.
