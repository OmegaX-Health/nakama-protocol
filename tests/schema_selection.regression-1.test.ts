import assert from "node:assert/strict";
import test from "node:test";

import schemaSelectionModule from "../frontend/lib/schema-selection.ts";

const { schemaParamForSeriesSelection } =
  schemaSelectionModule as typeof import("../frontend/lib/schema-selection.ts");

const SERIES_WITH_UNRESOLVED_LIVE_SCHEMA = {
  termsVersion: "",
  comparabilityHashHex: "a4259e0c49b3aa53ee6b376e40afda60f7c47f2e9449738985ffb9898afc92f9",
  comparabilityKey: "catastrophic-protection-2026",
};

test("schemas route does not write invalid fallback schema params when live schemas exist", () => {
  // Regression: ISSUE-003 - /schemas opened on a schema=:hash URL that immediately rendered "Schema not found".
  // Found by /qa on 2026-05-09.
  // Report: .gstack/qa-reports/qa-report-localhost-3001-2026-05-09.md
  assert.equal(
    schemaParamForSeriesSelection(SERIES_WITH_UNRESOLVED_LIVE_SCHEMA, null, 2),
    null,
  );
});

test("schemas route keeps fallback schema params for series-only snapshots", () => {
  assert.equal(
    schemaParamForSeriesSelection(SERIES_WITH_UNRESOLVED_LIVE_SCHEMA, null, 0),
    ":a4259e0c49b3aa53ee6b376e40afda60f7c47f2e9449738985ffb9898afc92f9",
  );
});
