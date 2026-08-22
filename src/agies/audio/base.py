"""Abstract base class for audio data sources (Interface Segregation Principle).

Every audio source provider must implement this interface.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from agies.audio.models import AudioTrack

logger = logging.getLogger("agies.audio.base")


class BaseAudioSource(ABC):
    """Abstract interface for a single audio data source provider.

    Implementing classes must provide:
        - ``name``: A unique provider identifier string.
        - ``search()``: Search for tracks by query, genre, and duration filters.
        - ``is_available()``: Check whether the provider is reachable.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def search(
        self,
        query: str = "",
        genre: Optional[str] = None,
        min_duration: Optional[float] = None,
        max_duration: Optional[float] = None,
        limit: int = 10,
    ) -> List[AudioTrack]:
        """Search for audio tracks matching the given criteria.

        Args:
            query: Free-text search query.
            genre: Optional genre filter.
            min_duration: Minimum duration in seconds.
            max_duration: Maximum duration in seconds.
            limit: Maximum number of results to return.

        Returns:
            List of AudioTrack objects with metadata and download/stream URLs.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider API is reachable and functional.

        Returns:
            True if the provider can serve requests.
        """
