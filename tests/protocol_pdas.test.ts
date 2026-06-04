import test from "node:test";
import assert from "node:assert/strict";

import fixturesModule from "../frontend/lib/devnet-fixtures.ts";
import protocolModule from "../frontend/lib/protocol.ts";

const {
  DEVNET_PROTOCOL_FIXTURE_STATE,
  DEFAULT_HEALTH_PLAN_ADDRESS,
  DEFAULT_LIQUIDITY_POOL_ADDRESS,
} = fixturesModule as typeof import("../frontend/lib/devnet-fixtures.ts");
const {
  buildAttestClaimCaseTx,
  buildOpenMemberPositionTx,
  deriveClaimAttestationPda,
  deriveHealthPlanPda,
  deriveLiquidityPoolPda,
  deriveReserveDomainPda,
} = protocolModule as typeof import("../frontend/lib/protocol.ts");

test("fixture addresses stay deterministic under canonical seeds", () => {
  const [openDomain, wrapperDomain] = DEVNET_PROTOCOL_FIXTURE_STATE.reserveDomains;
  const seekerPlan = DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans[0]!;
  const pool = DEVNET_PROTOCOL_FIXTURE_STATE.liquidityPools[0]!;

  assert.equal(
    deriveReserveDomainPda({ domainId: openDomain.domainId }).toBase58(),
    openDomain.address,
  );
  assert.equal(
    deriveReserveDomainPda({ domainId: wrapperDomain.domainId }).toBase58(),
    wrapperDomain.address,
  );
  assert.equal(
    deriveHealthPlanPda({ reserveDomain: seekerPlan.reserveDomain, planId: seekerPlan.planId }).toBase58(),
    DEFAULT_HEALTH_PLAN_ADDRESS,
  );
  assert.equal(
    deriveLiquidityPoolPda({ reserveDomain: pool.reserveDomain, poolId: pool.poolId }).toBase58(),
    DEFAULT_LIQUIDITY_POOL_ADDRESS,
  );
  assert.match(
    deriveClaimAttestationPda({
      claimCase: seekerPlan.address,
      oracle: DEFAULT_HEALTH_PLAN_ADDRESS,
    }).toBase58(),
    /^[1-9A-HJ-NP-Za-km-z]{32,44}$/,
  );
});

test("claim attestation builders reject unsupported decisions before chain submission", () => {
  assert.throws(
    () =>
      buildAttestClaimCaseTx({
        oracle: DEFAULT_HEALTH_PLAN_ADDRESS,
        claimCaseAddress: DEVNET_PROTOCOL_FIXTURE_STATE.claimCases[0]!.address,
        recentBlockhash: "11111111111111111111111111111111",
        decision: 99,
        attestationHashHex: "11".repeat(32),
        attestationRefHashHex: "22".repeat(32),
        schemaKeyHashHex: "33".repeat(32),
      }),
    /claim attestation decision must be one of 0/,
  );
});

test("claim attestation builder wires plan oracle accounts", () => {
  const claim = DEVNET_PROTOCOL_FIXTURE_STATE.claimCases[0]!;
  const fundingLine = DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines.find((row) => row.address === claim.fundingLine)!;
  const oracle = DEFAULT_HEALTH_PLAN_ADDRESS;
  const tx = buildAttestClaimCaseTx({
    oracle,
    healthPlanAddress: claim.healthPlan,
    claimCaseAddress: claim.address,
    fundingLineAddress: fundingLine.address,
    recentBlockhash: "11111111111111111111111111111111",
    decision: 0,
    attestationHashHex: "11".repeat(32),
    attestationRefHashHex: "22".repeat(32),
    schemaKeyHashHex: "33".repeat(32),
  });
  const keys = tx.instructions[0]!.keys;
  const keyFor = (address: string) => keys.find((key) => key.pubkey.toBase58() === address);

  assert.equal(keys.length, 6);
  assert.equal(keyFor(oracle)?.isSigner, true);
  assert.equal(keyFor(claim.healthPlan)?.isWritable, false);
  assert.equal(keyFor(claim.address)?.isWritable, true);
  assert.equal(keyFor(fundingLine.address)?.isWritable, false);
  assert.equal(
    keyFor(deriveClaimAttestationPda({ claimCase: claim.address, oracle }).toBase58())?.isWritable,
    true,
  );
});

test("member enrollment builder is removed with the on-chain membership surface", () => {
  const plan = DEVNET_PROTOCOL_FIXTURE_STATE.healthPlans[0]!;
  const memberWallet = DEVNET_PROTOCOL_FIXTURE_STATE.wallets.find((wallet) => wallet.role === "member")!.address;
  const inviteAuthority = plan.membershipInviteAuthority!;
  assert.throws(
    () =>
      buildOpenMemberPositionTx({
        wallet: memberWallet,
        healthPlanAddress: plan.address,
        recentBlockhash: "11111111111111111111111111111111",
        seriesScopeAddress: null,
        subjectCommitmentHashHex: "11".repeat(32),
        eligibilityStatus: 0,
        delegatedRightsMask: 0,
        proofMode: 0,
        inviteIdHashHex: "22".repeat(32),
        inviteExpiresAt: 0n,
        inviteAuthorityAddress: inviteAuthority,
      }),
    /open_member_position was removed/,
  );
});
