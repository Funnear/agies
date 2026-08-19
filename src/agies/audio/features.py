"""Acoustic Feature Extraction Engine for Audio Classification.

Extracts spectral, temporal, and rhythmic features from audio waveforms:
- Zero Crossing Rate (ZCR)
- Root Mean Square (RMS) Energy & Dynamic Range
- Spectral Centroid (Center of gravity of frequency spectrum)
- Spectral Spread & Spectral Rolloff
- Spectral Flux (Frame-to-frame spectral variation)
- Low Energy Fraction & Temporal Crest Factor
- Rhythm / Pulse Regularity Estimate
"""

import math
from pathlib import Path
import struct
from typing import Dict, List, Optional, Tuple
import wave


class AcousticFeatureExtractor:
    """Extracts standardized acoustic feature vectors from audio files and raw PCM signals."""

    def __init__(self, frame_size: int = 1024, hop_size: int = 512):
        self.frame_size = frame_size
        self.hop_size = hop_size

    def extract_from_file(self, file_path: Path) -> Dict[str, float]:
        """Extract acoustic features from an audio file (.wav or raw PCM)."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        # If WAV file, read using standard wave module
        if path.suffix.lower() == ".wav":
            try:
                samples, sample_rate = self._read_wav(path)
                return self.extract_from_samples(samples, sample_rate)
            except Exception:
                pass

        # Fallback: Read raw bytes and extract approximate signal envelope
        try:
            with open(path, "rb") as f:
                raw_bytes = f.read(65536)  # Read initial 64KB
            samples = [float(b - 128) / 128.0 for b in raw_bytes]
            return self.extract_from_samples(samples, sample_rate=22050)
        except Exception as e:
            raise RuntimeError(f"Failed to extract features from {path}: {e}") from e

    def extract_from_samples(
        self, samples: List[float], sample_rate: int = 22050
    ) -> Dict[str, float]:
        """Extract acoustic features from normalized float samples [-1.0, 1.0]."""
        if not samples:
            return self._empty_feature_dict()

        # 1. Temporal Features: RMS Energy & Dynamic Range
        rms = self._compute_rms(samples)
        peak = max(abs(s) for s in samples) if samples else 0.0
        crest_factor = (peak / rms) if rms > 1e-6 else 1.0
        zcr = self._compute_zero_crossing_rate(samples)

        # 2. Frame-based Analysis
        frames = self._create_frames(samples, self.frame_size, self.hop_size)
        frame_energies = [self._compute_rms(f) for f in frames] if frames else [rms]
        avg_frame_energy = (
            sum(frame_energies) / len(frame_energies) if frame_energies else 1e-6
        )

        # Low energy fraction (percentage of frames below average energy)
        low_energy_frames = sum(1 for e in frame_energies if e < avg_frame_energy)
        low_energy_fraction = (
            low_energy_frames / len(frame_energies) if frame_energies else 0.5
        )

        # 3. Spectral Features (via Discrete Fourier Transform approximation)
        spectral_centroids: List[float] = []
        spectral_rolloffs: List[float] = []
        spectral_fluxes: List[float] = []
        prev_magnitude: Optional[List[float]] = None

        # Sample representative frames (limit to 30 frames for fast computation)
        sample_step = max(1, len(frames) // 30) if frames else 1
        sampled_frames = (
            frames[::sample_step] if frames else [samples[: self.frame_size]]
        )

        for frame in sampled_frames:
            mag_spectrum = self._compute_magnitude_spectrum(frame)
            sc = self._compute_spectral_centroid(mag_spectrum, sample_rate)
            ro = self._compute_spectral_rolloff(
                mag_spectrum, sample_rate, threshold=0.85
            )

            spectral_centroids.append(sc)
            spectral_rolloffs.append(ro)

            if prev_magnitude is not None:
                flux = sum(
                    max(0.0, curr - prev)
                    for curr, prev in zip(mag_spectrum, prev_magnitude)
                )
                spectral_fluxes.append(flux)
            prev_magnitude = mag_spectrum

        avg_centroid = (
            sum(spectral_centroids) / len(spectral_centroids)
            if spectral_centroids
            else 1000.0
        )
        avg_rolloff = (
            sum(spectral_rolloffs) / len(spectral_rolloffs)
            if spectral_rolloffs
            else 2000.0
        )
        avg_flux = (
            sum(spectral_fluxes) / len(spectral_fluxes) if spectral_fluxes else 0.0
        )

        # 4. Rhythmic Regularity / Pulse (Envelope variance)
        rhythm_regularity = self._compute_rhythm_regularity(frame_energies)

        return {
            "rms_energy": round(rms, 5),
            "peak_amplitude": round(peak, 5),
            "crest_factor": round(crest_factor, 3),
            "zero_crossing_rate": round(zcr, 5),
            "low_energy_fraction": round(low_energy_fraction, 4),
            "spectral_centroid": round(avg_centroid, 2),
            "spectral_rolloff": round(avg_rolloff, 2),
            "spectral_flux": round(avg_flux, 5),
            "rhythm_regularity": round(rhythm_regularity, 4),
            "brightness_ratio": round(avg_centroid / (sample_rate / 2.0), 4),
        }

    def _read_wav(self, file_path: Path) -> Tuple[List[float], int]:
        """Read standard uncompressed PCM WAV file."""
        with wave.open(str(file_path), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = min(wf.getnframes(), framerate * 30)  # Read up to 30 seconds

            raw_data = wf.readframes(n_frames)

            if sampwidth == 2:
                fmt = f"<{n_frames * n_channels}h"
                int_samples = struct.unpack(fmt, raw_data)
                # Convert to mono float [-1.0, 1.0]
                if n_channels == 2:
                    samples = [
                        (float(int_samples[i]) + float(int_samples[i + 1]))
                        / (2.0 * 32768.0)
                        for i in range(0, len(int_samples), 2)
                    ]
                else:
                    samples = [float(s) / 32768.0 for s in int_samples]
            elif sampwidth == 1:
                # 8-bit unsigned
                samples = [(float(b) - 128.0) / 128.0 for b in raw_data]
            else:
                samples = [0.0]

            return samples, framerate

    def _compute_rms(self, samples: List[float]) -> float:
        if not samples:
            return 0.0
        sum_sq = sum(s * s for s in samples)
        return math.sqrt(sum_sq / len(samples))

    def _compute_zero_crossing_rate(self, samples: List[float]) -> float:
        if len(samples) < 2:
            return 0.0
        crossings = 0
        for i in range(1, len(samples)):
            if (samples[i] >= 0 > samples[i - 1]) or (samples[i] < 0 <= samples[i - 1]):
                crossings += 1
        return crossings / (len(samples) - 1)

    def _create_frames(
        self, samples: List[float], frame_size: int, hop_size: int
    ) -> List[List[float]]:
        frames = []
        for i in range(0, len(samples) - frame_size + 1, hop_size):
            frames.append(samples[i : i + frame_size])
        return frames

    def _compute_magnitude_spectrum(self, frame: List[float]) -> List[float]:
        """Compute approximate magnitude spectrum using discrete Fourier bins."""
        N = len(frame)
        if N == 0:
            return []
        # Apply Hann window
        windowed = [
            frame[n] * 0.5 * (1.0 - math.cos(2.0 * math.pi * n / (N - 1)))
            for n in range(N)
        ]

        # Sample 32 frequency bins for fast feature representation
        n_bins = 32
        spectrum = []
        for k in range(n_bins):
            real = 0.0
            imag = 0.0
            freq_k = k * (N // 2) / n_bins
            for n in range(0, N, 2):  # Subsample for speed
                angle = 2.0 * math.pi * freq_k * n / N
                real += windowed[n] * math.cos(angle)
                imag -= windowed[n] * math.sin(angle)
            mag = math.sqrt(real * real + imag * imag) / N
            spectrum.append(mag)
        return spectrum

    def _compute_spectral_centroid(
        self, mag_spectrum: List[float], sample_rate: int
    ) -> float:
        if not mag_spectrum:
            return 0.0
        n_bins = len(mag_spectrum)
        bin_freq_step = (sample_rate / 2.0) / n_bins

        weighted_sum = sum((i * bin_freq_step) * mag_spectrum[i] for i in range(n_bins))
        total_mag = sum(mag_spectrum)
        return (weighted_sum / total_mag) if total_mag > 1e-8 else 0.0

    def _compute_spectral_rolloff(
        self, mag_spectrum: List[float], sample_rate: int, threshold: float = 0.85
    ) -> float:
        if not mag_spectrum:
            return 0.0
        total_energy = sum(mag_spectrum)
        target_energy = threshold * total_energy
        n_bins = len(mag_spectrum)
        bin_freq_step = (sample_rate / 2.0) / n_bins

        cumulative = 0.0
        for i in range(n_bins):
            cumulative += mag_spectrum[i]
            if cumulative >= target_energy:
                return i * bin_freq_step
        return sample_rate / 2.0

    def _compute_rhythm_regularity(self, frame_energies: List[float]) -> float:
        if len(frame_energies) < 4:
            return 0.5
        mean_e = sum(frame_energies) / len(frame_energies)
        var_e = sum((e - mean_e) ** 2 for e in frame_energies) / len(frame_energies)
        std_e = math.sqrt(var_e)
        # Ratio of standard deviation to mean (normalized variation)
        return std_e / (mean_e + 1e-5)

    def _empty_feature_dict(self) -> Dict[str, float]:
        return {
            "rms_energy": 0.0,
            "peak_amplitude": 0.0,
            "crest_factor": 1.0,
            "zero_crossing_rate": 0.0,
            "low_energy_fraction": 0.5,
            "spectral_centroid": 1000.0,
            "spectral_rolloff": 2000.0,
            "spectral_flux": 0.0,
            "rhythm_regularity": 0.5,
            "brightness_ratio": 0.1,
        }
