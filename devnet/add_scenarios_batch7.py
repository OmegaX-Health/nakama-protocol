"""
KR 1.3 — Batch 7: TRV30-T3-005 through TRV30-T3-008
4 new Travel 30 Tier 3 (surgery + ICU) scenarios.
Incident countries: Thailand, Mexico, Kenya, Singapore.
All hit product max $3,000 — funded by travel30-liquidity.
"""
import json, pathlib

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

T30_POLICY_SERIES = "29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco"
HEALTH_PLAN       = "D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6"
OPERATOR          = "BGN6pVpuD9GPSsExtBi7pe4RLCJrkFVsQd9mw7ZdH8Ez"
T30_LIQUIDITY_FL  = "HBrdsf7UjYK5tRoM9j6YaxfV7nFBkVhnJbrmTLVaDiEr"

NEW_SCENARIOS = [

    # ── TRV30-T3-005 ── Ruptured ectopic pregnancy / Bangkok, Thailand ────────
    {
        "_comment": "--- TRAVEL 30 | TIER 3 — SURGERY + ICU (new batch, x4) ---",
        "scenarioId": "TRV30-T3-005",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 31,
            "sex": "F",
            "nationality": "AU",
            "originCountry": "Australia",
            "destinationCountry": "Thailand",
            "preExistingConditions": "none (prior normal IUCD inserted 3 years ago, currently in situ)",
            "policyInceptionDaysAgo": 12,
            "memberWalletSim": "sim-member-wallet-TRV30-T3-005"
        },
        "clinicalSetting": {
            "incidentCountry": "Thailand",
            "incidentCity": "Bangkok",
            "facilityType": "Samitivej Sukhumvit Hospital — Emergency and Gynaecology Surgery",
            "facilityName": "Samitivej Sukhumvit Hospital",
            "eventContext": "Leisure travel — 3-week backpacking trip through Southeast Asia",
            "incidentDayOfCoverage": 12
        },
        "diagnosis": {
            "primaryDiagnosis": "Ruptured right tubal ectopic pregnancy with haemoperitoneum — emergency laparoscopic right salpingectomy",
            "icdCode": "O00.10",
            "icdDescription": "Tubal ectopic pregnancy without intrauterine pregnancy",
            "clinicalNarrative": (
                "Patient presented with sudden severe right iliac fossa pain and syncope episode. "
                "BP 86/50 on arrival, HR 128, GCS 14. "
                "Pregnancy test: bhCG positive (4,200 IU/L). "
                "Transvaginal ultrasound: no intrauterine gestational sac; "
                "right adnexal heterogeneous mass 4.3cm; significant free fluid in "
                "Pouch of Douglas and perihepatic space (haemoperitoneum). "
                "IUCD visualised in utero. "
                "Immediate resuscitation: 2L IV crystalloid, group and crossmatch. "
                "Emergency laparoscopic surgery: right tubal ectopic confirmed, "
                "active haemorrhage from ruptured fimbrial end. "
                "Right salpingectomy performed. Estimated intraoperative blood loss 700mL. "
                "2 units packed red blood cells transfused intraoperatively. "
                "Left tube and ovary intact; IUCD left in situ (decision deferred to patient "
                "and Australian gynaecologist). "
                "Surgical ICU: 2 nights — haemodynamic monitoring post-resuscitation, "
                "haemoglobin stability check, pain management. "
                "Haemoglobin stabilised at 10.2 g/dL. "
                "Ward nights 3-4. Fully ambulatory. Discharged day 5."
            ),
            "documentsAvailable": [
                "ED triage and gynaecology assessment note",
                "bhCG result",
                "transvaginal ultrasound report",
                "emergency surgical consent and operative note (right salpingectomy)",
                "anaesthesia and blood transfusion record",
                "ICU nursing chart (nights 1-2)",
                "haemoglobin trend chart",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 8900,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 8900,
            "amountClaimed": 3000,
            "amountApproved": 3000,
            "amountDenied": 0,
            "denialBreakdown": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid — product maximum $3,000 reached. "
                "Ruptured ectopic pregnancy is an acute life-threatening gynaecological emergency. "
                "Emergency surgery + ICU 2 nights confirmed. Full product maximum disbursed."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "bhCG result + TVUS report",
                "operative note (right salpingectomy)",
                "blood transfusion record",
                "ICU nursing chart (nights 1-2)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Ruptured ectopic pregnancy — haemodynamic instability, emergency "
                "laparoscopic salpingectomy, blood transfusion, ICU 2 nights confirmed. "
                "All Tier 3 criteria met. Full product maximum $3,000 approved."
            ),
            "reviewCompletedHours": 18.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t3-sim-005",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 3000,
            "paidAmountUsdc": 3000,
            "fundingLineCharged": "genesis-travel30-liquidity",
            "fundingLineAddress": T30_LIQUIDITY_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T3-006 ── Severe TBI + decompressive craniotomy / Guadalajara ───
    {
        "scenarioId": "TRV30-T3-006",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 22,
            "sex": "M",
            "nationality": "US",
            "originCountry": "United States",
            "destinationCountry": "Mexico",
            "preExistingConditions": "none",
            "policyInceptionDaysAgo": 5,
            "memberWalletSim": "sim-member-wallet-TRV30-T3-006"
        },
        "clinicalSetting": {
            "incidentCountry": "Mexico",
            "incidentCity": "Guadalajara, Jalisco",
            "facilityType": "Hospital Civil de Guadalajara Fray Antonio Alcalde — Neurosurgery",
            "facilityName": "Hospital Civil de Guadalajara Fray Antonio Alcalde",
            "eventContext": "Leisure travel — road traffic accident, pedestrian struck by vehicle",
            "incidentDayOfCoverage": 5
        },
        "diagnosis": {
            "primaryDiagnosis": "Severe traumatic brain injury — acute subdural haematoma with midline shift, emergency decompressive craniotomy and haematoma evacuation",
            "icdCode": "S06.5X5A",
            "icdDescription": "Traumatic subdural haemorrhage with loss of consciousness greater than 24 hours with return to pre-existing conscious level, initial encounter",
            "clinicalNarrative": (
                "Patient was struck as a pedestrian by a vehicle running a red light. "
                "GCS 7 on paramedic arrival. Bilateral miosis. "
                "CT head: acute subdural haematoma right hemisphere 45mL, "
                "midline shift 12mm, right uncal herniation signs, "
                "scattered cerebral contusions bilateral frontal regions. "
                "Emergency decompressive craniotomy: right-sided large craniectomy, "
                "subdural clot evacuated, haemostasis achieved. "
                "Intraoperative ICP monitor placed (Camino). "
                "Post-operative: ICU 4 nights — mechanical ventilation nights 1-2, "
                "ICP management (head of bed 30 degrees, osmotherapy, "
                "sedation protocol), extubated day 3. GCS 14 at extubation. "
                "Step-down ward nights 5-7. Neurologically: mild right-sided facial "
                "weakness resolving. Discharged day 8 to rehabilitation facility."
            ),
            "documentsAvailable": [
                "paramedic and ED trauma assessment note",
                "CT head report (pre- and post-operative)",
                "neurosurgery operative note (decompressive craniotomy + haematoma evacuation)",
                "anaesthesia record",
                "ICP monitoring chart",
                "ICU nursing chart (nights 1-4) with GCS and ventilation records",
                "step-down ward chart",
                "rehabilitation referral and discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 22000,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 22000,
            "amountClaimed": 3000,
            "amountApproved": 3000,
            "amountDenied": 0,
            "denialBreakdown": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid — product maximum $3,000 reached. "
                "Severe TBI with emergency neurosurgery and ICU 4 nights confirmed. "
                "Full product maximum disbursed. Accidental road traffic accident: covered."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "CT head report",
                "neurosurgery operative note",
                "ICU nursing chart (nights 1-4)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Severe TBI with acute SDH — emergency decompressive craniotomy, "
                "ICU 4 nights (including mechanical ventilation) confirmed. "
                "All Tier 3 criteria met and significantly exceeded. "
                "Product maximum $3,000 approved."
            ),
            "reviewCompletedHours": 20.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t3-sim-006",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 3000,
            "paidAmountUsdc": 3000,
            "fundingLineCharged": "genesis-travel30-liquidity",
            "fundingLineAddress": T30_LIQUIDITY_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T3-007 ── Severe P. falciparum malaria + MOF / Nairobi ──────────
    {
        "scenarioId": "TRV30-T3-007",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 40,
            "sex": "F",
            "nationality": "GB",
            "originCountry": "United Kingdom",
            "destinationCountry": "Kenya",
            "preExistingConditions": "none (no malaria chemoprophylaxis taken — traveller declined prophylaxis)",
            "policyInceptionDaysAgo": 16,
            "memberWalletSim": "sim-member-wallet-TRV30-T3-007"
        },
        "clinicalSetting": {
            "incidentCountry": "Kenya",
            "incidentCity": "Nairobi",
            "facilityType": "Aga Khan University Hospital Nairobi — Infectious Disease ICU",
            "facilityName": "Aga Khan University Hospital Nairobi",
            "eventContext": "Leisure travel — 3-week Kenya safari with remote lodge stays",
            "incidentDayOfCoverage": 16
        },
        "diagnosis": {
            "primaryDiagnosis": "Severe Plasmodium falciparum malaria with cerebral involvement and multi-organ dysfunction",
            "icdCode": "B50.0",
            "icdDescription": "Plasmodium falciparum malaria with cerebral complications",
            "clinicalNarrative": (
                "Patient with 4-day prodrome (fever, chills, myalgia — initially attributed "
                "to viral illness). On day 4: GCS deteriorated to 9 (cerebral malaria), "
                "jaundice, oliguria. "
                "Blood smear + rapid RDT: P. falciparum, parasitaemia 11% (high density). "
                "Multi-organ involvement: "
                "Liver: bilirubin 94 umol/L, ALT 280 IU/L. "
                "Renal: creatinine 290 umol/L (acute kidney injury KDIGO stage 2). "
                "Haematological: platelets 22,000 (severe thrombocytopaenia), "
                "Hb 7.8 g/dL (haemolytic anaemia). "
                "IV artesunate initiated immediately. "
                "Platelet transfusion: 2 adult therapeutic doses (Hb and platelets recovered). "
                "Fluid resuscitation with careful renal monitoring. "
                "ICU admission: 3 nights — GCS monitoring, renal function trend, "
                "parasitaemia clearance checks q12h. "
                "Parasitaemia cleared to <1% by 48h. Creatinine returned to 110 umol/L. "
                "Completed oral artemether-lumefantrine for consolidation. "
                "Step-down ward nights 4-5. Discharged day 6."
            ),
            "documentsAvailable": [
                "ED and infectious disease assessment note",
                "blood smear and RDT result (P. falciparum, 11% parasitaemia)",
                "serial parasitaemia clearance results (q12h)",
                "full blood count, liver and renal function trend chart",
                "IV artesunate administration record",
                "platelet transfusion record",
                "ICU nursing chart (nights 1-3)",
                "step-down ward chart",
                "discharge summary"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 15200,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 15200,
            "amountClaimed": 3000,
            "amountApproved": 3000,
            "amountDenied": 0,
            "denialBreakdown": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid — product maximum $3,000 reached. "
                "Severe P. falciparum malaria with ICU 3 nights. "
                "Failure to take prophylaxis does not constitute an exclusion under "
                "genesis-acute-v1 (no negligence exclusion for prophylaxis non-adherence). "
                "Full product maximum disbursed."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "blood smear/RDT result",
                "serial parasitaemia clearance chart",
                "ICU nursing chart (nights 1-3)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Severe P. falciparum malaria with cerebral involvement and multi-organ "
                "dysfunction — ICU 3 nights confirmed. No surgical procedure: "
                "ICU admission >= 2 nights independently satisfies Tier 3 criteria. "
                "No prophylaxis use is not an exclusion under genesis-acute-v1 terms. "
                "Product maximum $3,000 approved."
            ),
            "reviewCompletedHours": 22.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t3-sim-007",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 3000,
            "paidAmountUsdc": 3000,
            "fundingLineCharged": "genesis-travel30-liquidity",
            "fundingLineAddress": T30_LIQUIDITY_FL,
            "policySeries": T30_POLICY_SERIES,
            "healthPlan": HEALTH_PLAN,
            "obligationStatus": "SETTLED"
        }
    },

    # ── TRV30-T3-008 ── Type B aortic dissection + TEVAR / Singapore ──────────
    {
        "scenarioId": "TRV30-T3-008",
        "product": "genesis-travel-30-v1",
        "clinicalTier": 3,
        "tierLabel": "SURGERY_ICU_2NIGHTS",
        "patientProfile": {
            "age": 58,
            "sex": "M",
            "nationality": "US",
            "originCountry": "United States",
            "destinationCountry": "Singapore",
            "preExistingConditions": "hypertension (on ramipril 10mg — disclosed at policy purchase as controlled)",
            "policyInceptionDaysAgo": 3,
            "memberWalletSim": "sim-member-wallet-TRV30-T3-008"
        },
        "clinicalSetting": {
            "incidentCountry": "Singapore",
            "incidentCity": "Singapore",
            "facilityType": "Singapore General Hospital — Vascular Surgery and Cardiac ICU",
            "facilityName": "Singapore General Hospital (SGH)",
            "eventContext": "Business travel — financial services summit, Marina Bay Sands",
            "incidentDayOfCoverage": 3
        },
        "diagnosis": {
            "primaryDiagnosis": "Stanford Type B acute aortic dissection (descending thoracic aorta) — thoracic endovascular aortic repair (TEVAR)",
            "icdCode": "I71.10",
            "icdDescription": "Dissection of unspecified part of aorta",
            "clinicalNarrative": (
                "Patient developed sudden-onset severe tearing interscapular pain during "
                "conference dinner, radiating to lumbar region. BP 188/106 (right arm). "
                "CT aortogram: Stanford Type B dissection — entry tear at 2cm distal to "
                "left subclavian artery origin, dissection extending to bilateral iliac "
                "arteries. False lumen patent (no branch vessel malperfusion identified). "
                "Entry tear maximum diameter 28mm. "
                "Medical management: IV labetalol antihypertensive protocol — "
                "target BP 100-120 systolic. Haemodynamically stable. "
                "Vascular surgery decision: TEVAR indicated (entry tear >25mm, "
                "aneurysmal false lumen risk). "
                "ICU pre-operative night 1 (BP control protocol). "
                "TEVAR performed day 2: 3-zone stent graft deployed (36mm x 200mm + "
                "16mm x 100mm distal extension). Entry tear excluded. Spinal cord monitoring "
                "intraoperatively — no ischaemia. "
                "Post-TEVAR cardiac ICU: 2 nights — BP management, spinal cord ischaemia "
                "monitoring, renal function checks. "
                "Step-down ward nights 4-5. Discharged day 6 on oral metoprolol + "
                "amlodipine dual antihypertensive regimen."
            ),
            "documentsAvailable": [
                "ED assessment and cardiology/vascular surgery note",
                "CT aortogram report (Type B dissection, entry tear measurement)",
                "TEVAR operative note (stent graft details and angiographic result)",
                "anaesthesia and spinal cord monitoring record",
                "cardiac ICU nursing chart (nights 1-3)",
                "post-TEVAR CT aortogram (entry tear exclusion confirmed)",
                "step-down ward chart",
                "discharge summary with antihypertensive plan"
            ]
        },
        "claimFinancials": {
            "productMaxBenefit": 3000,
            "benefitMode": "hybrid_fixed_reimbursement",
            "invoicedMedicalCostUSD": 45000,
            "fixedBenefitApplied": 0,
            "reimbursableExpenses": 45000,
            "amountClaimed": 3000,
            "amountApproved": 3000,
            "amountDenied": 0,
            "denialBreakdown": None,
            "settlementCurrency": "USDC",
            "settlementNote": (
                "Travel 30 hybrid — product maximum $3,000 reached. "
                "Type B aortic dissection is an acute life-threatening vascular emergency. "
                "Controlled hypertension is a pre-existing condition but does not exclude "
                "the acute aortic dissection event. TEVAR + ICU 3 nights confirmed. "
                "Full product maximum disbursed."
            )
        },
        "oracleFlow": {
            "oraclePhase": 0,
            "reviewerType": "human_operator",
            "operatorAddress": OPERATOR,
            "documentsReviewed": [
                "CT aortogram report (Type B dissection)",
                "TEVAR operative note",
                "cardiac ICU nursing chart (nights 1-3)",
                "discharge summary"
            ],
            "tierClassified": "TIER_3_SURGERY_ICU_2NIGHTS",
            "reviewOutcome": "APPROVED",
            "reviewNotes": (
                "Stanford Type B aortic dissection — TEVAR and cardiac ICU 3 nights confirmed. "
                "Pre-existing controlled hypertension: does not exclude the acute dissection "
                "event under genesis-acute-v1 (acute vascular catastrophe, not routine "
                "hypertension management). All Tier 3 criteria met. Product maximum approved."
            ),
            "reviewCompletedHours": 24.0
        },
        "onChainOutcome": {
            "claimCaseId": "trv30-t3-sim-008",
            "intakeStatus": 4,
            "intakeStatusLabel": "FULLY_SETTLED",
            "approvedAmountUsdc": 3000,
            "paidAmountUsdc": 3000,
            "fundingLineCharged": "genesis-travel30-liquidity",
            "fundingLineAddress": T30_LIQUIDITY_FL,
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

    print("Batch 7 done.")
    print("event7Scenarios unchanged: {}".format(len(data["event7Scenarios"])))
    print("travel30Scenarios: {} -> {}".format(before, after))
    print("Total: {}".format(len(data["event7Scenarios"]) + after))


if __name__ == "__main__":
    main()
