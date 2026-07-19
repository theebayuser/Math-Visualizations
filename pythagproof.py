import numpy as np
from manim import *

# ----------------------------------------------------------------------
#  Pythagorean Theorem -- proof by similar triangles.
#  Scale the (a, b, c) right triangle by a, by b, and by c; the three
#  copies tile a single rectangle whose top edge is c^2 and whose bottom
#  edges are a^2 + b^2.  Same top, same bottom  =>  c^2 = a^2 + b^2.
#
#  Each copy is built with ONLY a similarity transform (uniform scale)
#  followed by rigid motions (reflection / rotation / translation) -- never
#  an arbitrary shape morph -- so it visibly stays "the same triangle,"
#  just bigger and rigidly moved into place.
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

a = 1.4
b = 1.05
c = float(np.hypot(a, b))
W = a * a + b * b          # rectangle width  (= c^2)
Hh = a * b                 # rectangle height

C_ORIG = YELLOW
C_XA = RED
C_XB = BLUE
C_XC = PURPLE

# layout (Reels safe zone: keep inside y in [-4.0, 5.26])
TITLE_Y = 4.55
TRI_C = np.array([0.0, 3.0, 0.0])      # the small reference triangle
RECT_C = np.array([0.0, 0.1, 0.0])     # the assembled rectangle
EQ_Y = -3.2

# rectangle-slot triangles, in rectangle-local coords (origin bottom-left)
RED_V = [(0, 0), (a * a, 0), (0, a * b)]
BLUE_V = [(a * a, 0), (W, 0), (W, a * b)]
PURP_V = [(0, a * b), (a * a, 0), (W, a * b)]
RECT_OFF = RECT_C - np.array([W / 2, Hh / 2, 0.0])


def solve_rigid_transform(verts, k):
    """Given a piece's 3 target vertices (rectangle-local, 2D tuples) and its
    scale factor k (relative to the original triangle with legs b along x
    and a along y from its right-angle vertex), find the right-angle vertex
    P0 and the rigid motion -- an optional reflection across the x-axis,
    then a rotation -- that turns the axis-aligned scaled original
    (legs (k*b, 0) and (0, k*a)) into this exact target triangle."""
    verts = [np.array(v, dtype=float) for v in verts]
    for i in range(3):
        P = verts[i]
        others = [verts[j] for j in range(3) if j != i]
        for o1, o2 in (others, others[::-1]):
            e1, e2 = o1 - P, o2 - P
            if (abs(np.linalg.norm(e1) - k * b) < 1e-6
                    and abs(np.linalg.norm(e2) - k * a) < 1e-6
                    and abs(np.dot(e1, e2)) < 1e-6):
                m1, m2 = e1 / (k * b), e2 / (k * a)
                M = np.column_stack([m1, m2])
                reflect = np.linalg.det(M) < 0
                Mrot = M @ np.diag([1.0, -1.0]) if reflect else M
                angle = np.degrees(np.arctan2(Mrot[1, 0], Mrot[0, 0]))
                return P, reflect, angle
    raise ValueError("no matching right-angle vertex found")


def side_label(p, q, tex, color, out=1.0, buff=0.3, font_size=32):
    """Label for the side p->q, offset along the (left-hand) perpendicular;
    flip with out=-1."""
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    mid = (p + q) / 2
    d = q - p
    n = np.array([-d[1], d[0], 0.0])
    n = n / np.linalg.norm(n) * out
    lab = MathTex(tex, color=color, font_size=font_size).move_to(mid + n * buff)
    # labels must render above later-added filled polygons (the purple slot
    # lands after the seam labels and would otherwise wash them out)
    lab.set_z_index(3)
    return lab


