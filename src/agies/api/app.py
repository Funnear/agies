from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from agies.api.routes import (
    analytics_router,
    audio_router,
    discovery_router,
    graph_router,
    keys_router,
    memory_router,
    venues_router,
)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="AGIES API (Audio Gathering & Industry Ecosystem System)",
        description="""
# AGIES API Service

### Capabilities:
- **Audio Data Sources**: Search & stream audio across Jamendo, Freesound, Internet Archive, Wikimedia Commons, Musopen, and Local storage.
- **Music Industry Knowledge Graph**: Explore entity networks connecting Artists, Record Labels, Agencies, Studios, and Producers.
- **Venue Discovery & Booking Matchmaker**: AI-matched artist discovery for music venues and direct booking contact resolution.
- **Behavioral & Predictive Analytics**: Power brokers, creative sub-communities, label mobility, SPRI studio reliance, structural holes, and collaboration link prediction.
- **Security**: Protected with Tiered API Keys (`X-API-Key`) and sliding-window rate limiting.

### Authentication:
Pass your API key in the header:
```http
X-API-Key: agies_test_key_123
```
        """,
        version="0.2.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Enable CORS for web clients & dashboards
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers under /api/v1
    app.include_router(audio_router, prefix="/api/v1")
    app.include_router(graph_router, prefix="/api/v1")
    app.include_router(analytics_router, prefix="/api/v1")
    app.include_router(keys_router, prefix="/api/v1")
    app.include_router(memory_router, prefix="/api/v1")
    app.include_router(venues_router, prefix="/api/v1")
    app.include_router(discovery_router, prefix="/api/v1")

    frontend_file = Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "index.html"

    @app.get("/", include_in_schema=False)
    @app.get("/app", include_in_schema=False)
    @app.get("/studio", include_in_schema=False)
    async def root():
        if frontend_file.exists():
            return FileResponse(frontend_file)
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["System"])
    async def health():
        return {"status": "ok", "service": "agies-api", "version": "0.2.0"}

    return app


app = create_app()
