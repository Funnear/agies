"""Audio Data Providers — Free, GDPR-compliant, royalty-free audio file providers.

Resolves: https://github.com/Funnear/agies/issues/4

This package provides a unified interface for discovering and fetching audio files
from free, open-licensed sources that comply with EU laws (GDPR, copyright).

Supported providers:
    - Jamendo: CC-licensed music via REST API (requires client ID)
    - Internet Archive (archive.org): Public domain and CC audio (no API key)
    - Freesound: CC-licensed sound effects and samples (requires API key)

All providers implement the ``BaseAudioProvider`` interface (Interface Segregation)
and can be registered with ``AudioSearchService`` (Dependency Inversion).
"""

import logging

from agies.audio.base_audio_provider import (
    AudioProviderAuthenticationError,
    AudioProviderConnectionError,
    AudioProviderDownloadError,
    AudioProviderError,
    AudioProviderNotRegisteredError,
    AudioProviderRateLimitError,
    AudioProviderResponseError,
    AudioProviderUnavailableError,
    BaseAudioProvider,
)
from agies.audio.model_audio_track_metadata import AudioTrack
from agies.audio.provider_archive_org import ProviderArchiveOrg
from agies.audio.provider_freesound import ProviderFreesound
from agies.audio.provider_jamendo import JamendoProvider, ProviderJamendo
from agies.audio.search_service import AudioSearchService

logger = logging.getLogger("agies.audio")

__all__ = [
    "AudioProviderAuthenticationError",
    "AudioProviderConnectionError",
    "AudioProviderDownloadError",
    "AudioProviderError",
    "AudioProviderNotRegisteredError",
    "AudioProviderRateLimitError",
    "AudioProviderResponseError",
    "AudioProviderUnavailableError",
    "AudioSearchService",
    "AudioTrack",
    "BaseAudioProvider",
    "JamendoProvider",
    "ProviderArchiveOrg",
    "ProviderFreesound",
    "ProviderJamendo",
]
