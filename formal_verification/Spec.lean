import Mathlib.Algebra.BigOperators.Fin
import QEDGen.Solana.Account
import QEDGenMathlib.IndexedState

namespace OmegaxProtocol

open QEDGen.Solana
open QEDGen.Solana.IndexedState

set_option linter.unusedVariables false

abbrev BASIS_POINTS_DENOMINATOR : Nat := 10000
abbrev MAX_CONFIGURED_FEE_BPS : Nat := 9999
abbrev MAX_SELECTED_ASSET_PAYOUT_OVERPAY_BPS : Nat := 50

abbrev AccountIdx : Type := Fin MAX_CONFIGURED_FEE_BPS

structure AdjudicateClaimCaseArgs where
  review_state : Nat
  approved_amount : Nat
  denied_amount : Nat
  reserve_amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited AdjudicateClaimCaseArgs := ⟨{
  review_state := 0,
  approved_amount := 0,
  denied_amount := 0,
  reserve_amount := 0,
}⟩

structure AllocateCapitalArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited AllocateCapitalArgs := ⟨{
  amount := 0,
}⟩

structure AttachClaimEvidenceRefArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited AttachClaimEvidenceRefArgs := ⟨{
}⟩

structure AttestClaimCaseArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited AttestClaimCaseArgs := ⟨{
}⟩

structure AuthorizeClaimRecipientArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited AuthorizeClaimRecipientArgs := ⟨{
}⟩

structure BackfillSchemaDependencyLedgerArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited BackfillSchemaDependencyLedgerArgs := ⟨{
}⟩

structure ConfigureReserveAssetRailArgs where
  active : Bool
  max_staleness_seconds : Nat
  payout_enabled : Bool
  capacity_enabled : Bool
  max_confidence_bps : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited ConfigureReserveAssetRailArgs := ⟨{
  active := false,
  max_staleness_seconds := 0,
  payout_enabled := false,
  capacity_enabled := false,
  max_confidence_bps := 0,
}⟩

structure CreateAllocationPositionArgs where
  cap_amount : Nat
  weight_bps : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateAllocationPositionArgs := ⟨{
  cap_amount := 0,
  weight_bps := 0,
}⟩

structure CreateCapitalClassArgs where
  fee_bps : Nat
  pause_flags : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateCapitalClassArgs := ⟨{
  fee_bps := 0,
  pause_flags := 0,
}⟩

structure CreateDomainAssetVaultArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateDomainAssetVaultArgs := ⟨{
}⟩

structure CreateHealthPlanArgs where
  allowed_rail_mask : Nat
  pause_flags : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateHealthPlanArgs := ⟨{
  allowed_rail_mask := 0,
  pause_flags := 0,
}⟩

structure CreateLiquidityPoolArgs where
  fee_bps : Nat
  pause_flags : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateLiquidityPoolArgs := ⟨{
  fee_bps := 0,
  pause_flags := 0,
}⟩

structure CreateObligationArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateObligationArgs := ⟨{
  amount := 0,
}⟩

structure CreatePolicySeriesArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreatePolicySeriesArgs := ⟨{
}⟩

structure CreateReserveDomainArgs where
  allowed_rail_mask : Nat
  pause_flags : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited CreateReserveDomainArgs := ⟨{
  allowed_rail_mask := 0,
  pause_flags := 0,
}⟩

structure DeallocateCapitalArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited DeallocateCapitalArgs := ⟨{
  amount := 0,
}⟩

structure DepositReserveCapitalArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited DepositReserveCapitalArgs := ⟨{
  amount := 0,
}⟩

structure DepositIntoCapitalClassArgs where
  amount : Nat
  shares : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited DepositIntoCapitalClassArgs := ⟨{
  amount := 0,
  shares := 0,
}⟩

structure FundSponsorBudgetArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited FundSponsorBudgetArgs := ⟨{
  amount := 0,
}⟩

structure InitPoolOracleFeeVaultArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited InitPoolOracleFeeVaultArgs := ⟨{
}⟩

structure InitPoolTreasuryVaultArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited InitPoolTreasuryVaultArgs := ⟨{
}⟩

structure InitProtocolFeeVaultArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited InitProtocolFeeVaultArgs := ⟨{
}⟩

structure InitializeProtocolGovernanceArgs where
  protocol_fee_bps : Nat
  emergency_pause : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited InitializeProtocolGovernanceArgs := ⟨{
  protocol_fee_bps := 0,
  emergency_pause := false,
}⟩

structure InitializeSeriesReserveLedgerArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited InitializeSeriesReserveLedgerArgs := ⟨{
}⟩

structure MarkImpairmentArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited MarkImpairmentArgs := ⟨{
  amount := 0,
}⟩

structure OpenClaimCaseArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited OpenClaimCaseArgs := ⟨{
}⟩

structure OpenFundingLineArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited OpenFundingLineArgs := ⟨{
}⟩

structure OpenMemberPositionArgs where
  eligibility_status : Nat
  delegated_rights : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited OpenMemberPositionArgs := ⟨{
  eligibility_status := 0,
  delegated_rights := 0,
}⟩

structure ProcessRedemptionQueueArgs where
  shares : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited ProcessRedemptionQueueArgs := ⟨{
  shares := 0,
}⟩

structure PublishReserveAssetRailPriceArgs where
  price_usd_1e8 : Nat
  confidence_bps : Nat
  published_at_ts : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited PublishReserveAssetRailPriceArgs := ⟨{
  price_usd_1e8 := 0,
  confidence_bps := 0,
  published_at_ts := 0,
}⟩

structure RecordPremiumPaymentArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited RecordPremiumPaymentArgs := ⟨{
  amount := 0,
}⟩

structure RecordReserveEarningsArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited RecordReserveEarningsArgs := ⟨{
  amount := 0,
}⟩

structure RegisterOracleArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited RegisterOracleArgs := ⟨{
}⟩

structure RegisterOutcomeSchemaArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited RegisterOutcomeSchemaArgs := ⟨{
}⟩

structure ReleaseReserveArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited ReleaseReserveArgs := ⟨{
  amount := 0,
}⟩

structure RequestRedemptionArgs where
  shares : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited RequestRedemptionArgs := ⟨{
  shares := 0,
}⟩

structure ReserveObligationArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited ReserveObligationArgs := ⟨{
  amount := 0,
}⟩

structure ReturnReserveCapitalArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited ReturnReserveCapitalArgs := ⟨{
  amount := 0,
}⟩

structure RotateProtocolGovernanceAuthorityArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited RotateProtocolGovernanceAuthorityArgs := ⟨{
}⟩

structure SetPoolOracleArgs where
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited SetPoolOracleArgs := ⟨{
  active := false,
}⟩

structure SetPoolOraclePermissionsArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited SetPoolOraclePermissionsArgs := ⟨{
}⟩

structure SetPoolOraclePolicyArgs where
  quorum_m : Nat
  quorum_n : Nat
  oracle_fee_bps : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited SetPoolOraclePolicyArgs := ⟨{
  quorum_m := 0,
  quorum_n := 0,
  oracle_fee_bps := 0,
}⟩

structure SetProtocolEmergencyPauseArgs where
  emergency_pause : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited SetProtocolEmergencyPauseArgs := ⟨{
  emergency_pause := false,
}⟩

structure SettleClaimCaseArgs where
  amount : Nat
  rail_active : Bool
  rail_payout_enabled : Bool
  rail_price_usd_1e8 : Nat
  rail_max_staleness_seconds : Nat
  rail_max_confidence_bps : Nat
  rail_last_price_confidence_bps : Nat
  rail_last_price_published_at_ts : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited SettleClaimCaseArgs := ⟨{
  amount := 0,
  rail_active := false,
  rail_payout_enabled := false,
  rail_price_usd_1e8 := 0,
  rail_max_staleness_seconds := 0,
  rail_max_confidence_bps := 0,
  rail_last_price_confidence_bps := 0,
  rail_last_price_published_at_ts := 0,
}⟩

structure SettleClaimCaseSelectedAssetArgs where
  claim_credit_amount : Nat
  payout_amount : Nat
  max_overpay_bps : Nat
  claim_rail_active : Bool
  claim_rail_price_usd_1e8 : Nat
  claim_rail_max_staleness_seconds : Nat
  claim_rail_max_confidence_bps : Nat
  claim_rail_last_price_confidence_bps : Nat
  claim_rail_last_price_published_at_ts : Nat
  payout_rail_active : Bool
  payout_rail_payout_enabled : Bool
  payout_rail_price_usd_1e8 : Nat
  payout_rail_max_staleness_seconds : Nat
  payout_rail_max_confidence_bps : Nat
  payout_rail_last_price_confidence_bps : Nat
  payout_rail_last_price_published_at_ts : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited SettleClaimCaseSelectedAssetArgs := ⟨{
  claim_credit_amount := 0,
  payout_amount := 0,
  max_overpay_bps := 0,
  claim_rail_active := false,
  claim_rail_price_usd_1e8 := 0,
  claim_rail_max_staleness_seconds := 0,
  claim_rail_max_confidence_bps := 0,
  claim_rail_last_price_confidence_bps := 0,
  claim_rail_last_price_published_at_ts := 0,
  payout_rail_active := false,
  payout_rail_payout_enabled := false,
  payout_rail_price_usd_1e8 := 0,
  payout_rail_max_staleness_seconds := 0,
  payout_rail_max_confidence_bps := 0,
  payout_rail_last_price_confidence_bps := 0,
  payout_rail_last_price_published_at_ts := 0,
}⟩

