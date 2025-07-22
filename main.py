# This module contains a fully documented, modular Python workflow designed to
# automate the daily invoice processing tasks at TechAutomation Solutions.

#!/usr/bin/env python3

import os
import logging
from dotenv import load_dotenv
from services import repo, fetch, parse_invoices, validate, persist, report, notify

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

def run_daily_workflow():
    """Orchestrate the daily invoice processing workflow, including Git ops."""
    load_dotenv()              # Load .env secrets
    setup_logging()
    logger = logging.getLogger("main")

    try:
        # Step 1: Pull latest code so we're always in sync
        repo.checkout_code()

        # Step 2: Load invoice files
        files = fetch.list_invoice_files()
        if not files:
            logger.warning("No invoice files found. Exiting.")
            return

        processed = []
        for filepath in files:
            try:
                record = parse_invoices.from_pdf(filepath)
            except Exception as e:
                logger.error(f"Parsing failed for {filepath}", exc_info=True)
                notify.ops("Parsing Error", filepath, error=e)
                continue

            # Step 3: Validate business rules
            if not validate.invoice_record(record):
                logger.warning(f"Validation failed for {filepath}")
                notify.ops("Validation Error", filepath)
                continue

            # Step 4: Persist to CSV
            try:
                persist.to_csv(record)
            except Exception as e:
                logger.error(f"Persistence failed for {filepath}", exc_info=True)
                notify.ops("Persistence Error", filepath, error=e)
                continue

            processed.append(record)

        # Step 5: Generate & send summary
        summary_path = report.generate_daily_summary(processed)
        notify.email_report(summary_path)

        # Step 6: Push metrics back to GitHub
        repo.push_metrics(successful=len(processed), total=len(files))
        logger.info("Workflow completed successfully.")

    except Exception as e:
        logger.critical("Daily workflow failed", exc_info=True)
        notify.ops("Workflow Critical Failure", None, error=e)

if __name__ == "__main__":
    run_daily_workflow()

