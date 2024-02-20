import os
from pypdf import PdfReader
from pathlib import Path
import time

# Extracts plaintext from one PDF file
def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text().encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return text


def parse_pdfs(input_folder, output_file_dir):
    input_folder_path = Path(input_folder)

    for pdf_path in input_folder_path.glob('*.pdf'):
        output_file_path = f"{output_file_dir}/{pdf_path.stem}.txt"
        output_text = extract_text(pdf_path)
        
        # Write to text file
        with open(output_file_path, 'w', encoding='utf-8') as output:
            output.write(output_text)


if __name__ == "__main__":

    paper_dir = "./data/papers"
    paper_output_dir = "./data/parsed_papers"
    other_pdf_dir = "./data/other_pdfs"
    other_pdf_output_dir = "./data/parsed_other"

    start = time.time()

    parse_pdfs(paper_dir, paper_output_dir)
    parse_pdfs(other_pdf_dir, other_pdf_output_dir)

    print(f"Total parsing time: {time.time() - start} seconds")
