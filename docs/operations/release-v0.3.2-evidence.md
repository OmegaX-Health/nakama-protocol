# Release v0.3.2 Evidence

This is the production-promotion evidence snapshot for the pre-mainnet security
completion work. It is assembled for review, not a mainnet funding approval.
Mainnet sends and real reserve funding remain blocked until the remote CI/PR and
external-review gates below are closed.

## 1. Identity

| Field | Value |
|-------|-------|
| Release tag | `v0.3.2` |
| Candidate implementation commit | `a3756f6026c36c422c04d523a6f1290fe1756cff` |
| Branch where assembled | local `main` |
| Date assembled (UTC) | `2026-05-04T15:55:16Z` |
| Maintainer | `Marino Sabijan, MD <marinosabijan@gmail.com>` |

Push status: direct `main` push was rejected by branch protection:
`GH006: Changes must be made through a pull request; Required status check "verify" is expected.`
Remote CI for `a3756f6026c36c422c04d523a6f1290fe1756cff` is therefore a blocker until this
commit is pushed through an approved PR branch.

## 2. Generated Artifact Hashes

| Artifact | SHA-256 |
|----------|---------|
| `idl/omegax_protocol.json` | `1b725769b0edffdf74188132516b2a57babf937cd94a6c78bab4fa4cddc71c1b` |
| `idl/omegax_protocol.source-hash` file | `8c72c891fbf84b928c831fc73a030f157f42d8863ea9cb2cc02e860849c556cd` |
| `idl/omegax_protocol.source-hash` value | `cb89cecec5597e42d9dc2f958705aa10f83b8508237cd344177774154dbda762` |
| `shared/protocol_contract.json` | `14157588296844e66f7618fd96e46a5031c53e3c0207b6e6de193d8d96aa0082` |
| `frontend/lib/generated/protocol-contract.ts` | `4a0153cdfc5a4513cf3cd0a680a1e797b910c08449b9d95da9165f97bc83a8fa` |
| `frontend/lib/generated/protocol-contract.js` | `aba0d1fdf84bf9aa1f3c26405baef2174a05c12227d977ac99120aae78ce1e0c` |

| Drift gate | Result |
|------------|--------|
| `npm run idl:freshness:check` | PASS, inside `npm run verify:public` |
| `npm run protocol:contract:check` | PASS, inside `npm run verify:public` |

## 3. CI Evidence

| Workflow | Candidate run URL | Run ID | Conclusion | Status |
|----------|-------------------|--------|------------|--------|
| Public CI (`ci.yml`) | blocked until PR branch | n/a | n/a | BLOCKER |
| CodeQL (`codeql.yml`) | blocked until PR branch | n/a | n/a | BLOCKER |
| Localnet E2E (`localnet-e2e.yml`) | no remote run found for candidate | n/a | n/a | BLOCKER |

Last remote `main` baseline before this local commit:

| Workflow | Run URL | Run ID | Head SHA | Conclusion |
|----------|---------|--------|----------|------------|
| Public CI | `https://github.com/OmegaX-Health/omegax-protocol/actions/runs/25328526732` | `25328526732` | `be440d686f276e8dcc79316c3de9c18c634579a3` | success |
| CodeQL | `https://github.com/OmegaX-Health/omegax-protocol/actions/runs/25328526977` | `25328526977` | `be440d686f276e8dcc79316c3de9c18c634579a3` | success |

## 4. Branch Protection State

| Setting | Expected | Actual |
|---------|----------|--------|
| Branch protection enabled on `main` | yes | yes |
| Required PR review approvals | `>= 1` | `0` BLOCKER |
| Stale review dismissal | yes | yes |
| Required status checks | `verify` | `verify` |
| Strict status checks | yes | yes |
| Admin enforcement | yes | yes |
| Force pushes blocked | yes | yes |
| Branch deletion blocked | yes | yes |

## 5. Local Validation Lanes

| Lane | Command | Result | Artifact |
|------|---------|--------|----------|
| Repo baseline health | `npm run verify:public` | PASS | SBOM under `artifacts/sbom/` |
| Localnet protocol-surface audit | `OMEGAX_E2E_KEEP_ARTIFACTS=1 npm run test:e2e:localnet` | PASS | `artifacts/localnet-e2e-summary-2026-05-04T15-44-34-223Z.json` |
| Executable adversarial localnet | included in localnet E2E | PASS: `57 blocked`, `0 unexpectedSuccess`, `0 inconclusive` | `artifacts/localnet-adversarial-matrix-2026-05-04T15-44-34-224Z.json` |
| Operator drawer simulation | `SOLANA_KEYPAIR=<devnet governance keypair> npm run devnet:operator:drawer:sim` | PASS: `FAIL=0`; expected idempotent collisions and fixture skips only | console output |
| Mainnet preflight, no sends | `npm run protocol:bootstrap:genesis-live -- --plan` with distinct role wallets and mainnet USDC | PASS | console JSON; no transactions sent |
| Mainnet unsafe config tests | `npm run verify:public` node suite | PASS | `tests/genesis_live_bootstrap_config.test.ts`, `tests/genesis_live_bootstrap_plan_cli.test.ts` |

