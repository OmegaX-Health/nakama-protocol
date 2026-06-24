# Certora Solana Security Lane

This directory is the manual Certora Solana lane for the Nakama on-chain
program. It is intentionally separate from `npm run verify:public`: Certora
runs submit jobs to Certora's remote prover service, require a personal access
key, and are release-candidate evidence rather than normal public CI.

## Setup

Install the local tools:

```bash
pip3 install certora-cli
cargo install cargo-certora-sbf
```

Register for Certora's free personal access key and export it locally:

```bash
export CERTORAKEY=<personal_access_key>
```

Never commit `CERTORAKEY`, prover credentials, private source bundles, generated
job archives, or dashboard-only links that reveal private run material.

## Local Prerequisite Check

Run this from the repository root:

```bash
npm run certora:solana:check
```

The check verifies local prerequisites and the presence of the lane files. It
does not submit a remote job.

## Manual Sanity Run

Only run this when you are comfortable submitting the configured sources and
summaries to Certora's remote service:

```bash
npm run certora:solana:sanity
```

Because the workspace contains more than one `cdylib` program, the sanity
config sets `build_script` to `build_sanity_coverage.sh`, which scopes the
Certora SBF build to `programs/nakama_coverage_protocol` (the only crate wired
for Certora). Without it, `cargo certora-sbf` fails with "more than one cdylib
package found". Keep the script's `--tools-version` / `--features` in sync with
`cargo_tools_version` / `cargo_features` in the sanity config.

The committed sanity config runs the CVLR rules compiled under the program's
`certora` feature:

- `rule_selected_asset_payout_bounds`
- `rule_fee_recipient_binding`
- `rule_fee_vault_withdrawal_bounds`
- `rule_reserve_capacity_non_overflow`

These are constrained kernel/scalar models for selected high-value accounting
and binding invariants. They are not full Anchor handler proofs, do not prove
complete account-flow correctness, and do not make the repository
"Certora audited." A passing run is internal formal-verification evidence unless
Certora has actually performed and published a third-party review.

The npm wrapper temporarily rewrites the local `Cargo.lock` metadata version
from `4` to `3` while Certora builds because the Certora Solana platform-tools
metadata parser does not yet accept lockfile version 4. It restores the file
before exiting and does not change dependency resolution. The wrapper also
uses an ignored Certora-specific Cargo target directory so platform-tools
artifacts do not mix with normal local Rust build artifacts.

The starter sanity config passes `-solanaSkipCallRegInst true` because Anchor's
compiled SBF currently leaves indirect-call instructions that the Solana prover
cannot encode even after the rule is reduced to scalar accounting logic. Keep
that flag scoped to this starter lane and reassess it for each future rule; do
not treat it as a blanket soundness waiver.

## Query Latest Manual Run

After a manual submission, query the locally recorded latest job from this repo:

```bash
npm run certora:solana:status
```

The status command reads `.certora_internal/.certora_recent_jobs.json`, uses the
locally recorded anonymous dashboard token, and prints the job state plus rule
verdicts from the remote output bundle. It does not use `CERTORAKEY` directly
and does not write run output into tracked files. It redacts the private report
token by default; pass `-- --show-report-url` only when you intentionally want
the local terminal to print the dashboard link. The local status check treats
Certora `SUCCESS` and `VERIFIED` rule verdicts as passing.

## Relationship To QEDGen

QEDGen remains the local brownfield modeling lane for broad handler-surface
coverage. Certora is the narrower remote symbolic-prover lane for high-value
Solana kernel properties such as fee recipient binding, fee-vault withdrawal
bounds, selected-asset payout limits, and reserve-capacity arithmetic.
