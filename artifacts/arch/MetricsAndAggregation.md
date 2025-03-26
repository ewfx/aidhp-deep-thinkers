# 📊 Metrics, Sentiment, and Aggregation

In a multi-post user scenario, we don’t just rely on individual post outputs.

We aggregate across:
- ✅ All detected **intents** (weighted by frequency)
- ✅ All **post-level sentiments**
- ✅ **Dominant sentiment** at the user level (e.g., most common emotion across posts)

We also ensure:
- One primary + one exploratory recommendation per post
- De-duplication of products across posts
- Learning content is tailored to both intent and sentiment

This makes the assistant feel:
- Context-aware
- Emotionally intelligent
- Personalized, not templated

---

## 🧠 Why This Matters

People may show different needs and moods across posts.

Our metric aggregation ensures we don’t misinterpret their goals based on just one post.

For example:
- 2 positive posts about saving + 1 anxious post about investing
- Dominant sentiment = neutral
- We still suggest conservative investing + active saving tools
