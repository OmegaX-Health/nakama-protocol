// SPDX-License-Identifier: AGPL-3.0-or-later

"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useConnection } from "@solana/wallet-adapter-react";

import { ProtocolDetailDisclosure } from "@/components/protocol-detail-disclosure";
import { listPoolRules, listSchemas, type RuleSummary, type SchemaSummary } from "@/lib/protocol";
import { formatRpcError } from "@/lib/rpc-errors";

type PoolSchemasPanelProps = {
  poolAddress: string;
  onRefresh?: () => void;
};

function shortAddress(value: string): string {
  if (!value || value.length < 12) return value || "n/a";
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
}

export function PoolSchemasPanel({ poolAddress, onRefresh }: PoolSchemasPanelProps) {
  const { connection } = useConnection();
  const [schemas, setSchemas] = useState<SchemaSummary[]>([]);
  const [rules, setRules] = useState<RuleSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [schemaSearch, setSchemaSearch] = useState("");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [nextSchemas, nextRules] = await Promise.all([
        listSchemas({ connection, verifiedOnly: false }),
        listPoolRules({ connection, poolAddress, enabledOnly: false }),
      ]);
      setSchemas(nextSchemas);
      setRules(nextRules);
      onRefresh?.();
    } catch (cause) {
      setError(
        formatRpcError(cause, {
          fallback: "Failed to load schema policy state.",
          rpcEndpoint: connection.rpcEndpoint,
        }),
      );
    } finally {
      setLoading(false);
    }
  }, [connection, onRefresh, poolAddress]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const filteredSchemas = useMemo(() => {
    const query = schemaSearch.trim().toLowerCase();
    if (!query) return schemas;
    return schemas.filter((schema) =>
      [
        schema.schemaKey,
        schema.schemaKeyHashHex,
        schema.schemaHashHex,
        schema.metadataUri,
      ].some((value) => value.toLowerCase().includes(query)),
    );
  }, [schemaSearch, schemas]);

  return (
    <div className="space-y-4">
      <section className="surface-card-soft space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <p className="metric-label">Schema policy</p>
            <p className="field-help">
              Schema definitions are now off-chain metadata; on-chain attestations bind to oracle-supported schema hashes.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button type="button" className="secondary-button" onClick={() => void refresh()} disabled={loading}>
              {loading ? "Refreshing..." : "Refresh"}
            </button>
            <Link href="/schemas" className="secondary-button inline-flex">
              Open schema workspace
            </Link>
          </div>
        </div>
        {error ? <p className="field-error">{error}</p> : null}
      </section>

      <section className="surface-card-soft space-y-3">
        <div>
          <p className="metric-label">Current pool schema state</p>
          <p className="field-help">{rules.length} pool rules mapped across {schemas.length} known on-chain schemas.</p>
        </div>
        <div className="grid gap-3 md:grid-cols-3">
          <div className="metric-card">
            <p className="metric-label">On-chain schemas</p>
            <p className="metric-value">{schemas.length}</p>
          </div>
          <div className="metric-card">
            <p className="metric-label">Pool rules</p>
            <p className="metric-value">{rules.length}</p>
          </div>
          <div className="metric-card">
            <p className="metric-label">Registry mode</p>
            <p className="metric-value">Off-chain</p>
          </div>
        </div>
      </section>

      <section className="surface-card-soft space-y-3">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="metric-label">Known schema hashes</p>
            <p className="field-help">These rows come from live protocol state; new deployments should expect zero registry accounts.</p>
          </div>
          <input
            className="field-input max-w-xs"
            value={schemaSearch}
            onChange={(event) => setSchemaSearch(event.target.value)}
            placeholder="Search schema hashes"
          />
        </div>
        <div className="space-y-2">
          {filteredSchemas.length === 0 ? (
            <p className="field-help">No on-chain schema registry accounts are present.</p>
          ) : (
            filteredSchemas.map((schema) => (
              <article key={schema.address} className="rounded-md border border-[var(--border)] bg-[var(--surface)] p-3">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <p className="font-semibold text-[var(--foreground)]">{schema.schemaKey || shortAddress(schema.address)}</p>
                    <p className="text-xs text-[var(--muted-foreground)] break-all">{schema.schemaKeyHashHex}</p>
                  </div>
                  <span className="plans-badge plans-badge-neutral">Legacy</span>
                </div>
                <ProtocolDetailDisclosure
                  title="Metadata"
                >
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="metric-label">Address</span>
                      <p className="break-all text-[var(--foreground)]">{schema.address}</p>
                    </div>
                    <div>
                      <span className="metric-label">Schema hash</span>
                      <p className="break-all text-[var(--foreground)]">{schema.schemaHashHex}</p>
                    </div>
                    <div>
                      <span className="metric-label">Metadata URI</span>
                      <p className="break-all text-[var(--foreground)]">{schema.metadataUri || "n/a"}</p>
                    </div>
                  </div>
                </ProtocolDetailDisclosure>
              </article>
            ))
          )}
        </div>
      </section>

      <section className="surface-card-soft space-y-3">
        <div>
          <p className="metric-label">Pool rule references</p>
          <p className="field-help">Rules can still reference schema hashes; the schema account itself is no longer required.</p>
        </div>
        <div className="space-y-2">
          {rules.length === 0 ? (
            <p className="field-help">No pool rules reference this pool yet.</p>
          ) : (
            rules.map((rule) => (
              <article key={rule.address} className="rounded-md border border-[var(--border)] bg-[var(--surface)] p-3">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <p className="font-semibold text-[var(--foreground)]">{rule.ruleId || shortAddress(rule.address)}</p>
                    <p className="text-xs text-[var(--muted-foreground)] break-all">{rule.schemaKeyHashHex}</p>
                  </div>
                  <Link className="secondary-button inline-flex" href={`/schemas?rule=${encodeURIComponent(rule.address)}`}>
                    Open
                  </Link>
                </div>
              </article>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
