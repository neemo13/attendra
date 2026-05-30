import streamlit as st
import time
from src.ui.base_layout import style_base_layout, style_base_dashboard
from src.components.header import header_dashboard

# 🚀 IMPORT YOUR DATABASE UTILITIES HERE
from src.database.db import check_teacher_exist, create_teacher, teacher_login

def teacher_screen():
    style_base_dashboard()
    style_base_layout()
    header_dashboard(role="Teacher")

    if "teacher_mode" not in st.session_state:
        st.session_state["teacher_mode"] = "register"

    # Route interface state panels depending on state settings
    if st.session_state["teacher_mode"] == "register":
        st.markdown("## Register your teacher profile")
        st.write("Fill in your details to create your account.")
        with st.container(border=True):
            teacher_screen_register()
            
    elif st.session_state["teacher_mode"] == "login":
        st.markdown("## Teacher Login")
        st.write("Welcome back! Please enter your details.")
        with st.container(border=True):
            teacher_screen_login()
            
    # 🚀 NEW STATE BRANCH: Renders the dashboard when logged in
    elif st.session_state["teacher_mode"] == "dashboard":
        teacher_dashboard()


def teacher_screen_register():
    # 1. Enclose ONLY the data fields and a single primary submission trigger inside the form
    with st.form("teacher_register_form", clear_on_submit=False):
        username = st.text_input("Username / Email Address", placeholder="Username / Email Address", key="reg_user")
        name = st.text_input("Full Name", placeholder="Full Name", key="reg_name")
        p1 = st.text_input("Password", placeholder="Password", type="password", key="reg_p1")
        p2 = st.text_input("Confirm Password", placeholder="Confirm Password", type="password", key="reg_p2")

        st.markdown("<br>", unsafe_allow_html=True)
        register = st.form_submit_button("Register Now", type="primary", use_container_width=True, icon=':material/passkey:')

    # 2. Place navigation toggles cleanly underneath the form boundary
    st.markdown("<p style='text-align: center; margin-top: 10px;'>Already have an account?</p>", unsafe_allow_html=True)
    if st.button("Login Instead", type="secondary", use_container_width=True, icon=':material/login:', key="nav_to_login"):
        st.session_state["teacher_mode"] = "login"
        st.rerun()

    # Form logical evaluations execution block
    if register:
        if not (username and name and p1 and p2):
            st.error("Please fill in all required fields.")
        elif p1 != p2:
            st.error("Passwords do not match. Please verify your typing.")
        else:
            try:
                if check_teacher_exist(username):
                    st.error("This username/email is already registered. Try logging in!")
                else:
                    create_teacher(username, p1, name)
                    st.success("Account created successfully! Switching to Login...")
                    st.session_state["teacher_mode"] = "login"
                    st.rerun()
            except Exception as e:
                st.error(f"Registration failed: {e}")


def teacher_screen_login():
    # 1. Primary data payload tracking components 
    with st.form("teacher_login_form", clear_on_submit=False):
        email = st.text_input("Username / Email Address", placeholder="Username / Email Address", key="log_user")
        password = st.text_input("Password", placeholder="Password", type="password", key="log_p1")

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Login", type="primary", use_container_width=True, icon=':material/passkey:')

    # 2. Redirect fallback button sitting outside the form scope
    st.markdown("<p style='text-align: center; margin-top: 10px;'>New to Attendra?</p>", unsafe_allow_html=True)
    if st.button("Create Account", type="secondary", use_container_width=True, icon=':material/person_add:', key="nav_to_reg"):
        st.session_state["teacher_mode"] = "register"
        st.rerun()

    if submit:
        if email and password:
            with st.spinner("Authenticating..."):
                teacher_profile = teacher_login(email, password)
            
            if teacher_profile:
                st.toast('Welcome back!', icon='👋')
                time.sleep(1)

                # Save user metrics safely inside the session context state
                st.session_state["current_teacher"] = teacher_profile
                st.session_state["login_type"] = "teacher"  
                
                # 🚀 CHANGED HERE: Shift the mode state explicitly to dashboard before rerunning!
                st.session_state["teacher_mode"] = "dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
        else:
            st.error("Invalid credentials input.")


def teacher_dashboard():
    # 🚀 ADJUSTED HERE: Safely extract profile from 'current_teacher' matches 
    if "current_teacher" in st.session_state:
        teacher_data = st.session_state["current_teacher"]
        st.header(f"Welcome, {teacher_data['name']}!")
        
        # Add a logout option for clean state management
        if st.sidebar.button("Log Out", icon=':material/logout:'):
            st.session_state["teacher_mode"] = "login"
            st.session_state.pop("current_teacher", None)
            st.rerun()
    else:
        st.error("No teacher profile data found. Please log in again.")
        st.session_state["teacher_mode"] = "login"
        st.rerun()