"""Musopen Audio Data Source (Classical & Public Domain Music).

Registered under @register_source("musopen").
"""

from typing import Any, Dict, List, Optional
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


@register_source("musopen", aliases=["classical"])
class MusopenDataSource(AudioDataSource):
    """Musopen REST API Audio Data Source."""

    source_name = "musopen"
    BASE_URL = "https://musopen.org/api/v1"

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or self.config.api_key

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search classical recordings on Musopen."""
        params: Dict[str, Any] = {
            "q": audio_filter.query or "piano",
            "limit": audio_filter.limit,
            "offset": audio_filter.offset,
        }
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            data = self._request_with_retry(
                "GET", f"{self.BASE_URL}/music/", params=params
            )
        except Exception:
            return []

        results = data.get("results", []) if isinstance(data, dict) else []
        tracks = []
        for item in results:
            license_info = LicenseInfo(
                name="Public Domain (Musopen)",
                url="https://musopen.org/music/terms/",
                is_commercial_allowed=True,
                is_attribution_required=False,
            )

            file_url = item.get("file_url") or item.get("stream_url")
            tracks.append(
                AudioTrack(
                    id=str(item.get("id", "")),
                    provider=self.source_name,
                    title=item.get("title", "Classical Piece"),
                    artist=(
                        item.get("composer", {}).get("name", "Unknown Composer")
                        if isinstance(item.get("composer"), dict)
                        else str(item.get("composer", "Unknown Composer"))
                    ),
                    duration_seconds=(
                        float(item.get("duration", 0)) if item.get("duration") else None
                    ),
                    audio_format="mp3",
                    stream_url=file_url,
                    download_url=file_url,
                    license=license_info,
                    tags=["classical", item.get("instrument", "orchestra")],
                    extra_metadata={
                        "performer": item.get("performer"),
                        "period": item.get("period"),
                    },
                )
            )
        return tracks
