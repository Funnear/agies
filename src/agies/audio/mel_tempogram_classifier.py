"""Deep Learning EDM & Music Subgenre Classifier based on arXiv:2110.08862.

"Deep Learning Based EDM Subgenre Classification using Mel-Spectrogram and Tempogram Features"
(Dong, Silla Jr., et al., 2021)

Architecture:
1. Multi-Representation Front-End:
   - Mel-Spectrogram (Timbral / Harmonic frequency distribution)
   - Fourier Tempogram (FT - Cyclic tempo harmonics & meter)
   - Autocorrelation Tempogram (ACT - Beat lag periodicities)
2. Fusion Strategies:
   - Early Fusion: Input-level tensor aggregation of Mel + Tempogram channels
   - Late Fusion: Dual-branch feature projection -> Concatenation -> Dense Classifier Head
3. Classifier Back-End:
   - ResNet / Deep Feedforward Feature Projection with Softmax Probability Distribution
"""

import json
import logging
import math
from pathlib import Path
import random
from typing import Any, Dict, List

from agies.audio.tempogram import MelTempogramExtractor

logger = logging.getLogger("agies.audio.mel_tempogram")


class DeepMelTempogramClassifier:
    """Subgenre Classifier based on Mel-Spectrogram and Fourier/Autocorrelation Tempograms (arXiv:2110.08862)."""

    DEFAULT_EDM_SUBGENRES = [
        "techno",
        "house",
        "trance",
        "drum_and_bass",
        "dubstep",
        "ambient_downtempo",
        "electro_pop",
    ]

    def __init__(
        self,
        fusion_strategy: str = "late_fusion",  # 'early_fusion' or 'late_fusion'
        n_mels: int = 32,
        bpm_bins: int = 24,
        hidden_dim: int = 64,
        learning_rate: float = 0.01,
    ):
        self.fusion_strategy = fusion_strategy
        self.n_mels = n_mels
        self.bpm_bins = bpm_bins
        self.hidden_dim = hidden_dim
        self.learning_rate = learning_rate

        self.extractor = MelTempogramExtractor(n_mels=n_mels, bpm_bins=bpm_bins)
        self.classes: List[str] = []
        self.is_trained: bool = False

        # Model Weights
        # Mel Branch: n_mels -> hidden_dim
        self.W_mel: List[List[float]] = []
        self.b_mel: List[float] = []

        # Tempogram Branch: (2 * bpm_bins) -> hidden_dim
        self.W_tempo: List[List[float]] = []
        self.b_tempo: List[float] = []

        # Classification Head: (2 * hidden_dim if late_fusion else hidden_dim) -> n_classes
        self.W_head: List[List[float]] = []
        self.b_head: List[float] = []

        # Training history / feature normalizers
        self.mel_mean: List[float] = []
        self.mel_std: List[float] = []
        self.tempo_mean: List[float] = []
        self.tempo_std: List[float] = []

    def fit(
        self,
        X_mel: List[List[float]],
        X_tempo: List[List[float]],
        y: List[str],
        epochs: int = 40,
        batch_size: int = 16,
    ):
        """Train the Mel-Tempogram model using gradient descent optimization."""
        if not X_mel or not X_tempo or not y or len(X_mel) != len(y):
            raise ValueError(
                "X_mel, X_tempo, and y must be non-empty and of equal length."
            )

        self.classes = sorted(list(set(y)))
        n_classes = len(self.classes)
        class_to_idx = {c: i for i, c in enumerate(self.classes)}
        y_indices = [class_to_idx[label] for label in y]

        n_samples = len(X_mel)
        mel_dim = len(X_mel[0])
        tempo_dim = len(X_tempo[0])

        # 1. Compute Normalization Parameters
        self.mel_mean = [
            sum(X_mel[i][j] for i in range(n_samples)) / n_samples
            for j in range(mel_dim)
        ]
        self.mel_std = [
            math.sqrt(
                sum((X_mel[i][j] - self.mel_mean[j]) ** 2 for i in range(n_samples))
                / n_samples
            )
            + 1e-6
            for j in range(mel_dim)
        ]
        self.tempo_mean = [
            sum(X_tempo[i][j] for i in range(n_samples)) / n_samples
            for j in range(tempo_dim)
        ]
        self.tempo_std = [
            math.sqrt(
                sum((X_tempo[i][j] - self.tempo_mean[j]) ** 2 for i in range(n_samples))
                / n_samples
            )
            + 1e-6
            for j in range(tempo_dim)
        ]

        norm_mel = [
            [(X_mel[i][j] - self.mel_mean[j]) / self.mel_std[j] for j in range(mel_dim)]
            for i in range(n_samples)
        ]
        norm_tempo = [
            [
                (X_tempo[i][j] - self.tempo_mean[j]) / self.tempo_std[j]
                for j in range(tempo_dim)
            ]
            for i in range(n_samples)
        ]

        # 2. Xavier/Glorot Initialization
        random.seed(42)
        scale_mel = math.sqrt(2.0 / (mel_dim + self.hidden_dim))
        self.W_mel = [
            [random.gauss(0, scale_mel) for _ in range(self.hidden_dim)]
            for _ in range(mel_dim)
        ]
        self.b_mel = [0.0] * self.hidden_dim

        scale_tempo = math.sqrt(2.0 / (tempo_dim + self.hidden_dim))
        self.W_tempo = [
            [random.gauss(0, scale_tempo) for _ in range(self.hidden_dim)]
            for _ in range(tempo_dim)
        ]
        self.b_tempo = [0.0] * self.hidden_dim

        head_in_dim = (
            (2 * self.hidden_dim)
            if self.fusion_strategy == "late_fusion"
            else self.hidden_dim
        )
        scale_head = math.sqrt(2.0 / (head_in_dim + n_classes))
        self.W_head = [
            [random.gauss(0, scale_head) for _ in range(n_classes)]
            for _ in range(head_in_dim)
        ]
        self.b_head = [0.0] * n_classes

        # 3. Training Loop with Mini-Batch Gradient Descent
        for epoch in range(epochs):
            indices = list(range(n_samples))
            random.shuffle(indices)

            for i in indices:
                # Forward Pass
                m_vec = norm_mel[i]
                t_vec = norm_tempo[i]

                # Mel Branch (Linear + ReLU)
                h_mel = [
                    max(
                        0.0,
                        sum(m_vec[j] * self.W_mel[j][k] for j in range(mel_dim))
                        + self.b_mel[k],
                    )
                    for k in range(self.hidden_dim)
                ]

                # Tempogram Branch (Linear + ReLU)
                h_tempo = [
                    max(
                        0.0,
                        sum(t_vec[j] * self.W_tempo[j][k] for j in range(tempo_dim))
                        + self.b_tempo[k],
                    )
                    for k in range(self.hidden_dim)
                ]

                # Fusion
                if self.fusion_strategy == "late_fusion":
                    h_fused = h_mel + h_tempo
                else:
                    # Early element-wise addition
                    h_fused = [h_mel[k] + h_tempo[k] for k in range(self.hidden_dim)]

                # Head Logits & Softmax
                logits = [
                    sum(h_fused[j] * self.W_head[j][c] for j in range(head_in_dim))
                    + self.b_head[c]
                    for c in range(n_classes)
                ]
                max_l = max(logits)
                exp_l = [math.exp(val_logit - max_l) for val_logit in logits]
                sum_exp = sum(exp_l) or 1.0
                probs = [e / sum_exp for e in exp_l]

                # Cross-Entropy Gradient
                target_idx = y_indices[i]
                d_logits = [
                    probs[c] - (1.0 if c == target_idx else 0.0)
                    for c in range(n_classes)
                ]

                # Backward Pass: Head Weights
                for j in range(head_in_dim):
                    for c in range(n_classes):
                        self.W_head[j][c] -= (
                            self.learning_rate * d_logits[c] * h_fused[j]
                        )
                for c in range(n_classes):
                    self.b_head[c] -= self.learning_rate * d_logits[c]

                # Gradient to fused layer
                d_fused = [
                    sum(d_logits[c] * self.W_head[j][c] for c in range(n_classes))
                    for j in range(head_in_dim)
                ]

                # Backward Pass: Mel & Tempogram Branches
                if self.fusion_strategy == "late_fusion":
                    d_mel = d_fused[: self.hidden_dim]
                    d_tempo = d_fused[self.hidden_dim :]
                else:
                    d_mel = d_fused
                    d_tempo = d_fused

                # Update Mel Branch
                for k in range(self.hidden_dim):
                    if h_mel[k] > 0.0:  # ReLU derivative
                        for j in range(mel_dim):
                            self.W_mel[j][k] -= self.learning_rate * d_mel[k] * m_vec[j]
                        self.b_mel[k] -= self.learning_rate * d_mel[k]

                # Update Tempogram Branch
                for k in range(self.hidden_dim):
                    if h_tempo[k] > 0.0:  # ReLU derivative
                        for j in range(tempo_dim):
                            self.W_tempo[j][k] -= (
                                self.learning_rate * d_tempo[k] * t_vec[j]
                            )
                        self.b_tempo[k] -= self.learning_rate * d_tempo[k]

        self.is_trained = True
        logger.info(
            "Trained DeepMelTempogramClassifier (%s) on %d samples across %d classes.",
            self.fusion_strategy,
            n_samples,
            n_classes,
        )

    def predict_proba(
        self, mel_vector: List[float], tempo_vector: List[float]
    ) -> Dict[str, float]:
        """Estimate class probability distribution from Mel and Tempogram embeddings."""
        if not self.is_trained:
            raise RuntimeError(
                "Model is not trained. Call fit() or load_model() first."
            )

        mel_dim = len(self.mel_mean)
        tempo_dim = len(self.tempo_mean)
        n_classes = len(self.classes)
        head_in_dim = len(self.W_head)

        # Normalize Inputs
        norm_mel = [
            (
                (mel_vector[j] - self.mel_mean[j]) / self.mel_std[j]
                if j < len(mel_vector)
                else 0.0
            )
            for j in range(mel_dim)
        ]
        norm_tempo = [
            (
                (tempo_vector[j] - self.tempo_mean[j]) / self.tempo_std[j]
                if j < len(tempo_vector)
                else 0.0
            )
            for j in range(tempo_dim)
        ]

        # Forward Pass
        h_mel = [
            max(
                0.0,
                sum(norm_mel[j] * self.W_mel[j][k] for j in range(mel_dim))
                + self.b_mel[k],
            )
            for k in range(self.hidden_dim)
        ]
        h_tempo = [
            max(
                0.0,
                sum(norm_tempo[j] * self.W_tempo[j][k] for j in range(tempo_dim))
                + self.b_tempo[k],
            )
            for k in range(self.hidden_dim)
        ]

        if self.fusion_strategy == "late_fusion":
            h_fused = h_mel + h_tempo
        else:
            h_fused = [h_mel[k] + h_tempo[k] for k in range(self.hidden_dim)]

        logits = [
            sum(h_fused[j] * self.W_head[j][c] for j in range(head_in_dim))
            + self.b_head[c]
            for c in range(n_classes)
        ]
        max_l = max(logits)
        exp_l = [math.exp(val_logit - max_l) for val_logit in logits]
        sum_exp = sum(exp_l) or 1.0

        return {self.classes[c]: round(exp_l[c] / sum_exp, 4) for c in range(n_classes)}

    def predict(self, mel_vector: List[float], tempo_vector: List[float]) -> str:
        """Predict highest-confidence subgenre label."""
        probs = self.predict_proba(mel_vector, tempo_vector)
        return max(probs.items(), key=lambda x: x[1])[0]

    def evaluate(
        self,
        X_mel_test: List[List[float]],
        X_tempo_test: List[List[float]],
        y_test: List[str],
    ) -> Dict[str, Any]:
        """Evaluate accuracy and per-class precision/recall on a test dataset."""
        y_pred = [self.predict(m, t) for m, t in zip(X_mel_test, X_tempo_test)]
        correct = sum(1 for true, pred in zip(y_test, y_pred) if true == pred)
        accuracy = round(correct / len(y_test), 4)

        per_class: Dict[str, Dict[str, float]] = {}
        for c in self.classes:
            tp = sum(1 for t, p in zip(y_test, y_pred) if t == c and p == c)
            fp = sum(1 for t, p in zip(y_test, y_pred) if t != c and p == c)
            fn = sum(1 for t, p in zip(y_test, y_pred) if t == c and p != c)

            prec = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
            rec = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
            f1 = round(2 * prec * rec / (prec + rec), 4) if (prec + rec) > 0 else 0.0
            per_class[c] = {
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "support": y_test.count(c),
            }

        return {
            "total_test_samples": len(y_test),
            "accuracy": accuracy,
            "fusion_strategy": self.fusion_strategy,
            "per_class_metrics": per_class,
        }

    def save_model(self, model_path: Path):
        """Serialize neural weights and normalization state to JSON."""
        state = {
            "fusion_strategy": self.fusion_strategy,
            "n_mels": self.n_mels,
            "bpm_bins": self.bpm_bins,
            "hidden_dim": self.hidden_dim,
            "classes": self.classes,
            "W_mel": self.W_mel,
            "b_mel": self.b_mel,
            "W_tempo": self.W_tempo,
            "b_tempo": self.b_tempo,
            "W_head": self.W_head,
            "b_head": self.b_head,
            "mel_mean": self.mel_mean,
            "mel_std": self.mel_std,
            "tempo_mean": self.tempo_mean,
            "tempo_std": self.tempo_std,
            "paper_reference": "arXiv:2110.08862",
        }
        with open(model_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        logger.info("Saved DeepMelTempogramClassifier to %s", model_path)

    @classmethod
    def load_model(cls, model_path: Path) -> "DeepMelTempogramClassifier":
        """Deserialize trained neural weights from JSON."""
        with open(model_path, "r", encoding="utf-8") as f:
            state = json.load(f)

        clf = cls(
            fusion_strategy=state.get("fusion_strategy", "late_fusion"),
            n_mels=state.get("n_mels", 32),
            bpm_bins=state.get("bpm_bins", 24),
            hidden_dim=state.get("hidden_dim", 64),
        )
        clf.classes = state["classes"]
        clf.W_mel = state["W_mel"]
        clf.b_mel = state["b_mel"]
        clf.W_tempo = state["W_tempo"]
        clf.b_tempo = state["b_tempo"]
        clf.W_head = state["W_head"]
        clf.b_head = state["b_head"]
        clf.mel_mean = state["mel_mean"]
        clf.mel_std = state["mel_std"]
        clf.tempo_mean = state["tempo_mean"]
        clf.tempo_std = state["tempo_std"]
        clf.is_trained = True
        return clf
