"""Mel-Spectrogram and Tempogram Feature Extraction Engine.

Implements the feature representations from arXiv:2110.08862:
1. Mel-Spectrogram (Log-Mel Filterbank across time-frequency bins)
2. Onset Strength Novelty Curve (Spectral Flux derivative)
3. Fourier Tempogram (FT - Cyclic tempo periodicity via localized STFT)
4. Autocorrelation Tempogram (ACT - Pulse lag periodicity via localized autocorrelation)
"""

import math
from typing import Any, Dict, List, Optional


class MelFilterbank:
    """Constructs Mel-scale triangular filterbanks and log-mel energy representations."""

    def __init__(
        self,
        n_mels: int = 40,
        n_fft: int = 1024,
        sample_rate: int = 22050,
        f_min: float = 20.0,
        f_max: Optional[float] = None,
    ):
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.sample_rate = sample_rate
        self.f_min = f_min
        self.f_max = f_max or (sample_rate / 2.0)
        self.filters = self._build_filterbank()

    def _hz_to_mel(self, hz: float) -> float:
        return 2595.0 * math.log10(1.0 + hz / 700.0)

    def _mel_to_hz(self, mel: float) -> float:
        return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)

    def _build_filterbank(self) -> List[List[float]]:
        min_mel = self._hz_to_mel(self.f_min)
        max_mel = self._hz_to_mel(self.f_max)
        mel_points = [
            min_mel + i * (max_mel - min_mel) / (self.n_mels + 1)
            for i in range(self.n_mels + 2)
        ]
        hz_points = [self._mel_to_hz(m) for m in mel_points]
        bin_points = [int((self.n_fft + 1) * hz / self.sample_rate) for hz in hz_points]

        n_bins = self.n_fft // 2 + 1
        filterbank: List[List[float]] = []

        for m in range(1, self.n_mels + 1):
            f_m_minus = bin_points[m - 1]
            f_m = bin_points[m]
            f_m_plus = bin_points[m + 1]

            row = [0.0] * n_bins
            for k in range(f_m_minus, f_m):
                if f_m != f_m_minus:
                    row[min(k, n_bins - 1)] = (k - f_m_minus) / (f_m - f_m_minus)
            for k in range(f_m, f_m_plus):
                if f_m_plus != f_m:
                    row[min(k, n_bins - 1)] = (f_m_plus - k) / (f_m_plus - f_m)
            filterbank.append(row)

        return filterbank

    def apply(self, linear_spectrum: List[float]) -> List[float]:
        """Convert a linear magnitude spectrum into log-mel energy bands."""
        mel_energies: List[float] = []
        n_bins = len(linear_spectrum)

        for m_filter in self.filters:
            energy = 0.0
            for k in range(min(len(m_filter), n_bins)):
                energy += m_filter[k] * linear_spectrum[k]
            # Log-energy compression (dB scale)
            log_energy = math.log(max(energy, 1e-6))
            mel_energies.append(log_energy)

        return mel_energies


