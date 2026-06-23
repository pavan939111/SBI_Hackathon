"""
ChromaDB client wrappers querying document vector indexing tables.
"""
import chromadb
from app.core.config import settings

def get_chroma_client() -> chromadb.API:
    """Returns configured ChromaDB client wrapper connection."""
    return chromadb.HttpClient(
        host=settings.CHROMADB_HOST,
        port=settings.CHROMADB_PORT
    )
