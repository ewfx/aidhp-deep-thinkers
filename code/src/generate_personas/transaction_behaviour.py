import pandas as pd
import json
import os
# Dictionary mapping MCC codes to categories
# Construct the absolute path to mcc_codes.json
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
mcc_path = os.path.join(BASE_DIR, "data", "user_data", "mcc_codes.json")

with open(mcc_path, "r") as f:
    mcc_mapping = json.load(f)
    
travel_mccs = ["3000", "3500", "4511", "4582", "4722", "7011"]
entertainment_mccs = ["7832", "7922", "5813"]  # Movies, concerts, bars
tech_mccs = ["5734", "7372", "4816"]  # Electronics, software, digital goods
subscription_mccs = ["4899", "5968", "6300"]
luxury_mccs = ["5944", "5691", "5999"]
business_mccs = ["7392", "7311", "8742"]
investment_mccs = ["6211", "6051"]
family_mccs = ["8211", "8351", "5641"]
health_mccs = ["8099", "8011", "8050"]

def build_transaction_behavior_features(user_id, profile):
    transactions_df = pd.read_csv(BASE_DIR + "/data/user_data/transactions_df_merged.csv")

    # Get transactions for the given user_id
    user_txn = transactions_df[transactions_df["client_id"] == user_id]
    if user_txn.empty:
        print(f"No transactions found for client_id: {user_id}")
        return

    # Generate personas for the user
    transaction_persona = generate_transaction_personas(user_txn)
    # print(transaction_persona)

    # Add transaction_persona object to the profile of user.
    profile["transaction_persona"] = transaction_persona
    profile['risk_appetite'] = transaction_persona['risk_appetite']
    # print(profile)
    return profile


def generate_transaction_personas(transactions_df):
    """Generate personas from transaction data using actual MCC categories."""
    client_id = transactions_df["client_id"].iloc[0]
    transactions = transactions_df
    avg_spend = transactions["amount"].mean()
    top_category = get_top_category(transactions)
    age = transactions["current_age"].iloc[0]
    total_debt = transactions["total_debt"].iloc[0]
    yearly_income = transactions["yearly_income"].iloc[0]
    travel_freq = transactions[transactions["mcc"].astype(str).isin(travel_mccs)].shape[0]
    entertainment_count = transactions[transactions["mcc"].astype(str).isin(entertainment_mccs)].shape[0]
    tech_count = transactions[transactions["mcc"].astype(str).isin(tech_mccs)].shape[0]
    subscription_count = transactions[transactions["mcc"].astype(str).isin(subscription_mccs)].shape[0]
    luxury_spend_ratio = transactions[transactions["mcc"].astype(str).isin(luxury_mccs)]["amount"].sum() / transactions["amount"].sum()
    business_spend_ratio = transactions[transactions["mcc"].astype(str).isin(business_mccs)]["amount"].sum() / transactions["amount"].sum()
    investment_count = transactions[transactions["mcc"].astype(str).isin(investment_mccs)].shape[0]
    family_spend_count = transactions[transactions["mcc"].astype(str).isin(family_mccs)].shape[0]
    health_spend_count = transactions[transactions["mcc"].astype(str).isin(health_mccs)].shape[0]

    persona = {
        "client_id": client_id,
        "spender_type": classify_spender(avg_spend, transactions),
        "top_spending_category": top_category,
        "travel_frequency": "Frequent Traveler" if travel_freq > 5 else "Occasional Traveler",
        "entertainment_lover": entertainment_count > 3,
        "tech_enthusiast": tech_count > 3,
        "subscription_enthusiast": subscription_count > 3,
        "luxury_spender": bool(luxury_spend_ratio > 0.3),
        "business_owner": bool(business_spend_ratio > 0.3),
        "frequent_investor": investment_count > 5,
        "family_oriented": family_spend_count > 5,
        "health_wellness_focused": health_spend_count > 5,
        "risk_appetite": determine_risk_appetite(age, total_debt, yearly_income)
    }


    return persona

def classify_spender(avg_spend, transactions):
    """Categorize users based on spending amount and payment method."""
    debit_card_usage = transactions[transactions["card_type"] == "Debit"].shape[0]
    grocery_spend = transactions[transactions["mcc"].map(mcc_mapping).str.contains("Grocery|Utilities", na=False)]["amount"].sum()
    
    if debit_card_usage > transactions.shape[0] * 0.5 and grocery_spend > 0.3 * transactions["amount"].sum():
        return "Budget-Conscious Shopper"
    elif avg_spend > 1000:
        return "Luxury Spender"
    elif avg_spend > 500:
        return "Moderate Spender"
    else:
        return "General Shopper"

def get_top_category(transactions):
    """Find the most common spending category for a user based on MCC codes."""
    mapped_categories = transactions["mcc"].astype(str).map(mcc_mapping)
    return mapped_categories.mode()[0] if not mapped_categories.empty else "Unknown"

def determine_risk_appetite(age, total_debt, yearly_income):
    """Determine risk appetite based on age and debt-to-income ratio."""
    debt_ratio = total_debt / yearly_income if yearly_income > 0 else 1
    
    if age < 30 and debt_ratio < 0.3:
        return "High"
    elif 30 <= age <= 50 and debt_ratio < 0.5:
        return "Moderate"
    else:
        return "Low"

if __name__ == '__main__':
    with open("code/src/generate_personas/user_personas_with_posts.json") as f:
        personas = pd.read_json(f)
    # personas, transactions, investments, engagements, sentiments, products, content = load_data()
    selected_user_id = "U002"
    profile = personas[personas.user_id == selected_user_id].iloc[0]
    build_transaction_behavior_features(selected_user_id, profile)