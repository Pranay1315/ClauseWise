import os
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document

# Dictionary of legal document templates
document_templates = {
    "nda": {
        "title": "Non-Disclosure Agreement (NDA)",
        "description": "A contract to protect confidential information shared between two parties.",
        "fields": ["Disclosing Party Name", "Receiving Party Name", "Effective Date"],
        "content": """This Non-Disclosure Agreement ('Agreement') is made as of {Effective Date} by and between:
        
{Disclosing Party Name} (Disclosing Party), and {Receiving Party Name} (Receiving Party).

1. Confidential Information:
   The Disclosing Party agrees to share certain confidential and proprietary information.

2. Obligations of Receiving Party:
   The Receiving Party agrees to keep the information confidential.

3. Term & Termination:
   This Agreement remains in effect until terminated by either party.

Signed: ___________________________ (Disclosing Party)      Date: ___________________________
Signed: ___________________________ (Receiving Party)      Date: ___________________________
"""
    },
    "lease": {
        "title": "Lease Agreement",
        "description": "A legal contract between a landlord and a tenant for rental property.",
        "fields": ["Landlord Name", "Tenant Name", "Property Address", "Rent Amount", "Payment Due Date", "Start Date", "End Date"],
        "content": """This Lease Agreement ('Agreement') is made as of today between:
        
{Landlord Name} (Landlord) and {Tenant Name} (Tenant).

1. Property Description:
   The Landlord leases the property located at {Property Address} to the Tenant.

2. Lease Term:
   The lease starts on {Start Date} and continues until {End Date}.

3. Rent Payment:
   Tenant agrees to pay {Rent Amount} on {Payment Due Date} each month.

4. Governing Law:
   This Agreement is governed by the laws of the relevant jurisdiction.

Signed: ___________________________ (Landlord)       Date: ___________________________
Signed: ___________________________ (Tenant)       Date: ___________________________
"""
    },
    "employment": {
        "title": "Employment Contract",
        "description": "A contract defining terms of employment between an employer and an employee.",
        "fields": ["Employer Name", "Employee Name", "Job Title", "Company Name", "Salary", "Payment Period", "Notice Period", "Effective Date"],
        "content": """This Employment Agreement ('Agreement') is entered into on {Effective Date} between:

{Employer Name} (Employer) and {Employee Name} (Employee).

1. Position and Responsibilities:
   The Employee will work as {Job Title} at {Company Name}.

2. Compensation:
   The Employee will be paid {Salary} per {Payment Period}.

3. Termination:
   This Agreement may be terminated by either party with {Notice Period} notice.

Signed: ___________________________ (Employer)       Date: ___________________________
Signed: ___________________________ (Employee)       Date: ___________________________
"""
    }
}

# Function to create a PDF document
def create_pdf(filepath, document_data, filled_content):
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, document_data["title"])

    c.setFont("Helvetica", 12)
    y_position = 720
    for line in filled_content.split("\n"):
        c.drawString(100, y_position, line)
        y_position -= 20
        if y_position < 50:  # New page if needed
            c.showPage()
            y_position = 750

    c.save()

# Function to create a Word document
def create_word(filepath, document_data, filled_content):
    doc = Document()
    doc.add_heading(document_data["title"], level=1)

    for line in filled_content.split("\n"):
        doc.add_paragraph(line)

    doc.save(filepath)

# Function to generate the document
def generate_document():
    selected_doc = document_var.get()
    
    if selected_doc not in document_templates:
        messagebox.showerror("Error", "Please select a document type.")
        return
    
    document_data = document_templates[selected_doc]
    user_inputs = {}

    for field in document_data["fields"]:
        value = input_fields[field].get().strip()
        if not value:
            messagebox.showerror("Error", f"Please fill in {field}.")
            return
        user_inputs[field] = value

    filled_content = document_data["content"].format(**user_inputs)

    # Ask for save location
    save_dir = filedialog.askdirectory(title="Select Save Location")
    if not save_dir:
        return  # User canceled

    pdf_filename = os.path.join(save_dir, f"{selected_doc}_document.pdf")
    word_filename = os.path.join(save_dir, f"{selected_doc}_document.docx")

    create_pdf(pdf_filename, document_data, filled_content)
    create_word(word_filename, document_data, filled_content)

    messagebox.showinfo("Success", f"{document_data['title']} created!\n📄 PDF: {pdf_filename}\n📝 Word: {word_filename}")

# Function to update input fields dynamically
def update_fields(*args):
    selected_doc = document_var.get()
    
    for widget in field_frame.winfo_children():
        widget.destroy()  # Clear old fields

    if selected_doc in document_templates:
        document_data = document_templates[selected_doc]
        tk.Label(field_frame, text="Enter Details:", font=("Arial", 12, "bold")).pack(anchor="w")

        for field in document_data["fields"]:
            tk.Label(field_frame, text=field + ":", font=("Arial", 10)).pack(anchor="w")
            entry = tk.Entry(field_frame, width=40)
            entry.pack()
            input_fields[field] = entry

# Initialize Tkinter window
root = tk.Tk()
root.title("Legal Document Generator")
root.geometry("500x600")

# Dropdown menu for document selection
tk.Label(root, text="Select a Legal Document:", font=("Arial", 12, "bold")).pack(pady=10)
document_var = tk.StringVar(root)
document_var.trace("w", update_fields)

document_menu = tk.OptionMenu(root, document_var, *document_templates.keys())
document_menu.pack()

# Dynamic input fields frame
field_frame = tk.Frame(root)
field_frame.pack(pady=10)

input_fields = {}

# Generate button
generate_btn = tk.Button(root, text="Generate Document", command=generate_document, font=("Arial", 12, "bold"), bg="green", fg="white")
generate_btn.pack(pady=20)

root.mainloop()
