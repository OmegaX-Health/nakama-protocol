// SPDX-License-Identifier: AGPL-3.0-or-later

import test from "node:test";
import assert from "node:assert/strict";

import { PublicKey } from "@solana/web3.js";

import contractModule from "../frontend/lib/generated/protocol-contract.ts";
import protocolModule from "../frontend/lib/protocol.ts";

const { PROTOCOL_INSTRUCTION_DISCRIMINATORS } = contractModule as typeof import(
  "../frontend/lib/generated/protocol-contract.ts"
);
const {
  buildAcceptGovernanceAuthorityTx,
  buildCancelGovernanceAuthorityTransferTx,
  buildRotateGovernanceAuthorityTx,
  deriveProtocolGovernancePda,
  getProgramId,
} = protocolModule as typeof import("../frontend/lib/protocol.ts");

const RECENT_BLOCKHASH = "11111111111111111111111111111111";
const CURRENT_AUTHORITY = new PublicKey("So11111111111111111111111111111111111111112");
const NEXT_AUTHORITY = new PublicKey("oxhocTdPyENqy9RS13iaq2upoNAovMJHu9PMaBxrK8h");

function discriminatorForName(name: string): Uint8Array {
  const discriminator = (PROTOCOL_INSTRUCTION_DISCRIMINATORS as Record<string, Uint8Array>)[name];
  assert.ok(discriminator, `expected discriminator for ${name}`);
  return discriminator;
}

function assertProtocolIxShape(
  tx: {
    feePayer?: PublicKey;
    instructions: ReadonlyArray<{
      programId: PublicKey;
      data: Buffer | Uint8Array;
      keys: ReadonlyArray<{ pubkey: PublicKey; isSigner: boolean; isWritable: boolean }>;
    }>;
  },
  expectedName: string,
  expectedSigner: PublicKey,
) {
  assert.equal(tx.instructions.length, 1, `${expectedName} should produce one instruction`);
  const ix = tx.instructions[0]!;
  assert.equal(ix.programId.toBase58(), getProgramId().toBase58());
  assert.deepEqual(Array.from(ix.data.subarray(0, 8)), Array.from(discriminatorForName(expectedName)));
  assert.equal(ix.keys[0]!.pubkey.toBase58(), expectedSigner.toBase58());
  assert.equal(ix.keys[0]!.isSigner, true);
  assert.equal(ix.keys[1]!.pubkey.toBase58(), deriveProtocolGovernancePda().toBase58());
  assert.equal(ix.keys[1]!.isWritable, true);
  return ix;
}

test("governance authority builder now proposes transfer without changing signer", () => {
  const tx = buildRotateGovernanceAuthorityTx({
    governanceAuthority: CURRENT_AUTHORITY,
    newAuthority: NEXT_AUTHORITY,
    recentBlockhash: RECENT_BLOCKHASH,
  });

  const ix = assertProtocolIxShape(tx, "rotate_protocol_governance_authority", CURRENT_AUTHORITY);
  assert.equal(ix.keys.length, 2);
});

test("governance transfer accept and cancel builders expose the two-step surface", () => {
  const acceptTx = buildAcceptGovernanceAuthorityTx({
    pendingAuthority: NEXT_AUTHORITY,
    recentBlockhash: RECENT_BLOCKHASH,
  });
  const acceptIx = assertProtocolIxShape(acceptTx, "accept_protocol_governance_authority", NEXT_AUTHORITY);
  assert.equal(acceptIx.keys.length, 2);

  const cancelTx = buildCancelGovernanceAuthorityTransferTx({
    governanceAuthority: CURRENT_AUTHORITY,
    recentBlockhash: RECENT_BLOCKHASH,
  });
  const cancelIx = assertProtocolIxShape(
    cancelTx,
    "cancel_protocol_governance_authority_transfer",
    CURRENT_AUTHORITY,
  );
  assert.equal(cancelIx.keys.length, 2);
});
