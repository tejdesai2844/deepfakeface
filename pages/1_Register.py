# pages/1_Register.py
import streamlit as st
import re
import time
import db  # Import our database utility file
import sqlite3

st.set_page_config(page_title="Register", page_icon="📝")

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

# --- Logout Button in Sidebar ---
if st.session_state.get('logged_in') and st.session_state.user_info:
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

st.markdown('<div class="register-header"><h1>📝 Create Your Account</h1></div>', unsafe_allow_html=True)

if st.session_state.get('logged_in'):
    st.warning("You are already logged in. Please log out to register a new account.")
else:
    with st.form("register_form"):
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email Address", placeholder="your@email.com")
            password = st.text_input("Password", type="password", help="Minimum 8 characters, with uppercase, lowercase, numbers, and symbols.")
        with col2:
            city = st.text_input("City", placeholder="New York")
            mobile = st.text_input("Mobile Number", placeholder="+1234567890")
            confirm_password = st.text_input("Confirm Password", type="password")
        
        # Password strength indicator
        if password:
            strength_score = 0
            if len(password) >= 8: strength_score += 20
            if re.search(r'[A-Z]', password): strength_score += 20
            if re.search(r'[a-z]', password): strength_score += 20
            if re.search(r'\d', password): strength_score += 20
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): strength_score += 20
            
            strength_text, strength_class, strength_color = "Very Weak", "strength-very-weak", "#c62828"
            if strength_score == 40: strength_text, strength_class, strength_color = "Weak", "strength-weak", "#ef6c00"
            elif strength_score == 60: strength_text, strength_class, strength_color = "Medium", "strength-medium", "#ef6c00"
            elif strength_score >= 80: strength_text, strength_class, strength_color = "Strong", "strength-strong", "#2e7d32"
            
            st.markdown(f'<div class="password-strength {strength_class}">Password Strength: {strength_text}</div>'
                        f'<div class="progress-bar"><div class="progress-fill" style="width: {strength_score}%; background: {strength_color};"></div></div>', 
                        unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submitted:
            error_messages = []
            is_valid = True
            
            # Detailed Validation
            if not name or len(name.strip()) < 2 or not name.replace(" ", "").isalpha():
                error_messages.append("❌ Name must be at least 2 characters and contain only letters.")
                is_valid = False
            if not city or len(city.strip()) < 2 or not city.replace(" ", "").isalpha():
                error_messages.append("❌ City must be at least 2 characters and contain only letters.")
                is_valid = False
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                error_messages.append("❌ Please enter a valid email address.")
                is_valid = False
            if not re.match(r'^[\+]?[\d\s-]{10,15}$', mobile):
                error_messages.append("❌ Please enter a valid mobile number (at least 10 digits).")
                is_valid = False
            if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                error_messages.append("❌ Password must be 8+ chars with upper, lower, number, and symbol.")
                is_valid = False
            if password != confirm_password:
                error_messages.append("❌ Passwords do not match.")
                is_valid = False

            if not is_valid:
                for error in error_messages:
                    st.error(error)
            else:
                with st.spinner("Creating your account..."):
                    try:
                        db.insert_user(name.strip(), city.strip(), email.strip().lower(), mobile.strip(), password)
                        # Store registration data in session state for auto-fill
                        st.session_state.registration_email = email.strip().lower()
                        st.session_state.registration_password = password
                        st.success("🎉 Account created successfully! Redirecting to Login page...")
                        time.sleep(2)
                        st.switch_page("pages/2_Login.py")
                    except sqlite3.IntegrityError:
                        st.error("❌ This email is already registered. Please use a different email or log in.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")
