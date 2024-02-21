
import csv
import requests
import json
import os
import sys
from requests import Session
from typing import Generator, Union
from requests import Session
import subprocess
import pandas as pd



# want to be able to generate name variations
def get_name_variations(author_name: str):
    """
    Given a name, return a list of name variations
    """
    parts = author_name.split(' ')
    first = parts[0]
    last = parts[-1]
    middle_full = ''.join([f"{x}" for x in parts[1:-1]])
    middle = ''.join([f"{x[0]}." for x in parts[1:-1]])
    variations = [
        author_name,  # Original format
        f"{first}-{last}",  # First-Last
        f"{first[0]}. {last}",  # F.Last
    ]
    if middle:
        variations.append(f"{first} {middle} {last}")  # First M. Last
        variations.append(f"{first}-{middle_full}-{last}") 
    return variations

def add_author_id_csv(author_name, author_id, csv_file_path='semantic_scholar_test/authorId.csv'):
    # Check if the CSV file exists else make
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['author_name','author_id', 'manual'])

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([author_name,author_id, False])

def fetch_authorId (author_name:str):
    if not API_KEY:
        raise EnvironmentError("S2_API_KEY environment variable not set.")
    # Set up the headers with the API key
    headers = {
        "x-api-key": API_KEY
    }
    
    search_response = requests.get(
        'https://api.semanticscholar.org/graph/v1/author/search',
        headers=headers,
        params={'query': author_name}
    )
    if search_response.status_code ==200: # successful request
        author_id = search_response.json()['data'][0]['authorId']
        return author_id
    else:
        raise Exception(f"Error finding author ID: {search_response.status_code}")


# go over permutation of the name and get unique author id
def filter_unique_author_ids_with_names(input_csv_path, output_csv_path=None):
    if output_csv_path is None:
        output_csv_path = input_csv_path 
    unique_authors = {}

    with open(input_csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader) 
        for row in reader:
            author_name, author_id = row
            if author_id not in unique_authors:
                unique_authors[author_id] = {'names': [author_name], 'id': author_id}
            else:
                if author_name not in unique_authors[author_id]['names']:
                    unique_authors[author_id]['names'].append(author_name)
    
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header + ['associated_names'])  
        for author_id, data in unique_authors.items():
            names = "; ".join(data['names']) 
            writer.writerow([data['names'][0], author_id, names]) 