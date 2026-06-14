# Phase 0 Mainnet Surface Gating

Phase 0 keeps the on-chain OmegaX program broad and permissioned, but narrows the public mainnet console and bootstrap paths to the conservative live surface.

There is no on-chain `phase0` switch and no duplicated Founder checkout in this repository. The public console is the reserve, liability, LP, operator, and auditor surface. The consumer Founder reservation flow remains outside this repository in the OmegaX website and OmegaX Health protocol oracle service.

## Mainnet Profile

The frontend and bootstrap scripts share `GenesisPhase0LaunchProfile` from `frontend/lib/genesis-phase0-launch-profile.ts`.

Mainnet defaults:

- LP deposit actions are live.
- LP redemption requests are live.
- Capital, reserve, claims, and oracle dashboards are read-only.
- Operator settlement visibility is read-only.
- Rewards, RWA policy launch, hybrid launch, DAO fallback, and future launch choices render as disabled previews.
- Capital admin and policy admin actions are hidden unless operator execution is explicitly enabled.

The on-chain program still enforces the actual security boundary: signer authority, PDA/account binding, custody mint/program validation, Token-2022 rejection, no implicit cross-asset accounting, claim and obligation locks, and role-specific permissions.

## Devnet Profile

Devnet exposes the same code paths, but preview and rehearsal surfaces can become live behind explicit flags. This keeps the public branch identical while allowing devnet rehearsal without a staging-only fork.

Frontend flags:

| Flag | Effect |
|------|--------|
| `NEXT_PUBLIC_ENABLE_REWARD_LAUNCH=1` | Makes reward launch preview actionable on devnet. |
| `NEXT_PUBLIC_ENABLE_RWA_POLICY=1` | Makes RWA policy preview actionable on devnet. |
| `NEXT_PUBLIC_ENABLE_HYBRID_LAUNCH=1` | Makes hybrid launch preview actionable on devnet. |
| `NEXT_PUBLIC_ENABLE_DAO_FALLBACK=1` | Makes DAO fallback preview actionable on devnet. |
| `NEXT_PUBLIC_ENABLE_PROTOCOL_OPERATOR_ACTIONS=1` | Shows operator/admin execution surfaces. |
| `NEXT_PUBLIC_ALLOW_MAINNET_FUTURE_SURFACES=1` | Required in addition to the specific product flag before a future surface can become actionable on mainnet. |

## Bootstrap Guards

The Genesis live bootstrap maps operator environment variables into the same launch profile and refuses accidental mainnet creation of future or admin surfaces before any send path.

Mainnet product/admin allowlist variables:

| Attempted surface | Required product flag | Required mainnet allow flag |
|-------------------|-----------------------|-----------------------------|
| Reward launch | `OMEGAX_LIVE_ENABLE_REWARD_LAUNCH=1` | `OMEGAX_ALLOW_MAINNET_REWARD_LAUNCH=1` |
| RWA policy launch | `OMEGAX_LIVE_ENABLE_RWA_POLICY=1` | `OMEGAX_ALLOW_MAINNET_RWA_LAUNCH=1` |
| Hybrid launch | `OMEGAX_LIVE_ENABLE_HYBRID_LAUNCH=1` | `OMEGAX_ALLOW_MAINNET_HYBRID_LAUNCH=1` |
| Extra admin bootstrap | `OMEGAX_LIVE_ENABLE_ADMIN_BOOTSTRAP=1` | `OMEGAX_ALLOW_MAINNET_ADMIN_BOOTSTRAP=1` |

`npm run protocol:bootstrap:genesis-live -- --plan` must print:

- launch profile id, network, disabled surfaces, and hidden surfaces;
- LP class posture: open classes, 30-day lockup, queue-only redemption, classic SPL-only;
- redemption posture: public request surface and operator-processed queue;
- preferred settlement mint, role map, and no-send status.

## Same-Asset Claim Payouts

Phase 0 keeps claim and obligation settlement same-asset. A claim or obligation
settlement is denominated in the asset mint recorded on that liability, and the
on-chain program does not pay a different fallback token for that liability.

The on-chain program now requires `settle_claim_case` and `settle_obligation`
to include the matching domain vault, domain asset ledger, funding line,
funding-line ledger, plan ledger, optional series ledger, and SPL outflow
accounts for that asset. Settlement fails unless the liability mint, funding
line mint, reserve-domain vault, and reserve ledgers all bind to the same asset.

Mismatched custody or ledger inputs fail closed and cannot leave custody.
Frontend and backend services may surface other reserve assets for operator
rebalancing, but those assets must
be converted or rebalanced into the settlement mint before same-asset claim
settlement.

This makes USDC the preferred Genesis settlement rail while still allowing
approved fallback reserves such as PUSD, USDT, SOL, WBTC, or WETH to remain
visible as reserve inventory. The program does not swap assets, does not mutate
a USDC claim ledger while draining a WBTC vault, and does not treat pending
off-chain reservations as claims-paying reserve until activation/posting rules
have made that true.

## Reservation Visibility

The protocol dapp does not host the consumer Founder reservation payment flow.
Reservation payments are off-chain Squads custody records until activation.
They are not active cover, not LP deposits, and not claims-paying reserve.

Any protocol-facing operator copy must separate:

- accepted reservation products and payment rails;
- pending, activation-pending, refund-requested, and refunded reservation counts;
- Squads custody balances and reservation records;
- posted reserve, premium, and claim ledgers;
- claims-paying reserve impact.

Copy must stay explicit: pending reservations are refundable manual holds. They
do not become protocol reserve until a later activation/posting process books
them through the normal reserve controls.

Production website and oracle-service fallbacks must fail closed if the Founder
reservation campaign cannot be read. They should show a paused or unavailable
campaign instead of implying payments are open.

## Validation

Minimum checks for Phase 0 surface work:

```bash
npm run test:node
npm run verify:public
OMEGAX_E2E_KEEP_ARTIFACTS=1 npm run test:e2e:localnet
npm run protocol:bootstrap:genesis-live -- --plan
```

Strict devnet treasury pen-test is required after program or treasury-flow changes. For frontend/bootstrap-only Phase 0 gating changes, document why it was not rerun.
