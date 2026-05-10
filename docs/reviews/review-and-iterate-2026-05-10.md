# Review and Iterate Readiness Review

Date: May 10, 2026

Reviewed HEAD: `148018e4cd85`

This is the public-safe copy of the local review-and-iterate pass. The local
`.superstack/` build-context and HTML artifact were refreshed for operator
handoff, but that directory is intentionally blocked by the public hygiene gate
and must not be published.

## Verdict

The current branch is meaningfully stronger than the previous pass: the earlier
health-plan domain-control gap, membership-seat writability mismatch, direct
claim accounting bug, and private claim-review QEDGen wrapper drift are closed
or materially improved.

It is not mainnet-ready yet. The remaining blocker is lifecycle enforcement on
fresh capital allocations: an authorized allocator can still increase exposure
after an allocation position has been marked inactive or deallocation-only.

## Scorecard

| Dimension | Score | Evidence |
| --- | --- | --- |
| Security | `B-` | previous high-risk authorization and settlement-accounting issues are fixed, but allocation lifecycle freeze controls are not enforced by `allocate_capital` |
| Quality | `B+` | public gates, generated artifacts, and wrapper tests are strong; remaining drag is seed canonicalization and proof-completeness scope |
| Mainnet readiness | `No` | requires allocation lifecycle fix plus final localnet release-candidate evidence |

## Current findings

### Medium: allocation lifecycle controls are bypassable

`update_allocation_caps` can set `allocation_position.active` and
`allocation_position.deallocation_only`, but `allocate_capital` does not enforce
either flag before increasing exposure. The handler also skips active checks for
the surrounding `liquidity_pool` and `capital_class`.

Evidence:

- `programs/omegax_protocol/src/capital/allocations.rs:107`
- `programs/omegax_protocol/src/capital/allocations.rs:128`
- `programs/omegax_protocol/src/capital/allocations.rs:153`

Recommended fix:

```rust
require!(
    ctx.accounts.liquidity_pool.active,
    OmegaXProtocolError::LiquidityPoolInactive
);
require_capital_class_active(&ctx.accounts.capital_class)?;
require!(
    ctx.accounts.allocation_position.active
        && !ctx.accounts.allocation_position.deallocation_only,
    OmegaXProtocolError::AllocationPositionInactive,
);
```

Add regression coverage for inactive allocation positions and deallocation-only
allocation positions before mutation.

### Low: private review session ID canonicalization diverges

The frontend helper trims `sessionId` before deriving the private claim-review
session PDA, but the adjunct program stores and seeds raw
`args.session_id.as_bytes()` after only requiring that `trim()` is non-empty. A
whitespace-padded session ID can therefore be valid on-chain but unreachable by
the browser's derived lookup.

Evidence:

- `frontend/lib/private-claim-review.ts:113`
- `programs/omegax_private_claim_review/src/lib.rs:186`
- `programs/omegax_private_claim_review/src/lib.rs:704`
- `programs/omegax_private_claim_review/src/lib.rs:721`

Recommended fix:

Pick one canonical rule. Prefer rejecting leading/trailing whitespace on-chain
in `open_review_session` and `delegate_review_session`, then keep frontend trim
as input normalization. If whitespace is intentionally allowed, remove the
frontend trim and derive from raw bytes everywhere.

### Low: formal proof completeness should not be overclaimed

The QEDGen gates pass, and private claim-review operation/property coverage is
now 100%. The proof story is still a coverage/spec hygiene gate rather than a
complete formal proof package:

- the private claim-review run still lists missing Lean theorem obligations
- the generated main-protocol Anchor model still contains
  `todo!("fill non-mechanical effects, events, transfers, calls")` placeholders

Recommended fix:

Either describe those artifacts as scaffold/coverage gates only, or fill and
gate the missing theorem and non-mechanical-effect bodies before claiming formal
proof coverage for mainnet sign-off.

## Closed since the previous pass

| Prior finding | Current status |
| --- | --- |
| `create_health_plan` did not require reserve-domain control | Fixed; the current public Node suite includes the `[CSO-2026-05-10] health plan creation requires reserve-domain control` regression |
| `update_member_eligibility` mutated `membership_anchor_seat` without generated writability | Fixed; IDL freshness and protocol contract checks pass |
| Direct same-asset claim settlement consumed delivery buckets instead of a direct reserve/free-reserve path | Fixed; direct settlement now consumes free reserve and linked/selected-asset paths stay separate |
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
