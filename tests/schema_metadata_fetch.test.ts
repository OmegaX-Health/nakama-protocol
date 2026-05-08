import assert from "node:assert/strict";
import test from "node:test";

import schemaMetadataModule from "../frontend/lib/schema-metadata.ts";

const { fetchSchemaMetadata } =
  schemaMetadataModule as typeof import("../frontend/lib/schema-metadata.ts");

test("browser schema metadata fetch uses the same-origin proxy response", async () => {
  const globals = globalThis as typeof globalThis & { window?: unknown };
  const previousWindow = globals.window;
  const previousFetch = globalThis.fetch;
  const calls: string[] = [];

  Object.defineProperty(globalThis, "window", { configurable: true, value: {} });
  globalThis.fetch = async (input) => {
    calls.push(String(input));
    return new Response(JSON.stringify({
      metadata: { specVersion: "omegax.schema", outcomes: [] },
      error: null,
    }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  };

  try {
    const result = await fetchSchemaMetadata("https://protocol.omegax.health/schemas/standard-health-outcomes-v1.json");

    assert.deepEqual(result, {
      metadata: { specVersion: "omegax.schema", outcomes: [] },
      error: null,
    });
    assert.deepEqual(calls, [
      "/api/schema-metadata?uri=https%3A%2F%2Fprotocol.omegax.health%2Fschemas%2Fstandard-health-outcomes-v1.json",
    ]);
  } finally {
    globalThis.fetch = previousFetch;
    if (previousWindow === undefined) {
      delete globals.window;
    } else {
      Object.defineProperty(globalThis, "window", { configurable: true, value: previousWindow });
    }
  }
});

test("server schema metadata fetch rejects non-allowlisted hosts before fetch", async () => {
  const previousFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    throw new Error("fetch should not run for non-allowlisted metadata hosts");
  };

  try {
    const result = await fetchSchemaMetadata("https://169.254.169.254/latest/meta-data");

    assert.equal(calls, 0);
    assert.deepEqual(result, {
      metadata: null,
      error: {
        code: "unsupported_host",
        message: "Server-side schema metadata fetches are limited to bundled OmegaX schemas.",
      },
    });
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("server schema metadata fetch serves bundled OmegaX schemas without external fetch", async () => {
  const previousFetch = globalThis.fetch;
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    throw new Error("fetch should not run for bundled schema metadata");
  };

  try {
    const result = await fetchSchemaMetadata("https://protocol.omegax.health/schemas/genesis-protect-acute-claim-v1.json");

    assert.equal(calls, 0);
    assert.equal(result.error, null);
    assert.equal(typeof result.metadata, "object");
  } finally {
    globalThis.fetch = previousFetch;
  }
});
