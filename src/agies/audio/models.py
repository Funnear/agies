"""Data models for audio tracks, filters, and provider metadata."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LicenseInfo(BaseModel):
    """License details for an audio resource."""

    name: str = Field(description="License name (e.g., CC-BY 4.0, CC0, Public Domain)")
    url: Optional[str] = Field(default=None, description="Official license terms URL")
    is_commercial_allowed: bool = Field(
        default=True, description="Whether commercial use is permitted"
    )
    is_attribution_required: bool = Field(
        default=True, description="Whether attribution is required"
    )


class AudioTrack(BaseModel):
    """Normalized audio track model across all audio providers."""

    id: str = Field(description="Unique identifier for the track within the provider")
    provider: str = Field(
        description="Source provider (e.g. jamendo, freesound, archive_org)"
    )
    title: str = Field(description="Title of the audio track/sample")
    artist: str = Field(default="Unknown", description="Artist, creator, or uploader")
    duration_seconds: Optional[float] = Field(
        default=None, description="Duration in seconds"
    )
    audio_format: str = Field(
        default="mp3", description="Audio format (mp3, wav, flac, ogg)"
    )
    stream_url: Optional[str] = Field(
        default=None, description="URL for direct streaming preview"
    )
    download_url: Optional[str] = Field(
        default=None, description="URL to download the full audio file"
    )
    license: LicenseInfo = Field(
        default_factory=lambda: LicenseInfo(
            name="Creative Commons", url=None, is_commercial_allowed=True
        )
    )
    tags: List[str] = Field(
        default_factory=list, description="Tags, genres, or keywords"
    )
    waveform_url: Optional[str] = Field(
        default=None, description="Optional waveform image URL"
    )
    extra_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Raw provider metadata"
    )


@dataclass
class AudioFilter:
    """Filter parameters for querying audio providers."""

    query: str = ""
    tags: List[str] = field(default_factory=list)
    genre: Optional[str] = None
    mood: Optional[str] = None
    min_duration: Optional[float] = None
    max_duration: Optional[float] = None
    license_type: Optional[str] = None
    limit: int = 20
    offset: int = 0
