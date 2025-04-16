

import pandas as pd
import google.generativeai as genai
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('AIzaSyCiWdmF8HWxmtEnDPdERhvTexu_KhEnZFA'))
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_sql_query(user_question, df):
    """Generate SQL using Gemini based on user question and CSV structure"""
    prompt = f"""
    Given this CSV structure:
    Columns: {', '.join(df.columns)}
    Sample data: {df.head(3).to_dict()}

    Create an SQL query for: {user_question}
    - Use table name 'sales'
    - Return ONLY raw SQL code
    - Use SQLite syntax
    """
    
    response = model.generate_content(prompt)
    sql = response.text.strip('` \n')
    sql = sql.replace("sql\n", "")  
    return sql

def execute_query(sql, df):
    """Execute SQL query on the data"""
    conn = sqlite3.connect(':memory:')
    df.to_sql('sales', conn, index=False, if_exists='replace')
    
    try:
        result = pd.read_sql_query(sql, conn)
        return result
    except Exception as e:
        return pd.DataFrame({'Error': [str(e)]})
    finally:
        conn.close()
