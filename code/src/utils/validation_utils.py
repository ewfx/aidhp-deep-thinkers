def validate_customer_data(df):
    df.dropna(subset=['customer_id', 'name'], inplace=True)
    return df