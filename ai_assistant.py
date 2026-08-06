import streamlit as st
from ai_cleaner import (
    ask_dataset_question,
    generate_dataset_summary,
    generate_cleaning_suggestions,
    generate_data_quality_score,
    get_quality_badge
)


def show_ai_assistant(df):

    st.title("🤖 AI Data Assistant")

    st.markdown(
        """
        Ask questions about your dataset using **Google Gemini AI**.
        """
    )

    st.divider()

   

    score = generate_data_quality_score(df)

    c1, c2 = st.columns([1, 3])

    with c1:
        st.metric("Quality Score", f"{score}/100")

    with c2:
        st.success(get_quality_badge(score))

    st.divider()



    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "📊 Generate Dataset Summary",
            use_container_width=True
        ):

            with st.spinner("Gemini is analyzing your dataset..."):

                summary = generate_dataset_summary(df)

                st.markdown("## 📊 Dataset Summary")

                st.markdown(summary)

    with c2:

        if st.button(
            "🧹 Cleaning Suggestions",
            use_container_width=True
        ):

            with st.spinner("Generating recommendations..."):

                suggestions = generate_cleaning_suggestions(df)

                st.markdown("## 🧹 Cleaning Suggestions")

                st.markdown(suggestions)

    st.divider()


    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Summarize this dataset",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Summarize this dataset."

        if st.button(
            "Find data quality issues",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Find data quality issues."

        if st.button(
            "Recommend ML model",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Which machine learning model is suitable for this dataset?"

    with col2:

        if st.button(
            "Suggest charts",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Suggest the best visualizations."

        if st.button(
            "Find outliers",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Find possible outliers."

        if st.button(
            "Business insights",
            use_container_width=True
        ):
            st.session_state["ai_question"] = "Provide business insights."

    st.divider()


    default_question = st.session_state.get(
        "ai_question",
        ""
    )

    question = st.text_area(
        "Ask anything about your dataset",
        value=default_question,
        height=120,
        placeholder="Example: Which columns should I clean first?"
    )

    if st.button(
        "🚀 Ask Gemini",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Gemini is thinking..."):

                answer = ask_dataset_question(
                    df,
                    question
                )

                st.markdown("## 🤖 Gemini Answer")

                st.markdown(answer)
         

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.button(
        "💬 Save Conversation",
        use_container_width=True
    ):

        if question.strip() != "":

            st.session_state["chat_history"].append(
                {
                    "question": question,
                    "answer": answer if "answer" in locals() else ""
                }
            )

            st.success("Conversation saved.")

    st.divider()

 

    st.subheader("💬 Conversation History")

    if len(st.session_state["chat_history"]) == 0:

        st.info("No conversations yet.")

    else:

        for i, chat in enumerate(
            reversed(st.session_state["chat_history"]),
            start=1
        ):

            with st.expander(f"Conversation {i}"):

                st.markdown("### 🙋 Question")

                st.write(chat["question"])

                st.markdown("### 🤖 Gemini")

                st.markdown(chat["answer"])

    st.divider()

   

    if len(st.session_state["chat_history"]) > 0:

        text = ""

        for chat in st.session_state["chat_history"]:

            text += f"Question:\n{chat['question']}\n\n"

            text += f"Answer:\n{chat['answer']}\n\n"

            text += "=" * 60

            text += "\n\n"

        st.download_button(
            "📥 Download Conversation",
            data=text,
            file_name="AI_Conversation.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

   
    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True
    ):

        st.session_state["chat_history"] = []

        st.success("Conversation cleared.")

        st.rerun()

    st.divider()

    with st.expander("📋 Dataset Information"):

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", len(df))

        c2.metric("Columns", len(df.columns))

        c3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        c4.metric(
            "Duplicates",
            int(df.duplicated().sum())
        )

        st.write("### Columns")

        st.write(list(df.columns))

        st.write("### Data Types")

        st.dataframe(
            df.dtypes.astype(str),
            use_container_width=True
        )

    st.divider()

    with st.expander("💡 AI Tips"):

        st.markdown("""
### You can ask questions like:

- Summarize this dataset.

- Which columns contain missing values?

- Recommend machine learning algorithms.

- Suggest feature engineering.

- Find data quality issues.

- Detect outliers.

- Explain the relationships between variables.

- Suggest visualizations.

- Recommend preprocessing steps.

- Explain this dataset to a beginner.
""")