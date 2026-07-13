from manim import *
import numpy as np

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

# ---- palette (ties to the blue->red title gradient; matches the reference) ----
C_A = RED          # the "a" part
C_B = BLUE         # the "b" part
C_A2B = GOLD       # mixed a^2 b
C_AB2 = GREEN      # mixed a b^2   (also the 2D "ab" tile colour)

a = 1.6
b = 0.9
S = a + b

# ---- layout, tuned to the Reels safe zone (top 250px / bottom 420px /
# left 70px / right 193px reserved for UI at 1080x1920, i.e. 135 px/unit) ----
SAFE_TOP = 5.26
SAFE_BOTTOM = -4.0

TITLE_Y = 4.55
FIG = UP * 1.0       # where the figure is centred on screen
CUBE_FIG = FIG + LEFT * 0.65
CAPTION_Y = -2.3
EQ_Y = -3.35


def part(ch):
    """(center, size) along one axis for the 'a' or 'b' slab, cube centred at 0."""
    if ch == "a":
        return (-S / 2 + a / 2, a)
    return (S / 2 - b / 2, b)


def kind(triple):
    nb = triple.count("b")
    return {0: ("a3", C_A), 1: ("a2b", C_A2B), 2: ("ab2", C_AB2), 3: ("b3", C_B)}[nb]


