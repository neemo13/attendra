import streamlit as st
import numpy as np
from src.database.config import supabase
from src.database.db import format_attendance_log
from src.pipelines.voice_pipeline import process_bulk_audio

@st.dialog('Voice Attendance')
def voice_attendance_dialog(subject_id):
    st.write('Record audio to identify students.')
    audio_data = st.audio_input("Record classroom audio")

    if audio_data and st.button('Analyze & Add to Queue', type='primary'):
        with st.spinner('Processing...'):

            # 1. GUEST MODE INTERCEPTION
            if st.session_state.get('is_guest'):
                # Simulate analysis delay
                import time
                time.sleep(2)
                
                # Manually add the "Demo" students to the queue
                demo_students = ["123", "456"]
                for sid in demo_students:
                    already_in_queue = any(item['student_id'] == sid for item in st.session_state.attendance_master_queue)
                    if not already_in_queue:
                        new_log = format_attendance_log(sid, subject_id, True, source='Voice (Demo)')
                        st.session_state.attendance_master_queue.append(new_log)
                
                st.toast("Demo Mode: Audio processed and students added!")

            else:
                # Fetch candidates
                enrolled = supabase.table('subject_students')\
                    .select("student_id, students(voice_embedding)")\
                    .eq('subject_id', subject_id).execute().data
                
                candidates = {s['student_id']: np.array(s['students']['voice_embedding']) 
                            for s in enrolled if s['students'] and s['students'].get('voice_embedding')}
                
                # Get matches (now distance-based)
                scores = process_bulk_audio(audio_data.read(), candidates, threshold=0.4)
                matched_ids = set(scores.keys())
                
                # Append matches to the queue in session state
                for s in enrolled:
                    sid = s['student_id']
                    is_present = sid in matched_ids
                    
                    # Check for existing logs to prevent duplicates
                    already_in_queue = any(item['student_id'] == sid for item in st.session_state.attendance_master_queue)
                    
                    if not already_in_queue:
                        new_log = format_attendance_log(sid, subject_id, is_present, source='Voice')
                        st.session_state.attendance_master_queue.append(new_log)
                
                st.success("Successfully added to attendance queue!")
            st.session_state.active_dialog = None
            st.rerun() # This triggers the main UI to refresh and show the table