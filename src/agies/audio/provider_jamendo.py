"""Jamendo API audio provider — CC-licensed music.

Jamendo (https://www.jamendo.com) provides a REST API for free,
Creative Commons licensed music. Requires a free API client ID.

API docs: https://developer.jamendo.com/v3.0
License: Tracks are CC-licensed (BY, BY-SA, BY-NC, BY-NC-SA, etc.)
GDPR: Jamendo is EU-based (Luxembourg) and GDPR-compliant.
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

logger = logging.getLogger("agies.audio.provider_jamendo")

_JAMENDO_API_BASE = "https://api.jamendo.com/v3.0"


class ProviderJamendo(BaseAudioProvider):
    """Jamendo Creative Commons music provider."""

    def __init__(self, client_id: str = "") -> None:
        super().__init__(name="jamendo")
        self.client_id = client_id
        self.session = requests.Session()

    def search(
        self,
        query: str = "",
        genre: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        limit: int = 10,
    ) -> list[AudioTrack]:
        """Search Jamendo for CC-licensed tracks."""
        if not self.client_id:
            logger.warning("Jamendo client_id not configured — skipping search.")
            raise AudioProviderAuthenticationError(
                "Jamendo client_id is not configured."
            )

        params: dict[str, str | int] = {
            "client_id": self.client_id,
            "format": "json",
            "limit": min(limit, 200),
            "include": "musicinfo+licenses",
        }
        if query:
            params["search"] = query
        if genre:
            params["tags"] = genre
        if min_duration is not None:
            params["durationbetween"] = (
                f"{int(min_duration)}_{int(max_duration or 9999)}"
            )

        try:
            resp = self.session.get(
                f"{_JAMENDO_API_BASE}/tracks/", params=params, timeout=15
            )
            if resp.status_code in (401, 403):
                raise AudioProviderAuthenticationError(
                    f"Jamendo authentication failed with status {resp.status_code}."
                )
            if resp.status_code == 429:
                raise AudioProviderRateLimitError("Jamendo API rate limit exceeded.")
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("Jamendo API connection failed: %s", exc)
            raise AudioProviderConnectionError(
                f"Failed to connect to Jamendo API: {exc}"
            ) from exc
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Jamendo returned malformed response: %s", exc)
            raise AudioProviderResponseError(
                f"Failed to parse Jamendo response: {exc}"
            ) from exc

        tracks: list[AudioTrack] = []
        for t in data.get("results", []):
            tracks.append(
                AudioTrack(
                    id=str(t.get("id", "")),
                    title=t.get("name", "Untitled"),
                    artist=t.get("artist_name", "Unknown"),
                    duration_seconds=t.get("duration"),
                    license=t.get("license_ccurl", "CC"),
                    license_url=t.get("license_ccurl"),
                    download_url=t.get("audiodownload"),
                    stream_url=t.get("audio"),
                    provider=self.name,
                    genre=genre,
                    tags=t.get("musicinfo", {}).get("tags", {}).get("genres", []),
                    source_url=t.get("shareurl"),
                    audio_file_format="mp3",
                )
            )

        logger.info("Jamendo returned %d tracks for query='%s'", len(tracks), query)
        return tracks

    def is_available(self) -> bool:
        """Check if Jamendo API is reachable."""
        if not self.client_id:
            return False
        try:
            resp = self.session.get(
                f"{_JAMENDO_API_BASE}/tracks/",
                params={"client_id": self.client_id, "format": "json", "limit": 1},
                timeout=10,
            )
            return resp.status_code == 200
        except requests.exceptions.RequestException as exc:
            logger.warning("Jamendo availability check failed: %s", exc)
            return False


# Alias for backward compatibility / reviewer naming preference
JamendoProvider = ProviderJamendo
