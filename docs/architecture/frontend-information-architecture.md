# Frontend Information Architecture

The public protocol console is now organized around the canonical health-capital-markets nouns instead of a single overloaded pool workspace.

## Primary UI primitives

The public UI should treat these as first-order objects:

1. `HealthPlan`
2. `PolicySeries`
3. `ClaimCase`
4. `Obligation`
5. `LiquidityPool`
6. `CapitalClass`
7. `AllocationPosition`
8. `ReserveDomain`

## Navigation model

- `/` redirects to `/overview`, the editorial systems-map entrypoint for the protocol workbench
- `/overview` is the first-impression observer route for public protocol state, route selection, and explicit demo/live posture
- `/plans` is the sponsor/operator view
- `/plans/new?template=genesis-protect-acute` is the canonical Genesis bootstrap entrypoint
- `/plans?...&setup=genesis-protect-acute` is the bounded Genesis setup, reserve-warning, and issuance-posture view inside the mounted plan workspace
- `/capital` is the LP and capital-markets view
- `/claims` is the operator claim-intake, liability, and adjudication view
- `/members` is the operator-mediated enrollment and member-rights posture view
- `/governance` is the scoped-control, bootstrap, and authority view
- `/oracles` is the oracle registry, readiness, and pool-binding dashboard
- `/oracles/register` and `/oracles/[oracleAddress]/update` are the dedicated oracle profile authoring flows
- `/schemas` explains comparability and series versioning

Legacy `/pools/*` routes are retained only as redirects to avoid carrying pool-first concepts forward in the main UX.

Mounted canonical routes should resolve their primary data from the live protocol snapshot adapter rather than from checked-in fixture state. Fixtures remain valid for tests, docs, bootstrap generation, and local previews, but they should not be the default operator truth surface for the mounted workbenches.

## Genesis operator mode

Genesis Protect Acute uses the same mounted `/plans` workspace rather than a separate launch console.

- `/plans/new?template=genesis-protect-acute` seeds the canonical plan, pool, class, series, funding-line, and allocation shell for Event 7 and Travel 30.
- `/plans?...&setup=genesis-protect-acute` keeps the operator on the live plan workspace while exposing the Genesis checklist, reserve-warning posture, and per-SKU launch truth.
- `/plans?...&setup=genesis-protect-acute&tab=claims` is the Genesis operator claim queue, with queue filters and selected-case detail inside the mounted workspace rather than a separate operator app.
- `/plans?...&setup=genesis-protect-acute&tab=treasury` is the Genesis reserve console, with lane filters, degraded-visibility warnings, and treasury actions scoped from the selected live funding lane.
- Travel 30 is the primary launch SKU and Event 7 remains the fast demo SKU when no explicit Genesis series is selected.
- This mounted mode must speak in launch-readiness language: Founder reservations pending activation, not broadly live insurance today, and Phase 0 operator-backed claim review with later AI and decentralized steps framed as roadmap.
- Setup, claims, and treasury must share one Genesis-derived posture model so queue warnings, reserve warnings, and launch-readiness copy do not drift between tabs.

## Overview route

The overview route is not a generic dashboard. It is the protocol entry composition: a sticky editorial hero rail on the left and a flowing access stream on the right.

- The left rail establishes protocol mood and orientation through one large headline, one aggregate network value, a signal-wave moment, and compact metric chips.
- The right rail is the navigation surface. It stages the major workbench destinations as staggered route cards, then closes with a live field log.
- Desktop keeps the hero rail visually stable while the document scroll moves the access stream beneath the floating top and bottom chrome.
- Mobile collapses to one column, but keeps the same sequence and hierarchy instead of inventing a separate dashboard layout.

The approved visual grammar for this route lives in the repository-level [`DESIGN.md`](../../DESIGN.md). Treat that document as the source of truth when extending or redesigning `/overview` or any mounted protocol-console route.

## Route responsibility contract

Each mounted route must have one clear job:

| Route | Primary question | Route responsibility |
| --- | --- | --- |
| `/` | Where do I begin? | Redirect to `/overview` so the first impression is the public systems map. |
| `/overview` | What is live, pending, simulated, or unavailable? | Orient observers and route them to the correct workbench without implying fixture or demo state is live. |
| `/plans` | What sponsor/operator state exists for a plan and its coverage products? | Keep plan, member, claim, treasury, and Genesis setup state together. |
| `/capital` | What capital is posted, allocated, queued, or impaired? | Keep LP capital separate from sponsor budgets and claim obligations. |
| `/claims` | Which claim cases and obligations need review? | Mount the claim queue without presenting Phase 0 review as decentralized adjudication. |
| `/members` | Which wallets have plan/series rights? | Redirect into the mounted `/plans` member tab with context preserved. |
| `/governance` | Which authorities and proposals control protocol state? | Expose scoped control lanes and templates without hiding disabled-action reasons. |
| `/oracles` | Which oracle operators and bindings are visible? | Keep profile, schema, attestation, dispute, and staking readiness separate. |
| `/schemas` | Which outcome schemas and series comparability rules are live? | Provide first-class registry and inspector access from the main navigation. |
| `/coverage/*` | What public coverage terms and risk disclosures are referenced? | Stay read-only and bounded to the current Genesis launch truth. |
| `/magicblock-claim-room` | Is a private-review receipt verifiable? | Stay devnet-only for verification and fail closed on mainnet. |
| `/pools/*`, `/staking` | Where did retired routes move? | Redirect to canonical routes without reintroducing pool-first language. |

## Naming rules

- Use `HealthPlan` as the canonical protocol noun.
- Sponsor-facing copy may say `Program` where it improves comprehension, but it should still map to `HealthPlan`.
- Use `LiquidityPool` and `CapitalClass` explicitly for investor-facing surfaces.
- Do not use one generic `pool` label for both sponsor programs and LP vaults.

## Read-model rules

The frontend should answer different questions for different audiences:

- sponsors need funded budget, remaining budget, accrued obligations, paid outcomes, and claim status
- members need series rights, delegated rights, claim state, and payout history
- capital providers need NAV, reserved liabilities, pending queue pressure, impairment state, and exposure mix

Those views should be derived from the same canonical reserve kernel rather than from disconnected UI-specific math.
