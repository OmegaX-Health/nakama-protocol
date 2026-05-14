# Health Claim Simulation Public Summary

This is the public-safe summary of private OmegaX Health claim-simulation runs used as Genesis Protect evidence.

The detailed simulator, raw case rows, synthetic user profiles, scenario packs, health-agent samples, and devnet sentinel samples stay in `omegax-health`.

## Why This Exists

Protocol reviewers should be able to see that Genesis Protect has meaningful claim-realism testing without exposing the proprietary Health/oracle machinery.

This file is therefore aggregate-only: counts, hashes, run labels, and high-level findings.

## Current Public Evidence Set

| Run | Profile | Cases | Unique synthetic users | Raw size | Public status |
| --- | --- | ---: | ---: | ---: | --- |
| `v5-battle-llm-corpus` | `battle` | 198000 | 198000 | 3525675449 bytes | Current aggregate proof |
| `v4-max-3m` | `max` | 3000000 | 3000000 | 35927770314 bytes | Historical scale proof |

## Current Run

- Generated at: `2026-05-11T06:04:22.513Z`
- Seed: `genesis-protect-acute-claim-sim-v5-llm-corpus`
- Raw JSONL SHA-256: `d77ff58075c6fa8403ba27917720955b8cbe7a7815d71481d37dad67bcd8c17c`
- Raw JSONL status: private Health artifact, not tracked in protocol

Public finding: the current evidence set proves deterministic claim-case breadth and operational stress coverage at `198000` cases without publishing row-level case construction.

## Historical Scale Run

- Generated at: `2026-05-10`
- Seed: `genesis-protect-acute-claim-sim-v4-max`
- Profile: `max`
- Cases: `3000000`
- Unique synthetic users: `3000000`
- Lane counts: `1000000` `ops_realistic`, `1000000` `public_calibrated`, `1000000` `adversarial_stress`
- Raw JSONL SHA-256: `6b2bda58b35471d5186a2f0724ca52f7ddc75eb5fd7bf039519257ddf7bba8c2`
- Raw JSONL status: historical private export, overwritten locally by the later v5 corpus

Public finding: the simulator has already handled multi-million-case deterministic runs, but the raw corpus remains private.

## Public Boundary

Allowed here:

- Run ids
- Seeds
- Timestamps
- Case counts
- Unique synthetic user counts
- Lane counts
- Raw export sizes and hashes
- High-level findings

Not allowed here:

- Raw case rows
- Full synthetic user profiles
- Scenario-pack archetypes
- Detailed medical, payment, evidence, or operator-flow packets
- Health-agent request/response samples
- Devnet sentinel case samples
- Private backend or operator workflow traces

## Disclaimer

Synthetic planning artifact only. This is not real claim history, not external actuarial certification, not underwriting advice, and not legal or regulatory advice.
