"""Pydantic models for audio track metadata."""

from typing import List, Optional

from pydantic import BaseModel, Field


class AudioTrack(BaseModel):
    """Metadata for a single audio track from any provider."""

    id: str = Field(description="Provider-specific track identifier")
    title: str = Field(description="Track title")
    artist: str = Field(default="Unknown Artist")
    duration_seconds: Optional[float] = Field(
        default=None, description="Duration in seconds"
    )
    license: str = Field(
        default="Unknown", description="License type (e.g. CC-BY-4.0, Public Domain)"
    )
    license_url: Optional[str] = Field(
        default=None, description="URL to full license text"
    )
    download_url: Optional[str] = Field(
        default=None, description="Direct download URL for the audio file"
    )
    stream_url: Optional[str] = Field(default=None, description="Streaming preview URL")
    provider: str = Field(description="Source provider name")
    genre: Optional[str] = Field(default=None, description="Genre or tag")
    sample_rate: Optional[int] = Field(default=None, description="Sample rate in Hz")
    format: Optional[str] = Field(
        default=None, description="Audio format (mp3, wav, flac, ogg)"
    )
    tags: List[str] = Field(default_factory=list, description="Tags or keywords")
    source_url: Optional[str] = Field(
        default=None, description="URL to the track page on the provider's website"
    )
