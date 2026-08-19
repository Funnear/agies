"""High-level Audio Data Source Abstraction Layer.

Designed for sole contributors and small teams to add, configure, and maintain
new audio data sources with minimal boilerplate, automatic caching, retry logic,
and a pluggable registry.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import hashlib
import json
import logging
from pathlib import Path
import time
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type, Union
import requests

from agies.audio.models import AudioFilter, AudioTrack

logger = logging.getLogger("agies.audio.datasource")


@dataclass
class AudioSourceConfig:
    """Configuration for an audio data source."""

    api_key: Optional[str] = None
    client_id: Optional[str] = None
    timeout: int = 15
    max_retries: int = 3
    retry_backoff_factor: float = 1.5
    cache_dir: Optional[Path] = None
    enable_cache: bool = True
    rate_limit_delay_seconds: float = 0.0
    extra_headers: Dict[str, str] = field(default_factory=dict)


class AudioSourceRegistry:
    """Central registry for all audio data sources."""

    _registry: ClassVar[Dict[str, Type["AudioDataSource"]]] = {}

    @classmethod
    def register(cls, name: str, aliases: Optional[List[str]] = None) -> Callable:
        """Decorator to register an AudioDataSource implementation."""

        def decorator(subclass: Type["AudioDataSource"]):
            subclass.source_name = name.lower()
            cls._registry[name.lower()] = subclass
            if aliases:
                for alias in aliases:
                    cls._registry[alias.lower()] = subclass
            return subclass

        return decorator

    @classmethod
    def get(
        cls, name: str, config: Optional[AudioSourceConfig] = None, **kwargs
    ) -> "AudioDataSource":
        """Instantiate a registered data source by name."""
        name_lower = name.lower()
        if name_lower not in cls._registry:
            available = list(cls._registry.keys())
            raise ValueError(
                f"Unknown audio source '{name}'. Available sources: {available}"
            )

        source_cls = cls._registry[name_lower]
        return source_cls(config=config, **kwargs)

    @classmethod
    def list_available_sources(cls) -> List[str]:
        """Return unique registered source names."""
        return sorted(list(set(cls._registry.keys())))


# Global shortcut decorator
register_source = AudioSourceRegistry.register


class AudioDataSource(ABC):
    """Abstract base data source for all audio providers.

    Sole-contributor ergonomic design:
    - Automatically handles caching, request retries, rate limits, and chunked downloads.
    - Subclasses only need to implement `_fetch_tracks(query_filter)`.
    """

    source_name: str = "base_source"
    supports_commercial_filter: bool = True
    supports_duration_filter: bool = True
    supports_tag_filter: bool = True

    def __init__(self, config: Optional[AudioSourceConfig] = None, **kwargs):
        self.config = config or AudioSourceConfig(**kwargs)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "agies-audio-client/0.1.0 (+https://github.com/Funnear/agies)",
                **self.config.extra_headers,
            }
        )
        self._last_request_time = 0.0

        if self.config.cache_dir:
            self.cache_dir = Path(self.config.cache_dir)
        else:
            self.cache_dir = (
                Path.home() / ".cache" / "agies" / "audio" / self.source_name
            )

        if self.config.enable_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _rate_limit(self) -> None:
        """Enforce rate limiting delays if configured."""
        if self.config.rate_limit_delay_seconds > 0:
            elapsed = time.time() - self._last_request_time
            if elapsed < self.config.rate_limit_delay_seconds:
                time.sleep(self.config.rate_limit_delay_seconds - elapsed)
        self._last_request_time = time.time()

    def _get_cache_key(self, prefix: str, data: Any) -> str:
        """Generate a deterministic MD5 cache key."""
        serialized = json.dumps(data, sort_keys=True, default=str)
        digest = hashlib.md5(serialized.encode("utf-8")).hexdigest()
        return f"{prefix}_{digest}.json"

    def _request_with_retry(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """Perform HTTP request with caching and exponential backoff retries."""
        cache_file = None
        if self.config.enable_cache and use_cache and method.upper() == "GET":
            cache_key = self._get_cache_key("req", {"url": url, "params": params})
            cache_file = self.cache_dir / cache_key
            if cache_file.exists():
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to read cache {cache_file}: {e}")

        # Execute request with retry
        self._rate_limit()
        retries = 0
        backoff = 1.0

        while retries <= self.config.max_retries:
            try:
                resp = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                )
                resp.raise_for_status()
                result = resp.json()

                # Save cache
                if cache_file and self.config.enable_cache:
                    try:
                        with open(cache_file, "w", encoding="utf-8") as f:
                            json.dump(result, f)
                    except Exception as e:
                        logger.warning(f"Failed to write cache {cache_file}: {e}")

                return result

            except requests.exceptions.RequestException as e:
                retries += 1
                if retries > self.config.max_retries:
                    logger.error(
                        f"Request failed after {self.config.max_retries} retries: {e}"
                    )
                    raise
                time.sleep(backoff)
                backoff *= self.config.retry_backoff_factor

        return {}

    @abstractmethod
    def _fetch_tracks(self, audio_filter: AudioFilter) -> List[AudioTrack]:
        """Provider-specific search logic to override in subclasses."""
        pass

    def search(
        self,
        query: str = "",
        tags: Optional[List[str]] = None,
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[AudioTrack]:
        """Search tracks using clean, ergonomic kwargs."""
        audio_filter = AudioFilter(
            query=query,
            tags=tags or [],
            genre=genre,
            min_duration=min_duration,
            max_duration=max_duration,
            limit=limit,
            offset=offset,
        )
        return self._fetch_tracks(audio_filter)

    def download_track(
        self,
        track: AudioTrack,
        destination_dir: Union[str, Path] = "./downloads",
        filename: Optional[str] = None,
        chunk_size: int = 8192,
    ) -> Path:
        """Download track to local destination with sanitization and validation."""
        target_url = track.download_url or track.stream_url
        if not target_url:
            raise ValueError(f"Track '{track.id}' has no downloadable URL.")

        out_dir = Path(destination_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            safe_title = "".join(
                c for c in track.title if c.isalnum() or c in (" ", "_", "-")
            ).strip()
            filename = (
                f"{track.provider}_{track.id}_{safe_title[:30]}.{track.audio_format}"
            )

        dest_file = out_dir / filename
        if dest_file.exists() and dest_file.stat().st_size > 0:
            logger.info(f"Using existing cached download: {dest_file}")
            return dest_file

        self._rate_limit()
        resp = self.session.get(target_url, stream=True, timeout=self.config.timeout)
        resp.raise_for_status()

        with open(dest_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        return dest_file

    def download_batch(
        self,
        tracks: List[AudioTrack],
        destination_dir: Union[str, Path] = "./downloads",
    ) -> List[Path]:
        """Download multiple tracks sequentially."""
        downloaded = []
        for t in tracks:
            try:
                path = self.download_track(t, destination_dir=destination_dir)
                downloaded.append(path)
            except Exception as e:
                logger.error(f"Failed downloading track {t.id}: {e}")
        return downloaded


def get_audio_source(name: str, **kwargs) -> AudioDataSource:
    """Convenience helper to instantiate an audio data source."""
    return AudioSourceRegistry.get(name, **kwargs)
