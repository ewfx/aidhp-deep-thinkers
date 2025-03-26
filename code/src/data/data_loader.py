# Load data
import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
TRANSACTIONS_PATH = os.path.join(BASE_DIR, "data", "user_data", "transactions.csv")
INVESTMENTS_PATH = os.path.join(BASE_DIR, "data", "user_data", "investments.csv")
ENGAGEMENTS_PATH = os.path.join(BASE_DIR, "data", "user_data", "engagements.csv")
SENTIMENT_PATH = os.path.join(BASE_DIR, "data", "user_data", "sentiment_inputs.csv")
PRODUCTS_PATH = os.path.join(BASE_DIR, "data", "user_data", "products.csv")
CONTENT_PATH = os.path.join(BASE_DIR, "data", "user_data", "content.csv")
USER_PERSONAS_PATH = os.path.join(BASE_DIR, "code", "src", "generate_personas", "user_personas_with_posts.json")

# @st.cache_data
def load_data():
    transactions = pd.read_csv(TRANSACTIONS_PATH)
    investments = pd.read_csv(INVESTMENTS_PATH)
    engagements = pd.read_csv(ENGAGEMENTS_PATH)
    sentiments = pd.read_csv(SENTIMENT_PATH)
    products = pd.read_csv(PRODUCTS_PATH)
    content = pd.read_csv(CONTENT_PATH)
    with open(USER_PERSONAS_PATH) as f:
        personas = pd.read_json(f)
    return products, content

def load_personas(): 
    with open(USER_PERSONAS_PATH) as f:
        personas = pd.read_json(f)
    return personas