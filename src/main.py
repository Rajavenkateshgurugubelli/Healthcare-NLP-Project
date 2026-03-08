import logging
import time
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .nlp_engine import NLPEngine

app = FastAPI(
    title="MedNLP-RAG Engine",
    description="High-performance Medical Entity Extraction & RAG QA API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("med-nlp-api")

nlp_engine = None


class ClinicalTextPayload(BaseModel):
    text: str
    context: Optional[str] = None


class RAGQueryPayload(BaseModel):
    query: str
    top_k: int = 3


@app.on_event("startup")
async def startup_event():
    """Load large models on API startup explicitly"""
    global nlp_engine
    logger.info("Initializing Medical NLP Core Models...")
    # NOTE: In production, models might be served via TFServing/Triton
    nlp_engine = NLPEngine(load_heavy_models=True)
    logger.info("Models loaded successfully. System ready.")


@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "MedNLP-RAG"}


@app.post("/api/v1/analyze")
async def extract_clinical_entities(payload: ClinicalTextPayload):
    """
    BioBERT/ClinicalBERT based Entity Extraction
    Identifies Medical Conditions, Anatomies, and Treatments
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided.")

    start_time = time.time()
    try:
        entities = nlp_engine.extract_entities(payload.text)
        process_time = time.time() - start_time

        logger.info(
            f"Processed {len(payload.text)} chars in {process_time:.4f} seconds."
        )
        return {
            "entities": entities,
            "metadata": {
                "processing_time_sec": round(process_time, 4),
                "model_version": "dmis-lab/biobert-v1.1",
            },
        }
    except Exception as e:
        logger.error(f"Error during NLP extraction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal ML processing error")


@app.post("/api/v1/query")
async def query_clinical_knowledge(payload: RAGQueryPayload):
    """
    Query the vector store populated with Medical Guidelines/Notes
    """
    start_time = time.time()
    try:
        answer, sources = nlp_engine.query_rag(payload.query, k=payload.top_k)
        process_time = time.time() - start_time
        return {
            "answer": answer,
            "sources": sources,
            "processing_time_sec": round(process_time, 4),
        }
    except Exception as e:
        logger.error(f"Error during RAG fetch: {str(e)}")
        raise HTTPException(status_code=500, detail="Knowledge retrieval error")
