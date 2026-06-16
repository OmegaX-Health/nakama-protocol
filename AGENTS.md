# Nakama Protocol Agent Rules

This is a public repository. Keep instructions, code, docs, examples, and generated artifacts public-safe.

## Public Boundary
- Work within `README.md`, `CONTRIBUTING.md`, and the nearest local `README.md`.
- Do not add secrets, private keys, private endpoints, internal repo references, machine-local paths, local validator state, or deployment-only config.
- Private backend services, operator credentials, and production control-plane automation stay out of this repo.
- Commits intended for this repo require a DCO sign-off trailer. Use `git commit -s` so Public CI passes `Enforce DCO sign-off`.

## Repo Map
- `programs/nakama_coverage_protocol/`: on-chain program. Pair its local `README.md` with `docs/architecture/`.
- `frontend/`: public Next.js protocol console.
- `tests/`: fast Node verification suite.
- `e2e/`: heavier localnet protocol-surface matrix.
- `scripts/`: verification, generation, and operator tooling. Prefer root `npm run ...` wrappers when available.
- `idl/`, `shared/`, and `frontend/lib/generated/`: checked-in generated artifacts.

## Working Rules
- Keep changes focused and reviewable.
- Update the nearest README or operations doc when commands, responsibilities, or reviewer paths change.
- Add or update tests, docs, and checked-in artifacts when behavior changes.
- Do not hand-edit generated outputs in `idl/`, `shared/`, or `frontend/lib/generated/` unless a documented maintenance workflow explicitly requires it.
- If protocol surface or shared builders change, regenerate with `npm run anchor:idl` and `npm run protocol:contract`.

## Protect Buyer Boundary
- Founder reservation buyer flow belongs in the Nakama website Protect funnel and Nakama Health `protocol-oracle-service`, not as duplicate purchase UI in this console.
- The protocol console may show off-chain Squads-custody reservation status: campaign status, accepted rails, pending/activated/refunded counts, terms hash, linked coverage lane, and reserve-impact disclaimers.
- Keep Founder reservation, Protect quote, activated cover, treasury inventory, and claims-paying reserve semantically distinct in labels, models, and docs.
- Do not present pending reservations as active cover or available claims-paying reserve.
- If external consumer/oracle reservation campaign state cannot be read in production, fail closed in protocol-facing copy.
- Website `/protect/devnet` is a devnet live-coverage simulator owned by website plus Nakama Health app/oracle service. It is not a mainnet protocol-console surface and must not be described as public mainnet coverage.
- Protocol docs may reference the devnet simulator as QA/demo, but settlement truth stays with deployed protocol state, reserve controls, and later `ClaimCase`/`ClaimAttestation` activity.

## Genesis Protect Launch Keys
- Prepared public vanity operator wallet: `oxhocTdPyENqy9RS13iaq2upoNAovMJHu9PMaBxrK8h`.
- Do not commit the private keypair, seed phrase, absolute local keypair path, or funding details.
- When intentionally using this wallet as Genesis live oracle/operator, set `OMEGAX_LIVE_ORACLE_WALLET` to the public key and provide the private keypair only through local operator env via `OMEGAX_LIVE_ORACLE_KEYPAIR_PATH`.
- When intentionally using this wallet as deploy or governance signer, provide the private keypair only through local operator env via `SOLANA_KEYPAIR`.
- Confirm funding and signer role before any mainnet transaction; the vanity wallet was created for launch prep, not automatically authorized or funded.

## Protocol Status
- Treat the protocol surface as actively evolving during development and devnet work.
- Do not assume the current shape is frozen.
- Do not introduce `v2` names, parallel surfaces, or permanent compatibility layers by default.
- Prefer improving the current surface in place unless a real compatibility constraint requires a separate path.
- Keep `programs/nakama_coverage_protocol/src/`, `frontend/lib/protocol.ts`, `shared/protocol_contract.json`, and `idl/nakama_coverage_protocol.json` aligned as the current public surface.
- When editing adjacent code, remove stale `v2` wording from labels, docs, tests, and internal locals instead of carrying it forward.

## Verification
- Run the narrowest relevant checks before finishing.
- Normal public gate: `npm run verify:public`.
- Protocol builders, generated artifacts, or frontend/server helpers: `npm run test:node`.
- Broad protocol-surface, harness, or release-candidate sign-off: `npm run test:e2e:localnet`.

## Done Means
- Code, checked-in artifacts, and docs agree on the same public surface.
- Relevant validation passed, or the skipped heavier check is explicitly reported.
- No secrets, local validator state, deployment-only config, or machine-specific output were added.
