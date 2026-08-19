"""Jamendo Audio Data Source implementation (REST API v3.0).

Registered under @register_source("jamendo").
"""

from typing import Any, Dict, List, Optional
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


import os
import logging

logger = logging.getLogger("agies.audio.jamendo")


@register_source("jamendo", aliases=["jam"])
class JamendoDataSource(AudioDataSource):
    """Jamendo REST API v3.0 Audio Data Source."""

    source_name = "jamendo"
    BASE_URL = "https://api.jamendo.com/v3.0"

    def __init__(self, client_id: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.client_id = (
            client_id or self.config.client_id or os.environ.get("JAMENDO_CLIENT_ID")
        )

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search tracks on Jamendo."""
        params: Dict[str, Any] = {
            "client_id": self.client_id,
            "format": "json",
            "limit": audio_filter.limit,
            "offset": audio_filter.offset,
            "include": "musicinfo+licenses",
            "audioformat": "mp32",
        }

        if audio_filter.query:
            params["search"] = audio_filter.query
        if audio_filter.tags:
            params["tags"] = "+".join(audio_filter.tags)
        if audio_filter.genre:
            params["fuzzytags"] = audio_filter.genre
        if audio_filter.min_duration or audio_filter.max_duration:
            min_dur = int(audio_filter.min_duration or 0)
            max_dur = int(audio_filter.max_duration or 3600)
            params["durationbetween"] = f"{min_dur}_{max_dur}"

        try:
            data = self._request_with_retry(
                "GET", f"{self.BASE_URL}/tracks/", params=params
            )
        except Exception:
            return []

        results = data.get("results", [])
        return [self._parse_track(item) for item in results]

    def _parse_track(self, raw: Dict[str, Any]) -> AudioTrack:
        license_cc = raw.get(
            "license_ccurl", "https://creativecommons.org/licenses/by-nc-sa/3.0/"
        )
        is_commercial = "nc" not in license_cc.lower()

        license_info = LicenseInfo(
            name="Creative Commons (Jamendo)",
            url=license_cc,
            is_commercial_allowed=is_commercial,
            is_attribution_required=True,
        )

        stream_url = raw.get("audio")
        download_url = (
            raw.get("audiodownload")
            if raw.get("audiodownload_allowed", True)
            else stream_url
        )

        tags = []
        musicinfo = raw.get("musicinfo", {})
        if musicinfo.get("tags"):
            genres = musicinfo["tags"].get("genres", [])
            instruments = musicinfo["tags"].get("instruments", [])
            vartags = musicinfo["tags"].get("vartags", [])
            tags.extend(genres + instruments + vartags)

        return AudioTrack(
            id=str(raw.get("id")),
            provider=self.source_name,
            title=raw.get("name", "Untitled"),
            artist=raw.get("artist_name", "Unknown Artist"),
            duration_seconds=float(raw.get("duration", 0)),
            audio_format="mp3",
            stream_url=stream_url,
            download_url=download_url,
            license=license_info,
            tags=tags,
            waveform_url=raw.get("waveform"),
            extra_metadata={
                "album_name": raw.get("album_name"),
                "artist_id": raw.get("artist_id"),
                "release_date": raw.get("releasedate"),
                "bpm": musicinfo.get("bpm"),
                "speed": musicinfo.get("speed"),
            },
        )


# Backward compatibility alias
JamendoProvider = JamendoDataSource
