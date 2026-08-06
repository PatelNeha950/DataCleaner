import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from ai_cleaner import (
    generate_chart_insights,
    generate_dataset_summary,
    ask_dataset_question,
    generate_cleaning_suggestions,
    generate_data_quality_score,
    get_quality_badge
)
from ai_assistant import show_ai_assistant
from report import show_export_page
from config import *



configure_page()



def load_css():
    with open("style.css", "r", encoding="utf-8") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


load_css()

if SESSION_DATA not in st.session_state:
    st.session_state[SESSION_DATA] = None

if SESSION_CLEAN not in st.session_state:
    st.session_state[SESSION_CLEAN] = None

if SESSION_FILE not in st.session_state:
    st.session_state[SESSION_FILE] = ""



with st.sidebar:

    st.markdown(f"## {APP_NAME}")
    st.caption(APP_DESCRIPTION)
    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Upload CSV or Excel", type=SUPPORTED_FILES
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Dataset",
            "🧹 Cleaning",
            "📊 Visualization",
            "🤖 AI Assistant",
            "📥 Export",
        ],
    )

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.session_state[SESSION_DATA] = df
        st.session_state[SESSION_CLEAN] = df.copy()
        st.session_state[SESSION_FILE] = uploaded_file.name

    except Exception as e:
        st.error(f"Error loading file: {e}")


if page == "🏠 Dashboard":

    st.markdown(
        """
    <div class="glass">

    <div class="hero-title">
    🧹DataForge AI
    </div>

    <div class="hero-subtitle">
    Upload • Clean • Analyze • Visualize • Export datasets using AI
    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.session_state[SESSION_DATA] is None:

        st.info("👈 Upload a CSV or Excel file from the sidebar.")

    else:

        df = st.session_state[SESSION_DATA]

        rows = df.shape[0]
        cols = df.shape[1]
        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
            <div class="metric-card">
            <div class="metric-title">Rows</div>
            <div class="metric-value">{rows:,}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
            <div class="metric-card">
            <div class="metric-title">Columns</div>
            <div class="metric-value">{cols}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
            <div class="metric-card">
            <div class="metric-title">Missing</div>
            <div class="metric-value">{missing}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c4:
            st.markdown(
                f"""
            <div class="metric-card">
            <div class="metric-title">Duplicates</div>
            <div class="metric-value">{duplicates}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.write("")

        st.subheader("📋 Dataset Preview")

        st.dataframe(df.head(DEFAULT_ROWS), use_container_width=True)



elif page == "📄 Dataset":

    st.title("📄 Dataset Information")

    if st.session_state[SESSION_DATA] is None:
        st.warning("📂 Please upload a dataset first.")
        st.stop()

    df = st.session_state[SESSION_DATA]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Overview", "📊 Statistics", "❌ Missing Values", "ℹ️ Data Types"]
    )

    

    with tab1:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Rows", f"{df.shape[0]:,}")

        with c2:
            st.metric("Columns", df.shape[1])

        with c3:
            memory = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("Memory", f"{memory:.2f} MB")

        st.divider()

        st.subheader("Dataset Preview")

        row_count = len(df)

        if row_count == 1:
            rows = 1
            st.info("Dataset contains only one row.")
        else:
            rows = st.slider(
                "Preview Rows",
                min_value=1,
                max_value=row_count,
                value=min(10, row_count),
            )

        st.dataframe(df.head(rows), use_container_width=True)



    with tab2:

        st.subheader("Numerical Statistics")

        try:
            st.dataframe(df.describe().T, use_container_width=True)
        except Exception:
            st.info("No numeric columns found.")

        st.divider()

        st.subheader("Categorical Statistics")

        try:
            st.dataframe(
                df.describe(include="object").T, use_container_width=True
            )
        except Exception:
            st.info("No categorical columns found.")

   

    with tab3:

        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if len(missing) == 0:
            st.success("🎉 No missing values found.")
        else:
            report = missing.reset_index()
            report.columns = ["Column", "Missing Values"]
            report["Percentage"] = (
                report["Missing Values"] / len(df) * 100
            ).round(2)

            st.dataframe(report, use_container_width=True)
            st.bar_chart(report.set_index("Column")["Missing Values"])

   

    with tab4:

        info = pd.DataFrame(
            {
                "Column": df.columns,
                "Datatype": df.dtypes.astype(str),
                "Unique Values": [df[c].nunique() for c in df.columns],
                "Null Values": [df[c].isnull().sum() for c in df.columns],
            }
        )

        st.dataframe(info, use_container_width=True)



