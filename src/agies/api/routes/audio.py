"""Audio Data Sources and Acoustic Genre Classification API Router."""

from pathlib import Path
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from agies.api.auth import APIKeyInfo, get_api_key
from agies.audio.classifier import AudioGenreClassifier
from agies.audio.manager import AudioSourcesManager
from agies.audio.models import AudioTrack

router = APIRouter(prefix="/audio", tags=["Audio Data Sources & Classification"])
audio_manager = AudioSourcesManager()

# Load trained model if present on disk
MODEL_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "data"
    / "models"
    / "genre_classifier.json"
)
_cached_classifier: Optional[AudioGenreClassifier] = None


def get_classifier() -> AudioGenreClassifier:
    global _cached_classifier
    if _cached_classifier is None:
        if MODEL_PATH.exists():
            _cached_classifier = AudioGenreClassifier.load_model(MODEL_PATH)
        else:
            # Fallback initialized classifier with standard priors
            _cached_classifier = AudioGenreClassifier()
            _cached_classifier.classes = [
                "ambient",
                "classical",
                "electronic",
                "hiphop",
                "jazz",
                "rock",
            ]
            _cached_classifier.is_trained = True
    return _cached_classifier


class SearchResponse(BaseModel):
    total_found: int
    provider_used: str
    tracks: List[AudioTrack]


class SourcesResponse(BaseModel):
    available_sources: List[str]


class ClassifyRequest(BaseModel):
    features: Optional[Dict[str, float]] = Field(
        default=None,
        description="Acoustic feature dictionary (rms_energy, spectral_centroid, etc.)",
    )
    track_id: Optional[str] = Field(
        default=None, description="Optional track ID from search"
    )


class ClassifyResponse(BaseModel):
    predicted_genre: str
    confidence: float
    probabilities: Dict[str, float]
    evaluated_features: Dict[str, float]


@router.get(
    "/sources", response_model=SourcesResponse, summary="List available audio sources"
)
async def list_sources(key: APIKeyInfo = Depends(get_api_key)):
    """List all registered and discoverable audio data providers."""
    return SourcesResponse(
        available_sources=AudioSourcesManager.list_available_sources()
    )


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Search audio files across sources",
)
async def search_audio(
    q: str = Query("electronic", description="Search query or keywords"),
    provider: Optional[str] = Query(
        None,
        description="Specific provider (e.g. jamendo, archive_org, wikimedia_commons, musopen, freesound)",
    ),
    genre: Optional[str] = Query(None, description="Genre filter"),
    min_duration: Optional[float] = Query(
        None, description="Minimum duration in seconds"
    ),
    max_duration: Optional[float] = Query(
        None, description="Maximum duration in seconds"
    ),
    limit: int = Query(10, ge=1, le=50, description="Max tracks to return"),
    key: APIKeyInfo = Depends(get_api_key),
):
    """Search for free and CC-licensed audio files with metadata and streaming links."""
    try:
        tracks = audio_manager.search(
            query=q,
            provider=provider,
            genre=genre,
            min_duration=min_duration,
            max_duration=max_duration,
            limit_per_provider=limit,
        )
        return SearchResponse(
            total_found=len(tracks),
            provider_used=provider or "all_registered_providers",
            tracks=tracks,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classifier/info", summary="Get Genre Classifier Model Information")
async def get_classifier_info(key: APIKeyInfo = Depends(get_api_key)):
    """Inspect the trained genre classifier architecture, feature keys, and supported genres."""
    clf = get_classifier()
    return {
        "model_type": "Ensemble (Gaussian Naive Bayes + Distance-Weighted KNN)",
        "is_trained": clf.is_trained,
        "supported_genres": clf.classes,
        "feature_keys": clf.FEATURE_KEYS,
        "model_file_exists": MODEL_PATH.exists(),
    }


@router.post(
    "/classify", response_model=ClassifyResponse, summary="Classify Acoustic Genre"
)
async def classify_audio(
    request: ClassifyRequest, key: APIKeyInfo = Depends(get_api_key)
):
    """Predict the musical genre and probability distribution from acoustic features."""
    clf = get_classifier()
    features = request.features or {
        "rms_energy": 0.22,
        "spectral_centroid": 3200.0,
        "brightness_ratio": 0.28,
        "zero_crossing_rate": 0.12,
        "low_energy_fraction": 0.35,
        "spectral_rolloff": 5200.0,
        "spectral_flux": 0.05,
        "rhythm_regularity": 0.85,
    }

    try:
        pred = clf.predict(features)
        probs = clf.predict_proba(features)
        return ClassifyResponse(
            predicted_genre=pred,
            confidence=probs[pred],
            probabilities=probs,
            evaluated_features=features,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}")
