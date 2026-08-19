"""Unit tests for Audio Sources Library and AudioDataSource Abstraction."""

from pathlib import Path
import tempfile
from unittest.mock import patch

from agies.audio.archive import InternetArchiveDataSource
from agies.audio.datasource import (
    AudioDataSource,
    AudioSourceRegistry,
    get_audio_source,
    register_source,
)
from agies.audio.freesound import FreesoundDataSource
from agies.audio.jamendo import JamendoDataSource
from agies.audio.local import LocalAudioDataSource
from agies.audio.manager import AudioSourcesManager
from agies.audio.models import AudioFilter, AudioTrack, LicenseInfo
from agies.audio.musopen import MusopenDataSource
from agies.audio.wikimedia import WikimediaCommonsDataSource


def test_audio_models_serialization():
    lic = LicenseInfo(
        name="CC-BY 4.0",
        url="https://creativecommons.org/licenses/by/4.0/",
        is_commercial_allowed=True,
    )
    track = AudioTrack(
        id="12345",
        provider="jamendo",
        title="Midnight Groove",
        artist="DJ Synth",
        duration_seconds=180.5,
        audio_format="mp3",
        stream_url="https://example.com/stream.mp3",
        download_url="https://example.com/download.mp3",
        license=lic,
        tags=["electronic", "synthwave"],
    )

    assert track.id == "12345"
    assert track.license.is_commercial_allowed is True
    assert track.tags == ["electronic", "synthwave"]


def test_custom_source_registration():
    @register_source("custom_test_sound")
    class CustomSoundSource(AudioDataSource):
        def _fetch_tracks(self, audio_filter: AudioFilter):
            return [
                AudioTrack(
                    id="c_1",
                    provider=self.source_name,
                    title=f"Sample: {audio_filter.query}",
                    artist="Custom Artist",
                )
            ]

    source = get_audio_source("custom_test_sound")
    assert isinstance(source, CustomSoundSource)
    tracks = source.search("ambient")
    assert len(tracks) == 1
    assert tracks[0].title == "Sample: ambient"
    assert "custom_test_sound" in AudioSourceRegistry.list_available_sources()


def test_jamendo_provider_search_mock():
    provider = JamendoDataSource(client_id="test_client_id")
    mock_resp = {
        "results": [
            {
                "id": "1001",
                "name": "Summer Sunset",
                "artist_name": "Solaris",
                "duration": 210,
                "audio": "https://jamendo.com/audio/1001.mp3",
                "audiodownload": "https://jamendo.com/download/1001.mp3",
                "audiodownload_allowed": True,
                "license_ccurl": "https://creativecommons.org/licenses/by-sa/3.0/",
                "waveform": "https://jamendo.com/wave/1001.png",
                "musicinfo": {
                    "tags": {"genres": ["chillout"], "instruments": ["guitar"]}
                },
            }
        ]
    }

    with patch.object(provider, "_request_with_retry", return_value=mock_resp):
        tracks = provider.search(query="chillout", limit=5)
        assert len(tracks) == 1
        assert tracks[0].title == "Summer Sunset"
        assert tracks[0].artist == "Solaris"
        assert tracks[0].provider == "jamendo"
        assert "chillout" in tracks[0].tags


def test_freesound_provider_search_mock():
    provider = FreesoundDataSource(api_key="mock_key")
    mock_resp = {
        "results": [
            {
                "id": "555",
                "name": "Vintage Vinyl Crackle",
                "username": "sound_master",
                "duration": 12.4,
                "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                "previews": {"preview-hq-mp3": "https://freesound.org/preview/555.mp3"},
                "tags": ["vinyl", "crackle", "lofi"],
                "type": "wav",
            }
        ]
    }

    with patch.object(provider, "_request_with_retry", return_value=mock_resp):
        tracks = provider.search(query="crackle", limit=1)
        assert len(tracks) == 1
        assert tracks[0].title == "Vintage Vinyl Crackle"
        assert tracks[0].license.name == "CC0"
        assert tracks[0].stream_url == "https://freesound.org/preview/555.mp3"


def test_archive_org_provider_search_mock():
    provider = InternetArchiveDataSource()
    mock_resp = {
        "response": {
            "docs": [
                {
                    "identifier": "jazz_live_1955",
                    "title": "Live at Blue Note 1955",
                    "creator": "The Jazz Quartet",
                    "year": 1955,
                    "licenseurl": "https://creativecommons.org/publicdomain/mark/1.0/",
                }
            ]
        }
    }

    with patch.object(provider, "_request_with_retry", return_value=mock_resp):
        tracks = provider.search(query="jazz", limit=1)
        assert len(tracks) == 1
        assert tracks[0].id == "jazz_live_1955"
        assert tracks[0].artist == "The Jazz Quartet"


def test_musopen_provider_search_mock():
    provider = MusopenDataSource()
    mock_resp = {
        "results": [
            {
                "id": "99",
                "title": "Moonlight Sonata",
                "composer": {"name": "Ludwig van Beethoven"},
                "duration": 340,
                "file_url": "https://musopen.org/files/moonlight.mp3",
                "instrument": "piano",
            }
        ]
    }

    with patch.object(provider, "_request_with_retry", return_value=mock_resp):
        tracks = provider.search(query="beethoven", limit=1)
        assert len(tracks) == 1
        assert tracks[0].title == "Moonlight Sonata"
        assert tracks[0].artist == "Ludwig van Beethoven"
        assert tracks[0].provider == "musopen"


def test_wikimedia_commons_provider_search_mock():
    provider = WikimediaCommonsDataSource()
    mock_resp = {
        "query": {
            "pages": {
                "123": {
                    "title": "File:Forest_Birds.ogg",
                    "imageinfo": [
                        {
                            "url": "https://upload.wikimedia.org/Forest_Birds.ogg",
                            "extmetadata": {
                                "Artist": {"value": "Nature Enthusiast"},
                                "LicenseShortName": {"value": "CC-BY 4.0"},
                                "LicenseUrl": {
                                    "value": "https://creativecommons.org/licenses/by/4.0/"
                                },
                            },
                        }
                    ],
                }
            }
        }
    }

    with patch.object(provider, "_request_with_retry", return_value=mock_resp):
        tracks = provider.search(query="birds", limit=1)
        assert len(tracks) == 1
        assert "Forest_Birds.ogg" in tracks[0].title
        assert tracks[0].provider == "wikimedia_commons"


def test_local_audio_data_source():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        (tmp_path / "ambient_loop.wav").write_bytes(b"RIFF....WAVEfmt ....data....")
        (tmp_path / "drum_beat.mp3").write_bytes(b"ID3....")
        (tmp_path / "notes.txt").write_text("not an audio file")

        local_source = LocalAudioDataSource(root_dir=tmp_path)
        tracks = local_source.search()
        assert len(tracks) == 2
        titles = [t.title for t in tracks]
        assert "Ambient Loop" in titles
        assert "Drum Beat" in titles


def test_audio_sources_manager():
    manager = AudioSourcesManager()
    assert "jamendo" in manager.providers
    assert "freesound" in manager.providers
    assert "archive_org" in manager.providers
    assert "musopen" in manager.providers
    assert "wikimedia_commons" in manager.providers
    assert "local" in manager.providers
