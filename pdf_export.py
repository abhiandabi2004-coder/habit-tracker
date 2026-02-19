from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from datetime import datetime
from database import connect_db


def generate_pdf_report(user_id):

    file_path = "Habit_Tracker_Report.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    elements = []

    # ---------------- TITLE ---------------- #

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=28,
        spaceAfter=15
    )

    elements.append(Paragraph("HABIT TRACKER REPORT", title_style))
    elements.append(Spacer(1, 15))

    # ---------------- FETCH DATA ---------------- #

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, habit_name
        FROM habits
        WHERE user_id=?
    """, (user_id,))
    habits = cursor.fetchall()

    cursor.execute("""
        SELECT habit_id, date
        FROM habit_logs
    """)
    logs = cursor.fetchall()

    conn.close()

    # Convert logs to dictionary
    log_dict = {}
    for habit_id, date in logs:
        log_dict.setdefault(habit_id, []).append(date)

    # ---------------- CREATE TABLE ---------------- #

    header_row = ["HABIT"] + [str(i) for i in range(1, 32)]
    table_data = [header_row]

    current_month = datetime.now().strftime("%Y-%m")

    for habit_id, habit_name in habits:

        row = [habit_name]

        for day in range(1, 32):
            date_str = f"{current_month}-{str(day).zfill(2)}"

            if habit_id in log_dict and date_str in log_dict[habit_id]:
                row.append("✔")
            else:
                row.append("")

        table_data.append(row)

    if not habits:
        table_data.append(["No habits added"] + [""] * 31)

    # ----------- BETTER COLUMN WIDTHS ----------- #

    page_width, page_height = landscape(A4)

    habit_column_width = 2.2 * inch
    remaining_width = page_width - habit_column_width - 40
    day_column_width = remaining_width / 31

    col_widths = [habit_column_width] + [day_column_width] * 31

    table = Table(table_data, colWidths=col_widths, repeatRows=1)

    table.setStyle(TableStyle([

        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),

        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('LEFTPADDING', (0, 0), (0, -1), 6),
        ('RIGHTPADDING', (0, 0), (0, -1), 6),

        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (0, 0), (-1, 0), 9),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),

    ]))

    elements.append(table)

    doc.build(elements)

    return file_path
