#!/usr/bin/env python3
"""
Generate the Genesis Protect Acute v1 — Claim Verification Map PDF.
Output: devnet/omegax-genesis-claim-verification-map-2026-05-10.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Frame, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfgen_canvas
from reportlab.platypus.flowables import Flowable
import os

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "omegax-genesis-claim-verification-map-2026-05-10.pdf"
)

# ── Colours ──────────────────────────────────────────────────────────────────
TEAL        = colors.HexColor("#0891b2")
TEAL_DARK   = colors.HexColor("#0c4a6e")
TEAL_LIGHT  = colors.HexColor("#e0f2fe")
TEAL_MID    = colors.HexColor("#bae6fd")
DARK        = colors.HexColor("#0f172a")
DARK_NAVY   = colors.HexColor("#0c2340")
MID         = colors.HexColor("#334155")
MUTED       = colors.HexColor("#64748b")
RED         = colors.HexColor("#dc2626")
RED_LIGHT   = colors.HexColor("#fee2e2")
GREEN       = colors.HexColor("#16a34a")
GREEN_LIGHT = colors.HexColor("#dcfce7")
AMBER       = colors.HexColor("#d97706")
AMBER_LIGHT = colors.HexColor("#fef3c7")
WHITE       = colors.white
OFF_WHITE   = colors.HexColor("#f8fafc")
BORDER      = colors.HexColor("#cbd5e1")
SLATE_100   = colors.HexColor("#f1f5f9")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm
CONTENT_W = PAGE_W - 2 * MARGIN


# ── NumberedCanvas ────────────────────────────────────────────────────────────
class NumberedCanvas(pdfgen_canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        pg = self._pageNumber
        self.saveState()
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.3)
        self.line(MARGIN, 1.7 * cm, PAGE_W - MARGIN, 1.7 * cm)
        self.setFont("Helvetica", 6.5)
        self.setFillColor(MUTED)
        left = "OmegaX Protocol  ·  Genesis Protect Acute v1  ·  Claim Verification Map"
        right = f"Internal — Pre-Mainnet  ·  May 2026  ·  Page {pg} of {total}"
        self.drawString(MARGIN, 1.3 * cm, left)
        self.drawRightString(PAGE_W - MARGIN, 1.3 * cm, right)
        self.restoreState()


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    def ps(name, **kw):
        s[name] = ParagraphStyle(name, **kw)

    ps("cover_eyebrow", fontName="Helvetica", fontSize=8,
       textColor=TEAL_MID, leading=12, spaceBefore=0, spaceAfter=0)
    ps("cover_title", fontName="Helvetica-Bold", fontSize=22,
       textColor=WHITE, leading=28, spaceAfter=4)
    ps("cover_sub", fontName="Helvetica", fontSize=12,
       textColor=TEAL_MID, leading=16, spaceAfter=2)
    ps("cover_desc", fontName="Helvetica", fontSize=9,
       textColor=colors.HexColor("#94a3b8"), leading=14)
    ps("cover_meta_label", fontName="Helvetica-Bold", fontSize=8,
       textColor=TEAL_MID, leading=13)
    ps("cover_meta_val", fontName="Helvetica", fontSize=8,
       textColor=colors.HexColor("#e2e8f0"), leading=13)
    ps("cover_guar_title", fontName="Helvetica-Bold", fontSize=8.5,
       textColor=TEAL, leading=12)
    ps("cover_guar", fontName="Helvetica", fontSize=8,
       textColor=colors.HexColor("#e2e8f0"), leading=13)
    ps("cover_footer", fontName="Helvetica", fontSize=7.5,
       textColor=colors.HexColor("#475569"), leading=11)

    ps("h1", fontName="Helvetica-Bold", fontSize=13,
       textColor=WHITE, leading=18)
    ps("h2", fontName="Helvetica-Bold", fontSize=10.5,
       textColor=TEAL, leading=14, spaceBefore=12, spaceAfter=4)
    ps("h3", fontName="Helvetica-Bold", fontSize=9,
       textColor=DARK, leading=13, spaceBefore=8, spaceAfter=3)
    ps("body", fontName="Helvetica", fontSize=8.5,
       textColor=MID, leading=13, spaceAfter=5, alignment=TA_JUSTIFY)
    ps("body_bold", fontName="Helvetica-Bold", fontSize=8.5,
       textColor=DARK, leading=13, spaceAfter=4)
    ps("note", fontName="Helvetica-Oblique", fontSize=7.5,
       textColor=MUTED, leading=11, leftIndent=8, spaceAfter=5)
    ps("bullet", fontName="Helvetica", fontSize=8.5,
       textColor=MID, leading=13, leftIndent=14, spaceAfter=2)
    ps("cell", fontName="Helvetica", fontSize=7.5,
       textColor=MID, leading=11)
    ps("cell_hdr", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=WHITE, leading=11)
    ps("cell_bold", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=DARK, leading=11)
    ps("cell_code", fontName="Courier", fontSize=7,
       textColor=DARK, leading=11)
    ps("cell_green", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=GREEN, leading=11)
    ps("cell_red", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=RED, leading=11)
    ps("cell_amber", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=AMBER, leading=11)
    ps("cell_teal", fontName="Helvetica-Bold", fontSize=7.5,
       textColor=TEAL, leading=11)
    ps("cell_muted", fontName="Helvetica-Oblique", fontSize=7.5,
       textColor=MUTED, leading=11)

    return s


# ── Helper flowables ──────────────────────────────────────────────────────────
class SectionHeader(Flowable):
    """Teal banner for section headings."""
    def __init__(self, title, styles):
        super().__init__()
        self.title = title
        self.styles = styles
        self.width = CONTENT_W
        self.height = 0.75 * cm

    def draw(self):
        c = self.canv
        c.setFillColor(TEAL)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(WHITE)
        c.drawString(0.35 * cm, 0.2 * cm, self.title)


def section_hdr(title):
    return SectionHeader(title, None)


def P(text, style, s):
    return Paragraph(text, s[style])


def HR():
    return HRFlowable(width="100%", thickness=0.4, color=BORDER, spaceAfter=5, spaceBefore=5)


def SP(h=6):
    return Spacer(1, h)


def cell_p(text, s, style="cell"):
    return Paragraph(text, s[style])


def info_box(text, s, bg=TEAL_LIGHT, border=TEAL, border_width=3):
    t = Table([[Paragraph(text, s["body"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), border_width, border),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


BASE_TS = [
    ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 7.5),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, OFF_WHITE]),
    ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]


def std_table(rows, widths, extra_style=None):
    ts = BASE_TS[:]
    if extra_style:
        ts.extend(extra_style)
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle(ts))
    return t


def kv_table(pairs, s, key_w=4.5 * cm, key_color=TEAL):
    """Two-column key-value table (no header row)."""
    rows = []
    for k, v in pairs:
        rows.append([
            Paragraph(k, ParagraphStyle("kv_k", fontName="Helvetica-Bold",
                                        fontSize=7.5, textColor=key_color, leading=11)),
            Paragraph(v, s["cell"]),
        ])
    t = Table(rows, colWidths=[key_w, CONTENT_W - key_w])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, OFF_WHITE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Cover page (drawn on canvas via onFirstPage) ──────────────────────────────
def draw_cover(c, doc):
    w, h = PAGE_W, PAGE_H
    c.saveState()

    # Background
    c.setFillColor(DARK_NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Left accent bar
    c.setFillColor(TEAL)
    c.rect(0, 0, 5, h, fill=1, stroke=0)

    # Top stripe
    c.setFillColor(colors.HexColor("#0e3a5c"))
    c.rect(0, h - 3.2 * cm, w, 3.2 * cm, fill=1, stroke=0)

    # Program ID in top stripe
    c.setFont("Helvetica", 7.5)
    c.setFillColor(TEAL_MID)
    c.drawString(2.4 * cm, h - 1.1 * cm,
                 "OmegaX Protocol  ·  Program ID: Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawRightString(w - 2.4 * cm, h - 1.1 * cm,
                      "Solana Devnet  ·  Mainnet: Q3 2026")

    # KR label
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEAL)
    c.drawString(2.4 * cm, h - 2.2 * cm, "KR 1.4 — Onchain/Offchain Boundary Map")

    # Main title
    title_y = h - 5.2 * cm
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(WHITE)
    c.drawString(2.4 * cm, title_y, "Genesis Protect Acute v1")
    c.setFont("Helvetica-Bold", 17)
    c.setFillColor(TEAL_MID)
    c.drawString(2.4 * cm, title_y - 1.0 * cm, "Claim Verification Map")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawString(2.4 * cm, title_y - 1.9 * cm,
                 "On-Chain/Off-Chain Boundary  ·  PHI Separation  ·  LP Capital Protection")

    # Divider
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.line(2.4 * cm, title_y - 2.5 * cm, w - 2.4 * cm, title_y - 2.5 * cm)

    # Metadata block
    meta_y = title_y - 3.2 * cm
    meta = [
        ("Date",           "May 10, 2026"),
        ("Version",        "1.0"),
        ("Status",         "Pre-Mainnet Review"),
        ("Audience",       "Investors  ·  LPs  ·  Sponsors  ·  External Auditors"),
        ("Classification", "Internal — Pre-Mainnet Analysis"),
        ("Network",        "Solana (Devnet at publication)"),
    ]
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(TEAL_MID)
    col1x = 2.4 * cm
    col2x = 6.2 * cm
    row_h = 0.48 * cm
    for i, (label, value) in enumerate(meta):
        y = meta_y - i * row_h
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(TEAL_MID)
        c.drawString(col1x, y, label)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#e2e8f0"))
        c.drawString(col2x, y, value)

    # Guarantee box
    box_y = meta_y - len(meta) * row_h - 0.7 * cm
    box_h = 3.6 * cm
    box_x = 2.4 * cm
    box_w = w - 4.8 * cm
    c.setFillColor(colors.HexColor("#0e3a5c"))
    c.roundRect(box_x, box_y - box_h, box_w, box_h, 4, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.7)
    c.roundRect(box_x, box_y - box_h, box_w, box_h, 4, fill=0, stroke=1)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(TEAL)
    c.drawString(box_x + 0.5 * cm, box_y - 0.5 * cm,
                 "Three Protocol-Level Guarantees — No Operator Trust Required")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    guarantees = [
        "1.  Reserve capital cannot leave the vault without a valid, attested, settled ClaimCase",
        "2.  Evidence integrity is tamper-evident — hash is permanently immutable once the oracle attests",
        "3.  Raw patient data (PHI) never appears on Solana in any form — only 32-byte SHA-256 hashes",
    ]
    for j, g in enumerate(guarantees):
        c.drawString(box_x + 0.5 * cm, box_y - 1.1 * cm - j * 0.6 * cm, g)

    # Tag line
    tag_y = box_y - box_h - 0.8 * cm
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawString(col1x, tag_y,
                 "Every claim state  ·  Every verification event  ·  Every hash anchor  ·  Fully auditable from public chain data")

    # Footer
    c.setStrokeColor(colors.HexColor("#1e3a5f"))
    c.setLineWidth(0.5)
    c.line(col1x, 2.0 * cm, w - col1x, 2.0 * cm)
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(col1x, 1.5 * cm,
                 "© 2026 OmegaX Health Capital Markets  ·  omegax.health")

    c.restoreState()


# ── Main ──────────────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=2.0 * cm,
        bottomMargin=2.2 * cm,
        title="Genesis Protect Acute v1 — Claim Verification Map",
        author="OmegaX Protocol",
        subject="Claim Verification Map | KR 1.4",
    )

    s = make_styles()
    story = []

    def p(text, style="body"):
        return Paragraph(text, s[style])

    def C(text, style="cell"):
        return Paragraph(text, s[style])

    # ── Cover ─────────────────────────────────────────────────────────────────
    # Cover drawn by onFirstPage; Platypus starts from page 2.
    # We push a PageBreak so Platypus content begins on page 2.
    story.append(PageBreak())

    # ── SECTION: Executive Summary ────────────────────────────────────────────
    story.append(section_hdr("Executive Summary"))
    story.append(SP(8))
    story.append(p(
        "Genesis Protect Acute v1 processes health insurance claims through a cryptographically "
        "verifiable truth chain anchored on Solana. This document is the authoritative map of that "
        "chain — for investors, LPs, sponsors, and auditors who need to understand what the "
        "protocol guarantees and how to verify those guarantees from public on-chain data, "
        "<b>without accessing any patient health records</b>."
    ))
    story.append(SP(6))

    story.append(p("Three properties are enforced at the protocol level — no operator trust required:", "body_bold"))
    story.append(SP(4))

    guar_rows = [
        [C("#", "cell_hdr"), C("Property", "cell_hdr"), C("How it is enforced", "cell_hdr")],
        [C("1", "cell_bold"),
         C("Reserve capital cannot leave the vault on an unauthorized claim"),
         C("Only outflow path: PDA-signed SPL transfer gated on ClaimCase.intake_status = SETTLED (4) with a valid oracle attestation chain")],
        [C("2", "cell_bold"),
         C("Claim evidence is tamper-evident — retrospective forgery is impossible"),
         C("evidence_ref_hash immutable once attestation_count ≥ 1; hash equality enforced on-chain at attest_claim_case")],
        [C("3", "cell_bold"),
         C("Raw patient data (PHI) never appears on Solana in any form"),
         C("Only 32-byte SHA-256 fingerprints written on-chain; raw documents stay encrypted on the off-chain oracle portal")],
    ]
    t = Table(guar_rows, colWidths=[0.6 * cm, 6.5 * cm, CONTENT_W - 7.1 * cm])
    t.setStyle(TableStyle(BASE_TS + [
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f0f9ff")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f0fdf4")),
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#f0f9ff")),
    ]))
    story.append(t)
    story.append(SP(8))

    story.append(p("<b>What LPs and sponsors can verify independently</b> — from public Solana explorer data alone:", "body_bold"))
    for b in [
        "Every claim opened, every evidence hash committed, every oracle attestation, every adjudication decision, and every payout — each with timestamp and signing authority",
        "That vault balances decrease only on settled, attested claims",
        "That oracle attestations reference exactly the evidence packet that was reviewed (hash equality enforced on-chain — transaction reverts on mismatch)",
        "That protocol fees were correctly carved out at settlement",
    ]:
        story.append(p(f"• {b}", "bullet"))
    story.append(SP(6))
    story.append(info_box(
        "<b>Phase 0 posture:</b> Operator-backed oracle review with all material state transitions "
        "anchored on-chain. The roadmap toward fully decentralized adjudication is documented in §10.",
        s, bg=AMBER_LIGHT, border=AMBER
    ))

    # ── SECTION 1: Legend & Pre-Claim Foundation ──────────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§1 — Legend & Pre-Claim Foundation"))
    story.append(SP(8))

    leg_rows = [
        [C("Symbol", "cell_hdr"), C("Meaning", "cell_hdr")],
        [C("⛓"), C("Solana instruction (on-chain transaction)")],
        [C("🔒"), C("On-chain proof anchor (hash or state written to Solana)")],
        [C("📁"), C("Off-chain only (raw PHI, operator workflow, AI logs)")],
        [C("🔐"), C("TEE only (MagicBlock private review — hash exits, plaintext never does)")],
    ]
    story.append(std_table(leg_rows, [1.5 * cm, CONTENT_W - 1.5 * cm]))
    story.append(SP(10))

    story.append(p(
        "Before any claim opens, the protocol anchors the policy terms, pricing, and evidence "
        "requirements on-chain as <b>immutable hash commitments</b> inside the <code>PolicySeries</code> account. "
        "These are the root of the verification chain — every claim is evaluated against these anchored "
        "parameters. All material is locked (<code>material_locked = true</code>) before the series goes live."
    ))
    story.append(SP(6))

    ps_rows = [
        [C("PolicySeries field", "cell_hdr"), C("What it commits to", "cell_hdr"), C("Set by", "cell_hdr")],
        [C("terms_hash", "cell_code"), C("Full coverage terms and exclusion schedule"), C("Protocol governance")],
        [C("pricing_hash", "cell_code"), C("Premium structure and benefit tiers"), C("Protocol governance")],
        [C("payout_hash", "cell_code"), C("Benefit amounts per tier (T1/T2/T3) and reimbursement cap"), C("Protocol governance")],
        [C("reserve_model_hash", "cell_code"), C("Reserve methodology and VaR parameters"), C("Protocol governance")],
        [C("evidence_requirements_hash", "cell_code"), C("Required document types per claim tier"), C("Protocol governance")],
        [C("schema_binding_hash", "cell_code"), C("Binding to the verified OutcomeSchema (HealthPlan)"), C("Plan admin")],
    ]
    story.append(std_table(ps_rows, [5 * cm, 8 * cm, CONTENT_W - 13 * cm]))
    story.append(SP(6))
    story.append(p(
        "The <b>OutcomeSchema</b> (<code>genesis-protect-acute-claim</code> v1) is separately registered "
        "on-chain and must be marked <code>verified = true</code> by governance before any oracle can attest. "
        "Its <code>schema_key_hash</code> and <code>schema_hash</code> are snapshotted into every "
        "<code>ClaimAttestation</code>.", "note"
    ))

    # ── SECTION 2: State Machine ──────────────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§2 — Claim State Machine"))
    story.append(SP(8))
    story.append(p(
        "The <code>ClaimCase</code> account's <code>intake_status</code> field drives the complete claim "
        "lifecycle. No state can be skipped or forged without a valid signed Solana transaction from the "
        "authorized role."
    ))
    story.append(SP(6))

    sm_rows = [
        [C("State", "cell_hdr"), C("intake_status", "cell_hdr"),
         C("On-chain trigger", "cell_hdr"), C("Who signs", "cell_hdr"), C("Money moves?", "cell_hdr")],
        [C("OPEN", "cell_bold"), C("0", "cell_code"),
         C("open_claim_case"), C("Member or claims_operator or plan_admin"), C("No")],
        [C("UNDER_REVIEW", "cell_bold"), C("1", "cell_code"),
         C("Operator queue pickup (off-chain)"), C("—"), C("No")],
        [C("APPROVED"), C("2", "cell_code"),
         C("adjudicate_claim_case (approved_amount > 0)"), C("claims_operator"), C("No — reserve booked")],
        [C("DENIED", "cell_red"), C("3", "cell_code"),
         C("adjudicate_claim_case (approved_amount == 0)"), C("claims_operator"), C("No — obligation void")],
        [C("SETTLED", "cell_green"), C("4", "cell_code"),
         C("settle_claim_case / settle_claim_case_selected_asset"), C("claims_operator"), C("YES — USDC exits vault", "cell_green")],
        [C("CLOSED", "cell_muted"), C("5", "cell_code"),
         C("Reserved — Phase 1 dispute-case state"), C("—"), C("—")],
    ]
    story.append(std_table(sm_rows,
                           [2.0 * cm, 1.4 * cm, 5.2 * cm, 4.0 * cm, CONTENT_W - 12.6 * cm]))

    # ── SECTION 3: Instruction-to-Verification Map ────────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§3 — Instruction-to-Verification Map"))
    story.append(SP(8))
    story.append(p(
        "Every step that produces an on-chain proof is listed with the exact account written, the hash "
        "anchored, and the event emitted. Off-chain steps (📁) are shown for completeness — they leave "
        "no on-chain footprint at that point."
    ))

    steps = [
        ("Step 1 — open_claim_case ⛓", [
            ("Authorized signers", 'Member wallet  OR  health_plan.claims_operator  OR  health_plan.plan_admin'),
            ("PDA created", 'ClaimCase — seeds: ["claim_case", health_plan.key(), claim_id]'),
            ("State transition", "→ CLAIM_INTAKE_OPEN (0)"),
            ("🔒 On-chain writes", "claim_case.claimant · .policy_series · .funding_line · .evidence_ref_hash (initial) · .opened_at"),
            ("Event emitted", "ClaimCaseStateChangedEvent { claim_case, intake_status: 0, approved_amount: 0 }"),
            ("📁 Off-chain at this point", "Raw incident report, member identity docs — not yet submitted"),
            ("PHI on-chain?", "NO"),
            ("🔐 Security (PT-04)", "claimant constrained to member_position.wallet — operators cannot spoof claimant"),
        ]),
        ("Step 2 — authorize_claim_recipient ⛓  (optional)", [
            ("Authorized signers", "Member wallet ONLY — operators cannot set this"),
            ("State transition", "None"),
            ("🔒 On-chain writes", "claim_case.delegate_recipient (payout routing address)"),
            ("Event emitted", "None"),
            ("PHI on-chain?", "NO"),
        ]),
        ("Step 3 — Evidence upload & human review  📁", [
            ("Where", "OmegaX Health oracle portal (off-chain, encrypted)"),
            ("📁 Member uploads", "Discharge summary · itemized invoice · location proof · doctor note"),
            ("📁 AI pre-screening", "Completeness check, anomaly flags → operator queue"),
            ("📁 Human review", "Claims operator reviews raw PHI against policy_series.evidence_requirements_hash"),
            ("PHI on-chain?", "NO — raw documents never touch Solana"),
        ]),
        ("Step 4 — attach_claim_evidence_ref ⛓", [
            ("Authorized signers", "health_plan.claims_operator"),
            ("Precondition", "claim_case.attestation_count == 0  (mutable only before first oracle attestation)"),
            ("State transition", "None"),
            ("🔒 On-chain writes — hash 1", "claim_case.evidence_ref_hash  [SHA-256 of full evidence packet]"),
            ("🔒 On-chain writes — hash 2", "claim_case.decision_support_hash  [SHA-256 of operator review bundle]"),
            ("Event emitted", "None"),
            ("PHI on-chain?", "NO — only 32-byte hashes"),
            ("Evidence lock", "Once attestation_count ≥ 1: evidence_ref_hash permanently immutable. Revised evidence → new ClaimCase PDA."),
        ]),
        ("Step 5 — attest_claim_case ⛓", [
            ("Authorized signers", "oracle_profile.oracle"),
            ("Preconditions", "outcome_schema.verified == true  ·  oracle has ATTEST_CLAIM permission  ·  args.attestation_ref_hash == claim_case.evidence_ref_hash (enforced on-chain — reverts on mismatch)  ·  finality hold clear"),
            ("PDA created", 'ClaimAttestation — seeds: ["claim_attestation", claim_case.key(), oracle.key()]'),
            ("State transition", "claim_case.attestation_count++"),
            ("🔒 On-chain writes", "Full ClaimAttestation — see §3.5 field breakdown below"),
            ("Event emitted", "ClaimCaseAttestedEvent { claim_attestation, claim_case, oracle_profile, oracle, decision, attestation_hash }"),
            ("PHI on-chain?", "NO — only hash fields"),
            ("🔐 Security (PT-07)", "Oracle registration requires signer == args.oracle — no third-party registration possible"),
        ]),
        ("Step 6 — adjudicate_claim_case ⛓", [
            ("Authorized signers", "health_plan.claims_operator"),
            ("State transition (approve)", "→ APPROVED (2)  if  approved_amount > 0"),
            ("State transition (deny)", "→ DENIED (3)  if  approved_amount == 0"),
            ("🔒 On-chain writes", "claim_case.intake_status · .adjudicator [Pubkey] · .approved_amount · .denied_amount · .decision_support_hash"),
            ("Event emitted", "ClaimCaseStateChangedEvent { claim_case, intake_status, approved_amount }"),
            ("Denial path", "No Obligation PDA created. Denial reason anchored via decision_support_hash — full rationale off-chain."),
            ("PHI on-chain?", "NO — only amounts and pubkeys"),
        ]),
        ("Step 7 — reserve_obligation ⛓", [
            ("Authorized signers", "health_plan.claims_operator"),
            ("State transition", "Obligation.status → RESERVED (1)"),
            ("🔒 On-chain writes", "obligation.reserved_amount  ·  funding_line.reserved_amount ↑  ·  claim_case.linked_obligation"),
            ("Event emitted", "ObligationStatusChangedEvent { obligation, funding_line, status: 1, amount }"),
            ("Visibility", "Encumbered reserve is visible on the public protocol console in real time"),
            ("PHI on-chain?", "NO"),
        ]),
        ("Step 8 — settle_claim_case / settle_claim_case_selected_asset ⛓", [
            ("Authorized signers", "health_plan.claims_operator"),
            ("Preconditions", "reserve_asset_rail.payout_enabled == true  ·  price freshness within rail bounds  ·  recipient token account owner matches resolved recipient"),
            ("State transition", "→ SETTLED (4)  when  paid_amount ≥ approved_amount"),
            ("🔒 On-chain writes", "claim_case.paid_amount ↑  ·  .intake_status → SETTLED  ·  .closed_at  ·  domain_asset_vault.total_assets ↓"),
            ("SPL transfer", "transfer_from_domain_vault  (PDA-signed CPI) — THE ONLY AUTHORIZED OUTFLOW PATH"),
            ("Events emitted", "ClaimCaseStateChangedEvent  +  FeeAccruedEvent (protocol fee)  +  optional FeeAccruedEvent (oracle revshare if LP-backed)"),
            ("Multi-asset variant", "settle_claim_case_selected_asset → ClaimCaseSelectedAssetPayoutEvent { claim_asset_mint, payout_asset_mint, claim_credit_amount, payout_amount, settlement_reason_hash }"),
            ("PHI on-chain?", "NO"),
            ("🔐 Security (PT-01/02)", "transfer_from_domain_vault requires vault PDA signature via seeds — no unsigned outflow possible"),
        ]),
    ]

    for step_title, pairs in steps:
        story.append(SP(8))
        story.append(KeepTogether([
            p(step_title, "h2"),
            kv_table(pairs, s, key_w=4.8 * cm),
        ]))

    # ClaimAttestation field breakdown
    story.append(SP(10))
    story.append(p("ClaimAttestation — Complete On-Chain Fields (from Step 5):", "h3"))
    att_rows = [
        [C("Field", "cell_hdr"), C("Size", "cell_hdr"), C("What it represents", "cell_hdr")],
        [C("oracle", "cell_code"), C("Pubkey"), C("Oracle authority public key")],
        [C("oracle_profile", "cell_code"), C("Pubkey"), C("OracleProfile PDA reference")],
        [C("claim_case", "cell_code"), C("Pubkey"), C("Parent ClaimCase reference")],
        [C("health_plan", "cell_code"), C("Pubkey"), C("HealthPlan reference")],
        [C("policy_series", "cell_code"), C("Pubkey"), C("PolicySeries reference")],
        [C("decision", "cell_code"), C("u8"), C("0=approve  /  1=deny  /  2=request_review  /  3=abstain")],
        [C("attestation_hash", "cell_code"), C("32 bytes"), C("Oracle's own hash commitment (off-chain signed artifact)")],
        [C("attestation_ref_hash", "cell_code"), C("32 bytes"), C("MUST equal claim_case.evidence_ref_hash — enforced on-chain")],
        [C("evidence_ref_hash", "cell_code"), C("32 bytes"), C("Snapshot of evidence hash at attestation time")],
        [C("decision_support_hash", "cell_code"), C("32 bytes"), C("Snapshot of operator review bundle hash")],
        [C("schema_key_hash", "cell_code"), C("32 bytes"), C('Hash of the OutcomeSchema key ("genesis-protect-acute-claim")')],
        [C("schema_hash", "cell_code"), C("32 bytes"), C("Hash of the schema content at attestation time")],
        [C("schema_version", "cell_code"), C("u16"), C("Schema version at attestation time")],
        [C("created_at_ts", "cell_code"), C("i64"), C("Unix timestamp of attestation")],
    ]
    story.append(std_table(att_rows, [5.0 * cm, 1.8 * cm, CONTENT_W - 6.8 * cm]))

    # ── SECTION 4: PHI vs Proof Separation ───────────────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§4 — PHI vs. Proof Anchoring: Complete Separation"))
    story.append(SP(8))
    story.append(p(
        "This table is the canonical reference for what lives where. Nothing in the left column ever "
        "appears on Solana in any form. The right column is what external parties can read and verify."
    ))
    story.append(SP(6))

    phi_rows = [
        [C("Category", "cell_hdr"), C("Data (📁 off-chain only)", "cell_hdr"), C("🔒 On-chain proof anchor", "cell_hdr")],
        [C("Member identity", "cell_bold"), C("Passport, ID document, KYC data"),
         C("member_position.subject_commitment  [identity commitment hash]", "cell_code")],
        [C("Medical evidence", "cell_bold"), C("Discharge summary, doctor notes, clinical records"),
         C("claim_case.evidence_ref_hash  [SHA-256 of evidence packet]", "cell_code")],
        [C("Billing documents", "cell_bold"), C("Itemized invoice, proof of payment, receipts"),
         C("claim_case.evidence_ref_hash  (included in evidence packet)", "cell_code")],
        [C("Operator review", "cell_bold"), C("Review checklist, internal notes, AI flag log"),
         C("claim_case.decision_support_hash  [SHA-256 of review bundle]", "cell_code")],
        [C("Oracle decision", "cell_bold"), C("Full oracle assessment document"),
         C("claim_attestation.attestation_hash  [oracle's 32-byte commitment]", "cell_code")],
        [C("Policy terms", "cell_bold"), C("Full coverage terms text (PDF / doc)"),
         C("policy_series.terms_hash  [SHA-256 of terms document]", "cell_code")],
        [C("Evidence requirements", "cell_bold"), C("Required document checklist per tier"),
         C("policy_series.evidence_requirements_hash", "cell_code")],
        [C("Fraud notes", "cell_bold"), C("Investigation notes, referral details"),
         C("Not anchored on-chain in Phase 0", "cell_muted")],
        [C("AI screening logs", "cell_bold"), C("Pre-screening output, anomaly scores"),
         C("Not anchored on-chain in Phase 0", "cell_muted")],
        [C("TEE evidence packet", "cell_bold"), C("Plaintext PHI inside MagicBlock TEE (never exits)"),
         C("private_review_session.review_artifact_hash  (exits TEE as hash only)", "cell_code")],
    ]
    story.append(std_table(phi_rows, [3.2 * cm, 6.0 * cm, CONTENT_W - 9.2 * cm]))
    story.append(SP(8))
    story.append(info_box(
        "<b>Summary:</b> Every byte of raw PHI stays off-chain. What Solana records are the SHA-256 "
        "fingerprints of that data — sufficient for a third party to verify that the reviewed evidence "
        "matches what was attested, <b>without accessing the underlying medical content</b>.",
        s, bg=GREEN_LIGHT, border=GREEN
    ))

    # ── SECTION 5: Hash Chain ─────────────────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§5 — Complete On-Chain Hash Chain"))
    story.append(SP(8))
    story.append(p(
        "The chain below shows how each hash links to the next, forming a tamper-evident path from "
        "raw PHI to final USDC settlement on Solana."
    ))
    story.append(SP(6))

    chain_nodes = [
        (MUTED,       WHITE,  "RAW PHI (off-chain only)",
         "Medical records + invoices + location proof + doctor note\nStored encrypted on OmegaX Health oracle portal"),
        (None,        TEAL,   "▼  SHA-256 by operator after human review",  ""),
        (TEAL_LIGHT,  TEAL,   "🔒  ClaimCase.evidence_ref_hash  [32 bytes — Solana]",
         "Set by: attach_claim_evidence_ref (claims_operator)\nImmutable after: first attest_claim_case (attestation_count ≥ 1)"),
        (None,        TEAL,   "▼  Oracle verifies: attestation_ref_hash == evidence_ref_hash",
         "Enforced on-chain — transaction reverts if hashes do not match"),
        (TEAL_LIGHT,  TEAL,   "🔒  ClaimAttestation PDA  [Solana — permanent]",
         "attestation_hash · attestation_ref_hash · evidence_ref_hash\ndecision_support_hash · schema_key_hash · schema_hash\ndecision [u8] · oracle [Pubkey]"),
        (None,        TEAL,   "▼  adjudicate_claim_case (claims_operator)", ""),
        (TEAL_LIGHT,  TEAL,   "🔒  ClaimCase — adjudication record  [Solana — permanent]",
         "intake_status: APPROVED (2) or DENIED (3)\nadjudicator [Pubkey]  ·  approved_amount [u64]  ·  decision_support_hash"),
        (None,        TEAL,   "▼  reserve_obligation → settle_claim_case", ""),
        (GREEN_LIGHT, GREEN,  "🔒  Settlement — SPL token transfer  [Solana — permanent]",
         "intake_status: SETTLED (4)  ·  paid_amount [u64]  ·  closed_at [i64]\nrecipient: member_position.wallet or delegate_recipient\ndomain_asset_vault.total_assets ↓  ·  tx signature immutable"),
    ]

    for bg, border, title, desc in chain_nodes:
        is_arrow = bg is None
        if is_arrow:
            arrow_style = ParagraphStyle("arrow", fontName="Helvetica-Oblique",
                                         fontSize=7.5, textColor=border, leading=11)
            rows = [[Paragraph(title, arrow_style)]]
            if desc:
                desc_style = ParagraphStyle("arrow_d", fontName="Helvetica",
                                            fontSize=7, textColor=MUTED, leading=11)
                rows.append([Paragraph(desc, desc_style)])
            t = Table(rows, colWidths=[CONTENT_W])
            t.setStyle(TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 30),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
        else:
            title_style = ParagraphStyle("chain_t", fontName="Helvetica-Bold",
                                         fontSize=8, textColor=border, leading=12)
            rows = [[Paragraph(title, title_style)]]
            if desc:
                desc_style = ParagraphStyle("chain_d", fontName="Courier",
                                            fontSize=7, textColor=MID, leading=11)
                rows.append([Paragraph(desc, desc_style)])
            t = Table(rows, colWidths=[CONTENT_W - 0.5 * cm])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("LINEBEFORE", (0, 0), (0, -1), 3, border),
                ("LINEABOVE", (0, 0), (-1, 0), 0.5, border),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, border),
                ("LINEAFTER", (0, 0), (-1, -1), 0.5, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
        story.append(t)
        story.append(SP(2))

    story.append(SP(4))
    story.append(p(
        "<b>Verification property:</b> A third party who holds the original evidence packet can SHA-256 "
        "hash it and compare against <code>claim_case.evidence_ref_hash</code>. If they match, the "
        "evidence anchored on Solana is identical to what was reviewed — and the oracle's attestation "
        "applies to exactly that packet.", "note"
    ))

    # ── SECTION 6: MagicBlock ─────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§6 — MagicBlock TEE Private Review Path"))
    story.append(SP(8))
    story.append(p(
        "For claims requiring TEE-private handling, an adjunct program "
        "<code>omegax_private_claim_review</code> runs on MagicBlock Ephemeral Rollups. This path "
        "integrates at steps 4–5 of the standard lifecycle. "
        "<b>The main protocol vaults, funding lines, and obligations are never delegated to MagicBlock.</b>"
    ))
    story.append(SP(6))

    mb_rows = [
        [C("Standard path", "cell_hdr"), C("MagicBlock TEE private path", "cell_hdr")],
        [C("📁 Evidence upload (off-chain)"), C("📁 Evidence upload (off-chain)")],
        [C("⛓ attach_claim_evidence_ref"),
         C("🔐 TEE receives private packet\n⛓ open_review_session")],
        [C("⛓ attest_claim_case"),
         C("⛓ delegate_review_session (→ MagicBlock ER)\n🔐 Private review inside TEE — plaintext never leaves enclave\n⛓ record_private_review (review_artifact_hash only)\n⛓ record_private_payment_ref (payment_reference_hash only)\n⛓ commit_and_close_review_session (→ Solana base)\n⛓ attest_claim_case (main program — consumes artifact hash)")],
    ]
    story.append(std_table(mb_rows, [CONTENT_W / 2, CONTENT_W / 2]))
    story.append(SP(10))

    story.append(p("PHI boundary in the MagicBlock path:", "h3"))
    mb_phi_rows = [
        [C("What", "cell_hdr"), C("Where", "cell_hdr")],
        [C("Private evidence packet (plaintext)"), C("🔐 TEE enclave only — never on Solana, never on MagicBlock ER")],
        [C("review_artifact_hash"), C("🔒 MagicBlock ER → committed to Solana base")],
        [C("private_payment_reference_hash"), C("🔒 MagicBlock ER → committed to Solana base")],
        [C("Oracle attestation hash"), C("🔒 Standard ClaimAttestation PDA on Solana base")],
    ]
    story.append(std_table(mb_phi_rows, [5.5 * cm, CONTENT_W - 5.5 * cm]))

    # ── SECTION 7: Unhappy Paths ──────────────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§7 — Unhappy Paths: Verification Map"))
    story.append(SP(8))

    uh_rows = [
        [C("Scenario", "cell_hdr"), C("On-chain state", "cell_hdr"), C("What's verifiable", "cell_hdr")],
        [C("Incomplete evidence"), C("intake_status = OPEN (0), no evidence_ref_hash set"),
         C("Chain shows claim opened but no evidence attached")],
        [C("Evidence resubmission (pre-attestation)"), C("New attach_claim_evidence_ref updates evidence_ref_hash"),
         C("Each update is a distinct Solana tx; full history recoverable from tx logs")],
        [C("Evidence revision (post-attestation)"), C("New ClaimCase PDA opened"),
         C("Both cases publicly visible; original attestation chain immutable")],
        [C("Partial approval (Travel 30 top-up)"), C("approved_amount = fixed tier cap; second adjudication round for top-up"),
         C("Two separate ClaimCaseStateChangedEvent entries on-chain")],
        [C("Denial"), C("intake_status = DENIED (3); decision_support_hash updated"),
         C("Hash-committed reason; no obligation created; no funds reserved")],
        [C("Settlement deferred"), C("obligation.status = CLAIMABLE_PAYABLE (2)"),
         C("Encumbered reserve visible; vault balance unchanged")],
        [C("Impairment"), C("obligation.status = IMPAIRED (5) after mark_impairment"),
         C("ImpairmentRecordedEvent on-chain; LP junior class absorbs loss")],
        [C("Appeal (Phase 0)"), C("New ClaimCase PDA with appeal evidence"),
         C("New claim on-chain; original denial chain intact and immutable")],
    ]
    story.append(std_table(uh_rows, [3.5 * cm, 5.5 * cm, CONTENT_W - 9 * cm]))

    # ── SECTION 8: Obligation Lifecycle ──────────────────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§8 — Obligation State Lifecycle"))
    story.append(SP(8))
    story.append(p(
        "The <code>Obligation</code> account runs in parallel with <code>ClaimCase</code>. Every status "
        "transition emits <code>ObligationStatusChangedEvent \\{ obligation, funding_line, status, amount \\}</code>."
    ))
    story.append(SP(6))

    obl_rows = [
        [C("Status", "cell_hdr"), C("Value", "cell_hdr"), C("Trigger", "cell_hdr"), C("Effect", "cell_hdr")],
        [C("PROPOSED"), C("0", "cell_code"), C("adjudicate_claim_case (approved)"),
         C("Obligation PDA created; no reserve yet")],
        [C("RESERVED"), C("1", "cell_code"), C("reserve_obligation"),
         C("funding_line.reserved_amount ↑  —  LP capacity encumbered")],
        [C("CLAIMABLE_PAYABLE"), C("2", "cell_code"), C("Internal transition"),
         C("Ready for settlement payout")],
        [C("SETTLED", "cell_green"), C("3", "cell_code"), C("settle_claim_case"),
         C("Funds disbursed; obligation closed")],
        [C("CANCELED", "cell_red"), C("4", "cell_code"), C("Denial / void path"),
         C("No reserve taken; obligation void")],
        [C("IMPAIRED", "cell_red"), C("5", "cell_code"), C("mark_impairment"),
         C("LP junior class absorbs loss; ImpairmentRecordedEvent emitted")],
        [C("RECOVERED"), C("6", "cell_code"), C("Post-impairment recovery"),
         C("Partial or full recovery credited back to LP")],
    ]
    story.append(std_table(obl_rows, [3.2 * cm, 1.2 * cm, 4.8 * cm, CONTENT_W - 9.2 * cm]))

    # ── SECTION 9: Auditor Checklist ──────────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§9 — Independent Auditor Verification Checklist"))
    story.append(SP(8))
    story.append(p(
        "For any Genesis Protect Acute claim, an independent auditor can verify the following from "
        "<b>public on-chain data alone</b>. No access to raw PHI is required."
    ))
    story.append(SP(6))

    aud_rows = [
        [C("Question", "cell_hdr"), C("Where to look on-chain", "cell_hdr")],
        [C("Who opened the claim and when?"),
         C("claim_case.claimant  ·  .opened_at  ·  opening tx signature", "cell_code")],
        [C("Was the claimant an active policy member?"),
         C("member_position.active == true  ·  .eligibility_status == ELIGIBLE at claim time", "cell_code")],
        [C("What evidence hash was committed?"),
         C("claim_case.evidence_ref_hash", "cell_code")],
        [C("Was evidence locked before attestation?"),
         C("claim_case.attestation_count ≥ 1  →  hash is immutable", "cell_code")],
        [C("Who attested and with what decision?"),
         C("ClaimAttestation.oracle  ·  .decision  ·  .attestation_hash", "cell_code")],
        [C("Was the schema governance-verified?"),
         C("outcome_schema.verified == true at attestation time", "cell_code")],
        [C("Does the attestation match the evidence?"),
         C("claim_attestation.attestation_ref_hash == claim_case.evidence_ref_hash  (enforced on-chain)", "cell_code")],
        [C("Who adjudicated and what was the outcome?"),
         C("claim_case.adjudicator  ·  .intake_status  ·  .approved_amount", "cell_code")],
        [C("What funding line was reserved?"),
         C("claim_case.funding_line  ·  obligation.reserved_amount", "cell_code")],
        [C("Was payout made and to whom?"),
         C("claim_case.paid_amount  ·  .closed_at  ·  settlement tx  ·  recipient = delegate_recipient or member_position.wallet", "cell_code")],
        [C("Were fees correctly carved out?"),
         C("FeeAccruedEvent on settlement tx  ·  protocol_fee_vault.accrued_fees", "cell_code")],
        [C("Was policy material unchanged at claim time?"),
         C("policy_series.material_locked == true  ·  terms_hash unchanged since issuance", "cell_code")],
    ]
    story.append(std_table(aud_rows, [6.5 * cm, CONTENT_W - 6.5 * cm]))

    # ── SECTION 10: Phased Decentralization Roadmap ───────────────────────────
    story.append(PageBreak())
    story.append(section_hdr("§10 — Phased Decentralization Roadmap"))
    story.append(SP(8))
    story.append(p(
        "The protocol launches in a deliberately phased approach: Phase 0 achieves on-chain anchoring "
        "of all material claim state while retaining operator-supervised workflows for review queuing "
        "and oracle key management. The table below is an honest accounting of what each phase adds."
    ))
    story.append(SP(6))

    ph_rows = [
        [C("Item", "cell_hdr"), C("Phase 0 posture", "cell_hdr"), C("Phase 1 target", "cell_hdr")],
        [C("UNDER_REVIEW state"),
         C("Off-chain queue pickup — not a distinct on-chain intake_status transition"),
         C("Explicit on-chain set_claim_under_review instruction")],
        [C("Appeal linkage"),
         C("New ClaimCase PDA for appeals; correlated off-chain"),
         C("On-chain dispute-case linkage between original denial and appeal PDA")],
        [C("Fraud referral record"),
         C("Internal notes; hash not yet committed on-chain"),
         C("fraud_referral_hash field or dedicated instruction in protocol-oracle-service")],
        [C("Oracle key custody"),
         C("Claims operator hot wallet signs oracle transactions"),
         C("HSM / KMS boundary enforced before mainnet  (see claims-processing-spec §13)")],
        [C("Provider direct settlement"),
         C("Payout goes to member wallet or delegated recipient"),
         C("Provider KYB  +  delegate_recipient = verified provider wallet")],
    ]
    story.append(std_table(ph_rows, [3.5 * cm, 5.8 * cm, CONTENT_W - 9.3 * cm]))
    story.append(SP(8))
    story.append(info_box(
        "<b>Phase 0 communication standard:</b> Any external claim communication — to members, "
        "partners, or press — must describe the current posture as <b>operator-backed oracle review</b>, "
        "not fully decentralized adjudication. The on-chain record is authoritative; the governance of "
        "who writes to it is progressively decentralizing.",
        s, bg=AMBER_LIGHT, border=AMBER
    ))

    # ── SECTION 11: LP Capital Protection ────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§11 — LP Capital Protection Summary"))
    story.append(SP(8))
    story.append(p(
        "For LPs deploying capital into OmegaX Protocol liquidity pools, the claim architecture "
        "provides the following hard guarantees at the smart contract level."
    ))
    story.append(SP(6))

    lp_data = [
        ("Can an operator drain the vault without a real claim?",
         "NO",
         "Funds leave only via transfer_from_domain_vault PDA-signed CPI, gated on ClaimCase.intake_status = SETTLED (4) with a valid oracle attestation chain"),
        ("Can a fraudulent claim override a valid attestation?",
         "NO",
         "adjudicate_claim_case is gated on the oracle attestation chain; adjudicator pubkey permanently recorded on-chain"),
        ("Can evidence be altered after oracle review?",
         "NO",
         "evidence_ref_hash is immutable once attestation_count ≥ 1; any revision requires a new ClaimCase PDA"),
        ("Can LP losses be hidden?",
         "NO",
         "ImpairmentRecordedEvent emitted on-chain; ObligationStatusChangedEvent at every obligation state transition"),
        ("Can payout routing be changed by the operator?",
         "PARTIALLY",
         "Operator cannot override a member-set delegate_recipient; authorize_claim_recipient is member-only"),
        ("Is the oracle schema governance-controlled?",
         "YES",
         "outcome_schema.verified == true enforced on-chain at attestation; schema changes require governance authority signature"),
    ]
    lp_rows = [[C("LP Concern", "cell_hdr"), C("Answer", "cell_hdr"), C("Detail", "cell_hdr")]]
    for concern, answer, detail in lp_data:
        style = "cell_green" if answer in ("NO", "YES") else "cell_amber"
        lp_rows.append([C(concern), C(answer, style), C(detail)])

    story.append(std_table(lp_rows, [5 * cm, 1.8 * cm, CONTENT_W - 6.8 * cm]))

    # ── SECTION 12: References ────────────────────────────────────────────────
    story.append(SP(10))
    story.append(section_hdr("§12 — References"))
    story.append(SP(8))

    ref_rows = [
        [C("Document", "cell_hdr"), C("Path", "cell_hdr")],
        [C("Step-by-step claim truth chain narrative"),
         C("docs/architecture/genesis-protect-claim-trace.md", "cell_code")],
        [C("Claims processing specification (KR 1.2)"),
         C("docs/architecture/genesis-protect-acute-claims-processing-spec.md", "cell_code")],
        [C("Full operational protect flow (KR 1.1)"),
         C("docs/architecture/genesis-protect-acute-full-protect-flow.md", "cell_code")],
        [C("MagicBlock private claim room"),
         C("docs/architecture/magicblock-private-claim-room.md", "cell_code")],
        [C("Evidence schema (JSON)"),
         C("frontend/public/schemas/genesis-protect-acute-claim-v1.json", "cell_code")],
        [C("Anchor source — claim instructions"),
         C("programs/omegax_protocol/src/claims.rs", "cell_code")],
        [C("Anchor source — account states"),
         C("programs/omegax_protocol/src/state.rs", "cell_code")],
        [C("Anchor source — protocol events"),
         C("programs/omegax_protocol/src/events.rs", "cell_code")],
        [C("Anchor source — constants and seeds"),
         C("programs/omegax_protocol/src/constants.rs", "cell_code")],
    ]
    story.append(std_table(ref_rows, [6.5 * cm, CONTENT_W - 6.5 * cm]))

    story.append(SP(14))
    story.append(HR())
    story.append(SP(5))
    story.append(p(
        "© 2026 OmegaX Health Capital Markets  ·  omegax.health  ·  Internal — Pre-Mainnet  ·  "
        "Program ID: Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B", "note"
    ))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=draw_cover,
        onLaterPages=lambda c, d: None,
        canvasmaker=NumberedCanvas,
    )
    print(f"PDF written to:\n  {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
