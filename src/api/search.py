from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import SearchRequest
from src.domain.models.query_result import RetrievalResult
from src.api.auth import verify_api_key
from src.api.dependencies import retrieve_use_case
from src.logger.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=RetrievalResult)
def search(request:  SearchRequest, _: str = Depends(verify_api_key),) -> RetrievalResult:

    if not request.query.strip():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Query cannot be empty",
        )

    logger.info(f"Search request: {request.query}")

    return retrieve_use_case.execute(query = request.query)