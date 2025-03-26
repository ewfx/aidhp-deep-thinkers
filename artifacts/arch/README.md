# 💡 Financial Assistance from Social Media Posts

This part was explored as the requirement to make our **Financial Assistant** smart that reads a user's social media posts and recommends personalized **financial products**, **services**, and **educational content** based on detected **intent** and **sentiment**.

---

## 🧭 Goal

To interpret user-generated content (like Instagram captions, Reddit posts, or tweets) and understand:
- What financial needs they might have (e.g., saving, investing, debt)
- How they feel about those needs (e.g., stressed, excited, confused)
- What product/service or learning content could help them

---

## 🎯 Example

**Post:**  
> "Markets are scary right now. I don’t know where to invest safely."

**Detected:**
- Intent: `Investing & Wealth Building`
- Sentiment: `Negative`

**Recommendations:**
- ✅ Primary: Low-Risk Investment Tools  
- ✨ Exploratory: Beginner’s Guide to Mutual Funds  
- 📘 Learning: “Safe Investment Strategies for New Investors”

---

## 🔧 What This System Does

For each post:
- Detects top 2–3 **intent categories** using LLMs 
- Analyzes **sentiment** using FinBERT or RoBERTa (depending on financial context)
- Finds **related intents** using sentence embeddings (cosine similarity)
- Maps intents + sentiment to personalized product suggestions
- Uses another LLM to suggest **learning resources** (articles, guides, courses)

---

## 🧠 Intent Reasoning & Intelligence

This system goes beyond simple intent matching.

It uses techniques like:

- **Collaborative Intent Expansion**: Suggests related financial intents based on user patterns  
- **Context-Aware Metrics**: We consider not just what the user says, but how often, and with what tone

📎 Learn more about:
- 🔁 [Collaborative Intent Logic](./CollaborativeIntent.md)
- 📊 [User-Level Metrics & Design Considerations](./MetricsAndAggregation.md)

-----

## 🛠️ Tech Stack

| Component | Tools & Models |
|----------|----------------|
| Intent Detection | LLM via Together.ai / OpenRouter + LangChain using **Few Shot Prompting**  (`facebook/bart-large-mnli`)|
| Sentiment Analysis | FinBERT (financial) + RoBERTa (general) |
| Intent Similarity | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Recommendations | Custom mapping dictionary with titles & descriptions |
| Learning Suggestions | LLM-driven prompt using primary intent + sentiment |
| Orchestration | Python + Streamlit + LangChain |

---

## 🧠 Intent Categories

## 🧠 Intent Categories

Refined to ~20 user-centric, high-signal categories like:
- Budgeting & Expenses
- Debt & Stress
- Investing & Wealth Building
- Insurance Interest
- Product Discovery
- Lifestyle: Travel, Food, Wellness

Each intent can map to:
- Product recommendations
- Exploratory intent suggestions
- Personalized learning content

---

## ✅ Final Outcome

You get:
- 🔹 One **primary recommendation** per post
- 🔸 One **exploratory recommendation**
- 📘 One **learning content suggestion**
- ✅ Support for **multi-post user profiles**
- 🔍 De-duplication and intent-aware aggregation
- 🎯 Output driven entirely by user-generated text

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `post_to_product()` | Processes a single post for intent/sentiment and recommends accordingly |
| `posts_to_products()` | Processes a list of posts with per-post recommendations |
| `get_sentiment()` | Routes to FinBERT or RoBERTa depending on post context |
| `get_similar_intents_with_scores()` | Uses cosine similarity on sentence embeddings |
| `get_learning_recommendations()` | LLM-powered generator for educational suggestions |

---

## 🚀 Future Add-ons

- Streamlit chatbot interface
- Logging & analytics dashboard
- Fine-tuned LLM on real social finance posts
- Vector-based product discovery (RAG-style)

---

## 🧑‍💻 Example Usage

```python
from sentiment_engine import posts_to_products

posts = [
    \"Markets are scary, but I'm still buying the dip.\",
    \"Can't believe my credit card charges this much interest!\",
    \"Trying to learn how SIPs work.\"
]

recommendations, dominant_sentiment = posts_to_products(posts)

---

## 🔐 All models used are free, open-source, and API-accessible.

This project does **not rely on paid APIs** like OpenAI or Anthropic.

---

## 📢 Contact

Built by **Acanksha Jain**  
For any inquiries, drop a message!
