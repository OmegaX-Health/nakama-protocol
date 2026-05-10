"""
KR 1.3 — Batch 3: EVT7-T3-005 through EVT7-T3-008
4 new Event 7 Tier 3 (surgery + ICU, >= 2 nights) scenarios.
Incident countries: Kenya, Mexico, South Korea, Germany.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

E7_POLICY_SERIES = "6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX"
HEALTH_PLAN      = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR         = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
E7_LIQUIDITY_FL  = "Hw6LdQpUqiUShzocvt7R1qxkkiiZiWeWjEoR1Ehx3SLw"

# T3: 1000 in claimFinancials, 1000 on-chain (matches existing pattern)

NEW_SCENARIOS = [

    # ── EVT7-T3-005 ── Perforated appendix + peritoneal lavage / Nairobi ─────
    {
        "_comment": "--- EVENT 7 | TIER 3 — SURGERY + ICU (new batch, x4) ---",
        "scenarioId": "EVT7-T3-005",
        "product": "genesis-event-7-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 44,
            "sex": "M",
            "nationality": "KE",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 2,
            "memberWalletSim": "sim-member-wallet-EVT7-T3-005"
        },
        "clinicalSetting": {
            "incidentCountry": "Kenya",
            "incidentCity": "Nairobi",
            "facilityType": "The Nairobi Hospital — Emergency and General Surgery",
            "facilityName": "The Nairobi Hospital",
            "eventContext": "Nairobi Tech Summit — annual technology and investment conference, KICC",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Perforated appendix with localised peritonitis — emergency open appendectomy and peritoneal lavage",
            "icdCode": "K35.20",
            "icdDescription": "Acute appendicitis with generalised peritonitis, without mention of peritoneal abscess",
            "clinicalNarrative": (
                "Patient had dismissed progressively worsening abdominal pain for 3 days "
                "prior (thought it was food intolerance). On day 3 of conference presented "
                "to ED: rigid abdomen, guarding and rebound, temperature 39.2 degrees Celsius, "
                "HR 112, BP 104/68. WBC 24,800, CRP 310 mg/L. "
                "CT abdomen: perforated appendix with periappendiceal free air and "
                "localised right iliac fossa collection (4.2cm). "
                "Emergency open appendectomy via Lanz incision: perforated gangrenous appendix "
                "with faecolith. Peritoneal lavage with 3L warm saline. No bowel resection required. "
                "Abdomen closed primarily. Duration 75 minutes. "
                "Post-operative ICU: 2 nights (sepsis monitoring, IV piperacillin/tazobactam, "
                "haemodynamic stability). Surgical ward: nights 3 and 4. "
                "Apyrexial and tolerating diet by day 4. Discharged day 5."
            ),
            "documentsAvailable": [
                "ED assessment and surgical consultation note",
                "CT abdomen/pelvis report",
                "WBC and CRP laboratory results",
                "operative note (open appendectomy + peritoneal lavage)",
                "anaesthesia record",
                "ICU nursing charts (nights 1-2)",
                "surgical ward chart",
                "discharge summary with antibiotic plan"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 1000,
            "actualMedicalCostUSD": 7200,
            "amountClaimed": 1000,
            "amountApproved": 1000,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 3 maximum. Emergency surgery (appendectomy + peritoneal "
                "lavage) + ICU 2 nights confirmed. Full $1,000 benefit disbursed. "
                "Perforated appendicitis is an acute, life-threatening surgical emergency — "
                "not related to any pre-existing condition."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "CT abdomen report",
                "operative note",
                "ICU nursing charts (nights 1-2)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Perforated gangrenous appendicitis: emergency open surgery confirmed, "
                "ICU nights 1-2 documented. All Tier 3 criteria met (emergency surgery + "
                "ICU + minimum 2 nights in-hospital). No pre-existing condition relevant. "
                "Full fixed benefit approved."
            ),
            "reviewCompletedHours": 20.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t3-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 1000,
            "paidAmountUsdc": 1000,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T3-006 ── Epidural hematoma / Mexico City Design Week ────────────
    {
        "scenarioId": "EVT7-T3-006",
        "product": "genesis-event-7-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 37,
            "sex": "M",
            "nationality": "MX",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T3-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Mexico",
            "incidentCity": "Mexico City",
            "facilityType": "Hospital General de Mexico Dr. Eduardo Liceaga — Neurosurgery",
            "facilityName": "Hospital General de Mexico",
            "eventContext": "Mexico City Design Week — gallery opening event, Colonia Roma",
            "incidentDayOfCoverage": 1
        },
        "diagnosis": {
            "primaryDiagnosis": "Acute traumatic epidural haematoma — emergency craniotomy and haematoma evacuation",
            "icdCode": "S06.4X1A",
            "icdDescription": "Epidural haemorrhage with loss of consciousness of 30 minutes or less, initial encounter",
            "clinicalNarrative": (
                "Patient slipped on wet gallery floor and struck the right temporal region "
                "against a marble display plinth (corner impact). "
                "Initial GCS 15, mild headache, no LOC witnessed — walked away from scene. "
                "3 hours later: GCS deteriorated to 11, left-sided facial droop, unequal pupils "
                "(right 5mm sluggish, left 3mm reactive). "
                "Emergency CT head: right temporoparietal epidural haematoma 28mL, "
                "midline shift 7mm, right uncal herniation beginning. "
                "Emergency craniotomy — right pterional approach. Haematoma fully evacuated. "
                "Middle meningeal artery bleeding point identified and coagulated. "
                "Post-op GCS returned to 15 within 12 hours. "
                "Surgical ICU: 2 nights (ICP monitoring, neurological observations q1h). "
                "Neurology ward: nights 3-4. Discharged neurologically intact (GCS 15, "
                "no motor deficit) on day 5 with outpatient neurosurgery follow-up."
            ),
            "documentsAvailable": [
                "ED neurological assessment note",
                "CT head report (pre-operative)",
                "neurosurgery consent and operative note",
                "anaesthesia record",
                "ICU nursing chart (nights 1-2) with GCS trend",
                "post-operative CT head report",
                "neurology ward chart",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 1000,
            "actualMedicalCostUSD": 14500,
            "amountClaimed": 1000,
            "amountApproved": 1000,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 3 maximum. Emergency craniotomy for epidural haematoma "
                "with ICU 2 nights confirmed. Full $1,000 benefit disbursed. "
                "Classic 'talk and die' delayed deterioration pattern — acute traumatic event."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "CT head report",
                "operative note (craniotomy + haematoma evacuation)",
                "ICU nursing chart (nights 1-2)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Emergency craniotomy for traumatic epidural haematoma confirmed. "
                "ICU 2 nights with ICP monitoring documented. Tier 3 fully met. "
                "Delayed deterioration (lucid interval to GCS 11 over 3 hours) is classic "
                "EDH presentation — not inconsistent with the claim narrative. "
                "Accidental head trauma at gallery opening: covered."
            ),
            "reviewCompletedHours": 22.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t3-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 1000,
            "paidAmountUsdc": 1000,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T3-007 ── Compartment syndrome / K-Con Festival, Seoul ───────────
    {
        "scenarioId": "EVT7-T3-007",
        "product": "genesis-event-7-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 28,
            "sex": "M",
            "nationality": "JP",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 1,
            "memberWalletSim": "sim-member-wallet-EVT7-T3-007"
        },
        "clinicalSetting": {
            "incidentCountry": "South Korea",
            "incidentCity": "Seoul",
            "facilityType": "Asan Medical Center — Emergency & Orthopedic Surgery",
            "facilityName": "Asan Medical Center (Ulsan University Hospital of Medicine)",
            "eventContext": "KCON Korea — K-pop and Korean culture outdoor festival, Olympic Park",
            "incidentDayOfCoverage": 2
        },
        "diagnosis": {
            "primaryDiagnosis": "Traumatic compartment syndrome — right lower leg, emergency 4-compartment fasciotomy",
            "icdCode": "T79.A11A",
            "icdDescription": "Traumatic compartment syndrome of right lower extremity, initial encounter",
            "clinicalNarrative": (
                "Patient was forcibly compressed against a metal crowd-control barrier "
                "during a sudden surge toward the main stage. Initially ambulatory post-event, "
                "but developed progressive severe right calf pain and swelling over 4 hours. "
                "On arrival to Asan MC ED: right lower leg tense, woody swelling, "
                "pain out of proportion to passive stretch of toes. "
                "Compartment pressure measured (Stryker device): "
                "anterior 44 mmHg, lateral 38 mmHg, superficial posterior 41 mmHg, "
                "deep posterior 36 mmHg. Diastolic BP 78 mmHg. "
                "Delta P (diastolic - compartment pressure): anterior 34 mmHg — below 30 mmHg "
                "threshold in anterior compartment. Urgent surgical decision: fasciotomy. "
                "Emergency 4-compartment fasciotomy performed (two-incision technique, "
                "fibulectomy not required). Fasciotomy wounds left open. "
                "Myonecrosis: not present (viable muscle confirmed intraoperatively). "
                "Wound VAC applied day 1. ICU: 2 nights for limb perfusion monitoring "
                "and haemodynamic management (IV fluid resuscitation, urine output monitoring "
                "— CK peak 18,200 U/L, renal function preserved Cr 98 umol/L). "
                "Surgical ward: nights 3-4. Delayed primary wound closure performed day 4. "
                "Discharged day 6 with wound care plan and physiotherapy referral."
            ),
            "documentsAvailable": [
                "ED assessment note with compartment pressure measurements",
                "orthopedic surgical consent and operative note (fasciotomy)",
                "anaesthesia record",
                "intraoperative muscle viability assessment",
                "ICU nursing chart (nights 1-2) with CK trend and urine output",
                "wound VAC and closure procedure note",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 1000,
            "actualMedicalCostUSD": 11800,
            "amountClaimed": 1000,
            "amountApproved": 1000,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 3 maximum. Traumatic compartment syndrome — emergency "
                "fasciotomy + ICU 2 nights fully confirmed. Full $1,000 benefit disbursed. "
                "Crowd crush at festival: covered acute traumatic event."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "ED note with compartment pressure measurements",
                "operative note (4-compartment fasciotomy)",
                "ICU nursing chart (nights 1-2)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Compartment pressure measurements documented and meet surgical threshold. "
                "Emergency 4-compartment fasciotomy confirmed. ICU 2 nights for limb "
                "perfusion and rhabdomyolysis monitoring documented. "
                "All Tier 3 criteria met. Traumatic crush mechanism at music festival: covered."
            ),
            "reviewCompletedHours": 16.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t3-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 1000,
            "paidAmountUsdc": 1000,
            "fundingLineCharged": "genesis-event7-liquidity",
            "fundingLineAddress": E7_LIQUIDITY_FL,
            "policySeries": E7_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── EVT7-T3-008 ── Meningococcal meningitis / Berlin Music + Tech ─────────
    {
        "scenarioId": "EVT7-T3-008",
        "product": "genesis-event-7-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 31,
            "sex": "F",
            "nationality": "FR",
            "preExistingConditions": "none (MenACWY vaccination 4 years prior — MenB not administered)",
            "policyInceptionDaysAgo": 2,
            "memberWalletSim": "sim-member-wallet-EVT7-T3-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Germany",
            "incidentCity": "Berlin",
            "facilityType": "Charite Berlin — Campus Benjamin Franklin, Infectious Disease ICU",
            "facilityName": "Charite Universitatsmedizin Berlin (CBF Campus)",
            "eventContext": "Musikmesse Berlin — professional music industry trade fair and conference",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Bacterial meningococcal meningitis (Neisseria meningitidis serogroup B) — ICU admission",
            "icdCode": "A39.0",
            "icdDescription": "Meningococcal meningitis",
            "clinicalNarrative": (
                "Patient presented to hotel reception unable to stand, with severe headache, "
                "neck stiffness, photophobia, and a non-blanching petechial rash across trunk. "
                "Ambulance called; on arrival to Charite CBF: GCS 12, meningeal signs positive, "
                "petechial rash extending to lower limbs. Temp 39.8 degrees Celsius, HR 118, BP 102/64. "
                "IV ceftriaxone 2g + IV dexamethasone 10mg administered within 30 minutes of arrival "
                "(pre-LP empirical treatment, per AWMF guideline). "
                "Lumbar puncture: turbid CSF, opening pressure 28 cmH2O, "
                "WBC 2,400/uL (94% neutrophils), glucose 1.1 mmol/L (plasma 6.2), protein 3.8 g/L. "
                "CSF and blood culture: Neisseria meningitidis serogroup B. "
                "ICU admission: 3 nights (GCS monitoring, haemodynamic support, "
                "sodium management — SIADH developed night 1, corrected with fluid restriction). "
                "Neurology ward: nights 4-5. GCS returned to 15 by day 3. "
                "Hearing test performed (bilateral mild high-frequency sensorineural loss detected — "
                "audiology referral issued). Discharged day 6 on oral amoxicillin for remaining "
                "course and audiology follow-up."
            ),
            "documentsAvailable": [
                "ED triage and infectious disease assessment note",
                "lumbar puncture report with CSF analysis",
                "blood and CSF culture result (N. meningitidis serogroup B)",
                "antibiotic and dexamethasone administration record",
                "ICU nursing chart (nights 1-3) with GCS and sodium trend",
                "neurology ward chart",
                "audiology assessment",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 1000,
            "tierFixedBenefit": 1000,
            "actualMedicalCostUSD": 18600,
            "amountClaimed": 1000,
            "amountApproved": 1000,
            "amountDenied": 0,
            "denialReason": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Fixed-benefit Tier 3 maximum. ICU 3 nights for bacterial meningitis "
                "confirmed — no surgery required, but ICU admission of 2+ nights qualifies "
                "as Tier 3 under genesis-acute-v1 (surgery OR ICU >= 2 nights). "
                "Full $1,000 benefit disbursed."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "LP report and CSF culture (N. meningitidis serogroup B)",
                "ICU nursing chart (nights 1-3)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Meningococcal meningitis serogroup B confirmed by CSF culture. "
                "ICU admission 3 nights documented — exceeds the 2-night minimum for "
                "Tier 3 without requiring surgery (ICU >= 2 nights independently satisfies "
                "Tier 3 criteria under genesis-acute-v1). Full benefit approved."
            ),
            "reviewCompletedHours": 24.0
        },
        "onChainOutcome": {
            "claimCaseId": "evt7-t3-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 1000,
            "paidAmountUsdc": 1000,
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

    print("Batch 3 done.")
    print("event7Scenarios: {} -> {}".format(before, after))
    print("travel30Scenarios unchanged: {}".format(len(data["travel30Scenarios"])))
    print("Total: {}".format(after + len(data["travel30Scenarios"])))


if __name__ == "__main__":
    main()
