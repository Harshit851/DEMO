import streamlit as st
import pandas as pd
from Api_Sql_Gemini import get_table_info, generate_sql_query, run_query
import base64

# --- Page Config ---
st.set_page_config(page_title="Chat Interface_Streamlit | SB", layout="wide")

# --- Apply Background Images ---
def add_bg_from_local(main_bg, sidebar_bg):
    main_bg_ext = "jpg"
    sidebar_bg_ext = "jpg"

    with open(main_bg, "rb") as image_file:
        main_bg_base64 = base64.b64encode(image_file.read()).decode()
    with open(sidebar_bg, "rb") as image_file:
        sidebar_bg_base64 = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/{main_bg_ext};base64,{main_bg_base64}");
            background-size: cover;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/{sidebar_bg_ext};base64,{sidebar_bg_base64}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)

add_bg_from_local("bg_main.jpg", "bg_sidebar.jpg")

# --- Initialize History State ---
if "history" not in st.session_state:
    st.session_state.history = []
if "sql_query" not in st.session_state:
    st.session_state.sql_query = ""
if "query_result" not in st.session_state:
    st.session_state.query_result = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("## **⚙️ App Settings**")

    st.markdown("### 🧠 Query History")
    if st.session_state.history:
        for i, (q, s) in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"🕘 Query {i}"):
                st.markdown(f"**Q:** {q}")
                st.code(s, language="sql")
    else:
        st.info("No queries yet!")

    st.markdown("---")
    if st.checkbox("🔐 Show Gemini API Key"):
        st.code("SHUBH-API key", language="text")
    else:
        st.text("🔐 Gemini API Key: Hidden")

    st.markdown("---")
    selected_member = st.selectbox(
        "👥 Team Members",
        ["Mandakini Srivastava", "Navansh Mishra", "Shubh Bhardwaj (TL)"]
    )

# --- Main Content ---
st.title("💬 Interactive Chat Interface")
st.caption("Powered by Gemini AI | SSMS | SB")

st.header("Ask Anything about Transaction Data")
user_input = st.text_input("🔍 What would you like to know?", key="user_question")

# --- Buttons ---
col1, col2 = st.columns([1, 1])
with col1:
    run_clicked = st.button("▶️ Run Query")
with col2:
    clear_clicked = st.button("🧹 Clear Chat")

# --- Feedback Slider ---
st.markdown("### ⭐ Rate Your Experience")
rating = st.select_slider('Rate us:', ['', 'Bad', 'Good', 'Excellent'], label_visibility="visible")

if rating and rating != '':
    st.success("✅ Thanks for your valuable feedback!!")

# --- Run Query Logic ---
if run_clicked and user_input.strip():
    with st.spinner("⏳ SB AI is thinking..."):
        df_sample = get_table_info()
        sql = generate_sql_query(user_input, df_sample)
        st.session_state.sql_query = sql
        st.session_state.query_result = run_query(sql)
        st.session_state.history.append((user_input, sql))  # Save to history
    st.success("✅ Query executed successfully!")

# --- Clear Chat Logic ---
if clear_clicked:
    st.session_state.sql_query = ""
    st.session_state.query_result = None
    st.session_state.user_question = ""
    st.warning("⚠️ Chat cleared!")

# --- Progress bar if loading ---
if run_clicked:
    import time
    progress = st.progress(0)
    for percent in range(1, 101):
        time.sleep(0.005)
        progress.progress(percent)

# --- Show Output ---
if st.session_state.sql_query:
    st.subheader("🧠 Gemini Generated SQL")
    st.code(st.session_state.sql_query, language="sql")

if isinstance(st.session_state.query_result, pd.DataFrame):
    st.subheader("📊 Query Result")
    st.dataframe(st.session_state.query_result)
elif isinstance(st.session_state.query_result, str):
    st.error(st.session_state.query_result)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 | Created by Team | Streamlit + Gemini + SSMS_SQL Server | SB")
