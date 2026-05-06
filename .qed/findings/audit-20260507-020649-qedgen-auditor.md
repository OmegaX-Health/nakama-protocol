# QEDGen Auditor Report - 2026-05-07 02:06:49 MYT

## Digest

- Mode: QEDGen auditor skill, spec-aware against `omegax_protocol.qedspec` plus bootstrap coverage.
- Runtime: Anchor program with QEDGen codegen lane.
- Checkout: `main...origin/main [ahead 6]` at audit start; no unstaged files before this report.
- Real findings: 0 critical, 0 high, 1 medium.
- Spec and design gaps: 4.
- Suppressed or accepted false positives: 1 existing suppression.
- Silent repro count: 0. No critical or high finding survived escalation, so no Mollusk repro was written.

## Commands

- `/Users/dr_sabijan/.codex/skills/qedgen/bin/qedgen probe --spec omegax_protocol.qedspec`
  - Result: spec-aware mode, `findings: []`.
- `npm run qedgen:check`
  - Result: passed with `190 info, 1 warnings, 0 errors`.
  - Accepted warning: `missing_cpi_for_token_context` on `create_domain_asset_vault`.
- `/Users/dr_sabijan/.codex/skills/qedgen/bin/qedgen verify --probe-repros --json`
  - Result: no repro files found under `target/qedgen-repros`; no critical/high repros were required.
- `/Users/dr_sabijan/.codex/skills/qedgen/bin/qedgen probe --bootstrap --root .`
  - Result: detected `runtime: qedgen_codegen`, 70 handlers, and emitted `findings: []`.
- `/Users/dr_sabijan/.codex/skills/qedgen/bin/qedgen check --spec omegax_protocol.qedspec --anchor-project programs/omegax_protocol --coverage --json`
  - Result: exited nonzero because two exported governance handoff instructions are not covered by spec handlers.
- `npm run qedgen:reconcile`
  - Result: no Rust drift and no orphan proofs; 82 Lean proof obligations remain user-owned.
- `rg -n "init_if_needed|remaining_accounts|UncheckedAccount|invoke_signed|unsafe" programs/omegax_protocol/src`
  - Result: no `remaining_accounts`, `UncheckedAccount`, `invoke_signed`, or `unsafe` hits; several `init_if_needed` account contexts remain and were reviewed as seeded/canonical contexts rather than arbitrary-account entry points.

## [MEDIUM] Inactive Plan And Capital-Class Flags Do Not Stop Fresh Intake

Status: real structural issue. Medium severity; no critical/high repro required.

### Affected Code

- `programs/omegax_protocol/src/plans_membership.rs:66-93` lets a plan controller write `health_plan.active = args.active`.
- `programs/omegax_protocol/src/plans_membership.rs:257-324` opens a new member position while checking emergency pause and `PAUSE_FLAG_PLAN_OPERATIONS`, but not `health_plan.active`.
- `programs/omegax_protocol/src/claims.rs:979-1014` binds a claim to an eligible active member and open funding line, but has no `health_plan.active` guard in the account constraints.
- `programs/omegax_protocol/src/capital/classes.rs:67-94` lets a curator write `capital_class.active = args.active`.
- `programs/omegax_protocol/src/capital/lp_positions.rs:37-115` accepts a new LP deposit while checking emergency pause, positive amount, subscription pause flag, and class access mode, but not `capital_class.active`.
- `omegax_protocol.qedspec:1553-1570` models `capital_class.active`, while `omegax_protocol.qedspec:1595-1624` models `deposit_into_capital_class` without an `active == true` precondition.

### Attack Shape

An operator or curator can mark a health plan or capital class inactive, but direct program callers can still enter several fresh-intake paths if the separate pause flag is not also set. That means:

- a member position can be opened under an inactive health plan;
- a claim can be opened under an inactive health plan if the existing membership and funding-line constraints pass;
- an LP can deposit into an inactive capital class if subscriptions are not separately paused.

This does not produce an unauthenticated money-out path. Settlement, allocation, redemption, and fee withdrawals still go through the existing custody and authority checks. The risk is lifecycle-control bypass: shutdown, sunsetting, or incident-response state can be weaker on-chain than the admin/UI state implies.

### Recommended Fix

- Add a narrow `require_health_plan_active(&HealthPlan)` helper and call it from fresh plan/member/claim intake handlers where inactive means closed to new business.
- Add a narrow `require_capital_class_active(&CapitalClass)` helper and call it before `transfer_to_domain_vault` in `deposit_into_capital_class`.
- Keep wind-down semantics explicit. Redemptions may reasonably remain open while a class is inactive; deposits and new intake should not accidentally inherit that behavior.
- Update `omegax_protocol.qedspec` with matching `active == true` guards and properties so QEDGen can catch future lifecycle drift.

## Spec Gap: Governance Handoff Handlers Are Missing From The Spec

Status: verification-gate gap.

Direct QEDGen coverage reports two exported program instructions that have no spec handler:

- `accept_protocol_governance_authority`
- `cancel_protocol_governance_authority_transfer`

