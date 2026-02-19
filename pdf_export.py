from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from database import connect_db


def generate_pdf_report(user_id):

    file_path = "Habit_Tracker_Printable.pdf"
    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    # ---------------- TITLE ---------------- #

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=36,
        spaceAfter=20
    )

    elements.append(Paragraph("HABIT TRACKER", title_style))
    elements.append(Spacer(1, 20))

    # ---------------- FETCH HABITS ---------------- #

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_name
        FROM habits
        WHERE user_id=?
    """, (user_id,))

    habits = cursor.fetchall()
    conn.close()

    habit_names = [h[0] for h in habits]

    # If no habits exist, add blank rows
    if not habit_names:
        habit_names = [""] * 15

    # Limit printable rows (can increase if needed)
    max_rows = max(len(habit_names), 15)

    # ---------------- CREATE GRID ---------------- #

    # Header row: Day numbers
    header_row = ["HABIT"] + [str(i) for i in range(1, 32)]

    table_data = [header_row]

    for i in range(max_rows):
        if i < len(habit_names):
            row = [habit_names[i]] + [""] * 31
        else:
            row = [""] + [""] * 31
        table_data.append(row)

    # Column widths
    col_widths = [2.5 * inch] + [0.4 * inch] * 31

    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([

        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),

        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (0, -1), 9),

    ]))

    elements.append(table)

    # ---------------- FOOTER QUOTE ---------------- #

    elements.append(Spacer(1, 20))

    footer_style = ParagraphStyle(
        name="FooterStyle",
        fontSize=10,
        textColor=colors.grey
    )

    elements.append(Paragraph(
        "“Good habits are worth being fanatical about.” – John Irving",
        footer_style
    ))

    doc.build(elements)

    return file_path
