from sentence_transformers import SentenceTransformer, util
import torch

# Your 20 refined categories
intent_categories = [
    "Budgeting & Expenses", "Savings & Planning", "Debt & Stress", "Investing & Wealth Building",
    "Credit & Cards", "Insurance Interest", "Market Sentiment", "Financial Literacy & Learning",
    "Career & Income Goals", "Product Issues", "Product Discovery", "Complaints & Frustration",
    "Lifestyle: Food & Fashion", "Lifestyle: Travel", "Lifestyle: Entertainment",
    "Lifestyle: Wellness", "Positive Milestones", "Community & Sharing", "Generic Financial Concern"
]

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
intent_embeddings = model.encode(intent_categories, convert_to_tensor=True)

def get_similar_intents_with_scores(primary_intents, top_k=2, threshold=0.45):
    # print("✔️ Type of primary_intents:", type(primary_intents))
    # print("✔️ Value of primary_intents:", primary_intents)
    # print("primary intents in the function- ", primary_intents)
    similar_intents = {}

    for intent in primary_intents:
        print(f"🔍 Checking intent: {intent}")

        if intent not in intent_categories:
            # print(f"❌ '{intent}' not found in intent_categories list.")
            continue

        idx = intent_categories.index(intent)
        query_embedding = intent_embeddings[idx]
        cosine_scores = util.pytorch_cos_sim(query_embedding, intent_embeddings)[0]

        top_indices = torch.topk(cosine_scores, k=top_k + 1).indices.tolist()
        for i in top_indices:
            if i == idx or intent_categories[i] in primary_intents:
                continue
            label = intent_categories[i]
            score = round(float(cosine_scores[i]), 3)
            if( score >=threshold):
                similar_intents[label] = score


    # print("similar intents in the function- ", similar_intents)
    # Return sorted by score
    return dict(sorted(similar_intents.items(), key=lambda item: item[1], reverse=True))


# Example use
if __name__ == "__main__":
    primary_detected = ["Credit & Cards", "Savings & Planning"]
    exploratory = get_similar_intents_with_scores(primary_detected)

    print("Primary Intents:", primary_detected)
    print("Exploratory Intents (Suggested):", exploratory)

    primary_detected1 = ['Product Discovery', 'Lifestyle: Entertainment']
    exploratory1 = get_similar_intents_with_scores(primary_detected1)

    print("Primary Intents:", primary_detected1)
    print("Exploratory Intents (Suggested):", exploratory1)

    primary_detected2 = ['Market Sentiment', 'Investing & Wealth Building']
    exploratory2 = get_similar_intents_with_scores(primary_detected2)

    print("Primary Intents:", primary_detected2)
    print("Exploratory Intents (Suggested):", exploratory2)


