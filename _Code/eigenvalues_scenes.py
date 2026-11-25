"""Manim Community scenes for:
Eigenvalues and Eigenvectors — Geometric Intuition & Algebraic Meaning.

Student: Varad Annadate (E25B070724)
Course: Linear Algebra and Calculus (M3) • Internal Assessment
Style: 3Blue1Brown-inspired dark navy aesthetic with crisp Computer Modern math.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    DOWN,
    DR,
    FadeIn,
    FadeOut,
    GOLD_C,
    GREEN_C,
    GREY_B,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    UL,
    UP,
    UR,
    Arrow,
    Create,
    DashedLine,
    Dot,
    GrowArrow,
    Indicate,
    Line,
    NumberPlane,
    Polygon,
    ReplacementTransform,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    UL,
    VGroup,
    Write,
    config,
)

from math_helpers import (
    ACCENT_BLUE,
    ACCENT_CORAL,
    ACCENT_GOLD,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    AXIS_COLOR,
    BG_COLOR,
    GRID_COLOR,
    MUTED_TEXT,
    PRIMARY_TEXT,
    make_badge,
    make_det,
    make_info_card,
    make_matrix,
    math_svg,
)

config.background_color = BG_COLOR

A_MAT = np.array([[3.0, 1.0], [0.0, 2.0]])


def _vec_arrow(coords: tuple[float, float], color: str, stroke_width: float = 4.5) -> Arrow:
    return Arrow(
        ORIGIN,
        [coords[0], coords[1], 0.0],
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.16,
    )


def _span_line(direction: tuple[float, float], color: str, length: float = 12.0) -> DashedLine:
    dx, dy = direction
    norm = np.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm
    p1 = [-ux * length / 2, -uy * length / 2, 0.0]
    p2 = [ux * length / 2, uy * length / 2, 0.0]
    return DashedLine(p1, p2, color=color, stroke_width=2.0, stroke_opacity=0.55, dash_length=0.18)


def _base_plane() -> NumberPlane:
    return NumberPlane(
        x_range=[-8, 8, 1],
        y_range=[-5, 5, 1],
        background_line_style={
            "stroke_color": GRID_COLOR,
            "stroke_width": 1.3,
            "stroke_opacity": 0.8,
        },
        axis_config={
            "stroke_color": AXIS_COLOR,
            "stroke_width": 2.0,
        },
    )


# ---------------------------------------------------------------------------
# SCENE 1: OPENING FRAME + HOOK / CONTEXT (~45s)
# ---------------------------------------------------------------------------
class Scene1_Hook(Scene):
    def construct(self) -> None:
        # --- Opening Frame (Title, Concept, Student Name & ID) ---
        course = Text(
            "LINEAR ALGEBRA AND CALCULUS (M3)  •  INTERNAL ASSESSMENT",
            font="Helvetica Neue",
            font_size=18,
            color=ACCENT_BLUE,
            weight="BOLD",
        )
        title = Text(
            "Eigenvalues & Eigenvectors",
            font="Helvetica Neue",
            font_size=52,
            color=PRIMARY_TEXT,
            weight="BOLD",
        )
        subtitle = Text(
            "The Unchanging Directions Inside a Linear Transformation",
            font="Helvetica Neue",
            font_size=24,
            color=ACCENT_GOLD,
        )
        divider = Line(LEFT * 3.5, RIGHT * 3.5, color=ACCENT_BLUE, stroke_width=2.0)
        student = Text(
            "Varad Annadate   |   Student ID: E25B070724",
            font="Helvetica Neue",
            font_size=22,
            color=MUTED_TEXT,
        )

        opening = VGroup(course, title, subtitle, divider, student).arrange(DOWN, buff=0.35)
        opening.center()

        self.play(FadeIn(course, shift=UP * 0.2), run_time=0.8)
        self.play(Write(title), run_time=1.4)
        self.play(FadeIn(subtitle, shift=UP * 0.15), Create(divider), run_time=1.0)
        self.play(FadeIn(student), run_time=0.8)
        self.wait(4.0)
        self.play(FadeOut(opening), run_time=0.9)

        # --- Hook: Grid & Rotating vs Invariant Vectors ---
        badge = make_badge("1. HOOK & CONTEXT", ACCENT_BLUE).to_corner(UL, buff=0.35)
        plane = _base_plane()
        self.play(Create(plane), FadeIn(badge), run_time=1.4)

        # Sample vectors: some rotate off their span, two stay on their span!
        u_coords = (1.0, 1.0)      # goes to (4, 2) -> rotates
        w_coords = (0.0, 1.0)      # goes to (1, 2) -> rotates
        v1_coords = (1.0, 0.0)     # eigenvector -> (3, 0)
        v2_coords = (-1.0, 1.0)    # eigenvector -> (-2, 2)

        span_u = _span_line(u_coords, ACCENT_CORAL)
        span_w = _span_line(w_coords, ACCENT_PURPLE)
        span_v1 = _span_line(v1_coords, ACCENT_GREEN)
        span_v2 = _span_line(v2_coords, ACCENT_GOLD)

        vec_u = _vec_arrow(u_coords, ACCENT_CORAL)
        vec_w = _vec_arrow(w_coords, ACCENT_PURPLE)
        vec_v1 = _vec_arrow(v1_coords, ACCENT_GREEN)
        vec_v2 = _vec_arrow(v2_coords, ACCENT_GOLD)

        self.play(
            Create(span_u), Create(span_w), Create(span_v1), Create(span_v2),
            GrowArrow(vec_u), GrowArrow(vec_w), GrowArrow(vec_v1), GrowArrow(vec_v2),
            run_time=1.6,
        )
        self.wait(3.0)

        hook_label = make_info_card(
            "Apply a 2D Linear Transformation",
            [
                "Watch every vector as space stretches and shears.",
                "Most vectors get knocked off their span lines...",
            ],
            accent=ACCENT_BLUE,
            width=5.6,
        ).to_corner(UR, buff=0.35)
        self.play(FadeIn(hook_label), run_time=0.9)
        self.wait(2.5)

        # Animate transformation A
        new_u = tuple((A_MAT @ np.array(u_coords)).tolist())
        new_w = tuple((A_MAT @ np.array(w_coords)).tolist())
        new_v1 = tuple((A_MAT @ np.array(v1_coords)).tolist())
        new_v2 = tuple((A_MAT @ np.array(v2_coords)).tolist())

        self.play(
            plane.animate.apply_matrix(A_MAT),
            Transform(vec_u, _vec_arrow(new_u, ACCENT_CORAL)),
            Transform(vec_w, _vec_arrow(new_w, ACCENT_PURPLE)),
            Transform(vec_v1, _vec_arrow(new_v1, ACCENT_GREEN)),
            Transform(vec_v2, _vec_arrow(new_v2, ACCENT_GOLD)),
            run_time=4.0,
        )
        self.wait(3.5)

        # Fade out non-eigenvectors to spotlight the two invariant directions
        self.play(
            FadeOut(vec_u), FadeOut(span_u),
            FadeOut(vec_w), FadeOut(span_w),
            FadeOut(hook_label),
            run_time=1.0,
        )

        spotlight = make_info_card(
            "Invariant Directions!",
            [
                "Green (1, 0) stayed on its line — scaled by 3.",
                "Gold (-1, 1) stayed on its line — scaled by 2.",
                "Why do these special directions refuse to turn?",
            ],
            accent=ACCENT_GOLD,
            width=5.8,
        ).to_corner(UR, buff=0.35)

        self.play(FadeIn(spotlight), Indicate(vec_v1, color=ACCENT_GREEN), Indicate(vec_v2, color=ACCENT_GOLD), run_time=1.5)
        self.wait(8.0)
        self.play(FadeOut(*self.mobjects), run_time=1.0)


# ---------------------------------------------------------------------------
# SCENE 2: CONCEPT INTRODUCTION (~40s)
# ---------------------------------------------------------------------------
class Scene2_ConceptIntro(Scene):
    def construct(self) -> None:
        badge = make_badge("2. CONCEPT & DEFINITION", ACCENT_BLUE).to_corner(UL, buff=0.35)
        self.play(FadeIn(badge), run_time=0.7)

        # Learning objective
        obj_title = Text("Learning Objective", font="Helvetica Neue", font_size=26, color=ACCENT_GOLD, weight="BOLD")
        obj_text = Text(
            "By the end of this video, you will be able to understand, compute,\n"
            "and geometrically interpret eigenvalues and eigenvectors of a 2×2 matrix.",
            font="Helvetica Neue",
            font_size=23,
            color=PRIMARY_TEXT,
            line_spacing=1.35,
        )
        obj_group = VGroup(obj_title, obj_text).arrange(DOWN, buff=0.22).to_edge(UP, buff=1.15)
        obj_box = SurroundingRectangle(obj_group, color=ACCENT_GOLD, buff=0.28, corner_radius=0.14, stroke_width=1.6)

        self.play(FadeIn(obj_group), Create(obj_box), run_time=1.3)
        self.wait(6.5)
        self.play(FadeOut(obj_group), FadeOut(obj_box), run_time=0.8)

        # Formal Definition & Notation
        eq = math_svg(r"A\mathbf{v} = \lambda\mathbf{v}, \quad \mathbf{v} \neq \mathbf{0}", color=PRIMARY_TEXT, font_size=44)
        eq.move_to(UP * 1.55)
        eq_box = SurroundingRectangle(eq, color=ACCENT_BLUE, buff=0.28, corner_radius=0.14, stroke_width=2.0)

        self.play(Write(eq), Create(eq_box), run_time=1.6)
        self.wait(4.0)

        # Define every symbol before use
        n1 = VGroup(
            math_svg(r"A", color=ACCENT_BLUE, font_size=30),
            Text(":  an n × n square transformation matrix", font="Helvetica Neue", font_size=22, color=PRIMARY_TEXT),
        ).arrange(RIGHT, buff=0.2)

        n2 = VGroup(
            math_svg(r"\mathbf{v}", color=ACCENT_GREEN, font_size=30),
            Text(":  a non-zero eigenvector (direction stays on its span)", font="Helvetica Neue", font_size=22, color=PRIMARY_TEXT),
        ).arrange(RIGHT, buff=0.2)

        n3 = VGroup(
            math_svg(r"\lambda", color=ACCENT_GOLD, font_size=30),
            Text(":  the scalar eigenvalue (how much v stretches or flips)", font="Helvetica Neue", font_size=22, color=PRIMARY_TEXT),
        ).arrange(RIGHT, buff=0.2)

        n4 = Text(
            "Why v ≠ 0?  Because A·0 = 0 = λ·0 holds trivially for every λ — it reveals no direction.",
            font="Helvetica Neue",
            font_size=20,
            color=MUTED_TEXT,
        )

        notes = VGroup(n1, n2, n3, n4).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq_box, DOWN, buff=0.65)

        for item in [n1, n2, n3]:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=1.1)
            self.wait(3.2)

        self.play(FadeIn(n4, shift=UP * 0.15), run_time=1.1)
        self.wait(7.0)
        self.play(FadeOut(*self.mobjects), run_time=1.0)


# ---------------------------------------------------------------------------
# SCENE 3: VISUAL INTUITION (~55s)
# ---------------------------------------------------------------------------
class Scene3_VisualIntuition(Scene):
    def construct(self) -> None:
        badge = make_badge("3. VISUAL INTUITION", ACCENT_BLUE).to_corner(UL, buff=0.35)
        plane = _base_plane()
        self.play(Create(plane), FadeIn(badge), run_time=1.2)

        # Show matrix A on top-right
        a_eq = VGroup(
            math_svg(r"A =", color=ACCENT_BLUE, font_size=32),
            make_matrix([["3", "1"], ["0", "2"]], color=PRIMARY_TEXT, font_size=30),
        ).arrange(RIGHT, buff=0.18)
        a_card_bg = RoundedRectangle(
            corner_radius=0.14,
            width=a_eq.width + 0.5,
            height=a_eq.height + 0.4,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.5,
            fill_color="#090D16",
            fill_opacity=0.9,
        )
        a_eq.move_to(a_card_bg.get_center())
        a_card = VGroup(a_card_bg, a_eq).to_corner(UR, buff=0.35)
        self.play(FadeIn(a_card), run_time=0.8)

        # Basis vectors i-hat and j-hat + test vector w=(1,1)
        i_hat = _vec_arrow((1, 0), ACCENT_GREEN)
        j_hat = _vec_arrow((0, 1), ACCENT_CORAL)
        i_lbl = math_svg(r"\hat{\imath} = (1,0)", color=ACCENT_GREEN, font_size=22).next_to(i_hat, DOWN, buff=0.15)
        j_lbl = math_svg(r"\hat{\jmath} = (0,1)", color=ACCENT_CORAL, font_size=22).next_to(j_hat, LEFT, buff=0.15)

        span_x = _span_line((1, 0), ACCENT_GREEN)
        span_y = _span_line((0, 1), ACCENT_CORAL)

        self.play(
            Create(span_x), Create(span_y),
            GrowArrow(i_hat), GrowArrow(j_hat),
            FadeIn(i_lbl), FadeIn(j_lbl),
            run_time=1.4,
        )
        self.wait(3.5)

        # Transform plane and basis vectors
        self.play(
            FadeOut(i_lbl), FadeOut(j_lbl),
            plane.animate.apply_matrix(A_MAT),
            Transform(i_hat, _vec_arrow((3, 0), ACCENT_GREEN)),
            Transform(j_hat, _vec_arrow((1, 2), ACCENT_CORAL)),
            run_time=3.2,
        )
        i_after = math_svg(r"A\hat{\imath} = (3,0) = 3\hat{\imath}", color=ACCENT_GREEN, font_size=22).next_to(i_hat, DOWN, buff=0.2)
        j_after = math_svg(r"A\hat{\jmath} = (1,2) \text{ (rotated!)}", color=ACCENT_CORAL, font_size=22).next_to(j_hat, RIGHT, buff=0.18)
        self.play(FadeIn(i_after), FadeIn(j_after), run_time=1.0)
        self.wait(6.0)

        # Reset plane cleanly to test second eigenvector v2 = (-1, 1)
        self.play(
            FadeOut(i_hat), FadeOut(j_hat), FadeOut(i_after), FadeOut(j_after),
            FadeOut(span_x), FadeOut(span_y),
            FadeOut(plane),
            run_time=0.9,
        )

        plane2 = _base_plane()
        self.play(Create(plane2), run_time=0.9)

        v2 = _vec_arrow((-1, 1), ACCENT_GOLD)
        span_v2 = _span_line((-1, 1), ACCENT_GOLD)
        v2_lbl = math_svg(r"\mathbf{v}_2 = (-1, 1)", color=ACCENT_GOLD, font_size=24).next_to(v2, LEFT, buff=0.18)

        self.play(Create(span_v2), GrowArrow(v2), FadeIn(v2_lbl), run_time=1.2)
        self.wait(1.5)

        self.play(
            FadeOut(v2_lbl),
            plane2.animate.apply_matrix(A_MAT),
            Transform(v2, _vec_arrow((-2, 2), ACCENT_GOLD)),
            run_time=3.0,
        )
        v2_after = math_svg(r"A\mathbf{v}_2 = (-2, 2) = 2\mathbf{v}_2", color=ACCENT_GOLD, font_size=24).next_to(v2, LEFT, buff=0.2)
        self.play(FadeIn(v2_after), run_time=0.9)
        self.wait(5.5)

        # Quick visual guide to what lambda values mean
        lambda_card = make_info_card(
            "What Does λ Tell Us?",
            [
                "λ > 1   →  stretch along the line",
                "0 < λ < 1 →  shrink toward origin",
                "λ < 0   →  flip direction & scale",
                "λ = 0   →  collapse to the origin",
            ],
            accent=ACCENT_GOLD,
            width=5.0,
        ).to_corner(DR, buff=0.35)
        self.play(FadeIn(lambda_card), run_time=1.0)
        self.wait(9.0)
        self.play(FadeOut(*self.mobjects), run_time=1.0)


# ---------------------------------------------------------------------------
# SCENE 4: WORKED EXAMPLE — STEP-BY-STEP ALGEBRA (~75s)
# ---------------------------------------------------------------------------
class Scene4_WorkedExample(Scene):
    def construct(self) -> None:
        badge = make_badge("4. WORKED EXAMPLE", ACCENT_BLUE).to_corner(UL, buff=0.35)
        self.play(FadeIn(badge), run_time=0.7)

        # Header matrix
        header = VGroup(
            Text("Find eigenvalues and eigenvectors of ", font="Helvetica Neue", font_size=24, color=PRIMARY_TEXT),
            math_svg(r"A =", color=ACCENT_BLUE, font_size=28),
            make_matrix([["3", "1"], ["0", "2"]], color=PRIMARY_TEXT, font_size=26),
        ).arrange(RIGHT, buff=0.16).to_edge(UP, buff=0.95)
        self.play(FadeIn(header), run_time=1.0)

        # Step 1: Rewrite Av = lambda v -> (A - lambda I)v = 0
        s1_title = Text("Step 1: Rewrite as a homogeneous system", font="Helvetica Neue", font_size=22, color=ACCENT_GOLD, weight="BOLD")
        s1_eq1 = math_svg(r"A\mathbf{v} = \lambda\mathbf{v} \;\;\Longrightarrow\;\; A\mathbf{v} = (\lambda I)\mathbf{v} \;\;\Longrightarrow\;\; (A - \lambda I)\mathbf{v} = \mathbf{0}", color=PRIMARY_TEXT, font_size=28)
        s1_note = Text(
            "For a non-zero vector v to map to 0, (A − λI) must squish space — so det(A − λI) = 0.",
            font="Helvetica Neue",
            font_size=19,
            color=MUTED_TEXT,
        )
        s1 = VGroup(s1_title, s1_eq1, s1_note).arrange(DOWN, buff=0.22).move_to(UP * 0.55)

        self.play(FadeIn(s1_title), Write(s1_eq1), run_time=1.8)
        self.wait(2.5)
        self.play(FadeIn(s1_note), run_time=1.0)
        self.wait(5.5)
        self.play(FadeOut(s1), run_time=0.8)

        # Step 2: Characteristic equation det(A - lambda I) = 0
        s2_title = Text("Step 2: Solve the characteristic equation", font="Helvetica Neue", font_size=22, color=ACCENT_GOLD, weight="BOLD")
        mat_al = make_det([["3 - \\lambda", "1"], ["0", "2 - \\lambda"]], color=PRIMARY_TEXT, font_size=28, col_buff=1.15)
        eq_zero = math_svg(r"= 0", color=PRIMARY_TEXT, font_size=30)
        det_row = VGroup(mat_al, eq_zero).arrange(RIGHT, buff=0.22)
        char_poly = math_svg(r"(3 - \lambda)(2 - \lambda) - (1)(0) = 0", color=PRIMARY_TEXT, font_size=30)
        roots = math_svg(r"\lambda_1 = 3, \qquad \lambda_2 = 2", color=ACCENT_GOLD, font_size=34)

        s2 = VGroup(s2_title, det_row, char_poly, roots).arrange(DOWN, buff=0.35).move_to(DOWN * 0.15)
        self.play(FadeIn(s2_title), FadeIn(det_row), run_time=1.4)
        self.wait(3.0)
        self.play(Write(char_poly), run_time=1.5)
        self.wait(2.5)
        self.play(Write(roots), run_time=1.4)
        self.wait(5.0)
        self.play(FadeOut(s2), run_time=0.8)

        # Step 3: Eigenvectors for lambda_1 = 3 and lambda_2 = 2 side-by-side
        left_col = VGroup(
            math_svg(r"\text{For } \lambda_1 = 3:", color=ACCENT_GREEN, font_size=28),
            VGroup(
                make_matrix([["0", "1"], ["0", "-1"]], color=PRIMARY_TEXT, font_size=25),
                make_matrix([["x"], ["y"]], color=PRIMARY_TEXT, font_size=25),
                math_svg(r"=", color=PRIMARY_TEXT, font_size=26),
                make_matrix([["0"], ["0"]], color=PRIMARY_TEXT, font_size=25),
            ).arrange(RIGHT, buff=0.14),
            math_svg(r"y = 0, \;\; x \text{ free}", color=PRIMARY_TEXT, font_size=24),
            VGroup(
                math_svg(r"\mathbf{v}_1 =", color=ACCENT_GREEN, font_size=28),
                make_matrix([["1"], ["0"]], color=ACCENT_GREEN, font_size=26),
            ).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.32)

        right_col = VGroup(
            math_svg(r"\text{For } \lambda_2 = 2:", color=ACCENT_GOLD, font_size=28),
            VGroup(
                make_matrix([["1", "1"], ["0", "0"]], color=PRIMARY_TEXT, font_size=25),
                make_matrix([["x"], ["y"]], color=PRIMARY_TEXT, font_size=25),
                math_svg(r"=", color=PRIMARY_TEXT, font_size=26),
                make_matrix([["0"], ["0"]], color=PRIMARY_TEXT, font_size=25),
            ).arrange(RIGHT, buff=0.14),
            math_svg(r"x + y = 0 \;\Rightarrow\; x = -y", color=PRIMARY_TEXT, font_size=24),
            VGroup(
                math_svg(r"\mathbf{v}_2 =", color=ACCENT_GOLD, font_size=28),
                make_matrix([["-1"], ["1"]], color=ACCENT_GOLD, font_size=26),
            ).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, buff=0.32)

        cols = VGroup(left_col, right_col).arrange(RIGHT, buff=1.35).move_to(DOWN * 0.25)
        sep = Line(UP * 1.4, DOWN * 2.1, color=GRID_COLOR, stroke_width=2.0)

        self.play(Create(sep), FadeIn(left_col[0]), FadeIn(right_col[0]), run_time=1.0)
        self.play(FadeIn(left_col[1]), FadeIn(right_col[1]), run_time=1.5)
        self.wait(3.5)
        self.play(Write(left_col[2]), Write(right_col[2]), run_time=1.5)
        self.wait(3.0)
        self.play(FadeIn(left_col[3]), FadeIn(right_col[3]), run_time=1.3)
        self.wait(5.5)
        self.play(FadeOut(cols), FadeOut(sep), run_time=0.8)

        # Step 4: Verify by substitution!
        ver_title = Text("Step 4: Verify by direct substitution", font="Helvetica Neue", font_size=22, color=ACCENT_BLUE, weight="BOLD")
        ver1 = VGroup(
            make_matrix([["3", "1"], ["0", "2"]], color=PRIMARY_TEXT, font_size=26),
            make_matrix([["1"], ["0"]], color=ACCENT_GREEN, font_size=26),
            math_svg(r"=", color=PRIMARY_TEXT, font_size=28),
            make_matrix([["3"], ["0"]], color=ACCENT_GREEN, font_size=26),
            math_svg(r"= 3\,\mathbf{v}_1", color=ACCENT_GREEN, font_size=28),
        ).arrange(RIGHT, buff=0.16)

        ver2 = VGroup(
            make_matrix([["3", "1"], ["0", "2"]], color=PRIMARY_TEXT, font_size=26),
            make_matrix([["-1"], ["1"]], color=ACCENT_GOLD, font_size=26),
            math_svg(r"=", color=PRIMARY_TEXT, font_size=28),
            make_matrix([["-2"], ["2"]], color=ACCENT_GOLD, font_size=26),
            math_svg(r"= 2\,\mathbf{v}_2", color=ACCENT_GOLD, font_size=28),
        ).arrange(RIGHT, buff=0.16)

        ver_group = VGroup(ver_title, ver1, ver2).arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        self.play(FadeIn(ver_title), run_time=0.8)
        self.play(FadeIn(ver1), run_time=1.4)
        self.wait(3.5)
        self.play(FadeIn(ver2), run_time=1.4)
        self.wait(5.5)
        self.play(FadeOut(*self.mobjects), run_time=1.0)


# ---------------------------------------------------------------------------
# SCENE 5: INTERPRETATION (~50s)
# ---------------------------------------------------------------------------
class Scene5_Interpretation(Scene):
    def construct(self) -> None:
        badge = make_badge("5. INTERPRETATION", ACCENT_BLUE).to_corner(UL, buff=0.35)
        plane = _base_plane()
        self.play(Create(plane), FadeIn(badge), run_time=1.0)

        # Show eigenspaces and decompose x = (1, 2) = 3*v1 + 2*v2
        span_v1 = _span_line((1, 0), ACCENT_GREEN)
        span_v2 = _span_line((-1, 1), ACCENT_GOLD)
        v1 = _vec_arrow((1, 0), ACCENT_GREEN)
        v2 = _vec_arrow((-1, 1), ACCENT_GOLD)
        x_vec = _vec_arrow((1, 2), ACCENT_PURPLE)

        x_lbl = math_svg(r"\mathbf{x} = (1, 2) = 3\mathbf{v}_1 + 2\mathbf{v}_2", color=ACCENT_PURPLE, font_size=24).next_to(x_vec, UP + RIGHT, buff=0.15)

        self.play(Create(span_v1), Create(span_v2), GrowArrow(v1), GrowArrow(v2), run_time=1.3)
        self.play(GrowArrow(x_vec), FadeIn(x_lbl), run_time=1.3)
        self.wait(5.0)

        info = make_info_card(
            "Why Eigenvectors Simplify Repeated Steps",
            [
                "Write any vector x in the eigenbasis: x = 3v₁ + 2v₂.",
                "Applying A scales each component independently:",
                "Ax = 3(3v₁) + 2(2v₂) = 9v₁ + 4v₂ = (5, 4).",
            ],
            accent=ACCENT_PURPLE,
            width=5.8,
        ).to_corner(UR, buff=0.35)
        self.play(FadeIn(info), run_time=1.0)
        self.wait(5.0)

        # Animate A acting on v1, v2, x
        self.play(
            FadeOut(x_lbl),
            plane.animate.apply_matrix(A_MAT),
            Transform(v1, _vec_arrow((3, 0), ACCENT_GREEN)),
            Transform(v2, _vec_arrow((-2, 2), ACCENT_GOLD)),
            Transform(x_vec, _vec_arrow((5, 4), ACCENT_PURPLE)),
            run_time=3.2,
        )
        ax_lbl = math_svg(r"A\mathbf{x} = (5, 4)", color=ACCENT_PURPLE, font_size=24).next_to(x_vec, UP, buff=0.15)
        self.play(FadeIn(ax_lbl), run_time=0.9)
        self.wait(5.5)

        # Trace & Determinant connection card
        td_card = make_info_card(
            "Built-in Sanity Checks",
            [
                "Trace:       tr(A) = 3 + 2 = 5 = λ₁ + λ₂",
                "Determinant: det(A) = 6 = λ₁ · λ₂  (area scale!)",
                "Dominant λ₁ = 3 pulls Aⁿx toward v₁ over time.",
            ],
            accent=ACCENT_GOLD,
            width=5.8,
        ).to_corner(DR, buff=0.35)
        self.play(FadeIn(td_card), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(*self.mobjects), run_time=1.0)


# ---------------------------------------------------------------------------
# SCENE 6: SUMMARY & CREDITS / CLOSING FRAME (~35s)
# ---------------------------------------------------------------------------
class Scene6_SummaryCredits(Scene):
    def construct(self) -> None:
        badge = make_badge("6. SUMMARY & CREDITS", ACCENT_BLUE).to_corner(UL, buff=0.35)
        self.play(FadeIn(badge), run_time=0.7)

        title = Text("Three Core Takeaways", font="Helvetica Neue", font_size=34, color=ACCENT_GOLD, weight="BOLD").to_edge(UP, buff=0.95)
        self.play(FadeIn(title), run_time=0.8)

        t1 = make_info_card(
            "1. Geometric Meaning",
            ["Eigenvectors stay on their own span line under A; eigenvalues give the scale factor."],
            accent=ACCENT_GREEN,
            width=11.0,
        )
        t2 = make_info_card(
            "2. Algebraic Recipe",
            ["Solve det(A − λI) = 0 for λ, then solve (A − λI)v = 0 for non-zero v."],
            accent=ACCENT_BLUE,
            width=11.0,
        )
        t3 = make_info_card(
            "3. Power & Interpretation",
            ["In an eigenbasis, matrix multiplication becomes simple component-wise scaling."],
            accent=ACCENT_PURPLE,
            width=11.0,
        )
        takeaways = VGroup(t1, t2, t3).arrange(DOWN, buff=0.32).move_to(DOWN * 0.25)

        for card in [t1, t2, t3]:
            self.play(FadeIn(card, shift=UP * 0.2), run_time=1.1)
            self.wait(4.5)

        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(takeaways), run_time=0.9)

        # Closing Frame: Credits & AI Disclosure
        c_title = Text("Credits & AI Disclosure", font="Helvetica Neue", font_size=32, color=ACCENT_BLUE, weight="BOLD")
        c_lines = VGroup(
            Text("Created by: Varad Annadate  (Student ID: E25B070724)", font="Helvetica Neue", font_size=22, color=PRIMARY_TEXT, weight="BOLD"),
            Text("Course: Linear Algebra and Calculus (M3) — Internal Assessment", font="Helvetica Neue", font_size=20, color=MUTED_TEXT),
            Text("References: 3Blue1Brown (Essence of Linear Algebra, Ch. 14); Gilbert Strang (Intro to Linear Algebra)", font="Helvetica Neue", font_size=19, color=PRIMARY_TEXT),
            Text("Animation Engine: Manim Community Edition (Python) + Matplotlib Mathtext", font="Helvetica Neue", font_size=19, color=PRIMARY_TEXT),
            Text("Music Credit: Original ambient track synthesized in Python (music_gen.py)", font="Helvetica Neue", font_size=19, color=ACCENT_GOLD),
            Text("AI Disclosure: Antigravity (Gemini) assisted with Manim scripting, storyboard PDF, and narration draft.", font="Helvetica Neue", font_size=19, color=ACCENT_CORAL),
            Text("Voice-Over Narration: Varad Annadate", font="Helvetica Neue", font_size=19, color=ACCENT_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)

        closing = VGroup(c_title, c_lines).arrange(DOWN, buff=0.45).center()
        self.play(FadeIn(closing), run_time=1.4)
        self.wait(10.5)
        self.play(FadeOut(*self.mobjects), run_time=1.0)
