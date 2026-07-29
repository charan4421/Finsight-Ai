"""
FinSight AI — PDF Report Generator
Generates professional financial reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from backend.core.database import db

# ── COLORS ────────────────────────────────────────────────────────────────────
PURPLE = colors.HexColor("#7C3AED")
DARK   = colors.HexColor("#1A1A2E")
MID    = colors.HexColor("#6B7280")
WHITE  = colors.white
RED    = colors.HexColor("#EF4444")
GREEN  = colors.HexColor("#10B981")

# ── STYLES ────────────────────────────────────────────────────────────────────
title_s  = ParagraphStyle("title",  fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, leading=26, alignment=TA_CENTER)
sub_s    = ParagraphStyle("sub",    fontName="Helvetica",      fontSize=11, textColor=WHITE, leading=14, alignment=TA_CENTER)
sec_s    = ParagraphStyle("sec",    fontName="Helvetica-Bold", fontSize=13, textColor=PURPLE, leading=16, spaceBefore=16, spaceAfter=6)
body_s   = ParagraphStyle("body",   fontName="Helvetica",      fontSize=10, textColor=DARK,  leading=14, alignment=TA_JUSTIFY)
right_s  = ParagraphStyle("right",  fontName="Helvetica",      fontSize=9,  textColor=MID,   leading=12, alignment=TA_RIGHT)
footer_s = ParagraphStyle("footer", fontName="Helvetica",      fontSize=8,  textColor=MID,   leading=10, alignment=TA_CENTER)

def sp(n=8): return Spacer(1, n)

def section(title):
    return [
        HRFlowable(width="100%", thickness=1.5, color=PURPLE, spaceAfter=4),
        Paragraph(title, sec_s),
    ]

def money(value):
    try:
        return f"{float(value):,.0f} PLN"
    except:
        return "N/A"

def pct(value):
    try:
        return f"{float(value):.1f}%"
    except:
        return "N/A"


def generate_report(output_path: str = "finsight_report.pdf"):
    """Generate full financial report PDF"""

    if not db.is_loaded:
        db.load()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    story = []

    # ── HEADER ────────────────────────────────────────────────────────────────
    header_table = Table([[
        Paragraph("FinSight AI", title_s),
    ]], colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PURPLE),
        ("TOPPADDING", (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ]))
    story.append(header_table)
    story.append(sp(4))

    sub_table = Table([[
        Paragraph("Financial Intelligence Report — FinCorp Ltd", sub_s),
    ]], colWidths=[17*cm])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#6D28D9")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ]))
    story.append(sub_table)
    story.append(sp(4))

    now = datetime.now().strftime("%d %B %Y, %H:%M")
    story.append(Paragraph(f"Generated: {now}   |   Period: 2020-2024   |   Entities: 4", right_s))
    story.append(sp(12))

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    story += section("1. Executive Summary")

    rev = db.revenue_by_year()
    total_rev = rev["amount_pln"].sum()
    latest_rev = rev[rev["year"] == 2024]["amount_pln"].values
    latest_rev = latest_rev[0] if len(latest_rev) > 0 else 0
    anomalies = db.anomalies()
    overdue = db.overdue_invoices()
    overruns = db.budget_overruns()

    story.append(Paragraph(
        f"This report provides a comprehensive financial analysis of FinCorp Ltd and its 4 international "
        f"subsidiaries for the period 2020-2024. Total group revenue over the 5-year period reached "
        f"<b>{money(total_rev)}</b>, with 2024 revenue of <b>{money(latest_rev)}</b>. "
        f"The AI system detected <b>{len(anomalies)} anomalous transactions</b> requiring review, "
        f"<b>{len(overdue):,} overdue invoices</b> with a combined value of "
        f"<b>{money(overdue['amount_pln'].sum())}</b>, and "
        f"<b>{len(overruns)} months</b> of budget overruns across all entities.",
        body_s))
    story.append(sp(8))

    # ── KPI TABLE ─────────────────────────────────────────────────────────────
    story += section("2. Key Performance Indicators")

    kpi_data = [
        ["Metric", "Value", "Status"],
        ["Total Revenue 2024", money(latest_rev), "Stable"],
        ["Total Revenue 5Y", money(total_rev), "Growth"],
        ["Anomalies Detected", str(len(anomalies)), "Review needed"],
        ["Overdue Invoices", f"{len(overdue):,}", "Action needed"],
        ["Overdue Amount", money(overdue['amount_pln'].sum()), "High risk"],
        ["Budget Overrun Months", str(len(overruns)), "Monitor"],
    ]

    kpi_table = Table(kpi_data, colWidths=[7*cm, 5*cm, 5*cm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PURPLE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#F8F7FF"), WHITE]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(kpi_table)
    story.append(sp(12))

    # ── REVENUE ANALYSIS ──────────────────────────────────────────────────────
    story += section("3. Revenue Analysis by Year")

    rev_data = [["Year", "Revenue (PLN)", "vs Previous Year", "Notes"]]
    prev = None
    for _, row in rev[rev["year"] <= 2024].iterrows():
        yr = int(row["year"])
        amount = row["amount_pln"]
        if prev:
            change = ((amount - prev) / prev * 100)
            change_str = f"+{change:.1f}%" if change > 0 else f"{change:.1f}%"
        else:
            change_str = "-"
        notes = {
            2020: "COVID-19 impact",
            2021: "Recovery phase",
            2022: "Peak growth",
            2023: "Normalisation",
            2024: "Stable growth"
        }.get(yr, "")
        rev_data.append([str(yr), money(amount), change_str, notes])
        prev = amount

    rev_table = Table(rev_data, colWidths=[3*cm, 5*cm, 4*cm, 5*cm])
    rev_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PURPLE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("ALIGN", (1,0), (2,-1), "RIGHT"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#F8F7FF"), WHITE]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(rev_table)
    story.append(sp(12))

    # ── ENTITY COMPARISON ─────────────────────────────────────────────────────
    story += section("4. Entity Performance Comparison")

    entity_data = db.entity_comparison()
    ent_table_data = [["Entity", "Revenue (PLN)", "EBITDA (PLN)", "Net Income (PLN)", "Net Margin"]]
    for _, row in entity_data.iterrows():
        net_margin = (row["net_income_pln"] / row["revenue_pln"] * 100) if row["revenue_pln"] > 0 else 0
        ent_table_data.append([
            row["entity_id"],
            money(row["revenue_pln"]),
            money(row["ebitda_pln"]),
            money(row["net_income_pln"]),
            pct(net_margin),
        ])

    ent_table = Table(ent_table_data, colWidths=[3.5*cm, 4*cm, 3.5*cm, 3.5*cm, 2.5*cm])
    ent_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PURPLE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("ALIGN", (1,0), (-1,-1), "RIGHT"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#F8F7FF"), WHITE]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(ent_table)
    story.append(sp(12))

    # ── ANOMALIES ─────────────────────────────────────────────────────────────
    story += section("5. Anomaly Detection Report")

    story.append(Paragraph(
        f"The AI anomaly detection system identified <b>{len(anomalies)} suspicious transactions</b> "
        f"with a combined value of <b>{money(anomalies['amount_pln'].sum())}</b>. "
        f"These require immediate review by the finance and compliance teams.",
        body_s))
    story.append(sp(8))

    anom_data = [["Transaction ID", "Date", "Amount (PLN)", "Type", "Entity"]]
    for _, row in anomalies.head(10).iterrows():
        anom_data.append([
            str(row["txn_id"]),
            str(row["date"])[:10],
            money(row["amount_pln"]),
            str(row["anomaly_type"]),
            str(row["entity_id"]),
        ])

    anom_table = Table(anom_data, colWidths=[3.5*cm, 2.5*cm, 3.5*cm, 4.5*cm, 3*cm])
    anom_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), RED),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 9),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,1), (-1,-1), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#FEF2F2"), WHITE]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(anom_table)
    story.append(sp(12))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=PURPLE, spaceAfter=8))
    story.append(Paragraph(
        f"FinSight AI — Confidential Financial Report   |   Generated {now}   |   FinCorp Ltd · Warsaw, Poland",
        footer_s))

    doc.build(story)
    return output_path