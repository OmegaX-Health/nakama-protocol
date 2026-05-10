"""
KR 1.3 — Batch 5: TRV30-T1-005 through TRV30-T1-008
4 new Travel 30 Tier 1 (ER same-day) scenarios.
Incident countries: New Zealand, Barbados, Czech Republic, Vietnam.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

T30_POLICY_SERIES = "29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco"
HEALTH_PLAN       = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR          = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
T30_PREMIUMS_FL   = "8548dWwZAxPLR9mX4FWWASA1qatNj4hEgLDAmjRVWwLe"

NEW_SCENARIOS = [

    # ── TRV30-T1-005 ── Allergic conjunctivitis / Auckland, New Zealand ───────
    {
        "_comment": "--- TRAVEL 30 | TIER 1 — ER SAME-DAY (new batch, x4) ---",
        "scenarioId": "TRV30-T1-005",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 52,
            "sex": "F",
            "nationality": "GB",
            "originCountry": "United Kingdom",
            "destinationCountry": "New Zealand",
            "preExistingConditions": "mild seasonal hay fever (UK, spring — no NZ travel history)",
            "policyInceptionDaysAgo": 10,
            "memberWalletSim": "sim-member-wallet-TRV30-T1-005"
        },
        "clinicalSetting": {
            "incidentCountry": "New Zealand",
            "incidentCity": "Auckland",
            "facilityType": "Auckland City Hospital — Emergency Department",
            "facilityName": "Auckland City Hospital (Te Whatu Ora — Health New Zealand)",
            "eventContext": "Leisure travel — cultural and nature tourism, Auckland waterfront",
            "incidentDayOfCoverage": 10
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute bilateral allergic conjunctivitis — pohutukawa pollen exposure",
            "icdCode": "H10.13",
            "icdDescription": "Acute atopic conjunctivitis, bilateral",
            "clinicalNarrative": (
                "Patient developed sudden-onset bilateral eye redness, intense pruritus, "
                "profuse watery discharge, and periorbital swelling after walking through "
                "Auckland Botanic Gardens during the pohutukawa (Metrosideros excelsa) bloom "
                "season. Symptoms onset within 30 minutes of pollen exposure. "
                "Unable to open eyes on ED arrival. "
                "Slit-lamp examination: bilateral papillary conjunctival reaction, "
                "chemosis (3+), no corneal involvement, no fluorescein staining. "
                "Treatment: topical olopatadine 0.1% (antihistamine/mast cell stabiliser) "
                "bilateral, oral cetirizine 10mg, cool compresses. "
                "IV chlorphenamine 10mg for rapid symptom relief given severity on presentation. "
                "Symptoms reduced to mild within 3 hours. Discharged same day with 7-day "
                "topical antihistamine course and pollen avoidance advice."
            ),
            "documentsAvailable": [
                "ED triage note",
                "ophthalmology assessment (slit-lamp findings)",
                "medication administration record",
                "discharge summary with pollen avoidance advice"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 420,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 420,
            "amountClaimed": 420,
            "amountApproved": 420,
            "amountDenied": 0,
            "denialBreakdown": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid mode. Acute allergic conjunctivitis — ER same-day. "
                "All invoiced costs are medical and within NZ UCR schedule. "
                "Full amount approved. Background UK hay fever does not exclude "
                "an acute reaction to a novel allergen (NZ pohutukawa pollen)."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note",
                "ophthalmology assessment",
                "discharge summary"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Acute bilateral allergic conjunctivitis with chemosis — ER same-day discharge. "
                "NZ pohutukawa pollen is a distinct allergen from UK grass/tree pollens; "
                "the pre-existing hay fever does not constitute a pre-existing condition "
                "exclusion for this acute episode. Full invoice within UCR. Approved."
            ),
            "reviewCompletedHours": 4.5
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t1-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 420,
            "paidAmountUsdc": 420,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T1-006 ── Severe motion sickness + dehydration / Barbados ───────
    {
        "scenarioId": "TRV30-T1-006",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 61,
            "sex": "F",
            "nationality": "DE",
            "originCountry": "Germany",
            "destinationCountry": "Caribbean (cruise)",
            "preExistingConditions": "mild motion susceptibility (car sickness history — no prior severe episodes at sea)",
            "policyInceptionDaysAgo": 3,
            "memberWalletSim": "sim-member-wallet-TRV30-T1-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Barbados",
            "incidentCity": "Bridgetown",
            "facilityType": "Queen Elizabeth Hospital Barbados — Emergency Department",
            "facilityName": "Queen Elizabeth Hospital (QEH), Barbados",
            "eventContext": "Caribbean cruise — transatlantic crossing, Force 7 sea state day 3",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Severe motion sickness with dehydration — IV rehydration required",
            "icdCode": "T75.3XXA",
            "icdDescription": "Motion sickness, initial encounter",
            "clinicalNarrative": (
                "Patient experienced severe continuous vomiting (12+ episodes over 8 hours) "
                "during Force 7 (near-gale) sea conditions in the mid-Atlantic. "
                "Ship's medical officer assessed: unable to retain oral fluids, "
                "clinical dehydration with orthostatic hypotension (BP supine 112/70, "
                "BP standing 84/52). "
                "IV access established on board but IV antiemetic supply depleted. "
                "Decision: emergency disembarkation at Bridgetown port. "
                "QEH Barbados ED: IV ondansetron 4mg + IV Ringer's lactate 2.5L over 4 hours. "
                "Oral fluid tolerated by hour 3. Orthostasis resolved. "
                "Scopolamine transdermal patch applied for continued prophylaxis. "
                "Discharged same day with oral ondansetron and instructions."
            ),
            "documentsAvailable": [
                "ship medical officer assessment note",
                "QEH ED triage and assessment note",
                "IV fluid and antiemetic administration record",
                "orthostatic BP measurements",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 780,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 780,
            "amountClaimed": 780,
            "amountApproved": 640,
            "amountDenied": 140,
            "denialBreakdown": (
                "Port disembarkation transport surcharge $140 denied — vessel transfer to shore "
                "is classified as a logistical cost, not a medical service, under Travel 30 UCR schedule."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Acute dehydration from motion sickness requiring IV rehydration "
                "in hospital — covered acute event. Transport surcharge excluded per UCR."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ship medical officer note",
                "QEH ED assessment note",
                "IV fluid record",
                "discharge summary"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Severe motion sickness with clinical dehydration — IV rehydration required, "
                "same-day discharge. Medical costs $640 approved per Barbados UCR schedule. "
                "Port transfer surcharge $140 is a logistical cost, not a medical service — denied."
            ),
            "reviewCompletedHours": 5.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t1-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 640,
            "paidAmountUsdc": 640,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T1-007 ── Early Lyme disease / Czech Republic hiking ────────────
    {
        "scenarioId": "TRV30-T1-007",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 39,
            "sex": "M",
            "nationality": "US",
            "originCountry": "United States",
            "destinationCountry": "Czech Republic",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 4,
            "memberWalletSim": "sim-member-wallet-TRV30-T1-007"
        },
        "clinicalSetting": {
            "incidentCountry": "Czech Republic",
            "incidentCity": "Prague",
            "facilityType": "Motol University Hospital — Emergency and Infectious Disease",
            "facilityName": "Fakultni nemocnice v Motole (FN Motol)",
            "eventContext": "Leisure travel — hiking in Sumava National Park (Bohemian Forest)",
            "incidentDayOfCoverage": 4
        },
        "diagnosis": {
            "primaryDiagnosis": "Early localised Lyme borreliosis — erythema migrans, oral doxycycline initiated",
            "icdCode": "A69.20",
            "icdDescription": "Lyme disease, unspecified",
            "clinicalNarrative": (
                "Patient noticed an expanding annular skin lesion on left calf on day 4 of "
                "hiking in the Sumava forest area (high Ixodes ricinus tick density zone). "
                "Reported tick bite 3 days prior (removed with tweezers within 24h). "
                "On ED presentation: characteristic erythema migrans 14cm diameter, "
                "classic target morphology, no central clearing. "
                "No systemic symptoms (no fever, no arthralgias, no neurological symptoms). "
                "Infectious disease assessment: clinical diagnosis of early localised Lyme "
                "borreliosis based on EM morphology in endemic area post-tick bite. "
                "Lyme serology (ELISA) borderline IgM — confirmed clinical diagnosis. "
                "Treatment: oral doxycycline 100mg BD x 14 days. "
                "No IV treatment required (early localised presentation). "
                "Discharged same day with instructions and 2-week follow-up."
            ),
            "documentsAvailable": [
                "ED triage note",
                "infectious disease specialist assessment note",
                "erythema migrans clinical photograph (attached to records)",
                "Lyme serology result (IgM borderline positive)",
                "prescription for doxycycline",
                "discharge letter"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 360,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 360,
            "amountClaimed": 360,
            "amountApproved": 340,
            "amountDenied": 20,
            "denialBreakdown": (
                "Administrative registration fee CZK 500 (~$20) denied — "
                "non-medical administrative charge not covered under Travel 30 UCR schedule."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Acute Lyme disease — ER diagnosis and prescription. "
                "Medical costs $340 approved. Administrative registration fee $20 excluded."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note",
                "infectious disease assessment note",
                "Lyme serology result",
                "discharge letter"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Early Lyme borreliosis — EM confirmed clinically in endemic area, serology "
                "supportive. ER consultation and oral doxycycline prescription. Same-day discharge. "
                "$340 approved per Czech UCR schedule. Admin registration fee $20 denied."
            ),
            "reviewCompletedHours": 4.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t1-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 340,
            "paidAmountUsdc": 340,
            "fundingLineCharged": "genesis-travel30-premiums",
            "fundingLineAddress": T30_PREMIUMS_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T1-008 ── Volar plate finger fracture / Hanoi, Vietnam ──────────
    {
        "scenarioId": "TRV30-T1-008",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 44,
            "sex": "M",
            "nationality": "AU",
            "originCountry": "Australia",
            "destinationCountry": "Vietnam",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 6,
            "memberWalletSim": "sim-member-wallet-TRV30-T1-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Vietnam",
            "incidentCity": "Hanoi",
            "facilityType": "Vinmec International Hospital Hanoi — Emergency Department",
            "facilityName": "Vinmec International Hospital Times City, Hanoi",
            "eventContext": "Business travel — client meeting, taxi door incident",
            "incidentDayOfCoverage": 6
        },
        "diagnosis": {
            "primaryDiagnosis": "Volar plate avulsion fracture — right index finger PIP joint, closed reduction and splinting",
            "icdCode": "S63.644A",
            "icdDescription": "Other injury of intrinsic muscle, fascia and tendon of right index finger at wrist and hand level, initial encounter",
            "clinicalNarrative": (
                "Patient's right index finger was caught in a taxi door as it closed. "
                "Immediate pain and swelling at right index PIP joint. Unable to flex PIP. "
                "X-ray: small volar plate avulsion fracture at the base of the middle phalanx "
                "(PIP joint volar lip) — fragment 3mm x 2mm. No rotational deformity. "
                "Neurovascular exam: intact digital nerves and capillary refill. "
                "Hand surgeon assessment: closed injury, no displacement requiring ORIF. "
                "Management: closed reduction technique + dorsal extension block splint "
                "(PIP joint held at 30 degrees flexion). Tendon and nerve function confirmed intact "
                "post-splinting. Discharged same day with splint wear instructions "
                "x 4-6 weeks, NSAID analgesia, and hand therapy referral."
            ),
            "documentsAvailable": [
                "ED triage note",
                "hand surgeon assessment note",
                "X-ray right index finger report (volar plate avulsion confirmed)",
                "closed reduction and splinting procedure note",
                "pharmacy prescription (NSAID)",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 510,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 510,
            "amountClaimed": 510,
            "amountApproved": 470,
            "amountDenied": 40,
            "denialBreakdown": (
                "Outpatient pharmacy (NSAID pack) $40 denied — "
                "outpatient pharmacy costs excluded under Travel 30 Tier 1 base terms "
                "unless dispensed as part of an inpatient admission."
            ),
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid. Acute finger fracture with same-day ER management. "
                "Hospital and specialist costs $470 approved per Vietnam UCR schedule. "
                "Outpatient pharmacy $40 excluded per product terms."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note",
                "hand surgeon assessment note",
                "X-ray report",
                "splinting procedure note",
                "discharge summary"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED_PARTIAL",
            "reviewNotes": (
                "Volar plate avulsion fracture — X-ray and hand surgeon note confirm. "
                "Closed reduction and extension block splinting. Same-day discharge. "
                "$470 hospital + specialist approved per Vietnam UCR. "
                "Outpatient NSAID pharmacy $40 denied per Travel 30 base terms."
            ),
            "reviewCompletedHours": 5.5
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t1-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 470,
            "paidAmountUsdc": 470,
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

    print("Batch 5 done.")
    print("event7Scenarios unchanged: {}".format(len(data["event7Scenarios"])))
    print("travel30Scenarios: {} -> {}".format(before, after))
    print("Total: {}".format(len(data["event7Scenarios"]) + after))


if __name__ == "__main__":
    main()
