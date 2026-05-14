# Genesis Protect Analysis Hub

This folder is the public-safe evidence room for Genesis Protect pricing, reserve, claim-fixture, and risk-model analysis.

The protocol repo should show enough for builders, reviewers, and investors to understand that Genesis Protect has a working pricing, reserve, and claim-flow model. It should not expose proprietary Health/oracle simulation machinery.

## Executive Summary

Genesis Protect analysis is intentionally split:

- `omegax-protocol` shows public-safe proof: assumptions, launch gates, generated workbook outputs, curated fixtures, and aggregate simulation evidence.
- `omegax-health` owns proprietary claim realism: synthetic-user generation, scenario packs, health-agent samples, devnet sentinel samples, and raw JSONL exports.
- The public protocol story should be strong, but not leaky. Show the system works through aggregate evidence and reproducible protocol workbooks.

## Canonical Public Artifacts

| Area | Location | Regenerate | Public status |
| --- | --- | --- | --- |
| Fixed SKU launch gates | `../genesis-protect-acute-actuarial-review/` | `npm run genesis:actuarial:review` | Public-safe |
| Curve and market-structure PoC | `../nomad-protect-curve-poc/` | `npm run nomad:curve:poc` | Public-safe experimental |
| Public claim fixtures | `../genesis-protect-acute-claims/` | Manual fixture curation | Public-safe examples |
| Health claim-simulator summary | `./health-claim-simulation-public-summary.json` and `.md` | Export aggregate-only from Health | Public-safe aggregate |

## Evidence Model

| Layer | Public evidence | Private boundary |
| --- | --- | --- |
| Product truth | SKU prices, caps, waiting periods, reserve lanes, funding lines, launch gates | None, this is protocol-owned public truth |
| Actuarial launch gate | Deterministic p99.5 workbook and scenario matrix | Not an external actuarial certification |
| Claim fixtures | Curated 32-case fixture set for docs, console testing, and operator training | Not real claims and not canonical devnet state |
| Health simulation proof | Aggregate counts, hashes, run metadata, and high-level findings | No raw case rows, synthetic users, scenario packs, or agent samples |
| Future products | Curve and market-structure PoC | Not Genesis v1 pricing or a regulatory opinion |

## Public-Safe Story

1. Genesis v1 has public SKU truth and reserve gates in protocol metadata.
2. The fixed-SKU workbook validates that truth before writing generated outputs.
3. Curated public fixtures show what a claim packet looks like without exposing the proprietary generator.
4. Health aggregate summaries prove the private simulator can run at meaningful scale.
5. Curve PoCs show future product directions without changing the Genesis v1 launch gate.

## What Belongs Here

- Public-safe assumptions and scenario matrices.
- Generated workbook outputs and human-readable memos.
- Aggregate Health simulation summaries with counts, hashes, and high-level findings.
- Curated example claim fixtures that do not reveal internal synthetic-user generation logic.
- Clear disclaimers that these are planning artifacts, not external actuarial, legal, regulatory, or underwriting opinions.
- Human-readable summaries that a public reviewer can understand without private repo access.

## What Does Not Belong Here

- Raw Health `.cases.jsonl` exports.
- Full synthetic user profiles.
- Health scenario-pack archetypes or adversarial generation details.
- Health-agent samples, devnet sentinel samples, private operator workflow traces, or private backend endpoints.
- Machine-specific local paths, secrets, private key material, or production control-plane notes.

## Commands

From the protocol repo root:

```sh
npm run genesis:actuarial:review
npm run nomad:curve:poc
```

The fixed SKU workbook validates against public Genesis metadata before writing outputs. The curve PoC is explicitly experimental and does not replace Genesis Protect Acute v1 pricing.

## Current Read Order

1. `../genesis-protect-acute-actuarial-review/README.md`
2. `../genesis-protect-acute-actuarial-review/review-memo.md`
3. `../genesis-protect-acute-claims/README.md`
4. `health-claim-simulation-public-summary.md`
5. `health-claim-simulation-public-summary.json`
6. `../nomad-protect-curve-poc/README.md`
7. `../nomad-protect-curve-poc/hybrid-model-report.md`

## Update Workflow

1. Update public protocol assumptions or fixtures when protocol truth changes.
2. Regenerate public workbooks with the commands above.
3. If Health runs a new private simulation, copy only aggregate fields into this folder.
4. Run a leak check before committing:

```sh
rg -n 'synthetic[U]ser|healthAgent[R]equest|scenarioPack[S]ource|coverageClaims/syntheti[c]|evidence[I]tems|care[E]pisode|synthetic-user[-]' examples/genesis-protect-analysis examples/README.md
```

5. Keep protocol commits DCO-signed.

## Review Checklist

- The public story is understandable without private Health access.
- The Health proof is aggregate-only.
- Genesis v1 fixed-SKU analysis is not mixed with future curve experiments.
- Every artifact has a clear status: public-safe, public-safe experimental, curated fixture, or private aggregate.
- Disclaimers stay explicit and plain.

## Local-Only Internal Diligence

More detailed internal diligence may exist locally under `.superstack/`. That folder is ignored and should not be pushed unless a specific artifact is rewritten into public-safe form first.
