"""

# GenAI Hyperpersonalization Hackathon - Codebase Overview

## 📁 Folder Structure

-   **jobs/**: Contains all ETL and orchestration scripts.

    -   `ingest_*.py`: Individual ingestion jobs per dataset.
    -   `ingest_all.py`: Executes all ingestion jobs in batch.
    -   `build_features.py`: Builds customer features from raw ingested data.
    -   `generate_recommendations.py`: Runs the recommendation engine based on rules.
    -   `generate_business_insights.py`: Extracts actionable insights from features and recommendations.
    -   `export_outputs.py`: Exports outputs (features, recommendations, insights) to CSV files.

-   **utils/**: Common utility functions for DB operations, file handling, validation.

-   **feature_engineering/**: Contains logic to build features and feature utilities.

-   **recommendation_engine/**: Rule-based logic for financial product recommendations.

-   **insight_engine/**: Logic to generate business insights from processed data.

-   **config/**: Contains config file (`config.yaml`) for DB connection and file paths.

-   **outputs/**: Stores all final outputs in categorized folders:

    -   `features/`, `recommendations/`, `insights/`

-   **.env**: Environment variables (e.g., DB credentials if needed).

-   **requirements.txt**: All required Python packages for the project.

## ▶️ How to Run

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run data ingestion (all datasets):

    ```bash
    python jobs/ingest_all.py
    ```

3. Build customer features:

    ```bash
    python jobs/build_features.py
    ```

4. Generate recommendations:

    ```bash
    python jobs/generate_recommendations.py
    ```

5. Generate business insights:

    ```bash
    python jobs/generate_business_insights.py
    ```

6. Export all outputs:
    ```bash
    python jobs/export_outputs.py
    ```

## 📌 Notes

-   We use in-memory simulated DB via `utils/db_utils.py` (during hackathon).
-   All job scripts can run independently or sequentially.
-   Keep outputs under `outputs/` folder for submission or demo.

Happy hacking! 💡🚀
"""
