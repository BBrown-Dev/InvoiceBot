#!/usr/bin/env python3

#Creates a set of dummy invoice PDFs in the local 'invoices/' folder.
#Each PDF contains an invoice number and an amount due.

import os
from fpdf import FPDF


def create_dummy_invoice(folder: str, invoice_number: int, amount: float):
    """Generate a single dummy invoice PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, txt=f"Invoice Number: INV-{invoice_number:03d}", ln=True)
    pdf.cell(0, 10, txt=f"Amount Due: ${amount:.2f}", ln=True)

    filename = f"INV-{invoice_number:03d}.pdf"
    filepath = os.path.join(folder, filename)
    pdf.output(filepath)
    print(f"Created {filepath}")


def main():
    folder = "invoices"
    os.makedirs(folder, exist_ok=True)

    # Define a list of (invoice_number, amount) tuples
    invoices = [
        (1, 125.50),
        (2, 0.00),  # To test validation failure (amount = 0)
        (3, 347.80),
        (4, 915.25),
        (5, 49.99)
    ]

    for num, amt in invoices:
        create_dummy_invoice(folder, num, amt)


if __name__ == "__main__":
    main()
