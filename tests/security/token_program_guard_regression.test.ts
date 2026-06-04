// SPDX-License-Identifier: AGPL-3.0-or-later
//
// CSO-2026-04-29 regression: the public builders should not construct
// Token-2022 custody transactions for the v1 protocol surface.

import test from "node:test";
import assert from "node:assert/strict";

import { SystemProgram } from "@solana/web3.js";

import fixturesModule from "../../frontend/lib/devnet-fixtures.ts";
import protocolModule from "../../frontend/lib/protocol.ts";

const { DEVNET_PROTOCOL_FIXTURE_STATE } =
  fixturesModule as typeof import("../../frontend/lib/devnet-fixtures.ts");

const {
  buildCreateDomainAssetVaultTx,
  buildFundSponsorBudgetTx,
} = protocolModule as typeof import("../../frontend/lib/protocol.ts");

const recentBlockhash = "11111111111111111111111111111111";
const wallet = DEVNET_PROTOCOL_FIXTURE_STATE.wallets[0]!.address;
const recipient = DEVNET_PROTOCOL_FIXTURE_STATE.wallets[1]!.address;
const reserveDomain = DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains[0]!.address;
const fundingLine = DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines[0]!;

test("[CSO-2026-04-29] custody builders reject non-classic token program ids", () => {
  assert.throws(
    () => buildCreateDomainAssetVaultTx({
      authority: wallet,
      reserveDomainAddress: reserveDomain,
      assetMint: fundingLine.assetMint,
      recentBlockhash,
      tokenProgramId: SystemProgram.programId,
    }),
    /classic SPL Token program/,
  );

  assert.throws(
    () => buildFundSponsorBudgetTx({
      authority: wallet,
      healthPlanAddress: fundingLine.healthPlan,
      reserveDomainAddress: fundingLine.reserveDomain,
      fundingLineAddress: fundingLine.address,
      assetMint: fundingLine.assetMint,
      sourceTokenAccountAddress: wallet,
      vaultTokenAccountAddress: recipient,
      recentBlockhash,
      amount: 1n,
      tokenProgramId: SystemProgram.programId,
    }),
    /classic SPL Token program/,
  );

});
