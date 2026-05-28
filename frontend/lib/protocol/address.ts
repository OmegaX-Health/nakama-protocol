// SPDX-License-Identifier: AGPL-3.0-or-later

import { TOKEN_PROGRAM_ID } from "@solana/spl-token";
import { PublicKey, type Connection } from "@solana/web3.js";

import { PROTOCOL_PROGRAM_ID } from "../generated/protocol-contract";
import type { PublicKeyish } from "./types";

function configuredProtocolProgramId(): string {
  const runtimeEnv = typeof process !== "undefined" ? process.env : undefined;
  return (
    runtimeEnv?.NEXT_PUBLIC_PROTOCOL_PROGRAM_ID?.trim()
    || runtimeEnv?.PROTOCOL_PROGRAM_ID?.trim()
    || PROTOCOL_PROGRAM_ID
  );
}

const PROGRAM_ID = new PublicKey(configuredProtocolProgramId());

export function getProgramId(): PublicKey {
  return PROGRAM_ID;
}

export function toPublicKey(value: PublicKeyish): PublicKey {
  return value instanceof PublicKey ? value : new PublicKey(value);
}

export function normalizeAddress(value: PublicKeyish): string {
  return toPublicKey(value).toBase58();
}

export function classicTokenProgramId(tokenProgramId?: PublicKeyish | null): PublicKey {
  const candidate = toPublicKey(tokenProgramId ?? TOKEN_PROGRAM_ID);
  if (!candidate.equals(TOKEN_PROGRAM_ID)) {
    throw new Error("OmegaX Protocol v1 supports only the classic SPL Token program.");
  }
  return candidate;
}

export async function accountExists(connection: Connection, address: PublicKeyish): Promise<boolean> {
  const info = await connection.getAccountInfo(toPublicKey(address), "confirmed");
  return info !== null;
}
