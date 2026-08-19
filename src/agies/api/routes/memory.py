"""Graphify Memory API Router."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from agies.api.auth import APIKeyInfo, get_api_key
from agies.memory.graphify import GraphifyMemory

router = APIRouter(prefix="/memory", tags=["Graphify Memory"])
memory_engine = GraphifyMemory()


class GraphifyTextRequest(BaseModel):
    text: str = Field(
        description="Narrative text, query, observation, or conversation to graphify into memory"
    )
    session_id: Optional[str] = Field(
        default="global_session", description="Session or user identifier"
    )
    context_tags: Optional[List[str]] = Field(
        default=None, description="Optional context tags"
    )
    importance: float = Field(
        default=1.0, ge=0.1, le=5.0, description="Episodic importance weight"
    )


class GraphifyAudioEventRequest(BaseModel):
    track_title: str
    artist_name: str
    predicted_genre: str
    confidence: float
    detected_bpm: Optional[float] = None
    provider: Optional[str] = None


@router.post("/graphify", summary="Graphify unstructured text into memory")
async def graphify_text(
    request: GraphifyTextRequest, key: APIKeyInfo = Depends(get_api_key)
) -> Dict[str, Any]:
    """Extract entities, concepts, and relationships from text into the persistent graph memory."""
    try:
        return memory_engine.graphify_text(
            text=request.text,
            session_id=request.session_id,
            context_tags=request.context_tags,
            importance=request.importance,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graphification failed: {e}")


@router.post("/graphify-audio", summary="Graphify an audio analysis event into memory")
async def graphify_audio(
    request: GraphifyAudioEventRequest, key: APIKeyInfo = Depends(get_api_key)
) -> Dict[str, Any]:
    """Record an audio discovery and genre classification into associative graph memory."""
    try:
        return memory_engine.graphify_audio_event(
            track_title=request.track_title,
            artist_name=request.artist_name,
            predicted_genre=request.predicted_genre,
            confidence=request.confidence,
            detected_bpm=request.detected_bpm,
            provider=request.provider,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio graphification failed: {e}")


@router.get("/recall", summary="Associative multi-hop memory recall")
async def recall_memory(
    q: str = Query(
        ..., description="Query concept or search phrase for associative memory recall"
    ),
    hops: int = Query(
        2,
        ge=1,
        le=4,
        description="Number of graph traversal hops for neighborhood context",
    ),
    top_k: int = Query(10, ge=1, le=30, description="Max memory nodes to retrieve"),
    key: APIKeyInfo = Depends(get_api_key),
) -> Dict[str, Any]:
    """Perform multi-hop associative recall across the graph memory network."""
    return memory_engine.recall(query=q, hops=hops, top_k=top_k)


@router.get("/summary", summary="Get graph memory statistics")
async def get_memory_summary(key: APIKeyInfo = Depends(get_api_key)) -> Dict[str, Any]:
    """Retrieve memory node counts, edge distributions, and top associative hubs."""
    return memory_engine.get_summary()
