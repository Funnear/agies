"""Unified AudioSourcesManager orchestrator."""

from pathlib import Path
from typing import Dict, List, Optional
from agies.audio.datasource import (
    AudioDataSource,
    AudioSourceRegistry,
    get_audio_source,
)
from agies.audio.models import AudioTrack

# Ensure all providers are imported so they register automatically


class AudioSourcesManager:
    """Facade for searching, querying, and downloading audio from multiple providers."""

    def __init__(
        self,
        jamendo_client_id: Optional[str] = None,
        freesound_api_key: Optional[str] = None,
        musopen_api_key: Optional[str] = None,
        local_dir: str | Path = "./audio_data",
        default_timeout: int = 15,
    ):
        self.providers: Dict[str, AudioDataSource] = {
            "jamendo": get_audio_source(
                "jamendo", client_id=jamendo_client_id, timeout=default_timeout
            ),
            "freesound": get_audio_source(
                "freesound", api_key=freesound_api_key, timeout=default_timeout
            ),
            "archive_org": get_audio_source("archive_org", timeout=default_timeout),
            "musopen": get_audio_source(
                "musopen", api_key=musopen_api_key, timeout=default_timeout
            ),
            "wikimedia_commons": get_audio_source(
                "wikimedia_commons", timeout=default_timeout
            ),
            "local": get_audio_source("local", root_dir=local_dir),
        }

    def register_provider(self, name: str, provider: AudioDataSource) -> None:
        """Register a custom audio data source instance."""
        self.providers[name] = provider

    def get_provider(self, name: str) -> Optional[AudioDataSource]:
        """Get a registered provider by name."""
        return self.providers.get(name)

    @classmethod
    def list_available_sources(cls) -> List[str]:
        """List all discoverable registered data sources."""
        return AudioSourceRegistry.list_available_sources()

    def search(
        self,
        query: str = "",
        provider: Optional[str] = None,
        tags: Optional[List[str]] = None,
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit_per_provider: int = 10,
    ) -> List[AudioTrack]:
        """Search across one or all registered audio providers."""
        if provider:
            prov = self.providers.get(provider)
            if not prov:
                raise ValueError(
                    f"Unknown audio provider: '{provider}'. Available: {list(self.providers.keys())}"
                )
            return prov.search(
                query=query,
                tags=tags,
                genre=genre,
                min_duration=min_duration,
                max_duration=max_duration,
                limit=limit_per_provider,
            )

        results: List[AudioTrack] = []
        for _, prov in self.providers.items():
            try:
                tracks = prov.search(
                    query=query,
                    tags=tags,
                    genre=genre,
                    min_duration=min_duration,
                    max_duration=max_duration,
                    limit=limit_per_provider,
                )
                results.extend(tracks)
            except Exception:
                continue

        return results

    def download_track(
        self,
        track: AudioTrack,
        output_dir: str | Path = "./downloads",
        filename: Optional[str] = None,
    ) -> Path:
        """Download an audio track using its corresponding provider."""
        prov = self.providers.get(track.provider) or self.providers.get("jamendo")
        if not prov:
            raise ValueError(f"No provider found for track {track.id}")

        return prov.download_track(track, destination_dir=output_dir, filename=filename)
