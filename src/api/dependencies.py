"""
Dependencies
=============
Composition root — creates and wires all concrete implementations.
All objects are module-level singletons, created once at startup.

Import directly in endpoints:
    from src.api.dependencies import ingest_playlist_use_case
"""

from src.config import AppConfig
from src.logger.logger import setup_logger

logger = setup_logger(__name__)
config = AppConfig()

# ── Factories ─────────────────────────────────────────────────────────────────

from src.application.factories.embedder_factory import EmbedderFactory
from src.application.factories.vector_store_factory import VectorStoreFactory
from src.application.factories.llm_factory import LLMFactory
from src.application.factories.reranker_factory import RerankerFactory

# ── Use Cases ─────────────────────────────────────────────────────────────────
from src.application.usecases.retrieve_answer_use_case import RetrieveAnswerUseCase




# ── Embedder ──────────────────────────────────────────────────────────────────

embedder = EmbedderFactory().create(
    provider   = config.EMBEDDING_PROVIDER,
    model_name = config.EMBEDDING_MODEL_NAME,
    api_key    = config.COHERE_API_KEY,   # only used if provider=google
)

# ── Reranker ──────────────────────────────────────────────────────────────────
reranker = RerankerFactory().create(
    provider= config.RERANK_PROVIDER,
    api_key= config.COHERE_API_KEY, 
    model=config.RERANK_MODEL, 
    top_n= config.TOP_N , 
)

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = LLMFactory().create(
    provider=config.LLM_PROVIDER, 
    model_name=config.GROQ_LLM_MODEL,
    api_key=config.GROQ_API_KEY,
    temperature= 0
)

# ── Vector Store ──────────────────────────────────────────────────────────────

vector_store = VectorStoreFactory().create(
    provider        = config.VECTOR_STORE_PROVIDER,
    embedder        = embedder,
    collection_name = config.QDRANT_COLLECTION_NAME,
    qdrant_url      = config.QDRANT_URL,
    qdrant_api_key  = config.QDRANT_API_KEY
)

# ── Use Cases ─────────────────────────────────────────────────────────────────

retrieve_use_case  = RetrieveAnswerUseCase(
    embedder=embedder, 
    vector_store=vector_store, 
    reranker=reranker, 
    llm=llm, 
    top_k=config.TOP_K, 
    top_n=config.TOP_N
)


logger.info("All dependencies initialized.")