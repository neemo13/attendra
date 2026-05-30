import streamlit as st


def style_base_layout():

    st.markdown("""
    <style>

    /* HIDE STREAMLIT UI */
    #MainMenu,
    footer,
    header,
    .stAppHeader {
        visibility: hidden !important;
        display: none !important;
    }

    /* IMPORTANT: REMOVE NEGATIVE MARGIN */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        margin-top: 0rem !important;
    }

    /* FONT */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html,
    body,
    .stApp,
    p,
    label,
    h1,
    h2,
    h3 {
        font-family: 'Outfit', sans-serif !important;
    }

    /* BUTTON BASE */
    /* ALL BUTTONS */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"] {

        border-radius: 1.5rem !important;

        padding: 14px 28px !important;

        font-size: 18px !important;

        font-weight: 700 !important;

        border: none !important;

        transition: all 0.25s ease !important;

        color: white !important;
    }


    /* PRIMARY BUTTONS = PURPLE */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {

        background: #7C3AED !important;
    }


    /* SECONDARY BUTTONS = PINK */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {

        background: #EC4899 !important;
    }


    /* HOVER */
    .stButton > button:hover {

        transform: scale(1.03) !important;

        filter: brightness(1.08) !important;
    }
    div[data-testid="stTabs"] button p {
            color: #000000 !important;
            font-weight: bold !important;
        }

        h1, h2, h3 {
            color: #000000 !important;
        }

        /* TAB TEXT */
        div[data-testid="stTabs"] button p {
            color: #000000 !important;
            font-weight: bold !important;
        }

        /* HEADINGS */
        h1, h2, h3 {
            color: #000000 !important;
        }

        /* CAMERA BUTTON */
        div[data-testid="stCameraInput"] button,
        div[data-testid="stCameraInput"] button:hover,
        div[data-testid="stCameraInput"] button:focus,
        div[data-testid="stCameraInput"] button:active {

            background-color: #7C3AED !important;

            color: white !important;

            border-radius: 1.5rem !important;

            border: none !important;

            font-size: 18px !important;

            font-weight: 700 !important;

            padding: 14px 28px !important;

            box-shadow: none !important;
        }

        /* BUTTON TEXT */
        div[data-testid="stCameraInput"] button p,
        div[data-testid="stCameraInput"] button span {

            color: white !important;

            font-weight: 700 !important;
        }

        /* CAMERA WRAPPER */
        div[data-testid="stCameraInput"] {

            border-radius: 1.2rem !important;

            overflow: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)


def style_background_home():

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #F3E8FF, #E9D5FF) !important;
    }

    /* SMALLER TITLE */
    .main-title {

        font-size: 38px !important;

        font-weight: 800 !important;

        text-align: center !important;

        color: #0F172A !important;

        margin-top: 10px !important;

        margin-bottom: 0px !important;

        line-height: 1.1 !important;
    }

    /* SUBTITLE */
    .subtitle {

        text-align: center !important;

        font-size: 19px !important;

        font-weight: 600 !important;

        color: #475569 !important;

        margin-top: 6px !important;

        margin-bottom: 25px !important;
    }

    </style>
    """, unsafe_allow_html=True)


def style_base_dashboard():

    st.markdown("""
    <style>

    .stApp {
        background: #F3E8FF !important;
    }

    /* TOP PADDING FIX */
    .block-container {
        padding-top: 3rem !important;
    }

    .portal-title {

        font-size: 22px !important;

        font-weight: 700 !important;

        color: #1E293B !important;

        padding-top: 8px !important;
    }

    .portal-subtitle {

        font-size: 14px !important;

        color: #64748B !important;
    }

    </style>
    """, unsafe_allow_html=True)