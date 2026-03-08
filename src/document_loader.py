import os
import logging
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    LangChain-style document loader configured for Clinical Notes.
    Reads text files from a target directory and chunks them for vectorization.
    """
    def __init__(self, data_directory: str = "data"):
        self.data_directory = data_directory
        self._ensure_directory()
        
        # Setup text splitter optimized for clinical context windows
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def _ensure_directory(self):
        """Creates the data directory if it doesn't exist."""
        if not os.path.exists(self.data_directory):
            try:
                os.makedirs(self.data_directory)
                logger.info(f"Created data directory at {self.data_directory}")
            except Exception as e:
                logger.error(f"Failed to create data directory: {e}")

    def load_documents(self) -> list:
        """
        Loads all text files from the data directory.
        Returns a list of string chunks (paragraphs/documents).
        """
        try:
            loader = DirectoryLoader(self.data_directory, glob="*.txt", loader_cls=TextLoader)
            raw_documents = loader.load()
            
            if not raw_documents:
                logger.warning(f"No documents found in {self.data_directory}.")
                return []
                
            chunked_documents = self.text_splitter.split_documents(raw_documents)
            
            # Extract text content from LangChain Document objects
            documents = [doc.page_content for doc in chunked_documents]
            logger.info(f"Loaded and split {len(documents)} chunks from {self.data_directory}")
            return documents
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return []
