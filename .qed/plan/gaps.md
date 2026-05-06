# QEDGen Gaps

| Pattern | Status | Hypothesis |
| --- | --- | --- |
| `create_domain_asset_vault` init-only token-program account | Accepted warning | A QEDGen lint should distinguish SPL token program usage for token-account initialization from transfer CPI contexts. See `findings/001-domain-vault-init-token-program.md`. |
