# IDL

This directory contains checked-in Anchor IDL snapshots for the protocol
program and public adjunct programs.

## Purpose

- make protocol review easier from a fresh clone
- support client and SDK parity checks
- provide a stable public artifact for tooling that consumes the protocol interface

Regenerate it from the repository root with:

```bash
npm run anchor:idl
```

The command copies both checked-in public IDLs:

- `target/idl/omegax_protocol.json` -> `idl/omegax_protocol.json`
- `target/idl/omegax_private_claim_review.json` -> `idl/omegax_private_claim_review.json`

It also refreshes both source-hash files. Do not copy the MagicBlock adjunct
IDL manually; `npm run idl:freshness:check` gates both programs in CI.