Those handlers are exported in `programs/omegax_protocol/src/lib.rs` and implemented in `programs/omegax_protocol/src/governance.rs`. Because they are absent from `omegax_protocol.qedspec`, the two-step governance handoff path is outside the current formal handler coverage.

Recommended fix:

- Add spec handlers for accept and cancel governance authority transfer.
- Make the repo wrapper fail on `handler_coverage.kind == "ProgramInstructionNotInSpec"` or on any nonzero checker status that is not explicitly accepted.

## Spec Gap: Health-Plan Control Updates Are Under-Modeled

Status: spec gap that helps hide the lifecycle issue above.

`update_health_plan_controls` writes sponsor/operator, oracle, membership gate, rail, baseline, pause, active, and audit fields in code. The spec currently models only `audit_nonce +=! 1` at `omegax_protocol.qedspec:724-736`. QEDGen therefore cannot reason about whether `health_plan.active`, plan pause flags, membership mode, or rail controls are enforced by later handlers.

Recommended fix:

- Expand `update_health_plan_controls` effects to model the fields written by the Rust handler.
- Add properties tying deactivation and pause controls to new intake, claim intake, policy-series creation, and funding-line creation.

## Design Gap: Reserve Asset Price Confidence Is Stored But Not Enforced

Status: lower-confidence oracle-risk gap, not a standalone user-drain finding.

`publish_reserve_asset_rail_price` validates `confidence_bps <= 10000` and stores it in `last_price_confidence_bps` at `programs/omegax_protocol/src/reserve_waterfall.rs:96-123`. Freshness and selected-asset payout valuation then check nonzero price, nonzero staleness window, timestamp freshness, and max overpay bounds at `programs/omegax_protocol/src/reserve_waterfall.rs:190-292`, but they do not reject a fresh price whose confidence band is too wide.

This requires authorized oracle/governance input, so it is not a public attacker path by itself. It does mean the on-chain rail cannot currently distinguish a tight fresh quote from a fresh but low-confidence quote during selected-asset payout valuation.

Recommended fix:

- Add a configured `max_confidence_bps` or equivalent rail policy if payout valuation is supposed to reject low-confidence prices.
- Include that policy in `require_fresh_reserve_asset_price_at` or in the selected-asset payout value guard.
- Model the same guard in the spec.

## Design Gap: Selected-Asset Claim Settlement Fee Semantics Are Ambiguous

Status: spec/design ambiguity.

Same-asset `settle_claim_case` computes protocol and oracle fee carve-outs and only transfers the net recipient amount at `programs/omegax_protocol/src/claims.rs:208-390`. `settle_claim_case_selected_asset` validates cross-asset value bounds and transfers the selected payout asset at `programs/omegax_protocol/src/claims.rs:461-575`, but it has no protocol fee vault, oracle fee vault, or fee accrual path.

The README says settlement fee carve-outs must leave a positive net recipient payout at `README.md:99-100`, but the selected-asset route may intentionally be a separate payout lane. The spec should make that posture explicit either way.

Recommended fix:

- If selected-asset payouts should pay the same fees, add fee accounts/accrual and update the specs/tests.
- If selected-asset payouts are intentionally fee-exempt or fees are booked elsewhere, document that exception and add a spec assertion so future reviews do not repeatedly rediscover it.

## Design Gap: Health-Plan Creation Is Domain-Scoped But Not Domain-Controlled

Status: design/spec ambiguity, not escalated as a vulnerability without a confirmed domain-ownership requirement.

`create_health_plan` initializes a plan under an active reserve domain and sets the payer/signer as `plan_admin`, but it does not call `require_domain_control` or otherwise require reserve-domain governance/admin authority at `programs/omegax_protocol/src/plans_membership.rs:16-63` and `programs/omegax_protocol/src/plans_membership.rs:371-388`.

If health-plan creation is meant to be sponsor self-service inside a public reserve domain, that may be intended. If reserve domains are meant to be hard custody/legal settlement boundaries that control their child plan namespace, then this allows an arbitrary signer to occupy a predictable `(reserve_domain, plan_id)` health-plan PDA and create confusing or blocking plan roots.

Recommended fix:

- Decide and document the intended authority model.
- If reserve-domain control is required, gate creation with `require_domain_control`.
- If sponsor self-service is intended, add spec/docs language and UI/operator mitigations for plan-id squatting and public namespace confusion.

## Accepted False Positive

`missing_cpi_for_token_context:create_domain_asset_vault` remains accepted in `.qed/probe-suppress.toml`. The handler passes `token_program` for Anchor token-account initialization of the domain asset vault; it does not transfer SPL tokens in the handler body.

## Corpus Coverage Notes

Exploit-shape review covered sysvar spoofing, account field-chain anchoring, oracle freshness/manipulation, CPI authority confusion, rounding/fee accounting, account close redirection, nonce/admin replay, and lifecycle-state bypass.

No critical/high issue was reported because none had a firing Mollusk repro or a confirmed unauthenticated money-out/admin-takeover path. The remaining pressure is lifecycle semantics, QEDGen spec coverage, and oracle/operator policy clarity.
