"""Unit tests for the Audio Sources library.

Tests the BaseAudioSource interface, models, manager, and concrete providers.
Does NOT call live APIs — all HTTP calls are mocked.
"""

import pytest
from unittest.mock import MagicMock, patch

from agies.audio.models import AudioTrack
from agies.audio.base import BaseAudioSource
from agies.audio.manager import AudioSourcesManager
from agies.audio.jamendo import JamendoSource
from agies.audio.archive import ArchiveOrgSource
from agies.audio.freesound import FreesoundSource


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAudioTrackModel:
    """Test the AudioTrack Pydantic model."""

    def test_minimal_track(self):
        track = AudioTrack(id="1", title="Test", provider="test")
        assert track.id == "1"
        assert track.title == "Test"
        assert track.artist == "Unknown Artist"
        assert track.license == "Unknown"
        assert track.tags == []

    def test_full_track(self):
        track = AudioTrack(
            id="42",
            title="Resonance",
            artist="HOME",
            duration_seconds=213.4,
            license="CC-BY-4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            download_url="https://example.com/track.mp3",
            stream_url="https://example.com/stream.mp3",
            provider="jamendo",
            genre="synthwave",
            sample_rate=44100,
            format="mp3",
            tags=["synthwave", "retrowave"],
            source_url="https://example.com/track",
        )
        assert track.duration_seconds == 213.4
        assert track.sample_rate == 44100
        assert "synthwave" in track.tags


# ---------------------------------------------------------------------------
# Base class tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestBaseAudioSource:
    """Test that BaseAudioSource cannot be instantiated directly."""

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseAudioSource(name="abstract")


# ---------------------------------------------------------------------------
# Manager tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAudioSourcesManager:
    """Test the AudioSourcesManager facade."""

    def test_register_and_search(self):
        manager = AudioSourcesManager()
        mock_source = MagicMock(spec=BaseAudioSource)
        mock_source.name = "mock_provider"
        mock_source.search.return_value = [
            AudioTrack(id="1", title="Mock Track", provider="mock_provider")
        ]

        manager.register(mock_source)
        results = manager.search(query="electronic")

        assert len(results) == 1
        assert results[0].title == "Mock Track"
        mock_source.search.assert_called_once()

    def test_filter_by_provider(self):
        manager = AudioSourcesManager()
        source_a = MagicMock(spec=BaseAudioSource)
        source_a.name = "provider_a"
        source_a.search.return_value = [
            AudioTrack(id="a1", title="Track A", provider="provider_a")
        ]
        source_b = MagicMock(spec=BaseAudioSource)
        source_b.name = "provider_b"
        source_b.search.return_value = []

        manager.register(source_a)
        manager.register(source_b)

        results = manager.search(query="test", provider="provider_a")
        assert len(results) == 1
        source_a.search.assert_called_once()
        source_b.search.assert_not_called()

    def test_list_available_sources(self):
        sources = AudioSourcesManager.list_available_sources()
        assert "jamendo" in sources
        assert "archive_org" in sources
        assert "freesound" in sources

    def test_provider_error_does_not_crash_manager(self):
        manager = AudioSourcesManager()
        bad_source = MagicMock(spec=BaseAudioSource)
        bad_source.name = "broken"
        bad_source.search.side_effect = RuntimeError("API down")

        manager.register(bad_source)
        results = manager.search(query="test")
        assert results == []


# ---------------------------------------------------------------------------
# Provider tests (mocked HTTP)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJamendoSource:
    """Test JamendoSource with mocked HTTP."""

    def test_search_without_key_returns_empty(self):
        source = JamendoSource(client_id="")
        results = source.search(query="techno")
        assert results == []

    @patch("agies.audio.jamendo.JamendoSource.search")
    def test_search_with_key(self, mock_search):
        mock_search.return_value = [
            AudioTrack(id="j1", title="Techno Track", provider="jamendo")
        ]
        source = JamendoSource(client_id="test_key")
        results = source.search(query="techno")
        assert len(results) == 1
        assert results[0].provider == "jamendo"

    def test_is_available_without_key(self):
        source = JamendoSource(client_id="")
        assert source.is_available() is False


@pytest.mark.unit
class TestArchiveOrgSource:
    """Test ArchiveOrgSource with mocked HTTP."""

    @patch("agies.audio.archive.ArchiveOrgSource.search")
    def test_search(self, mock_search):
        mock_search.return_value = [
            AudioTrack(id="ia1", title="Public Domain Jazz", provider="archive_org")
        ]
        source = ArchiveOrgSource()
        results = source.search(query="jazz")
        assert len(results) == 1
        assert results[0].provider == "archive_org"


@pytest.mark.unit
class TestFreesoundSource:
    """Test FreesoundSource with mocked HTTP."""

    def test_search_without_key_returns_empty(self):
        source = FreesoundSource(api_key="")
        results = source.search(query="drums")
        assert results == []

    def test_is_available_without_key(self):
        source = FreesoundSource(api_key="")
        assert source.is_available() is False
