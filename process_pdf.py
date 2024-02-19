import os
import pypdf as pdf
import pdfplumber as plumb
from pypdf import PdfWriter

# Main document cleaning function
def parse_pdf(file):
    # TODO
    pass


def process_pdfs(directory_path, merger):

    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        doc = open(file_path, "rb")

        # Document parsing
        # TODO

        merger.append(doc)

    return merger


def merger_write(merger, file_path):
    merger.write(file_path)
    merger.close()


if __name__ == "__main__":

    merger = PdfWriter()

    input_dir = "./data/pdfs"

    process_pdfs(input_dir, merger)

    output_file = "./data/pdfs/parsed.pdf"

    merger_write(merger, output_file)
