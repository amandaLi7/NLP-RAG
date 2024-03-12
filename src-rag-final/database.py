from tqdm.notebook import tqdm
import pandas as pd
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt

# imports for embedding
from langchain.docstore.document import Document as LangchainDocument
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

# imports for vectorization of database

from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy





# please uncomment if cuda is available:
#   model_kwargs={"device": "cuda"},



EMBEDDING_MODEL_NAME = "thenlper/gte-base"

'''
Splitting the documents into chunks of maximum size `chunk_size` and 'chunk_overlap' tokens and return a list of documents.
'''
def split_documents(
    chunk_size: int,
    knowledge_base: List[LangchainDocument],
    chunk_overlap: int = None,
    tokenizer_name: Optional[str] = EMBEDDING_MODEL_NAME,
) -> List[LangchainDocument]:
    """
    Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.
    """

    if chunk_overlap is not None:
      chunk_overlap = chunk_overlap
    else:
      chunk_overlap=int(chunk_size / 10),

    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(tokenizer_name),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        strip_whitespace=True,
    )

    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])

    # Remove duplicates
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)

    return docs_processed_unique


'''
Create a knowledge vector database from the list of documents'''
def create_db(docs):
    docs_processed = split_documents(
        chunk_size = 450,
        chunk_overlap = 50,
        knowledge_base = docs,
        tokenizer_name=EMBEDDING_MODEL_NAME,
    )
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        multi_process=True,
        # model_kwargs={"device": "cuda"},
        encode_kwargs={"normalize_embeddings": True},  #  True for cosine similarity
    )

    KNOWLEDGE_VECTOR_DATABASE = FAISS.from_documents(
        docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
    )

    return KNOWLEDGE_VECTOR_DATABASE
