ResMatch - AI-Powered Resume Screening System    
📌 Overview

ResMatch is an AI-powered resume screening and job matching system that analyzes resumes and job descriptions to identify the most suitable candidates.
It extracts key information such as skills, education, experience, and certifications, and ranks candidates using semantic similarity and rule-based scoring.

🚀 Features

📄 Resume parsing (PDF, DOCX, TXT)

🧹 Text preprocessing and section extraction

🧠 Skill, education, experience, and certification extraction

🔍 Semantic similarity using Sentence Transformers (SBERT)

📊 Multi-factor scoring:

Skill match

Semantic similarity

Experience match

Education match

🏆 Candidate ranking system

⚡ FastAPI backend

🗂 Vector storage using ChromaDB

🏗 Project Structure    
resmatch/    
│     
├── app/     
│   ├── api/    
│   ├── ingestion/    
│   ├── preprocessing/    
│   ├── extraction/    
│   ├── embeddings/    
│   ├── vectordb/    
│   ├── scoring/    
│   ├── evaluation/    
│   └── pipeline/      
├── templates/    
├── static/    
├── data/       
├── requirements.txt    
├── README.md      
├── .gitignore     
└── run.py    

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/raeeskasim1/ResMatch.git
cd ResMatch
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate environment

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```


Data Ingestion

  -Extract text from resumes (PDF, DOCX, TXT)

Preprocessing

  -Clean and normalize text

  -Split into sections

  -Information Extraction

Extract:

  -Skills

  -Education

  -Experience

Embedding Generation

  -Convert text into vector embeddings using Sentence Transformers

Vector Storage

  -Store embeddings using ChromaDB

Scoring

  -Skill matching

  -Semantic similarity

  -Experience comparison

  -Education matching

  -Ranking

  -Rank candidates based on final score

📦 Dependencies

Python 3.10+

fastapi

uvicorn

sentence-transformers

chromadb

pypdf

python-docx

scikit-learn

numpy

pandas

⚠️ Notes

The vector database (chroma_store/) is generated dynamically and not included in the repository.

Uploaded resumes (storage/resumes/) are not stored in the repository.

Virtual environments and cache files are excluded using .gitignore.
