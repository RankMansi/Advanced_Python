import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from datetime import datetime
import os

# Step 1: Load order data from CSV file with exception handling
def load_orders(file):
    try:
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required_columns = ['Order ID', 'Customer Name', 'Product Name', 'Quantity', 'Unit Price']
            if not all(col in reader.fieldnames for col in required_columns):
                print(f"Error: CSV file is missing one or more required columns: {required_columns}")
                return None
            
            orders = []
            for row in reader:
                try:
                    order = {
                        'Order ID': row['Order ID'],
                        'Customer Name': row['Customer Name'],
                        'Product Name': row['Product Name'],
                        'Quantity': int(row['Quantity']),
                        'Unit Price': float(row['Unit Price'])
                    }
                    orders.append(order)
                except ValueError as e:
                    print(f"Error converting data for Order ID {row['Order ID']}: {e}. Skipping this order.")
            return orders
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
    return None

# Step 2: Create PDF with a table layout using ReportLab
def create_pdf_with_table(order, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Path for the PDF file
        pdf_path = os.path.join(folder, f"invoice_{order['Order ID']}.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)

        # List to store elements (tables, paragraphs, etc.)
        elements = []

        # Define styles for the table
        styles = getSampleStyleSheet()

        # Table data for the invoice
        table_data = [
            ["Invoice Number", f"{order['Order ID']}"],
            ["Date of Purchase", f"{datetime.now().strftime('%Y-%m-%d')}"],
            ["Customer Name", f"{order['Customer Name']}"],
            ["Product Name", f"{order['Product Name']}"],
            ["Quantity", f"{order['Quantity']}"],
            ["Unit Price", f"${order['Unit Price']:.2f}"],
            ["Total Amount", f"${order['Quantity'] * order['Unit Price']:.2f}"]
        ]

        # Create the table
        invoice_table = Table(table_data, colWidths=[150, 250])

        # Table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align the text
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font for header row
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Font for other rows
            ('FONTSIZE', (0, 0), (-1, 0), 14),  # Font size for header
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Font size for other rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines for the table
            ('TOPPADDING', (0, 0), (-1, -1), 10),  # Padding for top
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10)  # Padding for bottom
        ])
        invoice_table.setStyle(table_style)

        # Add table to elements
        elements.append(invoice_table)

        # Build the PDF
        doc.build(elements)

        print(f"Invoice created: {pdf_path}")

    except PermissionError:
        print(f"Error: Permission denied while creating invoice '{order['Order ID']}'.")
    except Exception as e:
        print(f"An unexpected error occurred while generating the invoice for order {order['Order ID']}: {e}")

# Step 3: Main logic to read orders and generate invoices
def generate_invoices():
    orders_file = 'Lab-7/orders.csv'
    orders = load_orders(orders_file)
    if orders is None or len(orders) == 0:
        print("No valid orders found to process. Exiting.")
        return
    invoices_folder = 'Lab-7/invoices'
    for order in orders:
        try:
            create_pdf_with_table(order, invoices_folder)
        except Exception as e:
            print(f"An error occurred while processing order {order['Order ID']}: {e}")

# Run the invoice generation process
print("Rank Mansi")
print("22BCP284")
try:
    generate_invoices()
except Exception as e:
    print(f"An unexpected error occurred in the process: {e}")
