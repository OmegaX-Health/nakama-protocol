"""
KR 1.3 — Batch 6: TRV30-T2-005 through TRV30-T2-008
4 new Travel 30 Tier 2 (overnight admission) scenarios.
Incident countries: Turkey, Malaysia, UAE, Portugal.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

T30_POLICY_SERIES = "29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco"
HEALTH_PLAN       = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR          = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
T30_PREMIUMS_FL   = "8548dWwZAxPLR9mX4FWWASA1qatNj4hEgLDAmjRVWwLe"

NEW_SCENARIOS = [

    # ── TRV30-T2-005 ── Acute calculous cholecystitis / Istanbul ─────────────
    {
        "_comment": "--- TRAVEL 30 | TIER 2 — OVERNIGHT (new batch, x4) ---",
        "scenarioId": "TRV30-T2-005",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 49,
            "sex": "F",
            "nationality": "US",
            "originCountry": "United States",
            "destinationCountry": "Turkey",
            "preExistingConditions": "known gallstones (cholelithiasis, diagnosed 2 years ago — asymptomatic, no prior biliary colic episodes)",
            "policyInceptionDaysAgo": 7,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-005"
        },
        "clinicalSetting": {
            "incidentCountry": "Turkey",
            "incidentCity": "Istanbul",
            "facilityType": "Memorial Hospital Sisli — Emergency Surgery",
            "facilityName": "Memorial Sisli Hospital (Memorial Saglik Grubu)",
            "eventContext": "Leisure travel — culinary and cultural tour, traditional food market visit",
            "incidentDayOfCoverage": 7
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute calculous cholecystitis — conservative management, overnight admission",
            "icdCode": "K80.00",
            "icdDescription": "Calculous cholecystitis without obstruction",
            "clinicalNarrative": (
                "Patient developed severe right upper quadrant pain and fever (38.4 degrees C) "
                "after a high-fat traditional meal. "
                "Murphy's sign positive. WBC 13,800, CRP 88 mg/L. "
                "Ultrasound abdomen: gallbladder wall thickened 5.8mm, gallstone impacted "
                "in cystic duct, pericholecystic fluid — consistent with acute cholecystitis. "
                "Surgical assessment: fit for cholecystectomy, however patient declined "
                "definitive surgery in Turkey, requesting management as a bridge to home surgery. "
                "Conservative management initiated: IV piperacillin/tazobactam 4.5g TDS, "
                "IV fluids, NPO, analgesia (IV morphine + ketorolac). "
                "Overnight admission: temperature normalised by morning, WBC trending down "
                "to 10,200 at 16h. Tolerating sips by morning. Afebrile at discharge. "
                "Discharged day 2 with oral antibiotics, low-fat diet, "
                "and urgent surgical referral on return to US."
            ),
            "documentsAvailable": [
                "ED assessment and surgical consultation note",
                "abdominal ultrasound report",
                "WBC and CRP laboratory results",
                "IV antibiotic and fluid administration record",
                "temperature and clinical observation chart",
                "discharge summary with surgical referral"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 2100,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 2100,
            "amountClaimed": 2100,
            "amountApproved": 1850,
            "amountDenied": 250,
            "denialBreakdown": (
                "Private room daily surcharge $250 denied — "
                "exceeds standard room UCR rate for Istanbul private hospital. "
                "All medical costs (IV antibiotics, ultrasound, labs, physician fees) approved."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Acute cholecystitis — overnight medical management. "
                "Known asymptomatic gallstones are a pre-existing finding, but the acute "
                "cholecystitis episode itself is an acute event covered under Travel 30. "
                "Medical costs $1,850 approved; private room surcharge $250 denied."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED assessment and surgical note",
                "ultrasound report",
                "WBC/CRP results",
                "discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Acute cholecystitis confirmed by US + inflammatory markers. "
                "Overnight admission for conservative management appropriate — "
                "patient declined surgery in Turkey (medically valid choice). "
                "Known asymptomatic cholelithiasis: the calculous cholecystitis episode "
                "is an acute complication, not routine management of the asymptomatic stones. "
                "Medical costs $1,850 approved. Private room surcharge $250 denied. Tier 2 confirmed."
            ),
            "reviewCompletedHours": 9.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 1850,
            "paidAmountUsdc": 1850,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T2-006 ── Moderate scald burns / Kuala Lumpur ──────────────────
    {
        "scenarioId": "TRV30-T2-006",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 36,
            "sex": "M",
            "nationality": "SG",
            "originCountry": "Singapore",
            "destinationCountry": "Malaysia",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 5,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Malaysia",
            "incidentCity": "Kuala Lumpur",
            "facilityType": "Hospital Kuala Lumpur (HKL) — Burns Unit",
            "facilityName": "Hospital Kuala Lumpur (Ministry of Health Malaysia)",
            "eventContext": "Business travel — cafe meeting, hot beverage spill incident",
            "incidentDayOfCoverage": 5
        },
        "diagnosis": {
            "primaryDiagnosis": "Partial-thickness (second-degree) scald burns — right forearm and anterior chest, 8% TBSA",
            "icdCode": "T23.211A",
            "icdDescription": "Burn of second degree of right forearm, initial encounter",
            "clinicalNarrative": (
                "Patient was scalded when a server accidentally spilled a full pot of boiling "
                "coffee (estimated 92-95 degrees C) across his right forearm and anterior chest. "
                "Burns assessment in ED: right forearm 5% TBSA partial thickness (blistering), "
                "anterior chest 3% TBSA partial thickness — total 8% TBSA. "
                "No circumferential burns. No inhalation injury. "
                "Wound management: blisters debrided, silver sulfadiazine cream applied, "
                "non-adherent dressings (Mepitel). IV morphine for pain control. "
                "Admission to burns unit for overnight pain management, "
                "dressing protocol and monitoring for secondary infection. "
                "Daily dressing change performed under procedural sedation. "
                "No skin grafting required. "
                "Discharged day 2 with outpatient dressing protocol and burns clinic follow-up."
            ),
            "documentsAvailable": [
                "ED burns assessment note (% TBSA mapping diagram)",
                "burns surgeon consultation note",
                "wound management and dressing record",
                "IV morphine administration log",
                "burns unit nursing chart",
                "discharge summary with outpatient dressing instructions"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 3200,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 3200,
            "amountClaimed": 3000,
            "amountApproved": 2700,
            "amountDenied": 500,
            "denialBreakdown": (
                "Premium Mepitel dressing brand surcharge $500 denied — "
                "standard equivalent non-adherent dressing is within UCR; "
                "brand-specific premium is above UCR schedule for Kuala Lumpur burns unit."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Partial-thickness burns 8% TBSA — overnight burns unit "
                "admission. Medical costs $2,700 approved; premium dressing surcharge $500 denied. "
                "Accidental scald: covered acute event."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "burns assessment note (TBSA mapping)",
                "burns surgeon note",
                "burns unit nursing chart",
                "discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Partial-thickness scald burns 8% TBSA — overnight burns unit admission "
                "confirmed. No grafting, no ICU — Tier 2 appropriate. "
                "$2,700 approved per KL burns unit UCR. Premium dressing brand surcharge "
                "$500 exceeds UCR — denied. Accidental event covered."
            ),
            "reviewCompletedHours": 8.5
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 2700,
            "paidAmountUsdc": 2700,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T2-007 ── Hypertensive urgency / Abu Dhabi wellness retreat ─────
    {
        "scenarioId": "TRV30-T2-007",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 57,
            "sex": "M",
            "nationality": "ZA",
            "originCountry": "South Africa",
            "destinationCountry": "United Arab Emirates",
            "preExistingConditions": "essential hypertension (on amlodipine 10mg daily — known, controlled, not disclosed at policy purchase)",
            "policyInceptionDaysAgo": 14,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-007"
        },
        "clinicalSetting": {
            "incidentCountry": "United Arab Emirates",
            "incidentCity": "Abu Dhabi",
            "facilityType": "Cleveland Clinic Abu Dhabi — Emergency Department",
            "facilityName": "Cleveland Clinic Abu Dhabi",
            "eventContext": "Leisure travel — corporate wellness retreat, desert resort",
            "incidentDayOfCoverage": 14
        },
        "diagnosis": {
            "primaryDiagnosis": "Hypertensive urgency — BP 218/138 mmHg with severe headache, no acute end-organ damage",
            "icdCode": "I10",
            "icdDescription": "Essential (primary) hypertension",
            "clinicalNarrative": (
                "Patient ran out of amlodipine 4 days prior. Presented to ED with severe "
                "occipital headache and visual 'greyness'. "
                "BP on arrival: 218/138 mmHg (right arm), 212/134 mmHg (left arm). "
                "Hypertensive urgency workup: ECG sinus rhythm, no LVH changes; "
                "troponin negative; creatinine 92 umol/L (baseline unknown); "
                "urine dipstick: no proteinuria; fundoscopy: grade 2 hypertensive changes only "
                "(A/V nicking, no papilloedema, no flame haemorrhages). "
                "No hypertensive emergency criteria met. "
                "IV labetalol titration protocol: BP reduced to 178/102 at 1h, 158/96 at 4h. "
                "Overnight admission for BP stabilisation and medication restart. "
                "Morning BP 142/88 on oral amlodipine + lisinopril added. "
                "Discharged with updated antihypertensive regimen and cardiology follow-up letter."
            ),
            "documentsAvailable": [
                "ED triage and assessment note",
                "serial BP measurement chart",
                "ECG",
                "troponin and renal function results",
                "fundoscopy report",
                "IV labetalol administration record",
                "ward overnight observation chart",
                "discharge summary with medication update"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 2800,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 2800,
            "amountClaimed": 2800,
            "amountApproved": 2400,
            "amountDenied": 400,
            "denialBreakdown": (
                "Above-UCR specialist cardiology consultation fee $400 denied — "
                "Cleveland Clinic Abu Dhabi specialist surcharge exceeds Abu Dhabi UCR schedule "
                "for equivalent emergency hypertension management. "
                "All core ER, IV medication, and monitoring costs approved."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Hypertensive urgency — acute symptomatic episode requiring "
                "overnight management. Underlying hypertension is a pre-existing condition, "
                "but the acute hypertensive urgency with severe symptoms (BP 218/138, severe "
                "headache) constitutes a covered acute event under Travel 30. "
                "$2,400 approved; specialist surcharge $400 denied."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED assessment note",
                "serial BP chart",
                "end-organ damage workup results (ECG, troponin, renal, fundoscopy)",
                "discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Hypertensive urgency: BP 218/138 with severe headache, no end-organ damage "
                "confirmed by full workup. Overnight admission for IV BP reduction and "
                "medication restart — clinically appropriate. "
                "Pre-existing hypertension does not exclude acute symptomatic hypertensive "
                "urgency: this is an acute decompensation event (medication lapse), not routine "
                "chronic management. $2,400 approved. Specialist surcharge $400 denied."
            ),
            "reviewCompletedHours": 11.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 2400,
            "paidAmountUsdc": 2400,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T2-008 ── Transient ischaemic attack / Lisbon, Portugal ─────────
    {
        "scenarioId": "TRV30-T2-008",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 64,
            "sex": "M",
            "nationality": "CA",
            "originCountry": "Canada",
            "destinationCountry": "Portugal",
            "preExistingConditions": "hypercholesterolaemia (on atorvastatin 40mg)",
            "policyInceptionDaysAgo": 8,
            "memberWalletSim": "sim-member-wallet-TRV30-T2-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Portugal",
            "incidentCity": "Lisbon (Lisboa)",
            "facilityType": "Hospital de Santa Maria — Stroke Unit (Via Verde AVC)",
            "facilityName": "Centro Hospitalar Universitario Lisboa Norte (CHULN) — HSM",
            "eventContext": "Leisure travel — cultural holiday, Belem riverside walk",
            "incidentDayOfCoverage": 8
        },
        "diagnosis": {
            "primaryDiagnosis": "Transient ischaemic attack (TIA) — right hand weakness and expressive aphasia, fully resolved, stroke workup admission",
            "icdCode": "G45.9",
            "icdDescription": "Transient cerebral ischaemia, unspecified",
            "clinicalNarrative": (
                "Patient developed sudden right hand weakness and word-finding difficulty "
                "lasting approximately 20 minutes while walking along the Belem riverside. "
                "Symptoms fully resolved before ambulance arrival. "
                "ABCD2 score: 5 (high-risk — age 64, BP 168/94, clinical features, "
                "duration 10-59 min, no diabetes). "
                "Admitted directly to stroke unit (Via Verde AVC) protocol. "
                "MRI DWI brain: no acute infarct. "
                "Carotid duplex: mild left internal carotid stenosis 40% (not haemodynamically "
                "significant). Cardiac: 12-lead ECG sinus rhythm; 24h Holter monitoring initiated "
                "(no AF detected on inpatient recording). Transthoracic echocardiogram: "
                "mild LV diastolic dysfunction, no thrombus, no PFO. "
                "Treatment: aspirin 300mg loading, clopidogrel co-loading, atorvastatin "
                "increased to 80mg. "
                "Discharged day 2 with neurology outpatient follow-up and 7-day Holter monitor "
                "issued for continued AF screening."
            ),
            "documentsAvailable": [
                "ED triage and neurology assessment note",
                "ABCD2 score documentation",
                "MRI DWI brain report (no infarct)",
                "carotid duplex ultrasound report",
                "24h Holter monitoring result",
                "echocardiogram report",
                "antiplatelet and statin loading record",
                "discharge summary with outpatient plan"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 3600,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 3600,
            "amountClaimed": 3000,
            "amountApproved": 2890,
            "amountDenied": 710,
            "denialBreakdown": (
                "MRI brain surcharge above UCR $460 denied — public hospital private room "
                "supplement $250 denied. Core stroke workup (ED, carotid duplex, ECG, "
                "Holter, echocardiogram, medications) fully approved."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. TIA with high-risk features — overnight stroke workup "
                "admission appropriate and covered. Hypercholesterolaemia is pre-existing "
                "but does not exclude TIA as an acute vascular event. "
                "$2,890 approved (capped at $3,000 product maximum, post-denial); "
                "above-UCR surcharges $710 denied."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "neurology assessment note with ABCD2",
                "MRI DWI brain report",
                "carotid duplex report",
                "24h Holter result",
                "discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "TIA — fully resolved symptoms, MRI confirms no infarct. "
                "ABCD2 score 5 = high-risk: overnight admission for full stroke workup "
                "is clinically mandated (Portuguese and international TIA guidelines). "
                "Pre-existing hypercholesterolaemia does not exclude TIA. "
                "$2,890 approved; MRI and room surcharges above UCR denied ($710). "
                "Tier 2 confirmed."
            ),
            "reviewCompletedHours": 12.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t2-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 2890,
            "paidAmountUsdc": 2890,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
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

    print("Batch 6 done.")
    print("event7Scenarios unchanged: {}".format(len(data["event7Scenarios"])))
    print("travel30Scenarios: {} -> {}".format(before, after))
    print("Total: {}".format(len(data["event7Scenarios"]) + after))


if __name__ == "__main__":
    main()
