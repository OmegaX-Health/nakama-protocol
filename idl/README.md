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

The MagicBlock private claim-room adjunct IDL is emitted by `anchor build` as
`target/idl/omegax_private_claim_review.json`; copy it into this directory
after adjunct surface changes and refresh
`omegax_private_claim_review.source-hash`.
