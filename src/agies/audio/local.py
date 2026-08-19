"""Local Audio Directory Data Source.

Enables loading and indexing local audio directories with the unified AudioDataSource interface.
Registered under @register_source("local").
"""

from pathlib import Path
from typing import List
from agies.audio.datasource import AudioDataSource, register_source
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo


@register_source("local", aliases=["local_files", "disk"])
class LocalAudioDataSource(AudioDataSource):
    """Local filesystem audio dataset data source."""

    source_name = "local"
    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"}

    def __init__(self, root_dir: str | Path = "./audio_data", **kwargs):
        super().__init__(**kwargs)
        self.root_dir = Path(root_dir)

    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Scan root_dir for matching audio files."""
        if not self.root_dir.exists():
            return []

        tracks: List[AudioTrack] = []
        search_query = audio_filter.query.lower()

        for file_path in self.root_dir.rglob("*"):
            if (
                file_path.is_file()
                and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ):
                stem = file_path.stem
                if (
                    search_query
                    and search_query not in stem.lower()
                    and search_query not in file_path.parent.name.lower()
                ):
                    continue

                uri = file_path.resolve().as_uri()
                ext = file_path.suffix.lstrip(".").lower()

                tracks.append(
                    AudioTrack(
                        id=str(file_path.name),
                        provider=self.source_name,
                        title=stem.replace("_", " ").replace("-", " ").title(),
                        artist=(
                            file_path.parent.name
                            if file_path.parent != self.root_dir
                            else "Local User"
                        ),
                        duration_seconds=None,
                        audio_format=ext,
                        stream_url=uri,
                        download_url=uri,
                        license=LicenseInfo(
                            name="Local User Asset",
                            is_commercial_allowed=True,
                            is_attribution_required=False,
                        ),
                        tags=["local", ext],
                        extra_metadata={
                            "local_path": str(file_path),
                            "size_bytes": file_path.stat().st_size,
                        },
                    )
                )

                if len(tracks) >= audio_filter.limit:
                    break

        return tracks
