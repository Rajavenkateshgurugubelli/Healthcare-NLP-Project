import os
import glob
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    Simulates a LangChain-style document loader configured for Clinical Notes.
    Reads text files from a target directory and chunks them for vectorization.
    """
    def __init__(self, data_directory: str = "data"):
        self.data_directory = data_directory
        self._ensure_directory()

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
        search_pattern = os.path.join(self.data_directory, "*.txt")
        file_paths = glob.glob(search_pattern)
        
        documents = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # A naive sentence chunking strategy.
                    chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 10]
                    documents.extend(chunks)
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
                
        if not documents:
            logger.warning(f"No documents found in {self.data_directory}. Fallback to default knowledge base.")

        return documents
