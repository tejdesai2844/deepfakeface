# Home.py
import streamlit as st
import time

st.set_page_config(
    page_title="DeepFake Detector",
    page_icon="🤖",
    layout="wide"
)

# Global, modern, consistent CSS for all pages
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #f7f8fa !important;
    color: #222 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%) !important;
    border-right: 2px solid #667eea !important;
    box-shadow: 4px 0 24px rgba(102,126,234,0.08) !important;
}
[data-testid="stSidebarNav"] a {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff !important;
    border-radius: 12px;
    padding: 12px 20px;
    margin: 8px 0;
    font-weight: 600;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
    transition: all 0.3s;
    display: block;
    text-align: center;
    text-decoration: none !important;
    border: none;
    outline: none;
}
[data-testid="stSidebarNav"] a:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    color: #fff !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: #fff !important;
    font-weight: 700;
    transform: scale(1.06);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.25);
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border: none;
    border-radius: 25px;
    padding: 14px 36px;
    font-weight: 600;
    font-size: 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    transition: all 0.3s;
    margin: 10px 0;
    cursor: pointer;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.18);
}
.stButton > button:active {
    transform: translateY(-1px) scale(0.98);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.12);
}
.stTextInput > div > div > input, .stTextArea > div > textarea {
    border-radius: 10px !important;
    border: 2px solid #e0e0e0 !important;
    padding: 12px 15px !important;
    font-size: 16px !important;
    transition: all 0.3s !important;
    background: #fff !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.12) !important;
    outline: none !important;
}
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #5f4bb6 !important;
    letter-spacing: 1px;
}
h1 {
    font-size: 2.5rem !important;
    margin-bottom: 1.2rem !important;
}
h2 {
    font-size: 2rem !important;
    margin-bottom: 1rem !important;
}
h3 {
    font-size: 1.3rem !important;
    margin-bottom: 0.8rem !important;
}
.stAlert, .stDataFrame, .stImage, .stFileUploader, .stSelectbox, .stForm, .stForm > div {
    border-radius: 15px !important;
    box-shadow: 0 4px 24px rgba(102, 126, 234, 0.07) !important;
    background: #fff !important;
    padding: 1.2rem !important;
}
.stMarkdown {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
.stAlert {
    border: none !important;
    font-size: 1rem !important;
}
@media (max-width: 768px) {
    .stButton > button {
        padding: 10px 18px !important;
        font-size: 14px !important;
    }
    [data-testid="stSidebarNav"] a {
        padding: 10px 12px !important;
        font-size: 13px !important;
    }
    h1 {
        font-size: 2rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
# This ensures that the session state variables are set only once.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.is_admin = False
    st.session_state.user_info = None

# --- Logout Button in Sidebar ---
# This will be displayed on all pages if the user is logged in.
if st.session_state.logged_in and st.session_state.user_info:
    st.sidebar.markdown("---")  # Add separator
    st.sidebar.markdown(f"**Welcome, {st.session_state.user_info['name']}!**")
    st.sidebar.markdown("---")  # Add separator
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user_info = None
        st.success("You have been logged out. Redirecting to home page...")
        time.sleep(1)
        st.switch_page("app.py") # Redirect to main app page

# --- Main Home Page Content ---
st.title("🤖 DeepFake Face Detection")

st.markdown("""
In today's digital world, it's becoming harder to tell real from fake—especially with the rise of **AI-generated faces**.  
Our *Deepfake Face Detection* tool is designed to help you uncover the truth behind facial images with just a click.

Powered by cutting-edge **machine learning models**, the system scans subtle patterns and inconsistencies in facial features that are often invisible to the human eye.  
Whether you're a **casual user**, **content creator**, or part of a **research or media team**, this tool offers a quick and reliable way to detect AI-generated (deepfake) faces.

### Use it to:
- 🧠 Explore how AI works  
- 🛡️ Protect yourself from misinformation  
- 🔍 Satisfy your curiosity  

**Deepfake detection made simple, smart, and secure.**
""")

st.info("Please **Register** a new account or **Login** using the navigation panel on the left to get started.")