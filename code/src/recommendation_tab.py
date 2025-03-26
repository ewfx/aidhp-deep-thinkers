import streamlit as st
import pandas as pd
from generate_recommendations.recommendation import get_top_recommendations, recommend_by_intent_with_enrichment
from feedback_log.log import log_feedback
from generate_personas.persona_enrichment import enrich_persona_from_posts
from generate_personas.transaction_behaviour import build_transaction_behavior_features
from collections import defaultdict
from generate_sentiment_intent.llm_post_to_product import posts_to_products
import os
import requests
from dotenv import load_dotenv
import time
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/inference"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"


BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
catalog_path = os.path.join(BASE_DIR, "data", "recommendable_products_catalog.csv")
intent_cooc_path = os.path.join(BASE_DIR, "data", "sentiment_data", "intent_cooccurrence_matrix.csv")
# Load required product catalog and intent co-occurrence matrix
catalog = pd.read_csv(catalog_path)
intent_cooc = pd.read_csv(intent_cooc_path)

def render_recommendation_tab(profile, selected_user_id, products, content, all_recommendation):
    """
    Renders the Recommendations tab in the Streamlit app.

    Args:
        profile (pd.Series): The user's profile containing details like risk appetite, financial goals, etc.
        selected_user_id (str): The ID of the currently logged-in user.
        products (pd.DataFrame): DataFrame containing product recommendations.
        content (pd.DataFrame): DataFrame containing content recommendations.
    """
    times = {}

    start_time = time.time()
    profile = build_transaction_behavior_features(selected_user_id, profile)
    times["Transaction Behavior Analysis"] = time.time() - start_time

    # start_time = time.time()
    # posts = profile.get("posts")
    # print(" seeing the posts - ", profile.get("posts"))
    # print(" the data type of post - ", type(profile.get("posts")))
    # print(" seeing the recommendations - ", all_recommendation)
    # primary_recommendations, exploratory_recommendations , mood, primary_intents, secondary_intents = posts_to_products(posts)
    # times["Intent-based Recommendation"] = time.time() - start_time
    # profile = enrich_persona_from_posts(profile)

    # user_intents = profile.get("derived_intents", [])
    # sentiment_label = profile.get("derived_sentiment", "Neutral")
    
    # Initialize a dictionary with lists for each sentiment category
    sentiment_to_intents = defaultdict(set)  # Using a set to avoid duplicates
    reco_items = pd.concat([products, content], ignore_index=True)

    # Iterate over all recommendations and map sentiments to primary intents
    for rec in all_recommendation:
        sentiment = rec["sentiment"]  # Extract sentiment
        primary_intents = rec["primary_intents"]  # Extract primary intents
        
        # Add each primary intent to the corresponding sentiment category
        sentiment_to_intents[sentiment].update(primary_intents)

    # Convert sets to lists for cleaner formatting
    sentiment_to_intents = {k: list(v) for k, v in sentiment_to_intents.items()}

    # Print the final dictionary
    print("the final sentiment and intent mapping - ", sentiment_to_intents)

    # Constructing the sentiment-intent text dynamically
    sentiment_phrases = []
    for sentiment, intents in sentiment_to_intents.items():
        if intents:
            sentiment_phrases.append(f"they express {sentiment} sentiment towards {', '.join(intents)}")

    # Joining the sentiment-intent phrases
    sentiment_intent_summary = " and ".join(sentiment_phrases) + " based on their social media activity."

    print("the intent and sentiment mapping - ", sentiment_intent_summary)

    transaction_persona = profile.get("transaction_persona", {})
    active_labels = [key for key, value in transaction_persona.items() if value is True]

    st.header("🎯 My Recommendations")
    user_profile_text = (
        f"User, aged {profile.get('age')}, works as a {profile.get('profession')}. "
        # f"They have interests in {', '.join(profile.get('interests', []))}, "
        f"They are focused on financial goals like {', '.join(profile.get('financial_goals', []))}, for which they have a {transaction_persona.get('risk_appetite', '')} risk appetite. "
        f"From their recent activity, {sentiment_intent_summary} "
        f"They spend mostly on {transaction_persona['top_spending_category']}, is a {transaction_persona['spender_type']} and is a {transaction_persona['travel_frequency']}. "
        f"And user identifies as : {', '.join(active_labels)}"
    )

    print("the user profile text - ", user_profile_text)
    # st.divider()
    # GenAI Mistral Based recommendations
    # st.subheader("📝Your Personal Finance Assistant's Recommendations")
    product_list = "\n".join([f"{rec['title']} - {rec['description']}" for _, rec in reco_items.iterrows()])
    prompt = (f"""
    On the basis of the following customer profile and available products and content,
    Customer Profile: {user_profile_text}\n
    Available Products/Content:\n{product_list}\n
    Recommend the top 3 most relevant financial products/service and content for the customer. Suggest 1 investment product, 1 credit product(card or loan), and 1 content piece.
    """)

    # print(prompt)
    start_time = time.time()

    try:
        recommendations_text = generate_mistral_response(prompt)
    except Exception as e:
        recommendations_text = f"LLM generation failed: {str(e)}"
    
    times["MistralAI Generation"] = time.time() - start_time

    print("recommednation_text - ", recommendations_text)
    # Split recommendations into list format
    # recommendations = recommendations_text.split("\n")[1:]  # Skipping the first line

    # for rec in recommendations:
    #     if rec.strip():  # Ignore empty lines
    #         parts = rec.split(":")  # Split by colon to separate title and description
            
    #         if len(parts) > 1:
    #             title = parts[0].strip()  # Extract title (e.g., "Investment Product")
    #             desc = ":".join(parts[1:]).strip()  # Extract full description
                
    #             with st.container():
    #                 st.markdown(f"### {title}")  # Bold title
    #                 st.write(desc)  # Display description in normal text
    #                 st.divider()  # Add a horizontal separator for better clarity

    
    st.markdown(recommendations_text)

    # Logic-based recommendations
        # if "luxury" in txn_behavior.lower():
        #     st.markdown("- 💳 **Premium Travel Credit Card** — Based on your international and luxury spends")
        # if profile.get("risk_appetite", "") == "Low":
        #     st.markdown("- 📈 **Safe Mutual Fund Plans** — Matches your conservative investment style")
        # if profile['income'] > 2000000:
        #     st.markdown("- 🏦 **Wealth Management Services** — Tailored for HNIs like you")
    st.divider()
    # Embedding-based recommendations
    st.subheader("🤖 Embedding-Based Recommendations")
    start_time = time.time()
    
    top_recommendations, similarity_times = get_top_recommendations(user_profile_text, reco_items, 3)
    times["Embedding based Recommendation"] = time.time() - start_time
    times["Similarity Calculation"] = similarity_times

    for _, row in top_recommendations.iterrows():
        st.markdown(f"**{row['title']}**  \n_{row['description']}_")
        st.markdown(f"**Source:** {row['type'].capitalize()} | **Method:** {row['method']} | **Score:** {float(row['score']):.2f}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Like", key=f"like_{row['title']}_{row['method']}"):
                log_feedback(selected_user_id, row['title'], row['method'], "like")
                st.success("Feedback logged: Like")
        with col2:
            if st.button("👎 Dislike", key=f"dislike_{row['title']}_{row['method']}"):
                log_feedback(selected_user_id, row['title'], row['method'], "dislike")
                st.warning("Feedback logged: Dislike")
        st.markdown("---")
    # st.divider()
    # Intent-based recommendations
    # st.subheader("🧠 Social Media Activity Based Product Recommendations")
    # start_time = time.time()
    # final_recos = recommend_by_intent_with_enrichment(
    #     user_intents=user_intents,
    #     sentiment=sentiment_label,
    #     products_df=catalog,
    #     cooc_df=intent_cooc,
    #     top_k=5
    # )
    # times["Intent-based Recommendation"] = time.time() - start_time
    # if primary_recommendations.empty:
    #     st.markdown("_No matches found for this user based on social media activity. We would need more data")
    # else:
    #     for recommendation in primary_recommendations:
    #         st.markdown(f"**{recommendation['title']}**")
    #         st.write(recommendation['desc'])
    #     for _, row in final_recos.iterrows():
    #         st.markdown(f"**{row['title']}**")
    #         st.markdown(f"_{row['description']}_")
    #         st.markdown(f"**Tags:** `{row['tags']}` | **Match Score:** {row['match_score']}  ")
    #         st.markdown("---")

    # st.divider()
    # # Suggested content
    # st.subheader("📚 Suggested Content")
    # if sentiment_label == "Negative":
    #     st.markdown("- 📘 _Market Safety Strategies_ — To help ease your concerns")
    # elif sentiment_label == "Positive":
    #     st.markdown("- 🌟 _Advanced Investing Playbook_ — Level up your portfolio")
    # elif sentiment_label == "Neutral":
    #     st.markdown("- 📗 _Balanced Financial Planning Tips_ — To keep you on track")

    # st.divider()
    #Explore More
    st.subheader("🧭 Explore More")
    st.markdown("- ✨ _Did you know?_ Try our new **Crypto Tax Assistant**")
    st.markdown("- 🚀 _Trending:_ Explore **Robo-advisory services** for hassle-free investing")

    return times;

def generate_mistral_response(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a expert financial advisor."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.7
    }
    response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        response = response.json()
        # print(response)
        content = response['output']['choices'][0]['text']
        # print(content)
        return content
    else:
        return f"LLM generation failed: {response.status_code} - {response.text}"