"""
Linear Regression Animation — single-block executable in VSCode
Run with:  manim -pql linear_regression_animation.py LinearRegressionScene
For HD:    manim -pqh linear_regression_animation.py LinearRegressionScene
"""

from manim import *
import numpy as np

BG       = "#000000"
DOT_COL  = "#00E5FF"
LINE_COL = "#FF6B6B"
RES_COL  = "#FFD166"
FS       = 26          # was 20 — larger equations


def fit(pts):
    xs = np.array([p[0] for p in pts], dtype=float)
    ys = np.array([p[1] for p in pts], dtype=float)
    if len(xs) < 2 or np.std(xs) < 1e-9:
        return 0.0, float(np.mean(ys))
    m = (np.mean(xs*ys) - np.mean(xs)*np.mean(ys)) / (np.mean(xs**2) - np.mean(xs)**2)
    return float(m), float(np.mean(ys) - m*np.mean(xs))


def make_gradient_title():
    """
    Single MathTex so LaTeX handles all spacing and baseline alignment.
    Gradient is applied leaf-by-leaf using each glyph's x-position.
    """
    title = MathTex(
        r"\mathbb{L}\mathrm{inear}\ \mathbb{R}\mathrm{egression}",
        font_size=36,
    ).move_to(UP * 3.3)

    leaves = [m for m in title.get_family() if m is not title]
    if not leaves:
        return title

    c_start = np.array(color_to_rgb("#00E5FF"))
    c_end   = np.array(color_to_rgb("#FF00FF"))

    xs = [m.get_center()[0] for m in leaves]
    x_min, x_max = min(xs), max(xs)
    span = x_max - x_min if x_max > x_min else 1.0

    for m, x in zip(leaves, xs):
        t   = (x - x_min) / span
        rgb = (1 - t) * c_start + t * c_end
        m.set_color(rgb_to_color(rgb))

    return title


