import streamlit as st
import os
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chat_models import ChatOpenAI
import ast
import re
# from langchain_community.chat_models import ChatTogether
# from langchain_community.chat_models import ChatTogether
# from langchain_together import ChatTogetherAI

# Intent categories
intent_categories = [
    "Budgeting & Expenses", "Savings & Planning", "Debt & Stress", "Investing & Wealth Building",
    "Credit & Cards", "Insurance Interest", "Market Sentiment", "Financial Literacy & Learning",
    "Career & Income Goals", "Product Issues", "Product Discovery", "Complaints & Frustration",
    "Lifestyle: Food & Fashion", "Lifestyle: Travel", "Lifestyle: Entertainment",
    "Lifestyle: Wellness", "Positive Milestones", "Community & Sharing", "Generic Financial Concern"
]

# Few-shot examples
examples = [
    {"post": "I'm tired of hidden charges on my card and struggling to manage my expenses.", "labels": ["Credit & Cards", "Budgeting & Expenses"]},
    {"post": "I really want to start saving for my future, even small steps count.", "labels": ["Savings & Planning"]},
    {"post": "The market makes me anxious, not sure how to invest safely.", "labels": ["Market Sentiment", "Investing & Wealth Building"]},
    {"post": "Just got promoted! Time to upgrade my lifestyle and maybe start investing.", "labels": ["Career & Income Goals", "Lifestyle: Luxury", "Investing & Wealth Building"]},
    {"post": "Having trouble accessing my account. Support hasn't responded.", "labels": ["Product Issues"]}
]

example_prompt = PromptTemplate(
    input_variables=["post", "labels"],
    template="Post: {post}\nIntent Categories: {labels}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=(
        "You are an AI assistant that detects high-level intent categories from social media posts.\n"
        "Choose the **2-3 most relevant categories** from this list:\n"
        f"{', '.join(intent_categories)}\n"
        "Respond with a JSON list of the matching categories."
    ),
    suffix="Post: {input_post}\nIntent Categories:\n[",
    input_variables=["input_post"]
)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Fetch the API key from environment variables
# MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"
# LLM setup (Together.ai example)

# llm = ChatTogether(
#     together_api_key=TOGETHER_API_KEY,
#     model="mistralai/Mistral-7B-Instruct",  # You can also try 'mistralai/Mixtral-8x7B-Instruct-v0.1'
#     temperature=0.3,
#     max_tokens=512
# )
llm = ChatOpenAI(
    openai_api_key="2ac32558c148559eb3bcb8e5a8538207ab3129e1341aedffdbdca198014f3bc8",              # your actual Together API key
    openai_api_base="https://api.together.xyz/v1",       # Together.ai's endpoint
    model_name="mistralai/Mistral-7B-Instruct-v0.1",          # Or Mixtral, Zephyr, etc.
    temperature=0.3
)

chain = few_shot_prompt | llm


def posts_to_intents(post: str) -> list:
    """
    Safely convert a single post to intent categories using the LLM.

    Args:
        post (str): A single social media post.

    Returns:
        List[str]: A list of predicted intent categories (empty if LLM fails).
    """
    response = chain.invoke({"input_post": post})
    raw_output = response.content
    print("📥 Raw LLM response:", raw_output)

    return extract_list_from_llm_response(raw_output)

def extract_list_from_llm_response(text):
    """
    Extract the first list-like structure from LLM response.
    """
    try:
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if match:
            list_str = match.group(0)
            return ast.literal_eval(list_str)
        else:
            print("⚠️ No list found in response.")
            return []
    except Exception as e:
        print("❌ Error extracting list:", e)
        return []

# Example use
if __name__ == "__main__":
    finance_post = "Markets are crashing. I feel like I'm losing everything."
    lifestyle_post = "Just had the best sushi night ever with friends!"

    response_finances = posts_to_intents(finance_post)
    response_lifestyle = posts_to_intents(lifestyle_post)
    print("response - ", response_finances)
    print("response_life - ", response_lifestyle)


