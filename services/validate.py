# Validates that invoice_total > 0 and invoice_number exists.

import logging

logger = logging.getLogger(__name__)

def invoice_record(record: dict) -> bool:

    try:
        num = record.get("invoice_number")
        total = record.get("invoice_total", 0)
        valid = bool(num) and float(total) > 0
        logger.info(
            f"Validation {'passed' if valid else 'failed'} for invoice {num}."
        )
        return valid
    except Exception:
        logger.exception("Exception during validation.")
        return False
