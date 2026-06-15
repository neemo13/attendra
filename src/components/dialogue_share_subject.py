import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialogue(subject_name, subject_code):
    app_domain = "http://localhost:8501"
    # Assuming the join URL structure includes the subject_code
    join_url = f"{app_domain}/join/{subject_code}"

    st.header(f"Share {subject_name}")
    st.write(f"Students can join **{subject_name}** by scanning this code or using the link below.")

    # Generate QR Code
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.info("Copy this link to share via WhatsApp or Email.")

    with col2:
        st.markdown("### Scan to Join")
        # Change use_column_width=True to use_container_width=True
        st.image(out.getvalue(), use_container_width=True, caption=f"QR for {subject_code}")

    # Add a close button
    if st.button("Close", use_container_width=True):
        st.session_state.active_dialog = None
        st.rerun()