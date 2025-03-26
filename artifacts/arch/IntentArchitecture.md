# 🧠 Smart Financial Assistant – System Architecture

This document outlines the complete architecture of the smart financial recommendation system. It breaks down the key components, their responsibilities, and how data flows through the system—from social media input to final recommendation output.

---

## 📌 Architecture Diagram

Below is a high-level system flowchart showing how components interact step by step:

![Architecture Diagram](./arch/architecture.webp) <!-- Replace with actual path to your image -->

> 💡 This flow shows a left-to-right processing pipeline for a single user post.

---

## 🧾 System Components Breakdown

### 1. **Input**
- **Component**: `User Post (Text Input)`
- **Source**: Social media platforms (Instagram, Reddit, etc.)
- **Role**: User-generated content to be analyzed

---

### 2. **NLP Pipeline**

#### 🔍 Intent Detection
- **Model**: `mistralai/Mistral-7B-Instruct-v0.1` via LangChain (Few-shot prompting)
- **Purpose**: Extract high-level financial or lifestyle intents from user text

#### 🧠 Sentiment Analysis
- **Models**:
  - `FinBERT-Tone` → for finance-related posts
  - `RoBERTa` → fallback for general or lifestyle posts
- **Purpose**: Determine the emotional tone of the post (positive, negative, neutral)

#### 🔄 Exploratory Intent Matching
- **Embedding Model**: `all-MiniLM-L6-v2`
- **Similarity Engine**: Cosine similarity (FAISS optional)
- **Purpose**: Identify secondary (collaborative) intents related to primary ones

---

### 3. **Recommendation Engine**

#### 🎯 Primary Recommendation
- Mapped from top detected intent + sentiment

#### ✨ Exploratory Recommendation
- Mapped from related (collaborative) intents

#### 📘 Learning Content Generator
- Uses LLM prompt to generate educational tips/resources relevant to user’s situation

---

### 4. **Aggregator & Output**

- Deduplicates product titles across all posts
- Ensures one primary and one exploratory suggestion per post
- Aggregates sentiment across all posts to compute dominant emotional tone
- Final output includes:
  - Primary Recommendation
  - Exploratory Recommendation
  - Learning Resource

---

## ✅ Summary

- Built using open-source, free-accessible LLMs and embeddings
- Modular design enables future extension (e.g., user profile tracking, personalization)
- Designed to work for both single and multi-post user inputs



