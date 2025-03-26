import pandas as pd
from collections import defaultdict
import itertools
import ast

# Load enriched Instagram and Reddit datasets
instagram_df = pd.read_csv("data/sentiment_data/instagram_enriched.csv")
reddit_df = pd.read_csv("data/sentiment_data/reddit_enriched_output.csv")
# Ensure intents are lists

instagram_df["intents"] = instagram_df["intents"].fillna("[]").apply(ast.literal_eval)
reddit_df["intents"] = reddit_df["intents"].fillna("[]").apply(ast.literal_eval)

# Assign weights to posts
instagram_df["weight"] = 1.0
reddit_df["upvote_ratio"] = reddit_df["upvote_ratio"].fillna(1.0)
reddit_df["weight"] = reddit_df.get("upvote_ratio", 1).apply(lambda x: 1 + 2 * (x / reddit_df["upvote_ratio"].max()) )
# print("here we added the wreights to intents as well - ")
# print(instagram_df.head())  
# print(reddit_df.head())

# Combine both datasets
combined_df = pd.concat([instagram_df, reddit_df], ignore_index=True)
# print("here we combined the two datasets - ")
# print(combined_df.head())

# Build intent co-occurrence matrix
co_occurrence = defaultdict(lambda: defaultdict(float))
# print(" before co_occurrence - ")
# print(co_occurrence)

for _, row in combined_df.iterrows():
    intents = list(set(row["intents"]))
    weight = row["weight"]
    for a, b in itertools.combinations(sorted(intents), 2):
        co_occurrence[a][b] += weight
        co_occurrence[b][a] += weight
# print(" after co_occurrence - ")
# print(co_occurrence)

# Normalize co-occurrence
normalized_matrix = defaultdict(dict)
for intent, related in co_occurrence.items():
    max_score = max(related.values())
    for other_intent, score in related.items():
        normalized_matrix[intent][other_intent] = round(score / max_score, 3)

# print("normalized_matrix - ")
# print(normalized_matrix)

# Convert to DataFrame for analysis
flat_records = []
for intent, related in normalized_matrix.items():
    for other_intent, score in related.items():
        flat_records.append({
            "intent": intent,
            "related_intent": other_intent,
            "score": score
        })


cooc_df = pd.DataFrame(flat_records)
cooc_df.to_csv("intent_cooccurrence_matrix.csv", index=False)
print("✅ Intent co-occurrence matrix saved to intent_cooccurrence_matrix.csv")
