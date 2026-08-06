import io
import pandas as pd
import streamlit as st
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from ai_cleaner import (
    generate_dataset_summary,
    generate_cleaning_suggestions,
    generate_data_quality_score,
    get_quality_badge
)

def show_export_page(df):

    st.title("📥 Export Center")

    st.markdown(
        """
        Download your cleaned dataset or generate an AI report.
        """
    )

    st.divider()

    st.subheader("📂 Export Dataset")

    c1, c2 = st.columns(2)

    with c1:

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c2:

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Cleaned Data")

        st.download_button(
            label="⬇ Download Excel",
            data=excel_buffer.getvalue(),
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.divider()

    

    st.subheader("📊 Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing", int(df.isnull().sum().sum()))
    c4.metric("Duplicates", int(df.duplicated().sum()))

    st.divider()


    if st.button("📄 Generate PDF Report", use_container_width=True):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("<b> DataForge AI Report</b>", styles["Title"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(
            Paragraph(f"Rows : {len(df)}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Columns : {len(df.columns)}", styles["BodyText"])
        )

        story.append(
            Paragraph(
                f"Missing Values : {int(df.isnull().sum().sum())}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Duplicate Rows : {int(df.duplicated().sum())}",
                styles["BodyText"]
            )
        )

        doc.build(story)

        st.download_button(
            "⬇ Download PDF",
            data=buffer.getvalue(),
            file_name="AI_Data_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
     

    st.divider()

    st.header("🤖 AI Report Generator")

    quality_score = generate_data_quality_score(df)

    badge = get_quality_badge(quality_score)

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Data Quality Score",
            f"{quality_score}/100"
        )

    with c2:

        st.success(badge)

    st.divider()

    generate_ai = st.button(
        "🚀 Generate Complete AI Report",
        use_container_width=True
    )

    if generate_ai:

        with st.spinner("Gemini is analyzing your dataset..."):

            ai_summary = generate_dataset_summary(df)

            cleaning = generate_cleaning_suggestions(df)

        st.success("AI Report Generated Successfully!")

  

        st.subheader("📊 Executive Summary")

        st.markdown(ai_summary)

        st.divider()

        st.subheader("🧹 Cleaning Recommendations")

        st.markdown(cleaning)

        st.divider()

        st.subheader("📈 Dataset Statistics")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Rows",
                len(df)
            )

            st.metric(
                "Columns",
                len(df.columns)
            )

        with col2:

            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        st.divider()

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

      
        pdf_buffer = io.BytesIO()

        doc = SimpleDocTemplate(pdf_buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "DataForge AI REPORT",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Data Quality Score :</b> {quality_score}/100",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Status :</b> {badge}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>Executive Summary</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                ai_summary.replace("\n", "<br/>"),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>Cleaning Recommendations</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                cleaning.replace("\n", "<br/>"),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))
  

        story.append(
            Paragraph(
                "<b>Dataset Information</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"Rows : {len(df)}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Columns : {len(df.columns)}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Missing Values : {int(df.isnull().sum().sum())}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Duplicate Rows : {int(df.duplicated().sum())}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))

     

        story.append(
            Paragraph(
                "<b>Columns</b>",
                styles["Heading2"]
            )
        )

        for column in df.columns:

            story.append(
                Paragraph(
                    f"• {column} ({df[column].dtype})",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 15))

        

        story.append(
            Paragraph(
                "<b>Missing Value Report</b>",
                styles["Heading2"]
            )
        )

        missing = df.isnull().sum()

        for column, value in missing.items():

            story.append(
                Paragraph(
                    f"{column} : {value}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 15))

    

        numeric = df.select_dtypes(include="number")

        if not numeric.empty:

            story.append(
                Paragraph(
                    "<b>Numerical Statistics</b>",
                    styles["Heading2"]
                )
            )

            description = numeric.describe().round(2)

            for column in description.columns:

                stats = description[column]

                story.append(
                    Paragraph(
                        f"""
<b>{column}</b><br/>
Mean : {stats['mean']:.2f}<br/>
Std : {stats['std']:.2f}<br/>
Min : {stats['min']:.2f}<br/>
Max : {stats['max']:.2f}
""",
                        styles["BodyText"]
                    )
                )

        story.append(Spacer(1, 20))

        
       

        story.append(
            Paragraph(
                "<b>Generated by DataForge AI System</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                """
This report was automatically generated using
Google Gemini AI and Streamlit.

It contains AI-generated insights,
cleaning recommendations,
dataset profiling,
and quality assessment.

Thank you for using DataForge AI.
""",
                styles["BodyText"]
            )
        )

        

        doc.build(story)

        pdf_buffer.seek(0)

        st.success("✅ PDF Report Generated Successfully!")

        st.download_button(
            label="📥 Download AI Report",
            data=pdf_buffer,
            file_name="AI_Data_Cleaner_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )