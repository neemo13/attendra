import streamlit as st
from PIL import Image

@st.dialog("Capture or upload photos")
def add_photos_dialog(subject):
    st.write(f'Adding media for: **{subject["name"]}**')
    
    # Simple choice
    choice = st.radio("Method", ["Camera", "Upload"], horizontal=True)
    
    # We use a temporary list to buffer new images within this dialog session
    # to avoid re-triggering the append logic during reruns
    if "temp_new_images" not in st.session_state:
        st.session_state.temp_new_images = []

    if choice == "Camera":
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo and cam_photo not in st.session_state.temp_new_images:
            st.session_state.temp_new_images.append(cam_photo)
            st.toast("Photo captured and queued!")
            
    elif choice == "Upload":
        files = st.file_uploader("Upload images", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
        if files:
            for f in files:
                if f not in st.session_state.temp_new_images:
                    st.session_state.temp_new_images.append(f)
            st.toast(f"Added {len(files)} photos to queue.")

    # Show count of pending images
    st.info(f"Photos queued in this session: {len(st.session_state.temp_new_images)}")

    # The only button that matters
    if st.button("Finish & Return", type="primary", use_container_width=True):
        # Move temporary files to the permanent attendance_images list
        for f in st.session_state.temp_new_images:
            # Only add to the main list if not already present
            if f not in st.session_state.attendance_images:
                st.session_state.attendance_images.append(Image.open(f))
        
        # Clear temp buffer and close dialog
        st.session_state.temp_new_images = []
        st.session_state.active_dialog = None
        st.rerun()