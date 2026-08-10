import streamlit as st
from ai_cleaner import (
    ask_dataset_question,
    generate_dataset_summary,
    generate_cleaning_suggestions,
    generate_data_quality_score,
    get_quality_badge,
)


def show_ai_assistant(df):

    st.title("🤖 AI Data Assistant")
    st.caption("Ask questions about your dataset using **Google Gemini AI**.")

    st.divider()

    # -------------------------------------------------------------------------
    # DATA QUALITY SCORE CARD
    # -------------------------------------------------------------------------
    score = generate_data_quality_score(df)

    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("Quality Score", f"{score}/100")
    with c2:
        st.success(f"Status: {get_quality_badge(score)}")

    st.divider()

    # -------------------------------------------------------------------------
    # SESSION STATE INITIALIZATION
    # -------------------------------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "latest_summary" not in st.session_state:
        st.session_state["latest_summary"] = None

    if "latest_suggestions" not in st.session_state:
        st.session_state["latest_suggestions"] = None

    if "current_answer" not in st.session_state:
        st.session_state["current_answer"] = None

    # -------------------------------------------------------------------------
    # ONE-CLICK ANALYSIS BUTTONS
    # -------------------------------------------------------------------------
    c1, c2 = st.columns(2)

    with c1:
        if st.button("📊 Generate Dataset Summary", use_container_width=True):
            with st.spinner("Gemini is analyzing your dataset..."):
                st.session_state["latest_summary"] = generate_dataset_summary(df)

    with c2:
        if st.button("🧹 Cleaning Suggestions", use_container_width=True):
            with st.spinner("Generating recommendations..."):
                st.session_state["latest_suggestions"] = generate_cleaning_suggestions(df)

    # Render Summary if stored in session state
    if st.session_state["latest_summary"]:
        st.markdown("## 📊 Dataset Summary")
        st.markdown(st.session_state["latest_summary"])
        st.divider()

    # Render Suggestions if stored in session state
    if st.session_state["latest_suggestions"]:
        st.markdown("## 🧹 Cleaning Suggestions")
        st.markdown(st.session_state["latest_suggestions"])
        st.divider()

    # -------------------------------------------------------------------------
    # SUGGESTED QUESTIONS
    # -------------------------------------------------------------------------
    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Summarize this dataset", use_container_width=True):
            st.session_state["ai_question"] = "Summarize this dataset."
            st.rerun()

        if st.button("Find data quality issues", use_container_width=True):
            st.session_state["ai_question"] = "Find data quality issues."
            st.rerun()

        if st.button("Recommend ML model", use_container_width=True):
            st.session_state["ai_question"] = "Which machine learning model is suitable for this dataset?"
            st.rerun()

    with col2:
        if st.button("Suggest charts", use_container_width=True):
            st.session_state["ai_question"] = "Suggest the best visualizations."
            st.rerun()

        if st.button("Find outliers", use_container_width=True):
            st.session_state["ai_question"] = "Find possible outliers."
            st.rerun()

        if st.button("Business insights", use_container_width=True):
            st.session_state["ai_question"] = "Provide business insights."
            st.rerun()

    st.divider()

    # -------------------------------------------------------------------------
    # USER QUESTION INPUT
    # -------------------------------------------------------------------------
    default_question = st.session_state.get("ai_question", "")

    question = st.text_area(
        "Ask anything about your dataset",
        value=default_question,
        height=120,
        placeholder="Example: Which columns should I clean first?",
    )

    if st.button("🚀 Ask Gemini", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Gemini is thinking..."):
                answer = ask_dataset_question(df, question)

                # Save answer in state
                st.session_state["current_answer"] = answer

                # Automatically append to conversation history
                st.session_state["chat_history"].append(
                    {"question": question, "answer": answer}
                )

    # Display current Gemini Answer
    if st.session_state["current_answer"]:
        st.markdown("## 🤖 Gemini Answer")
        st.markdown(st.session_state["current_answer"])

    st.divider()

    # -------------------------------------------------------------------------
    # CONVERSATION HISTORY & EXPORT
    # -------------------------------------------------------------------------
    st.subheader("💬 Conversation History")

    if not st.session_state["chat_history"]:
        st.info("No conversations yet.")
    else:
        for i, chat in enumerate(reversed(st.session_state["chat_history"]), start=1):
            with st.expander(f"Conversation {len(st.session_state['chat_history']) - i + 1}: {chat['question'][:50]}..."):
                st.markdown("### 🙋 Question")
                st.write(chat["question"])
                st.markdown("### 🤖 Gemini")
                st.markdown(chat["answer"])

        st.divider()

        # Download Conversation
        formatted_history = ""
        for chat in st.session_state["chat_history"]:
            formatted_history += f"Question:\n{chat['question']}\n\n"
            formatted_history += f"Answer:\n{chat['answer']}\n\n"
            formatted_history += "=" * 60 + "\n\n"

        c_dl, c_clr = st.columns(2)

        with c_dl:
            st.download_button(
                "📥 Download Conversation",
                data=formatted_history,
                file_name="AI_Conversation.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with c_clr:
            if st.button("🗑 Clear Conversation", use_container_width=True):
                st.session_state["chat_history"] = []
                st.session_state["current_answer"] = None
                st.session_state["ai_question"] = ""
                st.success("Conversation cleared.")
                st.rerun()

    st.divider()

    # -------------------------------------------------------------------------
    # DATASET OVERVIEW EXPANDERS
    # -------------------------------------------------------------------------
    with st.expander("📋 Dataset Information"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{len(df):,}")
        c2.metric("Columns", len(df.columns))
        c3.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")
        c4.metric("Duplicates", f"{int(df.duplicated().sum()):,}")

        st.write("### Columns")
        st.write(list(df.columns))

        st.write("### Data Types")
        st.dataframe(df.dtypes.astype(str), use_container_width=True)

    with st.expander("💡 AI Tips"):
        st.markdown(
            """
### Useful Prompts:
- **Summarize this dataset** in non-technical terms.
- Which columns contain **missing values or anomalies**?
- Recommend **machine learning models** suitable for predicting `[column_name]`.
- Suggest **feature engineering steps** to improve data quality.
- Detect potential **outliers** in numeric columns.
- Explain the **correlations** between key attributes.
"""
        )
