import streamlit as st
from src.database.db import hash_pass, check_pass, supabase

def account_settings_ui(user_data, role):
    if st.session_state.get('is_guest', False):
        st.sidebar.info("⚙️ Account Settings are disabled in Guest Mode.")
        return
    
    with st.sidebar:
        with st.expander("⚙️ Account Settings"):
            with st.form("change_pwd_form"):
                st.subheader("Change Password")
                current_pwd = st.text_input("Current Password", type="password")
                new_pwd = st.text_input("New Password", type="password")
                confirm_pwd = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    if new_pwd != confirm_pwd:
                        st.error("Passwords do not match!")
                    elif not check_pass(current_pwd, user_data['password']):
                        st.error("Incorrect current password.")
                    else:
                        # Update logic
                        table = "students" if role == "student" else "teachers"
                        id_col = "student_id" if role == "student" else "teacher_id"
                        
                        hashed = hash_pass(new_pwd)
                        supabase.table(table).update({"password": hashed}).eq(id_col, user_data[id_col]).execute()
                        st.success("Password updated!")