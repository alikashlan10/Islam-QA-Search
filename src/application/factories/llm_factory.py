from langchain_core.language_models import BaseChatModel
from src.domain.enums.llm_provider import LLMProvider
from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class LLMFactory:
    """
    Creates LangChain BaseChatModel instances.
    All providers implement the same interface — drop-in replaceable.
    """

    def create(
        self,
        provider:    LLMProvider,
        model_name:  str,
        api_key:     str = None,
        temperature: float = 0.0,   # 0.0 = deterministic — best for QA
    ) -> BaseChatModel:

        logger.info(f"Creating LLM: provider={provider} model={model_name}")

        if provider == LLMProvider.GROQ:
            from langchain_groq import ChatGroq
            return ChatGroq(
                model_name   = model_name,
                groq_api_key = api_key,
                temperature  = temperature,
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
