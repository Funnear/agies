"""Base abstract class for all audio source providers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
import requests

from agies.audio.models import AudioFilter, AudioTrack


class BaseAudioProvider(ABC):
    """Abstract base provider interface."""

    def __init__(self, name: str, timeout: int = 15):
        self.name = name
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "agies-audio-client/0.1.0 (+https://github.com/Funnear/agies)"
            }
        )

    @abstractmethod
    def search(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Search for audio tracks matching the filter criteria."""
        pass

    @abstractmethod
    def get_track(self, track_id: str) -> Optional[AudioTrack]:
        """Retrieve full details for a single track by its ID."""
        pass

    def download_track(
        self,
        track: AudioTrack,
        output_dir: str | Path,
        filename: Optional[str] = None,
        chunk_size: int = 8192,
    ) -> Path:
        """Download track audio content to a local directory.

        Args:
            track: AudioTrack to download.
            output_dir: Directory where the file should be saved.
            filename: Optional custom filename. Defaults to sanitize `{provider}_{id}.{format}`.
            chunk_size: Streaming chunk size in bytes.

        Returns:
            Path to the downloaded file.
        """
        download_url = track.download_url or track.stream_url
        if not download_url:
            raise ValueError(
                f"No downloadable or streamable URL available for track {track.id}"
            )

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        if not filename:
            # Clean filename
            sanitized_title = "".join(
                c for c in track.title if c.isalnum() or c in (" ", "_", "-")
            ).strip()
            filename = f"{track.provider}_{track.id}_{sanitized_title[:40]}.{track.audio_format}"

        destination_file = out_path / filename

        response = self.session.get(download_url, stream=True, timeout=self.timeout)
        response.raise_for_status()

        with open(destination_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        return destination_file
