import pandas as pd
from utils.db_utils import insert_into_db
from utils.file_utils import load_csv_file
from utils.validation_utils import validate_customer_data
import yaml

CONFIG_PATH = "config/config.yaml"

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

def ingest_customer_data():
    file_path = config['data_sources']['customers']
    df = load_csv_file(file_path)
    df = validate_customer_data(df)
    insert_into_db(df, table_name='customers')

if __name__ == "__main__":
    ingest_customer_data()