class BinomialTheorem(ThreeDScene):
    def construct(self):
        self.current_eq = None
        self.caption = None

        # ---------- title (screen-locked, present from the start) ----------
        title = Tex(r"$\mathbb{B}$inomial $\mathbb{T}$heorem", font_size=56)
        title.set_color_by_gradient(BLUE, RED)
        title.move_to(UP * TITLE_Y)
        self.add_fixed_in_frame_mobjects(title)

        # start face-on: xy-plane looks like a normal 2D scene
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        self.stage_square()
        self.stage_cube()
        self.stage_outro()

    # ================================================================== #
    #  fixed-in-frame helpers                                            #
    # ================================================================== #
    def show_eq(self, tex, rt=0.6):
        eq = MathTex(tex, font_size=42)
        box = RoundedRectangle(
            width=eq.width + 0.6, height=eq.height + 0.5, corner_radius=0.15,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=BLUE_B, stroke_width=2,
        )
        grp = VGroup(box, eq).move_to(UP * EQ_Y)
        self.add_fixed_in_frame_mobjects(grp)
        anims = [FadeIn(grp)]
        old = self.current_eq
        if old is not None:
            anims.append(FadeOut(old))
        self.play(*anims, run_time=rt)
        if old is not None:
            self.remove(old)
        self.current_eq = grp

    def show_caption(self, tex, color=WHITE, rt=0.4):
        cap = MathTex(tex, font_size=52, color=color)
        cap.move_to(UP * CAPTION_Y)
        self.add_fixed_in_frame_mobjects(cap)
        anims = [FadeIn(cap)]
        if self.caption is not None:
            anims.append(FadeOut(self.caption))
        self.play(*anims, run_time=rt)
        if self.caption is not None:
            self.remove(self.caption)
        self.caption = cap

    def clear_caption(self, rt=0.3):
        if self.caption is not None:
            self.play(FadeOut(self.caption), run_time=rt)
            self.remove(self.caption)
            self.caption = None

    # ================================================================== #
    #  (a+b)^2  — the square                                             #
    # ================================================================== #
    def stage_square(self):
        tiles, groups = [], {0: [], 1: [], 2: []}
        for xi in "ab":
            for yi in "ab":
                cx, dx = part(xi)
                cy, dy = part(yi)
                nb = (xi == "b") + (yi == "b")
                col = {0: C_A, 1: C_AB2, 2: C_B}[nb]
                r = Rectangle(width=dx, height=dy, fill_color=col, fill_opacity=1,
                              stroke_color=BLACK, stroke_width=2)
                r.move_to([cx, cy, 0])
                tiles.append(r)
                groups[nb].append(r)
        square = VGroup(*tiles).shift(FIG)

        # Open directly on the completed degree-2 picture and theorem.
        self.add(square)
        eq = MathTex(r"(a+b)^2 = a^2 + 2ab + b^2", font_size=42)
        box = RoundedRectangle(
            width=eq.width + 0.6, height=eq.height + 0.5, corner_radius=0.15,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=BLUE_B, stroke_width=2,
        )
        self.current_eq = VGroup(box, eq).move_to(UP * EQ_Y)
        self.add_fixed_in_frame_mobjects(self.current_eq)
        self.add(self.current_eq)
        self.wait(0.4)

        # First identify the two unmixed terms, a^2 and b^2.
        pure_tiles = VGroup(*groups[0], *groups[2])
        self.show_caption(r"a^2 \quad \mathrm{and} \quad b^2", color=WHITE)
        self.play(pure_tiles.animate.set_stroke(YELLOW, 5), run_time=0.4)
        self.play(Indicate(pure_tiles, color=WHITE, scale_factor=1.1), run_time=0.8)
        self.play(pure_tiles.animate.set_stroke(BLACK, 2), run_time=0.4)
        self.clear_caption()

        # Then emphasise the two green "ab" tiles = the coefficient 2.
        ab_tiles = VGroup(*groups[1])
        self.show_caption(r"2 \times ab", color=C_AB2)
        self.play(ab_tiles.animate.set_stroke(YELLOW, 5), run_time=0.4)
        self.play(Indicate(ab_tiles, color=WHITE, scale_factor=1.12), run_time=0.9)
        self.play(ab_tiles.animate.set_stroke(BLACK, 2), run_time=0.4)
        self.clear_caption()
        self.wait(0.3)
        self.square = square

    # ================================================================== #
    #  (a+b)^3  — the cube                                               #
    # ================================================================== #
    def stage_cube(self):
        boxes = []            # (mobject, type_key, color)
        by_type = {"a3": [], "a2b": [], "ab2": [], "b3": []}
        for xi in "ab":
            for yi in "ab":
                for zi in "ab":
                    cx, dx = part(xi)
                    cy, dy = part(yi)
                    cz, dz = part(zi)
                    typ, col = kind((xi, yi, zi))
                    box = Prism(dimensions=[dx, dy, dz])
                    box.set_fill(col, opacity=1)
                    box.set_stroke(BLACK, 1)
                    box.set_shade_in_3d(True)
                    box.move_to([cx, cy, cz])
                    boxes.append((box, typ, col))
                    by_type[typ].append(box)
        cube = VGroup(*[bx for bx, _, _ in boxes]).shift(CUBE_FIG)

        # lift the camera: the flat square gains depth
        self.move_camera(phi=68 * DEGREES, theta=-45 * DEGREES, run_time=1.6)
        self.play(FadeIn(cube), FadeOut(self.square), run_time=1.0)
        self.begin_ambient_camera_rotation(rate=0.06)
        self.show_eq(r"(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3")
        self.wait(0.6)

        # explode radially so all 8 pieces are visible
        fig_center = CUBE_FIG
        orig = {}
        expl = {}
        for bx, _, _ in boxes:
            c = bx.get_center()
            orig[bx] = c
            expl[bx] = fig_center + (c - fig_center) * 1.9
        self.play(*[bx.animate.move_to(expl[bx]) for bx, _, _ in boxes],
                  run_time=1.2)

        # highlight each term-type in turn -> coefficient = piece count
        order = [("a3", r"1 \times a^3", C_A),
                 ("a2b", r"3 \times a^2b", C_A2B),
                 ("ab2", r"3 \times ab^2", C_AB2),
                 ("b3", r"1 \times b^3", C_B)]
        all_boxes = [bx for bx, _, _ in boxes]
        for typ, cap, col in order:
            targets = by_type[typ]
            others = [bx for bx in all_boxes if bx not in targets]
            self.show_caption(cap, color=col)
            self.play(*[bx.animate.set_opacity(0.12) for bx in others], run_time=0.4)
            self.play(*[Indicate(bx, color=WHITE, scale_factor=1.15) for bx in targets],
                      run_time=0.8)
            self.play(*[bx.animate.set_opacity(1.0) for bx in others], run_time=0.4)
        self.clear_caption()

        # reassemble
        self.play(*[bx.animate.move_to(orig[bx]) for bx, _, _ in boxes], run_time=1.0)
        self.cube = cube

    # ================================================================== #
    #  Outro — the general formula                                      #
    # ================================================================== #
    def stage_outro(self):
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1.0)
        self.play(FadeOut(self.cube), run_time=0.6)

        general = MathTex(
            r"(a+b)^n = \sum_{k=0}^{n} \binom{n}{k}\, a^{\,n-k} b^{\,k}",
            font_size=48,
        )
        gbox = RoundedRectangle(
            width=general.width + 0.7, height=general.height + 0.6, corner_radius=0.18,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=BLUE_B, stroke_width=2,
        )
        ggrp = VGroup(gbox, general).move_to(FIG)
        self.add_fixed_in_frame_mobjects(ggrp)
        anims = [FadeIn(ggrp, scale=0.9)]
        old = self.current_eq
        if old is not None:
            anims.append(FadeOut(old))
        self.play(*anims, run_time=0.8)
        if old is not None:
            self.remove(old)
        self.current_eq = ggrp
        self.wait(2.4)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        BinomialTheorem().render()
