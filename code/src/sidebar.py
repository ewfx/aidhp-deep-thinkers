import streamlit as st 

def sidebar(profile):
    """
    Renders the sidebar for the application.

    Args:
        profile (pd.Series): The user's profile containing details like name.
    """
    st.markdown(f"### 👋 Hello, {profile['name']}")
    if st.button("🚪 Logout"):
        del st.session_state.user_id
        del st.session_state.current_page
        st.rerun()