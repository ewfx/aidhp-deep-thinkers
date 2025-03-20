from utils.db_utils import fetch_from_db
from insight_engine.insight_generator import (
    product_trend_by_age_group,
    avg_sentiment_by_income,
    high_spend_low_product,
    low_engaged_high_intent
)

if __name__ == "__main__":
    df = fetch_from_db("customer_features")

    print("\nTop Products by Age Group:")
    print(product_trend_by_age_group(df))

    print("\nAverage Sentiment Score by Income Bracket:")
    print(avg_sentiment_by_income(df))

    print("\nHigh Spenders with No Recommendations:")
    print(high_spend_low_product(df))

    print("\nHigh Intent but Low Engagement Customers:")
    print(low_engaged_high_intent(df))