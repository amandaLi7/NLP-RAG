## Vashisth (vashistt)
- Data: 
  - worked with semantic scholar api to get faculty JSONs
  - download papers by faculty
  - Data Cleaning for JSONs: automatically convert the JSONs into a set of paper and author related questions 
  - Function to generate Question Answer pairs from the chunks automatically using LLama2
- Setting up of the retriever, reranker, and Reader LLM pipeline: 
  - Embedding + Vector DB: getting the data, embedding, creating the vector data base
    - Experimented with different similarity criterion
  - Retriever: document retrieval, re-ranker based on the query (integrating colbert re-ranker in the pipeline)
  - Reader LLM: processing the context and the question in the reader LLM
- Experimenting with Models and prompts:
  - Set up the pipeline with all these models so we can do experiments over them and running them with and without GPU
    - Gemini 2B 
    - Flan T5 (small/base/large)
    - Llama2 7B (LLama CCP quantized version)
    - Mistral 7B
  - Experimented with temperature, top-p; verbosity, and prompts for each model
- Evaluation
  - Wrote the pipeline to do get metrics over different kinds of document categories
- Report:
  - Corresponding report sections on JSONs, Model Selection, Embedding, Retrieiver and Reranking
  - LaTex tables and part of the analysis


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
  - Extensive processing of schedule of classes PDFs into natural language
  - Prepending metadata to academic paper chunks
  - Hand annotation and question generation of all PDF files
- Experimentation:
  - Experimenting with various prompting methods for Llama, Mistral
  - Adjusting PDF text as necessary based on
- Evaluation:
  - Adjusted metrics pipeline to accommodate all model outputs
  - Generated metrics for all experiments after they were finalized
- Report and Deliverables:
  - Generated outputs for both Llama models on full test set and outputs for Llama and Mistral in no-context setting
  - Inter-annotator analysis and corresponding section of report
  - PDF (academic paper and schedule of classes) sections in Data Cleaning and Processing

