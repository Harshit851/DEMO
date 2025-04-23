import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Gemini import list_tables, generate_sql_query, execute_query
import requests
import time
import datetime


# === PAGE SETUP ===
st.set_page_config(page_title="Data Insight Assistant", layout="centered")  # Moved to the top

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Failed to load animation: {r.status_code}")
            return None
    except Exception as e:
        st.error(f"Error loading animation: {e}")
        return None


st.markdown("""
    <style>
        body {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .main {
            background-color: #ffffffdd;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        }

        .stTextInput>div>div>input {
            border: 1px solid #d1d5db;
            padding: 12px;
        }
    </style>
""", unsafe_allow_html=True)


# === FIXED CONFIG ===
FIXED_DATABASE = "Harshit" # Replace with your actual database name


st.title("Data Insight Assistant")
st.markdown("Select tables, ask questions, and visualize insights from your database.")

# === STEP 1: LOAD TABLES ===
try:
    all_tables = list_tables(FIXED_DATABASE)
except Exception as e:
    st.error(f"Error loading tables: {e}")
    st.stop()

# === STEP 2: SELECT TABLES ===
selected_tables = st.multiselect("Select one or more tables from the database", all_tables)

# === Function to get table column names ===
def get_column_names(table_name):
    try:
        # Assuming your 'Gemini' module has a function to fetch column names
        columns = execute_query(f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}'
        """, FIXED_DATABASE)
        return [col['COLUMN_NAME'] for col in columns.to_dict('records')]
    except Exception as e:
        st.warning(f"Could not retrieve column names for '{table_name}': {e}")
        return []

# === STEP 3: PREVIEW SELECTED TABLES (COLUMN NAMES ONLY) ===
if selected_tables:
    st.markdown("### Table Columns")
    for table in selected_tables:
        st.markdown(f"**📘 {table}**")
        column_names = get_column_names(table)
        if column_names:
            st.markdown(", ".join(column_names))
        else:
            st.warning(f"Could not display column names for '{table}'.")

# === STEP 4: ASK QUESTION ===
if selected_tables:
    user_question = st.text_input(" Drop your question here..", placeholder=" eg:Show total sales by category")

    if user_question:
        with st.spinner(" Generating SQL..."):
            try:
                # Add table context to the question
                table_context = ", ".join(selected_tables)
                prompt = f"Use the following tables: {table_context}. {user_question}"
                sql_query = generate_sql_query(prompt)
                result_df = execute_query(sql_query, FIXED_DATABASE)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        # === STEP 5: DISPLAY SQL + RESULTS ===
        st.markdown("### Generated SQL Query")
        st.code(sql_query, language="sql")

        st.markdown("### Explected Result")
        if not result_df.empty:
            st.dataframe(result_df, use_container_width=True)

            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Download Result as CSV", csv, "query_result.csv", "text/csv")

            # === STEP 6: VISUALIZATION ===
            st.markdown("### Visualization makes easy to understand")

            cat_cols = result_df.select_dtypes(include=['object', 'category']).columns.tolist()
            num_cols = result_df.select_dtypes(include='number').columns.tolist()

            if cat_cols and num_cols:
                chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Pie"])
                x_col = st.selectbox("X-axis (categorical)", cat_cols)
                y_col = st.selectbox("Y-axis (numeric)", num_cols)
                chart_data = result_df[[x_col, y_col]].dropna()

                if chart_type == "Bar":
                    st.bar_chart(chart_data.set_index(x_col))
                elif chart_type == "Line":
                    st.line_chart(chart_data.set_index(x_col))
                elif chart_type == "Pie":
                    pie_data = chart_data.groupby(x_col)[y_col].sum().nlargest(10)
                    fig, ax = plt.subplots()
                    pie_data.plot.pie(autopct='%1.1f%%', ylabel='', ax=ax, figsize=(6, 6))
                    st.pyplot(fig)

                # === STEP 7: INTERPRETATION ===
                st.markdown("### 🧠 Basic Interpretation")
                try:
                    top = chart_data.sort_values(by=y_col, ascending=False).iloc[0]
                    bottom = chart_data.sort_values(by=y_col).iloc[0]

                    st.markdown(f"- **{y_col}** is highest for **{top[x_col]}**: `{top[y_col]:,.2f}`")
                    st.markdown(f"- **{y_col}** is lowest for **{bottom[x_col]}**: `{bottom[y_col]:,.2f}`")

                    if chart_type == "Line":
                        st.markdown(f"- The line chart shows trends in **{y_col}** across **{x_col}**.")
                    elif chart_type == "Pie":
                        st.markdown(f"- Pie chart displays the contribution of **{x_col}** to **{y_col}**.")
                except Exception as e:
                    st.warning("Couldn't interpret the chart.")
            else:
                st.warning("Need at least one categorical and one numeric column to visualize.")

        else:
            st.warning("Query returned no results.")
else:
    st.info("Please select one or more tables to begin.")


st.sidebar.title("Navigation")
st.sidebar.markdown("Explore your database:")
st.sidebar.markdown("- 📈 Sales Trends\n- 👥 Customer Insights\n- 🛍 Transaction Performance")
st.sidebar.markdown("---")
st.sidebar.title(" Feedback")

feedback = st.sidebar.text_area("How can we improve?", height=100)
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success(" Thanks for your feedback!")