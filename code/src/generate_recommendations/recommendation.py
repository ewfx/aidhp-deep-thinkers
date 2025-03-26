import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
import time

def get_top_recommendations(user_text, items_df, top_n=5):
    """
    Recommend top-N items for a user using both cosine similarity and FAISS (L2).
    
    Args:
        user_text (str): Combined user profile string.
        items_df (pd.DataFrame): Must have 'title' and 'description' columns.
        top_n (int): Number of recommendations to return.

    Returns:
        pd.DataFrame: Top-N recommendations with both methods.
        dict: Time taken for cosine and faiss.
    """
    start_sentenceTransformer = time.time()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentenceTransformer_time = time.time() - start_sentenceTransformer
    full_texts = items_df["title"] + ": " + items_df["description"]

    # Generate embeddings
    user_embedding = model.encode([user_text])[0]
    item_embeddings = model.encode(full_texts.tolist())
    
    # Cosine similarity
    start_cosine = time.time()
    cosine_sim = cosine_similarity([user_embedding], item_embeddings)[0]
    cos_top_idx = np.argsort(cosine_sim)[::-1][:top_n]
    cosine_results = items_df.iloc[cos_top_idx].copy()
    cosine_results["score"] = cosine_sim[cos_top_idx]
    cosine_results["method"] = "Cosine Similarity"
    cosine_time = time.time() - start_cosine


    # FAISS
    start_faiss = time.time()
    d = item_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(item_embeddings).astype("float32"))
    _, faiss_top_idx = index.search(np.array([user_embedding]).astype("float32"), top_n)
    faiss_time = time.time() - start_faiss
    faiss_top_idx = faiss_top_idx[0]
    faiss_results = items_df.iloc[faiss_top_idx].copy()
    faiss_results["score"] = "N/A"
    faiss_results["method"] = "FAISS (L2 Distance)"

    # Combine
    # combined_df = pd.concat([cosine_results, faiss_results], ignore_index=True)

    return cosine_results, {
        "cosine": round(cosine_time, 3),
        "faiss": round(faiss_time, 3),
        "sentenceTransformer": round(sentenceTransformer_time, 3)
    }


def recommend_by_intent_with_enrichment(user_intents, sentiment, products_df, cooc_df, top_k=3):
    """
    Recommends products based on user intents + enriched co-occurring intents.

    Args:
        user_intents (List[str])
        sentiment (str)
        products_df (DataFrame): must have 'tags' column
        cooc_df (DataFrame): co-occurrence matrix with 'intent', 'related_intent', 'score'
        top_k (int)

    Returns:
        pd.DataFrame
    """
    #right now thwe filtering is happenong based on the score
    #we can use ranking and filtering too

    # Expand intents using co-occurrence matrix
    print(" indise the intent recommendation-")
    print("sentiment - ", sentiment)
    print("products_df - ", products_df)
    print("cooc_df - ", cooc_df)
    print("user_intents - ", user_intents)
    enriched_intents = set(user_intents)
    print("enriched_intents - ", enriched_intents)
    for intent in user_intents:
        top_related = cooc_df[cooc_df["intent"] == intent].sort_values(
            by="score", ascending=False
        ).head(2)["related_intent"].tolist()
        enriched_intents.update(top_related)
    print("updated enriched intents - ", enriched_intents)

    # Score products by overlap
    def match_score(row):
        product_tags = set(row["tags"].split(", "))
        return len(product_tags & enriched_intents)

    # Filter and score
    scored_df = products_df.copy()
    scored_df["match_score"] = scored_df.apply(match_score, axis=1)
    print("scored_df - ", scored_df)
    recommendations = scored_df[scored_df["match_score"] > 0]
    print("recommendations - ", recommendations)

    # Sentiment-aware filtering (example: avoid risk when user is negative)
    if sentiment == "negative":
        recommendations = recommendations[
            ~recommendations["title"].str.contains("crypto|stocks", case=False)
        ]

    print("recommendations after sentiment filtering - ", recommendations)

    return recommendations.sort_values(by="match_score", ascending=False).head(top_k)
