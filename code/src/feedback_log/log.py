import os
from datetime import datetime
import pandas as pd

FEEDBACK_LOG_PATH = "data/feedback_data/feedback_log.csv"

# Save feedback
def log_feedback(user_id, item_title, method, feedback_type):
    timestamp = datetime.now().isoformat()
    log_entry = pd.DataFrame([{ 
        "user_id": user_id, 
        "item_title": item_title, 
        "method": method, 
        "feedback_type": feedback_type, 
        "timestamp": timestamp
    }])
    if os.path.exists(FEEDBACK_LOG_PATH):
        log_entry.to_csv(FEEDBACK_LOG_PATH, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(FEEDBACK_LOG_PATH, index=False)