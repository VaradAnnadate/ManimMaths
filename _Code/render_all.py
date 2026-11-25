"""Render all 6 Manim scenes at 1080p, synthesize subtle music, and build _Video.mp4."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from music_gen import generate_ambient_track

ROOT = Path(__file__).resolve().parent.parent
CODE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = CODE_DIR / "media"
SCENES_FILE = CODE_DIR / "eigenvalues_scenes.py"

SCENES = [
    "Scene1_Hook",
    "Scene2_ConceptIntro",
    "Scene3_VisualIntuition",
    "Scene4_WorkedExample",
    "Scene5_Interpretation",
    "Scene6_SummaryCredits",
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> None:
    manim_bin = Path(sys.executable).parent / "manim"

    # 1. Render each scene at 1080p 30fps (-qh is 1080p60; -r 1920,1080 --fps 30 is crisp & fast)
    rendered_clips: list[Path] = []
    for scene in SCENES:
        run([
            str(manim_bin),
            "render",
            "-r", "1920,1080",
            "--fps", "30",
            "--media_dir", str(MEDIA_DIR),
            str(SCENES_FILE),
            scene,
        ])
        clip = MEDIA_DIR / "videos" / "eigenvalues_scenes" / "1080p30" / f"{scene}.mp4"
        if not clip.exists():
            raise FileNotFoundError(f"Expected rendered clip not found: {clip}")
        rendered_clips.append(clip)

    # 2. Concatenate clips with ffmpeg concat demuxer
    concat_list = CODE_DIR / "concat_list.txt"
    concat_list.write_text(
        "\n".join(f"file '{clip.as_posix()}'" for clip in rendered_clips) + "\n",
        encoding="utf-8",
    )
    silent_video = CODE_DIR / "_Video_silent.mp4"
    run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(silent_video),
    ])

    # 3. Probe exact video duration so ambient track matches cleanly
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(silent_video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    duration_sec = float(probe.stdout.strip())
    print(f"Total video duration: {duration_sec:.2f} seconds ({duration_sec / 60:.2f} min)")

    # 4. Generate subtle background music & mux into _Video.mp4
    music_wav = CODE_DIR / "background_music.wav"
    generate_ambient_track(music_wav, duration_sec=duration_sec + 1.0)

    final_video = ROOT / "_Video.mp4"
    run([
        "ffmpeg", "-y",
        "-i", str(silent_video),
        "-i", str(music_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_video),
    ])
    print(f"Done! Final video saved to {final_video}")


if __name__ == "__main__":
    main()
