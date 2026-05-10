"""
KR 1.3 — Batch 1: EVT7-T1-005 through EVT7-T1-008
Adds 4 new Event 7 Tier 1 (ER same-day) scenarios with diverse
nationalities and incident countries to maximise generalisability.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

# ── shared constants ──────────────────────────────────────────────────────────
E7_POLICY_SERIES  = "6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX"
HEALTH_PLAN       = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR          = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
E7_PREMIUMS_FL    = "2115rGD6zKmUhLGk9zwqbA9tdcA5nuAwRNaQDLcgSpWA"

# T1 fixed benefit: 150 in claimFinancials, 300 on-chain (matches existing pattern)

NEW_SCENARIOS = [
    # ── EVT7-T1-005 ── Corneal abrasion / Dubai Art Week / UAE ───────────────
    {
        "_comment": "--- EVENT 7 | TIER 1 — ER SAME-DAY (new batch, x4) ---",
        "scenarioId": "EVT7-T1-005",
        "product": "genesis-event-7-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 33,
            "sex": "F",
            "nationality": "DE",
            "preExistingConditions": "daily soft contact lens wearer (no prior ocular pathology)",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T1-005"
        },
        "clinicalSetting": {
            "incidentCountry": "United Arab Emirates",
            "incidentCity": "Dubai",
            "facilityType": "American Hospital Dubai — Ophthalmology Emergency",
            "facilityName": "American Hospital Dubai",
            "eventContext": "Art Dubai — international modern and contemporary art fair at Madinat Jumeirah",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Traumatic corneal abrasion — right eye, contact lens related",
            "icdCode": "S05.01XA",
            "icdDescription": "Injury of conjunctiva and corneal abrasion without foreign body, right eye, initial encounter",
            "clinicalNarrative": (
                "Patient's soft contact lens shifted and became dislodged while walking through "
                "an outdoor sculpture garden in a sandstorm advisory (Shamal wind conditions). "
                "Attempted lens repositioning caused a corneal abrasion (right eye). "
                "Slit-lamp examination: linear epithelial defect 4mm × 1.5mm at 3 o'clock, "
                "fluorescein-positive. No infiltrate, no anterior chamber reaction. "
                "Topical antibiotic (ofloxacin 0.3% QID × 5 days) and lubricating drops prescribed. "
                "Contact lens wear suspended for 7 days. No eye patching (current evidence base). "
                "Discharged with ophthalmology review in 48 hours."
            ),
            "documentsAvailable": [
                "ophthalmology emergency assessment note",
                "slit-lamp examination record",
                "fluorescein staining report",
                "pharmacy prescription",
                "discharge note"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 150,
            "actualMedicalCostUSD": 520,
            "amountClaimed": 150,
            "amountApproved": 150,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 1. ER ophthalmology visit, same-day discharge. "
                "Corneal abrasion is an acute accidental injury — covered under genesis-acute-v1. "
                "Contact lens-related aggravation does not constitute negligence exclusion."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ophthalmology emergency assessment note",
                "slit-lamp examination record",
                "discharge note"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Acute traumatic corneal abrasion confirmed by slit-lamp and fluorescein staining. "
                "Same-day discharge. No overnight admission. Tier 1 criteria met. "
                "Contact lens-related mechanism does not trigger exclusion — abrasion is accidental."
            ),
            "reviewCompletedHours": 4.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t1-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 300,
            "paidAmountUsdc": 300,
            "fundingLineCharged": "genesis-event7-premiums",
            "fundingLineAddress": E7_PREMIUMS_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T1-006 ── Dog bite + wound closure / Singapore FinTech Festival ─
    {
        "scenarioId": "EVT7-T1-006",
        "product": "genesis-event-7-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 42,
            "sex": "M",
            "nationality": "US",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 3,
            "memberWalletSim": "sim-member-wallet-EVT7-T1-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Singapore",
            "incidentCity": "Singapore",
            "facilityType": "Tan Tock Seng Hospital — Emergency Department",
            "facilityName": "Tan Tock Seng Hospital (TTSH)",
            "eventContext": "Singapore FinTech Festival — outdoor networking zone, marina promenade",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Dog bite — right forearm laceration requiring wound closure and rabies post-exposure prophylaxis (PEP)",
            "icdCode": "W54.0XXA",
            "icdDescription": "Bitten by dog, initial encounter",
            "clinicalNarrative": (
                "Patient was bitten by an unleashed dog near the marina networking area. "
                "Right forearm: 3.2cm full-thickness laceration with irregular edges, "
                "minor subcutaneous fat exposure, no tendon involvement. "
                "Wound copiously irrigated with 1L normal saline. "
                "Primary wound closure: 4 × 3-0 Vicryl deep sutures + 5 × 3-0 nylon skin sutures. "
                "Tetanus toxoid (Td) booster administered — last dose >10 years prior. "
                "Dog owner identified; vaccination records unavailable. "
                "Per Singapore MOH rabies PEP protocol (dog from unknown vaccination status): "
                "rabies immunoglobulin (HRIG) 20 IU/kg infiltrated wound + day-0 rabies vaccine (PCECV) "
                "initiated. Neurovascular exam: intact. Discharged same day with wound care "
                "instructions and PEP schedule (day 3, 7, 14, 28)."
            ),
            "documentsAvailable": [
                "ED triage note",
                "wound care and closure report",
                "tetanus immunization record",
                "HRIG and rabies vaccine administration record",
                "PEP schedule letter",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 150,
            "actualMedicalCostUSD": 890,
            "amountClaimed": 150,
            "amountApproved": 150,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 1. Acute accidental animal bite — covered. "
                "Rabies PEP initiation on day 0 is part of acute ER management, not a separate "
                "outpatient series claim. Tier 1 fixed benefit applies to this ER episode."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note",
                "wound closure report",
                "HRIG and vaccine administration record",
                "discharge summary"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Dog bite with laceration repair and same-day discharge confirmed. "
                "Rabies PEP initiation is standard acute management in Singapore for uncertain "
                "vaccination status — not an exclusion. Tier 1 criteria met. "
                "Subsequent PEP doses (day 3, 7, 14, 28) are outpatient follow-up and not "
                "additional claim events under the same policy cycle."
            ),
            "reviewCompletedHours": 5.5
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t1-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 300,
            "paidAmountUsdc": 300,
            "fundingLineCharged": "genesis-event7-premiums",
            "fundingLineAddress": E7_PREMIUMS_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T1-007 ── Epistaxis / Monza Music Week / Italy ──────────────────
    {
        "scenarioId": "EVT7-T1-007",
        "product": "genesis-event-7-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 26,
            "sex": "M",
            "nationality": "BR",
            "preExistingConditions": "mild intermittent allergic rhinitis (seasonal, not on therapy at time of event)",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T1-007"
        },
        "clinicalSetting": {
            "incidentCountry": "Italy",
            "incidentCity": "Monza (Milan metropolitan area)",
            "facilityType": "Pronto Soccorso — Ospedale San Gerardo di Monza",
            "facilityName": "ASST Monza — Ospedale San Gerardo",
            "eventContext": "Monza Circuit Music Festival — outdoor festival in the Autodromo grounds",
            "incidentDayOfCoverage": 1
        },
        "diagnosis": {
            "primaryDiagnosis": "Spontaneous epistaxis — anterior nasal cavity (Little's area), unilateral right",
            "icdCode": "R04.0",
            "icdDescription": "Epistaxis",
            "clinicalNarrative": (
                "Patient developed profuse right-sided epistaxis at the outdoor festival "
                "(dry, warm conditions — 32°C, low ambient humidity). "
                "Bleeding uncontrolled by pinching for 20 minutes; attended Pronto Soccorso. "
                "BP 128/80 (normal). No anticoagulant use. Anterior rhinoscopy: "
                "active bleeding from Little's area (right Kiesselbach plexus). "
                "Anterior packing with BIPP ribbon gauze × 1 strip + 20-minute compression. "
                "Bleeding controlled. Haemoglobin 13.8 g/dL (not significantly dropped). "
                "Patient observed 2 hours — no re-bleed. Packing removed in situ. "
                "Discharged with ENT clinic referral for possible cautery if recurrence."
            ),
            "documentsAvailable": [
                "pronto soccorso triage note",
                "ENT assessment note",
                "anterior nasal packing record",
                "discharge letter"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 150,
            "actualMedicalCostUSD": 280,
            "amountClaimed": 150,
            "amountApproved": 150,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 1. Acute spontaneous epistaxis — acute event, "
                "same-day discharge. Seasonal rhinitis is a pre-existing condition but "
                "does not exclude acute epistaxis under genesis-acute-v1 terms."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "pronto soccorso triage note",
                "ENT assessment note",
                "discharge letter"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Acute epistaxis requiring ER anterior nasal packing. Same-day discharge. "
                "No overnight admission. Background allergic rhinitis does not constitute "
                "a pre-existing condition exclusion for an acute epistaxis event — these are "
                "distinct clinical presentations. Tier 1 criteria met."
            ),
            "reviewCompletedHours": 3.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t1-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 300,
            "paidAmountUsdc": 300,
            "fundingLineCharged": "genesis-event7-premiums",
            "fundingLineAddress": E7_PREMIUMS_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T1-008 ── Acute urticaria + angioedema / Tokyo Game Show ────────
    {
        "scenarioId": "EVT7-T1-008",
        "product": "genesis-event-7-v1",
        "clinicalTier": 1,
        "tierLabel": "ER_SAME_DAY",
        "patientProfile": {
            "age": 29,
            "sex": "F",
            "nationality": "CA",
            "preExistingConditions": "known shellfish allergy (mild prior reaction — localized hives only; no prior anaphylaxis; carries no EpiPen)",
            "policyInceptionDaysAgo": 2,
            "memberWalletSim": "sim-member-wallet-EVT7-T1-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Japan",
            "incidentCity": "Chiba (Greater Tokyo Area)",
            "facilityType": "Emergency Department — Chiba University Hospital",
            "facilityName": "Chiba University Hospital (Chiba Daigaku Byoin)",
            "eventContext": "Tokyo Game Show — indoor consumer electronics and gaming expo, Makuhari Messe",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute allergic urticaria with lip and periorbital angioedema — suspected shellfish exposure",
            "icdCode": "L50.0",
            "icdDescription": "Allergic urticaria",
            "clinicalNarrative": (
                "Patient consumed fried food from an expo vendor. Within 20 minutes: "
                "generalised urticaria (trunk, arms, legs) + bilateral lip angioedema "
                "and periorbital oedema. No stridor, no dyspnea, no hypotension. "
                "BP 118/74, SpO2 99%, HR 94. "
                "IV diphenhydramine 50mg + IV ranitidine 50mg + IV methylprednisolone 40mg. "
                "Epinephrine 0.3mg IM administered (periorbital angioedema approaching airway risk). "
                "Observed 4 hours post-epinephrine (biphasic reaction protocol). "
                "Symptoms fully resolved. Discharged with oral prednisolone 25mg × 3 days, "
                "oral cetirizine, and EpiPen prescription."
            ),
            "documentsAvailable": [
                "ED triage note",
                "allergy assessment and medication record",
                "epinephrine administration record",
                "observation log (4-hour biphasic watch)",
                "discharge summary with EpiPen prescription"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 150,
            "actualMedicalCostUSD": 740,
            "amountClaimed": 150,
            "amountApproved": 150,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 1. Acute allergic reaction managed and discharged same day. "
                "Known allergy does not exclude acute allergic event — distinction between "
                "pre-existing condition (the allergy) and the acute episode (the reaction)."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage note",
                "allergy assessment and medication record",
                "epinephrine administration record",
                "discharge summary"
            ],
            "tierClassified": "TIER_1_ER_SAME_DAY",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Acute allergic urticaria with angioedema — ER management, same-day discharge. "
                "Known shellfish allergy is a pre-existing condition but is not an exclusion "
                "for the acute episode itself under genesis-acute-v1. "
                "4-hour observation post-epinephrine is standard of care and does not "
                "constitute overnight admission (patient discharged within same calendar day). "
                "Tier 1 criteria met."
            ),
            "reviewCompletedHours": 2.5
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t1-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 300,
            "paidAmountUsdc": 300,
            "fundingLineCharged": "genesis-event7-premiums",
            "fundingLineAddress": E7_PREMIUMS_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
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

    print(f"Batch 1 done. event7Scenarios: {before} → {after}")
    print(f"travel30Scenarios unchanged: {len(data['travel30Scenarios'])}")
    print(f"Total scenarios: {after + len(data['travel30Scenarios'])}")


if __name__ == "__main__":
    main()
