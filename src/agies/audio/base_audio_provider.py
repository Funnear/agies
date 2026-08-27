"""Abstract base provider interface and domain exceptions for audio data sources.

Every audio source provider must inherit from ``BaseAudioProvider`` and raise
domain-specific ``AudioProviderError`` subclasses upon expected failures.
"""

import logging
from abc import ABC, abstractmethod

from agies.audio.model_audio_track_metadata import AudioTrack

logger = logging.getLogger("agies.audio.base_audio_provider")


# ---------------------------------------------------------------------------
# Domain Exceptions
# ---------------------------------------------------------------------------


class AudioProviderError(Exception):
    """Base exception for all domain-level audio provider errors."""


class AudioProviderConnectionError(AudioProviderError):
    """Raised when a provider is unreachable due to network, DNS, or timeout failure."""


class AudioProviderAuthenticationError(AudioProviderError):
    """Raised when API credentials are missing, invalid, or expired."""


class AudioProviderRateLimitError(AudioProviderError):
    """Raised when a provider rejects requests due to rate limiting or quota exhaustion."""


class AudioProviderResponseError(AudioProviderError):
    """Raised when a provider returns an invalid, malformed, or unparseable response."""


class AudioProviderDownloadError(AudioProviderError):
    """Raised when track metadata was found, but the audio file cannot be downloaded."""


class AudioProviderUnavailableError(AudioProviderError):
    """Raised when a provider is temporarily unavailable or returns a service-level failure."""


class AudioProviderNotRegisteredError(AudioProviderError):
    """Raised when a requested audio provider is not registered."""


# ---------------------------------------------------------------------------
# Base Provider Interface
# ---------------------------------------------------------------------------


class BaseAudioProvider(ABC):
    """Abstract interface for a single audio data source provider.

    Implementing classes must provide:
        - ``name``: A unique provider identifier string.
        - ``search()``: Search for tracks by query, genre, and duration filters.
        - ``is_available()``: Check whether the provider is reachable.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def search(
        self,
        query: str = "",
        genre: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        limit: int = 10,
    ) -> list[AudioTrack]:
        """Search for audio tracks matching the given criteria.

        Args:
            query: Free-text search query.
            genre: Optional genre filter.
            min_duration: Minimum duration in seconds.
            max_duration: Maximum duration in seconds.
            limit: Maximum number of results to return.

        Returns:
            List of AudioTrack objects with metadata and download/stream URLs.

        Raises:
            AudioProviderError: If the provider experiences an operational failure.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider API is reachable and functional.

        Returns:
            True if the provider can serve requests.
        """