class LinearRegressionScene(Scene):

    def construct(self):
        self.camera.background_color = BG

        # ── TITLE — mathbb first letters + gradient fill ──────────────────────
        title = make_gradient_title()

        # ── AXES ──────────────────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=4.0, y_length=3.6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2.0,
                "include_tip": True,
                "tip_length": 0.15,
            },
        ).move_to(UP * 0.85)

        # ── EQUATIONS ─────────────────────────────────────────────────────────
        eq_model = MathTex(r"\hat{y} = \hat{\beta}_0 + \hat{\beta}_1 x",
                           font_size=FS, color=WHITE)
        eq_resid = MathTex(r"e_i = y_i - \hat{y}_i",
                           font_size=FS, color=RES_COL)
        eq_rss   = MathTex(r"\mathrm{RSS} = \textstyle\sum_{i=1}^{n} e_i^{\,2}",
                           font_size=FS, color=RES_COL)

        eq_col = VGroup(eq_model, eq_resid, eq_rss)\
            .arrange(DOWN, aligned_edge=LEFT, buff=0.30)

        panel_width  = ax.width - 0.2
        panel_height = eq_col.height + 0.52

        panel_fill = RoundedRectangle(
            width=panel_width, height=panel_height,
            corner_radius=0.12,
            fill_color=BLUE_D, fill_opacity=0.28,
            stroke_width=0,
        )
        panel_stroke = RoundedRectangle(
            width=panel_width, height=panel_height,
            corner_radius=0.12, fill_opacity=0,
            stroke_color=BLUE_C, stroke_width=2.0,
        )

        eq_group = VGroup(panel_fill, panel_stroke, eq_col)\
            .next_to(ax, DOWN, buff=0.35)

        panel_fill.move_to(eq_col)
        panel_stroke.move_to(eq_col)

        # ── DRAW EVERYTHING IN AT START ───────────────────────────────────────
        self.play(Write(title), Create(ax), run_time=1.0)
        self.play(
            FadeIn(panel_fill),
            Create(panel_stroke),
            FadeIn(eq_col),
            run_time=0.8,
        )
        self.wait(0.4)

        live_model = eq_model
        live_resid = eq_resid
        live_rss   = eq_rss

        # ── DATA POINTS ───────────────────────────────────────────────────────
        raw_pts = [
            (0.7, 1.0),
            (1.4, 4.9),
            (2.0, 1.8),
            (2.8, 6.2),
            (3.5, 2.9),
            (4.2, 5.4),
            (5.0, 3.6),
            (5.8, 8.1),
            (6.5, 5.2),
            (7.3, 9.3),
            (8.0, 6.0),
            (8.8, 9.5),
            (9.4, 7.4),
        ]

        dots      = VGroup()
        reg_line  = None
        resid_obj = None

        for i, (dx, dy) in enumerate(raw_pts):

            dot = Dot(ax.c2p(dx, dy), radius=0.09, color=DOT_COL)\
                    .set_fill(DOT_COL, opacity=0.95)\
                    .set_stroke(WHITE, width=0.8, opacity=0.5)
            self.play(FadeIn(dot, scale=0.5), run_time=0.20)
            dots.add(dot)

            cur = raw_pts[: i + 1]

            if len(cur) >= 2:
                m, b = fit(cur)
                y_hat = m * dx + b

                # Clip the regression line to the axes box [0,10] x [0,10]
                _x0, _x1 = 0.0, 10.0
                _y0, _y1 = 0.0, 10.0
                _cands = [_x0, _x1]
                if abs(m) > 1e-9:
                    _cands += [(_y0 - b) / m, (_y1 - b) / m]
                _valid = [x for x in _cands
                          if _x0 <= x <= _x1 and _y0 <= m*x+b <= _y1]
                if len(_valid) < 2:
                    _px0, _px1 = 0.0, 10.0
                else:
                    _px0, _px1 = min(_valid), max(_valid)

                new_line = Line(
                    ax.c2p(_px0, m*_px0+b),
                    ax.c2p(_px1, m*_px1+b),
                    stroke_width=3.0, color=LINE_COL,
                ).set_stroke(opacity=0.92)

                foot = ax.c2p(dx, y_hat)
                tip  = ax.c2p(dx, dy)
                new_res = VGroup(
                    Line(foot, tip, stroke_width=4.0, color=RES_COL).set_stroke(opacity=1.0),
                    Dot(foot, radius=0.055, color=RES_COL).set_fill(RES_COL, opacity=1),
                    Dot(tip,  radius=0.055, color=RES_COL).set_fill(RES_COL, opacity=1),
                )

                la = Create(new_line) if reg_line is None else Transform(reg_line, new_line)

                if resid_obj is None:
                    self.play(la, FadeIn(new_res), run_time=0.22)
                else:
                    self.play(la, FadeOut(resid_obj), run_time=0.15)
                    self.play(FadeIn(new_res), run_time=0.12)

                if reg_line is None:
                    reg_line = new_line
                resid_obj = new_res

            if i >= 3 and len(cur) >= 2:
                m, b = fit(cur)
                y_hat = m * dx + b
                sign  = "+" if b >= 0 else "-"

                n_model = MathTex(
                    rf"\hat{{y}} = {m:.2f}x \;{sign}\; {abs(b):.2f}",
                    font_size=FS, color=LINE_COL,
                ).move_to(live_model)

                ei = dy - y_hat
                n_resid = MathTex(
                    rf"e = {dy:.1f} - {y_hat:.1f} = {ei:+.1f}",
                    font_size=FS, color=RES_COL,
                ).move_to(live_resid)

                xs_ = np.array([p[0] for p in cur])
                ys_ = np.array([p[1] for p in cur])
                rss = float(np.sum((ys_ - (m*xs_+b))**2))
                n_rss = MathTex(
                    rf"\mathrm{{RSS}} = {rss:.1f}",
                    font_size=FS, color=RES_COL,
                ).move_to(live_rss)

                self.play(
                    ReplacementTransform(live_model, n_model),
                    ReplacementTransform(live_resid, n_resid),
                    ReplacementTransform(live_rss,   n_rss),
                    run_time=0.22,
                )
                live_model = n_model
                live_resid = n_resid
                live_rss   = n_rss

        self.wait(2.5)

        all_mobs = VGroup(
            title, ax, dots, reg_line,
            panel_fill, panel_stroke,
            live_model, live_resid, live_rss,
        )
        if resid_obj is not None:
            all_mobs.add(resid_obj)

        self.play(FadeOut(all_mobs), run_time=0.9)