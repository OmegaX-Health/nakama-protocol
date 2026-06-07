<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# Anchor to Quasar Migration

This note tracks the public protocol program migration from Anchor to Quasar.
Quasar documentation: <https://quasar-lang.com/docs>.

## Current Migration State

The branch is intentionally staged. The default build path still compiles the
existing Anchor program while the Quasar feature path exposes the remaining
source-port work.

Completed setup:

- Root `Quasar.toml` declares the protocol project for the Quasar CLI.
- `rust-toolchain.toml` and CI Rust pins are bumped to `1.89.0`, which is the
  current compiler floor required by the Quasar dependency graph.
- `programs/omegax_protocol/src/platform.rs` centralizes framework imports so
  implementation modules no longer import Anchor preludes directly.
- `programs/omegax_protocol/src/quasar_discriminators.rs` preserves the current
  checked-in IDL instruction, account, and event discriminator bytes.
- `npm run quasar:discriminators` regenerates those constants from
  `idl/omegax_protocol.json`.
- `tests/quasar_discriminators.test.ts` verifies instruction, account, and
  event discriminator parity against the checked-in IDL.
- Quasar account definitions now have explicit account discriminators. Dynamic
  account-state structs are split from the Anchor Borsh definitions behind
  `cfg(feature = "quasar")`, with fixed fields first and bounded Quasar
  `String`/`Vec` fields at the tail so the zero-copy account macro accepts the
  layout.
- The Quasar platform seam aliases `Pubkey` to Quasar `Address` for account
  state during the staged port, and state accounts expose a Quasar `INIT_SPACE`
  compatibility constant for existing init-site expressions.
- Anchor-only error messages, compatibility macros, instruction-arg derives,
  and `#[max_len]` helper attributes are gated off the Quasar path so the
  remaining Quasar compile output focuses on facade, context, and POD layout
  work.
- The root instruction facade is split by feature flag. The Anchor path keeps
  forwarding to the existing handlers, while the Quasar path declares the
  current 21 public instructions with literal Quasar discriminator bytes and
  forwards the active canonical handlers.
- Anchor-only generated `__client_accounts_*` reexports are gated off the
  Quasar path, and the Quasar platform seam now preserves the existing
  `Result<T>` spelling as `core::result::Result<T, ProgramError>`.
- Dynamic account data now flows through feature-gated `*AccountData<'info>`
  aliases. Anchor resolves those aliases back to the existing Borsh account
  structs, while Quasar resolves them to the borrowed dynamic account views,
  letting shared helpers and most account wrappers carry the required lifetime
  without changing default-path behavior.
- Claim lifecycle account contexts now have the same feature-gated Quasar
  wrapper shape across intake, recipient authorization, adjudication, and direct
  settlement. Evidence attachment and oracle attestation are no longer part of
  the base protocol surface.
- Funding-obligation account contexts now use the same Quasar reference-wrapper
  shape across funding-line opening, sponsor and premium inflows, reserve
  capital, obligations, reserve release, and settlement.
- Plan/membership and reserve-custody account contexts now also use
  feature-gated Quasar reference wrappers and account-data aliases. The
  account-context dynamic lifetime bucket is cleared across the current public
  surface.

The active Quasar compile inventory is:

```bash
npm run quasar:check
```

As of the latest migration checkpoint, that command compiles the
`omegax_protocol` library under the Quasar feature path. The Quasar surface is
therefore a release-chain input, not a fail-closed placeholder, and
`npm run quasar:check` is part of the public release gate. Remaining work is
runtime parity and adversarial coverage for Quasar money paths, especially
claims, reserve capital returns, settlement, and pause behavior.

## Port Order

1. Add Quasar runtime parity tests for the active money-path handlers: claims,
   obligations, reserve-capital return, and pause behavior.
2. Rewrite any remaining `#[derive(Accounts)]` contexts by domain module, preserving PDA
   seeds, constraints, and writability exactly. Start with reserve custody,
   plans, funding, and claims because they exercise init, update,
   token-custody, and settlement paths.
3. Convert account state structs to Quasar account layouts with explicit
   account discriminators from `quasar_discriminators::account`. Preserve the
   public wire shape where possible; any layout break requires regenerated IDL,
   contract artifacts, frontend builders, and release docs.
4. Convert instruction args from Anchor-serialized structs to Quasar instruction
   parameters. For dynamic strings, use Quasar's Borsh-compatible `u32` length
   prefix unless a public surface change is intentional.
5. Convert events to Quasar event discriminators or replace unsupported event
   shapes with explicit primitive-only public events.
6. Replace Anchor/Anchor SPL CPI calls with Quasar and `quasar-spl` calls.
7. Regenerate IDL and protocol contract artifacts with the documented Quasar
   flow once the Quasar program compiles.

## Optimization Rules

- Prefer Quasar's zero-copy account access for hot read/update paths after the
  account layout is ported.
- Keep checked arithmetic in reserve, fee, and claim settlement kernels; do not
  trade accounting safety for compute-unit reductions.
- Preserve discriminator bytes during the migration so external builders can be
  updated deliberately rather than by surprise.
- Use `quasar profile` after the Quasar build succeeds to compare compute-unit
  changes against the Anchor baseline.
