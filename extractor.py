
import fitz  # PyMuPDF
import json

# Set the correct file name
pdf_path = "Form ADT-1-29092023_signed.pdf"

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

# Parse the extracted text into structured fields
def parse_text_to_json(text):
    data = {}
    lines = text.split('\n')

    def extract_line(keyword):
        return next((line.split('*')[-1].strip() for line in lines if keyword in line), "")

    data["company_name"] = extract_line("Name of the company")
    data["cin"] = extract_line("Corporate identity number")
    data["registered_office"] = extract_line("Address of the registered office")
    data["appointment_date"] = extract_line("Date of appointment")
    data["auditor_name"] = extract_line("Name of the auditor")
    data["auditor_address"] = extract_line("Address of the Auditor")
    data["auditor_frn_or_membership"] = extract_line("Membership Number")
    data["appointment_type"] = "New Appointment" if "Nature of appointment" in text else "Unknown"

    return data

# Run extraction
text = extract_text_from_pdf(pdf_path)
data = parse_text_to_json(text)

# Save JSON output
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)

print("JSON saved as output.json")

# Generate summary
def generate_summary(data):
    return (
        f"{data['company_name']} has appointed {data['auditor_name']} as its statutory auditor "
        f"effective from {data['appointment_date']}. "
        "This appointment has been recorded via Form ADT-1 and includes the necessary consents and board resolutions."
    )

summary = generate_summary(data)
with open("summary.txt", "w") as f:
    f.write(summary)

print("Summary saved as summary.txt")
