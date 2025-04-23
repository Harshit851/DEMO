## Mysql Assistant
A Streamlit-powered application that transforms natural language questions into SQL queries based on the data(Tables) are there in the database and presents both tabular results and interactive visualizations with basic graph summaries.

## 🚀 Features
````
-📂 choose table from Connected database 

-💬 Ask questions in plain English

-🧠 Auto-generates SQL queries using a language model

-📊 View results as tables, bar/line/pie charts

-📝 Read quick insights through graph interpretations

-📥 Download query results as CSV
````

### 🛠️ How It Works
```
select the tables from the database 

Ask a Question
Enter a natural language question about the data (e.g., "What is the total sales by region?").

SQL Generation & Execution
Your query is converted into an SQL statement and executed on the uploaded data.

Results Display
The app shows the output as a table and lets you download it.

Visualize the Output
Choose chart type (Bar, Line, Pie) and axis columns to generate a dynamic chart.

Read Insights
Auto-generated textual summaries help interpret the graph (e.g., highest/lowest values, trend lines).
````

## 📦 Installation
Make sure Python is installed, then run:

```
pip install streamlit pandas matplotlib
pip install pyodbc
pip install google.generativeai
```

## Running the App

````
streamlit run Streamlit_app.py

````

## 📁 Project Structure

```
├── streamlit_app.py       # Main Streamlit app
├── Gemini.py              # SQL generation and query execution logic
├── README.md              # Project documentation
├── Csv file               # Data (Customer,Sales,transactionlog tables)

```
## configuration
```
-GEMINI_API_KEY = ""  ## insert your Api Key(GEMINI)
-SQL_SERVER_NAME = "Hp\SQLEXPRESS"  # Enter Your server name 
-SQL_DATABASE = "XYZ"  # your Database name 
-ODBC_DRIVER = "ODBC Driver 17 for SQL Server"  # Ensure this driver is installed

```

## 💡 Future Improvements
```
-Export charts as images or PDF

-Connects to the server and access the database 

-Add advanced chart options (e.g., bar, line)

-Enhance natural language understanding with context

```


