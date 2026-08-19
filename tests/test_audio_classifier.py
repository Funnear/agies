"""Unit tests for Audio Feature Extraction and Genre Classifier."""

from pathlib import Path
import tempfile

from agies.audio.classifier import AudioGenreClassifier
from agies.audio.dataset import AudioGenreDatasetCollector
from agies.audio.features import AcousticFeatureExtractor


def test_acoustic_feature_extractor_synthetic_signal():
    extractor = AcousticFeatureExtractor()

    # Generate synthetic sine wave (440Hz A4)
    sample_rate = 22050
    duration_secs = 1.0
    import math

    freq = 440.0
    n_samples = int(sample_rate * duration_secs)
    samples = [
        0.8 * math.sin(2.0 * math.pi * freq * (i / sample_rate))
        for i in range(n_samples)
    ]

    features = extractor.extract_from_samples(samples, sample_rate=sample_rate)

    assert "rms_energy" in features
    assert "zero_crossing_rate" in features
    assert "spectral_centroid" in features
    assert "brightness_ratio" in features
    assert features["rms_energy"] > 0.4
    assert 0.03 <= features["zero_crossing_rate"] <= 0.05


def test_audio_genre_classifier_training_and_inference():
    clf = AudioGenreClassifier(k_neighbors=3)

    # Synthetic training data
    train_X = [
        {
            "rms_energy": 0.05,
            "spectral_centroid": 900.0,
            "brightness_ratio": 0.08,
            "zero_crossing_rate": 0.03,
        },
        {
            "rms_energy": 0.06,
            "spectral_centroid": 1100.0,
            "brightness_ratio": 0.09,
            "zero_crossing_rate": 0.04,
        },
        {
            "rms_energy": 0.28,
            "spectral_centroid": 3500.0,
            "brightness_ratio": 0.30,
            "zero_crossing_rate": 0.12,
        },
        {
            "rms_energy": 0.32,
            "spectral_centroid": 4000.0,
            "brightness_ratio": 0.35,
            "zero_crossing_rate": 0.15,
        },
    ]
    train_y = ["classical", "classical", "electronic", "electronic"]

    clf.fit(train_X, train_y)
    assert clf.is_trained
    assert set(clf.classes) == {"classical", "electronic"}

    # Test prediction
    classical_query = {
        "rms_energy": 0.04,
        "spectral_centroid": 950.0,
        "brightness_ratio": 0.07,
        "zero_crossing_rate": 0.03,
    }
    pred = clf.predict(classical_query)
    probs = clf.predict_proba(classical_query)

    assert pred == "classical"
    assert probs["classical"] > probs["electronic"]

    electronic_query = {
        "rms_energy": 0.30,
        "spectral_centroid": 3800.0,
        "brightness_ratio": 0.32,
        "zero_crossing_rate": 0.14,
    }
    pred_elec = clf.predict(electronic_query)
    assert pred_elec == "electronic"


def test_classifier_save_and_load():
    clf = AudioGenreClassifier(k_neighbors=2)
    train_X = [
        {"rms_energy": 0.05, "spectral_centroid": 900.0, "zero_crossing_rate": 0.02},
        {"rms_energy": 0.25, "spectral_centroid": 3200.0, "zero_crossing_rate": 0.11},
    ]
    train_y = ["classical", "rock"]
    clf.fit(train_X, train_y)

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        clf.save_model(tmp_path)
        assert tmp_path.exists()

        loaded_clf = AudioGenreClassifier.load_model(tmp_path)
        assert loaded_clf.is_trained
        assert loaded_clf.classes == ["classical", "rock"]

        res = loaded_clf.predict(
            {"rms_energy": 0.04, "spectral_centroid": 850.0, "zero_crossing_rate": 0.02}
        )
        assert res == "classical"
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_dataset_collector_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = AudioGenreDatasetCollector(storage_dir=Path(tmpdir))
        dataset = collector.collect_dataset(
            genres=["classical", "electronic", "ambient"], samples_per_genre=8
        )

        assert dataset["total_samples"] == 24
        assert len(dataset["records"]) == 24
        assert set(dataset["genres"]) == {"classical", "electronic", "ambient"}

        # Train and evaluate
        clf, metrics = collector.train_classifier_on_dataset(
            dataset=dataset, test_split_ratio=0.25
        )
        assert clf.is_trained
        assert metrics["accuracy"] >= 0.5
        assert "per_class_metrics" in metrics
