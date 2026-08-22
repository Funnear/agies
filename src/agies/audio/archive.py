"""Internet Archive (archive.org) audio source — public domain and CC audio.

The Internet Archive hosts millions of free audio recordings under
public domain and CC licenses. No API key required.

API docs: https://archive.org/developers/
License: Public Domain, CC-BY, CC-BY-SA, and other open licenses.
GDPR: archive.org is a US non-profit; no personal data is collected by this client.
"""

import logging
from typing import List, Optional

import requests

from agies.audio.base import BaseAudioSource
from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.archive")

_IA_SEARCH_URL = "https://archive.org/advancedsearch.php"
_IA_METADATA_URL = "https://archive.org/metadata"
_IA_DOWNLOAD_URL = "https://archive.org/download"


class ArchiveOrgSource(BaseAudioSource):
    """Internet Archive audio source — no API key required."""

    def __init__(self):
        super().__init__(name="archive_org")
        self.session = requests.Session()

    def search(
        self,
        query: str = "",
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit: int = 10,
    ) -> List[AudioTrack]:
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
            logger.error("Internet Archive search failed: %s", exc)
            return []
        except Exception as exc:
            logger.error("Unexpected error querying Internet Archive: %s", exc)
            raise

        tracks = []
        for doc in data.get("response", {}).get("docs", []):
            identifier = doc.get("identifier", "")
            tracks.append(
                AudioTrack(
                    id=identifier,
                    title=doc.get("title", "Untitled"),
                    artist=doc.get("creator", "Unknown"),
                    license=doc.get("licenseurl", "Public Domain"),
                    license_url=doc.get("licenseurl"),
                    download_url=f"{_IA_DOWNLOAD_URL}/{identifier}",
                    provider=self.name,
                    genre=genre or "",
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
        except Exception as exc:
            logger.error("Internet Archive availability check failed: %s", exc)
            return False
