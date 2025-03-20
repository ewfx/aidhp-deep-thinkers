import pandas as pd
from utils.db_utils import insert_into_db
from utils.file_utils import load_csv_file
import yaml

CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

def ingest_transaction_data():
    file_path = config['data_sources']['transactions']
    df = load_csv_file(file_path)
    insert_into_db(df, table_name='transactions')

if __name__ == "__main__":
    ingest_transaction_data()