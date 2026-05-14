# Genesis Protect Acute Actuarial Review

## Scope

This folder is the public-safe fixed-SKU launch-gate workbook for Genesis Protect Acute Event 7 and Travel 30.

## Rules

- Keep this folder public-safe. `omegax-protocol` is a public repository.
- Do not import raw Health claim-simulation JSONL, synthetic-user profiles, scenario-pack internals, local `.superstack/` reports, private endpoint details, or machine-local paths.
- Treat generated outputs as deterministic workbook artifacts. Prefer changing `assumptions.json`, `scenario-matrix.json`, or `scripts/genesis_actuarial_review.ts` over manually editing generated conclusions.
- Keep SKU facts aligned with `frontend/lib/genesis-protect-acute.ts` and the Genesis Protect analysis hub.
- Frame the workbook as a launch-gate model, not an external actuarial opinion, insurance filing, legal opinion, or regulatory approval.
- Country posture is an operational gating taxonomy, not a legal availability promise.

## Validation

- Run `npm run genesis:actuarial:review` after changing assumptions, scenarios, generated outputs, or source metadata.
- Run `node --import tsx --test tests/genesis_actuarial_review.test.ts` for focused test coverage.
- Run `git diff --check` before committing.
- Protocol commits require DCO sign-off.
