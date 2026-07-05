"""
PDF Report Generator — Produces a professional PDF market research report.

Uses fpdf2 to build a styled PDF with cover page, SWOT table,
competitor matrix, and all analysis sections.
"""

import os
from datetime import datetime

from fpdf import FPDF

from agents.analyst import AnalysisResult

# ---------------------------------------------------------------------------
# Color palette (matches DOCX theme)
# ---------------------------------------------------------------------------
COLOR_DARK_BLUE = (26, 55, 108)
COLOR_MED_BLUE = (46, 109, 180)
COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_BG = (240, 245, 255)
COLOR_GREEN_BG = (240, 255, 244)
COLOR_RED_BG = (255, 245, 245)
COLOR_AMBER_BG = (255, 251, 240)
COLOR_TEAL_BG = (240, 255, 255)
COLOR_GREEN = (29, 122, 74)
COLOR_RED = (155, 28, 28)
COLOR_AMBER = (146, 96, 13)
COLOR_TEAL = (13, 102, 107)
COLOR_GRAY = (156, 163, 175)
COLOR_BLACK = (30, 30, 30)


BULLET = "-"

_UNICODE_REPLACEMENTS = {
    "\u2013": "-",  # en dash
    "\u2014": "--",  # em dash
    "\u2018": "'",  # left single quote
    "\u2019": "'",  # right single quote
    "\u201c": '"',  # left double quote
    "\u201d": '"',  # right double quote
    "\u2022": "-",  # bullet
    "\u20ac": "EUR",  # euro sign
    "\u00fc": "ue",  # ü
    "\u00e4": "ae",  # ä
    "\u00f6": "oe",  # ö
    "\u00dc": "Ue",  # Ü
    "\u00c4": "Ae",  # Ä
    "\u00d6": "Oe",  # Ö
    "\u00df": "ss",  # ß
}


def _sanitize(text: str) -> str:
    """Replace Unicode characters that are outside latin-1 range."""
    for char, replacement in _UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _ReportPDF(FPDF):
    """Custom FPDF subclass with header/footer styling."""

    def __init__(self, company: str):
        super().__init__()
        self.company = company

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*COLOR_GRAY)
        self.cell(
            0, 10, f"Market Research Report  |  {self.company}  |  Page {self.page_no()}", align="C"
        )


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------


def _add_cover_page(pdf: _ReportPDF, company: str):
    pdf.add_page()
    pdf.ln(60)

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*COLOR_DARK_BLUE)
    pdf.cell(0, 14, "MARKET RESEARCH REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*COLOR_MED_BLUE)
    pdf.cell(0, 12, company, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*COLOR_GRAY)
    pdf.cell(
        0,
        8,
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )


def _add_heading(pdf: _ReportPDF, text: str):
    pdf.ln(6)
    # Keep the heading attached to at least a few lines of its content
    if pdf.will_page_break(30):
        pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*COLOR_DARK_BLUE)
    pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")

    # Divider line
    pdf.set_draw_color(*COLOR_MED_BLUE)
    pdf.set_line_width(0.3)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)


def _add_body_text(pdf: _ReportPDF, text: str):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*COLOR_BLACK)
    pdf.multi_cell(0, 5.5, _sanitize(text))
    pdf.ln(3)


def _add_bullet_list(pdf: _ReportPDF, items: list[str]):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*COLOR_BLACK)
    for item in items:
        text = _sanitize(item)
        # Keep each bullet on one page
        lines = pdf.multi_cell(pdf.epw - 8, 5.5, text, dry_run=True, output="LINES")
        if pdf.will_page_break(len(lines) * 5.5):
            pdf.add_page()
        x = pdf.get_x()
        pdf.cell(8, 5.5, BULLET)
        pdf.multi_cell(0, 5.5, text)
        pdf.set_x(x)
    pdf.ln(3)


