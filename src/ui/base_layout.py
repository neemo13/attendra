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
    button[kind="tertiary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-tertiary"] {

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

    div.stButton > button[data-testid="baseButton-primary"] {
        background-color: #7C3AED !important;
        color: white !important;
    }

    /* SECONDARY = PINK (#EC4899) */
    div.stButton > button[data-testid="baseButton-secondary"] {
        background-color: #EC4899 !important;
        color: white !important;
    }   

    /* SECONDARY BUTTONS = PINK */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {

        background: #EC4899 !important;
    }
            
    /* TERTIARY BUTTONS = PINK */
    button[kind="tertiary"],
    button[data-testid="baseButton-tertiary"] {

        background: #000000 !important;
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
        
        /* Add this to your style_base_layout */
        /* ==========================================
        ATTENDRA DESIGN SYSTEM
        ========================================== */

        :root{
            --primary:#7C3AED;
            --secondary:#EC4899;
            --bg:#F3E8FF;
            --card:#FFFFFF;
            --text:#0F172A;
            --muted:#64748B;
            --border:#D8B4FE;
            --success:#22C55E;
            --danger:#EF4444;
        }


        /* SUBJECT CARDS */

        .subject-card{

            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            padding: 22px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 10px 25px rgba(124,58,237,0.08) !important;

            transition: all .2s ease !important;
        }

        .subject-card:hover{

            transform: translateY(-2px);

            box-shadow:
                0 14px 30px rgba(124,58,237,0.12) !important;
        }


        /* SUBJECT TYPOGRAPHY */

        .subject-title{

            font-size: 22px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 6px;
        }

        .subject-meta{

            font-size: 14px;
            color: var(--muted);
        }

        .subject-divider{

            border: none;
            border-top: 1px solid #F1F5F9;
            margin: 14px 0;
        }

        .subject-stat{

            font-size: 15px;
            color: #334155;
            font-weight: 500;
        }


        /* STATUS BADGES */

        .badge-success{

            background: #F0FDF4;
            color: #166534;
            border-left: 4px solid #22C55E;
            padding: 10px;
            border-radius: 10px;
            font-weight: 600;
        }

        .badge-danger{

            background: #FEF2F2;
            color: #B91C1C;
            border-left: 4px solid #EF4444;
            padding: 10px;
            border-radius: 10px;
            font-weight: 600;
        }


        /* SECTION TITLES */

        .control-title{

            font-size: 28px;
            font-weight: 700;
            color: var(--text);
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
    
    /* ======================================
   WHITE STREAMLIT CONTAINERS
   ====================================== */

    

    </style>
    """, unsafe_allow_html=True)