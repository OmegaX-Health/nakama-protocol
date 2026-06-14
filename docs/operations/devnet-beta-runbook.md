# Devnet Beta Runbook

This runbook covers shared-devnet rollout for the current canonical OmegaX protocol surface, including the mounted console, frontend parity, operator drawer simulation, and observability sign-off.

## Go / No-Go Gate

All of the following should be green before a public devnet beta event:

- `npm run anchor:idl`
- `npm run protocol:contract`
- `npm run verify:public`
- `npm run test:e2e:localnet`
- `npm run beta:consistency:check`
- `npm run protocol:contract:check`
- `npm run frontend:build`
- `npm run devnet:beta:deploy`
- `npm run protocol:bootstrap:devnet-live`
- `npm run devnet:frontend:bootstrap`
- `npm run devnet:frontend:signoff`
- `npm run devnet:operator:drawer:sim`
- `npm run devnet:beta:observe` with no unexplained high-severity failures

If the launch window requires a rehearsal deployment, run the same sequence against the rehearsal program id before upgrading the canonical shared devnet.

## Launch Sequence

1. Re-lock the checked artifacts with `npm run anchor:idl` and `npm run protocol:contract`, then rerun `npm run verify:public` and `npm run test:e2e:localnet`.
2. Run `npm run devnet:beta:deploy` to rebuild the checked deploy artifact and refresh the canonical bootstrap bundle under `devnet/` and `frontend/`.
3. Upgrade the canonical shared-devnet program id explicitly with the checked `target/deploy/omegax_protocol.so`.
   Use the canonical program id from `Anchor.toml` / `frontend/lib/protocol.ts`, not the raw `target/deploy/omegax_protocol-keypair.json` address if those ever drift.
   The helper now prints the exact canonical command:
   `solana program deploy --program-id 6EXiDfGVbG7V1X2xaEALDZ7CtSuezkM8ZvXXFpk5WxQM --upgrade-authority ~/.config/solana/id.json target/deploy/omegax_protocol.so`
4. Run `npm run protocol:bootstrap:devnet-live` to seed or refresh the canonical reserve-domain, asset-vault, plan, policy-series, funding-line, and proof-claim graph on shared devnet. This bootstrap does not create retired governance, member-seat, oracle-registry, liquidity-pool, capital-class, or allocation accounts, and it does not move SPL custody balances.
5. Run `npm run devnet:frontend:bootstrap` and `npm run devnet:frontend:signoff` so the mounted console is validated against the refreshed shared-devnet fixture/env set.
6. Run `npm run devnet:operator:drawer:sim` to prove current reserve, plan, funding, obligation, claim, and control builders still reach the deployed program without mutating state.
7. Capture observability with `OBSERVABILITY_OUTPUT_JSON=artifacts/devnet_observability.json npm run devnet:beta:observe` and archive the output with the rollout notes.
8. Keep a structured monitoring window for the first 24 hours after rollout.

## Observability

### Quick snapshot

```bash
npm run devnet:beta:observe
```

### Save structured output

```bash
OBSERVABILITY_OUTPUT_JSON=artifacts/devnet_observability.json npm run devnet:beta:observe
```

### Signals to review

- instruction success and failure counts
- dominant failure reasons from program logs
- missing or zeroed canonical fixture addresses after shared-devnet bootstrap
- operator drawer simulation failures or frontend parity regressions

## Incident Runbooks

### Control authority recovery

Trigger: reserve-domain, plan, sponsor, or claims control authority cannot execute required safety actions.

Steps:
1. Confirm the deployed program id, current reserve-domain admin, plan admin/sponsor operator, claims operator, and the signer or multisig expected to control each role.
2. If a role cannot be recovered through the existing configured authority, initialize a replacement devnet environment or redeploy with the intended authority before treating the environment as usable.
3. If the required safety action is a stop, set the relevant reserve-domain or health-plan `pause_flags` through the authorized update-control path.
4. Validate the resulting authority and pause state through on-chain readback plus frontend signoff.
5. Execute a low-risk follow-up drawer simulation before resuming normal operations.
6. Resume only after authority checks, pause posture, and builder simulation are green.

### Emergency pause

Trigger: abnormal claim settlement failures, replay anomalies, or governance compromise suspicion.

Steps:
1. Set the relevant reserve-domain or health-plan pause flags through the authorized update-control path.
2. Announce the pause and investigation window in operator channels.
3. Run an observability snapshot and collect affected signatures.
4. Validate the remediation on a dry-run wallet set.
5. Unpause only through the same approved authority path after the fix is verified.

### Failed bootstrap remediation

Trigger: live bootstrap fails or leaves the shared-devnet fixture graph partially refreshed.

Steps:
1. Inspect the failing signature, program logs, and the final JSON summary from `protocol:bootstrap:devnet-live`.
2. If the failure was caused by a missing mint, signer mismatch, or unsupported retired fixture row, fix the env or fixture filter and rerun the bootstrap.
3. If the bootstrap partially executed, verify account existence and idempotency before retrying.
4. Run `npm run devnet:frontend:bootstrap`, `npm run devnet:frontend:signoff`, and `npm run devnet:operator:drawer:sim` after remediation.
5. Capture the root cause and update the launch checklist.

## Ownership

- Control-authority operations owner: protocol core team
- Oracle operations owner: oracle service team
- Frontend and operator support owner: protocol web team
- Incident commander: assigned per launch window
