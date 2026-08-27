"""Audio Search Service — unified search and discovery across registered audio providers.

Implements the Dependency Inversion principle: the search service depends on the
``BaseAudioProvider`` abstraction rather than concrete provider implementations.
"""

import logging

from agies.audio.base_audio_provider import (
    AudioProviderError,
    AudioProviderNotRegisteredError,
    BaseAudioProvider,
)
from agies.audio.model_audio_track_metadata import AudioTrack

logger = logging.getLogger("agies.audio.search_service")


class AudioSearchService:
    """Facade that aggregates audio file search across registered providers."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseAudioProvider] = {}

    def register(self, provider: BaseAudioProvider) -> None:
        """Register an audio provider with the search service."""
        provider_name = provider.name
        if provider_name in self._providers:
            logger.warning(
                "Audio provider '%s' is already registered; registration skipped.",
                provider_name,
            )
            return

        self._providers[provider_name] = provider
        logger.info(
            "Registered audio provider: %s",
            self._providers[provider_name].name,
        )

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

        for current_provider in self._select_providers(provider):
            if not current_provider.is_available():
                logger.warning("Provider '%s' is unavailable.", current_provider.name)
                continue

            try:
                tracks = current_provider.search(
                    query=query,
                    genre=genre,
                    min_duration=min_duration,
                    max_duration=max_duration,
                    limit=limit_per_provider,
                )
                results.extend(tracks)
                logger.info(
                    "Provider '%s' returned %d tracks.",
                    current_provider.name,
                    len(tracks),
                )
            except AudioProviderError as exc:
                logger.warning(
                    "Provider '%s' failed during search: %s",
                    current_provider.name,
                    exc,
                )

        return results

    def _select_providers(self, provider: str | None) -> list[BaseAudioProvider]:
        """Select a specific registered provider or all registered providers."""
        if provider is None:
            return list(self._providers.values())

        try:
            return [self._providers[provider]]
        except KeyError as exc:
            raise AudioProviderNotRegisteredError(provider) from exc
