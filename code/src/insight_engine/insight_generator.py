import pandas as pd

def product_trend_by_age_group(features_df):
    return features_df.groupby('age_group')['recommended_products'].explode().value_counts().reset_index(name='count')

def avg_sentiment_by_income(features_df):
    return features_df.groupby('income_bracket')['avg_sentiment_score'].mean().reset_index()

def high_spend_low_product(features_df):
    return features_df[(features_df['avg_spending'] > 1000) & (features_df['recommended_products'].apply(lambda x: len(x)==0))][['customer_id', 'avg_spending']]

def low_engaged_high_intent(features_df):
    return features_df[(features_df['avg_sentiment_score'] > 0.5) & (features_df['avg_spending'] < 200)][['customer_id', 'avg_sentiment_score', 'avg_spending']]
