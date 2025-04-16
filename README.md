#  Conversational Analytics with Google Gemini & Streamlit

An intelligent, user-friendly analytics tool that leverages the power of Google Gemini and natural language processing to generate SQL queries from everyday English. Perfect for non-technical users looking to explore and visualize their customer data effortlessly.

##  Project Overview

This project bridges the gap between complex database querying and business users who prefer intuitive interfaces. Using Google's Gemini 2.0 Flash model, users can ask natural language questions like:

> "How many customers are from New York?"

And instantly get SQL results, charts, or summaries without writing a single line of code.


Our project demonstrates this transformation by combining:
-  **LLMs (Large Language Models)** for SQL generation
-  **Streamlit & Plotly** for rich interactive visualizations
-  **SQLite** for a local, easy-to-use database
-  Real-world customer data for business context

##  Features

-  **Conversational Interface** for generating SQL
-  Tabular data view with filters
-  Multiple Chart Types (Bar, Line, Pie, Area, Histogram)
-  Smart Summarization of analytics
-  Local SQLite DB integration
-  Environment-based API security (.env for Gemini Key)

##  Technologies Used

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Plotly](https://plotly.com/)
- [SQLite](https://sqlite.org/index.html)
- Python Standard Libraries (`os`, `dotenv`, `sqlite3`, `csv`, `pandas`)

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Revellabs_project1
```

### 2. Set up Virtual Environment (Optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google API Key
Create a `.env` file in the project root and add your Gemini API key:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Load the Dataset
Update the path in `sql.py` to match your CSV location and run:
```bash
python sql.py
```

### 6. Run the App
```bash
streamlit run app.py
```

##  Project Structure

```
Revellabs_project1/
├── app.py               # Main Streamlit app
├── sql.py               # Script to create and populate the SQLite database
├── .env                 # Environment variables (not committed)
├── .gitignore           # Ignore environment files and DB
├── database.db          # SQLite database (created at runtime)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

##  Example Prompts

- How many customers are from Canada?
- Show number of customers by segment.
- Total customers in each country.
- What is the most common city?

##  Sample Chart

After asking "How many customers per segment?", you can visualize:
- Bar Chart of Segment vs Count
- Pie Chart of Segment distribution
- Summary like "Total Customers: X", "Top Segment: Consumer"
