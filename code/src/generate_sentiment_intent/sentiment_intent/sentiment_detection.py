from generate_sentiment_intent.sentiment_intent.models import run_finbert, run_roberta
# from sentiment_intent.models import run_finbert, run_roberta

FINANCE_KEYWORDS = [
    "stock", "invest", "investment", "equity", "trading", "market", "fund", "portfolio",
    "crypto", "bitcoin", "ethereum",
    "debt", "loan", "emi", "borrow", "credit", "interest", "bill", "due", "repayment",
    "saving", "save", "savings", "spending", "budget", "expense", "cashflow",
    "retirement", "pension", "401k", "nps",
    "salary", "income", "paycheck", "tax", "insurance", "premium", "cover"
]

finance_intents = [
    "Budgeting & Expenses",
    "Savings & Planning",
    "Debt & Stress",
    "Investing & Wealth Building",
    "Credit & Cards",
    "Insurance Interest",
    "Market Sentiment",
    "Financial Literacy & Learning",
    "Career & Income Goals",
    "Product Issues",
    "Product Discovery",
    "Complaints & Frustration",
    "Generic Financial Concern"
]


def is_finance_context(text):
    text = text.lower()
    return any(keyword in text for keyword in FINANCE_KEYWORDS)

def is_finance_post(text, detected_intents=None):
    text = text.lower()
    keyword_match = any(keyword in text for keyword in FINANCE_KEYWORDS)

    intent_match = False
    if detected_intents:
        intent_match = any(intent in finance_intents for intent in detected_intents)

    return keyword_match or intent_match

def get_sentiment(text, detected_intents=None):
    # print(" we are for sentiment -", text, " with detected intents -",  detected_intents)
    if is_finance_post(text, detected_intents):
        sentiment = run_finbert(text)
    else:
        sentiment = run_roberta(text)
    # print(" you gave the sentiment - ", sentiment)
    
    return sentiment[0]

if __name__ == "__main__":
    finance_post = "Markets are crashing. I feel like I'm losing everything."
    lifestyle_post = "Just had the best sushi night ever with friends!"

    response_finances = get_sentiment(finance_post)
    response_lifestyle = get_sentiment(lifestyle_post)
    print("response - ", response_finances)
    print("response_life - ", response_lifestyle)



