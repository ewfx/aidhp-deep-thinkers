import pandas as pd
from generate_recommendations.recommendation import get_top_recommendations

user_text = "Interested in crypto, passive income, and wealth growth. Feeling optimistic about long-term investments."
items_df = pd.read_csv("user_data/products.csv")  # or merge products + content
results_df, times = get_top_recommendations(user_text, items_df)

print(results_df[["title", "method", "score"]])
print("Timing:", times)
