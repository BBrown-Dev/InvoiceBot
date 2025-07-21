
# Extracts text from each page of the PDF and returns
# a dict with at least 'invoice_number' and 'invoice_total'.


import pdfplumber
import logging

logger = logging.getLogger(__name__)

def from_pdf(filepath: str) -> dict:

    try:
        with pdfplumber.open(filepath) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # Simple extraction logic - looks for lines "Invoice Number: XXX" and "Amount Due: $YYY"
        invoice_number = None
        invoice_total = 0.0

        for line in text.splitlines():
            if "Invoice Number:" in line:
                invoice_number = line.split("Invoice Number:")[1].strip()
            if "Amount Due:" in line:
                amt = line.split("Amount Due:")[1].strip().lstrip("$")
                invoice_total = float(amt)

        record = {
            "file_path": filepath,
            "invoice_number": invoice_number,
            "invoice_total": invoice_total,
            "raw_text": text
        }

        logger.info(f"Parsed invoice {invoice_number} from {filepath}.")
        return record

    except Exception:
        logger.exception(f"Error parsing PDF: {filepath}")
        raise
