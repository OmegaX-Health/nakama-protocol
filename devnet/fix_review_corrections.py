"""
KR 1.3 — Post-review corrections pass
Fixes applied:
  1. TRV30-T2-005/006/007/008: fundingLine premiums → liquidity
  2. TRV30-T2-REVIEW-001: rename → TRV30-T3-REVIEW-002 (tier is already 3)
  3. EVT7-T1-008: Tokyo/Japan/shellfish → Warsaw/Poland/wasp sting (dedup vs EVT7-T1-003)
  4. TRV30-T1-008: Vietnam/Hanoi/finger → Japan/Osaka/finger  (dedup vs TRV30-T1-003 Vietnam)
  5. TRV30-T1-DEN-002: Thailand/Bangkok → Philippines/Manila  (Thailand overrepresentation)
  6. TRV30-T3-DEN-002: Thailand/Bangkok → Morocco/Marrakech   (Thailand overrepresentation)
"""
import json, pathlib, copy

FILE = pathlib.Path(__file__).parent.parent / \
    "examples/genesis-protect-acute-claims/genesis-acute-claim-simulations-v1.json"

T30_PREMIUMS  = "8548dWwZAxPLR9mX4FWWASA1qatNj4hEgLDAmjRVWwLe"
T30_LIQUIDITY = "HBrdsf7UjYK5tRoM9j6YaxfV7nFBkVhnJbrmTLVaDiEr"

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = []

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: TRV30-T2-005/006/007/008 — funding line premiums → liquidity
# ─────────────────────────────────────────────────────────────────────────────
FL_FIX_IDS = {"TRV30-T2-005", "TRV30-T2-006", "TRV30-T2-007", "TRV30-T2-008"}
for s in data["travel30Scenarios"]:
    if s["scenarioId"] in FL_FIX_IDS:
        oc = s["onChainOutcome"]
        oc["fundingLineCharged"] = "genesis-travel30-liquidity"
        oc["fundingLineAddress"] = T30_LIQUIDITY
        changes.append("Fix 1: {} fundingLine -> liquidity".format(s["scenarioId"]))

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: TRV30-T2-REVIEW-001 → TRV30-T3-REVIEW-002
# ─────────────────────────────────────────────────────────────────────────────
for s in data["travel30Scenarios"]:
    if s["scenarioId"] == "TRV30-T2-REVIEW-001":
        s["scenarioId"] = "TRV30-T3-REVIEW-002"
        s["onChainOutcome"]["claimCaseId"] = "trv30-t3-review-002"
        changes.append("Fix 2: TRV30-T2-REVIEW-001 renamed -> TRV30-T3-REVIEW-002")
        break

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: EVT7-T1-008 — Tokyo/Japan/shellfish urticaria → Warsaw/Poland/wasp sting
# ─────────────────────────────────────────────────────────────────────────────
for s in data["event7Scenarios"]:
    if s["scenarioId"] == "EVT7-T1-008":
        s["patientProfile"]["nationality"] = "SE"
        s["patientProfile"]["preExistingConditions"] = (
            "known wasp venom hypersensitivity (single prior mild local reaction at age 20 "
            "— no prior systemic reaction; EpiPen never prescribed)"
        )
        s["clinicalSetting"]["incidentCountry"] = "Poland"
        s["clinicalSetting"]["incidentCity"] = "Warsaw"
        s["clinicalSetting"]["facilityType"] = (
            "Emergency Department — Szpital Kliniczny im. Ks. Anny Mazowieckiej, Warsaw"
        )
        s["clinicalSetting"]["facilityName"] = (
            "Szpital Kliniczny im. Ks. Anny Mazowieckiej (SKAM)"
        )
        s["clinicalSetting"]["eventContext"] = (
            "Orange Warsaw Festival — major outdoor music festival, Legia Warsaw stadium grounds"
        )
        s["diagnosis"]["primaryDiagnosis"] = (
            "Acute systemic allergic reaction to hymenoptera (wasp) sting "
            "— generalised urticaria with facial and lip angioedema"
        )
        s["diagnosis"]["icdCode"] = "T63.461A"
        s["diagnosis"]["icdDescription"] = (
            "Toxic effect of venom of wasps, accidental, initial encounter"
        )
        s["diagnosis"]["clinicalNarrative"] = (
            "Patient was stung by a wasp on the right forearm while standing near a food "
            "vendor at the outdoor festival. Within 15 minutes: extensive truncal and limb "
            "urticaria (wheals 3-8cm), bilateral lip angioedema, periorbital oedema. "
            "No stridor, no dyspnoea, no hypotension. BP 124/78, SpO2 99%, HR 102. "
            "IM epinephrine 0.3mg administered (lip angioedema encroaching on oral cavity). "
            "IV chlorphenamine 10mg + IV methylprednisolone 80mg. "
            "Observation 4 hours post-epinephrine (biphasic anaphylaxis protocol). "
            "Symptoms fully resolved within 2 hours. BP, SpO2 stable throughout. "
            "Discharged with oral prednisolone 25mg x 3 days, oral cetirizine, "
            "and EpiPen prescription with referral to allergy clinic on return to Sweden."
        )
        s["diagnosis"]["documentsAvailable"] = [
            "ED triage note",
            "allergy assessment and medication administration record",
            "epinephrine and IV antihistamine record",
            "4-hour observation chart (biphasic watch)",
            "discharge summary with EpiPen prescription"
        ]
        s["claimFinancials"]["settlementNote"] = (
            "Fixed-benefit Tier 1. Acute systemic allergic reaction to insect sting — "
            "ER management, same-day discharge. Mild prior local reaction history does not "
            "exclude the acute systemic episode under genesis-acute-v1 terms."
        )
        s["oracleFlow"]["reviewNotes"] = (
            "Acute systemic allergic reaction to wasp sting confirmed — urticaria with "
            "facial and lip angioedema. IM epinephrine administered. 4-hour observation "
            "post-epinephrine. Same-day discharge. Known wasp hypersensitivity (mild prior "
            "local reaction only) does not constitute pre-existing condition exclusion "
            "for a new systemic episode under genesis-acute-v1. Tier 1 confirmed."
        )
        s["onChainOutcome"]["claimCaseId"] = "evt7-t1-sim-008"  # unchanged
        changes.append("Fix 3: EVT7-T1-008 -> Warsaw/Poland/wasp sting, nationality SE")
        break

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: TRV30-T1-008 — Vietnam/Hanoi/finger → Japan/Osaka/finger
# ─────────────────────────────────────────────────────────────────────────────
for s in data["travel30Scenarios"]:
    if s["scenarioId"] == "TRV30-T1-008":
        # Keep AU/M/44 — Australians frequently visit Osaka
        s["patientProfile"]["destinationCountry"] = "Japan"
        s["clinicalSetting"]["incidentCountry"] = "Japan"
        s["clinicalSetting"]["incidentCity"] = "Osaka"
        s["clinicalSetting"]["facilityType"] = (
            "Emergency Department — Osaka Red Cross Hospital (Osaka Sekijuji Byoin)"
        )
        s["clinicalSetting"]["facilityName"] = "Osaka Red Cross Hospital (Osaka Sekijuji Byoin)"
        s["clinicalSetting"]["eventContext"] = (
            "Business and leisure travel — culinary tourism, Kuromon Ichiba Market area"
        )
        s["clinicalSetting"]["incidentDayOfCoverage"] = 6
        # Diagnosis essentially unchanged — volar plate avulsion from taxi door → hotel step
        s["diagnosis"]["clinicalNarrative"] = (
            "Patient slipped on a wet step at a traditional machiya guesthouse and "
            "reflexively grabbed a metal handrail, hyper-extending the right index finger. "
            "Immediate pain and swelling at right index PIP joint. Unable to flex PIP actively. "
            "X-ray at Osaka Red Cross ED: volar plate avulsion fracture at the base of the "
            "middle phalanx (PIP joint volar lip) — fragment 3mm x 2mm. No rotational deformity. "
            "Neurovascular exam: intact digital nerves and capillary refill. "
            "Hand surgeon assessment: closed injury, no indication for ORIF. "
            "Closed reduction + dorsal extension block splint (PIP at 30 degrees flexion). "
            "Tendon and nerve function confirmed intact post-splinting. "
            "Discharged same day with splint wear instructions x 4-6 weeks, "
            "NSAID analgesia, and hand therapy referral."
        )
        s["claimFinancials"]["settlementNote"] = (
            "Travel 30 hybrid. Acute finger fracture — ER same-day management. "
            "Hospital and specialist costs approved per Japan UCR schedule. "
            "Outpatient pharmacy excluded per Travel 30 base terms."
        )
        s["oracleFlow"]["reviewNotes"] = (
            "Volar plate avulsion fracture — X-ray and hand surgeon note confirm. "
            "Closed reduction and extension block splinting. Same-day discharge. "
            "$470 hospital + specialist approved per Osaka UCR schedule. "
            "Outpatient NSAID pharmacy $40 denied per Travel 30 base terms."
        )
        changes.append("Fix 4: TRV30-T1-008 -> Japan/Osaka (was Vietnam/Hanoi)")
        break

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: TRV30-T1-DEN-002 — Thailand/Bangkok → Philippines/Manila
# ─────────────────────────────────────────────────────────────────────────────
for s in data["travel30Scenarios"]:
    if s["scenarioId"] == "TRV30-T1-DEN-002":
        s["patientProfile"]["destinationCountry"] = "Philippines"
        s["clinicalSetting"]["incidentCountry"] = "Philippines"
        s["clinicalSetting"]["incidentCity"] = "Manila"
        s["clinicalSetting"]["facilityType"] = (
            "Asian Eye Institute — Outpatient Optometry Clinic (not emergency)"
        )
        s["clinicalSetting"]["facilityName"] = (
            "Asian Eye Institute, Rockwell Health Center, Makati"
        )
        s["clinicalSetting"]["eventContext"] = (
            "Leisure travel — taking advantage of lower optometry costs in the Philippines"
        )
        # Update narrative references from Bangkok to Manila
        old_narrative = s["diagnosis"]["clinicalNarrative"]
        s["diagnosis"]["clinicalNarrative"] = old_narrative.replace(
            "Bangkok Eye Hospital", "Asian Eye Institute Manila"
        ).replace("hospital website", "clinic website")

        # Update investigation findings
        s["diagnosis"]["investigationFindings"] = [
            "Appointment pre-booked 2 days in advance via clinic website",
            "Appointment type explicitly logged as 'Annual Eye Check' in clinic system",
            "No acute complaint documented anywhere in the clinical record",
            "Services rendered are standard routine optometry, not emergency ophthalmology"
        ]
        s["diagnosis"]["documentsAvailable"] = [
            "Asian Eye Institute Manila appointment booking confirmation (type: Annual Eye Check)",
            "optometry assessment report",
            "new spectacle and contact lens prescription",
            "itemized invoice"
        ]
        s["claimFinancials"]["settlementNote"] = (
            "FULL DENIAL. Routine optometry visit — elective, pre-planned. "
            "genesis-acute-v1 Section 5.1 applies. "
            "No coverage for routine check-ups regardless of cost or location."
        )
        s["oracleFlow"]["reviewNotes"] = (
            "Appointment pre-booked 2 days prior, type 'Annual Eye Check'. "
            "No acute complaint in any part of the clinical record. "
            "Services rendered are standard routine optometry. "
            "This is an elective pre-planned visit — Section 5.1 applies. "
            "The claim narrative ('eye emergency') is contradicted by the "
            "booking and clinical documentation. Denied."
        )
        changes.append("Fix 5: TRV30-T1-DEN-002 -> Philippines/Manila (was Thailand)")
        break

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6: TRV30-T3-DEN-002 — Thailand/Bangkok → Morocco/Marrakech
# ─────────────────────────────────────────────────────────────────────────────
for s in data["travel30Scenarios"]:
    if s["scenarioId"] == "TRV30-T3-DEN-002":
        s["patientProfile"]["destinationCountry"] = "Morocco"
        s["clinicalSetting"]["incidentCountry"] = "Morocco"
        s["clinicalSetting"]["incidentCity"] = "Marrakech"
        s["clinicalSetting"]["facilityType"] = (
            "Clinique Internationale de Marrakech — Emergency Orthopaedic Surgery"
        )
        s["clinicalSetting"]["facilityName"] = "Clinique Internationale de Marrakech"
        s["clinicalSetting"]["eventContext"] = (
            "Leisure travel — hotel staircase fall on day of arrival (before policy activated)"
        )
        # Update clinical narrative
        s["diagnosis"]["clinicalNarrative"] = (
            "Patient fell on hotel staircase on the day of arrival in Marrakech, "
            "landing on outstretched right hand. "
            "X-ray right wrist: severely displaced distal radius fracture "
            "(Colles-type, dorsal angulation 45 degrees, radial shortening 8mm). "
            "Orthopaedic surgery: open reduction and internal fixation (ORIF) "
            "with volar locking plate under general anaesthesia. Duration 80 minutes. "
            "Overnight admission + hand therapy day 2. Discharged day 2. "
            "POLICY TIMELINE INVESTIGATION: "
            "Policy purchase timestamp: 2026-04-18 14:22 UTC. "
            "Policy activation (inception): 2026-04-19 00:00 UTC. "
            "Incident timestamp (hotel CCTV and hospital ED record): "
            "2026-04-18 17:45 local Marrakech time (UTC+1) = 2026-04-18 16:45 UTC. "
            "The incident occurred 2 hours and 23 minutes after policy purchase "
            "but 7 hours and 15 minutes BEFORE the policy activation time."
        )
        s["diagnosis"]["documentsAvailable"] = [
            "ED triage note (timestamp 2026-04-18 16:45 UTC confirmed)",
            "X-ray right wrist report",
            "orthopaedic operative note (ORIF volar locking plate)",
            "anaesthesia record",
            "policy certificate (purchase 2026-04-18 14:22 UTC, inception 2026-04-19 00:00 UTC)",
            "hotel CCTV incident log (timestamp corroborating ED record)"
        ]
        s["claimFinancials"]["settlementNote"] = (
            "FULL DENIAL. Incident 7h 15min before policy activation. "
            "Coverage commences at inception date 00:00 UTC, not at purchase timestamp. "
            "Member has no other active travel insurance on file."
        )
        s["oracleFlow"]["reviewNotes"] = (
            "Timeline verified from three independent sources: hospital ED record, "
            "hotel CCTV, and policy certificate. "
            "Incident: 2026-04-18 16:45 UTC. "
            "Policy inception: 2026-04-19 00:00 UTC. "
            "Delta: -7h 15min (incident pre-dates inception). "
            "The injury itself would have qualified as Tier 3 had it occurred within "
            "the coverage window. Denial is purely administrative — timing. "
            "No coverage applies."
        )
        changes.append("Fix 6: TRV30-T3-DEN-002 -> Morocco/Marrakech (was Thailand)")
        break

# ─────────────────────────────────────────────────────────────────────────────
# Write corrected file
# ─────────────────────────────────────────────────────────────────────────────
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=== Corrections applied ===")
for c in changes:
    print("  " + c)
print()
print("Total fixes: {}".format(len(changes)))
print("Scenarios: E7={}, T30={}, Total={}".format(
    len(data["event7Scenarios"]),
    len(data["travel30Scenarios"]),
    len(data["event7Scenarios"]) + len(data["travel30Scenarios"])
))
