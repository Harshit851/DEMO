import streamlit as st
import pandas as pd
from Gemini import generate_sql_query, execute_query

st.set_page_config(page_title="CSV SQL Assistant", layout="centered")
st.title("Analyze your data using SQL")

uploaded_file = st.file_uploader(" **Feed me your data** ", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.write(" **Your Data:**")
    st.dataframe(df.head(6))

    user_question = st.text_input("What your Question? : ")

    if user_question:
        with st.spinner("Generating SQL and getting results..."):
            sql = generate_sql_query(user_question, df)
            result_df = execute_query(sql, df)

            st.subheader(" Generated SQL Query")
            st.code(sql, language="sql")

            st.subheader("Result")
            st.dataframe(result_df)
# this is a ui