class TempogramExtractor:
    """Extracts Fourier Tempograms (FT) and Autocorrelation Tempograms (ACT)."""

    def __init__(
        self,
        sample_rate: int = 22050,
        hop_size: int = 512,
        win_length_sec: float = 4.0,
        min_bpm: float = 60.0,
        max_bpm: float = 200.0,
        bpm_bins: int = 32,
    ):
        self.sample_rate = sample_rate
        self.hop_size = hop_size
        self.frame_rate = sample_rate / hop_size
        self.win_length_frames = int(win_length_sec * self.frame_rate)
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.bpm_bins = bpm_bins
        self.bpm_candidates = [
            min_bpm + i * (max_bpm - min_bpm) / (bpm_bins - 1) for i in range(bpm_bins)
        ]

    def compute_onset_novelty(self, frames: List[List[float]]) -> List[float]:
        """Compute spectral-flux based onset novelty curve."""
        novelty: List[float] = []
        prev_mag: Optional[List[float]] = None

        for frame in frames:
            # Simple FFT magnitude
            N = len(frame)
            mag = []
            for k in range(16):
                real, imag = 0.0, 0.0
                freq = k * (N // 2) / 16
                for n in range(0, N, 4):  # Subsampled discrete transform
                    ang = 2.0 * math.pi * freq * n / N
                    real += frame[n] * math.cos(ang)
                    imag -= frame[n] * math.sin(ang)
                mag.append(math.sqrt(real * real + imag * imag))

            if prev_mag is not None:
                flux = sum(max(0.0, curr - prev) for curr, prev in zip(mag, prev_mag))
                novelty.append(flux)
            else:
                novelty.append(0.0)
            prev_mag = mag

        return novelty

    def compute_fourier_tempogram(
        self, onset_envelope: List[float]
    ) -> List[List[float]]:
        """Fourier Tempogram (FT): Localized STFT over the onset novelty curve."""
        ft_matrix: List[List[float]] = []
        L = len(onset_envelope)
        if L < 4:
            return [[0.0] * self.bpm_bins]

        # Step through onset envelope
        step = max(1, L // 20)
        for center in range(0, L, step):
            start = max(0, center - self.win_length_frames // 2)
            end = min(L, center + self.win_length_frames // 2)
            window_slice = onset_envelope[start:end]
            N = len(window_slice)
            if N == 0:
                continue

            tempo_row: List[float] = []
            for bpm in self.bpm_candidates:
                freq_hz = bpm / 60.0  # Beats per second
                omega = 2.0 * math.pi * (freq_hz / self.frame_rate)
                real = sum(window_slice[n] * math.cos(omega * n) for n in range(N))
                imag = sum(window_slice[n] * math.sin(omega * n) for n in range(N))
                mag = math.sqrt(real * real + imag * imag) / (N + 1e-6)
                tempo_row.append(mag)

            # Normalize row
            max_val = max(tempo_row) or 1.0
            ft_matrix.append([round(v / max_val, 4) for v in tempo_row])

        return ft_matrix or [[0.0] * self.bpm_bins]

    def compute_autocorrelation_tempogram(
        self, onset_envelope: List[float]
    ) -> List[List[float]]:
        """Autocorrelation Tempogram (ACT): Localized lag autocorrelation."""
        act_matrix: List[List[float]] = []
        L = len(onset_envelope)
        if L < 4:
            return [[0.0] * self.bpm_bins]

        step = max(1, L // 20)
        for center in range(0, L, step):
            start = max(0, center - self.win_length_frames // 2)
            end = min(L, center + self.win_length_frames // 2)
            window_slice = onset_envelope[start:end]
            N = len(window_slice)
            if N == 0:
                continue

            mean_val = sum(window_slice) / N
            var_val = sum((v - mean_val) ** 2 for v in window_slice) or 1.0

            tempo_row: List[float] = []
            for bpm in self.bpm_candidates:
                # Lag in frames corresponding to this BPM period
                period_sec = 60.0 / bpm
                lag_frames = int(period_sec * self.frame_rate)
                if lag_frames >= N:
                    tempo_row.append(0.0)
                    continue

                autocorr = (
                    sum(
                        (window_slice[n] - mean_val)
                        * (window_slice[n + lag_frames] - mean_val)
                        for n in range(N - lag_frames)
                    )
                    / var_val
                )
                tempo_row.append(max(0.0, autocorr))

            max_val = max(tempo_row) or 1.0
            act_matrix.append([round(v / max_val, 4) for v in tempo_row])

        return act_matrix or [[0.0] * self.bpm_bins]


class MelTempogramExtractor:
    """Unified Extractor combining Log-Mel Spectrogram, Fourier Tempogram (FT), and Autocorrelation Tempogram (ACT)."""

    def __init__(
        self,
        n_mels: int = 32,
        bpm_bins: int = 24,
        frame_size: int = 1024,
        hop_size: int = 512,
        sample_rate: int = 22050,
    ):
        self.mel_fb = MelFilterbank(
            n_mels=n_mels, n_fft=frame_size, sample_rate=sample_rate
        )
        self.tempogram = TempogramExtractor(
            sample_rate=sample_rate, hop_size=hop_size, bpm_bins=bpm_bins
        )
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.sample_rate = sample_rate

    def extract_features(self, samples: List[float]) -> Dict[str, Any]:
        """Extract multi-representation features (Mel-Spectrogram, FT, ACT) from raw audio samples."""
        if not samples:
            return {
                "mel_spectrogram_summary": [0.0] * self.mel_fb.n_mels,
                "fourier_tempogram_summary": [0.0] * self.tempogram.bpm_bins,
                "autocorr_tempogram_summary": [0.0] * self.tempogram.bpm_bins,
                "detected_tempo_bpm": 120.0,
            }

        # 1. Slice Frames
        frames = [
            samples[i : i + self.frame_size]
            for i in range(0, len(samples) - self.frame_size + 1, self.hop_size)
        ] or [samples[: self.frame_size]]

        # 2. Extract Mel-Spectrogram
        mel_frames: List[List[float]] = []
        for frame in frames[:: max(1, len(frames) // 25)]:
            # Magnitude spectrum
            N = len(frame)
            mag = []
            for k in range(self.frame_size // 2 + 1):
                real, imag = 0.0, 0.0
                freq = k
                for n in range(0, min(N, 128), 4):
                    ang = 2.0 * math.pi * freq * n / N
                    real += frame[n] * math.cos(ang)
                    imag -= frame[n] * math.sin(ang)
                mag.append(math.sqrt(real * real + imag * imag))
            mel_energies = self.mel_fb.apply(mag)
            mel_frames.append(mel_energies)

        # 3. Compute Onset Novelty & Tempograms
        onset_novelty = self.tempogram.compute_onset_novelty(frames)
        ft_matrix = self.tempogram.compute_fourier_tempogram(onset_novelty)
        act_matrix = self.tempogram.compute_autocorrelation_tempogram(onset_novelty)

        # Summary averages for compact vector embedding
        n_mel_bands = self.mel_fb.n_mels
        mel_summary = (
            [
                round(
                    sum(mel_frames[i][m] for i in range(len(mel_frames)))
                    / max(1, len(mel_frames)),
                    4,
                )
                for m in range(n_mel_bands)
            ]
            if mel_frames
            else [0.0] * n_mel_bands
        )

        n_bpm_bins = self.tempogram.bpm_bins
        ft_summary = [
            round(
                sum(ft_matrix[i][b] for i in range(len(ft_matrix)))
                / max(1, len(ft_matrix)),
                4,
            )
            for b in range(n_bpm_bins)
        ]
        act_summary = [
            round(
                sum(act_matrix[i][b] for i in range(len(act_matrix)))
                / max(1, len(act_matrix)),
                4,
            )
            for b in range(n_bpm_bins)
        ]

        # Detect peak tempo from combined tempogram
        combined_tempo_curve = [
            ft_summary[b] + act_summary[b] for b in range(n_bpm_bins)
        ]
        peak_idx = max(range(n_bpm_bins), key=lambda b: combined_tempo_curve[b])
        detected_tempo = round(self.tempogram.bpm_candidates[peak_idx], 1)

        return {
            "mel_spectrogram_summary": mel_summary,
            "fourier_tempogram_summary": ft_summary,
            "autocorr_tempogram_summary": act_summary,
            "detected_tempo_bpm": detected_tempo,
            "mel_bands_count": n_mel_bands,
            "tempogram_bins_count": n_bpm_bins,
        }
