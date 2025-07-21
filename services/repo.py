# This module manages Git operations and Copilot‐assisted PR merges (GitHub CLI + Copilot chat).

import subprocess
import logging

logger = logging.getLogger(__name__)

def checkout_code():
    try:
        subprocess.run(["gh", "repo", "clone", "BBrown-Dev/InvoiceBot.git"], check=True)
        logger.info("Code checkout complete.")
    except subprocess.CalledProcessError as e:
        logger.error("Git checkout failed", exc_info=True)
        raise

def push_metrics(successful, total):
    logger.info(f"Pushing metrics: {successful}/{total}")
    # Custom GitHub CLI logic here
