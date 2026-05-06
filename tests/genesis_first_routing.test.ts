import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

test("root route redirects into the health capital markets overview", () => {
  const source = readFileSync(new URL("../frontend/app/page.tsx", import.meta.url), "utf8");

  assert.match(source, /redirect\(["']\/overview["']\)/);
});
