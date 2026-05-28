// SPDX-License-Identifier: AGPL-3.0-or-later

import { MAX_ID_SEED_BYTES } from "./constants";

export const TEXT_ENCODER = new TextEncoder();
export const ZERO_HASH_HEX = "00".repeat(32);

export function utf8ByteLength(value: string): number {
  return TEXT_ENCODER.encode(value).length;
}

export function isSeedIdSafe(value: string): boolean {
  const length = utf8ByteLength(value);
  return length > 0 && length <= MAX_ID_SEED_BYTES;
}

export function assertSeedId(value: string, label = "seed id"): void {
  if (!isSeedIdSafe(value)) {
    throw new Error(`${label} must be 1..${MAX_ID_SEED_BYTES} UTF-8 bytes.`);
  }
}

export function bytesToHex(value: unknown): string {
  if (value instanceof Uint8Array) {
    return Array.from(value, (byte) => byte.toString(16).padStart(2, "0")).join("");
  }
  if (Array.isArray(value)) {
    return Array.from(value, (byte) => Number(byte).toString(16).padStart(2, "0")).join("");
  }
  return "";
}

export function normalizeHex32(value: string): string {
  const normalized = value.trim().toLowerCase().replace(/^0x/, "");
  if (!/^[0-9a-f]{64}$/.test(normalized)) {
    throw new Error("Expected a 32-byte hex string.");
  }
  return normalized;
}

export function normalizeOptionalHex32(value?: string | null): string {
  const trimmed = value?.trim();
  if (!trimmed) return ZERO_HASH_HEX;
  return normalizeHex32(trimmed);
}

export function hexToFixedBytes(value: string, size: number): Uint8Array {
  const normalized = value.trim().toLowerCase().replace(/^0x/, "");
  const expectedLength = size * 2;
  if (!new RegExp(`^[0-9a-f]{${expectedLength}}$`).test(normalized)) {
    throw new Error(`Expected a ${size}-byte hex string.`);
  }
  const bytes = new Uint8Array(size);
  for (let index = 0; index < size; index += 1) {
    bytes[index] = Number.parseInt(normalized.slice(index * 2, index * 2 + 2), 16);
  }
  return bytes;
}

export async function hashStringTo32Hex(value: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", TEXT_ENCODER.encode(value));
  return bytesToHex(new Uint8Array(digest));
}
