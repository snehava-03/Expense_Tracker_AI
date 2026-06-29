# pdf_generator.py
# Generates monthly report PDF using ReportLab

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from datetime import datetime


def generate_monthly_report(summary, ai_analysis, month_year):
    """
    Generates a PDF monthly report.
    Returns PDF as bytes — sent directly to browser as download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=inch*0.75, leftMargin=inch*0.75,
                            topMargin=inch*0.75, bottomMargin=inch*0.75)

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=22, textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=6
    )
    story.append(Paragraph("FinSight AI — Monthly Report", title_style))
    story.append(Paragraph(f"Period: {month_year}", styles["Normal"]))
    story.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # Financial Summary Table
    heading_style = ParagraphStyle(
        "Heading", parent=styles["Heading2"],
        textColor=colors.HexColor("#1e3a8a"), spaceAfter=8
    )
    story.append(Paragraph("Financial Summary", heading_style))

    table_data = [
        ["Item", "Amount"],
        ["Total Income",   f"Rs. {summary.get('income', 0):,.2f}"],
        ["Total Expenses", f"Rs. {summary.get('expenses', 0):,.2f}"],
        ["Net Savings",    f"Rs. {summary.get('savings', 0):,.2f}"],
        ["Savings Rate",   f"{summary.get('savings_rate', 0):.1f}%"],
    ]

    table = Table(table_data, colWidths=[3*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 11),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.HexColor("#f9fafb"), colors.white]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
        ("PADDING",      (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

    # Category Breakdown
    story.append(Paragraph("Spending by Category", heading_style))
    cat_data = [["Category", "Amount", "% of Expenses"]]
    total_exp = summary.get("expenses", 1)
    for cat, amt in summary.get("categories", {}).items():
        pct = (amt / total_exp * 100) if total_exp > 0 else 0
        cat_data.append([cat, f"Rs. {amt:,.2f}", f"{pct:.1f}%"])

    cat_table = Table(cat_data, colWidths=[2.5*inch, 2*inch, 2*inch])
    cat_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.HexColor("#f9fafb"), colors.white]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
        ("PADDING",       (0, 0), (-1, -1), 8),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 20))

    # AI Analysis
    story.append(Paragraph("AI Financial Advisor Insights", heading_style))
    # Clean up markdown symbols from Gemini response
    clean_analysis = ai_analysis.replace("**", "").replace("*", "•")
    for line in clean_analysis.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), styles["Normal"]))
            story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer