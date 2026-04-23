from pydantic_settings import BaseSettings
from src.domain.enums.vector_store_provieder import VectorStoreProvider
from src.domain.enums.embedder_provider import EmbedderProvider
from src.domain.enums.reranker_provider import RerankerProvider
from src.domain.enums.llm_provider import LLMProvider
import os 

class AppConfig(BaseSettings):

    # Logs
    LOG_LEVEL:str = "INFO"
    LOG_FILE:str = "logs/app.log"

    # LLMs
    GROQ_LLM_MODEL:str = "openai/gpt-oss-120b"
    GROQ_API_KEY:str = ""
    LLM_PROVIDER : LLMProvider = LLMProvider.GROQ

    ##Vectordb
    QDRANT_URL:str = ""
    QDRANT_COLLECTION_NAME:str = "islam_qa_v2"
    QDRANT_API_KEY:str = ""
    QDRANT_VECTOR_SIZE : int = 1024
    VECTOR_STORE_PROVIDER:  VectorStoreProvider= VectorStoreProvider.QDRANT
    TOP_K : int = 20

    ##rerank model
    RERANK_MODEL:str = "rerank-multilingual-v3.0",
    RERANK_PROVIDER : RerankerProvider = RerankerProvider.COHERE
    TOP_N : int = 5
    
    ##Emebdding model
    EMBEDDING_MODEL_NAME:str = ""
    COHERE_API_KEY:str = ""
    EMBEDDING_PROVIDER:     EmbedderProvider   = EmbedderProvider.COHERE

    ##App
    API_KEY:str = ""
    
    class Config:
        env_file = ".env"