elif page == "🧹 Cleaning":

    st.title("🧹 Data Cleaning")

    if st.session_state[SESSION_CLEAN] is None:
        st.warning("📂 Please upload a dataset first.")
        st.stop()

    df = st.session_state[SESSION_CLEAN].copy()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "❌ Missing Values",
            "🔁 Duplicates",
            "🗑 Columns",
            "🔤 Text Cleaning",
        ]
    )


    with tab1:

        st.subheader("Handle Missing Values")

        method = st.selectbox(
            "Choose Method",
            [
                "Drop Rows",
                "Fill Mean",
                "Fill Median",
                "Fill Mode",
                "Fill Zero",
            ],
        )

        if st.button("Apply Missing Value Cleaning"):

            numeric = df.select_dtypes(include="number").columns

            if method == "Drop Rows":
                df = df.dropna()

            elif method == "Fill Mean":
                for col in numeric:
                    df[col] = df[col].fillna(df[col].mean())

            elif method == "Fill Median":
                for col in numeric:
                    df[col] = df[col].fillna(df[col].median())

            elif method == "Fill Mode":
                for col in df.columns:
                    mode = df[col].mode()
                    if not mode.empty:
                        df[col] = df[col].fillna(mode.iloc[0])

            elif method == "Fill Zero":
                df = df.fillna(0)

            st.session_state[SESSION_CLEAN] = df
            st.success("✅ Missing values cleaned.")

  

    with tab2:

        duplicates = int(df.duplicated().sum())

        st.metric("Duplicate Rows", duplicates)

        if st.button("Remove Duplicates"):

            before = len(df)
            df = df.drop_duplicates()
            after = len(df)

            st.session_state[SESSION_CLEAN] = df
            st.success(f"Removed {before - after} duplicate rows.")


    with tab3:

        selected = st.multiselect("Select Columns", df.columns.tolist())

        if st.button("Delete Selected Columns"):

            if selected:
                df = df.drop(columns=selected)
                st.session_state[SESSION_CLEAN] = df
                st.success("Selected columns deleted.")

 

    with tab4:

        text_columns = df.select_dtypes(include="object").columns.tolist()

        if not text_columns:
            st.info("No text columns found.")
        else:
            column = st.selectbox("Select Text Column", text_columns)

            action = st.selectbox(
                "Action",
                ["Uppercase", "Lowercase", "Title Case", "Trim Spaces"],
            )

            if st.button("Apply Text Cleaning"):

                if action == "Uppercase":
                    df[column] = df[column].astype(str).str.upper()

                elif action == "Lowercase":
                    df[column] = df[column].astype(str).str.lower()

                elif action == "Title Case":
                    df[column] = df[column].astype(str).str.title()

                elif action == "Trim Spaces":
                    df[column] = df[column].astype(str).str.strip()

                st.session_state[SESSION_CLEAN] = df
                st.success("✅ Text cleaned successfully.")

    st.divider()

    st.subheader("Preview Cleaned Dataset")

    st.dataframe(
        st.session_state[SESSION_CLEAN].head(20), use_container_width=True
    )


elif page == "📊 Visualization":

    st.title("📊 Interactive Data Visualization")

    if st.session_state[SESSION_CLEAN] is None:
        st.warning("📂 Please upload a dataset first.")
        st.stop()

    df = st.session_state[SESSION_CLEAN]

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📊 Bar Chart",
            "📈 Line Chart",
            "🥧 Pie Chart",
            "⚫ Scatter Plot",
            "📦 Box Plot",
            "📉 Histogram",
            "🔥 Correlation Heatmap",
        ]
    )



    with tab1:

        st.subheader("📊 Bar Chart")

        if len(categorical_cols) == 0 or len(numeric_cols) == 0:

            st.info("Need at least one categorical and one numeric column.")

        else:

            x = st.selectbox(
                "Category Column", categorical_cols, key="bar_x"
            )

            y = st.selectbox("Numeric Column", numeric_cols, key="bar_y")

            color = st.checkbox(
                "Color by Category", value=True, key="bar_color"
            )

            fig = px.bar(
                df,
                x=x,
                y=y,
                color=x if color else None,
                template="plotly_white",
                text_auto=True,
                title=f"{y} by {x}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Generate AI Insights", key="bar_ai"):

                with st.spinner("Analyzing chart..."):

                    insights = generate_chart_insights(
                        df, "Bar Chart", x, y
                    )

                    st.markdown("## 🤖 AI Insights")
                    st.markdown(insights)


    with tab2:

        st.subheader("📈 Line Chart")

        if len(numeric_cols) < 2:

            st.info("Need at least two numeric columns.")

        else:

            x = st.selectbox("X Axis", numeric_cols, key="line_x")

            y = st.selectbox(
                "Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="line_y"
            )

            markers = st.checkbox(
                "Show Markers", value=True, key="markers"
            )

            fig = px.line(
                df,
                x=x,
                y=y,
                markers=markers,
                template="plotly_white",
                title=f"{y} vs {x}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Generate AI Insights", key="line_ai"):

                with st.spinner("Gemini is analyzing..."):

                    insights = generate_chart_insights(
                        df, "Line Chart", x, y
                    )

                    st.markdown("## 🤖 AI Insights")
                    st.markdown(insights)


    with tab3:

        st.subheader("🥧 Pie Chart")

        if len(categorical_cols) == 0:

            st.info("No categorical columns available.")

        else:

            column = st.selectbox(
                "Category", categorical_cols, key="pie_column"
            )

            pie_df = df[column].value_counts().reset_index()

            pie_df.columns = [column, "Count"]

            fig = px.pie(
                pie_df,
                names=column,
                values="Count",
                hole=0.45,
                template="plotly_white",
                title=f"Distribution of {column}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Generate AI Insights", key="pie_ai"):

                with st.spinner("Generating AI insights..."):

                    insights = generate_chart_insights(
                        df, "Pie Chart", column, None
                    )

                    st.markdown("## 🤖 AI Insights")
                    st.markdown(insights)

   

    with tab4:

        st.subheader("⚫ Scatter Plot")

        if len(numeric_cols) < 2:

            st.info("Need at least two numeric columns.")

        else:

            x = st.selectbox("X Axis", numeric_cols, key="scatter_x")

            y = st.selectbox(
                "Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_y"
            )

            color = st.selectbox(
                "Color By (Optional)",
                ["None"] + categorical_cols,
                key="scatter_color",
            )

            fig = px.scatter(
                df,
                x=x,
                y=y,
                color=None if color == "None" else color,
                template="plotly_white",
                title=f"{y} vs {x}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Analyze Scatter Plot", key="scatter_ai"):

                with st.spinner("Gemini is analyzing..."):

                    insights = generate_chart_insights(
                        df, "Scatter Plot", x, y
                    )

                    st.markdown(insights)


    with tab5:

        st.subheader("📦 Box Plot")

        if len(numeric_cols) == 0:

            st.info("No numeric columns found.")

        else:

            column = st.selectbox(
                "Select Column", numeric_cols, key="box_col"
            )

            fig = px.box(
                df,
                y=column,
                template="plotly_white",
                title=f"Box Plot of {column}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Explain Outliers", key="box_ai"):

                with st.spinner("Generating AI Insights..."):

                    insights = generate_chart_insights(
                        df, "Box Plot", column
                    )

                    st.markdown(insights)

  

    with tab6:

        st.subheader("📉 Histogram")

        if len(numeric_cols) == 0:

            st.info("No numeric columns available.")

        else:

            column = st.selectbox(
                "Numeric Column", numeric_cols, key="histogram"
            )

            bins = st.slider("Bins", 5, 100, 30)

            fig = px.histogram(
                df,
                x=column,
                nbins=bins,
                template="plotly_white",
                title=f"Distribution of {column}",
            )

            fig.update_layout(height=550, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Explain Distribution", key="hist_ai"):

                with st.spinner("Analyzing distribution..."):

                    insights = generate_chart_insights(
                        df, "Histogram", column
                    )

                    st.markdown(insights)

    with tab7:

        st.subheader("🔥 Correlation Heatmap")

        if len(numeric_cols) < 2:

            st.info("Need at least two numeric columns.")

        else:

            corr = df[numeric_cols].corr(numeric_only=True)

            fig = px.imshow(
                corr,
                text_auto=".2f",
                color_continuous_scale="Blues",
                aspect="auto",
                title="Correlation Matrix",
            )

            fig.update_layout(height=650, title_x=0.5)

            st.plotly_chart(fig, use_container_width=True)

            if st.button("🤖 Correlation Insights", key="corr_ai"):

                with st.spinner("Gemini is analyzing correlations..."):

                    insights = generate_chart_insights(
                        df, "Correlation Heatmap", ", ".join(numeric_cols)
                    )

                    st.markdown("## 🤖 AI Correlation Insights")
                    st.markdown(insights)
elif page == "🤖 AI Assistant":

    if st.session_state[SESSION_CLEAN] is None:

        st.warning("📂 Please upload a dataset first.")

    else:

        show_ai_assistant(
            st.session_state[SESSION_CLEAN]
        )
elif page == "📥 Export":

    if st.session_state[SESSION_CLEAN] is None:

        st.warning("📂 Please upload a dataset first.")

    else:

        show_export_page(
            st.session_state[SESSION_CLEAN]
        )