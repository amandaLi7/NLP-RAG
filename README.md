# NLP-RAG (11-711 Assignment 2: End-to-end NLP System Building)

You can find the details of the assignment in our report here 
## Assignment Overview

This project involves developing a Retrieval Augmented Generation (RAG) system for answering questions about the Language Technology Institute (LTI) and Carnegie Mellon University (CMU).

### Key Components
1. Prepare raw data by compiling a knowledge resource
2. Annotate data for model development and testing
3. Develop a RAG system with document & query embedder, document retriever, and document reader
4. Generate results on an unseen test set
5. Write a comprehensive report

### Data Preparation and Annotation

#### Compiling a knowledge resource
For the test set and RAG systems, a knowledge resource of relevant documents was compiled. The following publicly available resources were recommended:

+ Faculty @ LTI
    - List of faculty ([LTI faculty directory](https://lti.cs.cmu.edu/directory/all/154/1))
    - Research papers by LTI faculty and their metadata ([Semantic Scholar API](https://www.semanticscholar.org/product/api))
    - Teaching information
+ Courses @ CMU
    - Courses offered by each department at CMU and their metadata ([Schedule of Classes](https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/completeSchedule))
    - Academic calendars for 2023-2024 and 2024-2025 ([CMU calendar](https://www.cmu.edu/hub/calendar/))
+ Academics @ LTI
    - Programs offered by LTI ([website](https://lti.cs.cmu.edu/learn))
    - Program handbooks ([PhD](https://lti.cs.cmu.edu/sites/default/files/PhD_Student_Handbook_2023-2024.pdf), [MLT](https://lti.cs.cmu.edu/sites/default/files/MLT%20Student%20Handbook%202023%20-%202024.pdf), [MIIS](https://lti.cs.cmu.edu/sites/default/files/MIIS%20Handbook_2023%20-%202024.pdf), [MCDS](https://lti.cs.cmu.edu/sites/default/files/MCDS%20Handbook%2023-24%20AY.pdf), [MSAII](https://msaii.cs.cmu.edu/sites/default/files/Handbook-MSAII-2022-2023.pdf))
+ Events @ CMU
    - Spring carnival and reunion weekend 2024 ([schedule](https://web.cvent.com/event/ab7f7aba-4e7c-4637-a1fc-dd1f608702c4/websitePage:645d57e4-75eb-4769-b2c0-f201a0bfc6ce?locale=en))
    - Commencement 2024 ([schedule](https://www.cmu.edu/commencement/schedule/index.html))
+ History @ SCS and CMU
    - School of Computer Science ([25 great things](https://www.cs.cmu.edu/scs25/25things), [history](https://www.cs.cmu.edu/scs25/history))
    - [CMU fact sheet](https://www.cmu.edu/about/cmu_fact_sheet_02.pdf) and [history](https://www.cmu.edu/about/history.html)
    - Buggy and its history ([article](https://www.cmu.edu/news/stories/archives/2019/april/spring-carnival-buggy.html))
    - Athletics ([Tartans](https://athletics.cmu.edu/athletics/tartanfacts), [Scotty](https://athletics.cmu.edu/athletics/mascot/about), [Kiltie Band](https://athletics.cmu.edu/athletics/kiltieband/index))

#### Additional Data Preparation Steps
- Clean and convert data into suitable formats
- Create test data for system evaluation
- Prepare training data for model development
- Estimate data quality through inter-annotator agreement

### RAG System Development
- Implement document & query embedder, document retriever, and document reader
- Freedom to use any open-source model and library

### Evaluation
- System will be tested on an unseen test set
- Metrics: answer recall, exact match, and F1 score

### Report and Submission Requirements
- 7-page limit report detailing data creation, model details, results, and analysis
- Submit report, GitHub repository link, team contributions, annotated data, and system outputs

### Model and Data Policy
- Use only publicly accessible models and data
- Allowed to use open-source libraries with proper attribution

## Project Structure
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
