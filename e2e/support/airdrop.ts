// SPDX-License-Identifier: AGPL-3.0-or-later

import {
  Connection,
  Keypair,
  LAMPORTS_PER_SOL,
  PublicKey,
  SystemProgram,
  Transaction,
  sendAndConfirmTransaction,
} from "@solana/web3.js";

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function loadLocalnetFunder(): Keypair | null {
  const raw = process.env.OMEGAX_E2E_ORIGINAL_GOVERNANCE_SECRET_KEY_JSON?.trim();
  if (!raw) return null;
  const parsed = JSON.parse(raw) as number[];
  return Keypair.fromSecretKey(Uint8Array.from(parsed));
}

async function transferFromLocalnetFunder(
  connection: Connection,
  funder: Keypair,
  recipient: PublicKey,
  lamports: number,
): Promise<void> {
  if (recipient.equals(funder.publicKey)) {
    const balance = await connection.getBalance(recipient, "confirmed");
    if (balance >= lamports) return;
    throw new Error(`Localnet funder ${recipient.toBase58()} has insufficient genesis SOL`);
  }

  const tx = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: funder.publicKey,
      toPubkey: recipient,
      lamports,
    }),
  );
  await sendAndConfirmTransaction(connection, tx, [funder], { commitment: "confirmed" });
}

export async function requestConfirmedAirdrop(
  connection: Connection,
  recipient: PublicKey,
  lamports = 5 * LAMPORTS_PER_SOL,
  attempts = 20,
): Promise<void> {
  const localnetFunder = loadLocalnetFunder();
  if (localnetFunder) {
    await transferFromLocalnetFunder(connection, localnetFunder, recipient, lamports);
    return;
  }

  let lastError: unknown;
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const latest = await connection.getLatestBlockhash("confirmed");
      const signature = await connection.requestAirdrop(recipient, lamports);
      await connection.confirmTransaction({ signature, ...latest }, "confirmed");
      return;
    } catch (error) {
      lastError = error;
      await sleep(Math.min(1_000, 150 * (attempt + 1)));
    }
  }
  throw lastError instanceof Error
    ? lastError
    : new Error(`Airdrop failed for ${recipient.toBase58()}`);
}

export async function requestConfirmedAirdrops(
  connection: Connection,
  recipients: PublicKey[],
  lamports = 5 * LAMPORTS_PER_SOL,
  batchSize = 1,
): Promise<void> {
  for (let index = 0; index < recipients.length; index += batchSize) {
    const batch = recipients.slice(index, index + batchSize);
    await Promise.all(batch.map((recipient) => requestConfirmedAirdrop(connection, recipient, lamports)));
  }
}
