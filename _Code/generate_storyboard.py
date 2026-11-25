"""Generate the 6-Scene Storyboard PDF required for the M3 Internal Assessment."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUT_PDF = ROOT / "Storyboard_Eigenvalues_and_Eigenvectors.pdf"


def build_storyboard() -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="M3 Storyboard - Eigenvalues and Eigenvectors",
        author="Varad Annadate (E25B070724)",
    )

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#102A43")
    blue = colors.HexColor("#2B6CB0")
    slate = colors.HexColor("#4A5568")
    light_bg = colors.HexColor("#F0F4F8")

    h1 = ParagraphStyle(
        "H1", parent=styles["Heading1"], fontSize=18, textColor=navy, spaceAfter=4, leading=22
    )
    sub = ParagraphStyle(
        "Sub", parent=styles["Normal"], fontSize=10.5, textColor=blue, spaceAfter=10
    )
    h2 = ParagraphStyle(
        "H2", parent=styles["Heading2"], fontSize=12.5, textColor=navy, spaceBefore=10, spaceAfter=6
    )
    body = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9.5, textColor=colors.HexColor("#1A202C"), leading=13
    )
    cell_bold = ParagraphStyle(
        "CellBold", parent=body, fontName="Helvetica-Bold", fontSize=9, textColor=navy
    )
    cell_text = ParagraphStyle("CellText", parent=body, fontSize=8.8, leading=12)

    elements = [
        Paragraph("LINEAR ALGEBRA AND CALCULUS (M3) • INTERNAL ASSESSMENT", sub),
        Paragraph("6-Scene Storyboard: Eigenvalues &amp; Eigenvectors", h1),
        Paragraph(
            "<b>Student:</b> Varad Annadate &nbsp;|&nbsp; <b>Student ID:</b> E25B070724 &nbsp;|&nbsp; "
            "<b>Topic:</b> Eigenvalues and Eigenvectors (Linear Algebra) &nbsp;|&nbsp; <b>Target Duration:</b> ~5 min (1080p 16:9)",
            body,
        ),
        Spacer(1, 8),
        Paragraph("One-Sentence Learning Objective", h2),
        Paragraph(
            "<i>\"By the end of this video, the viewer will be able to understand, compute, and geometrically "
            "interpret eigenvalues and eigenvectors of a 2×2 matrix.\"</i>",
            body,
        ),
        Spacer(1, 8),
        Paragraph("6-Scene Storyboard Plan", h2),
    ]

    rows = [
        [
            Paragraph("<b>Scene</b>", cell_bold),
            Paragraph("<b>Purpose</b>", cell_bold),
            Paragraph("<b>Visual, Narration &amp; Math Plan</b>", cell_bold),
        ],
        [
            Paragraph("<b>1. Hook / Context</b><br/>(Opening + ~45s)", cell_bold),
            Paragraph("Spark curiosity and motivate why invariant directions matter.", cell_text),
            Paragraph(
                "<b>Visual:</b> Opening title frame (Title, Concept, Varad Annadate, E25B070724). "
                "Transition to dark 3b1b-style 2D NumberPlane with 4 vectors and dashed span lines. "
                "Apply A = [[3, 1], [0, 2]].<br/>"
                "<b>Math &amp; Narration:</b> Most vectors rotate off their span lines, but (1,0) and (-1,1) stay "
                "pinned to their lines, only scaling. Ask: <i>Why do these special directions refuse to turn?</i>",
                cell_text,
            ),
        ],
        [
            Paragraph("<b>2. Concept Introduction</b><br/>(~40s)", cell_bold),
            Paragraph("Define the concept, notation, and learning goal.", cell_text),
            Paragraph(
                "<b>Visual:</b> Learning objective card, then formal equation A<b>v</b> = λ<b>v</b> (<b>v</b> ≠ <b>0</b>) "
                "with color-coded notation breakdown.<br/>"
                "<b>Math &amp; Narration:</b> Define A (n×n matrix), <b>v</b> (non-zero eigenvector), λ (scalar eigenvalue). "
                "Explain why <b>v</b> = <b>0</b> is excluded (A·<b>0</b> = λ·<b>0</b> trivially for all λ).",
                cell_text,
            ),
        ],
        [
            Paragraph("<b>3. Visual Intuition</b><br/>(~55s)", cell_bold),
            Paragraph("Build geometric understanding before algebra.", cell_text),
            Paragraph(
                "<b>Visual:</b> Animate basis vectors î=(1,0) and ĵ=(0,1) under A: î stays on x-axis at (3,0), "
                "while ĵ rotates to (1,2). Reset and animate <b>v</b><sub>2</sub>=(-1,1) scaling to (-2,2) on y=-x. "
                "Show λ-meaning card (stretch, shrink, flip, collapse).<br/>"
                "<b>Narration:</b> Connect eigenvalues directly to scaling factors along invariant lines.",
                cell_text,
            ),
        ],
        [
            Paragraph("<b>4. Worked Example</b><br/>(~75s)", cell_bold),
            Paragraph("Demonstrate step-by-step algebraic derivation and verification.", cell_text),
            Paragraph(
                "<b>Visual &amp; Math:</b><br/>"
                "1) A<b>v</b> = λ<b>v</b> ⇒ (A − λI)<b>v</b> = <b>0</b>; explain why det(A − λI) = 0.<br/>"
                "2) det([[3−λ, 1], [0, 2−λ]]) = (3−λ)(2−λ) = 0 ⇒ λ<sub>1</sub>=3, λ<sub>2</sub>=2.<br/>"
                "3) Solve (A−3I)<b>v</b>=<b>0</b> ⇒ <b>v</b><sub>1</sub>=(1,0); (A−2I)<b>v</b>=<b>0</b> ⇒ <b>v</b><sub>2</sub>=(-1,1).<br/>"
                "4) Verify by substitution: A<b>v</b><sub>1</sub>=3<b>v</b><sub>1</sub>, A<b>v</b><sub>2</sub>=2<b>v</b><sub>2</sub>.",
                cell_text,
            ),
        ],
        [
            Paragraph("<b>5. Interpretation</b><br/>(~50s)", cell_bold),
            Paragraph("Connect algebra back to visual meaning.", cell_text),
            Paragraph(
                "<b>Visual:</b> Decompose <b>x</b> = (1,2) = 3<b>v</b><sub>1</sub> + 2<b>v</b><sub>2</sub> on the grid; "
                "animate A<b>x</b> = 9<b>v</b><sub>1</sub> + 4<b>v</b><sub>2</sub> = (5,4).<br/>"
                "<b>Math &amp; Narration:</b> Show how an eigenbasis turns matrix multiplication into independent "
                "component scaling, and verify tr(A) = 5 = λ<sub>1</sub>+λ<sub>2</sub>, det(A) = 6 = λ<sub>1</sub>λ<sub>2</sub>.",
                cell_text,
            ),
        ],
        [
            Paragraph("<b>6. Summary &amp; Credits</b><br/>(~35s)", cell_bold),
            Paragraph("Reinforce 3 core takeaways and cite sources/AI/music.", cell_text),
            Paragraph(
                "<b>Visual:</b> 3 takeaway cards (Geometry, Algebraic Recipe, Eigenbasis Power), followed by Closing Frame.<br/>"
                "<b>Credits &amp; Disclosure:</b> References (3Blue1Brown, Gilbert Strang), original synthesized ambient music "
                "credit (music_gen.py), AI disclosure (Antigravity/Gemini for Manim code, storyboard, script draft; "
                "voice-over by Varad Annadate).",
                cell_text,
            ),
        ],
    ]

    table = Table(rows, colWidths=[3.5 * cm, 4.0 * cm, 10.3 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), light_bg),
                ("TEXTCOLOR", (0, 0), (-1, 0), navy),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)
    print(f"Generated storyboard PDF: {OUT_PDF}")


if __name__ == "__main__":
    build_storyboard()