def _add_swot_table(pdf: _ReportPDF, swot):
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2
    row_pairs = [
        (
            "STRENGTHS",
            swot.strengths,
            COLOR_GREEN,
            COLOR_GREEN_BG,
            "WEAKNESSES",
            swot.weaknesses,
            COLOR_AMBER,
            COLOR_AMBER_BG,
        ),
        (
            "OPPORTUNITIES",
            swot.opportunities,
            COLOR_TEAL,
            COLOR_TEAL_BG,
            "THREATS",
            swot.threats,
            COLOR_RED,
            COLOR_RED_BG,
        ),
    ]

    for (
        left_label,
        left_items,
        left_color,
        left_bg,
        right_label,
        right_items,
        right_color,
        right_bg,
    ) in row_pairs:
        left_text = "\n".join(f"  {BULLET} {_sanitize(item)}" for item in left_items)
        right_text = "\n".join(f"  {BULLET} {_sanitize(item)}" for item in right_items)

        # Keep header and content of each row pair on the same page:
        # measure the row height up front and break early if needed
        pdf.set_font("Helvetica", "", 9)
        left_lines = pdf.multi_cell(col_w, 5, left_text, dry_run=True, output="LINES")
        right_lines = pdf.multi_cell(col_w, 5, right_text, dry_run=True, output="LINES")
        row_height = 8 + max(len(left_lines), len(right_lines)) * 5
        if pdf.will_page_break(row_height):
            pdf.add_page()

        # Headers
        pdf.set_font("Helvetica", "B", 10)
        for label, color in [(left_label, left_color), (right_label, right_color)]:
            pdf.set_fill_color(*color)
            pdf.set_text_color(*COLOR_WHITE)
            pdf.cell(col_w, 8, label, border=1, fill=True, align="C")
        pdf.ln()

        # Content
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*COLOR_BLACK)

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        pdf.set_fill_color(*left_bg)
        pdf.multi_cell(col_w, 5, left_text, border="LBR", fill=True)
        left_height = pdf.get_y() - y_start

        pdf.set_xy(x_start + col_w, y_start)
        pdf.set_fill_color(*right_bg)
        pdf.multi_cell(col_w, 5, right_text, border="BR", fill=True)
        right_height = pdf.get_y() - y_start

        pdf.set_y(y_start + max(left_height, right_height))
        pdf.ln(3)


