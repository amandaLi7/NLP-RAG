import os
import pypdf as pdf
import pdfplumber as plumb
from pypdf import PdfWriter

# Merge PDFs
merger = PdfWriter()

for file in os.listdir('./data/pdf'):
    file_path = os.path.join('./data/pdf', file)
    doc = open(file_path, "rb")

    # Document parsing here
    # TODO

    merger.append(doc)

merger.write("./data/pdf/merged-pdf.pdf")
merger.close()
