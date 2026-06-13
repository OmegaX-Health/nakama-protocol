# OmegaX Protocol

OmegaX Protocol's current launch job is concrete: help a sponsor fund Travel 30 acute travel protection for a cohort, show whether the reserve posture can support it, and trace every claim from evidence to payout.

Plainly: a sponsor can fund a protected group, see what backs the promise, and audit what happened when a claim is reviewed or paid.

The current public launch reference is Genesis Protect Acute. `Travel 30` is the primary Founder SKU: a 100-seat cohort where 99 USDC reserves access to a reserve-indexed 30-day travel cap targeting up to 250,000 USDC at activation, unlocked only when the posted claims-paying reserve/backstop reaches the required threshold and final terms are ready. `Event 7` is the short-window cohort/demo SKU, with a 7-day window and a 3,000 USDC fixed-benefit cap. Both remain bounded launch surfaces: reservations are not active cover today, pending custody is not claims-paying reserve, this is not comprehensive travel insurance, and Phase 0 claim review is operator-backed rather than fully decentralized.

On Solana devnet beta today, the public surface in this repository can already anchor:

- sponsor-funded reward or protection lanes with explicit reserve and funding-line attribution
- operator-mediated member enrollment, claim intake, obligations, reserve booking, and payouts
- LP-facing capital pools, classes, allocations, redemptions, and impairment handling
- normalized outcome events produced by OmegaX Health or future compatible oracle operators

## Start Here

