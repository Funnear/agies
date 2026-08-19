"""Internet Archive Audio Data Source (Archive.org).

Registered under @register_source("archive_org").
"""

from typing import List
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


@register_source("archive_org", aliases=["archive", "ia"])
class InternetArchiveDataSource(AudioDataSource):
    """Internet Archive Audio Data Source."""

    source_name = "archive_org"
    SEARCH_URL = "https://archive.org/advancedsearch.php"
    METADATA_URL = "https://archive.org/metadata"
    DOWNLOAD_BASE = "https://archive.org/download"

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search audio on Archive.org."""
        query_terms = ["mediatype:audio"]

        if audio_filter.query:
            query_terms.append(f"({audio_filter.query})")

        if audio_filter.genre:
            query_terms.append(f"genre:({audio_filter.genre})")

        if audio_filter.tags:
            tag_clause = " OR ".join([f"subject:({t})" for t in audio_filter.tags])
            query_terms.append(f"({tag_clause})")

        full_query = " AND ".join(query_terms)

        params = {
            "q": full_query,
            "fl[]": "identifier,title,creator,description,year,licenseurl,mediatype",
            "rows": min(audio_filter.limit, 50),
            "page": (
                (audio_filter.offset // audio_filter.limit) + 1
                if audio_filter.limit > 0
                else 1
            ),
            "output": "json",
        }

        try:
            data = self._request_with_retry("GET", self.SEARCH_URL, params=params)
        except Exception:
            return []

        docs = data.get("response", {}).get("docs", [])
        tracks = []
        for doc in docs:
            identifier = doc.get("identifier")
            if not identifier:
                continue

            license_url = doc.get(
                "licenseurl", "https://creativecommons.org/licenses/publicdomain/"
            )
            is_commercial = "nc" not in license_url.lower()

            license_info = LicenseInfo(
                name=(
                    "Public Domain / Open Access"
                    if "publicdomain" in license_url
                    else "Creative Commons"
                ),
                url=license_url,
                is_commercial_allowed=is_commercial,
                is_attribution_required="publicdomain" not in license_url,
            )

            stream_url = f"{self.DOWNLOAD_BASE}/{identifier}"
            creator = doc.get("creator", "Internet Archive Contributor")
            if isinstance(creator, list):
                creator = ", ".join(creator)

            tracks.append(
                AudioTrack(
                    id=identifier,
                    provider=self.source_name,
                    title=doc.get("title", identifier),
                    artist=creator,
                    duration_seconds=None,
                    audio_format="mp3",
                    stream_url=stream_url,
                    download_url=stream_url,
                    license=license_info,
                    tags=[str(doc.get("year", ""))] if doc.get("year") else [],
                    extra_metadata={
                        "description": doc.get("description"),
                        "identifier": identifier,
                    },
                )
            )

        return tracks


# Backward compatibility alias
InternetArchiveProvider = InternetArchiveDataSource
