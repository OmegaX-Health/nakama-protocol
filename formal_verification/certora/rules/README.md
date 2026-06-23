# Certora Rules

Add CVLR rules incrementally and keep each rule mapped to an existing Nakama
security invariant or regression test. The current sanity lane intentionally
uses constrained kernel/scalar models that Certora Solana can prove remotely
today; it does not claim full Anchor handler/account-flow proofs.

Implemented in `programs/nakama_coverage_protocol/src/certora.rs`:

- `rule_selected_asset_payout_bounds`: selected-asset payout value must stay
  between the claim value and the configured maximum overpay.
- `rule_fee_recipient_binding`: fee withdrawals must bind the accepted
  recipient owner to the configured nonzero fee recipient.
- `rule_fee_vault_withdrawal_bounds`: fee-vault withdrawals must be positive,
  non-overflowing, and no larger than accrued fees minus prior withdrawals.
- `rule_reserve_capacity_non_overflow`: reserve balance-sheet free and
  redeemable capacity calculations must not overflow and must not exceed funded
  balance.

Future rule candidates:

- Extend vault-transfer bounds from the fee-vault scalar model into selected
  claim, obligation, redemption, and reserve-settlement submodels.
- Add deeper PDA/signature binding models once the Solana prover path can carry
  more Anchor account-flow structure without losing determinism.

Do not add rules only to prove already-trivial happy paths. Prioritize money
movement, reserve accounting, oracle/claim finality, and privileged role
boundaries.
