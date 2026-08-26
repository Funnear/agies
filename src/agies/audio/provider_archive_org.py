"""Internet Archive (archive.org) audio provider — public domain and CC audio.

The Internet Archive hosts millions of free audio recordings under
public domain and CC licenses. No API key required.

API docs: https://archive.org/developers/
License: Public Domain, CC-BY, CC-BY-SA, and other open licenses.
GDPR: archive.org is a US non-profit; no personal data is collected by this client.
"""

import json
import logging

import requests

from agies.audio.base_audio_provider import (
    AudioProviderConnectionError,
    AudioProviderResponseError,
    BaseAudioProvider,
)
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.provider_archive_org")

_IA_SEARCH_URL = "https://archive.org/advancedsearch.php"
_IA_DOWNLOAD_URL = "https://archive.org/download"


class ProviderArchiveOrg(BaseAudioProvider):
    """Internet Archive audio provider — no API key required."""

    def __init__(self) -> None:
        super().__init__(name="archive_org")
        self._session: requests.Session | None = None

    @property
    def session(self) -> requests.Session:
        """Create the HTTP session only when this provider is first used."""
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def search(
        self,
        query: str = "",
        genre: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
        limit: int = 10,
    ) -> list[AudioTrack]:
        """Search Internet Archive for audio files."""
        q_parts = ["mediatype:audio"]
        if query:
            q_parts.append(query)
        if genre:
            q_parts.append(f"subject:{genre}")

        q_string = " AND ".join(q_parts)
        params = {
            "q": q_string,
            "fl[]": "identifier,title,creator,licenseurl",
            "rows": min(limit, 50),
            "page": 1,
            "output": "json",
        }

        try:
            resp = self.session.get(_IA_SEARCH_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("Internet Archive search connection failed: %s", exc)
            raise AudioProviderConnectionError(
                f"Failed to connect to Internet Archive API: {exc}"
            ) from exc
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Internet Archive returned malformed response: %s", exc)
            raise AudioProviderResponseError(
                f"Failed to parse Internet Archive response: {exc}"
            ) from exc

        tracks: list[AudioTrack] = []
        docs = data.get("response", {}).get("docs", [])
        for doc in docs:
            identifier = doc.get("identifier", "")
            if not identifier:
                continue
            tracks.append(
                AudioTrack(
                    id=identifier,
                    title=doc.get("title", "Untitled"),
                    artist=doc.get("creator", "Unknown"),
                    license=doc.get("licenseurl", "Public Domain"),
                    license_url=doc.get("licenseurl"),
                    download_url=f"{_IA_DOWNLOAD_URL}/{identifier}",
                    provider=self.name,
                    genre=genre,
                    source_url=f"https://archive.org/details/{identifier}",
                )
            )

        logger.info(
            "Internet Archive returned %d items for query='%s'", len(tracks), query
        )
        return tracks

    def is_available(self) -> bool:
        """Check if archive.org is reachable."""
        try:
            resp = self.session.get(
                _IA_SEARCH_URL,
                params={"q": "mediatype:audio", "rows": 1, "output": "json"},
                timeout=10,
            )
            return resp.status_code == 200
        except requests.exceptions.RequestException as exc:
            logger.warning("Internet Archive availability check failed: %s", exc)
            return False