structure SettleObligationArgs where
  amount : Nat
  rail_active : Bool
  rail_payout_enabled : Bool
  rail_price_usd_1e8 : Nat
  rail_max_staleness_seconds : Nat
  rail_max_confidence_bps : Nat
  rail_last_price_confidence_bps : Nat
  rail_last_price_published_at_ts : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited SettleObligationArgs := ⟨{
  amount := 0,
  rail_active := false,
  rail_payout_enabled := false,
  rail_price_usd_1e8 := 0,
  rail_max_staleness_seconds := 0,
  rail_max_confidence_bps := 0,
  rail_last_price_confidence_bps := 0,
  rail_last_price_published_at_ts := 0,
}⟩

structure UpdateAllocationCapsArgs where
  cap_amount : Nat
  weight_bps : Nat
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateAllocationCapsArgs := ⟨{
  cap_amount := 0,
  weight_bps := 0,
  active := false,
}⟩

structure UpdateCapitalClassControlsArgs where
  pause_flags : Nat
  queue_only_redemptions : Bool
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateCapitalClassControlsArgs := ⟨{
  pause_flags := 0,
  queue_only_redemptions := false,
  active := false,
}⟩

structure UpdateHealthPlanControlsArgs where
  allowed_rail_mask : Nat
  pause_flags : Nat
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateHealthPlanControlsArgs := ⟨{
  allowed_rail_mask := 0,
  pause_flags := 0,
  active := false,
}⟩

structure UpdateLpPositionCredentialingArgs where
  credentialed : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateLpPositionCredentialingArgs := ⟨{
  credentialed := false,
}⟩

structure UpdateMemberEligibilityArgs where
  eligibility_status : Nat
  delegated_rights : Nat
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateMemberEligibilityArgs := ⟨{
  eligibility_status := 0,
  delegated_rights := 0,
  active := false,
}⟩

structure UpdateOracleProfileArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateOracleProfileArgs := ⟨{
}⟩

structure UpdateReserveDomainControlsArgs where
  allowed_rail_mask : Nat
  pause_flags : Nat
  active : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited UpdateReserveDomainControlsArgs := ⟨{
  allowed_rail_mask := 0,
  pause_flags := 0,
  active := false,
}⟩

structure VerifyOutcomeSchemaArgs where
  verified : Bool
  deriving Repr, DecidableEq, BEq

instance : Inhabited VerifyOutcomeSchemaArgs := ⟨{
  verified := false,
}⟩

structure VersionPolicySeriesArgs where
  deriving Repr, DecidableEq, BEq

instance : Inhabited VersionPolicySeriesArgs := ⟨{
}⟩

structure WithdrawArgs where
  amount : Nat
  deriving Repr, DecidableEq, BEq

instance : Inhabited WithdrawArgs := ⟨{
  amount := 0,
}⟩

inductive Status where
  | Uninitialized
  | Live
  deriving Repr, DecidableEq, BEq

