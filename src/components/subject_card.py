import streamlit as st

def subject_card(name, code, section, stats, footer_callback=None, edit_callback=None):
    with st.container(border=True):
        st.subheader(f"📖 {name}")
        st.caption(f"Code: {code} | Section: {section}")
        
        if isinstance(stats, dict) and stats:
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="🧑‍🎓 Students", value=stats.get("students", 0))
            with c2:
                st.metric(label="📚 Classes", value=stats.get("classes", 0))
        else:
            st.info("No stats available.")
            
        # Footer section for actions
        if footer_callback or edit_callback:
            st.divider()
            b1, b2 = st.columns(2)
            
            if footer_callback:
                with b1:
                    if st.button("Share", key=f"share_{code}", icon=":material/share:", use_container_width=True):
                        footer_callback()
            
            if edit_callback:
                with b2:
                    # Hide Edit button for guests
                    if not st.session_state.get('is_guest', False):
                        if st.button("Edit", key=f"edit_{code}", icon=":material/edit:", use_container_width=True):
                            edit_callback()
                    else:
                        st.button("Edit", key=f"edit_disabled_{code}", disabled=True, use_container_width=True)