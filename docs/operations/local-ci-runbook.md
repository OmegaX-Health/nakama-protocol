# Local CI Runbook

Use local checks before pushing so GitHub Actions stays a final gate instead of
the first place a failure is discovered.

## Cheap default gate

Run this before ordinary code changes:

```bash
npm ci
npm --prefix frontend ci
npm run ci:public
```

`ci:public` covers Rust formatting, Rust tests, Rust linting, Quasar checks,
IDL freshness, protocol contract sync, Node tests, frontend build, semantic
readiness, and public hygiene.

## Release/security gate

Run this before public release candidates:

```bash
npm run verify:public
```

This extends the cheap gate with license audit, npm dependency advisories, and
SBOM generation.

## Localnet E2E

Run this when touching the on-chain program, IDL, shared protocol contract,
protocol frontend surface, or localnet harness:

```bash
npm run anchor:build:checked
OMEGAX_E2E_SKIP_BUILD=1 npm run test:e2e:localnet
```

If the Solana or Anchor toolchain is missing locally, use the manual hosted
`Localnet E2E` workflow for a release candidate only.

## QEDGen/Formal Verification

Run these when touching QEDGen specs, formal verification, covered program code,
or proof-generation scripts:

```bash
npm run qedgen:check
npm run qedgen:check:private-claim-review
npm run qedgen:codegen
git diff --exit-code -- nakama_coverage_protocol.qedspec formal_verification
npm run qedgen:verify
npm run qedgen:reconcile
```

Use the manual hosted `QEDGen Verify` workflow only after local reproduction or
for a release candidate.

## Hosted workflow budget rules

- `Public CI` is the only normal automatic hosted gate.
- `CodeQL` runs weekly or manually.
- `Localnet E2E` is manual.
- `QEDGen Verify` is manual.
- Avoid reruns unless the failing log shows an infrastructure-only failure.
