import streamlit as st

def render_model_insights_tab(times, sentiment_time):
    # print("times", times)

    """
    Renders the Model Insights tab in the Streamlit app.

    Args:
        times (dict): Dictionary containing execution times for different models or processes.
    """
    st.subheader("📊 Model Metrics")
    for step, duration in times.items():
        if isinstance(duration, dict):
            st.markdown(f"**{step}:**")
            for sub_step, sub_duration in duration.items():
                st.markdown(f"**{sub_step}:** {sub_duration:.2f} seconds")
                # st.progress(min(sub_duration / max(duration.values()), 1.0))
        else:
            st.markdown(f"**{step}:** {duration:.2f} seconds")
            # st.progress(min(duration / max(times.values()), 1.0))
    
    st.markdown(f"**LLM Intent & Sentinment Extraction model:** {sentiment_time:.2f} seconds")
    st.divider()

    if "Similarity Score" in times:
        st.markdown(f"**⏱ Cosine Similarity Execution Time:** {times['Similarity Score'].get('cosine', 'N/A')} seconds")
        st.markdown(f"**⏱ Faiss Similarity Execution Time:** {times['Similarity Score'].get('faiss', 'N/A')} seconds")
        st.markdown(f"**⏱ Sentence Transformer Execution Time:** {times['Similarity Score'].get('sentenceTransformer', 'N/A')} seconds")

    if st.button("📄 Show Sentiment Model Evaluation Summary"):
        st.markdown("""
        **Objective:** Evaluate and select a finance-domain-appropriate sentiment analysis model for powering personalized recommendations.

        **Models Evaluated:**
        - `yiyanghkust/finbert-tone` (Financial news tone)
        - `ProsusAI/finbert` (General finance)
        - `amphora/bert-base-finance-sentiment` (Finance + Reddit)

        **Evaluation Results:**
        | Model               | Accuracy | Avg Confidence | Notes                                   |
        |--------------------|----------|----------------|-----------------------------------------|
        | finbert-tone        | 86.6%    | 0.82           | Most consistent with short user inputs  |
        | prosus-finbert      | 80.0%    | 0.77           | Good on formal statements               |
        | amphora-finbert     | 73.3%    | 0.71           | Struggled with emotional phrasing       |

        **Selected Model:** `yiyanghkust/finbert-tone`
        - Best suited for user-generated financial concern texts
        - Lightweight and fast for PoC deployment

        **Next Steps:**
        - Optional fine-tuning with labeled user data
        - Integration with intent detection for deeper personalization
        """)