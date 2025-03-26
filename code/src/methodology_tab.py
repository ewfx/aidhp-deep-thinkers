import streamlit as st
from generate_personas.persona_enrichment import view_enriched_persona
from generate_recommendations.recommendation import recommend_by_intent_with_enrichment
from generate_sentiment_intent.sentiment_intent_pipeline import analyze_text
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
catalog_path = os.path.join(BASE_DIR, "data", "recommendable_products_catalog.csv")
intent_cooc_path = os.path.join(BASE_DIR, "data", "sentiment_data", "intent_cooccurrence_matrix.csv")
# Load required product catalog and intent co-occurrence matrix
catalog = pd.read_csv(catalog_path)
intent_cooc = pd.read_csv(intent_cooc_path)

def render_methodology_tab(profile):
    """
    Renders the Persona Enrichment tab in the Streamlit app.

    Args:
        profile (pd.Series): The user's profile containing details like intents and sentiment.
        intent_cooc (pd.DataFrame): DataFrame containing intent co-occurrence data.
        catalog (pd.DataFrame): DataFrame containing the product catalog.
    """
    st.subheader("🔎 Persona Enrichment: From Signal to Suggestion")

    # Text input from user or sample journal/post
    user_input = st.text_area("Paste a social post or journal entry:")
    if st.button("🔍 Analyze Input"):
        nlp_result = analyze_text(user_input)

        # Display extracted intents and sentiment
        st.markdown(f"**Extracted Intents:** `{', '.join(nlp_result['intents'])}`")
        st.markdown(f"**Sentiment:** {nlp_result['sentiment'].capitalize()} ({nlp_result['confidence']*100:.1f}%)")
        st.markdown(f"**Model Used:** {nlp_result['routed_model']}")

        # Show co-occurrence enrichment
        enriched_intents = set(nlp_result["intents"])
        for intent in nlp_result["intents"]:
            top_related = intent_cooc[intent_cooc["intent"] == intent].sort_values(by="score", ascending=False).head(2)
            enriched_intents.update(top_related["related_intent"].tolist())

        st.markdown(f"**Final Enriched Intents:** `{', '.join(enriched_intents)}`")

        # Get recommendations
        final_recos = recommend_by_intent_with_enrichment(
            user_intents=list(enriched_intents),
            sentiment=nlp_result["sentiment"],
            products_df=catalog,
            cooc_df=intent_cooc,
            top_k=5
        )

        # Display recommendations
        st.divider()
        st.subheader("🧠 Matched Product Recommendations")
        for _, row in final_recos.iterrows():
            st.markdown(f"**{row['title']}**")
            st.markdown(f"_{row['description']}_")
            st.markdown(f"**Tags:** `{row['tags']}` | **Match Score:** {row['match_score']}  ")
            st.markdown("---")

        # View enriched persona
        view_enriched_persona(profile)