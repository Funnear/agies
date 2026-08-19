"""Wikimedia Commons Audio Data Source.

Registered under @register_source("wikimedia_commons").
"""

from typing import Any, Dict, List
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


@register_source("wikimedia_commons", aliases=["wikimedia", "commons"])
class WikimediaCommonsDataSource(AudioDataSource):
    """Wikimedia Commons MediaWiki API Audio Data Source."""

    source_name = "wikimedia_commons"
    API_URL = "https://commons.wikimedia.org/w/api.php"

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search audio files on Wikimedia Commons."""
        search_term = audio_filter.query or "music"
        params: Dict[str, Any] = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:audio {search_term}",
            "gsrnamespace": 6,  # File namespace
            "gsrlimit": min(audio_filter.limit, 50),
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "format": "json",
        }

        try:
            data = self._request_with_retry("GET", self.API_URL, params=params)
        except Exception:
            return []

        pages = data.get("query", {}).get("pages", {})
        tracks = []
        for page_id, pdata in pages.items():
            imageinfo = pdata.get("imageinfo", [{}])[0]
            file_url = imageinfo.get("url")
            if not file_url:
                continue

            raw_title = pdata.get("title", "").replace("File:", "")
            extmetadata = imageinfo.get("extmetadata", {})
            artist_raw = extmetadata.get("Artist", {}).get(
                "value", "Wikimedia Contributor"
            )
            # Strip simple HTML tags from artist if present
            clean_artist = (
                artist_raw.replace("<b>", "")
                .replace("</b>", "")
                .replace("<i>", "")
                .replace("</i>", "")
            )
            license_short = extmetadata.get("LicenseShortName", {}).get(
                "value", "Creative Commons / Public Domain"
            )
            license_url = extmetadata.get("LicenseUrl", {}).get(
                "value", "https://creativecommons.org/licenses/by-sa/4.0/"
            )

            tracks.append(
                AudioTrack(
                    id=str(page_id),
                    provider=self.source_name,
                    title=raw_title,
                    artist=clean_artist[:50],
                    duration_seconds=None,
                    audio_format=(
                        "ogg"
                        if ".ogg" in file_url.lower()
                        else (
                            "mp3"
                            if ".mp3" in file_url.lower()
                            else "flac" if ".flac" in file_url.lower() else "audio"
                        )
                    ),
                    stream_url=file_url,
                    download_url=file_url,
                    license=LicenseInfo(
                        name=license_short,
                        url=license_url,
                        is_commercial_allowed=True,
                        is_attribution_required=True,
                    ),
                    tags=["wikimedia", "open_audio"],
                    extra_metadata={
                        "description": extmetadata.get("ImageDescription", {}).get(
                            "value"
                        ),
                        "mime": imageinfo.get("mime"),
                        "size_bytes": imageinfo.get("size"),
                    },
                )
            )

        return tracks