class PythagoreanProof(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{P}$ythagorean $\mathbb{T}$heorem", font_size=40)
        title.set_color_by_gradient(RED, PURPLE, BLUE)
        title.move_to(UP * TITLE_Y)
        self.add(title)

        # ---- the reference triangle: legs a (vertical), b (horizontal) ----
        yellow = Polygon(ORIGIN, RIGHT * b, UP * a,
                         fill_color=C_ORIG, fill_opacity=0.9,
                         stroke_color=BLACK, stroke_width=2)
        yellow.shift(TRI_C - yellow.get_center_of_mass())
        vo, vb, va = yellow.get_vertices()[:3]   # right-angle vertex, b-vertex, a-vertex
        lab_a = side_label(vo, va, "a", C_ORIG, out=1.0, buff=0.25)
        lab_b = side_label(vo, vb, "b", C_ORIG, out=-1.0, buff=0.25)
        lab_c = side_label(vb, va, "c", C_ORIG, out=-1.0, buff=0.25)

        self.play(DrawBorderThenFill(yellow), run_time=1.0)
        self.play(FadeIn(lab_a), FadeIn(lab_b), FadeIn(lab_c), run_time=0.5)
        self.wait(0.4)

        # world-space slot vertices (for the seam/edge labels)
        rv = [RECT_OFF + np.array([x, y, 0.0]) for x, y in RED_V]
        bv = [RECT_OFF + np.array([x, y, 0.0]) for x, y in BLUE_V]
        pv = [RECT_OFF + np.array([x, y, 0.0]) for x, y in PURP_V]

        stages = [
            (r"\times\, a", C_XA, RED_V, a, [
                side_label(rv[0], rv[1], "a^2", C_XA, out=-1.0),        # bottom
                side_label(rv[0], rv[2], "ab", C_XA, out=1.0),          # left
                side_label(rv[1], rv[2], "ac", WHITE, out=-1.0, buff=0.32),  # seam
            ]),
            (r"\times\, b", C_XB, BLUE_V, b, [
                side_label(bv[0], bv[1], "b^2", C_XB, out=-1.0),        # bottom
                side_label(bv[1], bv[2], "ab", C_XB, out=-1.0),         # right
                side_label(bv[0], bv[2], "bc", WHITE, out=1.0, buff=0.32),   # seam
            ]),
            (r"\times\, c", C_XC, PURP_V, c, [
                side_label(pv[0], pv[2], "c^2", C_XC, out=1.0),         # top
            ]),
        ]

        top_label = None
        bottom_labels = []
        for cap_tex, col, verts, k, labels in stages:
            P0_local, reflect, angle = solve_rigid_transform(verts, k)
            target_world = RECT_OFF + np.array([P0_local[0], P0_local[1], 0.0])
            anchor = vo   # scale + reorient happen right at the original's own corner

            cap = MathTex(cap_tex, color=col, font_size=44)
            cap.next_to(yellow, RIGHT, buff=0.9).align_to(yellow, UP)
            self.play(FadeIn(cap, shift=LEFT * 0.2), run_time=0.4)

            # ---- 1. multiply: a pure, uniform scale about the fixed corner ----
            copy = yellow.copy()
            copy.set_color(col)
            self.play(copy.animate.scale(k, about_point=anchor), run_time=0.9)

            # ---- 2. only rigid motions from here: reflect, then rotate ----
            if reflect:
                self.play(copy.animate.flip(axis=RIGHT, about_point=anchor), run_time=0.5)
            if abs(angle) > 1e-3:
                self.play(copy.animate.rotate(angle * DEGREES, about_point=anchor),
                          run_time=0.7)

            # the piece is now fully "multiplied" and correctly oriented, just
            # not yet in the rectangle -- hold so that state reads clearly
            self.wait(0.4)
            self.play(FadeOut(cap), run_time=0.3)

            # ---- 3. add it to the rectangle: a pure translation ----
            self.play(copy.animate.shift(target_world - anchor), run_time=1.0)
            self.play(*[FadeIn(l) for l in labels], run_time=0.5)
            self.wait(0.3)
            if col == C_XC:
                top_label = labels[0]
            else:
                bottom_labels.append(labels[0])

        self.wait(0.5)

        # ---- the punchline: same rectangle edge, two readings ----
        self.play(Indicate(top_label, color=WHITE, scale_factor=1.3), run_time=0.8)
        self.play(*[Indicate(l, color=WHITE, scale_factor=1.3) for l in bottom_labels],
                  run_time=0.8)

        eq = MathTex("c^2", "=", "a^2", "+", "b^2", font_size=52)
        eq[0].set_color(C_XC)
        eq[2].set_color(C_XA)
        eq[4].set_color(C_XB)
        box = RoundedRectangle(
            width=eq.width + 0.7, height=eq.height + 0.55, corner_radius=0.16,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=BLUE_B, stroke_width=2,
        )
        grp = VGroup(box, eq).move_to(UP * EQ_Y)
        self.play(FadeIn(grp, shift=UP * 0.25), run_time=0.8)
        self.wait(2.2)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        PythagoreanProof().render()
