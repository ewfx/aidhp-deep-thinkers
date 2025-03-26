import pandas as pd
from nlp_pipeline import batch_analyze_text

# Load Reddit dataset
input_path = "data/sentiment_data/reddit_data.csv"
df = pd.read_csv(input_path)

# Run the NLP pipeline on the 'post' column
print("🔍 Running intent + sentiment enrichment on Reddit posts...")
enriched_df = batch_analyze_text(df, text_col="title", source_col=None)

# Save the enriched dataset
output_path = "data/sentiment_data/reddit_enriched_output.csv"
enriched_df.to_csv(output_path, index=False)
print(f"✅ Enriched data saved to {output_path}")
