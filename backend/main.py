"""
Main entry point for the AI FloorPlanner Backend FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from utils.logger import get_logger
from api import (
    chat_router,
    session_router,
    validate_router,
    generate_router,
    health_router,
)

# Initialize settings and logger
settings = get_settings()
logger = get_logger("main")


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Backend API for AI-Powered Floor Plan Generation",
        version=settings.APP_VERSION,
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routers
    app.include_router(health_router)
    app.include_router(session_router)
    app.include_router(chat_router)
    app.include_router(validate_router)
    app.include_router(generate_router)

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Shutting down {settings.APP_NAME}")

    return app


# Create the global app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )
