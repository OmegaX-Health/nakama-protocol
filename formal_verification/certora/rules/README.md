# Certora Rule Backlog

Add CVLR rules incrementally and keep each rule mapped to an existing OmegaX
security invariant or regression test. The first candidates are:

- `rule_fee_recipient_binding`: fee withdrawals must pay the configured fee
  recipient and must not route to arbitrary token accounts.
- `rule_vault_transfer_bounds`: vault outflows must never exceed accrued fees,
  approved claim amounts, outstanding obligations, or pending redemption value.
- `rule_selected_asset_payout_bounds`: selected-asset payouts must satisfy the
  configured underpay/overpay bounds and preserve the canonical claim credit.
- `rule_reserve_capacity_non_overflow`: reserve-capacity arithmetic must not
  overflow or make available capacity exceed configured exposure limits.

Do not add rules only to prove already-trivial happy paths. Prioritize money
movement, reserve accounting, oracle/claim finality, and privileged role
boundaries.
