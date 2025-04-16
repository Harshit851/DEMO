from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Configure the API key
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
except Exception as e:
    st.error(f"Error configuring Google Gemini API: {e}")

# Function to load Google Gemini model and provide SQL query as response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        st.error(f"Error generating response from Gemini: {e}")
        return None

# Prompt for the Gemini model
prompt = [
    """
    You are a SQL expert in converting English questions to SQL query!
    The SQL database has the CustomerData table with the following columns:
    CustomerID, Name, Segment, Country, City.

    Example1: How many entries of records are present?
    → SELECT COUNT(*) FROM CustomerData;

    Example2: How many customers reside in the city of New York?
    → SELECT COUNT(*) FROM CustomerData WHERE City='New York';

    Example3: How many customers are of consumer segment?
    → SELECT COUNT(*) FROM CustomerData WHERE Segment='Consumer';

    Do not wrap SQL commands with triple quotes or markdown formatting.
    """
]

# Streamlit app config
st.set_page_config(page_title="Gemini SQL Query Generator", page_icon=":guardsman:", layout="wide")
st.header("Gemini App to Retrieve SQL data")

# Text input for user question
user_question = st.text_input("Enter your question:")

df = pd.DataFrame()  # Initialize df to avoid reference before assignment

# Generate and Run SQL
if user_question:
    with st.spinner("Generating SQL query using Gemini..."):
        try:
            response = get_gemini_response(user_question, prompt)
            sql_query = response.strip().strip("sql").strip("```")
            st.subheader("📝 Generated SQL Query")
            st.code(sql_query, language="sql")
        except Exception as e:
            st.error(f"Error generating SQL: {e}")
            st.stop()

    with st.spinner("📡 Executing query on SQLite..."):
        try:
            conn = sqlite3.connect("database.db")
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            st.success("✅ Query executed successfully!")
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
            st.stop()

# Display Results
if not df.empty:
    # Always show the table view
    st.subheader("📋 Table View of the Data")
    st.dataframe(df)

    # Handle single-number or single-cell result
    if df.shape == (1, 1):
        st.subheader("🔢 Single Value Result")
        st.metric(label=df.columns[0], value=df.iloc[0, 0])

    # Dropdown for charts and summary only (when there is more than one column)
    elif df.shape[1] > 1:
        st.subheader("📊 Choose how to visualize the result")
        output_type = st.selectbox("Select visualization type", ["Bar Chart", "Line Chart", "Pie Chart", "Area Chart", "Histogram", "Summary"])

        # Chart or Summary rendering
        if output_type != "Summary":
            with st.expander("📈 Chart Settings", expanded=True):
                if df.shape[1] < 2:
                    st.warning("Need at least two columns for charting.")
                else:
                    x_col = st.selectbox("X-axis", df.columns, index=0)
                    y_col = st.selectbox("Y-axis", df.columns, index=1)
                    theme_color = st.color_picker("🎨 Pick a chart color", "#636EFA")

                    if output_type == "Bar Chart":
                        fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=[theme_color])
                    elif output_type == "Line Chart":
                        fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=[theme_color])
                    elif output_type == "Pie Chart":
                        fig = px.pie(df, names=x_col, values=y_col)
                    elif output_type == "Area Chart":
                        fig = px.area(df, x=x_col, y=y_col, color_discrete_sequence=[theme_color])
                    elif output_type == "Histogram":
                        fig = px.histogram(df, x=y_col, nbins=20, color_discrete_sequence=[theme_color])

                    st.plotly_chart(fig, use_container_width=True)

        else:
            # Summary section
            st.subheader("🧾 Summary")
            if df.shape[1] >= 2:
                total = df.iloc[:, 1].sum()
                top_row = df.iloc[df.iloc[:, 1].idxmax()]
                st.markdown(f"- *Total {df.columns[1]}*: {total}")
                st.markdown(f"- *Top {df.columns[0]}*: {top_row[0]} with value {top_row[1]}")
            else:
                st.info("Not enough data to summarize.")
