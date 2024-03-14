import os, re, string
from typing import List
import time


def remove_hyphens(text: str) -> str:
    """

    This fails for:
    * Natural dashes: well-known, self-replication, use-cases, non-semantic,
                      Post-processing, Window-wise, viewpoint-dependent
    * Trailing math operands: 2 - 4
    * Names: Lopez-Ferreras, VGG-19, CIFAR-100
    """
    lines = [line.rstrip() for line in text.split("\n")]

    # Find dashes
    line_numbers = []
    for line_no, line in enumerate(lines[:-1]):
        if line.endswith("-"):
            line_numbers.append(line_no)
    # Replace
    for line_no in line_numbers:
        lines = dehyphenate(lines, line_no)

    return "\n".join(lines)


# Remove hyphens from the end of a line and the next line
def dehyphenate(lines: List[str], line_no: int) -> List[str]:
    next_line = lines[line_no + 1]
    word_suffix = next_line.split(" ")[0]

    lines[line_no] = lines[line_no][:-1] + word_suffix
    lines[line_no + 1] = lines[line_no + 1][len(word_suffix) :]
    return lines


# Remove non-alphanumeric characters
def remove_nonalphanumeric(text: str) -> str:
    pattern = re.compile(r'[^a-zA-Z0-9\s' + re.escape(string.punctuation) + ']+')
    cleaned_text = pattern.sub(' ', text)
    return cleaned_text


# Short lines are typically a result of faulty table or equation parsing
def remove_short_lines(text: str) -> str:
    lines = [line for line in text.split("\n") if len(line) > 20]
    return "\n".join(lines)


def remove_newlines(text: str) -> str:
    # Remove newlines at the ends of lines only so that text is one long string
    lines = [line.strip() for line in text.split("\n")]
    return " ".join(lines)


def pseudo_chunk(text: str, chunk_size: int) -> List[str]:
    # For each chunk, find the period ('.') closest the end of chunksize from start index
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i : i + chunk_size]
        # Index of closest end of sentence
        last_period = chunk.rfind(".")
        if last_period == -1:
            last_period = chunk_size
        chunks.append(chunk[:last_period + 1].strip() + ' ')
        i += last_period + 1
    return '\n'.join(chunks)


def process_text(text: str) -> str:
    text = remove_hyphens(text)
    text = remove_nonalphanumeric(text)
    text = remove_short_lines(text)
    text = remove_newlines(text)
    # text = pseudo_chunk(text, 256)
    return text


def clean_pdfs(input_folder, output_folder):
    for file_path in os.listdir(input_folder):
        output_path = f"{output_folder}/{file_path}"
        if not os.path.exists(output_path):
            text = open(f"{input_folder}/{file_path}", "r")
            processed_text = process_text(text.read())
            with open(output_path, "w") as output:
                output.write(processed_text)


if __name__ == "__main__":

    parsed_papers_dir = "./data/parsed_papers"
    cleaned_papers_dir = "./data/cleaned_papers"

    parsed_other_dir = "./data/parsed_other"
    cleaned_other_dir = "./data/cleaned_other"

    start = time.time()

    clean_pdfs(parsed_papers_dir, cleaned_papers_dir)
    # clean_pdfs(parsed_other_dir, cleaned_other_dir)

    print(f"Time to clean: {time.time() - start}")