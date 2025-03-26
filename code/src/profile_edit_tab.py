import streamlit as st
import json
import os
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
PERSONAS_FILE = os.path.join(BASE_DIR, "code", "src", "generate_personas", "user_personas_with_posts.json")

def load_personas():
    with open(PERSONAS_FILE, "r") as f:
        return json.load(f)

def save_personas(personas):
    with open(PERSONAS_FILE, "w") as f:
        json.dump(personas, f, indent=4)

def render_profile_edit_tab(profile):
    personas = load_personas()
    def save_profile(user_profile):
        for i, persona in enumerate(personas):
            if persona["user_id"] == st.session_state.user_id:
                personas[i] = user_profile
                break
        save_personas(personas)
        st.success("Profile updated successfully!")
    
    user_profile = profile.to_dict()
    
    if user_profile is not None:
        st.subheader("Edit Your Profile")
        
        with st.form(key="profile_edit_form"):
            # Editable fields
            user_profile["name"] = st.text_input("Name", user_profile["name"])
            user_profile["age"] = st.number_input("Age", value=user_profile["age"], min_value=18, max_value=100)
            user_profile["profession"] = st.text_input("Profession", user_profile["profession"])
            user_profile["income"] = st.number_input("Income", user_profile["income"], step=10000)
            user_profile["risk_appetite"] = st.selectbox("Risk Appetite", ["Low", "Moderate", "High"], index=["Low", "Moderate", "High"].index(user_profile["risk_appetite"]))
            user_profile["financial_goals"] = st.text_area("Financial Goals (comma separated)", ", ".join(user_profile["financial_goals"])).split(", ")

            submitted = st.form_submit_button("Save Changes", on_click=save_profile, args=(user_profile,))        

            if submitted:
                st.rerun()
            # Save Button
            # st.button("Save Changes", on_click=save_profile, args=(user_profile,), key="save_profile")
    else:
        st.warning("User profile not found.")
