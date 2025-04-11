import streamlit as st
import pandas as pd
from core_logic import generate_sql_query, execute_query

st.set_page_config(page_title="CSV SQL Assistant", layout="centered")
st.title("📊 CSV Q&A using Gemini")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.write("📋 **Preview:**")
    st.dataframe(df.head())

    user_question = st.text_input("Ask a question about the data:")

    if user_question:
        with st.spinner("Generating SQL and getting results..."):
            sql = generate_sql_query(user_question, df)
            result_df = execute_query(sql, df)

            st.subheader("🧠 Generated SQL Query")
            st.code(sql, language="sql")

            st.subheader("📊 Result")
            st.dataframe(result_df)
# this is a ui
