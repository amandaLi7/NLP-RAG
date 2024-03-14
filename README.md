# NLP-RAG
11-711 Assignment 2: End-to-end NLP System Building

## Files
The structure of our repositorty is as follows, with relevant files in each folder mentioned below with a brief description:

#### data
- Contains all the data we collected, parsed, and processed for training, testing, and evaluating our models.

#### dev
- Contains all the files we used for data cleaning and processing, model pipeline development and experimentation, metric calculation, and statistical testing.
- embeddings_store.ipynb: Code for the generation of vector store databases of documents (outputs stored in dev/faiss_folders).
- eval_metrics.ipynb: Notebook for metric calculation; calculates the f1, recall, and exact match scores of our model outputs to annotated reference answers.
- ##### src-rag
  - Contains various model experimentation notebooks (src-rag final contains the final versions of these initial experiments)
- ##### src_colelction-preprocessing
  - Contains all files used for data collection, cleaning, and processing. 
- ##### system_outptus_dev
  - Contains .txt and .csv files of model outputs and files for IAA.

#### faiss_folders
- Contains all vector store embeddings of chunked documents.

#### src-rag-final
- Contains the final model pipelines used on the 770 official test set + on our own set:
  - FlanT5-large.ipynb
  - FlanT5-xlarge.ipynb
  - LlamaCcp-notemplate-1shot_TESTSET.ipynb
  - LlamaCcp-notemplate.ipynb
  - Mistral.ipynb
- paired-bootstrap.py: Notebook used for significance testing between outputs.

#### system_outputs
- Contains 3 files of answers to the 770 official test set.

## How to Run
The 5 notebooks listed in the section above are our final model pipelines. They can be run as regular Python Notebooks with paths to the correct embeddings. Due to the restructuring of our repo for submission, some file paths will be invalid; we are working on correcting all file paths to reflect this new folder organization, and in the meantime, some files will still contain incorrect file paths. We thank the TAs for their patience as we make these corrections!

Due to the size of our final embedding file, we were not able to upload it to GitHub. Please find the embedding files in the folder 'faiss_index_total_final_new' at [this GDrive link](https://drive.google.com/drive/folders/1BDwDQrWU4DbaWDrk9v9Ga5jythLgVXJ1).
