import streamlit as st
import os
from generate_sentiment_intent.llm_post_to_product import post_to_product
from generate_sentiment_intent.sentiment_intent.llm_based_intents import posts_to_intents
from generate_sentiment_intent.sentiment_intent.llm_similarity_embedding import get_similar_intents_with_scores
from generate_sentiment_intent.sentiment_intent.sentiment_detection import get_sentiment

def render_posts_to_recommendation_tab():
    """
    Shows how we use posts and their sentiment to recommendation.

    It's an interactive build
    """
      # Streamlit UI
    st.title("🔍Posts Recommendation")
    user_input = st.text_area("Tell us how are you feeling today:")

    if st.button("Show Recommendation") and user_input:
        primary_recommendations, exploratory_recommendations , mood, primary_intents, secondary_intents = post_to_product(user_input)
        # primary_intents = posts_to_intents(user_input)
        # similar_with_scores = get_similar_intents_with_scores(primary_intents)
        # mood = get_sentiment(user_input, primary_intents)

        mood_emoji = "😊" if mood == "positive" else "😟" if mood == "negative" else "😐"

        st.subheader(f"🎯 We see the overall mood is {mood_emoji}")

        st.subheader("🎯 Recommendations")
        for recommendation in primary_recommendations:
            st.markdown(f"**{recommendation['title']}**")
            st.write(recommendation['desc'])
        st.write("🔸 As you intends this -")
        st.write(", ".join(primary_intents))

        st.subheader("🎯 You should explore this too -")
        for recommendation in exploratory_recommendations:
            st.markdown(f"**{recommendation['title']}**")
            st.write(recommendation['desc'])
        st.write("🔸 You might be intending this as well -")
        st.write(",".join(secondary_intents))
        # st.write(", ".join(similar_with_scores.keys()))

    if st.button("Back To Login"):
        st.session_state.current_page = "login"


