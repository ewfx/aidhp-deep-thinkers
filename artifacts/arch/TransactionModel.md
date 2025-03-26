# 💳 Transaction Behavior & Profile-Enriched Financial Recommendations

This module extends our smart financial assistant by analyzing **user transaction behavior** and **demographic data** to enrich user profiles and provide better intent-driven recommendations using LLMs.

---

## 🧭 Objective

To go beyond just social media insights by incorporating **real-world spending behavior** and enabling users to **personalize their profile inputs**:
- Classify users based on transaction history
- Allow users to update profile fields like age, interests, and profession
- Generate fresh recommendations dynamically based on updated profiles

---

## 🧠 Key Features

### 1. **Transaction Persona Builder**
Implemented in `transaction_behaviour.py`, this module reads a user's transaction history and calculates:

- **Spending behavior** (average spend, luxury vs. budget, card usage)
- **Lifestyle markers**: 
  - Frequent traveler
  - Entertainment lover
  - Subscription enthusiast
  - Family- or health-focused
- **Risk Appetite**:
  - Calculated based on age + debt-to-income ratio

These features are stored under the user's `transaction_persona` profile.

---

### 2. **User Profile Enrichment + Editing**
In addition to automated profile generation, the system also supports **manual profile customization**:

Users can edit fields such as:
- `age`
- `profession`
- `financial interests` (e.g., saving, investing, credit building)

These edits are:
- Reflected immediately in the profile
- Used to generate **updated recommendations**
- Persisted in the backend to maintain continuity in future sessions

---

### 3. **LLM-Powered Recommendation (`recommendation.py`)**

Once a user’s profile is enriched with transaction and social media data, we:

1. Merge the profile into a natural language prompt
2. Feed the prompt into a **zero-shot LLM (Mistral-7B via LangChain)**
3. Generate customized product or service suggestions

This allows us to:
- Adapt suggestions based on actual financial behavior
- Handle users with limited social media signals
- Provide educational guidance based on risk/lifestyle profile

---

## 🛠️ Tech Stack

| Component | Tech/Model Used |
|----------|-----------------|
| MCC Mapping & Persona Rules | `pandas`, JSON mappings, business logic |
| LLM Recommendation | `mistralai/Mistral-7B-Instruct-v0.1` via `LangChain` |
| Embedding-based Search (Optional) | `all-MiniLM-L6-v2`, FAISS, cosine similarity |
| Co-occurrence Expansion | Uses collaborative intent expansion logic |
| Profile Editor | Frontend interface + backend JSON update |

---

## ⏱️ Performance Snapshot

| Step | Avg Time (seconds) |
|------|--------------------|
| Transaction Behavior Analysis | 0.02 |
| LLM Recommendation (Mistral) | 2.78 |
| Embedding Model Inference | 6.14 |
| Cosine Similarity | 0.02 |
| FAISS Search | 0.11 |

---

## 🧑‍💻 Example Workflow

```python
from transaction_behaviour import build_transaction_behavior_features
from recommendation import get_top_recommendations

# Step 1: Enrich profile using transaction data
profile = build_transaction_behavior_features(user_id, base_profile)

# Optional: Apply user-edited values
profile['age'] = 42
profile['profession'] = 'Freelancer'
profile['interests'] = ['investing', 'retirement planning']

# Step 2: Feed enriched profile text into LLM
user_prompt = build_prompt_from_profile(profile)
recommendations = llm_chain.invoke(user_prompt)
