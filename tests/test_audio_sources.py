"""Unit tests for the Audio Providers library.

Tests the BaseAudioProvider interface, models, search service, and concrete providers.
Uses mock HTTP responses to verify JSON parsing, query generation, and domain error handling.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests
from pydantic import ValidationError

from agies.audio.base_audio_provider import (
    AudioProviderAuthenticationError,
    AudioProviderConnectionError,
    AudioProviderNotRegisteredError,
    AudioProviderResponseError,
    BaseAudioProvider,
)
from agies.audio.model_audio_track_metadata import AudioTrack
from agies.audio.provider_archive_org import ProviderArchiveOrg
from agies.audio.provider_freesound import ProviderFreesound
from agies.audio.provider_jamendo import ProviderJamendo
from agies.audio.search_service import AudioSearchService

_MOCK_TEST_CLIENT_ID = "mock_test_client_id_123"
_MOCK_TEST_API_KEY = "mock_test_api_key_456"


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
        assert track.audio_file_format is None

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
            audio_file_format="mp3",
            tags=["synthwave", "retrowave"],
            source_url="https://example.com/track",
        )
        assert track.duration_seconds == 213.4
        assert track.sample_rate == 44100
        assert track.audio_file_format == "mp3"
        assert "synthwave" in track.tags

    def test_rejects_unsupported_audio_file_format(self):
        with pytest.raises(ValidationError):
            AudioTrack(
                id="42",
                title="Unsupported",
                provider="test",
                audio_file_format="m4a",
            )


# ---------------------------------------------------------------------------
# Base class tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestBaseAudioProvider:
    """Test that BaseAudioProvider cannot be instantiated directly."""

    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            BaseAudioProvider(name="abstract")  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# Search Service tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAudioSearchService:
    """Test the AudioSearchService facade."""

    def test_register_and_search(self):
        service = AudioSearchService()
        mock_provider = MagicMock(spec=BaseAudioProvider)
        mock_provider.name = "mock_provider"
        mock_provider.is_available.return_value = True
        mock_provider.search.return_value = [
            AudioTrack(id="1", title="Mock Track", provider="mock_provider")
        ]

        service.register(mock_provider)
        results = service.search(query="electronic")

        assert len(results) == 1
        assert results[0].title == "Mock Track"
        mock_provider.search.assert_called_once_with(
            query="electronic",
            genre=None,
            min_duration=None,
            max_duration=None,
            limit=10,
        )

    def test_filter_by_provider(self):
        service = AudioSearchService()
        provider_a = MagicMock(spec=BaseAudioProvider)
        provider_a.name = "provider_a"
        provider_a.is_available.return_value = True
        provider_a.search.return_value = [
            AudioTrack(id="a1", title="Track A", provider="provider_a")
        ]
        provider_b = MagicMock(spec=BaseAudioProvider)
        provider_b.name = "provider_b"
        provider_b.is_available.return_value = True
        provider_b.search.return_value = []

        service.register(provider_a)
        service.register(provider_b)

        results = service.search(query="test", provider="provider_a")
        assert len(results) == 1
        provider_a.search.assert_called_once()
        provider_b.search.assert_not_called()

    def test_register_skips_provider_with_duplicate_name(self, caplog):
        service = AudioSearchService()
        first_provider = MagicMock(spec=BaseAudioProvider)
        first_provider.name = "archive_org"
        first_provider.is_available.return_value = True
        first_provider.search.return_value = []
        replacement_provider = MagicMock(spec=BaseAudioProvider)
        replacement_provider.name = "archive_org"
        replacement_provider.is_available.return_value = True

        service.register(first_provider)
        service.register(replacement_provider)
        service.search(query="test")

        first_provider.search.assert_called_once()
        replacement_provider.search.assert_not_called()
        assert "already registered; registration skipped" in caplog.text

    def test_provider_domain_error_handled_gracefully(self):
        service = AudioSearchService()
        bad_provider = MagicMock(spec=BaseAudioProvider)
        bad_provider.name = "broken"
        bad_provider.is_available.return_value = True
        bad_provider.search.side_effect = AudioProviderConnectionError(
            "Connection timeout"
        )

        service.register(bad_provider)
        results = service.search(query="test")
        assert results == []

    def test_unexpected_programming_bug_propagates(self):
        service = AudioSearchService()
        buggy_provider = MagicMock(spec=BaseAudioProvider)
        buggy_provider.name = "buggy"
        buggy_provider.is_available.return_value = True
        buggy_provider.search.side_effect = AttributeError("Unexpected code bug")

        service.register(buggy_provider)
        with pytest.raises(AttributeError):
            service.search(query="test")

    def test_skips_unavailable_provider(self):
        service = AudioSearchService()
        unavailable_provider = MagicMock(spec=BaseAudioProvider)
        unavailable_provider.name = "unavailable"
        unavailable_provider.is_available.return_value = False

        service.register(unavailable_provider)

        assert service.search(query="test") == []
        unavailable_provider.search.assert_not_called()

    def test_raises_for_unregistered_provider(self):
        service = AudioSearchService()

        with pytest.raises(AudioProviderNotRegisteredError):
            service.search(query="test", provider="missing")


# ---------------------------------------------------------------------------
# Provider tests with mocked network responses
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProviderJamendo:
    """Test ProviderJamendo JSON parsing and error handling."""

    def test_session_is_created_lazily(self):
        provider = ProviderJamendo(client_id=_MOCK_TEST_CLIENT_ID)

        assert provider._session is None
        assert isinstance(provider.session, requests.Session)
        assert provider._session is provider.session

    def test_search_without_key_raises_auth_error(self):
        provider = ProviderJamendo(client_id="")
        with pytest.raises(AudioProviderAuthenticationError):
            provider.search(query="techno")

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

        provider = ProviderJamendo(client_id=_MOCK_TEST_CLIENT_ID)
        results = provider.search(
            query="techno", genre="electronic", min_duration=60, max_duration=300
        )

        assert len(results) == 1
        track = results[0]
        assert track.id == "12345"
        assert track.title == "Deep Resonance"
        assert track.artist == "Artist Alpha"
        assert track.provider == "jamendo"
        assert track.download_url == "https://download.jamendo.com/12345.mp3"
        assert track.audio_file_format == "mp3"
        assert "techno" in track.tags

    @patch("requests.Session.get")
    def test_search_connection_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        provider = ProviderJamendo(client_id=_MOCK_TEST_CLIENT_ID)
        with pytest.raises(AudioProviderConnectionError):
            provider.search(query="techno")

    @patch("requests.Session.get")
    def test_search_malformed_json(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_resp

        provider = ProviderJamendo(client_id=_MOCK_TEST_CLIENT_ID)
        with pytest.raises(AudioProviderResponseError):
            provider.search(query="techno")

    @patch("requests.Session.get")
    def test_is_available_true(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        provider = ProviderJamendo(client_id=_MOCK_TEST_CLIENT_ID)
        assert provider.is_available() is True

    def test_is_available_without_key(self):
        provider = ProviderJamendo(client_id="")
        assert provider.is_available() is False


@pytest.mark.unit
class TestProviderArchiveOrg:
    """Test ProviderArchiveOrg JSON parsing and error handling."""

    def test_session_is_created_lazily(self):
        provider = ProviderArchiveOrg()

        assert provider._session is None
        assert isinstance(provider.session, requests.Session)
        assert provider._session is provider.session

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

        provider = ProviderArchiveOrg()
        results = provider.search(query="classical", genre="symphony", limit=5)

        assert len(results) == 1
        track = results[0]
        assert track.id == "audio_sample_01"
        assert track.title == "Public Domain Classical"
        assert track.artist == "Symphony Orchestra"
        assert track.provider == "archive_org"
        assert (
            track.download_url is not None
            and "archive.org/download/audio_sample_01" in track.download_url
        )

    @patch("requests.Session.get")
    def test_search_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        provider = ProviderArchiveOrg()
        with pytest.raises(AudioProviderConnectionError):
            provider.search(query="test")

    @patch("requests.Session.get")
    def test_is_available_true(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        provider = ProviderArchiveOrg()
        assert provider.is_available() is True


@pytest.mark.unit
class TestProviderFreesound:
    """Test ProviderFreesound JSON parsing and error handling."""

    def test_session_is_created_lazily(self):
        provider = ProviderFreesound(api_key=_MOCK_TEST_API_KEY)

        assert provider._session is None
        assert isinstance(provider.session, requests.Session)
        assert provider._session is provider.session

    def test_search_without_key_raises_auth_error(self):
        provider = ProviderFreesound(api_key="")
        with pytest.raises(AudioProviderAuthenticationError):
            provider.search(query="drums")

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

        provider = ProviderFreesound(api_key=_MOCK_TEST_API_KEY)
        results = provider.search(
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
        assert track.audio_file_format == "wav"

    @patch("requests.Session.get")
    def test_search_auth_error(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_get.return_value = mock_resp
        provider = ProviderFreesound(api_key="invalid_key")
        with pytest.raises(AudioProviderAuthenticationError):
            provider.search(query="drums")

    def test_is_available_without_key(self):
        provider = ProviderFreesound(api_key="")
        assert provider.is_available() is False

    @patch("requests.Session.get")
    def test_is_available_with_key(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        provider = ProviderFreesound(api_key=_MOCK_TEST_API_KEY)
        assert provider.is_available() is True
