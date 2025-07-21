"""
    Given a list of invoice dicts, writes a summary CSV with:
      - total_invoices
      - total_amount
      - average_amount
    Returns path to summary file.
    """

import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)
SUMMARY_PATH = os.getenv("SUMMARY_CSV", "daily_summary.csv")

def generate_daily_summary(records: list) -> str:

    try:
        df = pd.DataFrame(records)
        summary = {
            "total_invoices": len(df),
            "total_amount": df["invoice_total"].sum(),
            "average_amount": df["invoice_total"].mean() if len(df) else 0
        }
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(SUMMARY_PATH, index=False)
        logger.info(f"Daily summary written to {SUMMARY_PATH}.")
        return SUMMARY_PATH
    except Exception:
        logger.exception("Failed to generate summary report.")
        raise
