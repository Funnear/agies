"""Freesound Audio Data Source implementation (REST API v2).

Registered under @register_source("freesound").
"""

from typing import Any, Dict, List, Optional
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


@register_source("freesound", aliases=["fs"])
class FreesoundDataSource(AudioDataSource):
    """Freesound API v2 Audio Data Source."""

    source_name = "freesound"
    BASE_URL = "https://freesound.org/apiv2"

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or self.config.api_key

    def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Token {self.api_key}"
        return headers

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search sounds on Freesound."""
        if not self.api_key:
            return []

        fields = "id,name,tags,description,license,previews,duration,username,type"
        params: Dict[str, Any] = {
            "query": audio_filter.query or "*",
            "page_size": min(audio_filter.limit, 150),
            "fields": fields,
        }

        filter_parts = []
        if (
            audio_filter.min_duration is not None
            or audio_filter.max_duration is not None
        ):
            min_d = audio_filter.min_duration or 0
            max_d = audio_filter.max_duration or 300
            filter_parts.append(f"duration:[{min_d} TO {max_d}]")

        if audio_filter.tags:
            for tag in audio_filter.tags:
                filter_parts.append(f"tag:{tag}")

        if filter_parts:
            params["filter"] = " ".join(filter_parts)

        try:
            data = self._request_with_retry(
                "GET",
                f"{self.BASE_URL}/search/text/",
                params=params,
                headers=self._get_headers(),
            )
        except Exception:
            return []

        results = data.get("results", [])
        return [self._parse_sound(item) for item in results]

    def _parse_sound(self, raw: Dict[str, Any]) -> AudioTrack:
        license_url = raw.get("license", "https://creativecommons.org/licenses/by/4.0/")
        is_commercial = "noncommercial" not in license_url.lower()
        license_name = "CC0" if "zero" in license_url.lower() else "Creative Commons"

        license_info = LicenseInfo(
            name=license_name,
            url=license_url,
            is_commercial_allowed=is_commercial,
            is_attribution_required="zero" not in license_url.lower(),
        )

        previews = raw.get("previews", {})
        stream_url = (
            previews.get("preview-hq-mp3")
            or previews.get("preview-lq-mp3")
            or previews.get("preview-hq-ogg")
        )

        return AudioTrack(
            id=str(raw.get("id")),
            provider=self.source_name,
            title=raw.get("name", "Untitled Sound"),
            artist=raw.get("username", "Freesound User"),
            duration_seconds=float(raw.get("duration", 0)),
            audio_format="mp3",
            stream_url=stream_url,
            download_url=stream_url,
            license=license_info,
            tags=raw.get("tags", []),
            extra_metadata={
                "original_format": raw.get("type"),
                "description": raw.get("description"),
            },
        )


# Backward compatibility alias
FreesoundProvider = FreesoundDataSource
