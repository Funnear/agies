"""API Routers package."""

from agies.api.routes.audio import router as audio_router
from agies.api.routes.graph import router as graph_router
from agies.api.routes.analytics import router as analytics_router
from agies.api.routes.keys import router as keys_router
from agies.api.routes.memory import router as memory_router
from agies.api.routes.venues import router as venues_router

__all__ = [
    "audio_router",
    "graph_router",
    "analytics_router",
    "keys_router",
    "memory_router",
    "venues_router",
]
