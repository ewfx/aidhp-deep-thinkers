import re
import emoji
import pandas as pd
import torch
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
from generate_sentiment_intent.sentiment_intent.models import run_finbert, run_roberta
from generate_sentiment_intent.sentiment_intent.collaborative_filtering.intent_labels import FINANCE_INTENTS, INTENT_LABELS

# Load all models once
bart_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# ----------------------
# Preprocessing
# ----------------------
def clean_text(text, source="general"):
    text = str(text)
    text = emoji.demojize(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"[^a-zA-Z0-9\s:]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ----------------------
# Batch processing logic
# ----------------------
def batch_analyze_text(df, text_col, source_col=None, threshold=0.5, max_intents=3):
    enriched_rows = []
    tqdm.pandas()

    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = row[text_col]
        source = row[source_col] if source_col else "general"
        cleaned = clean_text(text, source)

        if cleaned:
            # Intent detection (multi-label)
            result = bart_classifier(cleaned, candidate_labels=INTENT_LABELS, multi_label=True)
            intents = [label for label, score in zip(result["labels"], result["scores"]) if score >= threshold][:max_intents]

            # Sentiment routing
            use_finbert = any(intent in FINANCE_INTENTS for intent in intents)
            sentiment, confidence = run_finbert(cleaned) if use_finbert else run_roberta(cleaned)

            enriched_rows.append({
                "cleaned_text": cleaned,
                "intents": intents,
                "sentiment": sentiment,
                "confidence": confidence,
                "routed_model": "finbert" if use_finbert else "roberta"
            })

    enriched_df = pd.concat([df.reset_index(drop=True), pd.DataFrame(enriched_rows)], axis=1)
    return enriched_df
