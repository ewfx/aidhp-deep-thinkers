from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

user_text = "interested in travel, crypto, investing. Goal: wealth diversification. Feeling optimistic about the market."

product_texts = [
    "Premium travel credit card with lounge access and forex benefits",
    "Crypto investment advisory for high-risk takers",
    "Safe mutual fund plans for long-term growth"
]

user_vector = model.encode(user_text)
product_vectors = model.encode(product_texts)

print("User Vector:", user_vector)
print("Product Vectors:", product_vectors)

print("Shape of user vector: " , user_vector.shape)
print("Shape of product vectors: ", product_vectors.shape)

similarity_product = cosine_similarity([user_vector], product_vectors)
print("Similarity Scores:", similarity_product)
similarities = similarity_product[0]
print("Cosine Similarity Scores:" , similarities)

#rank the products based on similarity scores
top_indices = np.argsort(similarities)[::-1]
for idx in top_indices[:3]:
    print(f"Recommendation: {product_texts[idx]} (Score: {similarities[idx]:.2f})")
# **Evaluation Metrics:**
# - **Cosine Similarity:** Measure of similarity between user sentiment and product descriptions
# - **Euclidean Distance:** Measure of distance between user sentiment and product descriptions