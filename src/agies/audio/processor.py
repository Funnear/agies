"""Audio Processing, Integrity Verification, and Parallel Downloading Engine."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import logging
from pathlib import Path
import struct
from typing import Any, Dict, List, Optional, Tuple, Union
import requests

from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.processor")


class AudioInspector:
    """Inspects audio files, validates format headers, and verifies file integrity."""

    @staticmethod
    def inspect_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze local audio file headers and metadata."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = p.stat().st_size
        ext = p.suffix.lower()

        # Read first 128 bytes for header signature verification
        with open(p, "rb") as f:
            header = f.read(128)

        is_valid = False
        detected_format = "unknown"
        extra: Dict[str, Any] = {}

        if header.startswith(b"ID3") or (
            len(header) > 1 and header[0] == 0xFF and (header[1] & 0xE0) == 0xE0
        ):
            is_valid = True
            detected_format = "mp3"
        elif header.startswith(b"RIFF") and b"WAVE" in header[:16]:
            is_valid = True
            detected_format = "wav"
            if len(header) >= 36:
                try:
                    channels = struct.unpack_from("<H", header, 22)[0]
                    sample_rate = struct.unpack_from("<I", header, 24)[0]
                    bits_per_sample = struct.unpack_from("<H", header, 34)[0]
                    extra = {
                        "channels": channels,
                        "sample_rate": sample_rate,
                        "bits_per_sample": bits_per_sample,
                    }
                except Exception:
                    pass
        elif header.startswith(b"OggS"):
            is_valid = True
            detected_format = "ogg"
        elif header.startswith(b"fLaC"):
            is_valid = True
            detected_format = "flac"
        elif file_size > 0:
            # General audio fallback
            is_valid = True
            detected_format = ext.lstrip(".")

        return {
            "file_path": str(p.resolve()),
            "file_name": p.name,
            "file_size_bytes": file_size,
            "detected_format": detected_format,
            "is_header_valid": is_valid,
            "sha256": (
                hashlib.sha256(p.read_bytes()).hexdigest()
                if file_size < 50 * 1024 * 1024
                else None
            ),
            **extra,
        }

    @staticmethod
    def verify_stream_url(
        url: str, timeout: int = 10
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """Verify if a remote audio stream URL is active and return MIME type and content length."""
        try:
            resp = requests.head(url, allow_redirects=True, timeout=timeout)
            if resp.status_code >= 400:
                # Some servers disallow HEAD, retry with GET stream
                resp = requests.get(url, stream=True, timeout=timeout)

            content_type = resp.headers.get("Content-Type", "")
            content_length = (
                int(resp.headers.get("Content-Length", 0))
                if resp.headers.get("Content-Length")
                else None
            )
            is_valid = resp.status_code == 200 and (
                "audio" in content_type
                or "application/ogg" in content_type
                or "octet-stream" in content_type
            )
            return is_valid, content_type, content_length
        except Exception:
            return False, None, None


class ParallelAudioDownloader:
    """Thread-safe parallel downloader for batch audio harvesting."""

    def __init__(self, max_workers: int = 4, timeout: int = 20):
        self.max_workers = max_workers
        self.timeout = timeout

    def download_tracks_parallel(
        self,
        tracks: List[AudioTrack],
        output_dir: Union[str, Path] = "./downloads",
    ) -> Dict[str, Union[Path, Exception]]:
        """Download multiple tracks concurrently with progress reporting."""
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        results: Dict[str, Union[Path, Exception]] = {}

        def _download_single(track: AudioTrack) -> Tuple[str, Path]:
            url = track.download_url or track.stream_url
            if not url:
                raise ValueError(f"No download URL for track {track.id}")

            safe_title = "".join(
                c for c in track.title if c.isalnum() or c in (" ", "_", "-")
            ).strip()
            fname = (
                f"{track.provider}_{track.id}_{safe_title[:30]}.{track.audio_format}"
            )
            dest = out_dir / fname

            if dest.exists() and dest.stat().st_size > 0:
                return track.id, dest

            resp = requests.get(url, stream=True, timeout=self.timeout)
            resp.raise_for_status()

            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=16384):
                    if chunk:
                        f.write(chunk)

            return track.id, dest

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_track = {executor.submit(_download_single, t): t for t in tracks}
            for future in as_completed(future_to_track):
                track = future_to_track[future]
                try:
                    tid, path = future.result()
                    results[tid] = path
                except Exception as e:
                    results[track.id] = e
                    logger.error(f"Failed downloading {track.title}: {e}")

        return results
