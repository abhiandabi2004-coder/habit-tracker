from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from database import connect_db
import pandas as pd


def generate_pdf_report(user_id):

    file_path = "Habit_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    title_style = ParagraphStyle(name="Title", fontSize=20)
    elements.append(Paragraph("Habit Summary Report", title_style))
    elements.append(Spacer(1, 20))

    conn = connect_db()

    df = pd.read_sql(
        """
        SELECT habits.habit_name, habit_logs.date, habit_logs.value
        FROM habit_logs
        JOIN habits ON habits.id = habit_logs.habit_id
        WHERE habits.user_id=?
        """,
        conn,
        params=(user_id,),
    )

    conn.close()

    if df.empty:
        elements.append(Paragraph("No data available.", title_style))
    else:
        summary = df.groupby("habit_name")["value"].sum().reset_index()

        for _, row in summary.iterrows():
            elements.append(
                Paragraph(
                    f"{row['habit_name']} - Total Logged Value: {row['value']}",
                    title_style,
                )
            )
            elements.append(Spacer(1, 10))

    doc.build(elements)
    return file_path
