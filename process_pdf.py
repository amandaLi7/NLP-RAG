import os
import pypdf as pdf
import pdfplumber as plumb
from pypdf import PdfReader
from pathlib import Path


# def parse_pdfs(directory_path, merger):

#     for file in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, file)
#         # Read file with pdfplumber
#         with plumb.open(file_path) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 merger.append(text)

#     return merger


# def merger_write(merger, file_path):
#     merger.write(file_path)
#     merger.close()


def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

# Function to process multiple PDFs and combine text into one file
def parse_pdfs(input_folder, output_file_path):
    output_text = ''
    input_folder_path = Path(input_folder)
    
    for pdf_path in input_folder_path.glob('*.pdf'):
        output_text += extract_text(pdf_path)
    
    with open(output_file_path, 'w', encoding='utf-8') as output:
        output.write(output_text)


if __name__ == "__main__":

    input_dir = "./data/pdfs"
    output_file = "./data/pdfs/parsed.pdf"

    parse_pdfs(input_dir, output_file)

    

