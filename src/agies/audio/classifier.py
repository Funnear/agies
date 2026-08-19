"""Machine Learning Audio Genre Classifier.

Provides multi-class acoustic classification:
- Gaussian Naive Bayes & Distance-Weighted K-Nearest Neighbors Classifier
- Feature Normalization & MinMax/Z-Score Scaling
- Confidence score probability estimation
- Model save/load persistence (JSON format)
"""

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

from agies.audio.features import AcousticFeatureExtractor

logger = logging.getLogger("agies.audio.classifier")


class AudioGenreClassifier:
    """Acoustic Machine Learning Genre Classifier."""

    FEATURE_KEYS = [
        "rms_energy",
        "peak_amplitude",
        "crest_factor",
        "zero_crossing_rate",
        "low_energy_fraction",
        "spectral_centroid",
        "spectral_rolloff",
        "spectral_flux",
        "rhythm_regularity",
        "brightness_ratio",
    ]

    def __init__(self, k_neighbors: int = 5):
        self.k_neighbors = k_neighbors
        self.extractor = AcousticFeatureExtractor()
        self.classes: List[str] = []
        self.train_X: List[List[float]] = []
        self.train_y: List[str] = []
        self.feature_means: List[float] = []
        self.feature_stds: List[float] = []
        self.class_priors: Dict[str, float] = {}
        self.class_feature_stats: Dict[str, Dict[str, Tuple[float, float]]] = {}
        self.is_trained: bool = False

    def fit(self, X: List[Dict[str, float]], y: List[str]):
        """Train the classifier on a list of feature dictionaries and genre labels."""
        if not X or not y or len(X) != len(y):
            raise ValueError("X and y must be non-empty and of equal length.")

        self.classes = sorted(list(set(y)))
        raw_vectors = [[f.get(k, 0.0) for k in self.FEATURE_KEYS] for f in X]

        # 1. Compute normalization parameters (Mean & Std)
        n_samples = len(raw_vectors)
        n_features = len(self.FEATURE_KEYS)

        self.feature_means = [
            sum(raw_vectors[i][j] for i in range(n_samples)) / n_samples
            for j in range(n_features)
        ]
        self.feature_stds = [
            math.sqrt(
                sum(
                    (raw_vectors[i][j] - self.feature_means[j]) ** 2
                    for i in range(n_samples)
                )
                / n_samples
            )
            + 1e-6
            for j in range(n_features)
        ]

        # 2. Normalize Training Data
        self.train_X = [self._normalize_vector(v) for v in raw_vectors]
        self.train_y = list(y)

        # 3. Compute Gaussian Statistics per Class (Naive Bayes prior & conditional likelihoods)
        for c in self.classes:
            c_indices = [i for i, label in enumerate(y) if label == c]
            self.class_priors[c] = len(c_indices) / n_samples
            self.class_feature_stats[c] = {}

            for j, fkey in enumerate(self.FEATURE_KEYS):
                vals = [raw_vectors[i][j] for i in c_indices]
                c_mean = sum(vals) / len(vals) if vals else 0.0
                c_var = (
                    sum((v - c_mean) ** 2 for v in vals) / len(vals) if vals else 1.0
                )
                self.class_feature_stats[c][fkey] = (c_mean, math.sqrt(c_var) + 1e-6)

        self.is_trained = True
        logger.info(
            "Trained AudioGenreClassifier on %d samples across classes: %s",
            n_samples,
            self.classes,
        )

    def predict_proba(self, features: Dict[str, float]) -> Dict[str, float]:
        """Estimate class probability distribution for an acoustic feature dictionary."""
        if not self.is_trained:
            raise RuntimeError(
                "Classifier is not trained. Call fit() or load_model() first."
            )

        # Combined scoring: Gaussian Log-Likelihood + KNN Density
        raw_vector = [features.get(k, 0.0) for k in self.FEATURE_KEYS]
        norm_vector = self._normalize_vector(raw_vector)

        # 1. KNN Distance-Weighted Voting
        distances = []
        for i, train_vec in enumerate(self.train_X):
            dist = math.sqrt(
                sum(
                    (norm_vector[j] - train_vec[j]) ** 2
                    for j in range(len(norm_vector))
                )
            )
            distances.append((dist, self.train_y[i]))

        distances.sort(key=lambda x: x[0])
        top_k = distances[: min(self.k_neighbors, len(distances))]

        knn_scores: Dict[str, float] = {c: 0.0 for c in self.classes}
        for dist, label in top_k:
            weight = 1.0 / (dist + 1e-4)
            knn_scores[label] += weight

        # 2. Gaussian Naive Bayes Log-Likelihood
        nb_scores: Dict[str, float] = {}
        for c in self.classes:
            log_prob = math.log(max(self.class_priors.get(c, 1e-5), 1e-5))
            for j, fkey in enumerate(self.FEATURE_KEYS):
                mean, std = self.class_feature_stats[c][fkey]
                val = raw_vector[j]
                # Gaussian PDF log
                exponent = -0.5 * ((val - mean) / std) ** 2
                log_prob += exponent - math.log(std)
            nb_scores[c] = log_prob

        # Softmax over combined scores
        max_nb = max(nb_scores.values())
        exp_nb = {c: math.exp(nb_scores[c] - max_nb) for c in self.classes}
        sum_exp = sum(exp_nb.values())
        norm_nb = {c: exp_nb[c] / sum_exp for c in self.classes}

        # Ensemble weights: 60% KNN + 40% Naive Bayes
        total_knn = sum(knn_scores.values()) or 1.0
        norm_knn = {c: knn_scores[c] / total_knn for c in self.classes}

        final_probs: Dict[str, float] = {}
        for c in self.classes:
            p = 0.6 * norm_knn[c] + 0.4 * norm_nb[c]
            final_probs[c] = round(p, 4)

        # Normalize to exactly 1.0
        total_p = sum(final_probs.values()) or 1.0
        return {c: round(final_probs[c] / total_p, 4) for c in self.classes}

    def predict(self, features: Dict[str, float]) -> str:
        """Predict the most likely genre for an acoustic feature dictionary."""
        probs = self.predict_proba(features)
        return max(probs.items(), key=lambda x: x[1])[0]

    def predict_file(self, file_path: Path) -> Dict[str, Any]:
        """Extract features from an audio file and predict genre with confidence."""
        features = self.extractor.extract_from_file(file_path)
        probs = self.predict_proba(features)
        predicted_genre = max(probs.items(), key=lambda x: x[1])[0]
        confidence = probs[predicted_genre]

        return {
            "file": str(file_path),
            "predicted_genre": predicted_genre,
            "confidence": confidence,
            "probabilities": probs,
            "extracted_features": features,
        }

    def evaluate(
        self, X_test: List[Dict[str, float]], y_test: List[str]
    ) -> Dict[str, Any]:
        """Evaluate accuracy and per-class precision/recall on a test dataset."""
        if not X_test:
            return {"accuracy": 0.0}

        y_pred = [self.predict(x) for x in X_test]
        correct = sum(1 for true, pred in zip(y_test, y_pred) if true == pred)
        accuracy = round(correct / len(y_test), 4)

        per_class: Dict[str, Dict[str, float]] = {}
        for c in self.classes:
            tp = sum(1 for t, p in zip(y_test, y_pred) if t == c and p == c)
            fp = sum(1 for t, p in zip(y_test, y_pred) if t != c and p == c)
            fn = sum(1 for t, p in zip(y_test, y_pred) if t == c and p != c)

            precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
            recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
            f1 = (
                round(2 * precision * recall / (precision + recall), 4)
                if (precision + recall) > 0
                else 0.0
            )

            per_class[c] = {
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "support": y_test.count(c),
            }

        return {
            "total_samples": len(y_test),
            "accuracy": accuracy,
            "per_class_metrics": per_class,
        }

    def save_model(self, model_path: Path):
        """Serialize trained classifier state to JSON."""
        state = {
            "classes": self.classes,
            "k_neighbors": self.k_neighbors,
            "feature_keys": self.FEATURE_KEYS,
            "feature_means": self.feature_means,
            "feature_stds": self.feature_stds,
            "class_priors": self.class_priors,
            "class_feature_stats": self.class_feature_stats,
            "train_X": self.train_X,
            "train_y": self.train_y,
        }
        with open(model_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        logger.info("Saved AudioGenreClassifier to %s", model_path)

    @classmethod
    def load_model(cls, model_path: Path) -> "AudioGenreClassifier":
        """Deserialize trained classifier state from JSON."""
        with open(model_path, "r", encoding="utf-8") as f:
            state = json.load(f)

        clf = cls(k_neighbors=state.get("k_neighbors", 5))
        clf.classes = state["classes"]
        clf.feature_means = state["feature_means"]
        clf.feature_stds = state["feature_stds"]
        clf.class_priors = state["class_priors"]
        clf.class_feature_stats = state["class_feature_stats"]
        clf.train_X = state["train_X"]
        clf.train_y = state["train_y"]
        clf.is_trained = True
        return clf

    def _normalize_vector(self, vector: List[float]) -> List[float]:
        return [
            (vector[j] - self.feature_means[j]) / self.feature_stds[j]
            for j in range(len(vector))
        ]