## 6. Dependency Scan

| Field | Value |
|-------|-------|
| `license:audit` | PASS inside `npm run verify:public` |
| Root npm production deps | `103` |
| Frontend npm production deps | `465` |
| Cargo deps | `253` |
| npm advisories | root `3`, frontend `3`; all covered by `docs/operations/dependency-advisory-risk-acceptance.md` |
| SBOM status | PASS, wrote `artifacts/sbom/root-npm-sbom.json`, `artifacts/sbom/frontend-npm-sbom.json`, `artifacts/sbom/cargo-tree.txt` |

## 7. Actuarial Gate

| Field | Value |
|-------|-------|
| Actuarial review state | PASS |
| Source | `npm run genesis:actuarial:review` generated `examples/genesis-protect-acute-actuarial-review/review-output.json` and memo artifacts with no tracked diff |
| Reviewer | internal maintainer, `2026-05-04` |

This release does not add arbitrary launch deposit caps or arbitrary claim caps.
Product terms may define coverage limits; settlement remains constrained by
actual settlement-asset reserve/funding/allocation capacity.

## 8. Devnet Treasury Gate

| Field | Value |
|-------|-------|
| Devnet bootstrap | PASS, `OMEGAX_DEVNET_ROLE_MIN_LAMPORTS=0 npm run protocol:bootstrap:devnet-live` completed after public RPC 429 retries |
| Canary seeding | PARTIAL RERUN: public devnet RPC rate-limited the fresh seed command after linked-claim and test-asset steps; strict pen-test verified all required canaries were already live |
| Strict pen-test | PASS, `npm run devnet:treasury:pen-test -- --strict` |
| Strict result | `8 blocked`, `0 vulnerable`, `0 skipped`, `0 inconclusive` |
| Evidence | `artifacts/devnet-treasury-pen-test-2026-05-04T15-53-44-974Z.json`, `artifacts/devnet-treasury-pen-test-2026-05-04T15-53-44-974Z.md`, tracked summary `docs/security/devnet-treasury-pen-test-2026-05-04.md` |

## 9. Mainnet Preflight

No mainnet transaction was sent. The `--plan` path exits after config/keypair
validation and JSON plan output.

| Field | Value |
|-------|-------|
| RPC | `https://api.mainnet-beta.solana.com` |
| Program ID planned | `Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B` |
| Settlement mint | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| Governance authority used for plan | `AiNPYZQkbfcTkSh3r9vPKAMgMa3TbU47Jk3TaKTCB4Sg` |
| Governance config address | `CsBxTVjC4Y8oWuoU9xdp91du7WCaQWEbGyNBTuc7weDU` |
| Reserve domain | `WfQ7PjCTwuTCn3KM4mxUmyjQSw3RvcnyT3Gfdg2WUoq` |
| Health plan | `D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6` |
| Event 7 series | `6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX` |
| Travel 30 series | `29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco` |
| Pool | `GvfgrHmzoPZXpn1H7L85R7qA9iFr3dBhZYNb5WeXMXqt` |
| Senior class | `7BUpgc71EhLoFcH7PdqHkNyrGYdiCcX9FQ3rS55Moyui` |
| Junior class | `9JAzzfoyysVg1DDoAdXZBN2Hy834RkgGnv5shUg3qywR` |
| Role-map status | distinct wallets supplied for sponsor, sponsor operator, claims operator, oracle, curator, allocator, sentinel, and reserve admin |
| Multisig posture | REQUIRED before real reserve funding; not proven in this evidence package |

Unsafe config proof:

- Missing `OMEGAX_REQUIRE_DISTINCT_OPERATOR_KEYS` fails in node tests.
- Collapsed roles fail in node tests.
- Missing oracle keypair file fails in `--plan` mode before send path.
- Oracle wallet/keypair mismatch fails in `--plan` mode before send path.
- Mainnet-like custom RPC URLs are treated as mainnet unless explicitly overridden.

## 10. External Review / Public Posture

| Field | Value |
|-------|-------|
| External audit completed for this release | no — no external audit conducted |
| Bug bounty program | no public bounty recorded in this repo |
| Third-party review date | none |
| Internal pen-test report | `docs/security/devnet-treasury-pen-test-2026-05-04.md` |
| Outstanding high/critical internal findings | none known after the strict devnet run; external review still missing |

Public messaging must not claim audited, fully decentralized claims, uncapped
solvency, or mixed-asset settlement. Other reserve assets may be shown as
reserve context only; they do not settle USDC claims without an explicit
priced/haircut/conversion or funding action.

## 11. Sign-off

This evidence is sufficient for local pre-mainnet readiness review only. It is
not sufficient for public mainnet funding until the candidate commit has a green
PR/remote CI record, branch review policy is fixed or explicitly accepted, and
money/control surfaces receive independent review.

Signed-off-by: Marino Sabijan, MD <marinosabijan@gmail.com>  
Date: 2026-05-04
