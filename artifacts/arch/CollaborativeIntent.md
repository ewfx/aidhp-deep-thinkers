# 🔁 Collaborative Intent Expansion

In real-world behavior, people don’t talk about financial goals in isolation.

A user posting about credit card struggles might also be worried about budgeting, or thinking about building savings.

We introduce **Collaborative Intent** — a method to infer **related, co-occurring financial needs** by:

- Building a co-occurrence map across intents
- Using sentence embeddings + cosine similarity to find related categories
- Expanding recommendations with this “intent graph”

This helps surface:
- Additional product recommendations
- More relevant learning content
- Serendipitous value for the user

---

## 🔍 Example

**Post:**  
> “My investments are not growing like they used to. Wondering if I need to rebalance.”

- Primary Intent: `Investing & Wealth Building`
- Collaborative Intents:
  - `Risk Mitigation`
  - `Financial Literacy`
- Result:
  - Primary: ETF Rebalancing Tools
  - Exploratory: Safe Investment Strategies, Risk Diversification Guides
