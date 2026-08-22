"""Unit tests for the Audio Sources library.

Tests the BaseAudioSource interface, models, manager, and concrete providers.
Uses mock HTTP responses to verify JSON parsing, query generation, and error handling.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from agies.audio.archive import ArchiveOrgSource
from agies.audio.base import BaseAudioSource
from agies.audio.freesound import FreesoundSource
from agies.audio.jamendo import JamendoSource
from agies.audio.manager import AudioSourcesManager
from agies.audio.models import AudioTrack

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
        mock_source.search.assert_called_once_with(
            query="electronic",
            genre=None,
            min_duration=None,
            max_duration=None,
            limit=10,
        )

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
# Provider tests with mocked network responses
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJamendoSource:
    """Test JamendoSource JSON parsing and parameters."""

    def test_search_without_key_returns_empty(self):
        source = JamendoSource(client_id="")
        results = source.search(query="techno")
        assert results == []

    @patch("requests.Session.get")
    def test_search_success_parsing(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "results": [
                {
                    "id": "12345",
                    "name": "Deep Resonance",
                    "artist_name": "Artist Alpha",
                    "duration": 180.0,
                    "license_ccurl": "https://creativecommons.org/licenses/by/4.0/",
                    "audiodownload": "https://download.jamendo.com/12345.mp3",
                    "audio": "https://stream.jamendo.com/12345.mp3",
                    "shareurl": "https://www.jamendo.com/track/12345",
                    "musicinfo": {"tags": {"genres": ["techno", "electronic"]}},
                }
            ]
        }
        mock_get.return_value = mock_resp

        source = JamendoSource(client_id="test_key")
        results = source.search(
            query="techno", genre="electronic", min_duration=60, max_duration=300
        )

        assert len(results) == 1
        track = results[0]
        assert track.id == "12345"
        assert track.title == "Deep Resonance"
        assert track.artist == "Artist Alpha"
        assert track.provider == "jamendo"
        assert track.download_url == "https://download.jamendo.com/12345.mp3"
        assert "techno" in track.tags

    @patch("requests.Session.get")
    def test_search_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException(
            "Connection timeout"
        )
        source = JamendoSource(client_id="test_key")
        results = source.search(query="techno")
        assert results == []

    @patch("requests.Session.get")
    def test_is_available_true(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        source = JamendoSource(client_id="test_key")
        assert source.is_available() is True

    def test_is_available_without_key(self):
        source = JamendoSource(client_id="")
        assert source.is_available() is False


@pytest.mark.unit
class TestArchiveOrgSource:
    """Test ArchiveOrgSource JSON parsing and queries."""

    @patch("requests.Session.get")
    def test_search_success_parsing(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "response": {
                "docs": [
                    {
                        "identifier": "audio_sample_01",
                        "title": "Public Domain Classical",
                        "creator": "Symphony Orchestra",
                        "licenseurl": "https://creativecommons.org/publicdomain/zero/1.0/",
                    }
                ]
            }
        }
        mock_get.return_value = mock_resp

        source = ArchiveOrgSource()
        results = source.search(query="classical", genre="symphony", limit=5)

        assert len(results) == 1
        track = results[0]
        assert track.id == "audio_sample_01"
        assert track.title == "Public Domain Classical"
        assert track.artist == "Symphony Orchestra"
        assert track.provider == "archive_org"
        assert "archive.org/download/audio_sample_01" in track.download_url

    @patch("requests.Session.get")
    def test_search_error_handling(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Server error")
        source = ArchiveOrgSource()
        results = source.search(query="test")
        assert results == []

    @patch("requests.Session.get")
    def test_is_available_true(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        source = ArchiveOrgSource()
        assert source.is_available() is True


@pytest.mark.unit
class TestFreesoundSource:
    """Test FreesoundSource JSON parsing and queries."""

    def test_search_without_key_returns_empty(self):
        source = FreesoundSource(api_key="")
        results = source.search(query="drums")
        assert results == []

    @patch("requests.Session.get")
    def test_search_success_parsing(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "results": [
                {
                    "id": 998877,
                    "name": "Analog Synth Loop 120BPM",
                    "username": "synth_master",
                    "duration": 8.0,
                    "license": "http://creativecommons.org/licenses/by/3.0/",
                    "previews": {
                        "preview-hq-mp3": "https://cdn.freesound.org/previews/998/998877_hq.mp3",
                        "preview-lq-mp3": "https://cdn.freesound.org/previews/998/998877_lq.mp3",
                    },
                    "tags": ["synth", "analog", "loop"],
                    "samplerate": 48000,
                    "type": "wav",
                }
            ]
        }
        mock_get.return_value = mock_resp

        source = FreesoundSource(api_key="valid_token")
        results = source.search(
            query="analog", genre="synth", min_duration=2, max_duration=10
        )

        assert len(results) == 1
        track = results[0]
        assert track.id == "998877"
        assert track.title == "Analog Synth Loop 120BPM"
        assert track.artist == "synth_master"
        assert track.provider == "freesound"
        assert (
            track.stream_url == "https://cdn.freesound.org/previews/998/998877_hq.mp3"
        )
        assert track.sample_rate == 48000
        assert track.format == "wav"

    @patch("requests.Session.get")
    def test_search_error_handling(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("401 Unauthorized")
        source = FreesoundSource(api_key="bad_token")
        results = source.search(query="drums")
        assert results == []

    def test_is_available_without_key(self):
        source = FreesoundSource(api_key="")
        assert source.is_available() is False

    @patch("requests.Session.get")
    def test_is_available_with_key(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        source = FreesoundSource(api_key="valid_token")
        assert source.is_available() is True
