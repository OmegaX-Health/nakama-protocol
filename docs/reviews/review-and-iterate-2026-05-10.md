# Review and Iterate Readiness Review

Date: May 10, 2026

Reviewed HEAD: `148018e4cd85`

Follow-up status: the code findings below were patched on May 11, 2026 in the
release-gate follow-up. The historical review remains here to preserve the
audit trail.

This is the public-safe copy of the local review-and-iterate pass. The local
`.superstack/` build-context and HTML artifact were refreshed for operator
handoff, but that directory is intentionally blocked by the public hygiene gate
and must not be published.

## Verdict

The current branch is meaningfully stronger than the previous pass: the earlier
health-plan domain-control gap, membership-seat writability mismatch, direct
claim accounting bug, and private claim-review QEDGen wrapper drift are closed
or materially improved.

At review time it was not mainnet-ready because allocation lifecycle enforcement
was missing on fresh capital allocations. The follow-up patch now blocks fresh
allocation into inactive or deallocation-only allocation positions, inactive
liquidity pools, and inactive capital classes.

## Scorecard

| Dimension | Score | Evidence |
| --- | --- | --- |
| Security | `B` after follow-up | previous high-risk authorization and settlement-accounting issues are fixed; allocation lifecycle and mainnet bootstrap guard bypasses are now patched |
| Quality | `B+` after follow-up | generated artifacts, wrapper tests, and session ID canonicalization are aligned; formal lanes are documented as coverage/spec hygiene unless proof bodies are complete |
| Mainnet readiness | `No` | still requires full localnet release-candidate evidence and production operator sign-off before mainnet |

## Findings and follow-up status

### Medium: allocation lifecycle controls are bypassable

`update_allocation_caps` can set `allocation_position.active` and
`allocation_position.deallocation_only`, but `allocate_capital` does not enforce
either flag before increasing exposure. The handler also skips active checks for
the surrounding `liquidity_pool` and `capital_class`.

Evidence:

- `programs/nakama_coverage_protocol/src/capital/allocations.rs:107`
- `programs/nakama_coverage_protocol/src/capital/allocations.rs:128`
- `programs/nakama_coverage_protocol/src/capital/allocations.rs:153`

Recommended fix:

```rust
require!(
    ctx.accounts.liquidity_pool.active,
    NakamaProtocolError::LiquidityPoolInactive
);
require_capital_class_active(&ctx.accounts.capital_class)?;
require!(
    ctx.accounts.allocation_position.active
        && !ctx.accounts.allocation_position.deallocation_only,
    NakamaProtocolError::AllocationPositionInactive,
);
```

Follow-up: fixed. `allocate_capital` now calls lifecycle guards before mutation,
with Rust unit coverage and a security regression that checks the guard order
and IDL-exposed errors.

### Low: private review session ID canonicalization diverges

The frontend helper trims `sessionId` before deriving the private claim-review
session PDA, but the adjunct program stores and seeds raw
`args.session_id.as_bytes()` after only requiring that `trim()` is non-empty. A
whitespace-padded session ID can therefore be valid on-chain but unreachable by
the browser's derived lookup.

Evidence:

- `frontend/lib/private-claim-review.ts:113`
- `programs/nakama_private_claim_review/src/lib.rs:186`
- `programs/nakama_private_claim_review/src/lib.rs:704`
- `programs/nakama_private_claim_review/src/lib.rs:721`

Recommended fix:

Pick one canonical rule. Prefer rejecting leading/trailing whitespace on-chain
in `open_review_session` and `delegate_review_session`, then keep frontend trim
as input normalization. If whitespace is intentionally allowed, remove the
Follow-up: fixed. The adjunct program now rejects non-canonical session IDs
with leading or trailing whitespace, and the frontend PDA helper rejects the
same input before derivation.

### Low: formal proof completeness should not be overclaimed

The QEDGen gates pass, and private claim-review operation/property coverage is
now 100%. The proof story is still a coverage/spec hygiene gate rather than a
complete formal proof package:

- the private claim-review run still lists missing Lean theorem obligations
- the generated main-protocol Anchor model still contains
  `todo!("fill non-mechanical effects, events, transfers, calls")` placeholders

Recommended fix:

Follow-up: fixed by scoping. The README now states that the current QEDGen lane
is coverage/spec hygiene unless concrete proof bodies are committed, and that
generated theorem stubs or non-mechanical-effect placeholders are not mainnet
formal-proof sign-off.

### High: mainnet bootstrap guard override bypass

Follow-up audit found that `OMEGAX_LIVE_CLUSTER_OVERRIDE=devnet` could make the
bootstrap guard treat a literal mainnet RPC URL as non-mainnet. That skipped the
mainnet distinct-role hard fail.

Follow-up: fixed. Mainnet detection now remains load-bearing when the resolved
RPC URL is mainnet-like, regardless of a devnet/localnet cluster override.
Private mainnet-like rehearsals must use the documented break-glass override and
emit the release-evidence warning. The bypass regression was flipped into a
rejection test.

## Closed since the previous pass

| Prior finding | Current status |
| --- | --- |
| `create_health_plan` did not require reserve-domain control | Fixed; the current public Node suite includes the `[CSO-2026-05-10] health plan creation requires reserve-domain control` regression |
| `update_member_eligibility` mutated `membership_anchor_seat` without generated writability | Fixed; IDL freshness and protocol contract checks pass |
| Direct same-asset claim settlement consumed delivery buckets instead of a direct reserve/free-reserve path | Fixed; direct settlement now consumes free reserve and linked obligation settlement remains separate |
| Private claim-review QEDGen wrapper allowed stale no-property coverage | Improved; wrapper coverage is 100% and handler/effect drift is enforced, with proof completeness still tracked above |

## Verification

| Command | Result |
| --- | --- |
| `npm run verify:public` | Passed: Rust fmt/tests/clippy, IDL freshness, protocol contract check, 281 Node tests, Next build, semantic readiness, public hygiene, license audit, dependency advisory acceptance, and SBOM generation |
| `npm run qedgen:check` | Passed via wrapper acceptance: 177 info, 1 accepted warning, 0 errors; accepted warning remains `missing_cpi_for_token_context` on `create_domain_asset_vault` |
| `npm run qedgen:check:private-claim-review` | Passed with empty handler/effect coverage drift arrays and 100% operation/property coverage; upstream diagnostics still list missing Lean theorem obligations |
| `git diff --check` | Passed before docs edits |

`npm run test:e2e:localnet` was not rerun during this pass. Run it after the
allocation lifecycle fix before release-candidate or mainnet sign-off.
