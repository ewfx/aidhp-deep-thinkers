from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
SENTIMENT_PATH = os.path.join(BASE_DIR, "data", "user_data", "sentiment_inputs.csv")
# Load sentiment model
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def analyze_sentiment(user_id):
    sentiments = pd.read_csv(SENTIMENT_PATH)
    text = sentiments[sentiments.user_id == user_id]["text"].values[0]
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)[0]
    labels = ['Positive', 'Neutral', 'Negative']
    top_idx = torch.argmax(probs).item()
    return labels[top_idx], round(probs[top_idx].item(), 2)