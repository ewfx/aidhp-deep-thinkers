import pandas as pd
from utils.db_utils import insert_into_db, fetch_from_db
from recommendation_engine.recommendation_rules import rule_based_recommendation

if __name__ == "__main__":
    df = fetch_from_db("customer_features")
    df['recommended_products'] = df.apply(rule_based_recommendation, axis=1)
    insert_into_db(df[['customer_id', 'recommended_products']], table_name="customer_recommendations")