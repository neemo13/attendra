import streamlit as st


def header_home():
    st.markdown(
        "<div style='height:30px'></div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        try:
            st.image("src/ui/logo.jpg", width=300)
        except:
            pass

        st.markdown(
            '<h1 style="text-align:center;color:#7C3AED;font-weight:800;">ATTENDRA</h1>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="text-align:center;color:#6B7280;">AI Powered Attendance System</p>',
            unsafe_allow_html=True
        )

def header_dashboard(role="Teacher"):

    st.markdown("""
    <style>

    .portal-brand {
        font-size: 28px;
        font-weight: 800;
        color: #7C3AED;
        line-height: 1;
    }

    .portal-role {
        font-size: 14px;
        color: #EC4899;
        font-weight: 700;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }

    </style>
    """, unsafe_allow_html=True)

    in_dashboard = (
        st.session_state.get("teacher_mode") == "dashboard"
        or st.session_state.get("is_logged_in") is True
    )

    button_label = (
        "Logout"
        if in_dashboard
        else "Go Back Home"
    )

    col1, col2, col3 = st.columns([0.8, 5, 1.8])

    with col1:
        try:
            st.image(
                "src/ui/logo.jpg",
                width=60
            )
        except:
            pass

    with col2:

        st.markdown(
            f"""
            <div class="portal-brand">
                ATTENDRA
            </div>

            <div class="portal-role">
                {role.upper()} PORTAL
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        if st.button(
            button_label,
            key="nav_button",
            use_container_width=True
        ):

            if in_dashboard:

                st.session_state.clear()

            else:

                st.session_state["login_type"] = None
                st.session_state["teacher_mode"] = "register"
                st.session_state["is_logged_in"] = False

                st.session_state.pop(
                    "current_teacher",
                    None
                )

                st.session_state.pop(
                    "student_data",
                    None
                )

            st.rerun()

    st.divider()