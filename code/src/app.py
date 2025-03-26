import streamlit as st
st.set_page_config(page_title="FinanceGenAI", layout="wide")
import time
import os
import sys
from login_page import login_page
from main_page import main_page
# from profile_edit_tab import render_profile_edit_tab
from posts_to_recommendation import render_posts_to_recommendation_tab

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------- STREAMLIT APP ----------------
# Session state for login
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Login screen
if st.session_state.current_page == "login":
    authenticated_user_id = login_page()
    if authenticated_user_id:
        st.session_state.user_id = authenticated_user_id
        st.session_state.current_page = "main"
        st.rerun()  # Reload the app after successful login

elif st.session_state.current_page == "main":
    with st.spinner("Loading..."):
        time.sleep(15)
        main_page()
elif st.session_state.current_page == "profile_edit":
    render_posts_to_recommendation_tab()
      

