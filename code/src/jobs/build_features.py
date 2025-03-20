from feature_engineering.customer_features import generate_customer_features
from utils.db_utils import insert_into_db

if __name__ == "__main__":
    features_df = generate_customer_features()
    insert_into_db(features_df, table_name="customer_features")