# Genesis Protect Acute Public Claim Fixtures

## Scope

This folder contains curated public claim fixtures for Genesis Protect Acute. These are small, inspectable examples for reviewers, frontend consoles, operator training, and protocol documentation.

## Rules

- Keep fixtures public-safe, synthetic, and curated.
- Do not import raw Health claim-simulation JSONL, full synthetic profiles, scenario-pack internals, or proprietary generator logic.
- Do not describe these examples as real claims, paid claim history, medical advice, underwriting, legal advice, or live on-chain state.
- Keep fixture fields aligned with public schemas and protocol docs.
- If a richer example is needed, build a curated public fixture here rather than copying a private case row from `omegax-health`.

## Validation

- Run `jq empty genesis-acute-claim-simulations-v1.json` after editing the fixture JSON.
- Run relevant claim/schema tests when fields change: `node --import tsx --test tests/claim_funding_readiness.test.ts tests/magicblock_private_claim_review.test.ts` as applicable.
- Run `git diff --check` before committing.
- Protocol commits require DCO sign-off.
