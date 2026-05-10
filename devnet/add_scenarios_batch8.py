"""
KR 1.3 — Batch 8 (FINAL): TRV30 denials and under-review
  TRV30-T1-DEN-002 — routine elective eye exam (EXCL_5.1)
  TRV30-T2-DEN-002 — opioid rehabilitation / substance dependence (EXCL_5.6)
  TRV30-T3-DEN-002 — claim before policy activation date (EXCL_PRE)
  TRV30-T2-REVIEW-001 — complex polytrauma, specialist ortho report pending
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

T30_POLICY_SERIES = "29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco"
HEALTH_PLAN       = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR          = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
T30_LIQUIDITY_FL  = "HBrdsf7UjYK5tRoM9j6YaxfV7nFBkVhnJbrmTLVaDiEr"

NEW_SCENARIOS = [

    # ── TRV30-T1-DEN-002 ── Routine elective eye exam / Bangkok ──────────────
    {
        "_comment": "--- TRAVEL 30 | DENIAL — Elective routine check-up (EXCL_5.1) ---",
        "scenarioId": "TRV30-T1-DEN-002",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "denied": True,
        "patientProfile": {
            "age": 45,
            "sex": "F",
            "nationality": "GB",
            "originCountry": "United Kingdom",
            "destinationCountry": "Thailand",
            "preExistingConditions": "mild myopia (glasses wearer since age 12)",
            "policyInceptionDaysAgo": 10,
            "memberWalletSim": "sim-member-wallet-TRV30-T1-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "Thailand",
            "incidentCity": "Bangkok",
            "facilityType": "Bangkok Eye Hospital — Outpatient Optometry Clinic (not emergency)",
            "facilityName": "Bangkok Eye Hospital",
            "eventContext": "Leisure travel — taking advantage of lower optometry costs in Thailand",
            "incidentDayOfCoverage": 10
        },
        "diagnosis": {
            "primaryDiagnosis": "Routine comprehensive eye examination — myopia reassessment, new glasses and contact lens prescription",
            "icdCode": "Z01.01",
            "icdDescription": "Encounter for examination of eyes and vision without abnormal findings",
            "clinicalNarrative": (
                "Patient proactively booked an appointment at Bangkok Eye Hospital "
                "via the hospital website 2 days prior to attendance. "
                "Appointment type logged as 'Annual Eye Check' in the hospital booking system. "
                "Services provided: comprehensive refraction, automated keratometry, "
                "intraocular pressure check, fundoscopy, new spectacle prescription issued, "
                "contact lens trial fitting. "
                "No acute complaint — patient's stated reason: 'my glasses are 2 years old, "
                "checking if my prescription has changed'. "
                "No red eye, no pain, no sudden visual change, no trauma. "
                "Patient submitted the appointment invoice to Travel 30 as an 'eye emergency'."
            ),
            "documentsAvailable": [
                "Bangkok Eye Hospital appointment booking confirmation (type: Annual Eye Check)",
                "optometry assessment report",
                "new spectacle and contact lens prescription",
                "itemized invoice"
            ],
            "investigationFindings": [
                "Appointment pre-booked 2 days in advance via hospital website",
                "Appointment type explicitly logged as 'Annual Eye Check' in hospital system",
                "No acute complaint documented anywhere in the clinical record",
                "Services rendered are routine optometry, not emergency ophthalmology"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 310,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 310,
            "amountClaimed": 310,
            "amountApproved": 0,
            "amountDenied": 310,
            "denialBreakdown": (
                "Full claim denied. Routine elective eye examination and prescription update "
                "is explicitly excluded under genesis-acute-v1 Section 5.1 "
                "(Excluded Conditions: Elective and Pre-Planned Procedures and Check-ups). "
                "The visit was pre-booked, non-urgent, and not triggered by an acute ocular event. "
                "The patient's description of the visit as an 'eye emergency' is unsupported "
                "by any clinical record."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Routine optometry visit — elective, pre-planned. "
                "genesis-acute-v1 Section 5.1 applies. "
                "No coverage for routine check-ups regardless of cost or location."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "hospital booking confirmation (Annual Eye Check)",
                "optometry assessment report (no acute complaint)",
                "itemized invoice"
            ],
            "tierClassified": "NOT_APPLICABLE",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Section 5.1 — Elective and Pre-Planned Procedures and Check-ups",
            "reviewNotes": (
                "Appointment pre-booked 2 days prior, type 'Annual Eye Check'. "
                "No acute complaint in any part of the clinical record. "
                "Services rendered are standard routine optometry. "
                "This is an elective pre-planned visit — Section 5.1 applies. "
                "The claim narrative ('eye emergency') is contradicted by the "
                "booking and clinical documentation. Denied."
            ),
            "reviewCompletedHours": 2.5
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t1-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID"
        }
    },

    # ── TRV30-T2-DEN-002 ── Opioid rehabilitation / Singapore ────────────────
    {
        "_comment": "--- TRAVEL 30 | DENIAL — Substance dependence treatment (EXCL_5.6) ---",
        "scenarioId": "TRV30-T2-DEN-002",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "denied": True,
        "patientProfile": {
            "age": 33,
            "sex": "M",
            "nationality": "AU",
            "originCountry": "Australia",
            "destinationCountry": "Singapore",
            "preExistingConditions": "opioid use disorder (OUD) — on buprenorphine maintenance therapy in Australia",
            "policyInceptionDaysAgo": 15,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "Singapore",
            "incidentCity": "Singapore",
            "facilityType": "Tiong Bahru Community Hospital — Inpatient Rehabilitation Unit",
            "facilityName": "Tiong Bahru Community Hospital (SingHealth)",
            "eventContext": "Business and leisure travel — extended stay, elective inpatient rehabilitation",
            "incidentDayOfCoverage": 15
        },
        "diagnosis": {
            "primaryDiagnosis": "Opioid use disorder — voluntary inpatient detoxification and rehabilitation (5-day programme)",
            "icdCode": "F11.20",
            "icdDescription": "Opioid dependence, uncomplicated",
            "clinicalNarrative": (
                "Patient voluntarily enrolled in a 5-day inpatient opioid detoxification "
                "and rehabilitation programme at Tiong Bahru Community Hospital. "
                "Patient stopped buprenorphine maintenance 4 days before admission "
                "(self-managed taper). "
                "Programme: medically supervised withdrawal, clonidine for autonomic symptoms, "
                "psychological counselling, relapse prevention planning. "
                "No acute medical emergency or life-threatening complication occurred. "
                "Patient described admission on the claim form as 'acute medical hospitalisation "
                "for severe pain and withdrawal symptoms while travelling'."
            ),
            "documentsAvailable": [
                "Tiong Bahru Community Hospital admission record (voluntary rehabilitation programme)",
                "clinical psychology assessment note",
                "medication administration record (clonidine detox protocol)",
                "discharge summary (rehabilitation programme completion)"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 3800,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 3800,
            "amountClaimed": 3000,
            "amountApproved": 0,
            "amountDenied": 3800,
            "denialBreakdown": (
                "Full claim denied. Voluntary inpatient opioid detoxification and "
                "rehabilitation is explicitly excluded under genesis-acute-v1 Section 5.6 "
                "(Excluded Conditions: Substance Dependence Treatment and Detoxification). "
                "This exclusion applies regardless of clinical severity, the presence of "
                "withdrawal symptoms, or the geographical location of treatment. "
                "The characterisation of the admission as an 'acute medical hospitalisation' "
                "is inconsistent with the documented voluntary rehabilitation programme structure."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Voluntary substance dependence rehabilitation — "
                "genesis-acute-v1 Section 5.6 absolute exclusion. "
                "Member should seek coverage through Australian private health insurance "
                "if OUD rehab coverage exists under their home policy."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "hospital admission record (voluntary rehab programme)",
                "psychology assessment note",
                "discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Section 5.6 — Substance Dependence Treatment and Detoxification",
            "reviewNotes": (
                "Voluntary 5-day inpatient opioid detoxification programme confirmed by "
                "admission records and psychology note. No acute life-threatening event. "
                "Section 5.6 is an absolute exclusion — applies regardless of symptoms "
                "or clinical management involved. Denied."
            ),
            "reviewCompletedHours": 5.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID"
        }
    },

    # ── TRV30-T3-DEN-002 ── Claim before policy activation / Bangkok ──────────
    {
        "_comment": "--- TRAVEL 30 | DENIAL — Incident pre-dates policy activation (EXCL_PRE) ---",
        "scenarioId": "TRV30-T3-DEN-002",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "denied": True,
        "patientProfile": {
            "age": 47,
            "sex": "M",
            "nationality": "ZA",
            "originCountry": "South Africa",
            "destinationCountry": "Thailand",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 0,
            "memberWalletSim": "sim-member-wallet-TRV30-T3-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "Thailand",
            "incidentCity": "Bangkok",
            "facilityType": "Bumrungrad International Hospital — Emergency Orthopaedic Surgery",
            "facilityName": "Bumrungrad International Hospital",
            "eventContext": "Leisure travel — hotel staircase fall on day of arrival (before policy activated)",
            "incidentDayOfCoverage": 0
        },
        "diagnosis": {
            "primaryDiagnosis": "Displaced distal radius fracture (Colles-type) with operative ORIF — fall on outstretched hand",
            "icdCode": "S52.501A",
            "icdDescription": "Unspecified fracture of the lower end of right radius, initial encounter for closed fracture",
            "clinicalNarrative": (
                "Patient fell on hotel staircase on the day of arrival in Bangkok, "
                "landing on outstretched right hand. "
                "X-ray right wrist: severely displaced distal radius fracture "
                "(Colles-type, dorsal angulation 45 degrees, radial shortening 8mm). "
                "Orthopaedic surgery: open reduction and internal fixation (ORIF) "
                "with volar locking plate. Duration 80 minutes under general anaesthesia. "
                "Overnight admission + hand therapy day 2. Discharged day 2. "
                "POLICY TIMELINE INVESTIGATION: "
                "Policy purchase timestamp: 2026-04-18 14:22 UTC. "
                "Policy activation (inception): 2026-04-19 00:00 UTC. "
                "Incident timestamp (hotel CCTV and hospital ED record): "
                "2026-04-18 22:45 local Bangkok time (UTC+7) = 2026-04-18 15:45 UTC. "
                "The incident occurred 8 hours and 15 minutes after policy purchase "
                "but 8 hours and 15 minutes BEFORE the policy activation time."
            ),
            "documentsAvailable": [
                "ED triage note (timestamp 2026-04-18 22:45 Bangkok local / 15:45 UTC)",
                "X-ray right wrist report",
                "orthopaedic operative note (ORIF volar locking plate)",
                "anaesthesia record",
                "policy certificate (purchase 2026-04-18 14:22 UTC, inception 2026-04-19 00:00 UTC)",
                "hotel CCTV incident log (timestamp corroborating ED record)"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 6800,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 6800,
            "amountClaimed": 3000,
            "amountApproved": 0,
            "amountDenied": 3000,
            "denialBreakdown": (
                "Full claim denied. The incident timestamp (2026-04-18 15:45 UTC) "
                "pre-dates the policy activation time (2026-04-19 00:00 UTC) by 8 hours 15 minutes. "
                "Travel 30 coverage commences at 00:00 UTC on the policy inception date. "
                "The policy purchase timestamp does not constitute coverage commencement. "
                "Excluded under genesis-acute-v1 coverage window clause (EXCL_PRE): "
                "no retroactive coverage applies to incidents occurring before inception."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Incident 8h 15min before policy activation. "
                "Coverage commences at inception date 00:00 UTC, not at purchase timestamp. "
                "Member has no other active travel insurance on file. "
                "Claims operator advised member to seek reimbursement via South African "
                "medical aid or credit card travel protection if applicable."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note (timestamp verified: 2026-04-18 15:45 UTC)",
                "policy certificate (inception: 2026-04-19 00:00 UTC)",
                "hotel CCTV incident log (corroborating timestamp)"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Coverage Window Clause (EXCL_PRE) — incident before policy inception",
            "reviewNotes": (
                "Timeline verified from three independent sources: hospital ED record, "
                "hotel CCTV, and policy certificate. "
                "Incident: 2026-04-18 15:45 UTC. "
                "Policy inception: 2026-04-19 00:00 UTC. "
                "Delta: -8h 15min (incident pre-dates inception). "
                "The injury itself would have qualified as Tier 3 had it occurred within "
                "the coverage window. Denial is purely administrative — timing. "
                "No coverage applies."
            ),
            "reviewCompletedHours": 6.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t3-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID"
        }
    },

    # ── TRV30-T2-REVIEW-001 ── Complex polytrauma / Kuala Lumpur ─────────────
    {
        "_comment": "--- TRAVEL 30 | IN-FLIGHT / UNDER REVIEW — Polytrauma, specialist ortho report pending ---",
        "scenarioId": "TRV30-T2-REVIEW-001",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "inFlight": True,
        "patientProfile": {
            "age": 29,
            "sex": "M",
            "nationality": "NL",
            "originCountry": "Netherlands",
            "destinationCountry": "Malaysia",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 7,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-REVIEW-001"
        },
        "clinicalSetting": {
            "incidentCountry": "Malaysia",
            "incidentCity": "Kuala Lumpur",
            "facilityType": "Sunway Medical Centre — Emergency Trauma and Orthopaedic Surgery",
            "facilityName": "Sunway Medical Centre",
            "eventContext": "Leisure travel — road traffic accident involving motorcycle taxi, day 7",
            "incidentDayOfCoverage": 7
        },
        "diagnosis": {
            "primaryDiagnosis": "Complex polytrauma — left femur shaft fracture, right tibial plateau fracture, L2 transverse process fracture — orthopaedic fixation surgery + L2 spine clearance pending",
            "icdCode": "S72.301A",
            "icdDescription": "Unspecified fracture of shaft of right femur, initial encounter for closed fracture",
            "clinicalNarrative": (
                "Patient was a passenger on a motorcycle taxi involved in a collision "
                "with a van. Multiple injuries identified: "
                "(1) Left femur shaft fracture — displaced, mid-diaphyseal. "
                "(2) Right tibial plateau fracture — Schatzker Type II (split-depression). "
                "(3) L2 vertebral body right transverse process fracture (CT spine). "
                "Neurosurgery clearance for L2: no cord or cauda equina involvement, "
                "neurologically intact. Transverse process fracture: conservative management. "
                "Orthopaedic surgery day 1: "
                "Left femur — intramedullary nail (femoral rod). "
                "Right tibial plateau — open reduction, lateral plate fixation. "
                "Duration: 4 hours under general anaesthesia. "
                "Post-operative ICU: 2 nights — "
                "haemodynamic management (blood loss 900mL, 2 units pRBC), "
                "VTE prophylaxis initiated, bilateral lower limb monitoring. "
                "Step-down ward: patient still admitted. "
                "PENDING: specialist orthopaedic second opinion on tibial plateau fixation "
                "adequacy and L2 stability confirmation before rehabilitation plan finalised. "
                "Itemized invoice not yet received — hospital billing confirmed ETA 48-72h."
            ),
            "documentsAvailable": [
                "ED trauma assessment note",
                "CT scan reports (pelvis, bilateral lower limbs, spine)",
                "neurosurgery clearance note (L2 — conservative)",
                "orthopaedic operative note (femoral nail + tibial plateau ORIF)",
                "anaesthesia and blood transfusion record",
                "ICU nursing chart (nights 1-2)"
            ],
            "documentsPending": [
                "Specialist orthopaedic second opinion (tibial plateau fixation adequacy) — ETA 48h",
                "Itemized hospital invoice — Sunway Medical Centre billing (ETA 48-72h)",
                "L2 stability orthopaedic clearance letter — ETA 24h"
            ],
            "claimSubmittedAt": "2026-04-23T10:30:00Z"
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 0,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 0,
            "amountClaimed": 3000,
            "amountApproved": 0,
            "amountReserved": 3000,
            "amountDenied": 0,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Claim under active review. Full $3,000 product maximum reserved on "
                "genesis-travel30-liquidity FundingLine. "
                "Tier 3 criteria appear met (emergency orthopaedic surgery + ICU 2 nights). "
                "UCR review cannot be completed until itemized invoice is received. "
                "Orthopaedic specialist second opinion and L2 clearance letter pending — "
                "required to confirm final scope of covered treatment."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED trauma assessment note",
                "CT scan reports",
                "neurosurgery clearance note",
                "operative note (femoral nail + tibial plateau ORIF)",
                "ICU nursing chart (nights 1-2)"
            ],
            "documentsPending": [
                "Specialist orthopaedic second opinion — tibial plateau fixation adequacy (ETA 48h)",
                "L2 vertebral stability orthopaedic clearance (ETA 24h)",
                "Itemized hospital invoice (Sunway Medical Centre billing, ETA 48-72h)"
            ],
            "tierPreClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "PENDING",
            "reviewBlockingReason": (
                "Three documents pending: "
                "(1) Orthopaedic specialist second opinion on tibial plateau fixation "
                "adequacy — required to confirm whether further surgery is planned (affects "
                "total covered episode definition). "
                "(2) L2 stability clearance letter — required to confirm conservative "
                "management is the final decision (no deferred spinal surgery). "
                "(3) Itemized hospital invoice — UCR review cannot be performed on the "
                "lump sum; per-category itemization required "
                "(surgery theatre, ICU, ward, pharmacy, imaging)."
            ),
            "reviewSlaDeadlineHours": 48,
            "reviewElapsedHours": 8,
            "reviewCompletedHours": None,
            "anticipatedApprovedRange": "$2,800 - $3,000 (product maximum) upon UCR review"
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-review-001",
            "intakeStatus": 1,
            "intakeStatusLabel": "UNDER_REVIEW",
            "approvedAmountUsdc": 0,
            "reservedAmountUsdc": 3000,
            "paidAmountUsdc": 0,
            "fundingLineCharged": "genesis-travel30-liquidity",
            "fundingLineAddress": T30_LIQUIDITY_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "RESERVED",
            "expectedResolutionNote": (
                "Pending 3 documents (ETA 24-72h). "
                "Anticipated outcome: APPROVED_PARTIAL or FULLY_SETTLED at $3,000 "
                "product maximum after UCR itemization."
            )
        }
    }
]


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    before = len(data["travel30Scenarios"])
    data["travel30Scenarios"].extend(NEW_SCENARIOS)
    after = len(data["travel30Scenarios"])

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Batch 8 (FINAL) done.")
    print("event7Scenarios: {}".format(len(data["event7Scenarios"])))
    print("travel30Scenarios: {} -> {}".format(before, after))
    total = len(data["event7Scenarios"]) + after
    print("GRAND TOTAL: {}".format(total))
    assert total == 64, "Expected 64 scenarios, got {}".format(total)
    print("KR 1.3 COMPLETE: 64 scenarios confirmed.")


if __name__ == "__main__":
    main()
