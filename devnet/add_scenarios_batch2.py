"""
KR 1.3 — Batch 2: EVT7-T2-005 through EVT7-T2-008
4 new Event 7 Tier 2 (overnight admission) scenarios.
Diverse incident countries: UAE, Netherlands, Turkey, Thailand.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

E7_POLICY_SERIES = "6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX"
HEALTH_PLAN      = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR         = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
E7_LIQUIDITY_FL  = "Hw6LdQpUqiUShzocvt7R1qxkkiiZiWeWjEoR1Ehx3SLw"

# T2 fixed benefit: 500 in claimFinancials, 700 on-chain (matches existing pattern)

NEW_SCENARIOS = [

    # ── EVT7-T2-005 ── Exercise-induced hyponatremia / Dubai Marathon ─────────
    {
        "_comment": "--- EVENT 7 | TIER 2 — OVERNIGHT (new batch, x4) ---",
        "scenarioId": "EVT7-T2-005",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 38,
            "sex": "M",
            "nationality": "AU",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-005"
        },
        "clinicalSetting": {
            "incidentCountry": "United Arab Emirates",
            "incidentCity": "Dubai",
            "facilityType": "Rashid Hospital — Emergency & Internal Medicine",
            "facilityName": "Rashid Hospital (Dubai Health Authority)",
            "eventContext": "Standard Chartered Dubai Marathon — mass participation road race (42.195km)",
            "incidentDayOfCoverage": 1
        },
        "diagnosis": {
            "primaryDiagnosis": "Exercise-associated hyponatremia (EAH) — severe, symptomatic",
            "icdCode": "E87.1",
            "icdDescription": "Hypo-osmolality and hyponatraemia",
            "clinicalNarrative": (
                "Patient finished the full marathon in 4h 22min in 26 degrees Celsius ambient "
                "temperature. Collapsed at finish line: GCS 13, nausea, headache, confusion. "
                "Na+ on point-of-care testing: 122 mEq/L (severe hyponatraemia). "
                "No seizures at presentation. BP 106/68. "
                "IV hypertonic saline 3% — 100mL bolus over 10 minutes repeated once (Na+ "
                "target rise 5 mEq/L in first hour). Symptoms improved: GCS 15 within 90 minutes. "
                "Slow correction continued overnight: Na+ 131 mEq/L at 8h, 137 mEq/L at 16h. "
                "Overshoot prevention protocol maintained (free water restriction). "
                "Renal function preserved (Cr 88 umol/L). Discharged following morning."
            ),
            "documentsAvailable": [
                "ED triage and assessment note",
                "serial electrolyte results (Na+ trend chart)",
                "IV fluid and hypertonic saline administration record",
                "GCS observation chart",
                "ward discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 3100,
            "amountClaimed": 500,
            "amountApproved": 500,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 2. Overnight admission for acute symptomatic hyponatraemia "
                "management confirmed. Marathon participation (planned physical activity) does not "
                "constitute negligence or self-inflicted injury under genesis-acute-v1 terms."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED triage and assessment note",
                "serial electrolyte results",
                "IV hypertonic saline record",
                "ward discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Severe symptomatic EAH requiring overnight admission for careful sodium "
                "correction confirmed. Na+ 122 mEq/L on arrival — clearly pathological. "
                "Overnight correction to 137 mEq/L documented. Marathon participation is "
                "recreational sport, not excluded activity. Tier 2 criteria met."
            ),
            "reviewCompletedHours": 7.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 700,
            "paidAmountUsdc": 700,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T2-006 ── Acute gout + septic arthritis workup / ADE Amsterdam ──
    {
        "scenarioId": "EVT7-T2-006",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 51,
            "sex": "M",
            "nationality": "GB",
            "preExistingConditions": "gout (on allopurinol 300mg daily — 3-year history, 2 prior flares)",
            "policyInceptionDaysAgo": 2,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Netherlands",
            "incidentCity": "Amsterdam",
            "facilityType": "Amsterdam UMC — Emergency Internal Medicine",
            "facilityName": "Amsterdam UMC (location AMC)",
            "eventContext": "Amsterdam Dance Event (ADE) — electronic music conference and festival week",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute crystal arthropathy (gout flare) — right knee monoarthritis with septic joint exclusion workup",
            "icdCode": "M10.061",
            "icdDescription": "Idiopathic gout, right knee",
            "clinicalNarrative": (
                "Patient developed acute right knee monoarthritis overnight (day 2/3 of festival). "
                "Known gout, but flare was atypical: unusual site (knee rather than first MTP), "
                "high fever 38.9 degrees Celsius, WBC 14,200, CRP 118 mg/L. "
                "Septic arthritis could not be excluded clinically — joint aspiration performed "
                "under sterile technique: cloudy synovial fluid, WBC 42,000/uL (90% neutrophils). "
                "Polarised microscopy: strongly negative birefringent needle-shaped crystals "
                "(monosodium urate — diagnostic of gout). Gram stain: negative. "
                "Bacterial culture: no growth at 24h. "
                "Treated: colchicine + IV ketorolac (NSAIDs) + joint aspiration drained 18mL. "
                "Overnight admission for fever monitoring and culture result. Discharged day 2 "
                "on oral colchicine taper and allopurinol dose review."
            ),
            "documentsAvailable": [
                "ED assessment note",
                "joint aspirate analysis report (polarised microscopy + culture)",
                "WBC and CRP lab results",
                "fever observation chart",
                "medication administration record",
                "ward discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 2400,
            "amountClaimed": 500,
            "amountApproved": 500,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 2. Overnight admission clinically justified: septic arthritis "
                "could not be excluded without culture result. Pre-existing gout does not exclude "
                "the acute flare episode — genesis-acute-v1 covers acute events even when an "
                "underlying condition pre-exists, provided the acute presentation is genuinely new."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED assessment note",
                "joint aspirate analysis (MSU crystals confirmed, culture negative)",
                "fever observation chart",
                "ward discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Acute gout flare with clinically justified overnight admission for septic "
                "arthritis exclusion. Joint aspiration confirmed MSU crystals; culture negative. "
                "Overnight stay was medically necessary pending bacterial culture result — "
                "not administrative convenience. Pre-existing gout history does not trigger "
                "exclusion for the acute flare under genesis-acute-v1. Tier 2 confirmed."
            ),
            "reviewCompletedHours": 10.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 700,
            "paidAmountUsdc": 700,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T2-007 ── Multiple rib fractures / Istanbul Music Festival ───────
    {
        "scenarioId": "EVT7-T2-007",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 34,
            "sex": "F",
            "nationality": "US",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-007"
        },
        "clinicalSetting": {
            "incidentCountry": "Turkey",
            "incidentCity": "Istanbul",
            "facilityType": "Liv Hospital Bahcesehir — Emergency & Trauma Surgery",
            "facilityName": "Liv Hospital Bahcesehir",
            "eventContext": "Istanbul Music Festival — outdoor venue, temporary scaffold viewing platform",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Multiple left-sided rib fractures (ribs 5-8) — blunt chest trauma from fall",
            "icdCode": "S22.40XA",
            "icdDescription": "Multiple fractures of ribs, unspecified side, initial encounter for closed fracture",
            "clinicalNarrative": (
                "Patient fell approximately 1.5 metres from an overcrowded temporary scaffold "
                "platform at the festival grounds, landing left-side down on a metal barrier. "
                "On arrival: moderate left-sided chest wall pain, splinted breathing, "
                "SpO2 96% on air. BP 122/78. "
                "CT chest: displaced fractures of left ribs 5, 6, 7, 8 (posterior segments) — "
                "no pneumothorax, no haemothorax, no flail segment. "
                "Intercostal nerve block (4-level) with bupivacaine under ultrasound guidance. "
                "IV morphine PCA initiated. Incentive spirometry commenced. "
                "Overnight admission: respiratory physiotherapy, analgesia optimisation, "
                "SpO2 monitoring. SpO2 99% by morning. Discharged with rib belt, "
                "oral analgesia and respiratory physiotherapy instructions."
            ),
            "documentsAvailable": [
                "ED trauma assessment note",
                "CT chest radiology report",
                "intercostal nerve block procedure note",
                "PCA morphine administration log",
                "respiratory physiotherapy note",
                "ward discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 3800,
            "amountClaimed": 500,
            "amountApproved": 500,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 2. Overnight admission for pain management and respiratory "
                "monitoring after multiple rib fractures — clinically appropriate. "
                "Accidental fall from scaffold: covered acute traumatic event."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED trauma assessment note",
                "CT chest report",
                "intercostal nerve block note",
                "ward discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Multiple rib fractures (4 ribs, displaced) confirmed by CT — overnight "
                "admission for pain management and respiratory monitoring is clinically "
                "appropriate and expected for this injury pattern. No ICU, no surgical "
                "intervention — Tier 2 (not Tier 3) confirmed. Accidental trauma covered."
            ),
            "reviewCompletedHours": 8.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 700,
            "paidAmountUsdc": 700,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T2-008 ── Primary spontaneous pneumothorax / Bangkok festival ────
    {
        "scenarioId": "EVT7-T2-008",
        "product": "genesis-event-7-v1",
        "clinicalTier": 2,
        "tierLabel": "OVERNIGHT",
        "patientProfile": {
            "age": 22,
            "sex": "M",
            "nationality": "NL",
            "preExistingConditions": "tall, lean build (189cm, 72kg) — no prior respiratory history, no known Marfan syndrome",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T2-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Thailand",
            "incidentCity": "Bangkok",
            "facilityType": "Bumrungrad International Hospital — Emergency Department",
            "facilityName": "Bumrungrad International Hospital",
            "eventContext": "S2O Songkran Music Festival — large outdoor electronic music event",
            "incidentDayOfCoverage": 1
        },
        "diagnosis": {
            "primaryDiagnosis": "Primary spontaneous pneumothorax (PSP) — right-sided, moderate",
            "icdCode": "J93.11",
            "icdDescription": "Primary spontaneous pneumothorax",
            "clinicalNarrative": (
                "Patient developed sudden-onset right-sided pleuritic chest pain and dyspnoea "
                "while dancing at the festival. No trauma. "
                "CXR: right pneumothorax — lung collapsed to 35% of hemithorax. "
                "SpO2 94% on air. "
                "Intercostal chest tube drain inserted under local anaesthesia: "
                "16Fr Seldinger technique, right 4th intercostal space mid-axillary line. "
                "Immediate re-expansion confirmed on CXR post-drain. "
                "SpO2 improved to 99%. Drain placed on underwater seal. "
                "Overnight admission: drain patency and re-expansion monitoring. "
                "Repeat CXR morning: full lung re-expansion maintained. "
                "Drain clamped 4h, no recollapse — drain removed. "
                "Discharged with follow-up CXR in 2 weeks and CT thorax referral to "
                "evaluate for blebs/bullae."
            ),
            "documentsAvailable": [
                "ED assessment note",
                "CXR report (initial and post-drain)",
                "chest drain insertion procedure note",
                "underwater seal drainage log",
                "ward nursing observation chart",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 500,
            "actualMedicalCostUSD": 4200,
            "amountClaimed": 500,
            "amountApproved": 500,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 2. Overnight admission with chest drain for moderate "
                "spontaneous pneumothorax. No surgery, no ICU — Tier 2 (not Tier 3). "
                "Spontaneous pneumothorax is an acute event, not a pre-existing condition."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED assessment note",
                "CXR report (initial + post-drain)",
                "chest drain procedure note",
                "ward discharge summary"
            ],
            "tierClassified": "TIER_2_OVERNIGHT",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Primary spontaneous pneumothorax — moderate, managed with intercostal chest "
                "drain and overnight admission. Confirmed by CXR. No thoracoscopic surgery, "
                "no mechanical ventilation, no ICU — Tier 2 appropriate (chest drain + "
                "overnight does not meet Tier 3 threshold without surgical intervention or "
                "ICU admission). No pre-existing condition exclusion applicable. Approved."
            ),
            "reviewCompletedHours": 6.5
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t2-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 700,
            "paidAmountUsdc": 700,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
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

    print("Batch 2 done.")
    print("event7Scenarios: {} -> {}".format(before, after))
    print("travel30Scenarios unchanged: {}".format(len(data["travel30Scenarios"])))
    print("Total: {}".format(after + len(data["travel30Scenarios"])))


if __name__ == "__main__":
    main()
