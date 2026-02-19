import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from database import connect_db
import pandas as pd


def generate_pdf_report(user_id):

    file_path = "Habit_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    title_style = ParagraphStyle(name="Title", fontSize=20)
    elements.append(Paragraph("Habit Performance Report", title_style))
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

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

        fig = px.line(
            df,
            x="date",
            y="value",
            color="habit_name",
            markers=True,
        )

        img_bytes = fig.to_image(format="png")

        with open("temp_chart.png", "wb") as f:
            f.write(img_bytes)

        elements.append(Image("temp_chart.png", width=500, height=300))

    doc.build(elements)
    return file_path
