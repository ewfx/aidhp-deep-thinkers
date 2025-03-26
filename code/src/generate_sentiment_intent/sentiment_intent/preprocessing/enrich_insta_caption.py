import pandas as pd
from nlp_pipeline import batch_analyze_text

# Load dataset
input_path = "final_instagram_captions.csv"
df = pd.read_csv(input_path)

# Run the NLP pipeline on the 'caption' column
print("🔍 Running intent + sentiment enrichment on Instagram captions...")
enriched_df = batch_analyze_text(df, text_col="Caption", source_col=None)

# Save the enriched dataset
output_path = "data/sentiment_data/instagram_enriched.csv"
enriched_df.to_csv(output_path, index=False)
print(f"✅ Enriched data saved to {output_path}")
