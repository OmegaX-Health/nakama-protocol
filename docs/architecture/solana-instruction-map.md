# Solana Instruction Map

This map lists the current public instructions after the Quasar trimming pass.
The authoritative facade is
[`programs/nakama_coverage_protocol/src/lib.rs`](../../programs/nakama_coverage_protocol/src/lib.rs);
implementation and account contexts live in the domain modules under
`programs/nakama_coverage_protocol/src/`.

## Reserve Domains and Plans

| Instruction | Primary purpose |
| --- | --- |
| `create_reserve_domain` | create a hard custody or legal settlement boundary |
| `update_reserve_domain_controls` | update domain-scoped rails, pause flags, and active status |
| `create_domain_asset_vault` | create custody for one domain/mint pair |
| `create_health_plan` | create the sponsor/liability/control root |
| `update_health_plan_controls` | update plan operators, oracle authority, rails, and pause flags |
| `create_policy_series` | create a versioned product lane under a plan |
| `version_policy_series` | create a successor series version instead of silently mutating live terms |

## Funding and Reserve Accounting

| Instruction | Primary purpose |
| --- | --- |
| `open_funding_line` | create a sponsor budget, premium income, backstop, or subsidy funding line |
| `fund_sponsor_budget` | transfer sponsor budget tokens into the domain vault and increase reserve ledgers |
| `record_premium_payment` | transfer premium tokens into the domain vault and increase reserve ledgers |
| `deposit_reserve_capital` | let a contributor sign a simple backstop deposit and update its `CapitalContribution` balance |
| `return_reserve_capital` | return available free backstop capital to the recorded contributor without touching encumbered reserve |
| `record_reserve_earnings` | transfer realized same-mint earnings into the domain vault with a nonzero off-chain reference hash |

`CapitalContribution` is an attribution record, not a tokenized share class. It
lets the quote oracle or operator systems know who supplied backstop capital and
how much has been returned, while pricing, discounts, and manual reward policy
stay off-chain for this version.

`FundingFlowRecordedEvent.reference_hash` carries the relevant off-chain proof
fingerprint when one exists: contribution terms for reserve-capital deposits,
return reasons for capital returns, and earnings references for realized
reserve earnings. Sponsor-budget and premium inflows use a zero reference hash.

## Obligations and Claims

| Instruction | Primary purpose |
| --- | --- |
| `create_obligation` | create a canonical liability unit tied to a funding line |
| `reserve_obligation` | reserve liability against free plan/funding-line capacity and mirror linked claim reserve state |
| `settle_obligation` | settle or cancel an obligation with matching vault, ledger, funding-line, and SPL payout accounts |
| `release_reserve` | release reserved liability back to free capacity and mirror linked claim state |
| `open_claim_case` | open an explicit claim lifecycle for a claimant and funding line |
| `authorize_claim_recipient` | lock a non-default payout recipient before approval or payout state exists |
| `adjudicate_claim_case` | approve, deny, or request review while preserving claim evidence and decision fingerprints |
| `settle_claim_case` | settle an approved unlinked same-asset claim through the reserve kernel |

Raw medical/evidence packets and adjudication packages stay private and
off-chain. The base program stores only 32-byte proof fingerprints on
`ClaimCase`: `evidence_ref_hash` and `decision_support_hash`.

## Retired From the Live Surface

The trimmed live program no longer exposes protocol governance, fee vaults,
member-position/token-gate rails, oracle registry/schema registry accounts,
reserve-asset rail price feeds, liquidity pools, capital classes, LP positions,
allocation positions, redemption queues, impairment handlers, or on-chain
`ClaimAttestation` accounts.

Historical docs may still describe those ideas as roadmap or design history,
but they are not current IDL surface. Current review should follow `src/lib.rs`,
`src/reserve_custody.rs`, `src/plans_membership.rs`,
`src/funding_obligations/`, `src/claims.rs`, and the generated artifacts under
`idl/`, `shared/`, and `frontend/lib/generated/`.

## Planned Reserve Productivity Surface

The long-term reserve-productivity direction remains off the live IDL. When it
returns, it should stay separate from the claims kernel: deploy only eligible
free reserve, reconcile realized tokens before counting them as claims-paying
capacity, and record losses against the correct reserve scope.

Hard boundary: deployed principal, unrealized APY, and adapter-reported rewards
do not count as free claims-paying reserve.
