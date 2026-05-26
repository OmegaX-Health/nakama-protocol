// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Defense regression for the operator claim-intake UX: the chain requires
// args.claimant == member_position.wallet for both member and operator submits,
// so the operator drawer must derive claimant from the selected member position
// instead of accepting an arbitrary signer/operator override.

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const drawerSource = readFileSync(
  join(root, "frontend/components/plan-operator-drawer.tsx"),
  "utf8",
);
const functionalSpec = readFileSync(
  join(root, "docs/architecture/protocol-console-functional-spec.md"),
  "utf8",
);

test("[PT-04 defense] operator claim drawer derives claimant from selected member wallet", () => {
  assert.match(
    drawerSource,
    /const\s+claimIntakeClaimantAddress\s*=\s*selectedMemberForClaim\?\.wallet\s*\?\?\s*""/,
    "operator claim intake must derive claimant from the selected member wallet",
  );
  assert.match(
    drawerSource,
    /claimantAddress:\s*claimIntakeClaimantAddress/,
    "open-claim transaction must submit the derived member-wallet claimant",
  );
  assert.doesNotMatch(
    drawerSource,
    /setClaimant|value=\{claimant\}|claimantAddress:\s*claimant/,
    "operator claim intake must not keep a free-form claimant override",
  );
});

test("[PT-04 defense] functional spec forbids operator claimant override", () => {
  assert.match(
    functionalSpec,
    /operator flows must not override claimant/,
    "claim-intake spec must forbid operator claimant override",
  );
  assert.doesNotMatch(
    functionalSpec,
    /operator flow explicitly allows claimant override|operator flows may explicitly override claimant/,
    "claim-intake spec must not preserve stale operator override language",
  );
});
