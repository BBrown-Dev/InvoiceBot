# This module manages Git operations and Copilot‐assisted PR merges (GitHub CLI + Copilot chat).

import subprocess
import logging

logger = logging.getLogger(__name__)

def checkout_code():
    """Fetches the latest from origin/main into the workspace."""
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        logger.info("Git pull successful.")
    except subprocess.CalledProcessError:
        logger.exception("Git pull failed.")
        raise

def push_metrics(successful: int, total: int):
    """Commits and pushes a simple metrics file back to the repo."""
    try:
        msg = f"Processed {successful}/{total} invoices"
        # Write metrics.txt
        with open("metrics.txt", "w") as f:
            f.write(msg)

        # Stage changes
        subprocess.run(["git", "add", "."], check=True)
        # Check if there are staged changes
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode != 0:
            # There are changes to commit
            subprocess.run(["git", "commit", "-m", msg], check=True)
            subprocess.run(["git", "push"], check=True)
        else:
            # No changes to commit
            print("No changes to commit.")
        # subprocess.run(["git", "add", "metrics.txt"], check=True)
        # subprocess.run(["git", "commit", "-m", msg], check=True)
        # subprocess.run(["git", "push", "origin", "main"], check=True)
        logger.info("Metrics pushed to GitHub.")
    except subprocess.CalledProcessError:
        logger.exception("Failed to push metrics.")
        raise