structure State where
  governance_authority : Pubkey
  pending_authority : Pubkey
  authority : Pubkey
  plan_admin : Pubkey
  wallet : Pubkey
  depositor : Pubkey
  activation_authority : Pubkey
  owner : Pubkey
  admin : Pubkey
  oracle : Pubkey
  publisher : Pubkey
  audit_nonce : Nat
  protocol_fee_bps : Nat
  emergency_pause : Bool
  allowed_rail_mask : Nat
  pause_flags : Nat
  active : Bool
  total_assets : Nat
  last_price_usd_1e8 : Nat
  last_price_confidence_bps : Nat
  max_confidence_bps : Nat
  max_staleness_seconds : Nat
  payout_enabled : Bool
  capacity_enabled : Bool
  last_price_published_at_ts : Nat
  accrued_fees : Nat
  withdrawn_fees : Nat
  membership_mode : Nat
  eligibility_status : Nat
  delegated_rights : Nat
  funded_amount : Nat
  spent_amount : Nat
  reserved_amount : Nat
  paid_amount : Nat
  approved_amount : Nat
  denied_amount : Nat
  pending_amount : Nat
  activated_amount : Nat
  treasury_locked_amount : Nat
  refunded_amount : Nat
  canceled_amount : Nat
  next_queue_index : Nat
  refunded_at : Nat
  intake_status : Nat
  review_state : Nat
  recovered_amount : Nat
  appeal_count : Nat
  attestation_count : Nat
  supported_schema_count : Nat
  updated_at_ts : Nat
  updated_at : Nat
  created_at_ts : Nat
  closed_at : Nat
  oracle_fee_bps : Nat
  quorum_m : Nat
  quorum_n : Nat
  challenge_window_secs : Nat
  cap_amount : Nat
  weight_bps : Nat
  allocated_amount : Nat
  allocated_assets : Nat
  total_allocated : Nat
  pending_redemption_shares : Nat
  pending_redemption_assets : Nat
  pending_redemptions : Nat
  total_shares : Nat
  nav_assets : Nat
  queue_only_redemptions : Bool
  credentialed : Bool
  claimed : Bool
  verified : Bool
  closed_outcome_schema_count : Nat
  refund_amount : Nat
  settlement_net_payout_amount : Nat
  claim_net_payout_amount : Nat
  redemption_net_payout_amount : Nat
  fee_withdrawal_amount : Nat
  bump : Nat
  status : Status

def create_reserve_domainTransition (s : State) (signer : Pubkey) (args : CreateReserveDomainArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with status := .Live }
  else none

def update_reserve_domain_controlsTransition (s : State) (signer : Pubkey) (args : UpdateReserveDomainControlsArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with allowed_rail_mask := args.allowed_rail_mask, pause_flags := args.pause_flags, active := args.active, status := .Live }
  else none

def create_domain_asset_vaultTransition (s : State) (signer : Pubkey) (args : CreateDomainAssetVaultArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with total_assets := 0, status := .Live }
  else none

def create_health_planTransition (s : State) (signer : Pubkey) (args : CreateHealthPlanArgs) : Option State :=
  if signer = s.plan_admin ∧ s.status = .Live then
    some { s with status := .Live }
  else none

def update_health_plan_controlsTransition (s : State) (signer : Pubkey) (args : UpdateHealthPlanControlsArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with active := args.active, status := .Live }
  else none

def create_policy_seriesTransition (s : State) (signer : Pubkey) (args : CreatePolicySeriesArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with status := .Live }
  else none

def version_policy_seriesTransition (s : State) (signer : Pubkey) (args : VersionPolicySeriesArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with status := .Live }
  else none

