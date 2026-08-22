"""Audio Data Sources — Free, GDPR-compliant, royalty-free audio file providers.

Resolves: https://github.com/Funnear/agies/issues/4

This package provides a unified interface for discovering and fetching audio files
from free, open-licensed sources that comply with EU laws (GDPR, copyright).

Supported providers:
    - Jamendo: CC-licensed music via REST API (API key required)
    - Free Music Archive (archive.org): Public domain and CC audio
    - Freesound: CC-licensed sound effects and samples (API key required)
    - Musopen: Public domain classical music recordings
    - Wikimedia Commons: CC/public domain audio from Wikimedia

All providers implement the ``BaseAudioSource`` interface (Interface Segregation)
and are registered via ``AudioSourcesManager`` (Dependency Inversion).
"""

import logging

logger = logging.getLogger("agies.audio")
