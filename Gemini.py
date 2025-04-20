import pyodbc
import google.generativeai as genai
import pandas as pd

# ===== CONFIGURATION =====
GEMINI_API_KEY = ""
SQL_SERVER_NAME = "Hp\SQLEXPRESS"  # Use raw string for backslash
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
    You are a helpful SQL assistant. Write a mySQL Server compatible query for this question.
    analyze the schema and generate the mySQL query accordingly.

CREATE TABLE TransactionLog (
    Transaction_ID VARCHAR(50) NOT NULL,
    Customer_ID VARCHAR(50) NOT NULL,
    Transaction_Date DATE,
    Transaction_Type VARCHAR(50),
    Amount FLOAT,
    Payment_Mode VARCHAR(50),
    Status VARCHAR(50),
    Channel VARCHAR(50),
    Merchant_ID VARCHAR(50),
    PRIMARY KEY (Transaction_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

CREATE TABLE CustomerTable (
    Customer_ID VARCHAR(50) NOT NULL,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Email VARCHAR(50),
    Phone VARCHAR(50),
    Address VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Registration_Date DATE,
    PRIMARY KEY (Customer_ID)
);

CREATE TABLE SalesTable (
    Sale_ID VARCHAR(50) NOT NULL,
    Customer_ID VARCHAR(50),
    Product_ID DECIMAL(10, 2),
    Product_Name VARCHAR(50),
    Category VARCHAR(50),
    Quantity TINYINT,
    Unit_Price FLOAT,
    Discount FLOAT,
    Sale_Date DATE,
    PRIMARY KEY (Sale_ID)
);


    Only output the mySQL code, nothing else.

    Question: {question}
    """
    response = model.generate_content(prompt)
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