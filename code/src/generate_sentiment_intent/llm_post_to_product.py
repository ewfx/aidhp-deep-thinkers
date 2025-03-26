import os
from collections import Counter, defaultdict
from generate_sentiment_intent.sentiment_intent.intent_to_products import intent_to_products
from generate_sentiment_intent.sentiment_intent.llm_based_intents import posts_to_intents
from generate_sentiment_intent.sentiment_intent.sentiment_detection import get_sentiment
from generate_sentiment_intent.sentiment_intent.llm_similarity_embedding import get_similar_intents_with_scores

# from sentiment_intent.intent_to_products import intent_to_products
# from sentiment_intent.llm_based_intents import posts_to_intents
# from sentiment_intent.sentiment_detection import get_sentiment
# from sentiment_intent.llm_similarity_embedding import get_similar_intents_with_scores

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
import ast

def get_products_by_sentiment(intents, sentiment):
    recommended = []
    for intent in intents:
        if intent in intent_to_products:
            sentiment_products = intent_to_products[intent].get(sentiment.lower(), [])
            recommended.extend(sentiment_products)
    return recommended


def post_to_product(text):
    """
    Analyzes the text and returns a list of recommended products based on the detected intents and sentiment.

    Args:
        text (str): The input text to analyze.

    Returns:
        list: A list of recommended products.
    """
    primary_intent_response = posts_to_intents(text)
    if not primary_intent_response:
        print("We are facing connectivity issue, Let's try again later")
        return None, None, None, None, None

    if isinstance(primary_intent_response, str):
        try:
            primary_intent_response = ast.literal_eval(primary_intent_response)
        except Exception as e:
            print("❌ Could not parse LLM intent response:", e)
            primary_intent_response = []
    else:
        primary_intent_response = primary_intent_response

    post_sentiment = get_sentiment(text, primary_intent_response)
    similar_intents = get_similar_intents_with_scores(primary_intent_response)
    primary_recommended_products = get_products_by_sentiment(primary_intent_response, post_sentiment)
    exploratory_products = get_products_by_sentiment(similar_intents.keys(), post_sentiment)

    return primary_recommended_products, exploratory_products, post_sentiment, primary_intent_response, similar_intents

def posts_to_products(posts: list):
    """
    Processes a list of posts and returns one primary + one exploratory recommendation per post
    using intent and sentiment mappings. Avoids duplicate recommendations across posts.

    Args:
        posts (List[str]): A list of social media posts.

    Returns:
        List[Dict]: A list of recommendations (primary + exploratory) for each post.
    """
    all_recommendations = []
    seen_titles = set()
    all_sentiments = []

    for post in posts:
        print(f"\n📝 Processing post: {post}")

        primary_recs, exploratory_recs, sentiment, primary_intent, secondary_intent = post_to_product(post)
        all_sentiments.append(sentiment)

        primary_recommendation = None
        exploratory_recommendation = None

        if not primary_recs:
            continue

        # Choose first unique primary recommendation
        for product in primary_recs:
            if product["title"] not in seen_titles:
                primary_recommendation = product
                seen_titles.add(product["title"])
                break
        
        if not exploratory_recs:
            continue

        # Choose first unique exploratory recommendation
        for product in exploratory_recs:
            if product["title"] not in seen_titles:
                exploratory_recommendation = product
                seen_titles.add(product["title"])
                break

        # If no primary found, backfill from exploratory
        if not primary_recommendation and exploratory_recommendation:
            primary_recommendation = exploratory_recommendation
            exploratory_recommendation = None

        recommendations = {
            "post": post,
            "primary": primary_recommendation,
            "exploratory": exploratory_recommendation,
            "sentiment": sentiment,
            "primary_intents": primary_intent,
            "secondary_intents": secondary_intent
        }
        all_recommendations.append(recommendations)

    dominant_sentiment = Counter(all_sentiments).most_common(1)[0][0] if all_sentiments else "neutral"
    return all_recommendations, dominant_sentiment

if __name__ == "__main__":
    example_text = "Markets are scary, but I'm still buying the dip in crypto and stocks."
    result = post_to_product(example_text)
    print(result)
    # example_text2 = "Just attended the biggest concert of the year 🎤🎉"
    # result2 = post_to_product(example_text2)
    # print(result2)
    user_posts = [
        "Markets are scary, but I'm still buying the dip in crypto and stocks.",
        "Can't believe how much I'm paying in credit card interest.",
        "Trying to understand how SIPs actually work.",
        "Feeling overwhelmed by budgeting every month."
    ]

    all_recs , dominant_sentiment= posts_to_products(user_posts)
    print("overall mood is ", dominant_sentiment)

    print("\n=== Primary Recommendations ===")
    for idx, rec in enumerate(all_recs):
        if rec["primary"]:
            print(f"\n🔹 Post {idx+1}: {rec['post']}")
            print(f"🎯 Sentiment: {rec['sentiment']}")
            print(f"✅ Primary: {rec['primary']['title']} — {rec['primary']['desc']}")

    print("\n=== Exploratory Recommendations ===")
    for idx, rec in enumerate(all_recs):
        if rec["exploratory"]:
            print(f"\n🔹 Post {idx+1}: {rec['post']}")
            print(f"✨ Exploratory: {rec['exploratory']['title']} — {rec['exploratory']['desc']}")
