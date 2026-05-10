"""
Genesis Protect Acute v1 — Actuarial Reserve Analysis PDF Generator
OmegaX Protocol | April 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.colors import HexColor

# ── Palette ────────────────────────────────────────────────────────────────
TEAL        = HexColor('#0891b2')
TEAL_LIGHT  = HexColor('#e0f2fe')
TEAL_MID    = HexColor('#bae6fd')
RED         = HexColor('#dc2626')
RED_LIGHT   = HexColor('#fee2e2')
AMBER       = HexColor('#d97706')
AMBER_LIGHT = HexColor('#fef3c7')
GREEN       = HexColor('#16a34a')
GREEN_LIGHT = HexColor('#dcfce7')
DARK        = HexColor('#0f172a')
SLATE       = HexColor('#475569')
LIGHT_GREY  = HexColor('#f1f5f9')
MID_GREY    = HexColor('#e2e8f0')
WHITE       = colors.white

OUTPUT = r"C:\Users\Admin\Desktop\Repo Omega\omegax-protocol\devnet\omegax-genesis-actuarial-report-2026-04-23.pdf"

PAGE_W, PAGE_H = A4
MARGIN_L = 2.0 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 2.2 * cm
MARGIN_B = 2.2 * cm

# ── Header / Footer canvas callback ───────────────────────────────────────
def header_footer(canv, doc):
    canv.saveState()
    # Skip header/footer on cover page (page 1)
    if doc.page == 1:
        canv.restoreState()
        return

    # Header bar
    canv.setFillColor(TEAL)
    canv.rect(MARGIN_L, PAGE_H - 1.4 * cm, PAGE_W - MARGIN_L - MARGIN_R, 0.45 * cm, fill=1, stroke=0)
    canv.setFillColor(WHITE)
    canv.setFont('Helvetica-Bold', 7)
    canv.drawString(MARGIN_L + 4, PAGE_H - 1.08 * cm, 'Genesis Protect Acute v1  |  Actuarial Reserve Analysis')
    canv.drawRightString(PAGE_W - MARGIN_R - 4, PAGE_H - 1.08 * cm, 'OmegaX Protocol  —  Internal  |  Pre-Mainnet  |  April 2026')

    # Footer line
    canv.setStrokeColor(MID_GREY)
    canv.setLineWidth(0.5)
    canv.line(MARGIN_L, 1.4 * cm, PAGE_W - MARGIN_R, 1.4 * cm)
    canv.setFillColor(SLATE)
    canv.setFont('Helvetica', 7)
    canv.drawString(MARGIN_L, 0.9 * cm, '© 2026 OmegaX Health Capital Markets  —  Confidential')
    canv.drawRightString(PAGE_W - MARGIN_R, 0.9 * cm, f'Page {doc.page}')

    canv.restoreState()


# ── Style helpers ──────────────────────────────────────────────────────────
base_styles = getSampleStyleSheet()

def style(name, parent='Normal', **kw):
    s = ParagraphStyle(name, parent=base_styles[parent], **kw)
    return s

S_COVER_TITLE = style('CoverTitle', fontSize=26, leading=32,
                       textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)
S_COVER_SUB   = style('CoverSub',   fontSize=14, leading=20,
                       textColor=TEAL_MID, fontName='Helvetica', alignment=TA_CENTER)
S_COVER_META  = style('CoverMeta',  fontSize=8,  leading=13,
                       textColor=HexColor('#94a3b8'), fontName='Helvetica', alignment=TA_CENTER)
S_COVER_BADGE = style('CoverBadge', fontSize=9,  leading=13,
                       textColor=TEAL_MID, fontName='Helvetica-Bold', alignment=TA_CENTER)

S_SECTION     = style('Section', fontSize=13, leading=17, spaceBefore=18, spaceAfter=6,
                       textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_LEFT)
S_SUBSECTION  = style('Subsec', fontSize=10, leading=14, spaceBefore=12, spaceAfter=4,
                       textColor=TEAL, fontName='Helvetica-Bold')
S_BODY        = style('Body', fontSize=9, leading=14, spaceBefore=3, spaceAfter=3,
                       textColor=DARK, fontName='Helvetica', alignment=TA_JUSTIFY)
S_BODY_BOLD   = style('BodyBold', fontSize=9, leading=14,
                       textColor=DARK, fontName='Helvetica-Bold')
S_MONO        = style('Mono', fontSize=8.5, leading=13, spaceBefore=6, spaceAfter=6,
                       textColor=DARK, fontName='Courier',
                       backColor=LIGHT_GREY, leftIndent=12, rightIndent=12,
                       borderPad=6)
S_NOTE        = style('Note', fontSize=8, leading=12, spaceBefore=4, spaceAfter=4,
                       textColor=SLATE, fontName='Helvetica-Oblique')
S_WARN        = style('Warn', fontSize=8.5, leading=13,
                       textColor=AMBER, fontName='Helvetica-Bold')
S_OK          = style('Ok', fontSize=8.5, leading=13,
                       textColor=GREEN, fontName='Helvetica-Bold')
S_TH          = style('TH', fontSize=8, leading=11,
                       textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER)
S_TD          = style('TD', fontSize=8, leading=11,
                       textColor=DARK, fontName='Helvetica', alignment=TA_CENTER)
S_TD_L        = style('TDL', fontSize=8, leading=11,
                       textColor=DARK, fontName='Helvetica', alignment=TA_LEFT)
S_TD_RED      = style('TDR', fontSize=8, leading=11,
                       textColor=RED, fontName='Helvetica-Bold', alignment=TA_CENTER)
S_TD_GREEN    = style('TDG', fontSize=8, leading=11,
                       textColor=GREEN, fontName='Helvetica-Bold', alignment=TA_CENTER)


# ── Table style builder ────────────────────────────────────────────────────
def base_table_style(col_widths=None):
    return TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0),  TEAL),
        ('TEXTCOLOR',    (0, 0), (-1, 0),  WHITE),
        ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1, 0),  8),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ('GRID',         (0, 0), (-1, -1), 0.4, MID_GREY),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])


def section_header(text):
    """Returns a teal banner paragraph for section titles."""
    data = [[Paragraph(text, S_SECTION)]]
    t = Table(data, colWidths=[PAGE_W - MARGIN_L - MARGIN_R])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4]),
    ]))
    return t


def p(text, st=None):
    return Paragraph(text, st or S_BODY)


def sp(h=6):
    return Spacer(1, h)


def hr():
    return HRFlowable(width='100%', thickness=0.5, color=MID_GREY,
                      spaceBefore=4, spaceAfter=4)


# ── COVER PAGE ─────────────────────────────────────────────────────────────
def build_cover():
    story = []

    # Dark full-page background via a Table trick
    cover_data = [['']]
    cover_table = Table(cover_data,
                        colWidths=[PAGE_W - MARGIN_L - MARGIN_R],
                        rowHeights=[PAGE_H - MARGIN_T - MARGIN_B - 2 * cm])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK),
        ('ROUNDEDCORNERS', [8]),
    ]))

    # Build content as separate elements
    story.append(sp(2.5 * cm))

    # Logo line
    story.append(p('<b>Ω  OmegaX Health Capital Markets</b>',
                   style('logo', fontSize=11, textColor=TEAL_MID,
                         fontName='Helvetica-Bold', alignment=TA_CENTER)))
    story.append(sp(0.8 * cm))

    # Teal divider
    story.append(HRFlowable(width='40%', thickness=1.5, color=TEAL,
                             hAlign='CENTER', spaceBefore=0, spaceAfter=0))
    story.append(sp(0.8 * cm))

    # Main title
    story.append(p('Genesis Protect Acute v1', S_COVER_TITLE))
    story.append(sp(0.3 * cm))
    story.append(p('Actuarial Reserve Analysis', S_COVER_SUB))
    story.append(sp(0.2 * cm))
    story.append(p('Capacity  ·  Stress Scenarios  ·  LP Economics',
                   style('cov3', fontSize=11, textColor=HexColor('#64748b'),
                         fontName='Helvetica', alignment=TA_CENTER)))

    story.append(sp(1.8 * cm))
    story.append(HRFlowable(width='60%', thickness=0.5, color=HexColor('#334155'),
                             hAlign='CENTER', spaceBefore=0, spaceAfter=0))
    story.append(sp(1.0 * cm))

    # Meta grid
    meta = [
        ['Protocol', 'OmegaX Protocol — Solana / Anchor'],
        ['Program ID', 'Bn6eixac1QEEVErGBvBjxAd6pgB9e2q4XHvAkinQ5y1B'],
        ['Product', 'Genesis Protect Acute v1  (Event 7 + Travel 30)'],
        ['Date', 'April 23, 2026'],
        ['Classification', 'Internal — Pre-Mainnet Analysis'],
        ['Network', 'Devnet  →  Mainnet pending'],
    ]
    meta_style = TableStyle([
        ('ALIGN',        (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN',        (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME',     (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME',     (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE',     (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR',    (0, 0), (0, -1), TEAL_MID),
        ('TEXTCOLOR',    (1, 0), (1, -1), HexColor('#cbd5e1')),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('LEFTPADDING',  (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])
    meta_t = Table(meta, colWidths=[4.5 * cm, 10.5 * cm])
    meta_t.setStyle(meta_style)
    story.append(meta_t)

    story.append(sp(2.5 * cm))
    story.append(HRFlowable(width='40%', thickness=1.5, color=TEAL,
                             hAlign='CENTER', spaceBefore=0, spaceAfter=0))
    story.append(sp(0.6 * cm))
    story.append(p('© 2026 OmegaX Health Capital Markets  —  All rights reserved',
                   style('copy', fontSize=7.5, textColor=HexColor('#475569'),
                         fontName='Helvetica', alignment=TA_CENTER)))

    story.append(PageBreak())
    return story


# ── SECTION 1: Reserve Baseline ────────────────────────────────────────────
def build_section1():
    story = []
    story.append(section_header('1.  Protocol Reserve Baseline'))
    story.append(sp(8))
    story.append(p('The Genesis Protect Acute pool is a dedicated reserve sleeve on the OmegaX '
                   'devnet, backed by two capital classes (Senior and Junior) and structured '
                   'across three funding-line types per product SKU.'))
    story.append(sp(6))

    story.append(p('<b>Table 1 — Current Funding Stack (from devnet manifest)</b>', S_SUBSECTION))
    headers = [
        [p('Product', S_TH), p('Sponsor\n(type 0)', S_TH),
         p('Premiums\n(type 1)', S_TH), p('LP Reserve\n(type 2)', S_TH),
         p('Total', S_TH)]
    ]
    rows = [
        [p('Event 7', S_TD_L), p('$12,500', S_TD), p('$8,400\n(~215 policies)', S_TD),
         p('$12,500', S_TD), p('$33,400', S_TD)],
        [p('Travel 30', S_TD_L), p('—', S_TD), p('$9,900\n(~100 policies)', S_TD),
         p('$45,000', S_TD), p('$54,900', S_TD)],
        [p('Pool Total', style('ptot', fontSize=8, fontName='Helvetica-Bold',
                                textColor=WHITE, alignment=TA_LEFT)),
         p('', S_TD), p('', S_TD),
         p('$57,500 TVL', style('tvl', fontSize=8, fontName='Helvetica-Bold',
                                 textColor=WHITE, alignment=TA_CENTER)),
         p('', S_TD)],
    ]
    t1 = Table(headers + rows, colWidths=[3.0*cm, 2.8*cm, 3.5*cm, 3.2*cm, 2.5*cm])
    ts = base_table_style()
    ts.add('BACKGROUND', (0, 3), (-1, 3), DARK)
    ts.add('TEXTCOLOR',  (0, 3), (-1, 3), WHITE)
    ts.add('FONTNAME',   (0, 3), (-1, 3), 'Helvetica-Bold')
    ts.add('SPAN',       (2, 3), (3, 3))
    t1.setStyle(ts)
    story.append(t1)
    story.append(sp(6))

    story.append(p('<b>Capital class allocation:</b>  Junior class ($32,500) → $12,500 to Event 7 '
                   'LP lane + $20,000 to Travel 30 LP lane.  Senior class ($25,000) → entirely '
                   'allocated to Travel 30 LP lane.  The senior tranche absorbs losses only after '
                   'the junior first-loss class is depleted.'))
    story.append(sp(4))
    story.append(p('<b>Policy addresses:</b>  Health Plan <font name="Courier" size="7.5">'
                   'D38bBYTWAkcyJZHFaZLRYRJErwLNB45YKJPfxU4PL5F6</font>  |  '
                   'Event 7 Series <font name="Courier" size="7.5">'
                   '6ZfyGQUcW132mEmYBmT5RtoagZyTHi2gTuGQUHW2qTLX</font>  |  '
                   'Travel 30 Series <font name="Courier" size="7.5">'
                   '29XmfdaHceAeAvtiESAcNDXLsJxEqW2RBa3DttTUUcco</font>'))
    return story


# ── SECTION 2: Actuarial Parameters ───────────────────────────────────────
def build_section2():
    story = []
    story.append(sp(12))
    story.append(section_header('2.  Actuarial Parameters'))
    story.append(sp(8))
    story.append(p('The following parameters are derived from the 32 claim simulation scenarios '
                   '(genesis-acute-claim-simulations-v1.json) and standard actuarial assumptions '
                   'for acute short-term travel insurance.'))
    story.append(sp(6))

    story.append(p('<b>Table 2 — Product Parameter Summary</b>', S_SUBSECTION))
    h = [[p('Parameter', S_TH), p('Event 7', S_TH), p('Travel 30', S_TH)]]
    r = [
        [p('Premium retail', S_TD_L),       p('$39', S_TD),              p('$99', S_TD)],
        [p('Coverage duration', S_TD_L),    p('7 days', S_TD),           p('30 days', S_TD)],
        [p('Max benefit', S_TD_L),          p('$1,500', S_TD),           p('$5,000', S_TD)],
        [p('Benefit mode', S_TD_L),         p('Fixed-only', S_TD),       p('Hybrid UCR reimbursement', S_TD)],
        [p('Claim frequency', S_TD_L),      p('3%', S_TD),               p('4%', S_TD)],
        [p('Tier distribution', S_TD_L),    p('60% T1 / 30% T2 / 10% T3', S_TD),
                                             p('50% T1 / 35% T2 / 15% T3', S_TD)],
        [p('E[benefit | claimed]', S_TD_L), p('$540', S_TD),             p('$1,647', S_TD)],
        [p('E[cost per policy]', S_TD_L),
         p('$16.20', style('bold_teal', fontSize=8, fontName='Helvetica-Bold',
                            textColor=TEAL, alignment=TA_CENTER)),
         p('$65.86', style('bold_teal2', fontSize=8, fontName='Helvetica-Bold',
                            textColor=TEAL, alignment=TA_CENTER))],
        [p('Net margin per policy', S_TD_L),
         p('$22.80  (58.5%)', style('marg_g', fontSize=8, fontName='Helvetica-Bold',
                                    textColor=GREEN, alignment=TA_CENTER)),
         p('$33.14  (33.5%)', style('marg_g2', fontSize=8, fontName='Helvetica-Bold',
                                    textColor=GREEN, alignment=TA_CENTER))],
        [p('Loss ratio', S_TD_L),
         p('41.5%', S_TD),
         p('66.2%', S_TD)],
    ]
    t2 = Table(h + r, colWidths=[5.5*cm, 5.0*cm, 5.5*cm])
    t2.setStyle(base_table_style())
    story.append(t2)

    story.append(sp(6))
    story.append(p('<i>Tier benefit averages: Event 7 uses fixed benefits ($300 / $700 / $1,500). '
                   'Travel 30 UCR averages derived from simulation: T1 avg $603, '
                   'T2 avg $1,968, T3 avg $4,375.</i>', S_NOTE))
    return story


# ── SECTION 3: Reserve Formula ─────────────────────────────────────────────
def build_section3():
    story = []
    story.append(sp(12))
    story.append(section_header('3.  Reserve Capacity Formula & Maximum Members'))
    story.append(sp(8))

    story.append(p('Reserve requirements are derived from a <b>compound Poisson aggregate loss '
                   'model</b> at Value-at-Risk 99% (equivalent to Solvency II non-life SCR '
                   'simplified approach).  The two-term formula separates expected losses '
                   '(covered by premium flow) from tail variance (covered by LP reserve):'))
    story.append(sp(6))

    formula_data = [
        ['Event 7:', 'Reserve(N)  =  16.20 × N  +  262.9 × √N'],
        ['Travel 30:', 'Reserve(M)  =  65.86 × M  +  976.9 × √M'],
        ['', 'N, M  =  concurrent active policyholders'],
    ]
    ft = Table(formula_data, colWidths=[2.5*cm, 12.5*cm])
    ft.setStyle(TableStyle([
        ('FONTNAME',  (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME',  (1, 0), (1, -1), 'Courier'),
        ('FONTSIZE',  (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), TEAL),
        ('TEXTCOLOR', (1, 0), (1, 1), DARK),
        ('TEXTCOLOR', (1, 2), (1, 2), SLATE),
        ('FONTNAME',  (1, 2), (1, 2), 'Courier-Oblique'),
        ('BACKGROUND',(0, 0), (-1, 1), LIGHT_GREY),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING',  (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.3, MID_GREY),
    ]))
    story.append(ft)
    story.append(sp(6))

    story.append(p('<b>Standard deviation derivation:</b>  '
                   'Event 7: SD[S] = 113.0 × √N  (E[X<super>2</super>] = $426,000, p = 3%).  '
                   'Travel 30: SD[S] = 420.0 × √M  (E[X<super>2</super>] = $4,408,247, p = 4%).  '
                   'The √N scaling reflects the statistical diversification benefit as the pool grows.'))
    story.append(sp(8))

    story.append(p('<b>Table 3 — Reserve Requirements by Concurrent Member Count</b>', S_SUBSECTION))
    h = [[p('Concurrent Members\n(E7 / T30)', S_TH),
          p('E7 @95%', S_TH), p('E7 @99%', S_TH),
          p('T30 @95%', S_TH), p('T30 @99%', S_TH)]]
    r = [
        ['50 / 25',    '$2,125',  '$2,669',  '$5,102',  '$6,532'],
        ['100 / 50',   '$3,480',  '$4,249',  '$8,178',  '$10,200'],
        ['250 / 100',  '$6,990',  '$8,206',  '$13,495', '$16,355'],
        ['500 / 200',  '$12,258', '$13,978', '$22,941', '$26,986'],
        ['1,000 / 500', '$22,080', '$24,513', '$48,379', '$54,773'],
        ['2,000 / 1,000', '$40,717', '$44,160', '$87,706', '$96,748'],
        ['5,000 / 2,000', '$94,147', '$99,596', '$162,617', '$175,427'],
    ]
    # Format rows as Paragraphs
    def row_p(row, highlight=False):
        st = S_TD
        return [p(row[0], S_TD_L)] + [p(c, st) for c in row[1:]]

    t3 = Table(h + [row_p(r_) for r_ in r],
               colWidths=[3.5*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
    ts3 = base_table_style()
    # Highlight row for 1000/500 — current safe zone boundary
    ts3.add('BACKGROUND', (0, 5), (-1, 5), TEAL_LIGHT)
    ts3.add('FONTNAME',   (0, 5), (-1, 5), 'Helvetica-Bold')
    t3.setStyle(ts3)
    story.append(t3)
    story.append(sp(4))
    story.append(p('<i>Row highlighted (1,000 E7 / 500 T30) marks the approximate current safe operating zone.</i>', S_NOTE))
    story.append(sp(6))

    # Capacity box
    cap_data = [[
        p('Current Maximum Capacity (VaR 99%)', style('cap_h', fontSize=10,
           fontName='Helvetica-Bold', textColor=TEAL, alignment=TA_CENTER)),
    ], [
        p('Event 7: up to  <b>1,444 concurrent members</b>  |  '
          'Travel 30: up to  <b>502 concurrent members</b>',
          style('cap_b', fontSize=9.5, fontName='Helvetica', textColor=DARK, alignment=TA_CENTER)),
    ]]
    cap_t = Table(cap_data, colWidths=[PAGE_W - MARGIN_L - MARGIN_R])
    cap_t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), TEAL_LIGHT),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('BOX',           (0, 0), (-1, -1), 1.5, TEAL),
        ('ROUNDEDCORNERS', [5]),
    ]))
    story.append(cap_t)
    return story


# ── SECTION 4: Stress Scenarios ────────────────────────────────────────────
def build_section4():
    story = []
    story.append(PageBreak())
    story.append(section_header('4.  Stress Scenarios — Protocol Failure Cases'))
    story.append(sp(8))
    story.append(p('The following scenarios identify conditions under which the current reserve '
                   'stack is <b>insufficient</b>.  All assume correlated or structural failures '
                   'that break the independent-claims assumption underpinning the VaR model.'))
    story.append(sp(8))

    scenarios = [
        {
            'label': 'Scenario A — Mass Casualty / Correlated Event  (Event 7)',
            'color': RED,
            'bg': RED_LIGHT,
            'rows': [
                ('Situation', '100 Event 7 policyholders at the same festival. Structural collapse → 40% Tier 3 claims.'),
                ('Claims triggered', '40 × $1,500  =  $60,000'),
                ('Reserve available', '$33,400'),
                ('SHORTFALL', '−$26,600'),
                ('Root cause', 'Model assumes independent claims. A correlated event breaks this assumption entirely.'),
            ],
        },
        {
            'label': 'Scenario B — Pandemic / Regional Epidemic  (Travel 30)',
            'color': RED,
            'bg': RED_LIGHT,
            'rows': [
                ('Situation', '200 Travel 30 holders during a regional epidemic. Claim rate rises to 15%, 80% Tier 3.'),
                ('Claims triggered', '200 × 15% × 80% × $4,375  =  $105,000'),
                ('Reserve available', '$54,900'),
                ('SHORTFALL', '−$50,100'),
                ('Root cause', 'Correlated illness event across geographically dispersed policyholders.'),
            ],
        },
        {
            'label': 'Scenario C — Rapid Growth Without LP Injection  (Event 7)',
            'color': AMBER,
            'bg': AMBER_LIGHT,
            'rows': [
                ('Situation', 'Protocol scales to 3,000 concurrent Event 7 members without additional LP capital.'),
                ('Required @99%', '$62,997'),
                ('Available', '$33,400'),
                ('SHORTFALL', '−$29,597'),
                ('Critical threshold', '1,444 concurrent Event 7 members  (current safe limit).'),
            ],
        },
        {
            'label': 'Scenario D — LP Exit Crisis',
            'color': AMBER,
            'bg': AMBER_LIGHT,
            'rows': [
                ('Situation', 'Junior LP providers redeem $20,000. Event 7 LP reserve lane empties completely.'),
                ('Residual reserve', '$20,900  (sponsor + premiums only)'),
                ('Capacity impact', 'Drops from 1,444  →  835 concurrent members  (−42%)'),
                ('Root cause', 'Thin pool with no redemption lockup creates cliff-edge liquidity risk.'),
            ],
        },
    ]

    for sc in scenarios:
        sc_data = [[p(f'<b>{sc["label"]}</b>',
                      style('sc_h', fontSize=9, fontName='Helvetica-Bold',
                            textColor=sc['color']))]]
        for k, v in sc['rows']:
            is_sf = 'SHORTFALL' in k
            kst = style('sc_k', fontSize=8, fontName='Helvetica-Bold',
                        textColor=RED if is_sf else SLATE)
            vst = style('sc_v', fontSize=8, fontName='Helvetica-Bold' if is_sf else 'Helvetica',
                        textColor=RED if is_sf else DARK)
            sc_data.append([p(k, kst), p(v, vst)])

        sc_t = Table(sc_data,
                     colWidths=[PAGE_W - MARGIN_L - MARGIN_R])
        if len(sc_data[0]) == 1:
            inner = [[p(f'<b>{sc["label"]}</b>',
                        style('sc_h2', fontSize=9, fontName='Helvetica-Bold',
                              textColor=sc['color']))]]
            for k, v in sc['rows']:
                is_sf = 'SHORTFALL' in k
                inner.append([
                    p(k, style('sc_ki', fontSize=8, fontName='Helvetica-Bold',
                                textColor=RED if is_sf else SLATE)),
                    p(v, style('sc_vi', fontSize=8,
                                fontName='Helvetica-Bold' if is_sf else 'Helvetica',
                                textColor=RED if is_sf else DARK)),
                ])
            sc_t2 = Table(inner, colWidths=[3.5*cm, PAGE_W - MARGIN_L - MARGIN_R - 3.5*cm])
            sc_t2.setStyle(TableStyle([
                ('SPAN',          (0, 0), (1, 0)),
                ('BACKGROUND',    (0, 0), (-1, 0), sc['bg']),
                ('BACKGROUND',    (0, 1), (-1, -1), WHITE),
                ('ROWBACKGROUNDS',(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
                ('LEFTPADDING',   (0, 0), (-1, -1), 10),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
                ('TOPPADDING',    (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('BOX',           (0, 0), (-1, -1), 1, sc['color']),
                ('GRID',          (0, 1), (-1, -1), 0.3, MID_GREY),
            ]))
            story.append(KeepTogether([sc_t2, sp(8)]))
        else:
            story.append(KeepTogether([sc_t, sp(8)]))

    return story


# ── SECTION 5: Additional Reserve ─────────────────────────────────────────
def build_section5():
    story = []
    story.append(sp(6))
    story.append(section_header('5.  Additional LP Reserve Needed to Scale'))
    story.append(sp(8))
    story.append(p('The table below shows the total LP capital required at each growth milestone '
                   '(VaR 99%), and how much additional capital must be raised beyond the current '
                   '$57,500 pool.  Note that the first threshold (500 E7 + 200 T30) requires '
                   '<b>no additional capital</b> — the current pool is already sufficient.'))
    story.append(sp(6))

    story.append(p('<b>Table 4 — LP Scaling Requirements</b>', S_SUBSECTION))
    h = [[p('Target\n(E7 + T30 concurrent)', S_TH),
          p('Current LP', S_TH),
          p('Required LP @99%', S_TH),
          p('Additional LP Needed', S_TH)]]
    r = [
        ('500 + 200',     '$57,500', '$40,964',  ('$0  —  sufficient ✓', GREEN)),
        ('1,000 + 500',   '$57,500', '$79,286',  ('+$21,786', AMBER)),
        ('2,000 + 1,000', '$57,500', '$140,908', ('+$83,408', AMBER)),
        ('5,000 + 2,000', '$57,500', '$275,023', ('+$217,523', RED)),
        ('10,000 + 5,000','$57,500', '$586,665', ('+$529,165', RED)),
    ]
    rows = []
    for tgt, cur, req, (extra, col) in r:
        rows.append([
            p(tgt, S_TD_L),
            p(cur, S_TD),
            p(req, S_TD),
            p(extra, style(f'ex_{col}', fontSize=8, fontName='Helvetica-Bold',
                           textColor=col, alignment=TA_CENTER)),
        ])
    t4 = Table(h + rows, colWidths=[4.0*cm, 3.0*cm, 3.5*cm, 4.5*cm])
    t4.setStyle(base_table_style())
    story.append(t4)
    story.append(sp(6))
    story.append(p('<b>Key insight:</b>  LP reserve scales as √N (statistical diversification '
                   'benefit) while premium income scales linearly with N.  This means the '
                   'protocol becomes increasingly capital-efficient at higher member counts — '
                   'each additional dollar of LP supports progressively more policies.'))
    return story


# ── SECTION 6: APY Economics ───────────────────────────────────────────────
def build_section6():
    story = []
    story.append(PageBreak())
    story.append(section_header('6.  LP APY Economics'))
    story.append(sp(8))
    story.append(p('LP providers earn yield from the net premium surplus after expected claims.  '
                   'APY is calculated as annual surplus divided by total LP capital deployed:'))
    story.append(sp(4))

    formula2 = [
        ['APY  =', '( Annual_E7_policies × $22.80  +  Annual_T30_policies × $33.14 )  /  LP_deployed'],
    ]
    ft2 = Table(formula2, colWidths=[2.0*cm, 13.0*cm])
    ft2.setStyle(TableStyle([
        ('FONTNAME',  (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME',  (1, 0), (1, -1), 'Courier'),
        ('FONTSIZE',  (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), TEAL),
        ('BACKGROUND',(0, 0), (-1, -1), LIGHT_GREY),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING',  (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.3, MID_GREY),
    ]))
    story.append(ft2)
    story.append(sp(8))

    story.append(p('<b>Table 5 — APY at Current LP ($57,500)</b>', S_SUBSECTION))
    h5 = [[p('Annual Policy Volume\n(E7 + T30)', S_TH),
           p('Annual Surplus', S_TH),
           p('APY on $57,500', S_TH)]]
    apy_rows = [
        ('100 E7 + 50 T30',     '$3,937',  '6.8%',   SLATE,  'Conservative launch'),
        ('300 E7 + 100 T30',    '$10,154', '17.7%',  SLATE,  ''),
        ('500 E7 + 200 T30',    '$18,028', '31.4%',  GREEN,  ''),
        ('1,000 E7 + 400 T30',  '$36,056', '62.7%',  GREEN,  ''),
        ('2,000 E7 + 800 T30',  '$72,112', '125.4%', AMBER,  '⚠  requires more LP'),
    ]
    rows5 = []
    for vol, sur, apy, col, note in apy_rows:
        label = f'{vol}' + (f'  <i>({note})</i>' if note else '')
        rows5.append([
            p(label, S_TD_L),
            p(sur, S_TD),
            p(apy, style(f'apy_{col}', fontSize=8.5, fontName='Helvetica-Bold',
                         textColor=col, alignment=TA_CENTER)),
        ])
    t5 = Table(h5 + rows5, colWidths=[6.5*cm, 3.5*cm, 5.0*cm])
    t5.setStyle(base_table_style())
    story.append(t5)
    story.append(sp(8))

    story.append(p('<b>Table 6 — APY with LP Scaled Proportionally</b>', S_SUBSECTION))
    h6 = [[p('Scale\n(annual policies)', S_TH),
           p('LP Required', S_TH),
           p('Annual Surplus', S_TH),
           p('Stabilized APY', S_TH)]]
    rows6 = [
        ['2,000 E7 + 1,000 T30', '~$141,000', '$78,740',  '55.8%'],
        ['5,000 E7 + 2,000 T30', '~$275,000', '$180,280', '65.6%'],
        ['10,000 E7 + 5,000 T30','~$587,000', '$393,700', '67.1%'],
    ]
    t6 = Table(h6 + [[p(c, S_TD_L if i == 0 else S_TD) for i, c in enumerate(r)] for r in rows6],
               colWidths=[5.0*cm, 3.0*cm, 3.5*cm, 3.5*cm])
    t6.setStyle(base_table_style())
    story.append(t6)
    story.append(sp(6))
    story.append(p('<b>Convergence note:</b>  APY stabilizes at approximately <b>65–70%</b> at '
                   'large scale, reflecting the underlying product loss ratios (41.5% Event 7 / '
                   '66.2% Travel 30).  Early LP providers earn higher returns (30–60%+) as '
                   'compensation for bootstrapping tail risk on a thin pool.'))
    return story


# ── SECTION 7: Realistic Launch Scenario ───────────────────────────────────
def build_section7():
    story = []
    story.append(sp(10))
    story.append(section_header('7.  Realistic Launch Scenario'))
    story.append(sp(8))

    phases = [
        {
            'phase': 'Phase 1 — Bootstrap  (Q1–Q2 2026)',
            'color': GREEN,
            'bg': GREEN_LIGHT,
            'items': [
                ('Volume', '30–80 Event 7/month  |  10–25 Travel 30/month'),
                ('Concurrent members', '~50 E7  +  ~20 T30'),
                ('Solvency status', 'FULLY COVERED ✓  —  well within $33,400 / $54,900 reserves'),
                ('LP APY', '12–22%'),
                ('Primary risk', 'Correlated mass casualty at high-density single venue'),
                ('Action required', 'NONE  —  current pool is sufficient'),
            ],
        },
        {
            'phase': 'Phase 2 — Growth  (Q3–Q4 2026)',
            'color': TEAL,
            'bg': TEAL_LIGHT,
            'items': [
                ('Volume', '150–300 Event 7/month  |  40–80 Travel 30/month'),
                ('Concurrent members', '~200 E7  +  ~60 T30'),
                ('Solvency status', 'COVERED ✓'),
                ('LP APY', '35–55%'),
                ('Action required', 'Raise +$20,000–$30,000 LP to maintain safety margin'),
            ],
        },
        {
            'phase': 'Phase 3 — Scale  (2027)',
            'color': AMBER,
            'bg': AMBER_LIGHT,
            'items': [
                ('Volume', '500+ Event 7/month  |  100+ Travel 30/month'),
                ('Concurrent members', '~700 E7  +  ~100 T30  (approaching E7 solvency limit)'),
                ('Solvency status', 'APPROACHING THRESHOLD  ⚠'),
                ('LP APY', '55–65%'),
                ('Action required', 'Raise +$50,000–$80,000 LP  (target pool ~$110,000–$130,000)'),
            ],
        },
    ]

    for ph in phases:
        ph_data = [
            [p(f'<b>{ph["phase"]}</b>',
               style('ph_h', fontSize=9.5, fontName='Helvetica-Bold', textColor=ph['color']))]
        ]
        for k, v in ph['items']:
            ph_data.append([
                p(k, style('ph_k', fontSize=8, fontName='Helvetica-Bold', textColor=SLATE)),
                p(v, style('ph_v', fontSize=8, fontName='Helvetica', textColor=DARK)),
            ])
        inner = [[p(f'<b>{ph["phase"]}</b>',
                    style('ph_h2', fontSize=9.5, fontName='Helvetica-Bold',
                          textColor=ph['color']))]]
        for k, v in ph['items']:
            inner.append([
                p(k, style('ph_ki', fontSize=8, fontName='Helvetica-Bold', textColor=SLATE)),
                p(v, style('ph_vi', fontSize=8, fontName='Helvetica', textColor=DARK)),
            ])
        inner_t = Table(inner, colWidths=[3.8*cm, PAGE_W - MARGIN_L - MARGIN_R - 3.8*cm])
        inner_t.setStyle(TableStyle([
            ('SPAN',          (0, 0), (1, 0)),
            ('BACKGROUND',    (0, 0), (-1, 0), ph['bg']),
            ('ROWBACKGROUNDS',(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
            ('LEFTPADDING',   (0, 0), (-1, -1), 10),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
            ('TOPPADDING',    (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BOX',           (0, 0), (-1, -1), 1, ph['color']),
            ('GRID',          (0, 1), (-1, -1), 0.3, MID_GREY),
        ]))
        story.append(KeepTogether([inner_t, sp(8)]))

    story.append(sp(4))
    story.append(p('<b>Table 7 — Operational Thresholds Summary</b>', S_SUBSECTION))
    h7 = [[p('Scenario', S_TH), p('Current Pool\nSufficient?', S_TH), p('LP Action', S_TH)]]
    thresh_rows = [
        ('Up to 1,400 E7 + 500 T30 concurrent',
         ('YES ✓', GREEN), 'None required'),
        ('1,500–3,000 E7  or  500–1,000 T30',
         ('PARTIAL ⚠', AMBER), '+$50,000–$100,000 LP'),
        ('Over 3,000 E7  or  1,000 T30',
         ('NO ✗', RED), 'Mandatory LP scaling'),
        ('Correlated event  >30% Tier 3 same venue',
         ('NO ✗', RED), 'Reinsurance  or  per-event policyholder cap'),
    ]
    trows7 = []
    for sc, (suf, col), action in thresh_rows:
        trows7.append([
            p(sc, S_TD_L),
            p(suf, style(f'suf_{col}', fontSize=8, fontName='Helvetica-Bold',
                         textColor=col, alignment=TA_CENTER)),
            p(action, S_TD_L),
        ])
    t7 = Table(h7 + trows7, colWidths=[6.0*cm, 3.0*cm, 6.0*cm])
    t7.setStyle(base_table_style())
    story.append(t7)

    story.append(sp(10))
    # Recommendation box
    rec_data = [[
        p('Operational Recommendation',
          style('rec_h', fontSize=10, fontName='Helvetica-Bold', textColor=TEAL, alignment=TA_CENTER)),
    ], [
        p('The primary risk is not aggregate volume — the current $57,500 pool handles up to '
          '~1,444 Event 7 + ~502 Travel 30 concurrent members comfortably.  The critical '
          'vulnerability is <b>geographic concentration at a single event</b>.  '
          '<br/><br/>'
          'Recommended Phase 0 operational control:  implement a hard cap of <b>50 Event 7 '
          'policyholders per single named venue / event</b>.  This limits maximum correlated '
          'Tier 3 exposure to 50 × $1,500 = $75,000 — addressable with a moderate sponsor '
          'backstop top-up if triggered.',
          style('rec_b', fontSize=9, fontName='Helvetica', textColor=DARK,
                alignment=TA_JUSTIFY, leading=14)),
    ]]
    rec_t = Table(rec_data, colWidths=[PAGE_W - MARGIN_L - MARGIN_R])
    rec_t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), TEAL_LIGHT),
        ('BACKGROUND',    (0, 1), (-1, 1), WHITE),
        ('BOX',           (0, 0), (-1, -1), 1.5, TEAL),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 14),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 14),
    ]))
    story.append(rec_t)
    return story


# ── BUILD ───────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T + 0.6*cm,
        bottomMargin=MARGIN_B + 0.6*cm,
        title='Genesis Protect Acute v1 — Actuarial Reserve Analysis',
        author='OmegaX Health Capital Markets',
        subject='Capacity, Stress Scenarios & LP Economics',
    )

    story = []
    story += build_cover()
    story += build_section1()
    story += build_section2()
    story += build_section3()
    story += build_section4()
    story += build_section5()
    story += build_section6()
    story += build_section7()

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF created: {OUTPUT}")


if __name__ == '__main__':
    build()
