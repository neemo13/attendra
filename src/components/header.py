import streamlit as st


def header_home():

    st.markdown(
        "<div style='height:30px'></div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        try:
            st.image("src/ui/logo.jpg", width=300)
        except:
            pass

        st.markdown(
            '<h1 class="main-title">ATTENDRA</h1>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="subtitle">AI Powered Attendance System</p>',
            unsafe_allow_html=True
        )


def header_dashboard(role="Teacher"):

    col1, col2, col3 = st.columns([0.8,5.2,2])

    with col1:

        try:
            st.image("src/ui/logo.jpg", width=55)
        except:
            pass

    with col2:

        st.markdown(
            f'''
            <div class="portal-title">
                ATTENDRA
                <span class="portal-subtitle">
                    | {role} Portal
                </span>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col3:

        if st.button(
            "Go Back Home",
            type="secondary",
            use_container_width=True,
            key="go_home"
        ):

            st.session_state["login_type"] = None
            st.rerun()