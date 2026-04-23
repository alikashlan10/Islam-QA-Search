from langchain_core.embeddings import Embeddings
from langchain_cohere import CohereEmbeddings
from src.domain.enums.embedder_provider import EmbedderProvider
from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class EmbedderFactory:
    """
    Creates LangChain Embeddings instances.
    All providers implement the same Embeddings base class.
    """

    def create(
        self,
        provider:   EmbedderProvider,
        model_name: str,
        api_key:    str = None,
    ) -> Embeddings:

        logger.info(f"Creating embedder: provider={provider} model={model_name}")

        if provider == EmbedderProvider.COHERE:
            return CohereEmbeddings(
                model=model_name,
                cohere_api_key=api_key,
            )

        else:
            raise ValueError(f"Unsupported embedder provider: {provider}")

