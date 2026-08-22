"""Audio Sources Manager — unified search across all registered providers.

Implements the Dependency Inversion principle: high-level search logic depends
on the ``BaseAudioSource`` abstraction, not on any concrete provider.
"""

import logging
from typing import List, Optional

from agies.audio.base import BaseAudioSource
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.manager")

# Provider registry — providers that require no API key are always available.
_PROVIDER_NAMES = [
    "jamendo",
    "archive_org",
    "freesound",
]


class AudioSourcesManager:
    """Facade that aggregates search results from multiple audio sources."""

    def __init__(self):
        self._sources: List[BaseAudioSource] = []

    def register(self, source: BaseAudioSource) -> None:
        """Register an audio source provider."""
        self._sources.append(source)
        logger.info("Registered audio source: %s", source.name)

    def search(
        self,
        query: str = "",
        provider: Optional[str] = None,
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit_per_provider: int = 10,
    ) -> List[AudioTrack]:
        """Search across all registered providers (or a specific one).

        Args:
            query: Free-text search query.
            provider: If set, only search this specific provider.
            genre: Optional genre filter.
            min_duration: Minimum duration in seconds.
            max_duration: Maximum duration in seconds.
            limit_per_provider: Max results per provider.

        Returns:
            Aggregated list of AudioTrack results.
        """
        results: List[AudioTrack] = []

        for source in self._sources:
            if provider and source.name != provider:
                continue
            try:
                tracks = source.search(
                    query=query,
                    genre=genre,
                    min_duration=min_duration,
                    max_duration=max_duration,
                    limit=limit_per_provider,
                )
                results.extend(tracks)
                logger.info(
                    "Provider '%s' returned %d tracks.", source.name, len(tracks)
                )
            except Exception as exc:
                logger.error("Provider '%s' failed during search: %s", source.name, exc)

        return results

    @staticmethod
    def list_available_sources() -> List[str]:
        """List all known provider names (whether configured or not)."""
        return list(_PROVIDER_NAMES)
