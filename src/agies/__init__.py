"""AGIES: Audio Gathering & Industry Ecosystem System.

Provides:
- Audio Data Sources Abstraction & Registry (Jamendo, Freesound, Internet Archive, Musopen, Wikimedia Commons, Local Files)
- Audio Processing, Integrity Verification & Parallel Downloader
- Music Industry Knowledge Graph & Behavioral Pattern Analytics
- Advanced Structural Holes, K-Core Decomposition & Collaboration Prediction
- Interactive Physics Graph Visualizations
"""

from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo
from agies.audio.datasource import (
    AudioDataSource,
    AudioSourceConfig,
    AudioSourceRegistry,
    register_source,
    get_audio_source,
)
from agies.audio.processor import AudioInspector, ParallelAudioDownloader
from agies.audio.manager import AudioSourcesManager
from agies.graph.schema import (
    Artist,
    RecordLabel,
    ProductionHouse,
    Agency,
    Studio,
    Producer,
    Track,
    Release,
    RelationshipType,
)
from agies.graph.builder import MusicIndustryGraph
from agies.analytics.patterns import MusicIndustryAnalytics
from agies.analytics.advanced import AdvancedIndustryAnalytics
from agies.visualization.interactive import render_interactive_graph

__version__ = "0.2.0"

__all__ = [
    "AudioTrack",
    "AudioFilter",
    "LicenseInfo",
    "AudioDataSource",
    "AudioSourceConfig",
    "AudioSourceRegistry",
    "register_source",
    "get_audio_source",
    "AudioInspector",
    "ParallelAudioDownloader",
    "AudioSourcesManager",
    "Artist",
    "RecordLabel",
    "ProductionHouse",
    "Agency",
    "Studio",
    "Producer",
    "Track",
    "Release",
    "RelationshipType",
    "MusicIndustryGraph",
    "MusicIndustryAnalytics",
    "AdvancedIndustryAnalytics",
    "render_interactive_graph",
]
