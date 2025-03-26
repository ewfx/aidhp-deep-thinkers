# the purpose of this script is to identify the best working model for classifying the intent of the posts
# the script will load the sentiment data which has been manually labelled for intent and the models to be evaluated
# we will be using that true intent for the evaluation
# once we have the intent model defined - we would be using it to classify the semantic intent of the posts
# and then we will use it to work on the real data to identify the intent correlations

import pandas as pd
from transformers import pipeline
from sklearn.metrics import jaccard_score
import torch
import numpy as np
from ast import literal_eval
from collaborative_filtering.intent_labels import intent_labels
import time
import os

# Define the path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "intent_labeled_posts.csv")

# Print the current working directory and the CSV file path for debugging
print("Current working directory:", os.getcwd())
print("CSV file path:", csv_file_path)

# Load the data
df = pd.read_csv(csv_file_path)
df["mapped_intents"] = df["mapped_intents"].apply(literal_eval)

# Set device (use GPU if available)
device = 0 if torch.cuda.is_available() else -1

# Load zero-shot pipelines
print("Loading models...")
#it has been store in cache to avoid downloading again
classifier_bart = pipeline("zero-shot-classification", 
                           model="facebook/bart-large-mnli", 
                           cache_dir="./hf_cache",
                           device=device)

classifier_xlm = pipeline("zero-shot-classification", 
                          model="joeddav/xlm-roberta-large-xnli", 
                          cache_dir="./hf_cache",
                           device=device)


def compute_jaccard(true, pred):
    true_set = set(true)
    pred_set = set(pred)
    if not true_set and not pred_set:
        return 1.0
    return len(true_set & pred_set) / len(true_set | pred_set)

## Store results
results_old_way = []
start_model_no_batch = time.time()

print("Running predictions...")
for idx, row in df.iterrows():
    post = row["post"]
    true_intents = row["mapped_intents"]

    # BART prediction
    result_bart = classifier_bart(post, candidate_labels=intent_labels, multi_label=True)
    pred_bart = [label for label, score in zip(result_bart["labels"], result_bart["scores"]) if score > 0.3]

    # XLM-RoBERTa prediction
    result_xlm = classifier_xlm(post, candidate_labels=intent_labels, multi_label=True)
    pred_xlm = [label for label, score in zip(result_xlm["labels"], result_xlm["scores"]) if score > 0.3]

    # Store results
    results_old_way.append({
        "post": post,
        "true_intents": true_intents,
        "bart_pred": pred_bart,
        "xlm_pred": pred_xlm,
        "jaccard_bart": compute_jaccard(true_intents, pred_bart),
        "jaccard_xlm": compute_jaccard(true_intents, pred_xlm),
        "precision@1_bart": 1 if set(pred_bart[:1]) & set(true_intents) else 0,
        "precision@1_xlm": 1 if set(pred_xlm[:1]) & set(true_intents) else 0,
    })

# Save results
results_old_df = pd.DataFrame(results_old_way)
results_old_df.to_csv(os.path.join(script_dir, "data/sentiment_data/intent_model_comparison_results_no_batch_sizecsv.csv"), index=False)

# Show average scores
print("=== Model Evaluation Summary old way ===")
print("BART - Avg Jaccard:", round(results_old_df["jaccard_bart"].mean(), 3))
print("XLM-RoBERTa - Avg Jaccard:", round(results_old_df["jaccard_xlm"].mean(), 3))
print("BART - Precision@1:", round(results_old_df["precision@1_bart"].mean(), 3))
print("XLM - Precision@1:", round(results_old_df["precision@1_xlm"].mean(), 3))

model_no_batch_time = time.time() - start_model_no_batch
print("Time taken without batch processing:", model_no_batch_time)

# Process in batches - to increase the speed
batch_size = 8
#Store in result
results = []
start_model_batch = time.time()

for i in range(0, len(df), batch_size):
    batch_df = df.iloc[i:i + batch_size]
    posts = batch_df["post"].tolist()
    true_intents_list = batch_df["mapped_intents"].tolist()

    # Get predictions for BART
    result_bart = classifier_bart(posts, candidate_labels=intent_labels, multi_label=True, batch_size=batch_size)
    pred_bart_list = [[label for label, score in zip(res["labels"], res["scores"]) if score > 0.3] for res in result_bart]

    # Get predictions for XLM-RoBERTa
    result_xlm = classifier_xlm(posts, candidate_labels=intent_labels, multi_label=True, batch_size=batch_size)
    pred_xlm_list = [[label for label, score in zip(res["labels"], res["scores"]) if score > 0.3] for res in result_xlm]

    # Store batch results
    for post, true_intents, pred_bart, pred_xlm in zip(posts, true_intents_list, pred_bart_list, pred_xlm_list):
        results.append({
            "post": post,
            "true_intents": true_intents,
            "bart_pred": pred_bart,
            "xlm_pred": pred_xlm,
            "jaccard_bart": compute_jaccard(true_intents, pred_bart),
            "jaccard_xlm": compute_jaccard(true_intents, pred_xlm),
            "precision@1_bart": 1 if set(pred_bart[:1]) & set(true_intents) else 0,
            "precision@1_xlm": 1 if set(pred_xlm[:1]) & set(true_intents) else 0,
        })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(script_dir, "data/sentiment_data/intent_model_comparison_results_batch_size.csv"), index=False)

# Show average scores
print("=== Model Evaluation Summary ===")
print("BART - Avg Jaccard:", round(results_df["jaccard_bart"].mean(), 3))
print("XLM-RoBERTa - Avg Jaccard:", round(results_df["jaccard_xlm"].mean(), 3))
print("BART - Precision@1:", round(results_df["precision@1_bart"].mean(), 3))
print("XLM - Precision@1:", round(results_df["precision@1_xlm"].mean(), 3))

model_batch_time = time.time() - start_model_batch
print("Time taken without batch processing:", model_batch_time)
