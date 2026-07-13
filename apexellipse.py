import numpy as np
from manim import *

# ----------------------------------------------------------------------
#  Apex Ellipse -- launch a projectile at every angle with the same
#  speed; the highest point of each trajectory traces out an ellipse.
#  That ellipse always has eccentricity sqrt(3)/2, no matter the speed
#  or gravity (only its size changes).
#
#  Derivation (x measured from the launch point, A = v^2 / 2g):
#    trajectory(s) = (2A sin(2*theta) s,  4A sin^2(theta) s(1-s)),  s in [0,1]
#    apex = trajectory(0.5) = (A sin(2*theta), (A/2)(1 - cos(2*theta)))
#         = an ellipse centred (0, A/2), semi-axes A (horizontal), A/2 (vertical)
#    eccentricity = sqrt(1 - (1/2)^2) = sqrt(3)/2 -- independent of A.
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

C_TRAJ = BLUE
C_APEX = RED
C_ELLIPSE = RED

LAUNCH = DOWN * 1.1
N_TRAJ = 21
THETAS = np.linspace(0.08 * PI, 0.92 * PI, N_TRAJ)
A_MID = 1.25
A_LOW = 0.8

TITLE_Y = 4.55
CAPTION_Y = -1.75
EQ_Y = -2.85


def traj_point(theta, s, A):
    x = 2 * A * np.sin(2 * theta) * s
    y = 4 * A * np.sin(theta) ** 2 * s * (1 - s)
    return LAUNCH + np.array([x, y, 0.0])


def apex_point(theta, A):
    return traj_point(theta, 0.5, A)


def ellipse_point(phi, A):
    return LAUNCH + np.array([A * np.sin(phi), (A / 2) * (1 - np.cos(phi)), 0.0])


def make_trajectories(A, opacity=1.0):
    return VGroup(*[
        ParametricFunction(lambda s, th=th: traj_point(th, s, A), t_range=[0, 1],
                           color=C_TRAJ, stroke_width=2.5, stroke_opacity=opacity)
        for th in THETAS
    ])


def make_apex_dots(A):
    return VGroup(*[Dot(apex_point(th, A), radius=0.045, color=C_APEX) for th in THETAS])


def make_ellipse(A):
    return ParametricFunction(lambda phi: ellipse_point(phi, A), t_range=[0, TAU],
                              color=C_ELLIPSE, stroke_width=3.5)


class ApexEllipse(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{A}$pex $\mathbb{E}$llipse", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.move_to(UP * TITLE_Y)
        self.play(Write(title), run_time=1.0)

        ground = Line(LAUNCH + LEFT * 3.0, LAUNCH + RIGHT * 3.0,
                     color=GREY_C, stroke_width=2)
        launch_dot = Dot(LAUNCH, radius=0.06, color=WHITE)
        self.play(Create(ground), FadeIn(launch_dot), run_time=0.6)

        # ---- fan of trajectories, apex dots ----
        trajs = make_trajectories(A_MID)
        self.play(LaggedStartMap(Create, trajs, lag_ratio=0.06), run_time=2.4)
        apexes = make_apex_dots(A_MID)
        self.play(LaggedStartMap(FadeIn, apexes, lag_ratio=0.06, scale=0.4), run_time=1.2)
        self.wait(0.3)

        cap1 = Tex("the highest points form an ellipse", font_size=32)
        cap1.move_to(UP * CAPTION_Y)
        self.play(FadeIn(cap1, shift=UP * 0.15), run_time=0.5)

        # dim the trajectories so the ellipse reads clearly through the dots
        self.play(*[t.animate.set_stroke(opacity=0.22) for t in trajs], run_time=0.6)
        ellipse = make_ellipse(A_MID)
        self.play(Create(ellipse), run_time=1.4)
        self.wait(0.6)

        eq = MathTex(r"e = \frac{\sqrt{3}}{2} \approx 0.866", font_size=44)
        box = RoundedRectangle(
            width=eq.width + 0.7, height=eq.height + 0.55, corner_radius=0.16,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=RED_B, stroke_width=2,
        )
        eq_grp = VGroup(box, eq).move_to(UP * EQ_Y)
        self.play(FadeIn(eq_grp, shift=UP * 0.2), run_time=0.7)
        self.wait(1.2)

        # ---- invariance payoff: same eccentricity at every speed ----
        self.play(FadeOut(cap1), run_time=0.35)
        cap2 = Tex("same shape, any launch speed", font_size=32)
        cap2.move_to(UP * CAPTION_Y)
        self.play(FadeIn(cap2, shift=UP * 0.15), run_time=0.5)

        A_tracker = ValueTracker(A_MID)
        live_trajs = always_redraw(lambda: make_trajectories(A_tracker.get_value(), opacity=0.22))
        live_apex = always_redraw(lambda: make_apex_dots(A_tracker.get_value()))
        live_ellipse = always_redraw(lambda: make_ellipse(A_tracker.get_value()))

        self.remove(trajs, apexes, ellipse)
        self.add(live_trajs, live_apex, live_ellipse)

        self.play(A_tracker.animate.set_value(A_LOW), run_time=1.6, rate_func=smooth)
        self.wait(0.3)
        self.play(A_tracker.animate.set_value(A_MID), run_time=1.6, rate_func=smooth)
        self.wait(1.5)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        ApexEllipse().render()
