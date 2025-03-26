import streamlit as st
from generate_personas.sentiment_analysis import analyze_sentiment
from data.data_loader import load_data
from data.data_loader import load_personas
from sidebar import sidebar
from profile_tab import render_profile_tab
from recommendation_tab import render_recommendation_tab
from model_insights_tab import render_model_insights_tab
from methodology_tab import render_methodology_tab
from profile_edit_tab import render_profile_edit_tab
from posts_to_recommendation import render_posts_to_recommendation_tab
from generate_sentiment_intent.llm_post_to_product import posts_to_products
from social_media_activity_render import render_social_media_activity_recommendation
import time

# Load data
products, content = load_data()
# User logged in
def main_page():
    selected_user_id = st.session_state.user_id
    personas = load_personas()
    profile = personas[personas.user_id == selected_user_id].iloc[0]

    start_time = time.time()
    all_recommendation, dominant_mood = posts_to_products(profile.get("posts"))
    sentiment_model_time = time.time() - start_time

    # Sidebar
    with st.sidebar:
        sidebar(profile)

    # Dashboard
    st.title("💡 FinanceGenAI Dashboard")
    # tabs = st.tabs(["User Profile", "Recommendations", "Model Insights", "Persona Enrichment", "Edit Profile", "Tell us how you feel", "Social Media Activity based Recommendation"])

    # tabs = st.tabs(["User Profile", "Recommendations", "Model Insights", "Edit Profile", "Tell us how you feel", "Social Media Activity based Recommendation"])
    tabs = st.tabs(["User Profile", "Recommendations", "Social Media Activity based Recommendation", "Tell us how you feel","Edit Profile", "Metrics "])

    # User Profile Tab
    with tabs[0]:
        # sentiment_label, sentiment_score = analyze_sentiment(selected_user_id)
        # render_profile_tab(profile, sentiment_label, sentiment_score)
        render_profile_tab(profile)

    # Recommendations Tab
    with tabs[1]:
        times = render_recommendation_tab(profile, selected_user_id, products, content, all_recommendation)
    # with tabs[3]:
    #     render_methodology_tab(profile)

    with tabs[2]:
        render_social_media_activity_recommendation(all_recommendation)
        
    with tabs[3]:
        render_posts_to_recommendation_tab()

    with tabs[4]:
        render_profile_edit_tab(profile)

    # Model Insights Tab
    with tabs[5]:
        render_model_insights_tab(times, sentiment_model_time)