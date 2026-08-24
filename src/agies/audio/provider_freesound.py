"""Freesound API audio provider — CC-licensed sound samples and effects.

Freesound (https://freesound.org) provides CC-licensed audio samples,
loops, and effects. Requires a free API key.

API docs: https://freesound.org/docs/api/
License: CC0, CC-BY, CC-BY-NC (per sound).
GDPR: Freesound is operated by UPF (Barcelona, Spain) — EU-based, GDPR-compliant.
"""

import json
import logging

import requests

from agies.audio.base_audio_provider import (
    AudioProviderAuthenticationError,
    AudioProviderConnectionError,
    AudioProviderRateLimitError,
    AudioProviderResponseError,
    BaseAudioProvider,
)
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.provider_freesound")

_FREESOUND_API_BASE = "https://freesound.org/apiv2"


class ProviderFreesound(BaseAudioProvider):
    """Freesound CC-licensed audio samples provider."""

    def __init__(self, api_key: str = "") -> None:
        super().__init__(name="freesound")
        self.api_key = api_key
        self.session = requests.Session()

    def search(
        self,
        query: str = "",
        genre: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        limit: int = 10,
    ) -> list[AudioTrack]:
        """Search Freesound for audio samples."""
        if not self.api_key:
            logger.warning("Freesound api_key not configured — skipping search.")
            raise AudioProviderAuthenticationError(
                "Freesound API key is not configured."
            )

        search_query = query
        if genre:
            search_query = f"{search_query} {genre}".strip()

        params: dict[str, str | int] = {
            "token": self.api_key,
            "query": search_query,
            "page_size": min(limit, 150),
            "fields": "id,name,username,duration,license,previews,tags,type,samplerate",
        }
        if min_duration is not None:
            params["filter"] = f"duration:[{min_duration} TO {max_duration or '*'}]"

        try:
            resp = self.session.get(
                f"{_FREESOUND_API_BASE}/search/text/", params=params, timeout=15
            )
            if resp.status_code in (401, 403):
                raise AudioProviderAuthenticationError(
                    f"Freesound authentication failed with status {resp.status_code}."
                )
            if resp.status_code == 429:
                raise AudioProviderRateLimitError("Freesound API rate limit exceeded.")
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("Freesound API connection failed: %s", exc)
            raise AudioProviderConnectionError(
                f"Failed to connect to Freesound API: {exc}"
            ) from exc
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Freesound returned malformed response: %s", exc)
            raise AudioProviderResponseError(
                f"Failed to parse Freesound response: {exc}"
            ) from exc

        tracks: list[AudioTrack] = []
        for s in data.get("results", []):
            previews = s.get("previews", {})
            tracks.append(
                AudioTrack(
                    id=str(s.get("id", "")),
                    title=s.get("name", "Untitled"),
                    artist=s.get("username", "Unknown"),
                    duration_seconds=s.get("duration"),
                    license=s.get("license", "CC"),
                    stream_url=previews.get(
                        "preview-hq-mp3", previews.get("preview-lq-mp3")
                    ),
                    provider=self.name,
                    genre=genre,
                    tags=s.get("tags", []),
                    sample_rate=s.get("samplerate"),
                    audio_file_format=s.get("type", "wav"),
                    source_url=f"https://freesound.org/people/{s.get('username')}/sounds/{s.get('id')}/",
                )
            )

        logger.info("Freesound returned %d sounds for query='%s'", len(tracks), query)
        return tracks

    def is_available(self) -> bool:
        """Check if Freesound API is reachable."""
        if not self.api_key:
            return False
        try:
            resp = self.session.get(
                f"{_FREESOUND_API_BASE}/search/text/",
                params={"token": self.api_key, "query": "test", "page_size": 1},
                timeout=10,
            )
            return resp.status_code == 200
        except requests.exceptions.RequestException as exc:
            logger.warning("Freesound availability check failed: %s", exc)
            return False
