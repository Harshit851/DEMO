import pyodbc
import google.generativeai as genai
import pandas as pd

# ===== CONFIGURATION =====
GEMINI_API_KEY = ""  # Add your Gemini API key here
SQL_SERVER_NAME = r"Hp\SQLEXPRESS"  # Raw string for backslash
SQL_DATABASE = "Harshit"
ODBC_DRIVER = "ODBC Driver 17 for SQL Server"  # Ensure this driver is installed

# ===== INIT GEMINI =====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# ===== CONNECTION FUNCTION =====
def get_connection(database=None):
    db_part = f"DATABASE={database};" if database else ""
    conn_str = f"""
    DRIVER={{{ODBC_DRIVER}}};
    SERVER={SQL_SERVER_NAME};
    {db_part}
    Trusted_Connection=yes;
    """
    return pyodbc.connect(conn_str.strip())

# ===== LIST DATABASES =====
def list_databases():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")
        dbs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return dbs
    except Exception as e:
        raise RuntimeError(f"Error fetching databases: {e}")

# ===== LIST TABLES IN DATABASE =====
def list_tables(database):
    try:
        conn = get_connection(database)
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        raise RuntimeError(f"Error fetching tables: {e}")

# ===== GENERATE SQL QUERY FROM GEMINI =====
def generate_sql_query(question):
    prompt = f"""
-- Improved Prompt:

-- You are an expert SQL developer working exclusively with Microsoft SQL Server and the ODBC Driver 17 for SQL Server.
-- Your task is to generate 100% accurate and executable T-SQL queries that are compatible with this environment,
-- strictly adhering to the provided database schema.

-- Database Schema:

CREATE TABLE customers (
    Customer_ID NVARCHAR(50) PRIMARY KEY,
    Name NVARCHAR(50),
    Phone NVARCHAR(50),
    Address NVARCHAR(100)
);


CREATE TABLE shopping (
    Shopping_ID INT PRIMARY KEY IDENTITY(1,1),
    Customer_ID NVARCHAR(50) FOREIGN KEY REFERENCES customers(Customer_ID),
    Product NVARCHAR(50),
    Product_Category NVARCHAR(50),
    Units INT,
    Unit_Price FLOAT
);


CREATE TABLE transactions (
    Transaction_ID NVARCHAR(50) PRIMARY KEY,
    Customer_ID NVARCHAR(50) FOREIGN KEY REFERENCES customers(Customer_ID),
    Transaction_Date DATE,
    Transaction_Type NVARCHAR(50),
    Payment_Mode NVARCHAR(50),
    Status NVARCHAR(50),
    Channel NVARCHAR(50),
    Merchant_ID NVARCHAR(50)
);

-- Instructions:
anazlyze the schema and write a T-SQL query to answer the user's question.
-- 1. Use the provided schema to understand the tables and their relationships.
-- 1. Focus solely on generating T-SQL queries for Microsoft SQL Server.
-- 2. Use only the tables and columns defined in the provided schema.
-- 3. Employ appropriate SQL Server syntax (e.g., TOP, NVARCHAR, IDENTITY, GETDATE()).
-- 4. Utilize JOIN clauses based on Customer_ID to link tables where necessary.
-- 5. Interpret "total spent" as the sum of (Units * Unit_Price) from the shopping table.
-- 6. Define "least active" customers as those with the minimum number of entries in the transactions table.
-- 7. Define "most active" customers as those with the maximum number of entries in the transactions table.
-- 8. If a query requires arithmetic operations or aggregate functions (SUM, COUNT, MIN, MAX, AVG), apply them correctly.
-- 9. Return only the T-SQL query. Do not include explanations or descriptions.
-- 10. If the question is ambiguous or cannot be answered with the given schema, respond with "I cannot answer that."
-- 11. Ensure the query directly addresses the user's request and returns the exact number of items asked for (e.g., if "least active" is requested, return one result).

-- Example Questions (User will ask one of these or a similar question):

-- 1. Show the names and phone numbers of all customers.
-- 2. Find the total number of shopping transactions.
-- 3. List all products purchased by a specific customer (provide Customer_ID).
-- 4. Calculate the total amount spent by each customer.
-- 5. Identify the customer who has made the most shopping transactions.
-- 6. Identify the customer who has made the least shopping transactions.
-- 7. Find the most expensive product purchased and its price.
-- 8. List all transactions that occurred on a specific date (provide date).
-- 9. Show the different payment modes used in transactions.
-- 10. Find the average number of units purchased per shopping transaction.
-- 11. Get the names of customers who have made at least one transaction.
-- 12. Get the names of customers who have not made any transactions.
-- 13. Find the most frequent product category purchased.
-- 14. List customers and their last transaction date.
-- 15. Find the merchants with the highest number of transactions.

you have to analyze all the columns and tables in the schema to  write a every single SQL query to answer the question.
always take care of the quantity of returned rows are asked in the question.
-- 16. Find the customers who have spent the most in total.
Use joins wherever relevant (via Customer_ID which links the three tables).
increase the creativity of the response to make it more human-like.
-- Do not use any other database or table names other than the ones provided in the schema. 
-- Do not use any other SQL functions or keywords other than the ones provided in the schema.
-- Do not use any other SQL Server specific functions or keywords other than the ones provided in the schema.
always cross check the answer you provide and what is asked (ususally the question is asked in a human-like way).
-- Do not use any other SQL Server specific functions or keywords other than the ones provided in the schema.
dont youse select top 1 every single time use according to the need 
---
User question:
{question}
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 1.7,  # Balanced creativity + accuracy
            "top_k": 55,
            "top_p": 0.95
        }
    )
    sql_query = response.text.strip().strip("```sql").strip("```")
    return sql_query

# ===== EXECUTE SQL AND RETURN DATAFRAME =====
def execute_query(sql_query, database):
    try:
        conn = get_connection(database)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame.from_records(rows, columns=columns)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"SQL Execution failed: {e}")
