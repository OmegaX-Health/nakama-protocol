import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const protocolWorkbenchShell = readFileSync("frontend/components/protocol-workbench-shell.tsx", "utf8");
const workbenchModel = readFileSync("frontend/lib/workbench.ts", "utf8");

test("schemas route uses fullscreen workbench chrome", () => {
  // Regression: ISSUE-001 - /schemas kept the default inner-scroll shell, so the footer consumed viewport space and hid the lower registry rail.
  // Found by /qa on 2026-05-11.
  // Report: .gstack/qa-reports/qa-report-127-0-0-1-3001-2026-05-11.md
  assert.match(protocolWorkbenchShell, /"\/schemas"/);
});

test("primary workbench navigation exposes schemas and docs", () => {
  assert.match(workbenchModel, /href: "\/schemas", label: "Schemas"/);
  assert.match(protocolWorkbenchShell, /className="protocol-topbar-tab protocol-topbar-tab-external"/);
  assert.match(protocolWorkbenchShell, />\s*Docs\s*</);
});

test("compact workbench navigation closes on outside click and Escape", () => {
  assert.match(protocolWorkbenchShell, /const mobileNavButtonRef = useRef<HTMLButtonElement \| null>\(null\)/);
  assert.match(protocolWorkbenchShell, /const mobileNavRef = useRef<HTMLElement \| null>\(null\)/);
  assert.match(protocolWorkbenchShell, /document\.addEventListener\("pointerdown", handlePointerDown\)/);
  assert.match(protocolWorkbenchShell, /!mobileNavRef\.current\.contains\(target\)/);
  assert.match(protocolWorkbenchShell, /!mobileNavButtonRef\.current\?\.contains\(target\)/);
  assert.match(protocolWorkbenchShell, /event\.key === "Escape"[\s\S]*setIsMobileNavOpen\(false\)/);
});
