import assert from "node:assert/strict";
import test from "node:test";

import overviewMetricsModule from "../frontend/lib/overview-metrics.ts";
import workbenchModule from "../frontend/lib/workbench.ts";

const { EMPTY_OVERVIEW_STATS_SOURCE } =
  overviewMetricsModule as typeof import("../frontend/lib/overview-metrics.ts");
const { buildAuditTrail } = workbenchModule as typeof import("../frontend/lib/workbench.ts");

test("capital field log uses live empty source instead of fixture fallback", () => {
  // Regression: ISSUE-001 - custom RPC failure leaked demo capital activity.
  // Found by /qa on 2026-05-09.
  // Report: .gstack/qa-reports/qa-report-localhost-3001-2026-05-09.md
  const auditTrail = buildAuditTrail({
    section: "capital",
    source: EMPTY_OVERVIEW_STATS_SOURCE,
  });

  assert.equal(
    auditTrail[0]?.detail,
    "0 redemption sources remain across 0 pools using queued redemptions.",
  );
  assert.equal(auditTrail.some((item) => item.detail.includes("Omega Health Income Pool")), false);
  assert.equal(auditTrail.some((item) => item.detail.includes("fixture set")), false);
});
