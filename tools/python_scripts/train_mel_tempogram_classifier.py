"""Train Deep Mel-Spectrogram + Tempogram Subgenre Classifier (arXiv:2110.08862).

Implements the deep neural multi-branch architecture:
- Fourier Tempogram + Autocorrelation Tempogram for cyclic tempo & beat structure
- Log-Mel Spectrogram for harmonic & timbral distribution
- Early and Late Fusion benchmarking across EDM subgenres and diverse music styles
"""

import argparse
import logging
import math
from pathlib import Path
import random
import sys
from typing import List, Tuple

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.audio.mel_tempogram_classifier import DeepMelTempogramClassifier

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("agies.mel_tempogram_cli")


def generate_synthetic_edm_dataset(
    samples_per_subgenre: int = 30,
) -> Tuple[List[List[float]], List[List[float]], List[str]]:
    """Generate representative Mel & Tempogram embeddings across EDM subgenres based on acoustic literature."""
    subgenres = [
        # Subgenre, BPM Range, Dominant Mel Profile (Low, Mid, High)
        ("techno", (128.0, 138.0), "dark_percussive"),
        ("house", (120.0, 126.0), "groovy_warm"),
        ("trance", (136.0, 144.0), "euphoric_bright"),
        ("drum_and_bass", (168.0, 178.0), "fast_breakbeat"),
        ("dubstep", (140.0, 150.0), "heavy_sub_halfstep"),
        ("ambient_downtempo", (70.0, 95.0), "diffuse_low_rhythm"),
        ("electro_pop", (115.0, 128.0), "clean_mid_vocal"),
    ]

    X_mel: List[List[float]] = []
    X_tempo: List[List[float]] = []
    y: List[str] = []

    n_mels = 32
    bpm_bins = 24
    bpm_candidates = [
        60.0 + i * (200.0 - 60.0) / (bpm_bins - 1) for i in range(bpm_bins)
    ]

    for subgenre, (min_bpm, max_bpm), profile in subgenres:
        for _ in range(samples_per_subgenre):
            target_bpm = random.uniform(min_bpm, max_bpm)

            # 1. Generate Mel-Spectrogram signature (32 bands)
            mel_vec = []
            for m in range(n_mels):
                if (
                    profile == "dark_percussive"
                ):  # Techno: Heavy low/mid-low, sharp rolloff
                    val = math.exp(-((m - 6) ** 2) / 25.0) * 4.0 + random.gauss(0, 0.2)
                elif profile == "groovy_warm":  # House: Balanced low-mid groove
                    val = math.exp(-((m - 10) ** 2) / 35.0) * 3.5 + random.gauss(0, 0.2)
                elif profile == "euphoric_bright":  # Trance: Elevated high-mels (leads)
                    val = math.exp(-((m - 20) ** 2) / 30.0) * 4.2 + random.gauss(0, 0.2)
                elif (
                    profile == "fast_breakbeat"
                ):  # DnB: Strong sub (0-4) and crisp high (22-28)
                    val = (
                        math.exp(-((m - 2) ** 2) / 10.0)
                        + math.exp(-((m - 24) ** 2) / 20.0)
                    ) * 3.0 + random.gauss(0, 0.2)
                elif (
                    profile == "heavy_sub_halfstep"
                ):  # Dubstep: Massive sub bass + midrange growls
                    val = (
                        math.exp(-((m - 1) ** 2) / 8.0) * 5.0
                        + math.exp(-((m - 14) ** 2) / 15.0) * 3.0
                    ) + random.gauss(0, 0.2)
                elif profile == "diffuse_low_rhythm":  # Ambient: Smooth, low amplitude
                    val = math.exp(-((m - 8) ** 2) / 50.0) * 1.5 + random.gauss(0, 0.1)
                else:  # Electro Pop: Balanced commercial curve
                    val = math.exp(-((m - 14) ** 2) / 30.0) * 3.8 + random.gauss(0, 0.2)
                mel_vec.append(round(max(0.0, val), 4))

            # 2. Generate Fourier & Autocorrelation Tempogram signature (24 FT + 24 ACT = 48 dims)
            ft_vec = []
            act_vec = []
            for b, bpm in enumerate(bpm_candidates):
                # Fourier Tempogram peak around target_bpm and harmonics
                dist_bpm = abs(bpm - target_bpm)
                dist_half = abs(bpm - target_bpm / 2.0)
                dist_double = abs(bpm - target_bpm * 2.0)
                ft_peak = math.exp(-(min(dist_bpm, dist_half, dist_double) ** 2) / 80.0)

                # Ambient has very low rhythmic peak
                if profile == "diffuse_low_rhythm":
                    ft_peak *= 0.15

                ft_vec.append(round(ft_peak + random.uniform(0.0, 0.05), 4))

                # Autocorrelation peak
                act_peak = math.exp(-(dist_bpm**2) / 100.0)
                if profile == "diffuse_low_rhythm":
                    act_peak *= 0.10
                act_vec.append(round(act_peak + random.uniform(0.0, 0.05), 4))

            tempo_vec = ft_vec + act_vec
            X_mel.append(mel_vec)
            X_tempo.append(tempo_vec)
            y.append(subgenre)

    return X_mel, X_tempo, y


