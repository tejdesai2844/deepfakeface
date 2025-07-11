# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
import cv2
import numpy as np
import joblib
import time
from tensorflow.keras.models import load_model
import db # Import our database utility file

st.set_page_config(page_title="Dashboard", page_icon="📊")

# Enhanced CSS for beautiful buttons and dashboard styling
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

# --- Model Loading with Caching ---
# This ensures the models are loaded only once, improving performance.
@st.cache_resource
def load_prediction_models():
    """Load the trained model and label encoder."""
    try:
        model = load_model('trained_model.h5')
        label_encoder = joblib.load('label_encoder.pkl')
        return model, label_encoder
    except Exception as e:
        st.error(f"Error loading models: {e}. Please ensure 'trained_model.h5' and 'label_encoder.pkl' are in the root directory.")
        return None, None

model, label_encoder = load_prediction_models()

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

# --- Page Protection ---
if not st.session_state.get('logged_in'):
    st.error("🔒 You must be logged in to access the dashboard.")
    st.info("Please navigate to the Login page from the sidebar.")
else:
    # --- Admin Dashboard ---
    if st.session_state.get('is_admin'):
        st.title("📊 Admin Panel - User Management")
        
        st.subheader("All Registered Users")
        user_result = db.view_all_users()
        if user_result:
            clean_db = pd.DataFrame(user_result, columns=["ID", "Name", "City", "Email", "Mobile"])
            st.dataframe(clean_db, use_container_width=True)
        else:
            st.info("No users registered yet.")
            
        st.subheader("Delete a User")
        email_to_delete = st.selectbox("Select user email to delete", [row[3] for row in user_result] if user_result else [])
        if st.button("Delete User", type="primary"):
            if email_to_delete:
                db.delete_user(email_to_delete)
                st.success(f"User with email '{email_to_delete}' has been deleted.")
                st.rerun()
            else:
                st.warning("Please select a user to delete.")

    # --- User Dashboard ---
    else:
        st.title("🤖 DeepFake Detection Dashboard")
        st.write(f"Welcome, **{st.session_state.user_info['name']}**! Upload an image to check if it's real or a deepfake.")

        uploaded_file = st.file_uploader("Choose a face image...", type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", width=256)
            
            # Prediction button
            if st.button("Analyze Image"):
                if model and label_encoder:
                    with st.spinner("Analyzing..."):
                        # Preprocess the image
                        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                        img = cv2.imdecode(file_bytes, 1)
                        img = cv2.resize(img, (64, 64))
                        img_array = img.astype('float32') / 255
                        img_array = np.expand_dims(img_array, axis=0)

                        # Make prediction
                        prediction = model.predict(img_array)
                        predicted_index = np.argmax(prediction, axis=1)[0]
                        predicted_label = label_encoder.inverse_transform([predicted_index])[0]
                        
                        confidence = np.max(prediction) * 100
                        
                        st.subheader("Analysis Result")
                        if predicted_label.lower() == 'real':
                            st.success(f"✅ The image is likely **Real** (Confidence: {confidence:.2f}%)")
                        else:
                            st.error(f"❌ The image is likely a **DeepFake** (Confidence: {confidence:.2f}%)")
                else:
                    st.error("Models are not loaded. Cannot perform analysis.")