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
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    # ---------------- TITLE ---------------- #

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=30,
        spaceAfter=20
    )

    elements.append(Paragraph("HABIT TRACKER REPORT", title_style))
    elements.append(Spacer(1, 20))

    # ---------------- GET DATA ---------------- #

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch habits
    cursor.execute("""
        SELECT id, habit_name
        FROM habits
        WHERE user_id=?
    """, (user_id,))
    habits = cursor.fetchall()

    # Fetch logs
    cursor.execute("""
        SELECT habit_id, date
        FROM habit_logs
    """)
    logs = cursor.fetchall()

    conn.close()

    # Convert logs to dictionary
    log_dict = {}

    for habit_id, date in logs:
        if habit_id not in log_dict:
            log_dict[habit_id] = []
        log_dict[habit_id].append(date)

    # ---------------- CREATE GRID ---------------- #

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
        table_data.append(["No habits found"] + [""] * 31)

    # Column widths
    col_widths = [2.5 * inch] + [0.4 * inch] * 31

    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),

        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (0, -1), 9),

    ]))

    elements.append(table)

    doc.build(elements)

    return file_path
