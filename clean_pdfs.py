# author listing at the top of papers is an issue; sometimes people use
# unicode characters or there's other improper formatting. CHECK THIS

# eg:
# Sriram Yenamandra 1Arun Ramachandran 1Karmesh Yadav 1,2Austin Wang1
# Mukul Khanna1Theophile Gervet2,3Tsung Yen Yang2Vidhi Jain3
# Alexander William Clegg2John Turner2Zsolt Kira1Manolis Savva4
# Angel Chang4Devendra Singh Chaplot2Dhruv Batra1,2Roozbeh Mottaghi2
# Yonatan Bisk2,3Chris Paxton2
# 1Georgia Tech2FAIR, Meta AI3Carnegie Mellon4Simon Fraser

# papers written with double columns have a lot of new lines and words
# that are hyphenated because theyre cut off by new lines. CHECK THIS

# consider checking if a number is bounded on both sides by alpha characters,
# if so then separate with spaces

import os, re
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
    cleaned_text = re.sub(r'[^\w\s\d.,*@%#$&/~"\'\[\]\(\)\{\}-]', ' ', text)
    return cleaned_text


# Fix numeric characters bounded by alpha characters
def replace_bounded_numbers(text):
    corrected_text = re.sub(r'(?<=[a-zA-Z])\d+(?=[a-zA-Z])', ' ', text)
    return corrected_text


# Fix strings bounded by numeric characters
def replace_bounded_strings(text):
    corrected_text = re.sub(r'(?<=\d)[a-zA-Z\s]+(?=\d)', ' ', text)
    return corrected_text


def process_text(text: str) -> str:
    text = remove_hyphens(text)
    text = remove_nonalphanumeric(text)
    # text = replace_bounded_numbers(text)
    # text = replace_bounded_strings(text)
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

    # clean_pdfs(parsed_papers_dir, cleaned_papers_dir)
    clean_pdfs(parsed_other_dir, cleaned_other_dir)

    print(f"Time to clean: {time.time() - start}")