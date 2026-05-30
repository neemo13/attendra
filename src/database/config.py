# src/database/config.py
import streamlit as st
from supabase import create_client, Client

# Fetch keys individually (Ensure keys match the capitalization in your secrets.toml!)
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]

# Initialize the global client instance
supabase: Client = create_client(url, key)