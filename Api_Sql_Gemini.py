import pandas as pd
import pyodbc
import google.generativeai as genai

# ✅ Gemini API Key
genai.configure(api_key="AIzaSyCmpaaVg7ORvj0-AMp_Jm0jBqfRPU2RQjw")

# ✅ Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ SQL Server connection string (Windows Auth)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\SQLEXPRESS;"
    "DATABASE=test-manu;"  
    "Trusted_Connection=yes;"
)

# ✅ Get a sample of your table to show Gemini
def get_table_info():
    with pyodbc.connect(conn_str) as conn:
        df_customer = pd.read_sql("SELECT * FROM CustomerTable", conn)
        df_sales = pd.read_sql("SELECT * FROM SalesTable", conn)
        df_transaction = pd.read_sql("SELECT * FROM TransactionLog", conn)

    return {
        'CustomerTable': df_customer,
        'SalesTable': df_sales,
        'TransactionLog': df_transaction
    }

# ✅ Generate SQL using Gemini AI
def generate_sql_query_multi(user_question, table_dict):
    """
    table_dict: A dictionary with table names as keys and sample DataFrames as values.
    Example:
    {
        'CustomerTable': df_customer,
        'SalesTable': df_sales,
        'TransactionLog': df_trans
    }
    """
    table_descriptions = ""
    for table_name, df in table_dict.items():
        table_descriptions += f"Table name: {table_name}\n"
        table_descriptions += f"Columns: {', '.join(df.columns)}\n"
        sample_rows = df.head(3).to_dict(orient='records')
        table_descriptions += f"Sample rows: {sample_rows}\n\n"

    prompt = f"""
You are an expert in SQL Server. Write a valid SQL Server query using the following database schema and sample data.

{table_descriptions}

User question:
{user_question}

Return ONLY the SQL query without explanations.
"""
    response = model.generate_content(prompt)
    return response.text.strip().replace("```sql", "").replace("```", "").strip()

# ✅ Execute the SQL query
def run_query(sql):
    try:
        with pyodbc.connect(conn_str) as conn:
            df_result = pd.read_sql(sql, conn)
        return df_result
    except Exception as e:
        return f"❌ Error: {e}"

# ✅  Interactive loop
if __name__ == "__main__":
    print("✅ Ready! Connected to Gemini and SQL Server.")
    while True:
        question = input("\nAsk a question about your transaction_data (or type 'q' to quit): ")
        if question.lower() == 'q':
            break
        sample_data = get_table_info()
        sql = generate_sql_query(question, sample_data)
        print("\n🧠 SQL Generated:\n", sql)
        result = run_query(sql)
        print("\n📊 Query Result:")
        print(result)



