# 🚀 Financial Buddy

## 📌 Table of Contents
- [Introduction](#-introduction)
- [Demo](#-demo)
- [Inspiration](#-inspiration)
- [What It Does](#-what-it-does)
- [How We Built It](#-how-we-built-it)
- [Challenges We Faced](#-challenges-we-faced)
- [How to Run](#-how-to-run)
- [Tech Stack](#-tech-stack)
- [Team](#-team)

---

## 🎯 Introduction
The Financial Buddy is an AI-powered system that analyzes a user's social media posts and transaction history to recommend personalized financial products, services, and educational content. It bridges the gap between everyday language and financial guidance by combining sentiment analysis, intent detection, and real-world behavioral profiling.

---

## 🎥 Demo
📹 Video Demo: (https://drive.google.com/drive/folders/1BWVRTLrlVVyq1oi0AcEGcdFab2eVjNfb?usp=sharing)

🖼️ Screenshots:
- 📌 Architecture Overview → [Architecture README](artifacts/arch/IntentArchitecture.md)
- 📊 Model Metrics → [Intent Model Metrics](artifacts/arch/IntentModelMetrics.md)
- 🧠 Profile + Transaction Analysis → [Transaction Module README](artifacts/arch/TransactionModel.md)

---

## 💡 Inspiration
Most financial recommendation platforms rely on credit scores or demographic data. But users express intent and concerns in language — through social media, through emotions, through behavior. We wanted to build a system that could understand those signals and respond with actionable, personalized financial recommendations.

---

## ⚙️ What It Does
- Accepts social media posts as input
- Detects intent using few-shot prompting with Mistral-7B
- Analyzes sentiment using FinBERT or RoBERTa
- Extracts co-occurring (collaborative) intents using embeddings
- Maps intent+sentiment to financial product recommendations
- Suggests learning resources using LLM-based reasoning
- Enriches profiles using transaction behavior (spending categories, lifestyle, risk appetite)
- **Comprehensive Profiling**: Analyzes customer data (transactions, demographics, social media) to build detailed personas
- **Transaction Analysis**: Categorizes users by spending habits like luxury spender or budget-conscious
- **Recommendation Engine**: Generates suggestions aligned with persona type
- **Social Media Insights**: Extracts needs from text and delivers aligned content
- **Comparison Support**: Incorporates both embedding-based, logic-based, and GenAI-based recommendations
- **Editable Personas**: Users can modify profile attributes like age, interests, or profession and receive real-time refreshed recommendations
- **Guest Access**: Users can test the system without registering, receiving recommendations through conversational chat
---

## 🛠️ How We Built It
- Used LangChain to orchestrate LLM calls for intent and learning prompts
- Integrated `mistralai/Mistral-7B-Instruct-v0.1` via Together.ai
- Trained co-occurrence matrix from batch predictions using `facebook/bart-large-mnli`
- Sentiment model comparison led to selection of `yiyanghkust/finbert-tone`
- Sentence embeddings with `all-MiniLM-L6-v2` + cosine similarity
- FAISS added as optional similarity engine
- Profiles generated from transaction MCC codes and spending patterns

---

## 🚧 Challenges We Faced

1️⃣ **Choosing the Right GenAI Model**  
We evaluated multiple LLMs like GPT-3.5, LLaMA-2, GPT-4All, Mistral, and Phi-2. The key challenge was balancing performance, inference cost, and ease of deployment. Cloud APIs provided better results but were costly, while local deployment of large models required significant resources.

2️⃣ **API Pricing & Quota Limits**  
OpenAI and Hugging Face APIs exceeded free-tier quotas. We adopted Together.ai for free access to high-quality models like Mistral and LLaMA.

3️⃣ **Resource Constraints for Large Models**  
Running large models like Mistral-7B and LLaMA-2 locally was not feasible due to RAM limits. We explored quantized formats (GGUF/GGML) but settled on API-based inference for reliability.

4️⃣ **Zero-shot vs Few-shot Prompting**  
Zero-shot classification led to inconsistent and off-target intents. We switched to Few-Shot prompting using Mistral-7B via LangChain, which gave better results.

5️⃣ **Dataset Scaling & Logical Coherence**  
We generated synthetic data to scale, but had to ensure realistic transaction patterns and sentiment-intent alignment. Example: investment categories shouldn’t overlap with travel purchases.

6️⃣ **Ensuring Efficient Real-time & Batch Processing**  
The system needed to support both modes. FAISS helped speed up retrieval, and LLM reranking handled personalization.

7️⃣ **Streamlit UI Challenges**  
Profile editing via Streamlit initially triggered unnecessary reruns. We fixed this by encapsulating profile input in `st.form()` to ensure data was saved before re-rendering.

8️⃣ **Persona & Financial Feature Engineering**  
We designed personas based on transaction traits like average spend, MCC codes, and debt-to-income ratios. These helped contextualize LLM prompts and personalize recommendations.

---

## 🏃 How to Run
```bash
# Clone the repository
git clone https://github.com/ewfx/aidhp-deep-thinkers.git

# Install dependencies
pip install -r requirements.txt

#Together AI api key token in .env file
# TOGETHER_API_KEY = "YOUR_API_KEY"

# Run the app (Streamlit)
streamlit run app.py
```

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit for UI & profile editor  
- **Backend**: Python + LangChain for LLM orchestration  
- **LLM APIs**: Together.ai (Mistral-7B)  
- **Sentiment Models**: FinBERT-Tone (finance-specific), RoBERTa (generic fallback)  
- **Intent Models**: BART / XLM-R for zero-shot baseline, Mistral for few-shot  
- **Embeddings**: Hugging Face (`all-MiniLM-L6-v2`)  
- **Vector Search**: Cosine similarity + FAISS (optional)  
- **Data Processing**: pandas, NumPy  
- **Data Store**: Local JSON / CSV for user profiles, products, transaction logs
---

## 👥 Team
- **Acanksha Jain** 
- **Aditya Singhal** 
---

> Want to explore deeper? Start with the [Intent Model Metrics](artifacts/arch/IntentModelMetrics.md) or [Architecture Overview](.artifacts/arch/IntentArchitecture.md).