- [Genesis Protect V1 Curve Launch Plan](./docs/architecture/genesis-protect-v1-curve-launch.md)
- [Genesis Protect Claim Trace](./docs/architecture/genesis-protect-claim-trace.md)
- [What Exists Today](https://docs.omegax.health/docs/protocol/current-program-surface)
- [Repository Documentation Map](./docs/README.md)
- [SDK Overview](https://docs.omegax.health/docs/sdk/sdk-overview)

## Choose Your Path

### Sponsors and protection operators

Fund a Travel 30 cohort, inspect reserve sufficiency, follow claim obligations, and prove payouts without treating pending custody, premiums, LP capital, or claims-paying reserve as the same thing.

Start with:

- [Genesis Protect V1 Curve Launch Plan](./docs/architecture/genesis-protect-v1-curve-launch.md)
- [Genesis Protect Claim Trace](./docs/architecture/genesis-protect-claim-trace.md)
- [What Exists Today](https://docs.omegax.health/docs/protocol/current-program-surface)

### Capital integrators

Connect pools, classes, allocations, redemption queues, and reserve-domain accounting to the same Travel 30 / Event 7 launch truth.

Start with:

- [Protocol Architecture](https://docs.omegax.health/docs/protocol/architecture)
- [Public Release Gate](./docs/operations/public-release-gate.md)
- [Release v0.3.1](./docs/operations/release-v0.3.1.md)

### Oracle and event producers

Build normalized event pipelines, oracle operators, and verification services that feed OmegaX-compatible outcomes into the protocol.

Start with:

- [Oracle Event Production](https://docs.omegax.health/docs/oracle/event-production)
- [SDK Overview](https://docs.omegax.health/docs/sdk/sdk-overview)
- [What Exists Today](https://docs.omegax.health/docs/protocol/current-program-surface)

### Health / wallet / app builders

Use the public SDK and read models to integrate member state, claim intake, payout posture, and outcome-triggered experiences into apps, wallets, or agents.

Start with:

- [SDK Getting Started](https://docs.omegax.health/docs/sdk/sdk-getting-started)
- [SDK Workflows](https://docs.omegax.health/docs/sdk/sdk-workflows)
- [What Exists Today](https://docs.omegax.health/docs/protocol/current-program-surface)

## What Exists Today on Devnet Beta

- reserve domains and domain asset vaults define settlement boundaries and payment rails
- health plans, policy series, and funding lines define sponsor and member-side products
- operator-mediated member enrollment, claim intake, obligations, settlement, and impairment are mounted in the canonical console
- liquidity pools, capital classes, allocations, and redemptions define LP-facing exposure and queue behavior
- oracle registry and schema registry accounts let outside event producers and integrations target the same public surface

## Long-Term Destination

OmegaX Health is the first oracle and the public sponsor/operator console is the first managed experience around the protocol.

The destination is still health capital markets: one shared settlement foundation that can support sponsor programs, coverage products, outside oracle builders, wallet-native health apps, and capital formation without fragmenting the underlying accounting truth.

## Protocol Model

The canonical public model in this repository is:

- `ReserveDomain`: hard custody or legal segregation boundary
- `DomainAssetVault`: token custody per `[reserve_domain, asset_mint]`
- `HealthPlan`: sponsor/member/liability root
- `PolicySeries`: versioned product lane
- `FundingLine`: plan-side funding source
- `ClaimCase`: explicit adjudication lifecycle for material claims
- `Obligation`: canonical liability unit
- `LiquidityPool`: LP-facing capital sleeve
- `CapitalClass`: investor instrument inside a pool
- `AllocationPosition`: explicit capital-to-plan bridge

## Current Surface Notes

This repository treats the earlier pool-first surface as retired devnet history and improves the current canonical model in place.

- sponsor budgets are not LP capital
- reward and protection reconcile through one reserve kernel
- reserve truth is ledger-based, not implied by scattered treasuries
- restricted or wrapper-mediated participation is layered through reserve domains, capital classes, and managed LP credentialing rather than parallel protocols

## Release Status

Current publish target: `v0.3.1`.

The repository is a devnet-beta public protocol surface, not a live insurance
issuance surface. Current release notes, evidence templates, and operator
runbooks live under [`docs/operations/`](./docs/operations/); the root README
stays focused on orientation, setup, and verification.

Read the canonical design set first:

- [ADR 0001](./docs/adr/0001-health-capital-markets-rearchitecture.md)
- [WHY_THIS_MODEL](./docs/WHY_THIS_MODEL.md)
- [MIGRATION_MATRIX](./docs/MIGRATION_MATRIX.md)
- [Public Release Gate](./docs/operations/public-release-gate.md)
- [Devnet Beta Runbook](./docs/operations/devnet-beta-runbook.md)
- [Release v0.3.1](./docs/operations/release-v0.3.1.md)

## Repository Layout

- [`programs/omegax_protocol/`](./programs/omegax_protocol/) contains the onchain Anchor program
- [`frontend/`](./frontend/) contains the public protocol console and deterministic read models
- [`tests/`](./tests/) contains the fast Node-based scenario suite
- [`e2e/`](./e2e/) contains the heavier localnet audit entrypoint
- [`scripts/`](./scripts/) contains artifact generation and devnet migration helpers
- [`idl/`](./idl/), [`shared/`](./shared/), and [`frontend/lib/generated/`](./frontend/lib/generated/) contain checked-in generated contract artifacts

## Quick Start

Install dependencies:

```bash
npm ci
npm --prefix frontend ci
```

Regenerate the canonical onchain artifacts:

```bash
npm run anchor:idl
npm run protocol:contract
```

Run the fast scenario suite:

```bash
npm run test:node
```

Build the public console:

```bash
npm run frontend:build
```

Run the public verification gate:

```bash
npm run verify:public
```

## Formal Verification

QEDGen and Certora-oriented materials live under
[`formal_verification/`](./formal_verification/) with the root
[`omegax_protocol.qedspec`](./omegax_protocol.qedspec). Treat those lanes as
maintainer verification evidence, not as an external audit or mainnet formal
proof claim.

## Maintainer and Devnet Operations

These helpers are for repo maintainers and shared-devnet operators rather than first-time SDK consumers. Start with [Operator Runbooks](./docs/operations/runbooks.md) before running any command that can mutate shared devnet state.

- `npm run protocol:bootstrap` refreshes `devnet/health-capital-markets-manifest.json` and `devnet/health-capital-markets.env.example`
- `npm run protocol:bootstrap:devnet-live` seeds the canonical plan/capital/oracle/schema graph onto shared devnet using the configured signer
- `npm run devnet:frontend:bootstrap` syncs canonical fixture env values into `frontend/.env.local` and writes `frontend/public/devnet-fixtures.json`
- `npm run devnet:beta:deploy` runs checked build and artifact parity, then prints the operator-mediated deploy command
- `npm run devnet:frontend:smoke` and `npm run devnet:frontend:signoff` check the canonical fixture set and frontend parity matrix
- `npm run devnet:beta:observe` captures a structured observability snapshot for the shared devnet deployment

## Verification Philosophy

The fast suite now focuses on the scenarios that matter to the redesign:

- sponsor-only reward plan without LP capital
- LP-funded protection flows with reserve-aware redemption math
- one pool funding multiple series
- multiple pools co-funding one series
- reward plus protection under one plan root
- restricted capital-class semantics
- separate reserve-domain ring-fencing
- impairment and queue pressure
- scoped pause behavior
- migration smoke for legacy surface retirement

## Documentation Map

- [Solana Program Architecture](./docs/architecture/solana-program-architecture.md)
- [Solana Instruction Map](./docs/architecture/solana-instruction-map.md)
- [Repository Layout](./docs/architecture/repository-layout.md)
- [Frontend Information Architecture](./docs/architecture/frontend-information-architecture.md)
- [tests/README.md](./tests/README.md)

## Public-Safe Boundary

This repository is public-safe by design.

Do not commit:

- private backend services
- private endpoints
- secrets or local validator state
- operator credentials
- machine-specific output

Keep deployment-only control-plane automation outside this repository.
