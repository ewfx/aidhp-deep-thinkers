import streamlit as st
from data.data_loader import load_personas

def login_page():
    """
    Displays the login page and handles user authentication.

    Args:
        personas (pd.DataFrame): DataFrame containing user information (user_id, email, password, etc.).

    Returns:
        str: The authenticated user's ID if login is successful, otherwise None.
    """
    personas = load_personas()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.title("🔐 Financial Buddy")
        st.markdown("Welcome to Financial Buddy! Please login to continue.")
        login_id = st.text_input("Enter User ID or Email")
        login_pw = st.text_input("Enter Password", type="password")
    
        if st.button("Login"):
            # Check if the user exists in the personas DataFrame
            user_row = personas[(personas["user_id"] == login_id) | (personas["email"] == login_id)]
            if not user_row.empty and user_row.iloc[0]["password"] == login_pw:
                st.success("Login successful!")
                return user_row.iloc[0]["user_id"]  # Return the authenticated user ID
            else:
                st.error("Invalid credentials. Please try again.")
    
    with col2:
        st.title("👋 Guest User, Chat with us!")
        if st.button("Chat"):
            st.session_state.current_page = "profile_edit"
    return None  # Return None if login is not successful