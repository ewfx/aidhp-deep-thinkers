from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from torch.nn.functional import softmax

# Load FinBERT (finance-specific sentiment model)
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
finbert_model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

# Load RoBERTa (general social sentiment)
roberta_classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Sentiment labels for FinBERT
FINBERT_LABELS = ['positive', 'neutral', 'negative']

# Run FinBERT on finance text
def run_finbert(text):
    inputs = finbert_tokenizer(text, return_tensors="pt", truncation=True)
    outputs = finbert_model(**inputs)
    probs = softmax(outputs.logits, dim=1)[0]
    labels = ['positive', 'neutral', 'negative']
    top_idx = torch.argmax(probs).item()
    sentiment = labels[top_idx]
    confidence = round(probs[top_idx].item(), 3)
    return sentiment, confidence

ROBERTA_LABELS = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

# Run RoBERTa on general/lifestyle text
def run_roberta(text):
    result = roberta_classifier(text)[0]
    sentiment = ROBERTA_LABELS[result["label"]]  # Map to actual sentiment
    confidence = round(result["score"], 3)
    return sentiment, confidence

# Example use
if __name__ == "__main__":
    finance_post = "Markets are crashing. I feel like I'm losing everything."
    lifestyle_post = "Just had the best sushi night ever with friends!"

    print("Finance Example:", run_finbert(finance_post))
    print("Lifestyle Example:", run_roberta(lifestyle_post))
    print("Finance Example 2:", run_finbert("Stocks trade are fine"))
