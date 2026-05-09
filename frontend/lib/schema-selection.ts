// SPDX-License-Identifier: AGPL-3.0-or-later

export type SchemaSelectionSeries = {
  termsVersion: string;
  comparabilityHashHex?: string;
  comparabilityKey: string;
};

export type SchemaSelectionSchema = {
  address: string;
} | null;

export function schemaKeyForSeries(series: SchemaSelectionSeries): string {
  return `${series.termsVersion}:${series.comparabilityHashHex ?? series.comparabilityKey}`;
}

export function schemaParamForSeriesSelection(
  series: SchemaSelectionSeries,
  matchingSchema: SchemaSelectionSchema,
  liveSchemaCount: number,
): string | null {
  if (matchingSchema) return matchingSchema.address;
  return liveSchemaCount === 0 ? schemaKeyForSeries(series) : null;
}
