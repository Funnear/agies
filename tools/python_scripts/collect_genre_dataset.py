"""Audio Genre Dataset Collection and Classifier Training CLI."""

import argparse
import logging
from pathlib import Path
import sys

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.audio.dataset import AudioGenreDatasetCollector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("agies.audio_genre_cli")


def main():
    parser = argparse.ArgumentParser(
        description="Collect Audio Genre Dataset & Train ML Classifier"
    )
    parser.add_argument(
        "--samples-per-genre",
        type=int,
        default=15,
        help="Number of audio samples to collect per genre",
    )
    parser.add_argument(
        "--test-split", type=float, default=0.25, help="Test split ratio for evaluation"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/audio_dataset",
        help="Output directory for audio dataset",
    )
    parser.add_argument(
        "--model-out",
        type=str,
        default="data/models/genre_classifier.json",
        help="Path to save trained classifier model",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent.parent
    dataset_dir = project_root / args.output_dir
    model_path = project_root / args.model_out

    logger.info("=== 1. Curating Multi-Genre Audio Dataset ===")
    collector = AudioGenreDatasetCollector(storage_dir=dataset_dir)
    dataset = collector.collect_dataset(samples_per_genre=args.samples_per_genre)

    logger.info("Dataset Collection Summary:")
    logger.info("  Total Samples: %d", dataset["total_samples"])
    logger.info("  Genre Distribution: %s", dataset["distribution"])
    logger.info("  Manifest: %s", dataset["manifest_path"])

    logger.info("\n=== 2. Training Machine Learning Genre Classifier ===")
    classifier, metrics = collector.train_classifier_on_dataset(
        dataset=dataset,
        test_split_ratio=args.test_split,
        model_save_path=model_path,
    )

    logger.info("Classifier Evaluation Results:")
    logger.info("  Overall Accuracy: %.2f%%", metrics["accuracy"] * 100)
    logger.info("  Per-Class Metrics:")
    for genre, g_metrics in metrics["per_class_metrics"].items():
        logger.info(
            "    %-12s -> Precision: %.2f | Recall: %.2f | F1-Score: %.2f (Support: %d)",
            genre,
            g_metrics["precision"],
            g_metrics["recall"],
            g_metrics["f1"],
            g_metrics["support"],
        )

    logger.info("  Trained Model Saved: %s", model_path)

    # 3. Demonstration inference
    logger.info("\n=== 3. Testing Real-Time Inference on Sample Query ===")
    sample_features = dataset["records"][0]["features"]
    sample_genre = dataset["records"][0]["genre"]
    pred = classifier.predict(sample_features)
    probs = classifier.predict_proba(sample_features)
    logger.info("True Label: %s | Predicted: %s", sample_genre, pred)
    logger.info("Class Probabilities: %s", probs)
    logger.info("\n=== Audio Genre Classifier Pipeline Complete! ===")


if __name__ == "__main__":
    main()
