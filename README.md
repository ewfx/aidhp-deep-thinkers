# 🚀 Financial AI Buddy

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This project is a Streamlit-based AI-powered customer recommendation engine that analyzes transaction history, social media activity, and demographic details to generate personalized recommendations.

## 🎥 Demo 
📹 [Video Demo](https://drive.google.com/drive/folders/1BWVRTLrlVVyq1oi0AcEGcdFab2eVjNfb?usp=sharing)

## 💡 Inspiration
Our application addresses the need for a *Generative AI-driven solution* aimed at enhancing hyper-personalization. By leveraging advanced algorithms, the application analyzes customer profiles, social media activity, purchase history, sentiment data, and demographic details. This comprehensive analysis provides actionable insights that empower businesses to optimize customer engagement effectively.

## ⚙ What It Does
- *Comprehensive Profiling*: Analyzes customer data (transactions, demographics, social media, etc.) for detailed personas.
- *Transaction Analysis*: Identifies personas based on spending behavior (luxury, budget, etc.).
- *Recommendation*: Provides recommendations based on the identified persona of the user.
- *Social Media Insights*: Provides recommendations based on social media activity and intent.
- *Comparision*: Comparable Embedded, Logic and GenAI based recommendations.
- *Editable Personas*: Users can update their personas and receive refreshed, personalized recommendations.
- *Guest Access*: New users can try out features without registering by providing preferences to receive instant recommendations.

## 🛠️ How We Built It
- 

## 🚧 Challenges We Faced During Development
1️⃣ Choosing the Right GenAI Model

Evaluated models like GPT-3.5, LLaMA-2, GPT-4All, Mistral, and Phi-2.

Needed a balance between performance, inference cost, and local deployment feasibility.

Trade-off: Cloud APIs offer better results but are expensive; local models require high resources.

2️⃣ API Pricing & Quota Limits

OpenAI API exceeded free-tier quota, requiring a paid plan.

Hugging Face Inference API needed a Pro subscription for some models.

Workaround: Shifted to Together.AI API, which provides free inference for Mistral & LLaMA models.

3️⃣ Resource Constraints for Large Models

LLaMA-2, Mistral-7B, and Phi-2 were too large to run locally on limited RAM.

Needed quantization (GGUF/GGML) or API-based inference.

Switching to API-based models resolved memory issues.

4️⃣ Dataset Scaling & Logical Coherence Issues

Generated synthetic data to expand sample size.

Needed to ensure realistic transaction behaviors, including:

Logical transaction categories (e.g., Investment ≠ Flights)

Coherent social media sentiments

Meaningful customer preferences

5️⃣ Ensuring Efficient Real-time & Batch Processing

Needed both real-time and batch recommendations.

Integrated FAISS for fast retrieval and LLM reranking for personalization.

6️⃣ Streamlit UI Challenges

Profile editing triggered unnecessary re-runs, causing issues with data persistence.

Fix: Used st.form() to control user input submission, ensuring saving happens before refresh.

7️⃣ Persona & Financial Feature Engineering

Defined personas based on risk appetite, spending behavior, debt-to-income ratio.

Derived meaningful financial personas to align with recommendations.

## 🏃 How to Run
1. Clone the repository  

   git clone https://github.com/your-repo.git

2. Install dependencies  
   
   a. pip install -r requirements.txt (for Python)
   b. Generate your Together.API token and add in the .env file

3. Run the project  
   
   npm start  # or python app.py


## 🏗 Tech Stack
- 🔹 Frontend: Built with Streamlit, featuring a user-friendly UI
- 🔹 Backend: Built with python
- 🔹 API: Together.Ai API 
- 🔹 Main GenAI-Model: Mistral-7B-Instruct

## 👥 Team
- *Acanksha Jain* - [GitHub](#) | [LinkedIn](#)
- *Aditya Singhal* - [GitHub](#)[LinkedIn](#)