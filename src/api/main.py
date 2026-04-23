from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import search  

def create_app() -> FastAPI:
    app = FastAPI(
        title="Islam QA QUERY API",
        description="QUERY AND GET LLM PARSED ANSWER",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten later in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # healthcheck
    @app.get("/health")
    def health():
        return {"status": "ok"}


    # Routers 
    app.include_router(search.router)

    return app


app = create_app()