def open_funding_lineTransition (s : State) (signer : Pubkey) (args : OpenFundingLineArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live then
    some { s with status := .Live }
  else none

def fund_sponsor_budgetTransition (s : State) (signer : Pubkey) (args : FundSponsorBudgetArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def record_premium_paymentTransition (s : State) (signer : Pubkey) (args : RecordPremiumPaymentArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def deposit_reserve_capitalTransition (s : State) (signer : Pubkey) (args : DepositReserveCapitalArgs) : Option State :=
  if s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def return_reserve_capitalTransition (s : State) (signer : Pubkey) (args : ReturnReserveCapitalArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def record_reserve_earningsTransition (s : State) (signer : Pubkey) (args : RecordReserveEarningsArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def create_obligationTransition (s : State) (signer : Pubkey) (args : CreateObligationArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def reserve_obligationTransition (s : State) (signer : Pubkey) (args : ReserveObligationArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def settle_obligationTransition (s : State) (signer : Pubkey) (args : SettleObligationArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) ∧ (args.rail_active = true) ∧ (args.rail_payout_enabled = true) ∧ (args.rail_price_usd_1e8 > 0) ∧ (args.rail_max_staleness_seconds > 0) ∧ (args.rail_max_confidence_bps > 0) ∧ (args.rail_last_price_confidence_bps ≤ args.rail_max_confidence_bps) ∧ (args.rail_last_price_published_at_ts > 0) then
    some { s with status := .Live }
  else none

def release_reserveTransition (s : State) (signer : Pubkey) (args : ReleaseReserveArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) then
    some { s with status := .Live }
  else none

def open_claim_caseTransition (s : State) (signer : Pubkey) (args : OpenClaimCaseArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (s.active = true) then
    some { s with review_state := 0, status := .Live }
  else none

def authorize_claim_recipientTransition (s : State) (signer : Pubkey) (args : AuthorizeClaimRecipientArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) then
    some { s with status := .Live }
  else none

def adjudicate_claim_caseTransition (s : State) (signer : Pubkey) (args : AdjudicateClaimCaseArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.reserve_amount ≤ args.approved_amount) then
    some { s with review_state := args.review_state, approved_amount := args.approved_amount, denied_amount := args.denied_amount, status := .Live }
  else none

def settle_claim_caseTransition (s : State) (signer : Pubkey) (args : SettleClaimCaseArgs) : Option State :=
  if signer = s.authority ∧ s.status = .Live ∧ (s.emergency_pause = false) ∧ (args.amount > 0) ∧ (s.paid_amount + args.amount ≤ s.approved_amount) ∧ (args.rail_active = true) ∧ (args.rail_payout_enabled = true) ∧ (args.rail_price_usd_1e8 > 0) ∧ (args.rail_max_staleness_seconds > 0) ∧ (args.rail_max_confidence_bps > 0) ∧ (args.rail_last_price_confidence_bps ≤ args.rail_max_confidence_bps) ∧ (args.rail_last_price_published_at_ts > 0) then
    some { s with status := .Live }
  else none

inductive Operation where
  | create_reserve_domain (args : CreateReserveDomainArgs)
  | update_reserve_domain_controls (args : UpdateReserveDomainControlsArgs)
  | create_domain_asset_vault (args : CreateDomainAssetVaultArgs)
  | create_health_plan (args : CreateHealthPlanArgs)
  | update_health_plan_controls (args : UpdateHealthPlanControlsArgs)
  | create_policy_series (args : CreatePolicySeriesArgs)
  | version_policy_series (args : VersionPolicySeriesArgs)
  | open_funding_line (args : OpenFundingLineArgs)
  | fund_sponsor_budget (args : FundSponsorBudgetArgs)
  | record_premium_payment (args : RecordPremiumPaymentArgs)
  | deposit_reserve_capital (args : DepositReserveCapitalArgs)
  | return_reserve_capital (args : ReturnReserveCapitalArgs)
  | record_reserve_earnings (args : RecordReserveEarningsArgs)
  | create_obligation (args : CreateObligationArgs)
  | reserve_obligation (args : ReserveObligationArgs)
  | settle_obligation (args : SettleObligationArgs)
  | release_reserve (args : ReleaseReserveArgs)
  | open_claim_case (args : OpenClaimCaseArgs)
  | authorize_claim_recipient (args : AuthorizeClaimRecipientArgs)
  | adjudicate_claim_case (args : AdjudicateClaimCaseArgs)
  | settle_claim_case (args : SettleClaimCaseArgs)

def applyOp (s : State) (signer : Pubkey) : Operation → Option State
  | .create_reserve_domain args => create_reserve_domainTransition s signer args
  | .update_reserve_domain_controls args => update_reserve_domain_controlsTransition s signer args
  | .create_domain_asset_vault args => create_domain_asset_vaultTransition s signer args
  | .create_health_plan args => create_health_planTransition s signer args
  | .update_health_plan_controls args => update_health_plan_controlsTransition s signer args
  | .create_policy_series args => create_policy_seriesTransition s signer args
  | .version_policy_series args => version_policy_seriesTransition s signer args
  | .open_funding_line args => open_funding_lineTransition s signer args
  | .fund_sponsor_budget args => fund_sponsor_budgetTransition s signer args
  | .record_premium_payment args => record_premium_paymentTransition s signer args
  | .deposit_reserve_capital args => deposit_reserve_capitalTransition s signer args
  | .return_reserve_capital args => return_reserve_capitalTransition s signer args
  | .record_reserve_earnings args => record_reserve_earningsTransition s signer args
  | .create_obligation args => create_obligationTransition s signer args
  | .reserve_obligation args => reserve_obligationTransition s signer args
  | .settle_obligation args => settle_obligationTransition s signer args
  | .release_reserve args => release_reserveTransition s signer args
  | .open_claim_case args => open_claim_caseTransition s signer args
  | .authorize_claim_recipient args => authorize_claim_recipientTransition s signer args
  | .adjudicate_claim_case args => adjudicate_claim_caseTransition s signer args
  | .settle_claim_case args => settle_claim_caseTransition s signer args

/-- Property: abstract_state_progress_nonnegative. -/
def abstract_state_progress_nonnegative (s : State) : Prop :=
  s.audit_nonce ≥ 0

/-- Property: claim_payment_bounded. -/
def claim_payment_bounded (s : State) : Prop :=
  s.paid_amount ≤ s.approved_amount

end OmegaxProtocol