def _add_porters_table(pdf: _ReportPDF, forces):
    """Render Porter's Five Forces as a rating-coloured table."""
    rows = [
        ("Competitive Rivalry", forces.competitive_rivalry),
        ("Threat of New Entrants", forces.threat_of_new_entrants),
        ("Threat of Substitutes", forces.threat_of_substitutes),
        ("Bargaining Power of Suppliers", forces.bargaining_power_of_suppliers),
        ("Bargaining Power of Buyers", forces.bargaining_power_of_buyers),
    ]
    rating_bg = {
        "Low": COLOR_GREEN_BG,
        "Medium": COLOR_AMBER_BG,
        "High": COLOR_RED_BG,
    }
    widths = [55, 18, 105]  # mm — force / rating / rationale
    available = pdf.w - pdf.l_margin - pdf.r_margin
    scale = available / sum(widths)
    widths = [w * scale for w in widths]

    # Header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*COLOR_DARK_BLUE)
    pdf.set_text_color(*COLOR_WHITE)
    for label, w in zip(["Force", "Rating", "Rationale"], widths, strict=False):
        pdf.cell(w, 7, label, border=1, fill=True, align="C")
    pdf.ln()

    # Rows — multi-line rationale
    pdf.set_text_color(*COLOR_BLACK)
    for label, force in rows:
        x_start = pdf.l_margin
        y_start = pdf.get_y()

        # Compute height needed for the rationale at width widths[2]
        pdf.set_font("Helvetica", "", 8.5)
        rationale = _sanitize(force.rationale)
        line_count = max(
            1,
            len(
                pdf.multi_cell(
                    widths[2],
                    4.5,
                    rationale,
                    border=0,
                    align="L",
                    dry_run=True,
                    output="LINES",
                )
            ),
        )
        row_height = max(8, line_count * 4.5 + 1.5)

        # Force name cell
        pdf.set_xy(x_start, y_start)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(*COLOR_WHITE)
        pdf.cell(widths[0], row_height, _sanitize(label), border=1, fill=True)

        # Rating cell — coloured background
        pdf.set_xy(x_start + widths[0], y_start)
        pdf.set_fill_color(*rating_bg.get(force.rating, COLOR_WHITE))
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(widths[1], row_height, force.rating, border=1, fill=True, align="C")

        # Rationale cell
        pdf.set_xy(x_start + widths[0] + widths[1], y_start)
        pdf.set_fill_color(*COLOR_WHITE)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(
            widths[2], row_height / line_count, rationale, border=1, align="L", fill=True
        )

        # Advance Y for the next row
        pdf.set_xy(x_start, y_start + row_height)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(0, 5, "Industry attractiveness:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(0, 4.5, _sanitize(forces.summary))
    pdf.ln(3)


def _add_competitor_table(pdf: _ReportPDF, competitors):
    headers = ["Company", "Overview", "Key Strength", "Key Weakness"]
    widths = [30, 62, 45, 45]
    total_w = sum(widths)
    scale = (pdf.w - pdf.l_margin - pdf.r_margin) / total_w
    widths = [w * scale for w in widths]

    # Header row
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*COLOR_DARK_BLUE)
    pdf.set_text_color(*COLOR_WHITE)
    for i, header in enumerate(headers):
        pdf.cell(widths[i], 8, header, border=1, fill=True, align="C")
    pdf.ln()

    # Data rows
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*COLOR_BLACK)
    for idx, comp in enumerate(competitors):
        bg = COLOR_LIGHT_BG if idx % 2 == 0 else COLOR_WHITE
        pdf.set_fill_color(*bg)
        data = [comp.name, comp.overview, comp.key_strength, comp.key_weakness]
        row_height = 7
        for i, value in enumerate(data):
            pdf.cell(widths[i], row_height, _sanitize(value)[:50], border=1, fill=True)
        pdf.ln()

    pdf.ln(3)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_pdf_report(
    company: str,
    analysis: AnalysisResult,
    output_dir: str = "output",
) -> str:
    """
    Generate a professional PDF market research report.

    Args:
        company:    Company name used as title
        analysis:   Structured AnalysisResult from the AnalysisAgent
        output_dir: Directory where the file will be saved

    Returns:
        Absolute path to the generated .pdf file
    """
    os.makedirs(output_dir, exist_ok=True)

    pdf = _ReportPDF(company)
    pdf.set_auto_page_break(auto=True, margin=20)

    # Cover page
    _add_cover_page(pdf, company)

    # Content pages
    pdf.add_page()

    _add_heading(pdf, "Executive Summary")
    _add_body_text(pdf, analysis.executive_summary)

    _add_heading(pdf, "Company Overview")
    _add_body_text(pdf, analysis.company_overview)

    _add_heading(pdf, "Market Position")
    _add_body_text(pdf, analysis.market_position)

    _add_heading(pdf, "SWOT Analysis")
    _add_swot_table(pdf, analysis.swot)

    _add_heading(pdf, "Porter's Five Forces")
    _add_porters_table(pdf, analysis.porters_five_forces)

    _add_heading(pdf, "Competitive Landscape")
    _add_competitor_table(pdf, analysis.top_competitors)

    _add_heading(pdf, "Key Industry Trends")
    _add_bullet_list(pdf, analysis.key_trends)

    _add_heading(pdf, "Strategic Outlook")
    _add_body_text(pdf, analysis.investment_thesis)

    _add_heading(pdf, "Risk Factors")
    _add_bullet_list(pdf, analysis.risk_factors)

    # Save
    safe_name = company.lower().replace(" ", "_").replace("/", "-")
    filename = f"market_research_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)

    return os.path.abspath(filepath)
