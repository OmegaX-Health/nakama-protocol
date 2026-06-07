// SPDX-License-Identifier: AGPL-3.0-or-later

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const componentRoot = join(root, "frontend/components");

const retiredBuilders = [
  "buildAttachClaimEvidenceRefTx",
  "buildAttestClaimCaseTx",
  "buildOpenMemberPositionTx",
  "buildUpdateMemberEligibilityTx",
  "buildCreateLiquidityPoolTx",
  "buildCreateCapitalClassTx",
  "buildUpdateCapitalClassControlsTx",
  "buildDepositIntoCapitalClassTx",
  "buildRequestRedemptionTx",
  "buildProcessRedemptionQueueTx",
  "buildCreateAllocationPositionTx",
  "buildAllocateCapitalTx",
  "buildDeallocateCapitalTx",
  "buildMarkImpairmentTx",
  "buildRegisterOracleTx",
  "buildClaimOracleTx",
];

function componentFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((entry) => {
    const path = join(dir, entry);
    const stat = statSync(path);
    if (stat.isDirectory()) return componentFiles(path);
    return /\.(tsx|ts)$/.test(entry) ? [path] : [];
  });
}

test("public frontend components do not mount retired protocol transaction builders", () => {
  const offenders: string[] = [];
  for (const file of componentFiles(componentRoot)) {
    const source = readFileSync(file, "utf8");
    for (const builder of retiredBuilders) {
      if (source.includes(builder)) {
        offenders.push(`${file.replace(`${root}/`, "")}: ${builder}`);
      }
    }
  }
  assert.deepEqual(offenders, []);
});
