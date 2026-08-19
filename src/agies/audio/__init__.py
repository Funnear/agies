"""Audio sources, feature extraction, and genre classification module."""

from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo
from agies.audio.datasource import (
    AudioDataSource,
    AudioSourceConfig,
    AudioSourceRegistry,
    register_source,
    get_audio_source,
)
from agies.audio.jamendo import JamendoDataSource, JamendoProvider
from agies.audio.freesound import FreesoundDataSource, FreesoundProvider
from agies.audio.archive import InternetArchiveDataSource, InternetArchiveProvider
from agies.audio.musopen import MusopenDataSource
from agies.audio.wikimedia import WikimediaCommonsDataSource
from agies.audio.local import LocalAudioDataSource
from agies.audio.processor import AudioInspector, ParallelAudioDownloader
from agies.audio.manager import AudioSourcesManager
from agies.audio.features import AcousticFeatureExtractor
from agies.audio.classifier import AudioGenreClassifier
from agies.audio.dataset import AudioGenreDatasetCollector
from agies.audio.tempogram import (
    MelFilterbank,
    TempogramExtractor,
    MelTempogramExtractor,
)
from agies.audio.mel_tempogram_classifier import DeepMelTempogramClassifier

__all__ = [
    "AudioTrack",
    "AudioFilter",
    "LicenseInfo",
    "AudioDataSource",
    "AudioSourceConfig",
    "AudioSourceRegistry",
    "register_source",
    "get_audio_source",
    "JamendoDataSource",
    "JamendoProvider",
    "FreesoundDataSource",
    "FreesoundProvider",
    "InternetArchiveDataSource",
    "InternetArchiveProvider",
    "MusopenDataSource",
    "WikimediaCommonsDataSource",
    "LocalAudioDataSource",
    "AudioInspector",
    "ParallelAudioDownloader",
    "AudioSourcesManager",
    "AcousticFeatureExtractor",
    "AudioGenreClassifier",
    "AudioGenreDatasetCollector",
    "MelFilterbank",
    "TempogramExtractor",
    "MelTempogramExtractor",
    "DeepMelTempogramClassifier",
]
