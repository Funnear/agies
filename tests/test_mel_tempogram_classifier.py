"""Unit tests for Mel-Spectrogram and Tempogram Classifier (arXiv:2110.08862)."""

import math
from pathlib import Path
import tempfile

from agies.audio.mel_tempogram_classifier import DeepMelTempogramClassifier
from agies.audio.tempogram import (
    MelFilterbank,
    MelTempogramExtractor,
    TempogramExtractor,
)


def test_mel_filterbank_construction_and_application():
    fb = MelFilterbank(n_mels=32, n_fft=1024, sample_rate=22050)
    assert len(fb.filters) == 32
    assert len(fb.filters[0]) == 513

    # Generate synthetic linear spectrum
    linear_mag = [1.0 if 10 <= k <= 40 else 0.05 for k in range(513)]
    mel_energies = fb.apply(linear_mag)

    assert len(mel_energies) == 32
    assert all(isinstance(v, float) for v in mel_energies)


def test_tempogram_extractor_fourier_and_autocorrelation():
    tempogram = TempogramExtractor(sample_rate=22050, hop_size=512, bpm_bins=24)
    assert len(tempogram.bpm_candidates) == 24

    # Generate synthetic onset novelty with periodic 120 BPM pulse (2 Hz)
    fps = 22050 / 512  # ~43.06 frames/sec
    duration_frames = int(fps * 6.0)
    novelty = [
        1.0 if (i % int(fps / 2.0)) == 0 else 0.02 for i in range(duration_frames)
    ]

    ft = tempogram.compute_fourier_tempogram(novelty)
    act = tempogram.compute_autocorrelation_tempogram(novelty)

    assert len(ft) > 0
    assert len(ft[0]) == 24
    assert len(act) > 0
    assert len(act[0]) == 24


def test_mel_tempogram_unified_extractor():
    extractor = MelTempogramExtractor(n_mels=32, bpm_bins=24)

    # 1 second of 440 Hz audio
    sample_rate = 22050
    samples = [
        0.8 * math.sin(2.0 * math.pi * 440.0 * (i / sample_rate))
        for i in range(sample_rate)
    ]

    res = extractor.extract_features(samples)
    assert "mel_spectrogram_summary" in res
    assert "fourier_tempogram_summary" in res
    assert "autocorr_tempogram_summary" in res
    assert "detected_tempo_bpm" in res
    assert len(res["mel_spectrogram_summary"]) == 32
    assert len(res["fourier_tempogram_summary"]) == 24


def test_deep_mel_tempogram_classifier_training_and_serialization():
    clf = DeepMelTempogramClassifier(
        fusion_strategy="late_fusion", n_mels=16, bpm_bins=12, hidden_dim=32
    )

    # Synthetic Mel (16 dims) and Tempogram (24 dims)
    X_mel = [
        [4.0 if m < 5 else 0.5 for m in range(16)],  # Techno profile (low freq)
        [4.2 if m < 5 else 0.4 for m in range(16)],
        [0.5 if m < 5 else 3.8 for m in range(16)],  # Trance profile (high freq)
        [0.6 if m < 5 else 4.0 for m in range(16)],
    ]
    X_tempo = [
        [1.0 if b == 4 else 0.1 for b in range(24)],  # ~130 BPM
        [0.95 if b == 4 else 0.1 for b in range(24)],
        [1.0 if b == 8 else 0.1 for b in range(24)],  # ~140 BPM
        [0.98 if b == 8 else 0.1 for b in range(24)],
    ]
    y = ["techno", "techno", "trance", "trance"]

    clf.fit(X_mel, X_tempo, y, epochs=30)
    assert clf.is_trained
    assert clf.classes == ["techno", "trance"]

    # Inference
    pred = clf.predict(X_mel[0], X_tempo[0])
    probs = clf.predict_proba(X_mel[0], X_tempo[0])
    assert pred == "techno"
    assert probs["techno"] > probs["trance"]

    # Test serialization
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        clf.save_model(tmp_path)
        assert tmp_path.exists()

        loaded_clf = DeepMelTempogramClassifier.load_model(tmp_path)
        assert loaded_clf.is_trained
        assert loaded_clf.classes == ["techno", "trance"]

        pred_loaded = loaded_clf.predict(X_mel[2], X_tempo[2])
        assert pred_loaded == "trance"
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
