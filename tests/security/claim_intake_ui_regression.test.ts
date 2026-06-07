// SPDX-License-Identifier: AGPL-3.0-or-later
//
// Defense regression for the trimmed operator claim-intake UX: member-position
// accounts were retired, so the operator drawer must bind claims directly to a
// claimant wallet and carry the evidence fingerprint into the transaction.

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

test("[PT-04 defense] operator claim drawer uses direct claimant wallet input", () => {
  assert.match(
    drawerSource,
    /const\s+\[claimantAddress,\s*setClaimantAddress\]\s*=\s*useState\(""\)/,
    "operator claim intake must keep an explicit claimant wallet field",
  );
  assert.match(
    drawerSource,
    /claimantAddress:\s*claimantAddress\.trim\(\)/,
    "open-claim transaction must submit the normalized claimant wallet",
  );
  assert.match(
    drawerSource,
    /evidenceRefHashHex:\s*await\s+hashReason\(evidenceRef\)/,
    "open-claim transaction must carry the evidence reference fingerprint",
  );
  assert.doesNotMatch(
    drawerSource,
    /selectedMemberForClaim|claimIntakeClaimantAddress|memberPositionAddress:\s*selected/,
    "operator claim intake must not depend on retired member-position state",
  );
});

test("[PT-04 defense] functional spec reflects direct claimant claim intake", () => {
  assert.match(
    functionalSpec,
    /Claims now bind directly to a claimant wallet/,
    "claim-intake spec must describe the direct claimant-wallet model",
  );
  assert.doesNotMatch(
    functionalSpec,
    /operator flow explicitly allows claimant override|operator flows may explicitly override claimant|selected member position wallet/,
    "claim-intake spec must not preserve stale member-position claimant language",
  );
});
