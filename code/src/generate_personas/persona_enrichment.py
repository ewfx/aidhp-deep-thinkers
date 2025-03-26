from collections import Counter
from generate_sentiment_intent.sentiment_intent_pipeline import analyze_text
import streamlit as st

def enrich_persona_from_posts(profile, top_n_intents=3):
    """
    Analyze posts and enrich a user's profile with:
    - dominant sentiment
    - top N aggregated intents
    """
    if "posts" not in profile or not profile["posts"]:
        return profile

    all_intents = []
    all_sentiments = []

    for post in profile["posts"]:
        result = analyze_text(post)
        if result :
            all_intents.extend(result["intents"])
            all_sentiments.append(result["sentiment"])

    intent_counts = Counter(all_intents)
    top_intents = [intent for intent, _ in intent_counts.most_common(top_n_intents)]

    sentiment_counts = Counter(all_sentiments)
    dominant_sentiment = sentiment_counts.most_common(1)[0][0]

    profile["interests"] = top_intents
    profile["sentiment"] = dominant_sentiment
    profile["derived_intents"] = top_intents
    profile["derived_sentiment"] = dominant_sentiment

    return profile

def view_enriched_persona(profile):
    """
    Display an enriched user persona in Streamlit
    """
    st.subheader("🔎 Enriched Persona View")

    if "last_text_input" in profile:
        st.markdown(f"**Last Text Analyzed:** _{profile['last_text_input']}_")

    st.markdown(f"**Derived Intents:** `{', '.join(profile.get('derived_intents', []))}`")
    st.markdown(f"**Derived Sentiment:** `{profile.get('derived_sentiment', 'N/A')}`")

    st.divider()

    st.markdown("### Persona Snapshot")
    st.markdown(f"**Name:** {profile['name']}")
    st.markdown(f"**Age:** {profile['age']} | **Profession:** {profile['profession']}")
    st.markdown(f"**Income:** ₹{profile['income']:,}")
    st.markdown(f"**Risk Appetite:** {profile['risk_appetite']}")
    # st.markdown(f"**Investment Style:** {profile['investment_style']}")
    st.markdown(f"**Financial Goals:** {', '.join(profile['financial_goals'])}")
