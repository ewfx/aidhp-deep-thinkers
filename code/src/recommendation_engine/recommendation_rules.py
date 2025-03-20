def rule_based_recommendation(customer_row):
    recommendations = []
    if customer_row['income_bracket'] == 'High' and customer_row['avg_spending'] > 1000:
        recommendations.append("Premium Credit Card")
    if customer_row['income_bracket'] in ['Medium', 'High'] and customer_row['age_group'] in ['Adult', 'Middle-aged']:
        recommendations.append("Home Loan")
    if customer_row['avg_sentiment_score'] > 0.5:
        recommendations.append("Investment Advisory Services")
    if customer_row['age_group'] == 'Youth':
        recommendations.append("Student Savings Account")
    return recommendations