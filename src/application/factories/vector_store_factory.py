from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient


from src.domain.enums.vector_store_provieder import VectorStoreProvider
from src.config import AppConfig
from src.logger.logger import setup_logger

logger = setup_logger(__name__)
config = AppConfig()


class VectorStoreFactory:
    

    def create(
        self,
        provider:        VectorStoreProvider,
        embedder:        Embeddings,
        collection_name: str,
        qdrant_url:      str,
        qdrant_api_key:  str,
    ) -> VectorStore:

        if provider == VectorStoreProvider.QDRANT:
            return self._create_qdrant(
                embedder,
                collection_name,
                qdrant_url,
                qdrant_api_key,
            )

        raise ValueError(f"Unsupported vector store provider: {provider}")


    def _create_qdrant(
        self,
        embedder:        Embeddings,
        collection_name: str,
        qdrant_url:      str,
        qdrant_api_key:  str,
    ) -> QdrantVectorStore:

        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )

        # CHECK ONLY — NO CREATION
        collections = [c.name for c in client.get_collections().collections]

        if collection_name not in collections:
            raise ValueError(
                f"Qdrant collection '{collection_name}' does not exist. "
                "Make sure ingestion service created it."
            )

        # sparse embedder (BM25)
        sparse_embedder = FastEmbedSparse(model_name="Qdrant/bm25")

        return QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embedder,
            sparse_embedding=sparse_embedder,
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_vector_name="sparse",
        )