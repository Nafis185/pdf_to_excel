# from flask import Flask, render_template, request, send_file
# import os
# import re
# import pandas as pd
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # Folder to temporarily store uploaded PDFs
# UPLOAD_FOLDER = 'static/uploaded_pdfs/'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Route for the home page (Upload PDF)
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to handle PDF upload and conversion
# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     # Check if the PDF is part of the request
#     if 'pdf_file' not in request.files:
#         return "No file part", 400
    
#     pdf_file = request.files['pdf_file']

#     if pdf_file.filename == '':
#         return 'No selected file', 400

#     if pdf_file and pdf_file.filename.endswith('.pdf'):
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
#         pdf_file.save(file_path)

#         # Extract data from PDF and convert to Excel
#         data = extract_data_from_pdf(file_path)

#         # Create DataFrame and add summary
#         df = pd.DataFrame(data)
#         if not df.empty:
#             total_sum = df["Total"].sum()
#             total_orders = len(df)
#             summary_row = {
#                 "Order ID": "TOTAL SUMMARY",
#                 "Order Date": "",
#                 "Deliver To": "",
#                 "Phone": "",
#                 "Delivery Address": "",
#                 "Total": total_sum
#             }
#             df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

#         # Save DataFrame to Excel
#         output_excel = 'Extracted_Order_Details.xlsx'
#         df.to_excel(output_excel, index=False)

#         # Send the generated Excel file as a download
#         return send_file(output_excel, as_attachment=True)
#     return "Invalid file format. Please upload a PDF.", 400


# def extract_data_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     data = []

#     for page in reader.pages:
#         text = page.extract_text()
#         lines = text.split('\n')

#         order_id = ""
#         order_date = ""
#         deliver_to = ""
#         phone = ""
#         delivery_address = ""
#         total = 0.0

#         for idx, line in enumerate(lines):
#             # ---- Parse Order ID ----
#             if "Order ID" in line:
#                 match_id = re.search(r"Order ID\s*(\d+)", line)
#                 if match_id:
#                     order_id = match_id.group(1)
#                 else:
#                     if idx + 1 < len(lines):
#                         next_line_match = re.search(r"(\d+)", lines[idx + 1])
#                         if next_line_match:
#                             order_id = next_line_match.group(1)

#             # ---- Parse Order Date ----
#             if "Order Date" in line:
#                 match_date = re.search(r"Order Date:\s*(.*)", line)
#                 if match_date:
#                     order_date = match_date.group(1).strip()
#                 else:
#                     if idx + 1 < len(lines):
#                         order_date = lines[idx + 1].strip()

#             # ---- Parse Deliver To & Phone ----
#             if "Deliver To:" in line:
#                 dt_match = re.search(r"Deliver To:\s*(.*)", line)
#                 if dt_match:
#                     dt_str = dt_match.group(1).strip()
#                     phone_match = re.search(r"(?i)phone:\s*(\d+)", dt_str)
#                     if phone_match:
#                         phone = phone_match.group(1)
#                         dt_str = re.sub(r"(?i)phone:\s*\d+", "", dt_str).strip()
#                     deliver_to = dt_str

#             # ---- Parse Delivery Address ----
#             if "Delivery Address:" in line:
#                 addr_lines = []
#                 da_match = re.search(r"Delivery Address:\s*(.*)", line)
#                 if da_match:
#                     possible_addr = da_match.group(1).strip()
#                     if possible_addr and not re.search(r'Bill To|Billing Address', possible_addr, re.IGNORECASE):
#                         addr_lines.append(possible_addr)

#                 for j in range(1, 10):
#                     if idx + j < len(lines):
#                         next_line = lines[idx + j].strip()
#                         if "Bill To" in next_line or "Billing Address" in next_line:
#                             break
#                         addr_lines.append(next_line)
#                     else:
#                         break

#                 delivery_address = ', '.join(addr_lines)

#             # ---- Parse Total ----
#             if "Total:" in line:
#                 total_match = re.search(r'Total:\s*([\d,]+\.\d+|\d+)', line)
#                 if total_match:
#                     total = float(total_match.group(1).replace(',', ''))

