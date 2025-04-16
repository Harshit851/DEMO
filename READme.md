## Data Insight Assistant
A Streamlit-powered application that transforms natural language questions into SQL queries, executes them on user-uploaded CSV files, and presents both tabular results and interactive visualizations with basic graph summaries.

## 🚀 Features
````
📂 Upload any CSV dataset

💬 Ask questions in plain English

🧠 Auto-generates SQL queries using a language model

📊 View results as tables, bar/line/pie charts

📝 Read quick insights through graph interpretations

📥 Download query results as CSV
````

### 🛠️ How It Works
```
Upload CSV
Load any structured dataset via the file uploader.

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
```

## Running the App

````
streamlit run app.py

````

📁 Project Structure

```
├── app.py                 # Main Streamlit app
├── Gemini.py              # SQL generation and query execution logic
├── README.md              # Project documentation

```

## 💡 Future Improvements

```
Export charts as images or PDF

Support multiple CSV joins

Add advanced chart options (e.g., scatter, heatmap)

Enhance natural language understanding with context

```


