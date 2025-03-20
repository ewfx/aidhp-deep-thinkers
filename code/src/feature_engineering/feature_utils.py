import pandas as pd


def compute_age_group(age):
    if age < 25:
        return "Youth"
    elif age < 45:
        return "Adult"
    elif age < 65:
        return "Middle-aged"
    else:
        return "Senior"


def compute_income_bracket(income):
    if income < 30000:
        return "Low"
    elif income < 70000:
        return "Medium"
    else:
        return "High"


def compute_spending_score(transactions_df):
    spending = transactions_df.groupby('customer_id')['amount'].mean().reset_index()
    spending.columns = ['customer_id', 'avg_spending']
    return spending


def aggregate_sentiment(sentiment_df):
    sentiment = sentiment_df.groupby('customer_id')['sentiment_score'].mean().reset_index()
    sentiment.columns = ['customer_id', 'avg_sentiment_score']
    return sentiment