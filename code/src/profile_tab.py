import streamlit as st

def render_profile_tab(profile, sentiment_label=None, sentiment_score=None):
    """
    Renders the User Profile tab in the Streamlit app.

    Args:
        profile (pd.Series): The user's profile containing details like age, profession, income, etc.
        sentiment_label (str): The detected sentiment label for the user.
        sentiment_score (float): The confidence score for the detected sentiment.
    """
    st.subheader("👤 User Profile")
    st.markdown(f"**Age:** {profile['age']}  ")
    st.markdown(f"**Profession:** {profile['profession']}  ")
    st.markdown(f"**Income:** ₹{profile['income']:,}  ")
    st.markdown(f"**Risk Appetite:** {profile.get('risk_appetite', '')}  ")
    st.markdown(f"**Financial Goals:** {', '.join(profile.get('financial_goals', []))}  ")
    # st.markdown(f"**Sentiment Input:** _{profile.get('sentiment', '')}_")
    # st.markdown(f"**Detected Sentiment:** **{sentiment_label}** ({sentiment_score * 100:.1f}% confidence)")