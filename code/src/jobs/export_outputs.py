import os
from utils.db_utils import fetch_from_db

OUTPUT_DIR = "outputs"
FEATURES_DIR = os.path.join(OUTPUT_DIR, "features")
RECOMMENDATIONS_DIR = os.path.join(OUTPUT_DIR, "recommendations")
INSIGHTS_DIR = os.path.join(OUTPUT_DIR, "insights")

os.makedirs(FEATURES_DIR, exist_ok=True)
os.makedirs(RECOMMENDATIONS_DIR, exist_ok=True)
os.makedirs(INSIGHTS_DIR, exist_ok=True)

if __name__ == "__main__":
    df_features = fetch_from_db("customer_features")
    df_recos = fetch_from_db("customer_recommendations")
    df_insights = fetch_from_db("business_insights")  # Simulated placeholder

    df_features.to_csv(os.path.join(FEATURES_DIR, "customer_features.csv"), index=False)
    df_recos.to_csv(os.path.join(RECOMMENDATIONS_DIR, "customer_recommendations.csv"), index=False)
    df_insights.to_csv(os.path.join(INSIGHTS_DIR, "business_insights.csv"), index=False)

    print("✅ Outputs exported to 'outputs/' directory")
