"""Pydantic model for audio track metadata."""

from typing import Literal

from pydantic import BaseModel, Field


class AudioTrack(BaseModel):
    """Metadata for a single audio track from any provider."""

    # --- Identity & Source ---
    id: str = Field(
        description="Provider-specific track identifier",
    )
    title: str = Field(
        description="Track title",
    )
    artist: str = Field(
        default="Unknown Artist",
        description="Artist or creator name",
    )
    provider: str = Field(
        description="Source provider name",
    )
    source_url: str | None = Field(
        default=None,
        description="URL to the track page on the provider's website",
    )

    # --- Media & Streaming ---
    download_url: str | None = Field(
        default=None,
        description="Direct download URL for the audio file",
    )
    stream_url: str | None = Field(
        default=None,
        description="Streaming preview URL",
    )

    # --- Licensing & Rights ---
    license: str = Field(
        default="Unknown",
        description="License type (e.g. CC-BY-4.0, Public Domain)",
    )
    license_url: str | None = Field(
        default=None,
        description="URL to full license text",
    )

    # --- Musical & Technical Attributes ---
    duration_seconds: float | None = Field(
        default=None,
        description="Duration in seconds",
    )
    genre: str | None = Field(
        default=None,
        description="Genre or tag",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags or keywords",
    )
    sample_rate: int | None = Field(
        default=None,
        description="Sample rate in Hz",
    )
    audio_file_format: Literal["mp3", "wav", "flac", "ogg", "aiff"] | None = Field(
        default=None,
        description="Audio format supported by the registered providers",
    )
