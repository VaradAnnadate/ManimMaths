"""Synthesize a subtle, warm 3Blue1Brown-style ambient background track.

Generates a stereo WAV file using pure NumPy/SciPy (gentle warm pad + soft
arpeggiated sine/triangle bell notes in D major / B minor) at low volume so
spoken voice-over narration remains 100% clear.
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np


def _adsr(n_samples: int, sr: int, attack: float = 0.08, release: float = 0.8) -> np.ndarray:
    env = np.ones(n_samples, dtype=np.float64)
    a_n = min(int(attack * sr), n_samples // 2)
    r_n = min(int(release * sr), n_samples // 2)
    if a_n > 0:
        env[:a_n] = np.linspace(0.0, 1.0, a_n) ** 1.5
    if r_n > 0:
        env[-r_n:] = np.linspace(1.0, 0.0, r_n) ** 1.5
    return env


def generate_ambient_track(out_path: Path, duration_sec: float = 310.0, sr: int = 44100) -> Path:
    """Create a calm, subtle ambient instrumental WAV file."""
    n_total = int(duration_sec * sr)
    t = np.arange(n_total, dtype=np.float64) / sr

    left = np.zeros(n_total, dtype=np.float64)
    right = np.zeros(n_total, dtype=np.float64)

    # Ultra-subtle warm chord progression in D major / B minor (6 sec per chord = 24s cycle)
    chords = [
        [146.83, 220.00, 277.18],  # D3, A3, C#4
        [123.47, 185.00, 220.00],  # B2, F#3, A3
        [98.00, 196.00, 246.94],   # G2, G3, B3
        [110.00, 220.00, 277.18],  # A2, A3, C#4
    ]
    chord_dur = 6.0
    cycle_dur = chord_dur * len(chords)

    # 1. Very soft, slow-breathing sine pad
    cur = 0.0
    idx = 0
    while cur < duration_sec:
        freqs = chords[idx % len(chords)]
        start_i = int(cur * sr)
        end_i = min(n_total, int((cur + chord_dur + 1.2) * sr))
        seg_len = end_i - start_i
        if seg_len <= 0:
            break
        seg_t = np.arange(seg_len, dtype=np.float64) / sr
        env = _adsr(seg_len, sr, attack=1.8, release=2.0)

        pad_l = np.zeros(seg_len, dtype=np.float64)
        pad_r = np.zeros(seg_len, dtype=np.float64)
        for j, f in enumerate(freqs):
            detune = 1.0 + (0.0012 if j % 2 == 0 else -0.0012)
            wave_l = np.sin(2 * np.pi * f * seg_t) + 0.05 * np.sin(2 * np.pi * 2 * f * seg_t)
            wave_r = np.sin(2 * np.pi * f * detune * seg_t) + 0.05 * np.sin(2 * np.pi * 2 * f * detune * seg_t)
            pan = 0.35 + 0.3 * (j / max(1, len(freqs) - 1))
            pad_l += (1.0 - pan) * wave_l
            pad_r += pan * wave_r

        left[start_i:end_i] += 0.085 * env * pad_l
        right[start_i:end_i] += 0.085 * env * pad_r

        cur += chord_dur
        idx += 1

    # 2. Sparse, delicate felt-like sine notes (every 2.5 sec)
    note_dur = 2.4
    step = 2.5
    cur = 1.0
    step_idx = 0
    while cur < duration_sec - 1.5:
        chord_idx = int((cur % cycle_dur) // chord_dur)
        freqs = chords[chord_idx]
        f = freqs[(step_idx * 2) % len(freqs)] * 2.0
        start_i = int(cur * sr)
        end_i = min(n_total, int((cur + note_dur) * sr))
        seg_len = end_i - start_i
        if seg_len <= 0:
            break
        seg_t = np.arange(seg_len, dtype=np.float64) / sr
        env = np.exp(-1.6 * seg_t) * _adsr(seg_len, sr, attack=0.06, release=0.4)
        bell = np.sin(2 * np.pi * f * seg_t)
        pan = 0.42 + 0.16 * np.sin(step_idx * 0.6)
        left[start_i:end_i] += 0.025 * (1.0 - pan) * env * bell
        right[start_i:end_i] += 0.025 * pan * env * bell
        cur += step
        step_idx += 1

    # Global fade-in (2.5s) and fade-out (4.5s)
    fade_in = int(2.5 * sr)
    fade_out = int(4.5 * sr)
    left[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    right[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    left[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
    right[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)

    # Normalize gently 10% lower than before (0.08 -> 0.072) so voice-over sits cleanly on top
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-9)
    target_peak = 0.072
    left = np.clip(left * (target_peak / peak), -1.0, 1.0)
    right = np.clip(right * (target_peak / peak), -1.0, 1.0)

    stereo = np.stack([left, right], axis=1)
    pcm = (stereo * 32767.0).astype(np.int16)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())

    return out_path


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "background_music.wav"
    generate_ambient_track(out, duration_sec=315.0)
    print(f"Generated {out}")
