import pandas as pd
import pyodbc
import google.generativeai as genai

# ✅ Gemini API Key
genai.configure(api_key="SHUBH-api key")

# ✅ Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ SQL Server connection string (Windows Auth)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-DOER-SHUBH-BHARDWAJ\\SQLEXPRESS;"
    "DATABASE=transaction_data;"  
    "Trusted_Connection=yes;"
)

# ✅ Get a sample of your table to show Gemini
def get_table_info():
    with pyodbc.connect(conn_str) as conn:
        df = pd.read_sql("SELECT TOP 3 * FROM transaction_data", conn)
    return df

# ✅ Generate SQL using Gemini AI
def generate_sql_query(user_question, df_sample):
    prompt = f"""
You are an expert in SQL Server. Write a valid SQL Server query using this info:

Table name: transaction_data  
Columns: {list(df_sample.columns)}  
Sample rows: {df_sample.to_dict(orient='records')}  

Question: {user_question}

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
        question = input("\nAsk a question about your transaction data (or type 'q' to quit): ")
        if question.lower() == 'q':
            break
        sample_data = get_table_info()
        sql = generate_sql_query(question, sample_data)
        print("\n🧠 SQL Generated:\n", sql)
        result = run_query(sql)
        print("\n📊 Query Result:")
        print(result)



