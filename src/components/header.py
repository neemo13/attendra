import streamlit as st

def header_home():

    st.markdown("<br>", unsafe_allow_html=True)

    # CENTERED COLUMN LAYOUT (REAL STREAMLIT WAY)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.image("src/ui/logo.jpg", width=300)

        st.markdown(
            '<h1 class="main-title">ATTENDRA</h1>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p class="subtitle">
                AI Powered Attendance System
            </p>
            """,
            unsafe_allow_html=True
        )