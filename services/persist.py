# This module provides functionality to persist invoice data to a CSV file.
# Appends a single invoice record to a CSV. Creates file if needed.

import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)
CSV_PATH = os.getenv("PERSISTED_CSV", "persisted_invoices.csv")

def to_csv(record: dict):

    try:
        df = pd.DataFrame([record])
        if os.path.exists(CSV_PATH):
            df.to_csv(CSV_PATH, mode="a", header=False, index=False)
        else:
            df.to_csv(CSV_PATH, index=False)
        logger.info(f"Appended invoice {record.get('invoice_number')} to {CSV_PATH}.")
    except Exception:
        logger.exception("Failed to write record to CSV.")
        raise
