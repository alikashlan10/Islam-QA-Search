"""
RetrieveAnswer Use Case
========================
Full RAG pipeline:
    1. embed user query
    2. hybrid search vector store → top K chunks
    3. rerank chunks → top N most relevant
    4. build prompt with context
    5. LLM generates answer
    6. return answer + sources
"""

from dataclasses import dataclass
from typing import List

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_core.documents.compressor import BaseDocumentCompressor
from src.domain.models.query_result import RetrievalSource , RetrievalResult
from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class RetrieveAnswerUseCase:

    SYSTEM_PROMPT = """أنت مساعد متخصص في الفقه الإسلامي.
أجب على السؤال بناءً على المقاطع المقدمة فقط.
إذا لم تجد الإجابة في المقاطع، قل: "لا أعلم بناءً على المصادر المتاحة."
لا تخترع معلومات غير موجودة في المقاطع."""

    def __init__(
        self,
        embedder:     Embeddings,
        vector_store: VectorStore,
        reranker:     BaseDocumentCompressor,
        llm:          BaseChatModel,
        top_k:        int = 20,   # fetch K from vector store
        top_n:        int = 5,    # reranker keeps top N
    ) -> None:
        self._embedder     = embedder
        self._vector_store = vector_store
        self._reranker     = reranker
        self._llm          = llm
        self._top_k        = top_k
        self._top_n        = top_n

    def execute(self, query: str) -> RetrievalResult:

        logger.info(f"Processing query: {query}")

        # ── Step 1: Retrieve ───────────────────────────────────────────────────

        chunks = self._vector_store.similarity_search(
            query = query,
            k     = self._top_k,
        )
        logger.info(f"Retrieved {len(chunks)} chunks from vector store")

        if not chunks:
            return RetrievalResult(
                answer  = "لا توجد نتائج ذات صلة بسؤالك.",
                sources = [],
            )

        # ── Step 2: Rerank ─────────────────────────────────────────────────────

        reranked = self._reranker.compress_documents(
            documents = chunks,
            query     = query,
        )
        logger.info(f"Reranked to {len(reranked)} chunks")

        # ── Step 3: Build context ──────────────────────────────────────────────

        context = self._build_context(reranked)

        # ── Step 4: Generate answer ────────────────────────────────────────────

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"السؤال: {query}\n\nالمقاطع:\n{context}"),
        ]

        response = self._llm.invoke(messages)
        answer   = response.content
        logger.info("Answer generated successfully")

        # ── Step 5: Extract sources ────────────────────────────────────────────

        sources = self._extract_sources(reranked)

        return RetrievalResult(answer=answer, sources=sources)

    def _build_context(self, docs: List[Document]) -> str:
        """Formats reranked chunks into a numbered context string for the LLM."""
        return "\n\n".join(
            f"[{i+1}] {doc.page_content}"
            for i, doc in enumerate(docs)
        )

    def _extract_sources(self, docs: List[Document]) -> List[RetrievalSource]:
        """Extracts source metadata from reranked documents — deduplicated by video_id."""
        seen     = set()
        sources  = []

        for doc in docs:
            video_id = doc.metadata.get("video_id")
            if video_id and video_id not in seen:
                seen.add(video_id)
                sources.append(RetrievalSource(
                    video_id      = video_id,
                    chunk         = doc.page_content,  
                    title         = doc.metadata.get("title", ""),
                    thumbnail_url = doc.metadata.get("thumbnail_url", ""),
                    chunk_index   = doc.metadata.get("chunk_index", 0),
                ))

        return sources
