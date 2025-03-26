import streamlit as st

def render_social_media_activity_recommendation(all_recommendations):
    st.subheader("📢 Social Media-Based Recommendations")
    
    if not all_recommendations:
        st.info("No recommendations available at the moment.")
        return
    
    # Extract and display all primary and exploratory recommendations
    primary_recommendations = []
    exploratory_recommendations = []

    for rec in all_recommendations:
         # Handle cases where "primary" or "exploratory" might be None
        if rec.get("primary"):
            primary_recommendations.append(f"**{rec['primary'].get('title', 'Unknown')}**: {rec['primary'].get('desc', 'No description available')}")
        
        if rec.get("exploratory"):
            exploratory_recommendations.append(f"**{rec['exploratory'].get('title', 'Unknown')}**: {rec['exploratory'].get('desc', 'No description available')}")

    # Display Primary Recommendations
    st.subheader("🔹 Primary Recommendations")
    for primary in primary_recommendations:
        st.markdown(f"- {primary}")

    # Display Exploratory Recommendations
    st.subheader("🔸 You Can Explore These Too")
    for exploratory in exploratory_recommendations:
        st.markdown(f"- {exploratory}")
