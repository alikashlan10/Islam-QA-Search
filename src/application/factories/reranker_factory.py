from langchain_core.documents.compressor import BaseDocumentCompressor
from src.domain.enums.reranker_provider import RerankerProvider
from src.logger.logger import setup_logger
from src.config import AppConfig

logger = setup_logger(__name__)
config = AppConfig()

class _PassthroughReranker(BaseDocumentCompressor):
    """
    No-op reranker — returns documents unchanged.
    Useful for testing or when reranking is not needed.
    """
    top_n : int

    def compress_documents(self, documents, query, callbacks=None):
        return documents[:self.top_n]

    class Config:
        arbitrary_types_allowed = True


class RerankerFactory:
    """
    Creates LangChain BaseDocumentCompressor instances.
    All providers implement the same interface — drop-in replaceable.
    """

    def create(
        self,
        provider:  RerankerProvider,
        api_key:   str = None,
        model:     str = None,
        top_n:     int = 5,
    ) -> BaseDocumentCompressor:

        logger.info(f"Creating reranker: provider={provider} top_n={top_n}")

        if provider == RerankerProvider.NONE:
            return _PassthroughReranker(top_n=top_n)

        elif provider == RerankerProvider.COHERE:
            from langchain_cohere import CohereRerank
            return CohereRerank(
                cohere_api_key = api_key,
                model          = model ,
                top_n          = top_n,
            )


        else:
            raise ValueError(f"Unsupported reranker provider: {provider}")
