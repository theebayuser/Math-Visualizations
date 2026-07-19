import numpy as np
from manim import *

# ----------------------------------------------------------------------
#  Twelve Points -- the same 12 points, connected three different ways:
#  4 triangles, 3 squares, and a single {12/5} star polygon.  Finale
#  overlays all three edge sets on the same dots.
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

C_TRI = RED
C_SQR = BLUE
C_STAR = YELLOW
C_DOT = GREY_B

N = 12
CENTER = UP * 0.55
R = 2.55

TITLE_Y = 4.55
CAPTION_Y = -3.0

rng = np.random.default_rng(7)


def ring_points(seed_offset=0.0, r=R):
    """N points around a ring, seeded-jittered for an organic, non-perfect look."""
    pts = []
    for i in range(N):
        base_ang = TAU * i / N + PI / 2 + seed_offset
        ang = base_ang + rng.uniform(-0.09, 0.09)
        rad = r * (1 + rng.uniform(-0.07, 0.07))
        pts.append(CENTER + rad * np.array([np.cos(ang), np.sin(ang), 0.0]))
    return pts


def edge_group(pts, index_groups, color, closed=True, stroke_width=3.5):
    g = VGroup()
    for idxs in index_groups:
        verts = [pts[i] for i in idxs]
        poly = Polygon(*verts, color=color, stroke_width=stroke_width,
                       fill_opacity=0) if closed else VMobject(
            color=color, stroke_width=stroke_width).set_points_as_corners(verts)
        g.add(poly)
    return g


TRI_IDX = [(i, i + 4, i + 8) for i in range(4)]
SQR_IDX = [(i, i + 3, i + 6, i + 9) for i in range(3)]
STAR_IDX = [tuple((5 * k) % 12 for k in range(13))]   # closed {12/5} path


def make_dots(pts):
    return VGroup(*[Dot(p, radius=0.075, color=C_DOT) for p in pts])


class TwelveDots(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{T}$welve $\mathbb{P}$oints", font_size=40)
        title.set_color_by_gradient(RED, BLUE)
        title.move_to(UP * TITLE_Y)
        self.add(title)

        pts0 = ring_points(seed_offset=0.0)
        dots = make_dots(pts0)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.06, scale=0.3), run_time=1.2)
        self.wait(0.3)

        caption = None

        def show_caption(tex, color):
            nonlocal caption
            cap = Tex(tex, font_size=36, color=color).move_to(UP * CAPTION_Y)
            anims = [FadeIn(cap, shift=UP * 0.15)]
            if caption is not None:
                anims.append(FadeOut(caption))
            self.play(*anims, run_time=0.45)
            if caption is not None:
                self.remove(caption)
            caption = cap

        def morph_to(new_pts, run_time=1.1):
            self.play(*[dots[i].animate.move_to(new_pts[i]) for i in range(N)],
                      run_time=run_time, rate_func=smooth)

        # ---- phase A: 4 triangles ----
        pts_a = ring_points(seed_offset=0.15)
        morph_to(pts_a)
        tri = edge_group(pts_a, TRI_IDX, C_TRI)
        show_caption("4 triangles", C_TRI)
        self.play(LaggedStart(*[Create(t) for t in tri], lag_ratio=0.2), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(tri), run_time=0.5)

        # ---- phase B: 3 squares ----
        pts_b = ring_points(seed_offset=-0.2)
        morph_to(pts_b)
        sqr = edge_group(pts_b, SQR_IDX, C_SQR)
        show_caption("3 squares", C_SQR)
        self.play(LaggedStart(*[Create(s) for s in sqr], lag_ratio=0.25), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(sqr), run_time=0.5)

        # ---- phase C: one {12/5} star ----
        pts_c = ring_points(seed_offset=0.05)
        morph_to(pts_c)
        star = edge_group(pts_c, STAR_IDX, C_STAR, closed=False, stroke_width=3)
        show_caption("1 star", C_STAR)
        self.play(Create(star[0]), run_time=2.0, rate_func=linear)
        self.wait(0.8)

        # ---- finale: same points, all three edge sets together ----
        self.play(FadeOut(caption), run_time=0.35)
        caption = None
        tri_c = edge_group(pts_c, TRI_IDX, C_TRI)
        sqr_c = edge_group(pts_c, SQR_IDX, C_SQR)
        self.play(FadeIn(tri_c), FadeIn(sqr_c), run_time=0.9)
        show_caption("the same 12 points", WHITE)

        everything = VGroup(dots, star, tri_c, sqr_c)
        self.play(Rotate(everything, angle=TAU / 6, about_point=CENTER,
                          run_time=6.0, rate_func=linear))
        self.wait(0.5)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        TwelveDots().render()
