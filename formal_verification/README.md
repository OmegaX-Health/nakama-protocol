# Formal Verification

This directory contains maintainer verification lanes for OmegaX Protocol.

## QEDGen

The brownfield QEDGen spec lives at [`../omegax_protocol.qedspec`](../omegax_protocol.qedspec).
The local project config and accepted modeling notes live under [`../.qed/`](../.qed/).

```bash
npm run qedgen:check
npm run qedgen:codegen
npm run qedgen:verify
npm run qedgen:reconcile
```

`npm run qedgen:codegen` writes the Anchor verification model to
[`anchor_model/`](./anchor_model/), the Lean proof surface to
[`Spec.lean`](./Spec.lean), and generated Kani/proptest harnesses to
[`anchor_model/tests/`](./anchor_model/tests/).

Treat this lane as coverage and spec-hygiene evidence unless a specific
property has committed proof bodies. Generated theorem stubs, missing Lean
obligations, and placeholder effects in generated models are not production
proof coverage by themselves.

The currently accepted warning is `missing_cpi_for_token_context` on
`create_domain_asset_vault`. That handler accepts `token_program` for token
account initialization, not for a token transfer. The modeling gap is tracked in
[`../.qed/plan/findings/001-domain-vault-init-token-program.md`](../.qed/plan/findings/001-domain-vault-init-token-program.md)
and [`../.qed/plan/gaps.md`](../.qed/plan/gaps.md).

## Certora Solana

The optional Certora Solana lane lives in [`certora/`](./certora/). It is a
manual maintainer lane for narrow symbolic checks against high-value
kernel/scalar properties, not an external audit claim.

```bash
npm run certora:solana:check
```
