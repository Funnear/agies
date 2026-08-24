"""Audio Search Service — unified search and discovery across registered audio providers.

Implements the Dependency Inversion principle: the search service depends on the
``BaseAudioProvider`` abstraction rather than concrete provider implementations.
"""

import logging

from agies.audio.base_audio_provider import AudioProviderError, BaseAudioProvider
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.search_service")


class AudioSearchService:
    """Facade that aggregates audio file search across registered providers."""

    def __init__(self) -> None:
        self._providers: list[BaseAudioProvider] = []

    def register(self, provider: BaseAudioProvider) -> None:
        """Register an audio provider with the search service."""
        self._providers.append(provider)
        logger.info("Registered audio provider: %s", provider.name)

    def search(
        self,
        query: str = "",
        provider: str | None = None,
        genre: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        limit_per_provider: int = 10,
    ) -> list[AudioTrack]:
        """Search across all registered providers (or a specific audio provider).

        Args:
            query: Free-text search query.
            provider: If set, only search this specific provider name.
            genre: Optional genre filter.
            min_duration: Minimum duration in seconds.
            max_duration: Maximum duration in seconds.
            limit_per_provider: Max results per provider.

        Returns:
            Aggregated list of AudioTrack results.
        """
        results: list[AudioTrack] = []

        for p in self._providers:
            if provider and p.name != provider:
                continue

            try:
                tracks = p.search(
                    query=query,
                    genre=genre,
                    min_duration=min_duration,
                    max_duration=max_duration,
                    limit=limit_per_provider,
                )
                results.extend(tracks)
                logger.info("Provider '%s' returned %d tracks.", p.name, len(tracks))
            except AudioProviderError as exc:
                logger.warning(
                    "Provider '%s' failed during search: %s",
                    p.name,
                    exc,
                )

        return results

    def list_registered_sources(self) -> list[str]:
        """Return the names of all currently registered providers."""
        return [p.name for p in self._providers]
