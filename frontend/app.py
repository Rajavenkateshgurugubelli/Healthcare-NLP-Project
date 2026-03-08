import os

import requests
import streamlit as st

st.set_page_config(page_title="Healthcare NLP System", page_icon="🏥", layout="wide")

# Allow env var for docker networking mapping
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🏥 MedNLP-RAG Engine Explorer")
st.markdown("---")
st.markdown("""
This interface allows you to test the two core functionalities built into the system: 
**Biomedical Entity Extraction (NER)** and **Retrieval-Augmented Generation (RAG)** against clinical notes.
""")

tab1, tab2 = st.tabs(["🩺 Clinical Entity Extraction", "🧠 AI Chart Query (RAG)"])

with tab1:
    st.header("Extract Medical Entities")
    text_input = st.text_area(
        "Enter unstructured clinical text here:",
        value="Patient was diagnosed with Type 2 Diabetes Mellitus and prescribed Metformin 1000mg BID. She reports mild chest pain and shortness of breath upon exertion.",
        height=150,
    )

    if st.button("Process Clinical Text"):
        with st.spinner("Analyzing text with BioBERT..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/analyze", json={"text": text_input}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(
                        f"Processed in {data.get('metadata', {}).get('processing_time_sec', 'N/A')} seconds"
                    )
                    entities = data.get("entities", [])

                    if not entities:
                        st.info(
                            "No explicit medical entities confidently extracted from this text."
                        )
                    else:
                        st.write("### Extracted Entities")

                        # Formatting output
                        # Because of potential varying entity groups depending on HF model
                        for ent in entities:
                            group = ent.get("entity_group", "Medical_Concept")
                            word = ent.get("word", "").replace("##", "")
                            score = float(ent.get("score", 0))
                            st.markdown(
                                f"**{group}**: `{word}` (Confidence: {score:.2f})"
                            )
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(
                    f"Failed to connect to API Backend at {API_URL}. Is it running? {str(e)}"
                )

with tab2:
    st.header("Query Ingested Patient Charts")
    st.markdown(
        "Ask natural language questions against the stored patient charts vectorized using **FAISS**."
    )

    query_input = st.text_input(
        "Enter your question for the RAG engine:",
        value="What is the ejection fraction of the patient, and what is the treatment plan?",
    )

    if st.button("Query Knowledge Base", key="rag_btn"):
        with st.spinner("Searching FAISS Index and generating response..."):
            try:
                # Default top k to 3
                response = requests.post(
                    f"{API_URL}/api/v1/query", json={"query": query_input, "top_k": 3}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(
                        f"Query returned in {data.get('processing_time_sec', 'N/A')} seconds"
                    )

                    st.subheader("Answer Generation")
                    st.info(data.get("answer", "No answer generated."))

                    st.write("---")
                    st.subheader("Extracted Source Chunks")
                    sources = data.get("sources", [])
                    if sources:
                        for idx, src in enumerate(sources, 1):
                            st.markdown(f"**Source {idx}:**")
                            st.caption(f"> {src}")
                    else:
                        st.warning("No relevant sources retrieved.")
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(
                    f"Failed to connect to API Backend at {API_URL}. Is it running? {str(e)}"
                )
