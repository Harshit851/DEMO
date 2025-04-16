import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Gemini import generate_sql_query, execute_query

# Page setup
st.set_page_config(page_title="Data Insight Assistant", layout="centered")
st.title("Data Insight Assistant")

st.markdown("""
Upload a CSV file, ask questions in natural language, and generate insights with SQL and visualizations.
""")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully.")
        st.markdown("#### Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    # Question input
    st.markdown("#### Ask a Question")
    user_question = st.text_input("Enter your query about the data")

    if user_question:
        with st.spinner("Processing your query..."):
            try:
                sql = generate_sql_query(user_question, df)
                result_df = execute_query(sql, df)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.stop()

        st.markdown("#### Generated SQL Query")
        st.code(sql, language="sql")

        st.markdown("#### Query Result")
        if isinstance(result_df, pd.DataFrame) and not result_df.empty:
            st.dataframe(result_df, use_container_width=True)

            # Download option
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Result as CSV", csv, "query_result.csv", "text/csv")

            # Visualization
            st.markdown("#### Visualize the Result")

            categorical_cols = result_df.select_dtypes(include=['object', 'category']).columns.tolist()
            numeric_cols = result_df.select_dtypes(include='number').columns.tolist()

            if categorical_cols and numeric_cols:
                chart_type = st.selectbox("Select Chart Type", ["Bar", "Line", "Pie"])
                x_col = st.selectbox("X-axis", categorical_cols)
                y_col = st.selectbox("Y-axis", numeric_cols)

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

                # Basic interpretation
                st.markdown("#### Interpretation")

                try:
                    top = chart_data.sort_values(by=y_col, ascending=False).iloc[0]
                    bottom = chart_data.sort_values(by=y_col).iloc[0]

                    st.markdown(f"- **{y_col}** is highest for **{top[x_col]}**: {top[y_col]:,.2f}")
                    st.markdown(f"- **{y_col}** is lowest for **{bottom[x_col]}**: {bottom[y_col]:,.2f}")
                    
                    if chart_type == "Line":
                        st.markdown(f"- The line chart highlights how **{y_col}** trends across **{x_col}**.")
                except Exception as e:
                    st.warning("Could not generate interpretation.")

            else:
                st.warning("The result must contain at least one categorical and one numeric column for visualization.")
        else:
            st.warning("No results returned for this query.")
