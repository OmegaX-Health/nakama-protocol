# Nomad Protect Curve PoC

## Scope

This folder is an experimental public-safe actuarial/product model for future curve-priced protection and open risk backing. It does not replace the approved Genesis Protect Acute fixed-SKU launch model.

## Rules

- Keep the experiment public-safe and clearly labeled as exploratory.
- Do not merge future curve assumptions into Genesis Protect Acute launch doctrine without an explicit product decision.
- Do not import private Health claim-simulation rows, scenario-pack internals, local `.superstack/` diligence, or private market research into tracked artifacts.
- Keep member quote-curve mechanics separate from risk-backer capital mechanics.
- Avoid presenting prediction-market/backer concepts as regulatory, legal, or external actuarial approval.

## Validation

- Run `npm run nomad:curve:poc` after changing assumptions, product logic, or generated reports.
- Run `node --import tsx --test tests/nomad_curve_actuarial_poc.test.ts` for focused test coverage.
- Run `git diff --check` before committing.
- Protocol commits require DCO sign-off.