#         if order_id:
#             data.append({
#                 "Order ID": order_id,
#                 "Order Date": order_date,
#                 "Deliver To": deliver_to,
#                 "Phone": phone,
#                 "Delivery Address": delivery_address,
#                 "Total": total
#             })

#     return data

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, render_template, request, send_file
import os
import re
import pandas as pd
from PyPDF2 import PdfReader

app = Flask(__name__)

def index():
    return render_template('index.html')

# Folder to temporarily store uploaded PDFs
UPLOAD_FOLDER = 'static/uploaded_pdfs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the home page (Upload PDF)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle PDF upload and conversion
@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if the PDF is part of the request
    if 'pdf_file' not in request.files:
        return "No file part", 400
    
    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return 'No selected file', 400

    if pdf_file and pdf_file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(file_path)

        # Extract data from PDF and convert to Excel
        data = extract_data_from_pdf(file_path)

        # Create DataFrame and add summary
        df = pd.DataFrame(data)
        if not df.empty:
            total_sum = df["Total"].sum()
            total_orders = len(df)
            summary_row = {
                "Order ID": "TOTAL SUMMARY",
                "Order Date": "",
                "Deliver To": "",
                "Phone": "",
                "Delivery Address": "",
                "Total": total_sum
            }
            df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

        # Save DataFrame to Excel
        output_excel = 'Extracted_Order_Details.xlsx'
        df.to_excel(output_excel, index=False)

        # Send the generated Excel file as a download
        return send_file(output_excel, as_attachment=True)

    return "Invalid file format. Please upload a PDF.", 400


def extract_data_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    data = []

    for page in reader.pages:
        text = page.extract_text()
        lines = text.split('\n')

        order_id = ""
        order_date = ""
        deliver_to = ""
        phone = ""
        delivery_address = ""
        total = 0.0

        for idx, line in enumerate(lines):
            # ---- Parse Order ID ----
            if "Order ID" in line:
                match_id = re.search(r"Order ID\s*(\d+)", line)
                if match_id:
                    order_id = match_id.group(1)
                else:
                    if idx + 1 < len(lines):
                        next_line_match = re.search(r"(\d+)", lines[idx + 1])
                        if next_line_match:
                            order_id = next_line_match.group(1)

            # ---- Parse Order Date ----
            if "Order Date" in line:
                match_date = re.search(r"Order Date:\s*(.*)", line)
                if match_date:
                    order_date = match_date.group(1).strip()
                else:
                    if idx + 1 < len(lines):
                        order_date = lines[idx + 1].strip()

            # ---- Parse Deliver To & Phone ----
            if "Deliver To:" in line:
                dt_match = re.search(r"Deliver To:\s*(.*)", line)
                if dt_match:
                    dt_str = dt_match.group(1).strip()
                    phone_match = re.search(r"(?i)phone:\s*(\d+)", dt_str)
                    if phone_match:
                        phone = phone_match.group(1)
                        dt_str = re.sub(r"(?i)phone:\s*\d+", "", dt_str).strip()
                    deliver_to = dt_str

            # ---- Parse Delivery Address ----
            if "Delivery Address:" in line:
                addr_lines = []
                da_match = re.search(r"Delivery Address:\s*(.*)", line)
                if da_match:
                    possible_addr = da_match.group(1).strip()
                    if possible_addr and not re.search(r'Bill To|Billing Address', possible_addr, re.IGNORECASE):
                        addr_lines.append(possible_addr)

                for j in range(1, 10):
                    if idx + j < len(lines):
                        next_line = lines[idx + j].strip()
                        if "Bill To" in next_line or "Billing Address" in next_line:
                            break
                        addr_lines.append(next_line)
                    else:
                        break

                delivery_address = ', '.join(addr_lines)

            # ---- Parse Total ----
            if "Total:" in line:
                total_match = re.search(r'Total:\s*([\d,]+\.\d+|\d+)', line)
                if total_match:
                    total = float(total_match.group(1).replace(',', ''))

        if order_id:
            data.append({
                "Order ID": order_id,
                "Order Date": order_date,
                "Deliver To": deliver_to,
                "Phone": phone,
                "Delivery Address": delivery_address,
                "Total": total
            })

    return data


# Add the following block to handle local development
if __name__ == '__main__':
#     # Only run the Flask development server locally
    app.run(debug=True, host='0.0.0.0')