"""
generate_breakpoint_docs.py
Generates two Solana Breakpoint London 2026 partnership documents:
  1. omegax-event7-breakpoint-london-offer.pdf  — Product offer deck (5 pages)
  2. omegax-loi-solana-foundation-breakpoint.pdf — Letter of Intent (2 pages)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)

PAGE_W, PAGE_H = A4

# ── Palette ───────────────────────────────────────────────────────────────────
TEAL       = colors.HexColor("#0891b2")
TEAL_D     = colors.HexColor("#0e7490")
TEAL_LIGHT = colors.HexColor("#e0f2fe")
DARK       = colors.HexColor("#0f172a")
SLATE      = colors.HexColor("#334155")
MUTED      = colors.HexColor("#64748b")
LIGHT_BG   = colors.HexColor("#f8fafc")
BORDER     = colors.HexColor("#e2e8f0")
RED        = colors.HexColor("#dc2626")
GREEN      = colors.HexColor("#16a34a")
AMBER      = colors.HexColor("#d97706")
SOL_PURPLE = colors.HexColor("#9945FF")
SOL_GREEN  = colors.HexColor("#14F195")
WHITE      = colors.white
BLACK      = colors.black

MARGIN    = 2.2 * cm
CONTENT_W = PAGE_W - 2 * MARGIN   # ≈ 166 mm


# ── Style factory ─────────────────────────────────────────────────────────────
def ps(name, **kw):
    return ParagraphStyle(name, **kw)


# Shared paragraph styles
H1   = ps("H1",   fontSize=22, leading=28, textColor=DARK,   fontName="Helvetica-Bold",  spaceBefore=6,  spaceAfter=5)
H2   = ps("H2",   fontSize=15, leading=21, textColor=TEAL_D, fontName="Helvetica-Bold",  spaceBefore=12, spaceAfter=4)
H3   = ps("H3",   fontSize=12, leading=17, textColor=DARK,   fontName="Helvetica-Bold",  spaceBefore=8,  spaceAfter=4)
BODY = ps("BODY", fontSize=10, leading=15, textColor=SLATE,  fontName="Helvetica",        spaceAfter=5)
BODYJ= ps("BODYJ",fontSize=10, leading=15, textColor=SLATE,  fontName="Helvetica",        spaceAfter=5,  alignment=TA_JUSTIFY)
BOLD = ps("BOLD", fontSize=10, leading=15, textColor=DARK,   fontName="Helvetica-Bold",   spaceAfter=3)
SMALL= ps("SMALL",fontSize=8,  leading=12, textColor=MUTED,  fontName="Helvetica")
CNTR = ps("CNTR", fontSize=10, leading=15, textColor=SLATE,  fontName="Helvetica",        alignment=TA_CENTER)


# ── Shared helpers ────────────────────────────────────────────────────────────

def banner(text, bg=TEAL, fg=WHITE, size=12):
    """Full-width coloured section header banner."""
    st = ps(f"_bn_{id(text)}", fontSize=size, leading=size + 6,
            textColor=fg, fontName="Helvetica-Bold")
    t = Table([[Paragraph(text, st)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
    ]))
    return t


def data_table(rows, col_widths, has_header=True):
    """Generic styled data table with optional teal header row."""
    t = Table(rows, colWidths=col_widths, repeatRows=1 if has_header else 0)
    style = [
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("LEADING",       (0, 0), (-1, -1), 13),
        ("TEXTCOLOR",     (0, 0), (-1, -1), DARK),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    # Alternating row shading (skip header)
    for i in range(1 if has_header else 0, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        else:
            style.append(("BACKGROUND", (0, i), (-1, i), WHITE))
    if has_header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), TEAL),
            ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 9),
        ]
    t.setStyle(TableStyle(style))
    return t


def bul(text, indent=12):
    """Bullet point paragraph."""
    uid = str(id(text))[-6:]
    return Paragraph(
        f"&#x2022; &nbsp;{text}",
        ps(f"_bul_{uid}", fontSize=10, leading=15, textColor=SLATE,
           fontName="Helvetica", leftIndent=indent, spaceAfter=3),
    )


def check(text, indent=10):
    """Checkmark point paragraph (green ✓)."""
    uid = str(id(text))[-6:]
    return Paragraph(
        f"&#x2713; &nbsp;{text}",
        ps(f"_chk_{uid}", fontSize=10, leading=15, textColor=DARK,
           fontName="Helvetica", leftIndent=indent, spaceAfter=3),
    )


def arrow(text, indent=10):
    """Arrow point paragraph."""
    uid = str(id(text))[-6:]
    return Paragraph(
        f"&#x2192; &nbsp;{text}",
        ps(f"_arr_{uid}", fontSize=10, leading=15, textColor=SLATE,
           fontName="Helvetica", leftIndent=indent, spaceAfter=4),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  OFFER DECK
# ══════════════════════════════════════════════════════════════════════════════

OFFER_OUT = (
    r"C:\Users\Admin\Desktop\Repo Omega\omegax-protocol\devnet"
    r"\omegax-event7-breakpoint-london-offer.pdf"
)


def offer_hf(canvas, doc):
    """Header / footer callback — dark full-page bg on page 1, standard on rest."""
    canvas.saveState()
    p = doc.page

    if p == 1:
        # Dark full-page background
        canvas.setFillColor(DARK)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # Teal strip top
        canvas.setFillColor(TEAL)
        canvas.rect(0, PAGE_H - 0.55 * cm, PAGE_W, 0.55 * cm, fill=1, stroke=0)
        # Solana-green accent strip bottom
        canvas.setFillColor(SOL_GREEN)
        canvas.rect(0, 0, PAGE_W, 0.45 * cm, fill=1, stroke=0)
        canvas.restoreState()
        return

    # ── Other pages ────────────────────────────────────────────────────────
    # Top rule
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, PAGE_H - 1.6 * cm, PAGE_W - MARGIN, PAGE_H - 1.6 * cm)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(TEAL_D)
    canvas.drawString(MARGIN, PAGE_H - 1.3 * cm, "GENESIS PROTECT ACUTE — EVENT 7")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.3 * cm,
                           "Solana Breakpoint London 2026  |  OmegaX Protocol")
    # Bottom rule
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.8 * cm, PAGE_W - MARGIN, 1.8 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 1.2 * cm,
                      "OmegaX Health Capital Markets  |  Pre-Mainnet Proposal  |  April 2026")
    canvas.drawRightString(PAGE_W - MARGIN, 1.2 * cm, f"Page {p - 1}")
    canvas.restoreState()


def build_offer():
    doc = SimpleDocTemplate(
        OFFER_OUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2.2 * cm, bottomMargin=2.4 * cm,
    )
    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    def cvr(txt, **kw):
        return Paragraph(txt, ps(f"_cv_{id(txt)}", **kw))

    story += [
        Spacer(1, 3.5 * cm),
        cvr("GENESIS PROTECT ACUTE",
            fontSize=11, leading=16, textColor=SOL_GREEN,
            fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4),
        Spacer(1, 0.2 * cm),
        cvr("Event 7",
            fontSize=36, leading=44, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6),
        Spacer(1, 0.3 * cm),
        cvr("Conference Edition",
            fontSize=16, leading=22, textColor=colors.HexColor("#94a3b8"),
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=20),
        # Teal rule via table
        Table([[""]], colWidths=[CONTENT_W * 0.35],
              style=TableStyle([("LINEABOVE", (0, 0), (-1, -1), 2, TEAL),
                                ("TOPPADDING", (0,0),(-1,-1), 0),
                                ("BOTTOMPADDING",(0,0),(-1,-1),12)])),
        cvr("On-Chain Acute Medical Coverage for",
            fontSize=14, leading=20, textColor=colors.HexColor("#94a3b8"),
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4),
        cvr("Solana Breakpoint London 2026",
            fontSize=22, leading=28, textColor=SOL_GREEN,
            fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=22),
        cvr("The first DeFi-native acute medical protection product on Solana.",
            fontSize=13, leading=19, textColor=colors.HexColor("#cbd5e1"),
            fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=50),
        cvr("OmegaX Health Capital Markets  |  April 2026  |  Pre-Mainnet Proposal",
            fontSize=10, leading=15, textColor=MUTED,
            fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4),
        cvr("Program ID: Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B",
            fontSize=7.5, leading=11, textColor=colors.HexColor("#334155"),
            fontName="Helvetica", alignment=TA_CENTER),
        PageBreak(),
    ]

    # ── PAGE 2 — THE GAP ──────────────────────────────────────────────────────
    story += [
        Spacer(1, 0.3 * cm),
        banner("01  |  The Gap We Fill"),
        Spacer(1, 0.4 * cm),
        Paragraph("International Attendees. Zero Medical Coverage.", H1),
        Spacer(1, 0.2 * cm),
        Paragraph(
            "Thousands of attendees travel to Solana Breakpoint London from 80+ countries. "
            "They carry laptops, hardware wallets, and conference badges — but almost none "
            "carry adequate acute medical coverage for a short international trip.",
            BODYJ,
        ),
        Spacer(1, 0.4 * cm),
    ]

    gap_rows = [
        ["The Reality for Unprotected Attendees", ""],
        ["ER visit cost in the UK (tourist, uninsured)", "£800 – £6,000+"],
        ["Standard travel insurance — minimum duration", "30 days (overkill for a 5-day conference)"],
        ["Average reimbursement wait (traditional insurer)", "3 – 8 weeks"],
        ["Conference liability for attendee medical incidents", "Zero — attendees bear all risk"],
        ["Crypto-native attendees with adequate existing policy", "< 15 % (estimated)"],
        ["Languages covered by a typical London ER", "English only — barrier for international visitors"],
    ]
    t = Table(gap_rows, colWidths=[CONTENT_W * 0.58, CONTENT_W * 0.42])
    t.setStyle(TableStyle([
        ("SPAN",          (0, 0), (-1, 0)),
        ("BACKGROUND",    (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9.5),
        ("LEADING",       (0, 0), (-1, -1), 14),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
        ("TEXTCOLOR",     (0, 1), (-1, -1), SLATE),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0, 1), (0, -1), DARK),
        ("BACKGROUND",    (0, 2), (-1, 2), LIGHT_BG),
        ("BACKGROUND",    (0, 4), (-1, 4), LIGHT_BG),
        ("BACKGROUND",    (0, 6), (-1, 6), LIGHT_BG),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Existing solutions fail the conference use case: standard travel insurance is designed "
        "for 30-day+ holidays, not 5-day tech conferences. Claims are slow, opaque, and often "
        "exclude activities common at side events. "
        "<b>There is no product built specifically for the acute, short-duration, internationally "
        "mobile conference attendee.</b>",
        BODYJ,
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "OmegaX changes that.",
        ps("_teal_cta", fontSize=15, leading=21, textColor=TEAL_D,
           fontName="Helvetica-Bold", alignment=TA_CENTER),
    ))
    story.append(PageBreak())

    # ── PAGE 3 — THE PRODUCT ──────────────────────────────────────────────────
    story += [
        Spacer(1, 0.3 * cm),
        banner("02  |  Introducing Event 7"),
        Spacer(1, 0.4 * cm),
        Paragraph("7 Days. $39. Up to $1,500 Fixed Benefit.", H1),
        Spacer(1, 0.2 * cm),
        Paragraph(
            "Genesis Protect Acute Event 7 is the first product of the OmegaX protocol — "
            "a fixed-benefit acute medical policy engineered for the conference attendee: "
            "short duration, fixed benefit, instant USDC settlement, and full on-chain transparency.",
            BODYJ,
        ),
        Spacer(1, 0.4 * cm),
    ]

    # Three feature pillars
    fw = (CONTENT_W - 4) / 3
    feat_head_style = ps("_fh", fontSize=10, leading=14, textColor=TEAL_D,
                         fontName="Helvetica-Bold", alignment=TA_CENTER)
    feat_body_style = ps("_fb", fontSize=9, leading=13, textColor=SLATE,
                         fontName="Helvetica", alignment=TA_CENTER)
    feat = Table(
        [
            [Paragraph("FIXED BENEFIT", feat_head_style),
             Paragraph("FULLY ON-CHAIN", feat_head_style),
             Paragraph("ACTUARIALLY BACKED", feat_head_style)],
            [Paragraph("No paperwork. Approved claims settle in USDC within 24–48 h of discharge.", feat_body_style),
             Paragraph("Every policy, claim, and USDC movement is visible on Solana mainnet.", feat_body_style),
             Paragraph("41.5% loss ratio. VaR 99% reserve model. Pool fully collateralised at launch.", feat_body_style)],
        ],
        colWidths=[fw, fw, fw],
    )
    feat.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL_LIGHT),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("LINEAFTER",     (0, 0), (1, -1), 1, TEAL),
        ("BOX",           (0, 0), (-1, -1), 1, TEAL),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(feat)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Benefit Schedule", H3))
    tier_rows = [
        ["Clinical Tier", "Trigger", "Fixed Benefit"],
        ["Tier 1 — ER Same-Day",      "ER visit, discharged same day",              "$300"],
        ["Tier 2 — Overnight",         "Hospital admission, 1–2 nights",             "$700"],
        ["Tier 3 — Surgery + ICU",     "Surgery and / or ICU, 2+ nights",            "$1,500  (max)"],
    ]
    story.append(data_table(tier_rows, [CONTENT_W * 0.30, CONTENT_W * 0.48, CONTENT_W * 0.22]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Policy Mechanics", H3))
    for item in [
        "Premium: <b>$39 USDC</b> per policy, paid at mint",
        "Coverage window: <b>7 consecutive days</b> from activation",
        "Settlement currency: <b>USDC</b> — direct to policyholder wallet",
        "Claim review SLA: <b>24 hours</b> (Phase 0 human oracle)",
        "Max benefit per policy: <b>$1,500</b>  |  One claim per coverage period",
        "Policy format: <b>Solana account</b> linked to attendee wallet — no app download required",
    ]:
        story.append(bul(item))
    story.append(PageBreak())

    # ── PAGE 4 — THE OFFER ────────────────────────────────────────────────────
    story += [
        Spacer(1, 0.3 * cm),
        banner("03  |  The Breakpoint London Partnership Proposal"),
        Spacer(1, 0.4 * cm),
        Paragraph("Two Models. Your Choice.", H1),
        Spacer(1, 0.2 * cm),
        Paragraph(
            "We are proposing a formal partnership with the Solana Foundation to offer Genesis Protect "
            "Acute Event 7 to all Solana Breakpoint London 2026 attendees. "
            "Two commercial structures are available, both fully negotiable:",
            BODYJ,
        ),
        Spacer(1, 0.4 * cm),
        banner("Option A — Sponsored Coverage  (Foundation Pays)", bg=DARK, size=11),
        Spacer(1, 0.2 * cm),
    ]
    option_a = [
        ["Parameter", "Detail"],
        ["Who pays",          "Solana Foundation — bulk purchase on behalf of all registered attendees"],
        ["Cost per attendee", "$39 USDC per policy"],
        ["Example: 2,000 attendees", "Total premium $78,000  →  Expected net claim cost ≈ $32,400"],
        ["Example: 3,500 attendees", "Total premium $136,500  →  Expected net claim cost ≈ $56,700"],
        ["Attendee experience",   "Wallet-linked Event 7 policy delivered at badge pickup / registration QR"],
        ["Foundation receives",   "\"Protected by OmegaX\" co-brand  ·  On-chain proof of care  ·  PR value"],
        ["Surplus routing",       "Net underwriting surplus returned to SF Ecosystem Fund (negotiable)"],
    ]
    story.append(data_table(option_a, [CONTENT_W * 0.30, CONTENT_W * 0.70]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(banner("Option B — Opt-In at Registration  (Zero Cost to Foundation)", bg=TEAL_D, size=11))
    story.append(Spacer(1, 0.2 * cm))
    option_b = [
        ["Parameter", "Detail"],
        ["Who pays",          "Individual attendees — opt-in checkout during Breakpoint registration"],
        ["Cost per attendee", "$39 USDC per policy (self-purchased)"],
        ["Target opt-in rate","15 – 25 % of attendees  →  ≈ 300 – 875 policies at 2,000–3,500 attendees"],
        ["Integration",       "OmegaX policy mint widget embedded in Breakpoint checkout (iframe / link)"],
        ["Foundation receives","Revenue share: 10 % of net underwriting surplus → SF Ecosystem Fund"],
        ["OmegaX provides",   "Co-branded landing page  ·  Integration support  ·  Post-event analytics report"],
    ]
    story.append(data_table(option_b, [CONTENT_W * 0.30, CONTENT_W * 0.70]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Both options are fully negotiable. We are open to hybrid structures (e.g., Foundation sponsors "
        "a reduced-rate policy at $19 per attendee, OmegaX absorbs the delta). "
        "Our goal: a live, real-world proof of on-chain health capital markets at conference scale.",
        ps("_note", fontSize=9, leading=14, textColor=MUTED,
           fontName="Helvetica-Oblique", spaceAfter=4),
    ))
    story.append(PageBreak())

    # ── PAGE 5 — ON-CHAIN + WHY NOW ───────────────────────────────────────────
    story += [
        Spacer(1, 0.3 * cm),
        banner("04  |  On-Chain. Transparent. Fast."),
        Spacer(1, 0.4 * cm),
        Paragraph("Built Natively on Solana.", H1),
        Spacer(1, 0.2 * cm),
    ]
    flow_rows = [
        ["Step", "What Happens", "On-Chain Action"],
        ["1. Policy Mint",    "Attendee activates at registration or self-service",          "PolicyAccount created on Solana mainnet"],
        ["2. Medical Event",  "Attendee seeks emergency care — any facility, worldwide",      "—"],
        ["3. Claim Submit",   "Attendee submits invoice + discharge note via oracle portal",  "ClaimAccount created → SUBMITTED"],
        ["4. Oracle Review",  "Human operator reviews documents. SLA: 24 h. Tier assigned.", "intakeStatus → UNDER_REVIEW"],
        ["5. Approval",       "Claim approved. Benefit tier determined ($300 / $700 / $1,500).", "intakeStatus → APPROVED, USDC reserved"],
        ["6. Settlement",     "USDC transferred atomically to attendee wallet.",             "intakeStatus → FULLY_SETTLED"],
    ]
    story.append(data_table(flow_rows, [CONTENT_W * 0.14, CONTENT_W * 0.42, CONTENT_W * 0.44]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Protocol Integrity Guarantees", H3))
    for item in [
        "Reserve fully collateralised: LP pool backs every policy before mint is permitted",
        "Max capacity at launch: <b>1,444 concurrent Event 7 policyholders</b> (VaR 99% actuarial model)",
        "All transactions auditable on Solana Explorer — program Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B",
        "Reserve locked in protocol PDA — no LP withdrawal during active coverage window",
        "USDC settlement — no price volatility, no slippage, no gas overhead for the claimant",
    ]:
        story.append(check(item))

    story.append(Spacer(1, 0.4 * cm))
    story.append(banner("05  |  Why This. Why Now."))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("The Breakpoint Moment.", H2))
    for item in [
        "<b>OmegaX is the only DeFi-native health capital markets protocol on Solana.</b> No competitor is building this at protocol level.",
        "<b>Breakpoint London = first live deployment</b> of Genesis Protect Acute v1. A landmark event deserves a landmark first use.",
        "<b>The attendee profile is ideal:</b> crypto-native, globally mobile, technically sophisticated — and chronically underinsured for short international trips.",
        "<b>Real claim data, real settlement:</b> a fully loaded event pool generates live on-chain proof for institutional LP recruitment.",
        "<b>The headline writes itself:</b> \"Solana Breakpoint attendees covered by on-chain insurance\" — zero incremental PR cost for either party.",
    ]:
        story.append(arrow(item))

    story.append(Spacer(1, 0.5 * cm))
    # CTA box
    cta = Table([[
        Paragraph(
            "Ready to structure a deal?<br/>Contact us to align on the model that fits Breakpoint's budget and goals.<br/><br/>"
            "<b>hello@omegax.xyz  |  @omegaxprotocol  |  omegax.xyz</b>",
            ps("_cta", fontSize=11, leading=17, textColor=WHITE,
               fontName="Helvetica", alignment=TA_CENTER),
        )
    ]], colWidths=[CONTENT_W])
    cta.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL_D),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(cta)

    doc.build(story, onFirstPage=offer_hf, onLaterPages=offer_hf)
    print(f"Offer PDF: {OFFER_OUT}")


# ══════════════════════════════════════════════════════════════════════════════
#  LETTER OF INTENT
# ══════════════════════════════════════════════════════════════════════════════

LOI_OUT = (
    r"C:\Users\Admin\Desktop\Repo Omega\omegax-protocol\devnet"
    r"\omegax-loi-solana-foundation-breakpoint.pdf"
)


def loi_hf(canvas, doc):
    """Header / footer for LOI pages."""
    canvas.saveState()
    p = doc.page
    # Teal top strip
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 0.45 * cm, PAGE_W, 0.45 * cm, fill=1, stroke=0)
    # Header text
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(TEAL_D)
    canvas.drawString(MARGIN, PAGE_H - 1.1 * cm, "OmegaX Health Capital Markets")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.1 * cm,
                           "Letter of Intent — Solana Foundation × OmegaX")
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 1.4 * cm, PAGE_W - MARGIN, PAGE_H - 1.4 * cm)
    # Footer
    canvas.line(MARGIN, 1.8 * cm, PAGE_W - MARGIN, 1.8 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 1.2 * cm,
                      "Confidential  |  Non-Binding Letter of Intent  |  April 23, 2026")
    canvas.drawRightString(PAGE_W - MARGIN, 1.2 * cm, f"Page {p}")
    canvas.restoreState()


def loi_sec(title):
    uid = str(id(title))[-5:]
    return Paragraph(
        title,
        ps(f"_ls_{uid}", fontSize=12, leading=17, textColor=TEAL_D,
           fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=5),
    )


def loi_body(text):
    uid = str(id(text))[-5:]
    return Paragraph(
        text,
        ps(f"_lb_{uid}", fontSize=10.5, leading=16, textColor=DARK,
           fontName="Helvetica", spaceAfter=7, alignment=TA_JUSTIFY),
    )


def loi_bul(text):
    uid = str(id(text))[-5:]
    return Paragraph(
        f"&#x2022; &nbsp;{text}",
        ps(f"_lbu_{uid}", fontSize=10.5, leading=16, textColor=DARK,
           fontName="Helvetica", leftIndent=14, spaceAfter=4),
    )


def build_loi():
    doc = SimpleDocTemplate(
        LOI_OUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2.2 * cm, bottomMargin=2.4 * cm,
    )
    story = []

    # ── Sender block ──────────────────────────────────────────────────────────
    story += [
        Spacer(1, 0.2 * cm),
        Paragraph("OmegaX Health Capital Markets",
                  ps("_snd", fontSize=14, leading=20, textColor=DARK,
                     fontName="Helvetica-Bold", spaceAfter=2)),
        Paragraph("hello@omegax.xyz  |  omegax.xyz  |  @omegaxprotocol",
                  ps("_snd2", fontSize=9, leading=13, textColor=MUTED,
                     fontName="Helvetica", spaceAfter=2)),
        Paragraph("Solana Program ID: Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B",
                  ps("_snd3", fontSize=8, leading=12, textColor=MUTED,
                     fontName="Helvetica", spaceAfter=14)),
        HRFlowable(width=CONTENT_W, color=BORDER, thickness=1, spaceAfter=14),
    ]

    # Date + addressee block
    addr = [
        [Paragraph("April 23, 2026",
                   ps("_dt", fontSize=10, leading=15, textColor=DARK,
                      fontName="Helvetica")),
         Paragraph("", ps("_e1"))],
        [Paragraph("", ps("_e2")), Paragraph("", ps("_e3"))],
        [Paragraph("<b>To:</b>",
                   ps("_to1", fontSize=10, leading=15, textColor=DARK,
                      fontName="Helvetica")),
         Paragraph("Solana Foundation Events Team",
                   ps("_to2", fontSize=10, leading=15, textColor=DARK,
                      fontName="Helvetica-Bold"))],
        [Paragraph("", ps("_e4")),
         Paragraph("Solana Foundation",
                   ps("_to3", fontSize=10, leading=15, textColor=SLATE,
                      fontName="Helvetica"))],
    ]
    addr_t = Table(addr, colWidths=[CONTENT_W * 0.14, CONTENT_W * 0.86])
    addr_t.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(addr_t)
    story.append(Spacer(1, 0.3 * cm))

    # Subject line (teal left-bordered box)
    subj = Table([[
        Paragraph(
            "<b>RE: Letter of Intent — Genesis Protect Acute Event 7 × Solana Breakpoint London 2026</b>",
            ps("_subj", fontSize=11, leading=16, textColor=DARK, fontName="Helvetica-Bold"),
        )
    ]], colWidths=[CONTENT_W])
    subj.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL_LIGHT),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("LINEBEFORE",    (0, 0), (0, -1), 4, TEAL),
    ]))
    story.append(subj)
    story.append(Spacer(1, 0.4 * cm))

    story.append(loi_body("Dear Solana Foundation Team,"))
    story.append(Spacer(1, 0.1 * cm))

    # ── 1. Background ─────────────────────────────────────────────────────────
    story.append(loi_sec("1.  Background and Purpose"))
    story.append(loi_body(
        "OmegaX Health Capital Markets (\"OmegaX\") is building the first decentralised health capital "
        "markets protocol on Solana. Our flagship product, <b>Genesis Protect Acute v1</b>, is a "
        "fully on-chain acute medical insurance system featuring programmable reserve pools, oracle-verified "
        "claim processing, and USDC-denominated settlement on Solana mainnet."
    ))
    story.append(loi_body(
        "The purpose of this Letter of Intent is to propose a formal partnership with the Solana Foundation "
        "to deploy <b>Genesis Protect Acute Event 7</b> as the official acute medical protection product "
        "for <b>Solana Breakpoint London 2026</b>. This would represent the first live real-world deployment "
        "of the OmegaX protocol and a landmark demonstration of on-chain health capital markets at "
        "conference scale."
    ))

    # ── 2. Proposed Structure ─────────────────────────────────────────────────
    story.append(loi_sec("2.  Proposed Partnership Structure"))
    story.append(loi_body("OmegaX proposes two alternative commercial structures, subject to negotiation:"))

    story.append(Paragraph(
        "<b>Option A — Sponsored Coverage:</b>",
        ps("_oA", fontSize=10.5, leading=16, textColor=DARK,
           fontName="Helvetica-Bold", spaceAfter=3),
    ))
    for item in [
        "The Solana Foundation purchases Event 7 policies on behalf of all registered Breakpoint attendees.",
        "Cost: <b>$39 USDC per policy</b> (bulk pricing available for 2,000+ policies).",
        "Policies are wallet-linked and delivered at check-in or via registration QR flow.",
        "Expected net claim cost: ≈ 41.5% of total premium pool (actuarially modelled, VaR 99%).",
        "Optional: net underwriting surplus returned to the SF Ecosystem Fund at policy expiry.",
    ]:
        story.append(loi_bul(item))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph(
        "<b>Option B — Opt-In at Registration:</b>",
        ps("_oB", fontSize=10.5, leading=16, textColor=DARK,
           fontName="Helvetica-Bold", spaceAfter=3),
    ))
    for item in [
        "Event 7 presented as an optional add-on during Breakpoint registration checkout ($39 USDC).",
        "Zero upfront cost to the Solana Foundation.",
        "Target opt-in rate: 15–25% of attendees (~300–875 policies at 2,000–3,500 attendees).",
        "OmegaX provides a co-branded checkout widget and post-event analytics report.",
        "Revenue share: 10% of net underwriting surplus donated to the Solana Foundation Ecosystem Fund.",
    ]:
        story.append(loi_bul(item))
    story.append(Spacer(1, 0.1 * cm))
    story.append(loi_body(
        "The parties are open to hybrid structures. All binding obligations will arise only from a "
        "definitive partnership agreement."
    ))

    # ── 3. OmegaX Commitments ─────────────────────────────────────────────────
    story.append(loi_sec("3.  OmegaX Commitments"))
    story.append(loi_body(
        "Subject to execution of a definitive agreement, OmegaX commits to:"
    ))
    for item in [
        "<b>Reserve Adequacy:</b> Maintain a fully collateralised reserve pool prior to any policy mint, meeting or exceeding VaR 99% requirements for the expected policy volume.",
        "<b>Oracle Operations:</b> Staff Phase 0 human oracle operators for the duration of the coverage window plus 72 hours post-event, with a 24-hour claim review SLA.",
        "<b>Technical Integration:</b> Deliver a co-branded policy issuance flow compatible with the Breakpoint registration system (wallet-connect + USDC payment).",
        "<b>Transparency:</b> Provide the Solana Foundation with real-time access to all on-chain policy and claim data throughout the event and settlement period.",
        "<b>Mainnet Readiness:</b> Complete protocol audit and deploy Genesis Protect Acute v1 to Solana mainnet no later than 30 days prior to event start.",
        "<b>Post-Event Report:</b> Deliver a full actuarial and operational post-event analysis within 14 days of policy expiry.",
    ]:
        story.append(loi_bul(item))

    # ── 4. Foundation Commitments ─────────────────────────────────────────────
    story.append(loi_sec("4.  Foundation Commitments Requested"))
    story.append(loi_body("OmegaX respectfully requests the following from the Solana Foundation:"))
    for item in [
        "<b>Official Endorsement:</b> Recognition of OmegaX as the official medical protection partner for Solana Breakpoint London 2026, with branding in attendee communications and on the event website.",
        "<b>Registration Integration:</b> Integration of the OmegaX policy mint widget into the Breakpoint registration and check-in flow.",
        "<b>Co-Marketing:</b> Joint announcement across Solana Foundation social channels and Breakpoint conference materials.",
        "<b>Data Sharing:</b> Aggregated (anonymised) attendee count and origin data, sufficient to right-size the reserve pool prior to the event.",
    ]:
        story.append(loi_bul(item))

    story.append(PageBreak())

    # ── 5. Commercial Terms ───────────────────────────────────────────────────
    story.append(loi_sec("5.  Indicative Commercial Terms"))
    terms = [
        ["Term", "Indicative Position"],
        ["Premium per policy",          "$39 USDC (bulk discount TBD for Option A ≥ 2,000 policies)"],
        ["Revenue share (Option B)",    "10% of net underwriting surplus → SF Ecosystem Fund"],
        ["Surplus return (Option A)",   "Negotiable — SF Ecosystem Fund, rebate, or designated charity"],
        ["Minimum policy volume",       "200 policies (threshold for viable oracle staffing)"],
        ["Decision deadline",           "90 days prior to event start (for reserve deployment + integration)"],
        ["Protocol audit requirement",  "Complete prior to mainnet deployment (committed by OmegaX)"],
        ["Governing jurisdiction",      "To be agreed in definitive partnership agreement"],
    ]
    story.append(data_table(terms, [CONTENT_W * 0.38, CONTENT_W * 0.62]))

    # ── 6. Timeline ───────────────────────────────────────────────────────────
    story.append(loi_sec("6.  Indicative Timeline"))
    timeline = [
        ["Milestone", "Target Date"],
        ["LOI countersigned by Solana Foundation",         "May 2026"],
        ["Definitive Partnership Agreement executed",       "June 2026"],
        ["Protocol audit complete / Solana mainnet deploy", "July 2026"],
        ["Technical integration with Breakpoint registration","August 2026"],
        ["Reserve pool funded and sealed",                 "2 weeks pre-event"],
        ["Solana Breakpoint London 2026 — coverage window","September / October 2026 (TBC)"],
        ["Policy expiry + settlement complete",            "Within 72 h post-event"],
        ["Post-event actuarial report delivered",          "Within 14 days of expiry"],
    ]
    story.append(data_table(timeline, [CONTENT_W * 0.54, CONTENT_W * 0.46]))

    # ── 7. Non-Binding ────────────────────────────────────────────────────────
    story.append(loi_sec("7.  Non-Binding Nature"))
    story.append(loi_body(
        "This Letter of Intent is non-binding and is intended solely to record the mutual interest of "
        "the parties in exploring a partnership. It does not constitute a legally binding commitment "
        "and does not obligate either party to enter into a definitive agreement. All binding obligations "
        "will arise only upon execution of a separate, signed partnership agreement."
    ))

    # ── 8. Next Steps ────────────────────────────────────────────────────────
    story.append(loi_sec("8.  Next Steps"))
    story.append(loi_body(
        "We propose a call within the next two weeks to align on the preferred commercial structure, "
        "confirm event logistics, and agree a timeline for a definitive agreement. "
        "Please reach out at your earliest convenience:"
    ))
    next_t = Table([[
        Paragraph(
            "<b>hello@omegax.xyz  |  @omegaxprotocol  |  omegax.xyz</b>",
            ps("_nxt", fontSize=11, leading=16, textColor=WHITE,
               fontName="Helvetica-Bold", alignment=TA_CENTER),
        )
    ]], colWidths=[CONTENT_W])
    next_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), TEAL_D),
        ("TOPPADDING",    (0, 0), (-1, -1), 13),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
    ]))
    story.append(next_t)
    story.append(Spacer(1, 0.4 * cm))

    story.append(loi_body(
        "We are genuinely excited about the prospect of building something historic together — "
        "the first on-chain acute medical protection product deployed at a major web3 conference, "
        "on Solana. We look forward to hearing from you."
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(loi_body("Sincerely,"))
    story.append(Spacer(1, 0.7 * cm))

    sign = Table(
        [
            [Paragraph("OmegaX Protocol Team",
                       ps("_sg1", fontSize=11, leading=16, textColor=DARK,
                          fontName="Helvetica-Bold")), ""],
            [Paragraph("OmegaX Health Capital Markets",
                       ps("_sg2", fontSize=10, leading=15, textColor=SLATE,
                          fontName="Helvetica")), ""],
            [Paragraph("April 23, 2026",
                       ps("_sg3", fontSize=10, leading=15, textColor=SLATE,
                          fontName="Helvetica")), ""],
        ],
        colWidths=[CONTENT_W * 0.5, CONTENT_W * 0.5],
    )
    sign.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    story.append(sign)
    story.append(Spacer(1, 0.8 * cm))
    story.append(HRFlowable(width=CONTENT_W, color=BORDER, thickness=0.5))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "This document is confidential and intended solely for the Solana Foundation. "
        "OmegaX Protocol is built on Solana using the Anchor framework (AGPL-3.0). "
        "Genesis Protect Acute v1 is a pre-mainnet product undergoing final audit. "
        "Program ID: Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B",
        ps("_disc", fontSize=7.5, leading=11, textColor=MUTED,
           fontName="Helvetica", alignment=TA_CENTER),
    ))

    doc.build(story, onFirstPage=loi_hf, onLaterPages=loi_hf)
    print(f"LOI PDF: {LOI_OUT}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_offer()
    build_loi()
