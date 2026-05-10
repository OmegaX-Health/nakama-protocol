"""
KR 1.3 — Batch 4: EVT7 denials and under-review
  EVT7-T1-DEN-002 — claim outside coverage window (EXCL_WIN)
  EVT7-T2-DEN-002 — chronic COPD exacerbation (EXCL_5.4)
  EVT7-T3-DEN-002 — fraudulent invoice (EXCL_8.2)
  EVT7-T2-REVIEW-001 — severe concussion, CT inconclusive
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

E7_POLICY_SERIES = "6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX"
HEALTH_PLAN      = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR         = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
E7_LIQUIDITY_FL  = "Hw6LdQpUqiUShzocvt7R1qxkkiiZiWeWjEoR1Ehx3SLw"

NEW_SCENARIOS = [

    # ── EVT7-T1-DEN-002 ── Incident outside 7-day coverage window ────────────
    {
        "_comment": "--- EVENT 7 | DENIAL — Outside coverage window (EXCL_WIN) ---",
        "scenarioId": "EVT7-T1-DEN-002",
        "product": "genesis-event-7-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "denied": True,
        "patientProfile": {
            "age": 30,
            "sex": "M",
            "nationality": "IT",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 9,
            "memberWalletSim": "sim-member-wallet-EVT7-T1-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "Italy",
            "incidentCity": "Rome",
            "facilityType": "Pronto Soccorso — Ospedale San Giovanni Addolorata",
            "facilityName": "Azienda Ospedaliera San Giovanni Addolorata",
            "eventContext": "Rome Digital Festival — post-event backstage catering area (day 9 of 7-day policy)",
            "incidentDayOfCoverage": 9
        },
        "diagnosis": {
            "primaryDiagnosis": "Laceration of right thumb — catering knife injury, suture repair",
            "icdCode": "S61.111A",
            "icdDescription": "Open wound of right thumb with damage to nail, initial encounter",
            "clinicalNarrative": (
                "Patient suffered a 2.5cm laceration to the right thumb while cutting bread "
                "at a catering backstage area on the evening following the official festival "
                "close. Wound irrigated, 3 sutures placed. Discharged same day. "
                "Patient submitted claim 1 day after the incident. "
                "Investigation confirmed: Event 7 policy inception date 2026-04-10, "
                "coverage expires 2026-04-17 23:59 UTC. "
                "Incident occurred 2026-04-19 at 21:30 local Rome time (UTC+2) — "
                "equivalent to 2026-04-19 19:30 UTC. "
                "Incident is 2 days and ~20 hours outside the active coverage window."
            ),
            "documentsAvailable": [
                "pronto soccorso triage note",
                "wound repair record",
                "discharge letter",
                "policy certificate (inception 2026-04-10, expiry 2026-04-17)"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 150,
            "actualMedicalCostUSD": 210,
            "amountClaimed": 150,
            "amountApproved": 0,
            "amountDenied": 150,
            "denialBreakdown": (
                "Full claim denied. Incident timestamp (2026-04-19 19:30 UTC) falls outside "
                "the active Event 7 coverage window (2026-04-10 to 2026-04-17 23:59 UTC). "
                "The policy expired 2 days and 20 hours before the incident. "
                "Excluded under genesis-acute-v1 coverage window clause (EXCL_WIN): "
                "no coverage applies to incidents occurring after policy expiry."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Incident outside coverage period. "
                "Member should seek reimbursement via national health system (SSN Italy) "
                "or any other active travel or health policy."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "pronto soccorso triage note (timestamp confirmed)",
                "policy certificate (inception and expiry dates)",
                "discharge letter"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Coverage Window Clause (EXCL_WIN) — incident after policy expiry",
            "reviewNotes": (
                "Incident timestamp verified from hospital records: 2026-04-19 21:30 local "
                "(2026-04-19 19:30 UTC). Policy expired 2026-04-17 23:59 UTC. "
                "Gap: 43.5 hours post-expiry. No coverage extension applies. "
                "Denial is administrative — the clinical injury itself would have been "
                "eligible under Tier 1 criteria had it occurred within the policy window."
            ),
            "reviewCompletedHours": 2.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t1-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID"
        }
    },

    # ── EVT7-T2-DEN-002 ── Chronic COPD exacerbation / British Music Awards ───
    {
        "_comment": "--- EVENT 7 | DENIAL — Chronic disease management (EXCL_5.4) ---",
        "scenarioId": "EVT7-T2-DEN-002",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "denied": True,
        "patientProfile": {
            "age": 68,
            "sex": "M",
            "nationality": "US",
            "preExistingConditions": (
                "COPD GOLD Stage III (FEV1 38% predicted) — on triple inhaler therapy "
                "(LAMA/LABA/ICS); 4 documented exacerbations requiring hospitalisation in the "
                "past 12 months; home nebuliser user"
            ),
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "United Kingdom",
            "incidentCity": "London",
            "facilityType": "Imperial College Healthcare NHS Trust — Respiratory Medicine",
            "facilityName": "Charing Cross Hospital (Imperial College Healthcare NHS Trust)",
            "eventContext": "Brit Awards — indoor ceremony at O2 Arena, London",
            "incidentDayOfCoverage": 1
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute exacerbation of COPD (AECOPD) — moderate severity, overnight admission",
            "icdCode": "J44.1",
            "icdDescription": "Chronic obstructive pulmonary disease with acute exacerbation",
            "clinicalNarrative": (
                "Patient attended the awards ceremony and developed progressive dyspnoea "
                "and increased sputum production by mid-evening. SpO2 84% on air on arrival. "
                "FEV1 28% predicted (baseline 38%). CXR: hyperinflation, no consolidation, "
                "no pneumothorax. CRP 42 mg/L, WBC 10.4. "
                "Treated: nebulised salbutamol + ipratropium, IV hydrocortisone 200mg, "
                "oral prednisolone 40mg, oral doxycycline (Anthonisen Type 2 exacerbation). "
                "SpO2 improved to 92% on 2L O2. Overnight admission for continued monitoring. "
                "Discharged day 2 on prednisolone 30mg taper and updated COPD action plan. "
                "Respiratory consultant note: 'This is the patient's 5th hospitalised "
                "exacerbation in 13 months — management follows established chronic disease "
                "protocol.'"
            ),
            "documentsAvailable": [
                "ED respiratory assessment note",
                "CXR report",
                "spirometry (FEV1 on admission vs baseline)",
                "medication administration record",
                "respiratory consultant note",
                "previous hospitalisation summary (4 prior AECOPDs in 12 months)",
                "ward discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 2800,
            "amountClaimed": 500,
            "amountApproved": 0,
            "amountDenied": 500,
            "denialBreakdown": (
                "Full claim denied. Acute exacerbation of COPD in a patient with GOLD Stage III "
                "disease and 4 prior hospitalised exacerbations in 12 months constitutes "
                "management of a chronic progressive disease, not an acute de novo emergency event. "
                "The exacerbation pattern is an expected and recurrent feature of the patient's "
                "underlying condition. "
                "Excluded under genesis-acute-v1 Section 5.4 (Excluded Conditions: Chronic Disease "
                "Management) and EXCL_CTX (contextual chronic pattern). "
                "NOTE: this is factually distinct from, e.g., a non-COPD patient developing "
                "an acute viral pneumonia triggering a first-ever airway emergency — which would "
                "be covered. The determinative factor is the documented chronic recurrent pattern."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Recurrent AECOPD in advanced COPD — chronic disease management. "
                "genesis-acute-v1 Section 5.4 applies. Member's home insurer or Medicare/Medicaid "
                "may cover international treatment costs."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED respiratory assessment note",
                "respiratory consultant note",
                "prior AECOPD hospitalisation summary",
                "ward discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Section 5.4 — Chronic Disease Management + EXCL_CTX",
            "reviewNotes": (
                "COPD GOLD Stage III with 4 prior hospitalisations for AECOPD in 12 months. "
                "Respiratory consultant explicitly documents this as the 5th hospitalised "
                "exacerbation — consistent with an established pattern of chronic disease "
                "management, not an acute isolated emergency event. "
                "Section 5.4 applies. Denied."
            ),
            "reviewCompletedHours": 9.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID"
        }
    },

    # ── EVT7-T3-DEN-002 ── Fraudulent invoice / Kuala Lumpur convention ───────
    {
        "_comment": "--- EVENT 7 | DENIAL — Fraudulent invoice (EXCL_8.2) ---",
        "scenarioId": "EVT7-T3-DEN-002",
        "product": "genesis-event-7-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "denied": True,
        "patientProfile": {
            "age": 35,
            "sex": "M",
            "nationality": "CN",
            "preExistingConditions": "none declared",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T3-DEN-002"
        },
        "clinicalSetting": {
            "incidentCountry": "Malaysia",
            "incidentCity": "Kuala Lumpur",
            "facilityType": "Kuala Lumpur Convention Medical Clinic (alleged — address unverifiable)",
            "facilityName": "KLCC MedCentre (alleged)",
            "eventContext": "Malaysia Tech Expo — technology exhibition at KLCC Convention Centre",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute appendicitis — laparoscopic appendectomy (as claimed)",
            "icdCode": "K35.80",
            "icdDescription": "Other and unspecified acute appendicitis without abscess (as claimed)",
            "clinicalNarrative": (
                "Patient submitted a claim for emergency laparoscopic appendectomy with "
                "2-night ICU admission at 'KLCC MedCentre', Kuala Lumpur. "
                "Total invoice submitted: MYR 48,000 (~USD 10,200). "
                "INVESTIGATION FINDINGS: "
                "(1) Facility address does not exist — Malaysia MOH facility registry "
                "search returns no licensed hospital or clinic at the stated address. "
                "(2) Attending surgeon licence number (LS-2204-KL) cannot be verified against "
                "the Malaysian Medical Council register. "
                "(3) Invoice template is identical in layout and font to a fraudulent invoice "
                "template previously flagged by the Malaysian MOH Anti-Fraud Unit (case ref "
                "MOH-AF-2025-118) — known to be used by a fraud ring targeting travel insurers. "
                "(4) Patient's digital footprint (hotel check-in records, ride-share history, "
                "conference badge scans): patient was at the Petronas Towers skybridge tour "
                "and Pavilion KL shopping mall during the alleged hospitalisation period. "
                "(5) No ambulance or hospital admission record retrievable from MOH national "
                "hospital information system (MySejahtera integrated data)."
            ),
            "documentsAvailable": [
                "submitted invoice (KLCC MedCentre — unverifiable)",
                "alleged operative note (suspected fabricated)",
                "alleged ICU nursing chart (suspected fabricated)"
            ],
            "investigationFindings": [
                "Facility address does not exist in Malaysia MOH registry",
                "Surgeon licence number not found in Malaysian Medical Council database",
                "Invoice template matches known fraud ring template (MOH-AF-2025-118)",
                "Hotel, ride-share and conference badge records contradict claimed hospitalisation dates",
                "No MOH hospital admission record retrievable for patient during claim period"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 1000,
            "actualMedicalCostUSD": 10200,
            "amountClaimed": 1000,
            "amountApproved": 0,
            "amountDenied": 1000,
            "denialBreakdown": (
                "Full claim denied. Five independent lines of investigation confirm the "
                "submitted medical invoice is fabricated. The claimed procedure did not occur. "
                "Denied under genesis-acute-v1 Section 8.2 (Fraud and Misrepresentation). "
                "Event 7 policy voided retroactively. Fraud referral initiated."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "FULL DENIAL. Fraudulent claim — fabricated invoice and non-existent facility. "
                "Policy voided under Section 8.2. Referral made to Malaysian MOH Anti-Fraud Unit "
                "and Interpol financial crime desk."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "submitted invoice (flagged as fabricated)",
                "Malaysia MOH facility registry (negative search result)",
                "Malaysian Medical Council register (licence not found)",
                "MOH Anti-Fraud Unit template comparison report",
                "hotel and ride-share records (provided by patient's accommodation)",
                "conference badge scan log"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "DENIED",
            "exclusionClause": "genesis-acute-v1 Section 8.2 — Fraud and Misrepresentation",
            "reviewNotes": (
                "Multi-source investigation completed over 48 hours. Five independent "
                "evidence lines confirm the claim is fraudulent: non-existent facility, "
                "unverifiable clinician, known fraud template, contradicting location data, "
                "and absent MOH admission records. "
                "Claim denied, policy voided. Anti-fraud referral initiated."
            ),
            "reviewCompletedHours": 48.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t3-den-002",
            "intakeStatus": 5,
            "intakeStatusLabel": "DENIED",
            "approvedAmountUsdc": 0,
            "paidAmountUsdc": 0,
            "fundingLineCharged": None,
            "fundingLineAddress": None,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "VOID",
            "fraudReferralInitiated": True
        }
    },

    # ── EVT7-T2-REVIEW-001 ── Severe concussion, CT inconclusive / Seoul ──────
    {
        "_comment": "--- EVENT 7 | IN-FLIGHT / UNDER REVIEW — Concussion, CT motion artifact ---",
        "scenarioId": "EVT7-T2-REVIEW-001",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "inFlight": True,
        "patientProfile": {
            "age": 24,
            "sex": "M",
            "nationality": "AU",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 2,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-REVIEW-001"
        },
        "clinicalSetting": {
            "incidentCountry": "South Korea",
            "incidentCity": "Seoul",
            "facilityType": "Samsung Medical Center — Emergency Neurology",
            "facilityName": "Samsung Medical Center (Sungkyunkwan University School of Medicine)",
            "eventContext": "Seoul Ultra Music Festival — outdoor crowd surge near main stage barrier",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Severe concussion with confirmed loss of consciousness — CT inconclusive (motion artifact), specialist second-read pending",
            "icdCode": "S06.0X1A",
            "icdDescription": "Concussion with loss of consciousness of 30 minutes or less, initial encounter",
            "clinicalNarrative": (
                "Patient was pushed by crowd surge and struck head-first against a metal "
                "barrier post. Bystander confirmed loss of consciousness approximately 90 seconds. "
                "GCS on paramedic arrival: 12. GCS on ED arrival: 14. "
                "Significant ongoing headache, nausea, and two vomiting episodes. "
                "CT head performed: radiology report states 'No definitive acute intracranial "
                "abnormality identified. However, study quality is degraded by motion artifact "
                "particularly in bilateral temporal windows — subtle findings cannot be excluded.' "
                "Neurology team decision: CT is non-diagnostic due to artifact. "
                "Overnight admission for neurological observation (GCS q1h). "
                "Specialist neuroradiology second-read of the CT requested (ETA 24-48h). "
                "Decision pending: if second-read confirms intracranial pathology, "
                "MRI brain will be added and tier may be upgraded to T3."
            ),
            "documentsAvailable": [
                "paramedic handover record (LOC confirmed)",
                "ED neurological assessment note",
                "CT head report (motion artifact, non-diagnostic)"
            ],
            "documentsPending": [
                "Neuroradiology specialist second-read of CT head (ETA 24-48h)",
                "MRI brain (conditional — ordered if CT second-read shows pathology)"
            ],
            "claimSubmittedAt": "2026-04-22T08:10:00Z"
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 2600,
            "amountClaimed": 500,
            "amountApproved": 0,
            "amountReserved": 500,
            "amountDenied": 0,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Claim under active review. $500 reserved on genesis-event7-liquidity "
                "FundingLine pending neuroradiology second-read. "
                "Tier classification may be upgraded to T3 (benefit $1,000) if CT second-read "
                "or MRI confirms intracranial haematoma or contusion requiring ICU."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "paramedic handover record",
                "ED neurological assessment note",
                "CT head report (motion artifact)"
            ],
            "documentsPending": [
                "Neuroradiology specialist second-read (Samsung Medical Center radiology dept, ETA 24-48h)",
                "MRI brain (conditional on CT second-read outcome)"
            ],
            "tierPreClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "PENDING",
            "reviewBlockingReason": (
                "CT head is non-diagnostic due to motion artifact in bilateral temporal "
                "windows. Neuroradiology specialist second-read has been formally requested. "
                "Cannot finalise tier classification without diagnostic imaging: "
                "if CT second-read or subsequent MRI reveals contusion or haematoma "
                "requiring ICU, this case will be reclassified to Tier 3. "
                "Currently pre-classified as Tier 2 (overnight admission confirmed; "
                "LOC <30 min confirmed by bystander account)."
            ),
            "reviewSlaDeadlineHours": 24,
            "reviewElapsedHours": 14,
            "reviewCompletedHours": None,
            "anticipatedApprovedRange": "$500 (T2) or $1,000 (T3) depending on imaging outcome"
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-review-001",
            "intakeStatus": 1,
            "intakeStatusLabel": "UNDER_REVIEW",
            "approvedAmountUsdc": 0,
            "reservedAmountUsdc": 500,
            "paidAmountUsdc": 0,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "RESERVED",
            "expectedResolutionNote": (
                "Pending neuroradiology CT second-read (ETA 24-48h). "
                "Anticipated outcome: FULLY_SETTLED $500 (Tier 2) if imaging negative; "
                "upgraded to FULLY_SETTLED $1,000 (Tier 3) if haematoma/contusion confirmed."
            )
        }
    }
]


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    before = len(data["event7Scenarios"])
    data["event7Scenarios"].extend(NEW_SCENARIOS)
    after = len(data["event7Scenarios"])

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Batch 4 done.")
    print("event7Scenarios: {} -> {}".format(before, after))
    print("travel30Scenarios unchanged: {}".format(len(data["travel30Scenarios"])))
    print("Total: {}".format(after + len(data["travel30Scenarios"])))


if __name__ == "__main__":
    main()
