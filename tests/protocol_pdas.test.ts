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
  buildAttachClaimEvidenceRefTx,
  buildAttestClaimCaseTx,
  buildOpenMemberPositionTx,
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
});

test("claim evidence and attestation builders are removed with the on-chain attestation surface", () => {
  assert.throws(
    () =>
      buildAttachClaimEvidenceRefTx({
        authority: DEFAULT_HEALTH_PLAN_ADDRESS,
        healthPlanAddress: DEFAULT_HEALTH_PLAN_ADDRESS,
        claimCaseAddress: DEVNET_PROTOCOL_FIXTURE_STATE.claimCases[0]!.address,
        recentBlockhash: "11111111111111111111111111111111",
        evidenceRefHashHex: "11".repeat(32),
        decisionSupportHashHex: "22".repeat(32),
      }),
    /attach_claim_evidence_ref was removed/,
  );

  assert.throws(
    () =>
      buildAttestClaimCaseTx({
        oracle: DEFAULT_HEALTH_PLAN_ADDRESS,
        healthPlanAddress: DEFAULT_HEALTH_PLAN_ADDRESS,
        claimCaseAddress: DEVNET_PROTOCOL_FIXTURE_STATE.claimCases[0]!.address,
        fundingLineAddress: DEVNET_PROTOCOL_FIXTURE_STATE.fundingLines[0]!.address,
        recentBlockhash: "11111111111111111111111111111111",
        decision: 0,
        attestationHashHex: "11".repeat(32),
        attestationRefHashHex: "22".repeat(32),
        schemaKeyHashHex: "33".repeat(32),
      }),
    /attest_claim_case was removed/,
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
