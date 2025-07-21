# This module handles notifications via email and local ops alerts.
# Sends the daily summary CSV via SMTP email. Expects SMTP_SERVER, SMTP_PORT, EMAIL_FROM, EMAIL_TO in .env.


import os
import smtplib
import logging
from email.message import EmailMessage

logger = logging.getLogger(__name__)

def email_report(report_path: str):

    try:
        smtp_host = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 25))
        sender = os.getenv("EMAIL_FROM")
        recipient = os.getenv("EMAIL_TO")
        smtp_pass = os.getenv("SMTP_PASS")

        msg = EmailMessage()
        msg["Subject"] = "Daily Invoice Summary"
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content("Please see attached the daily invoice summary.")

        with open(report_path, "rb") as f:
            data = f.read()
            msg.add_attachment(
                data,
                maintype="text",
                subtype="csv",
                filename=os.path.basename(report_path)
            )

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()  # Initiate secure connection
            smtp.login(sender, smtp_pass)  # If authentication is needed
            smtp.send_message(msg)

        logger.info(f"Sent summary email to {recipient}.")
    except Exception:
        logger.exception("Failed to send summary email.")

def ops(subject: str, file: str = None, error: Exception = None):
    """
    Logs an operational alert. No external alerts configured.
    """
    msg = subject
    if file:
        msg += f" | File: {file}"
    if error:
        msg += f" | Error: {error}"
    logger.warning(msg)

