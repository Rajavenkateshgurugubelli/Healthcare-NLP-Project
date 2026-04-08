# CONTEXT.md — Healthcare NLP System (MedNLP-RAG Core)
# READ THIS FILE FIRST BEFORE WRITING ANY CODE OR ANSWERING ANY QUESTION.
# This is the single source of truth for the entire project.

---

## PROJECT IDENTITY

- **Project Name:** Healthcare NLP System (MedNLP-RAG Core)
- **Description:** A production-ready Natural Language Processing API designed for the healthcare domain. Extracts medical entities via BioBERT and answers clinical queries via Retrieval-Augmented Generation (RAG).
- **GitHub Repo:** Healthcare-NLP-Project
- **Owner:** Raja Venkatesh Gurugubelli
- **Status:** Planning / In Development

---

## TECH STACK (LOCKED)

| Component         | Technology              | Version / Details                        |
|-------------------|-------------------------|------------------------------------------|
| Language          | Python                  | >= 3.9                                   |
| Web Framework     | FastAPI                 | Backend REST API                         |
| Frontend          | Streamlit               | Decoupled interactive UI                 |
| RAG Engine        | LangChain               | Orchestration & chunking                 |
| Vector Database   | FAISS                   | In-memory fast similarity search         |
| Embeddings        | SentenceTransformers    | `all-MiniLM-L6-v2`                       |
| NLP / NER Model   | HuggingFace Transformers| `d4data/biomedical-ner-all` (BioBERT)    |
| Environment       | Docker / Docker Compose | Multi-container architecture             |

---

## EXACT PROJECT FOLDER STRUCTURE

```text
Healthcare-NLP-Project/
├── CONTEXT.md                  ← THIS FILE (Project Source of Truth)
├── README.md                   ← High-level overview
├── requirements.txt            ← Backend & ML dependencies
├── requirements-dev.txt        ← Testing dependencies (pytest, etc.)
├── Dockerfile                  ← Backend image definition
├── docker-compose.yml          ← Complete stack orchestration
├── Makefile                    ← Dev environment shortcuts
├── test_client.py              ← E2E API integration test script
├── data/
│   └── patient_10294.txt       ← Sample clinical notes for RAG ingestion
├── src/
│   ├── __init__.py
│   ├── main.py                 ← FastAPI entry point and routes
│   ├── nlp_engine.py           ← BioBERT and FAISS wrappers
│   └── document_loader.py      ← Text ingestion and chunking logic
├── frontend/
│   ├── Dockerfile              ← Streamlit image definition
│   └── app.py                  ← Streamlit UI implementation
└── tests/
    └── test_api.py             ← Pytest suites (To be implemented)
```

---

## IMPLEMENTATION PHASES & STATUS

Track completion here. Update when a phase is done.

- [x] Phase 0: Planning & Architecture (CONTEXT.md created)
- [x] Phase 1: Environment & Tooling (requirements.txt, Dockerfile, docker-compose.yml)
- [x] Phase 2: RAG Pipeline & Data Ingestion (LangChain splitters, FAISS indexing in nlp_engine.py)
- [x] Phase 3: Core NLP & Model Serving (BioBERT NER via d4data/biomedical-ner-all)
- [x] Phase 4: Backend API (FastAPI /analyze + /query endpoints with error handling)
- [x] Phase 5: Frontend UI (Streamlit with NER tab + RAG query tab)
- [x] Phase 6: Testing & QA (Pytest suite with health, analyze, query tests)

---

## ARCHITECTURE & CRITICAL RULES

### 1. Data Ingestion (RAG)
- Clinical notes must reside in the `data/` directory.
- `src/document_loader.py` must handle large text splitting appropriately (e.g., LangChain's `RecursiveCharacterTextSplitter` with healthcare-specific overlap).
- FAISS indices should be built in-memory on application startup (`startup_event` in `main.py`).

### 2. NLP Inference (NER)
- Use HuggingFace pipeline with `aggregation_strategy="simple"` to group subwords into full medical terms.
- For prototyping speed on CPU, we use `d4data/biomedical-ner-all`.
- Load heavy models **only once** upon application startup to prevent memory leaks and high inference latency.

### 3. FastAPI Backend
- Must run asynchronously (`uvicorn`).
- Endpoints must have robust exception handling (`HTTPException`) to never crash the main process on bad user input.
- Cross-Origin Resource Sharing (CORS) must be enabled to allow decoupled frontend communcation.

### 4. Streamlit Frontend
- Must run in an isolated environment/container.
- Communicates to the backend strictly via HTTP REST definitions. Read `API_URL` from environment variables.
- UI elements should be clean, abstracting the complexity of NLP.

---

## TARGET METRICS

| Metric | Target |
|---|---|
| API Inference Latency (NER) | < 1.0s per paragraph |
| RAG Retrieval Latency | < 500ms per query |
| Test Coverage | > 80% across `src/` |

---

## HOW TO USE THIS FILE (FOR AI ASSISTANTS)

When starting any session on this project:
1. Read this entire `CONTEXT.md` file first.
2. Check the Phase Status checkboxes to know where work left off.
3. Follow the locked Tech Stack strictly.
4. After completing a phase, update the checkbox in this file.
