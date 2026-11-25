# M3 Internal Assessment: Eigenvalues and Eigenvectors

**Student:** Varad Annadate  
**Student ID:** `E25B070724`  
**Course:** Linear Algebra and Calculus (M3)

This project explains the geometric meaning and algebraic calculation of eigenvalues and eigenvectors for a 2×2 matrix, using a Manim animation.

## Project files

- [`_Video.mp4`](_Video.mp4) — Final 1920×1080, 30 fps video, approximately 5:14 long. It contains six scenes, recorded narration, and subtle original background music. The visual timing was adjusted to match the narration.
- [`Storyboard_Eigenvalues_and_Eigenvectors.pdf`](Storyboard_Eigenvalues_and_Eigenvectors.pdf) — Six-scene storyboard.
- [`_Code/eigenvalues_scenes.py`](_Code/eigenvalues_scenes.py) — Manim source for all six scenes.
- [`_Code/math_helpers.py`](_Code/math_helpers.py) — Color palette, matrix and determinant builders, and Mathtext-to-SVG helpers.
- [`_Code/music_gen.py`](_Code/music_gen.py) — Generates the original ambient background music.
- [`_Code/render_all.py`](_Code/render_all.py) — Renders the animation scenes and creates a music-backed video.
- [`_Code/generate_storyboard.py`](_Code/generate_storyboard.py) — Generates the storyboard PDF.

The example uses the matrix

$$
A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix},
$$

with eigenvalues 3 and 2 and corresponding eigenvectors `(1, 0)` and `(-1, 1)`.

## Re-rendering the animation

With Python 3.13 and the required packages installed, run:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install manim numpy scipy matplotlib reportlab
python _Code/render_all.py
python _Code/generate_storyboard.py
```

`render_all.py` rebuilds the rendered scenes and music-backed video from source. The final narration-mixed `_Video.mp4` is included as a project deliverable.

## Credits and disclosure

- **References:** 3Blue1Brown, *Essence of Linear Algebra*, Chapter 14; Gilbert Strang, *Introduction to Linear Algebra*.
- **Music:** Original ambient instrumental synthesized with Python and NumPy.
- **AI disclosure:** Antigravity (Gemini) assisted with Manim scripting, storyboard generation, and drafting the narration script. The narration was recorded by Varad Annadate.
