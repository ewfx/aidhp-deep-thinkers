from generate_sentiment_intent.sentiment_intent.models import run_finbert, run_roberta
from generate_sentiment_intent.sentiment_intent.collaborative_filtering.intent_labels import FINANCE_INTENTS, INTENT_LABELS,FINANCE_KEYWORDS
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from generate_sentiment_intent.sentiment_intent.nlp_pipeline import clean_text
import re
import emoji


# Load models once
bart_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def should_use_finbert(intent_list):
    return any(intent in FINANCE_INTENTS for intent in intent_list)

def is_financial_text(text):
    return any(kw in text.lower() for kw in FINANCE_KEYWORDS)

def route_sentiment_model(text, detected_intents):
    if should_use_finbert(detected_intents) or is_financial_text(text):
        return "finbert"
    else:
        return "roberta"

def get_sentiment_model(text, intents):
    if should_use_finbert(intents) or is_financial_text(text):
        return "finbert"
    else:
        return "roberta"

def analyze_text(text):
    text = clean_text(text)
    if not text :
        return None
    intent_result = bart_classifier(text, candidate_labels=INTENT_LABELS, multi_label=True)
    intents = [label for label, score in zip(intent_result["labels"], intent_result["scores"]) if score >= 0.5]
    intents = intents[:4]  # Limit to top 4 intents

    # Step 2: Route to sentiment model
    use_finbert = any(intent in FINANCE_INTENTS for intent in intents)
    sentiment, confidence = run_finbert(text) if use_finbert else run_roberta(text)

    return {
        "text": text,
        "intents": intents,
        "sentiment": sentiment,
        "confidence": confidence,
        "routed_model": "finbert" if use_finbert else "roberta"
    }

if __name__ == "__main__":
    example_text = "Markets are scary, but I'm still buying the dip in crypto and stocks."
    result = analyze_text(example_text)
    print(result)
    example_text2 = "Just attended the biggest concert of the year 🎤🎉"
    result2 = analyze_text(example_text2)
    print(result2)

