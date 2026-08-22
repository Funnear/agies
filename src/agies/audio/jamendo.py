"""Jamendo API audio source — CC-licensed music.

Jamendo (https://www.jamendo.com) provides a REST API for free,
Creative Commons licensed music. Requires a free API client ID.

API docs: https://developer.jamendo.com/v3.0
License: Tracks are CC-licensed (BY, BY-SA, BY-NC, BY-NC-SA, etc.)
GDPR: Jamendo is EU-based (Luxembourg) and GDPR-compliant.
"""

import logging
from typing import List, Optional

import requests

from agies.audio.base import BaseAudioSource
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.jamendo")

# Jamendo free client IDs are available at https://devportal.jamendo.com/
_JAMENDO_API_BASE = "https://api.jamendo.com/v3.0"


class JamendoSource(BaseAudioSource):
    """Jamendo Creative Commons music source."""

    def __init__(self, client_id: str = ""):
        super().__init__(name="jamendo")
        self.client_id = client_id
        self.session = requests.Session()

    def search(
        self,
        query: str = "",
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit: int = 10,
    ) -> List[AudioTrack]:
        """Search Jamendo for CC-licensed tracks."""
        if not self.client_id:
            logger.warning("Jamendo client_id not set — skipping search.")
            return []

        params = {
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
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("Jamendo API request failed: %s", exc)
            return []
        except Exception as exc:
            logger.error("Unexpected error querying Jamendo: %s", exc)
            raise

        tracks = []
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
                    genre=genre or "",
                    tags=t.get("musicinfo", {}).get("tags", {}).get("genres", []),
                    source_url=t.get("shareurl"),
                    format="mp3",
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
        except Exception as exc:
            logger.error("Jamendo availability check failed: %s", exc)
            return False
