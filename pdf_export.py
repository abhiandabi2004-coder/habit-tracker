from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table
from database import connect_db
import pandas as pd

def generate_pdf_report(user_id):
    file_path = "habit_report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Habit Tracker Report", styles['Title']))
    elements.append(Spacer(1, 20))

    conn = connect_db()
    df = pd.read_sql("""
    SELECT habits.habit_name, habit_logs.date
    FROM habit_logs
    JOIN habits ON habits.id = habit_logs.habit_id
    WHERE habits.user_id=?
    """, conn, params=(user_id,))

    if not df.empty:
        data = [df.columns.tolist()] + df.values.tolist()
        table = Table(data)
        elements.append(table)

    doc.build(elements)
    return file_path