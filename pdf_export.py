from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from datetime import datetime
from database import connect_db


def generate_pdf_report(user_id):

    file_path = "Habit_Monthly_Tracker.pdf"

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
        name="Title",
        fontSize=24,
        spaceAfter=15
    )

    elements.append(Paragraph("MONTHLY HABIT TRACKER", title_style))
    elements.append(Spacer(1, 20))

    # ---------------- MONTH TABLE ---------------- #

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    current_month_index = datetime.now().month - 1

    month_row = []

    for i, month in enumerate(months):
        if i < current_month_index:
            month_row.append(f"<strike>{month}</strike>")
        else:
            month_row.append(month)

    month_table = Table([month_row], colWidths=[1 * inch] * 12)

    month_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(month_table)
    elements.append(Spacer(1, 30))

    # ---------------- FETCH HABITS ---------------- #

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

    # ---------------- CREATE 32-COLUMN TABLE ---------------- #

    header_row = ["Habit Name"] + [str(i) for i in range(1, 32)]
    table_data = [header_row]

    current_month_str = datetime.now().strftime("%Y-%m")

    for habit_id, habit_name in habits:

        row = [habit_name]

        for day in range(1, 32):
            date_str = f"{current_month_str}-{str(day).zfill(2)}"

            if habit_id in log_dict and date_str in log_dict[habit_id]:
                row.append("✔")
            else:
                row.append("")

        table_data.append(row)

    if not habits:
        table_data.append(["No habits added"] + [""] * 31)

    page_width, _ = landscape(A4)

    habit_col_width = 2.5 * inch
    remaining_width = page_width - habit_col_width - 40
    day_col_width = remaining_width / 31

    col_widths = [habit_col_width] + [day_col_width] * 31

    tracker_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    tracker_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    elements.append(tracker_table)

    doc.build(elements)

    return file_path
