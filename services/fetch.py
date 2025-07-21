# Retrieves files via local directory.

import os
import glob
import logging

logger = logging.getLogger(__name__)

def list_invoice_files():
    # Return a list of local PDF file paths from INVOICE_FOLDER.
    try:
        folder = os.getenv("INVOICE_FOLDER", "./invoices")
        pattern = os.path.join(folder, "*.pdf")
        files = glob.glob(pattern)
        logger.info(f"Found {len(files)} invoice file(s) in {folder}.")
        return files
    except Exception:
        logger.exception("Failed to list invoice files.")
        return []

