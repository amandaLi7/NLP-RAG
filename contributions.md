## Vashisth (vashistt)
- Data: 
  - worked with semantic scholar api to get faculty jsons
  - download papers by faculty
  - convert json to natural language dataset
- Setting up of the pipeline: 
  - Embedding + Vector DB: getting the data, embedding, creating the vector data base
  - Retriever: document retrieval, re-ranker based on the query 
  - Reader LLM: processing the context and the question in the reader LLM
- Experimenting with Models:
  - Gemini 2B 
  - Flan T5 (small/base/large)
- Benchmarking performance per document type


## Amanda (xal)
- Data:
  - processed webpages and hand annotated/cleaned them
  - especially the tables and the weird formatting of the Carnival schedule website
  - categorized different data set questions to be analyzed later
- Setting up of the pipeline:
  - created evaluation metrics code (exact match, f1, recall) for the outputs
  - created vector store embeddings code (FAISS) that saves, loads, and combines the data
- Experimentation
  - experimented with different parameters of the models, number of documents retrieved from the retriever, prompts, etc
  - debugged weird answer generations (in relation to updating the parameters and feedback on prompt updating)
- Report and deliverable:
  - generated system outputs for Flan T5 xlarge
  - wrote the corresponding webpage, FAISS, evaluation and significance testing portions, along with proofreading


## Emily (epguo)
- Data:
  - Parsing and processing academic paper PDFs, parsing 'other' PDFs
  - Extensive processing of schedule of classes PDFs
  - Prepending metadata to academic paper chunks
  - Hand annotation and question generation of all PDF files
- Experimentation:
  - Experimenting with various prompting methods for Llama, Mistral
  - Adjusting PDF text as necessary based on
- Report and Deliverables:
  - Generated outputs for both Llama models on full test set and outputs for Llama and Mistral in no-context setting
  - IAA section of report
  - PDF (academic paper and schedule of classes) sections in Data Cleaning and Processing

