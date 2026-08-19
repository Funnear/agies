"""Unit tests for Audio Processing, Header Inspection, and Parallel Downloader."""

from pathlib import Path
import tempfile
from unittest.mock import MagicMock, patch

from agies.audio.models import AudioTrack
from agies.audio.processor import AudioInspector, ParallelAudioDownloader


def test_audio_inspector_valid_headers():
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Path(tmp_dir)
        wav_file = p / "test.wav"
        # 44-byte standard PCM WAV header
        header = bytearray(44)
        header[0:4] = b"RIFF"
        header[8:12] = b"WAVE"
        header[12:16] = b"fmt "
        header[20:22] = b"\x01\x00"  # PCM
        header[22:24] = b"\x02\x00"  # 2 channels
        header[24:28] = b"\x44\xac\x00\x00"  # 44100 Hz
        header[34:36] = b"\x10\x00"  # 16-bit
        header[36:40] = b"data"
        wav_file.write_bytes(header)

        info = AudioInspector.inspect_file(wav_file)
        assert info["is_header_valid"] is True
        assert info["detected_format"] == "wav"
        assert info["channels"] == 2
        assert info["sample_rate"] == 44100
        assert info["bits_per_sample"] == 16


def test_audio_inspector_mp3_header():
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Path(tmp_dir)
        mp3_file = p / "test.mp3"
        mp3_file.write_bytes(b"ID3\x03\x00\x00\x00\x00\x00\x00" + b"\x00" * 100)

        info = AudioInspector.inspect_file(mp3_file)
        assert info["is_header_valid"] is True
        assert info["detected_format"] == "mp3"


def test_parallel_audio_downloader():
    tracks = [
        AudioTrack(
            id="t1",
            provider="jamendo",
            title="Track One",
            stream_url="https://example.com/t1.mp3",
        ),
        AudioTrack(
            id="t2",
            provider="jamendo",
            title="Track Two",
            stream_url="https://example.com/t2.mp3",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        downloader = ParallelAudioDownloader(max_workers=2)

        with patch("requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.iter_content.return_value = [
                b"mock audio chunk 1",
                b"mock audio chunk 2",
            ]
            mock_get.return_value = mock_resp

            results = downloader.download_tracks_parallel(tracks, output_dir=tmp_dir)
            assert len(results) == 2
            assert "t1" in results
            assert "t2" in results
            assert Path(results["t1"]).exists()
            assert Path(results["t2"]).exists()
