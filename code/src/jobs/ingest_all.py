from ingest_customers import ingest_customer_data
from ingest_transactions import ingest_transaction_data
from ingest_sentiments import ingest_sentiment_data
from ingest_organizations import ingest_organization_data

if __name__ == "__main__":
    ingest_customer_data()
    ingest_transaction_data()
    ingest_sentiment_data()
    ingest_organization_data()