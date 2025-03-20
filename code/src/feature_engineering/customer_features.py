import pandas as pd
from utils.db_utils import insert_into_db
from utils.file_utils import load_csv_file
from feature_engineering.feature_utils import (
    compute_age_group, compute_income_bracket,
    compute_spending_score, aggregate_sentiment
)
import yaml

CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

# Load all datasets
def load_all_datasets():
    customers = load_csv_file(config['data_sources']['customers'])
    transactions = load_csv_file(config['data_sources']['transactions'])
    sentiments = load_csv_file(config['data_sources']['sentiments'])
    organizations = load_csv_file(config['data_sources']['organizations'])
    return customers, transactions, sentiments, organizations


def generate_customer_features():
    customers, transactions, sentiments, organizations = load_all_datasets()

    # Age group & Income bracket
    customers['age_group'] = customers['age'].apply(compute_age_group)
    customers['income_bracket'] = customers['income_per_year'].apply(compute_income_bracket)

    # Spending Score
    spending_df = compute_spending_score(transactions)
    customers = pd.merge(customers, spending_df, on='customer_id', how='left')

    # Sentiment Score
    sentiment_df = aggregate_sentiment(sentiments)
    customers = pd.merge(customers, sentiment_df, on='customer_id', how='left')

    # Add organization-based features if needed later

    # Fill missing values
    customers.fillna({"avg_spending": 0, "avg_sentiment_score": 0}, inplace=True)

    return customers