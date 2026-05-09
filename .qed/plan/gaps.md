# QEDGen Gaps

| Pattern | Status | Hypothesis |
| --- | --- | --- |
| `create_domain_asset_vault` init-only token-program account | Accepted warning | A QEDGen lint should distinguish SPL token program usage for token-account initialization from transfer CPI contexts. See `findings/001-domain-vault-init-token-program.md`. |
| Lifecycle `active` flag written but not enforced on intake/deposit paths | Fixed in protocol guards | Health-plan fresh intake and capital-class deposits now require active status; the QEDGen spec mirrors those guards. See `findings/002-write-only-lifecycle-active-flag.md`. |
| Handler coverage drift masked by repo wrapper | Fixed in repo wrapper | The wrapper now fails on `ProgramInstructionNotInSpec` docs and any unaccepted nonzero checker status, even when docs lack `rule` and `severity`. |
