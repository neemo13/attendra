import streamlit as st


# =========================
# HOME PAGE STYLING
# =========================
def style_background_home():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

        <style>

            html, body, .stApp {
                font-family: 'Poppins', sans-serif;
            }

            .stApp{
                background: linear-gradient(135deg, #EEF2FF, #F8FAFC) !important;
                color: #1E293B;
            }

            .main-title{
                font-family: 'Montserrat', sans-serif !important;
                font-size: 64px;
                font-weight: 800;
                letter-spacing: 2px;
                color: #5865F2;
                text-align: center;
                margin-bottom: 10px;
            }

            .subtitle{
                text-align: center;
                font-size: 22px;
                color: #64748B;
                margin-top: -10px;
                margin-bottom: 20px;
            }

        </style>
    """, unsafe_allow_html=True)


# =========================
# DASHBOARD STYLING
# =========================
def style_base_dashboard():
    st.markdown("""
        <style>

            .stApp{
                background-color: #F5F7FF !important;
                color: #1E293B;
                font-family: 'Poppins', sans-serif;
            }

        </style>
    """, unsafe_allow_html=True)


# =========================
# BASE LAYOUT STYLING
# =========================
def style_base_layout():
    st.markdown("""
        <style>

            html, body, .stApp {
                font-family: 'Poppins', sans-serif;
            }

            .stApp{
                background-color: #EEF2FF !important;
                color: #1E293B;
            }

            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container{
                padding-top: 0.5rem;
            }

            h2 {
                font-size: 2.5rem !important;
                line-height: 1.2 !important;
                margin-bottom: 0 !important;
            }

            .stButton > button {
                border-radius: 1.5rem !important;
                padding: 10px 18px !important;
                font-weight: 600 !important;
                transition: transform 0.3s ease-in-out, background-color 0.3s ease !important;
            }

            /* PRIMARY */
            .stButton > button[kind="primary"] {
                background-color: #5865F2 !important;
                color: white !important;
                border: none !important;
            }

            .stButton > button[kind="primary"]:hover {
                background-color: #4752C4 !important;
            }

            /* SECONDARY */
            .stButton > button[kind="secondary"] {
                background-color: #E2E8F0 !important;
                color: #1E293B !important;
                border: none !important;
            }

            /* TERTIARY */
            .stButton > button[kind="tertiary"] {
                background-color: transparent !important;
                color: #5865F2 !important;
                border: 1px solid #5865F2 !important;
            }

            .stButton > button:hover {
                transform: scale(1.05) !important;
            }

        </style>
    """, unsafe_allow_html=True)