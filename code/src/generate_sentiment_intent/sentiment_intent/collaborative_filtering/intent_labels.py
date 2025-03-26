# Define your intent labels
intent_labels = [
    "financial management", "savings planning", "budgeting concern", "debt stress", "retirement planning",
    "financial literacy", "wealth building", "credit card interest", "travel card interest",
    "premium card curiosity", "EMI concern", "bank fee complaint", "risk mitigation", "market anxiety",
    "insurance interest", "income insecurity", "stocks investing", "mutual fund interest", "crypto investing",
    "SIP planning", "diversification intent", "account access issue", "transaction dispute",
    "feedback to provider", "product comparison", "food", "fashion", "luxury", "travel", "entertainment",
    "wellness", "fitness", "education", "self-improvement", "career growth", "motivation",
    "celebrating", "social sharing", "seeking advice", "complaining"
]

# Finance-related intent categories
FINANCE_INTENTS = {
    "financial management", "savings planning", "budgeting concern", "debt stress",
    "retirement planning", "financial literacy", "wealth building", "credit card interest",
    "travel card interest", "premium card curiosity", "EMI concern", "bank fee complaint",
    "risk mitigation", "market anxiety", "insurance interest", "income insecurity",
    "stocks investing", "mutual fund interest", "crypto investing", "SIP planning",
    "diversification intent"
}

# Complete label list (can be externalized)
INTENT_LABELS = list(FINANCE_INTENTS) + [
    "account access issue", "transaction dispute", "feedback to provider", "product comparison",
    "food", "fashion", "luxury", "travel", "entertainment", "wellness", "fitness",
    "education", "self-improvement", "career growth", "motivation", "celebrating",
    "social sharing", "seeking advice", "complaining"
]

FINANCE_KEYWORDS = [
    "stock", "invest", "crypto", "market", "debt", "loan", "retirement", 
    "saving", "mutual fund", "portfolio", "income", "interest", "EMI"
]