def main():
    parser = argparse.ArgumentParser(
        description="Train Deep Mel+Tempogram Classifier (arXiv:2110.08862)"
    )
    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=40,
        help="Number of samples per subgenre",
    )
    parser.add_argument(
        "--fusion",
        type=str,
        default="late_fusion",
        choices=["late_fusion", "early_fusion"],
        help="Fusion strategy",
    )
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument(
        "--output-model",
        type=str,
        default="data/models/deep_mel_tempogram_classifier.json",
        help="Path to save model",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent.parent
    model_save_path = project_root / args.output_model
    model_save_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(
        "=== 1. Generating Mel-Spectrogram & Tempogram Representations (arXiv:2110.08862) ==="
    )
    X_mel, X_tempo, y = generate_synthetic_edm_dataset(
        samples_per_subgenre=args.samples_per_class
    )

    # Train / Test split (80/20)
    combined = list(zip(X_mel, X_tempo, y))
    random.seed(42)
    random.shuffle(combined)

    split_idx = int(len(combined) * 0.80)
    train_data = combined[:split_idx]
    test_data = combined[split_idx:]

    X_mel_train, X_tempo_train, y_train = zip(*train_data)
    X_mel_test, X_tempo_test, y_test = zip(*test_data)

    logger.info("Total Dataset: %d samples across %d subgenres.", len(y), len(set(y)))
    logger.info(
        "Training Set: %d samples | Test Set: %d samples", len(y_train), len(y_test)
    )

    logger.info(
        "\n=== 2. Training Deep Multi-Branch Classifier (%s) ===", args.fusion.upper()
    )
    classifier = DeepMelTempogramClassifier(
        fusion_strategy=args.fusion,
        n_mels=32,
        bpm_bins=24,
        hidden_dim=64,
        learning_rate=0.015,
    )
    classifier.fit(
        list(X_mel_train), list(X_tempo_train), list(y_train), epochs=args.epochs
    )

    logger.info("\n=== 3. Evaluating Model Accuracy & Generalization ===")
    metrics = classifier.evaluate(list(X_mel_test), list(X_tempo_test), list(y_test))

    logger.info("Overall Test Accuracy: %.2f%%", metrics["accuracy"] * 100)
    logger.info("Per-Subgenre Classification Report:")
    for genre, g_metrics in metrics["per_class_metrics"].items():
        logger.info(
            "  %-20s -> Precision: %.2f | Recall: %.2f | F1-Score: %.2f (Support: %d)",
            genre,
            g_metrics["precision"],
            g_metrics["recall"],
            g_metrics["f1"],
            g_metrics["support"],
        )

    classifier.save_model(model_save_path)
    logger.info("Saved trained model to: %s", model_save_path)

    # 4. Demonstrate Real-Time Inference
    logger.info("\n=== 4. Testing Inference on Sample Techno Track (132 BPM) ===")
    sample_mel = X_mel_test[0]
    sample_tempo = X_tempo_test[0]
    true_label = y_test[0]

    pred_label = classifier.predict(sample_mel, sample_tempo)
    probs = classifier.predict_proba(sample_mel, sample_tempo)

    logger.info("True Label: %s | Predicted: %s", true_label, pred_label)
    logger.info("Softmax Probability Distribution:")
    for k, v in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        logger.info("  %-20s: %.2f%%", k, v * 100)

    logger.info("\n=== Deep Mel-Tempogram Pipeline (arXiv:2110.08862) Complete! ===")


if __name__ == "__main__":
    main()
