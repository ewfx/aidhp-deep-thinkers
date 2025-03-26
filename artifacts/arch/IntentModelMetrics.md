# 📊 Intent Detection Model Evaluation

This document summarizes the evaluation results of multiple components used in analyzing user social media posts. The goal was to extract **intents**, detect **sentiment**, and drive **recommendations** using interpretable and performant models.

We evaluated different approaches for:
- **Intent detection** (zero-shot vs LLM-based few-shot)
- **Sentiment classification** (financial domain-specific models)
- **Embedding & similarity matching** (semantic search)
- **Performance timings** across components

---

## ✅ Intent Detection Models

### Models Tested (Zero-shot)
- `facebook/bart-large-mnli`
- `joeddav/xlm-roberta-large-xnli`

Both were used with zero-shot prompting across a labeled set of ~30 social media posts. Batch processing was implemented to optimize runtime.

### 📈 Metrics Summary

| Metric | BART | XLM-RoBERTa |
|--------|------|-------------|
| Avg Jaccard | 0.195 | 0.109 |
| Precision@1 | 0.50 | 0.45 |
| Time (no batch) | 476.49 sec |  -  |
| Time (batch size=8) | 96.10 sec |  -  |

### 🚫 Limitations of Zero-Shot Models
- Many predictions were **semantically off** (human feedback).
- Behavior indicated **overfitting to label semantics**, but not true user intent.
- Misinterpretations in multi-intent posts (e.g., credit + savings).

### ✅ Final Approach Chosen
We switched to **Few-Shot Prompting** using **`mistralai/Mistral-7B-Instruct-v0.1`**, implemented with **LangChain**.
- LLM-based intent extraction showed better alignment with real-world phrasing
- Prompted with labeled examples and refined category list

---

## 🧠 Sentiment Detection Models

Financial sentiment requires specialized language handling. We compared 3 domain-specific models.

### Models Evaluated
- `yiyanghkust/finbert-tone` — Financial tone classification (positive/neutral/negative)
- `ProsusAI/finbert` — General finance
- `amphora/bert-base-finance-sentiment` — Fin/Reddit blend

### 📊 Results
| Model | Accuracy | Avg Confidence | Notes |
|-------|----------|----------------|-------|
| **yiyanghkust/finbert-tone** | 86.6% | 0.82 | ✅ Selected: Most consistent for short posts |
| ProsusAI/finbert | 80.0% | 0.77 | Good for formal/long text |
| amphora/bert-fin | 73.3% | 0.71 | Struggled with emotional phrasing |

---

## 🔎 Sentence Embeddings & Similarity

To identify related intents (for collaborative recommendation), we used:
- **Embedding model**: `all-MiniLM-L6-v2` (Hugging Face)
- **Similarity metric**: Cosine similarity
- **Semantic search engine**: FAISS (optional for large-scale)

For current prototype, **cosine** was sufficient due to small dataset size.

### 🔁 Collaborative Intent Expansion
- Co-occurrence + embedding similarity used to find secondary intents
- This enables exploratory recommendations beyond the user’s primary post content

---

## ⏱️ Component Timing Benchmarks

| Component | Time Taken (seconds) |
|-----------|----------------------|
| Transaction Behavior Analysis | 0.02 |
| **MistralAI Generation (LLM)** | 2.78 |
| Embedding-based Recommendation | 12.08 |
| Cosine Similarity Calculation | 0.02 |
| FAISS Search | 0.11 |
| SentenceTransformer Inference | 6.14 |
| Intent & Sentiment Extraction (LLM) | 3.74 |

---

## ✅ Summary

- Zero-shot intent models were tested but lacked reliability → migrated to LLM few-shot (Mistral)
- FinBERT tone (yiyanghkust) selected for best sentiment results
- Embedding + cosine used to enable exploratory intent and related recommendations
- Overall response time per post remains within real-time thresholds (~3–5 sec LLM, ~6–12 sec total)

📎 Next steps: Evaluate learning recommendation accuracy and user personalization depth.