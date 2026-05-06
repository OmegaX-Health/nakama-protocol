# 001 Domain Vault Token Program Is Init-Only

## Pattern

`token_program` is present on an Anchor account context for token-account
initialization, but the handler does not perform an SPL token transfer.

## Where It Fires

- Handler: `create_domain_asset_vault`
- QEDGen warning: `missing_cpi_for_token_context`

## Current Interpretation

`create_domain_asset_vault` wires the SPL token program into account
initialization for the domain asset vault token account. It does not move
tokens, credit a payout, or debit a deposit inside this handler.

## Why This Remains Open

QEDGen currently treats a `token_program` account as a strong signal that the
handler should model token-transfer CPI behavior. That heuristic is useful for
reserve-moving handlers, but this initialization-only path needs a narrower DSL
shape: token-program usage for account creation/binding rather than a transfer.

## TODO

Teach the QEDGen model how to express init-only SPL token program usage, or add
a structured suppression category for initialization contexts. Until then,
`create_domain_asset_vault` is the only accepted warning in the QEDGen lane.
