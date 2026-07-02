# SHL Assessment Recommendation Agent

An AI-powered recommendation system that helps recruiters identify the most suitable **SHL assessments** based on hiring requirements using **Semantic Search, LangGraph, FAISS, and Gemini 2.5 Flash**.

---

## 🚀 Live Demo

 **Application:** https://shraddha-dsa-shl-assessment-agent.hf.space

 **API Documentation:** https://shraddha-dsa-shl-assessment-agent.hf.space/docs

 **Health Check:** https://shraddha-dsa-shl-assessment-agent.hf.space/health

---

## 📌 Problem Statement

Recruiters often spend significant time searching through hundreds of SHL assessments to identify the most appropriate ones for a job role.

This project automates that process by allowing recruiters to simply describe the hiring requirement in natural language. The system retrieves the most relevant SHL assessments and generates AI-powered explanations for each recommendation.

---

## ✨ Features

- 🔍 Semantic search over **377+ SHL assessments**
- 🤖 AI-generated recommendations using **Gemini 2.5 Flash**
- 🧠 LangGraph-based workflow orchestration
- ⚡ Fast similarity search using **FAISS**
- 🌐 REST API built with **FastAPI**
- 🐳 Dockerized deployment
- ☁️ Deployed on Hugging Face Spaces

---

## 🏗️ Architecture

```text
Recruiter
     │
     ▼
 FastAPI API
     │
     ▼
 LangGraph Workflow
     │
 ┌───────────────┐
 │ Guardrail     │
 │ Intent        │
 │ Retrieval     │
 │ Recommendation│
 └───────────────┘
     │
     ▼
 FAISS Semantic Search
     │
     ▼
 Relevant Assessments
     │
     ▼
 Gemini 2.5 Flash
     │
     ▼
 JSON Response
```

---

## ⚙️ Workflow

1. Recruiter submits a hiring query.
2. Guardrail validates the request.
3. Intent Detection identifies the user objective.
4. FAISS retrieves the most relevant assessments.
5. Gemini generates recruiter-friendly explanations.
6. FastAPI returns structured recommendations.

---

## 📂 Project Structure

```
shl_assessment_agent/

├── agent/
│   ├── graph.py
│   ├── nodes.py
│   ├── retriever.py
│   ├── recommender.py
│   ├── comparator.py
│   ├── intent.py
│   ├── guardrails.py
│   └── state.py
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── config.py
│
├── catalog/
│   ├── catalog.json
│   ├── build_embeddings.py
│   ├── preprocess.py
│   └── download_catalog.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Workflow | LangGraph |
| LLM | Google Gemini 2.5 Flash |
| Semantic Search | FAISS |
| Embeddings | Sentence Transformers |
| API Validation | Pydantic |
| Deployment | Docker + Hugging Face Spaces |
| Version Control | Git & GitHub |

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

### Generate Recommendations

```
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring Java Backend Developer with Spring Boot and 3 years experience"
    }
  ]
}
```

---

## 🚀 Running Locally

### Clone the repository

```bash
git clone https://github.com/Shraddha-DSA/shl-assessment-agent.git
cd shl-assessment-agent
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create `.env`

```
GEMINI_API_KEY=YOUR_API_KEY
```

### Build the FAISS index

```bash
python catalog/build_embeddings.py
```

### Start the API

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 💡 Future Improvements

- Hybrid Retrieval (BM25 + FAISS)
- Multi-turn conversations
- Cross-encoder reranking
- Streamlit/React frontend
- User feedback loop
- Analytics dashboard

---

## 👩‍💻 Author

**Shraddha Tiwari**

- GitHub: https://github.com/Shraddha-DSA
- LinkedIn: https://www.linkedin.com/in/shraddhatiwari-91549a270/

---

## ⭐ If you found this project useful, consider giving it a star!
