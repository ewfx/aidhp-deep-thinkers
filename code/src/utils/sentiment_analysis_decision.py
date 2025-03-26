import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load your sentiment data
sentiments_df = pd.read_csv("data/user_data/sentiment_inputs.csv")

models_info = {
    "finbert-tone": {
        "name": "yiyanghkust/finbert-tone",
        "labels": ["Positive", "Neutral", "Negative"]
    },
    "prosus-finbert": {
        "name": "ProsusAI/finbert",
        "labels": ["positive", "neutral", "negative"]
    },
    "amphora-finbert": {
        "name": "nickwong64/bert-base-uncased-finance-sentiment",
        "labels": ["positive", "neutral", "negative"]
    }
}

loaded_models = {}
for key, info in models_info.items():
    tokenizer = AutoTokenizer.from_pretrained(info["name"])
    model = AutoModelForSequenceClassification.from_pretrained(info["name"])
    loaded_models[key] = {
        "tokenizer": tokenizer,
        "model": model,
        "labels": info["labels"]
    }

results = []

for _, row in sentiments_df.iterrows():
    user_id = row["user_id"]
    text = row["text"]
    model_outputs = {}

    for model_key, model_data in loaded_models.items():
        tokenizer = model_data["tokenizer"]
        model = model_data["model"]
        labels = model_data["labels"]

        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        outputs = model(**inputs)
        probs = softmax(outputs.logits, dim=1)[0]
        top_idx = torch.argmax(probs).item()

        model_outputs[model_key + "_label"] = labels[top_idx]
        model_outputs[model_key + "_confidence"] = round(probs[top_idx].item(), 2)

    results.append({
        "user_id": user_id,
        "text": text,
        **model_outputs
    })

results_df = pd.DataFrame(results)
results_df.to_csv("data/sentiment_data/sentiment_model_comparison.csv", index=False)
print("Model comparison saved to sentiment_model_comparison.csv")

# results_df["is_correct_finbert"] = results_df["finbert-tone_label"].str.lower() == results_df["true_label"].str.lower()
# accuracy = results_df["is_correct_finbert"].mean()
# print("Accuracy:", round(accuracy * 100, 2), "%")
