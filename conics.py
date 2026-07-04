import numpy as np
from manim import *


K = 0.6          # cone radius-per-height (slope of the radius)
H = 1.25         # half-height of the double cone

THETA_PARABOLA = np.arctan(1.0 / K)   # tilt angle where the section is a parabola
THETA_END = 100 * DEGREES             # final tilt (well into the hyperbola regime)
C_MID = 0.7                           # plane offset used while tilting through Ellipse/Parabola

# A cool-to-hot palette that mirrors the title's blue -> purple -> red gradient,
# one accent colour per stage of the journey.
KIND_COLORS = {
    "Circle": BLUE,
    "Ellipse": TEAL,
    "Parabola": PURPLE,
    "Hyperbola": RED,
}

# Vertical layout -- evenly spaced with a clear buffer at the very top and
# bottom of the frame (frame spans y = -4 .. 4).
TITLE_BUFF = 0.4
GRAPH_ANCHOR = UP * 2.15
LABEL_ANCHOR = DOWN * 2.85


def cone_func(u, v):
    # u : angle around,  v : signed height  -> double cone
    return np.array([K * v * np.cos(u), K * v * np.sin(u), v])


def plane_point(s, w, theta, c):
    """World point on the cutting plane, given its own orthonormal local
    coordinates (s along the fixed x-axis, w along the tilting axis)."""
    ct, st = np.cos(theta), np.sin(theta)
    return np.array([s, -c * st + w * ct, c * ct + w * st])


def section_coeffs(theta, c):
    """Coefficients of  s^2 = A*w^2 + B*w + C , the cone/plane intersection
    written in the plane's own local coordinates."""
    ct, st = np.cos(theta), np.sin(theta)
    A = K * K * st * st - ct * ct
    B = 2 * c * st * ct * (K * K + 1)
    C = c * c * (K * K * ct * ct - st * st)
    return A, B, C


def _theta_disconnect(c, theta_max, bound_frac=0.98):
    """The tilt angle at which the ellipse's far end first exits the finite
    cone (|Z| crosses the clip bound) -- i.e. the moment it visibly stops
    being a closed loop, well before the exact mathematical parabola angle."""
    def far_extent(theta):
        A, B, C = section_coeffs(theta, c)
        disc = max(B * B - 4 * A * C, 0.0)
        w1 = (-B + np.sqrt(disc)) / (2 * A)
        w2 = (-B - np.sqrt(disc)) / (2 * A)
        ct, st = np.cos(theta), np.sin(theta)
        return max(abs(c * ct + w1 * st), abs(c * ct + w2 * st))

    bound = H * bound_frac
    lo_t, hi_t = 1e-3, theta_max - 1e-3
    for _ in range(50):
        mid = (lo_t + hi_t) / 2
        if far_extent(mid) < bound:
            lo_t = mid
        else:
            hi_t = mid
    return lo_t


THETA_DISCONNECT = _theta_disconnect(C_MID, THETA_PARABOLA)


def _clip_to_cone(s_vals, w_vals, theta, c, n):
    """Keep only the contiguous run (around the vertex) that stays on the
    finite cone, i.e. where |Z| <= H, then resample it evenly."""
    ct, st = np.cos(theta), np.sin(theta)
    z = c * ct + w_vals * st
    mask = np.abs(z) <= H * 0.98
    if not mask[len(mask) // 2]:
        mask = np.abs(z) <= H * 1.05  # fall back with a looser bound
    mid = len(mask) // 2
    if not mask[mid]:
        return None
    lo_i = hi_i = mid
    while lo_i > 0 and mask[lo_i - 1]:
        lo_i -= 1
    while hi_i < len(mask) - 1 and mask[hi_i + 1]:
        hi_i += 1
    if hi_i - lo_i < 2:
        return None
    s_sub, w_sub = s_vals[lo_i:hi_i + 1], w_vals[lo_i:hi_i + 1]
    s_new = np.linspace(s_sub[0], s_sub[-1], n)
    w_new = np.interp(s_new, s_sub, w_sub)
    return np.stack([s_new, w_new], axis=1)


def _clip_w_range_to_cone(lo, hi, theta, c):
    """Intersect the ellipse's parameter range [lo, hi] with the range of
    w for which |Z| <= H, so an ellipse that grows past the finite cone's
    rim is truncated (an open arc) instead of just growing larger."""
    ct, st = np.cos(theta), np.sin(theta)
    if abs(st) < 1e-9:
        return lo, hi
    bound = H * 0.98
    wa = (bound - c * ct) / st
    wb = (-bound - c * ct) / st
    w_min, w_max = min(wa, wb), max(wa, wb)
    new_lo, new_hi = max(lo, w_min), min(hi, w_max)
    if new_hi - new_lo < 1e-6:
        return None
    return new_lo, new_hi


def local_curve_points(theta, c, n=50):
    """Return a list of (N,2) arrays of (s, w) points tracing the
    cross-section in the plane's own local coordinates, clipped to the
    finite double cone (|Z| <= H)."""
    A, B, C = section_coeffs(theta, c)

    if abs(A) < 1e-3:                       # ---- parabola ----
        if abs(B) < 1e-6:
            B = 1e-6
        s_vals = np.linspace(-3.0, 3.0, 400)
        w_vals = (s_vals ** 2 - C) / B
        seg = _clip_to_cone(s_vals, w_vals, theta, c, n)
        return [seg] if seg is not None else []

    if A < 0:                               # ---- circle / ellipse ----
        disc = max(B * B - 4 * A * C, 0.0)
        w1 = (-B + np.sqrt(disc)) / (2 * A)
        w2 = (-B - np.sqrt(disc)) / (2 * A)
        lo, hi = min(w1, w2), max(w1, w2)

        if hi - lo < 1e-6:
            # degenerate case: the plane only touches the cone at a single
            # point (e.g. the apex) -- draw a tiny ring to mark it, not nothing
            eps = 0.035
            angles = np.linspace(0, TAU, n)
            pt = np.stack([eps * np.cos(angles), lo + eps * np.sin(angles)], axis=1)
            return [pt]

        clipped = _clip_w_range_to_cone(lo, hi, theta, c)
        if clipped is None:
            return []
        lo, hi = clipped
        w_vals = np.linspace(lo, hi, n)
        R = np.clip(A * w_vals ** 2 + B * w_vals + C, 0, None)
        s_vals = np.sqrt(R)
        # two separate arcs (not force-joined) -- when an end is a true
        # root (s=0) they meet there naturally, forming a closed loop;
        # when an end is clipped by the cone's rim they stay open, so a
        # partly-clipped ellipse reads as a truncated arc, not a bigger loop
        top = np.stack([s_vals, w_vals], axis=1)
        bot = np.stack([-s_vals, w_vals], axis=1)
        return [top, bot]

    # ---- hyperbola : two open branches ----
    disc0 = B * B - 4 * A * C
    s_vals = np.linspace(-3.0, 3.0, 400)
    rad = np.clip(disc0 + 4 * A * s_vals ** 2, 0, None)
    sq = np.sqrt(rad)
    w_hi = (-B + sq) / (2 * A)
    w_lo = (-B - sq) / (2 * A)
    seg_hi = _clip_to_cone(s_vals, w_hi, theta, c, n)
    seg_lo = _clip_to_cone(s_vals, w_lo, theta, c, n)
    return [seg for seg in (seg_hi, seg_lo) if seg is not None]


def make_plane(theta, c):
    return Surface(
        lambda s, w: plane_point(s, w, theta, c),
        u_range=[-1.05, 1.05], v_range=[-1.3, 1.3], resolution=(2, 2),
        fill_opacity=0.28, checkerboard_colors=[BLUE_E, PURPLE_E],
        stroke_width=1, stroke_color=PURPLE_B,
    )


def _pad_segments(segs, n=2):
    """Always return exactly n segments (padding with degenerate points),
    so the mobject's child count never changes between frames -- a
    changing child count breaks always_redraw's fixed-in-frame state."""
    segs = list(segs)
    while len(segs) < n:
        segs.append(np.zeros((2, 2)))
    return segs[:n]


def make_curve_3d(theta, c, color=RED):
    group = VGroup()
    for pts in _pad_segments(local_curve_points(theta, c)):
        world_pts = [plane_point(s, w, theta, c) for s, w in pts]
        vm = VMobject(stroke_color=color, stroke_width=5, fill_opacity=0)
        vm.set_points_smoothly(world_pts)
        group.add(vm)
    return group


def make_mini_shape(theta, c, anchor, scale=0.36, color=RED):
    """Small flat preview of the true cross-section, recentred on `anchor`.
    The centring uses only the real segments -- padded placeholder segments
    (added so the mobject's child count stays fixed) must not skew it."""
    segs = local_curve_points(theta, c)
    if segs:
        all_pts = np.concatenate(segs, axis=0)
        center = (all_pts.min(axis=0) + all_pts.max(axis=0)) / 2
    else:
        center = np.zeros(2)
    ax, ay, _ = anchor

    group = VGroup()
    for pts in _pad_segments(segs):
        vm = VMobject(stroke_color=color, stroke_width=4, fill_opacity=0)
        flat_pts = [
            np.array([(s - center[0]) * scale + ax, (w - center[1]) * scale + ay, 0.0])
            for s, w in pts
        ]
        vm.set_points_smoothly(flat_pts)
        group.add(vm)
    return group


EQS = {
    "Circle": r"x^2+y^2=r^2",
    "Ellipse": r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1",
    "Parabola": r"x=a(y-k)^2+h",
    "Hyperbola": r"\frac{x^2}{a^2}-\frac{y^2}{b^2}=1",
}


def name_label(kind):
    color = KIND_COLORS[kind]
    txt = Text(kind, font_size=24, color=color)
    eqn = MathTex(EQS[kind], font_size=28, color=WHITE)
    eqn.next_to(txt, DOWN, buff=0.16)
    content = VGroup(txt, eqn)
    box = RoundedRectangle(
        width=content.width + 0.55, height=content.height + 0.38, corner_radius=0.14,
        fill_color=BLACK, fill_opacity=0.55, stroke_color=color, stroke_width=1.5,
    )
    box.move_to(content)
    return VGroup(box, content).move_to(LABEL_ANCHOR)


class ConicSections(ThreeDScene):
    def construct(self):
        # ---- Title: already fully drawn in, stays fixed at the top -------
        title = Tex(r"$\mathbb{C}$onic $\mathbb{S}$ections", font_size=40)
        title.set_color_by_gradient(BLUE, PURPLE, RED)
        title.to_edge(UP, buff=TITLE_BUFF)
        self.add_fixed_in_frame_mobjects(title)

        # ---- The double cone ----------------------------------------------
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)
        cone = Surface(
            cone_func, u_range=[0, TAU], v_range=[-H, H], resolution=(32, 16),
            checkerboard_colors=[GREY_C, GREY_D], fill_opacity=0.45,
            stroke_width=0.4, stroke_color=GREY_B,
        )
        self.play(Create(cone), run_time=1.2)
        self.wait(0.2)

        # ---- Live-updating plane, 3D cross-section, and top preview -------
        theta_tracker = ValueTracker(0.0)
        c_tracker = ValueTracker(C_MID)
        color_state = {"c": KIND_COLORS["Circle"]}

        plane = always_redraw(lambda: make_plane(theta_tracker.get_value(), c_tracker.get_value()))
        curve3d = always_redraw(lambda: make_curve_3d(
            theta_tracker.get_value(), c_tracker.get_value(), color_state["c"]))
        mini = always_redraw(lambda: make_mini_shape(
            theta_tracker.get_value(), c_tracker.get_value(), GRAPH_ANCHOR, color=color_state["c"]))

        graph_box = RoundedRectangle(
            width=1.3, height=1.5, corner_radius=0.14,
            fill_color=BLACK, fill_opacity=0.45, stroke_color=PURPLE_B, stroke_width=1.5,
        ).move_to(GRAPH_ANCHOR)
        graph_axes = Axes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=1.0, y_length=1.2,
            axis_config={"stroke_width": 1.5, "color": GREY_B, "tip_width": 0.08, "tip_height": 0.08},
        ).move_to(GRAPH_ANCHOR)

        label = name_label("Circle")
        self.add(plane, curve3d)
        self.add_fixed_in_frame_mobjects(graph_box, graph_axes, mini, label)
        self.wait(0.4)

        self.begin_ambient_camera_rotation(rate=0.10)

        def swap_label(old_label, new_kind):
            # the new label's own box/text already carry new_kind's colour,
            # but the live curve only switches to it once the crossfade is
            # done -- otherwise the shape's colour jumps ahead of the label
            new_label = name_label(new_kind)
            self.add_fixed_in_frame_mobjects(new_label)
            new_label.set_opacity(0)
            self.play(old_label.animate.set_opacity(0), new_label.animate.set_opacity(1), run_time=0.4)
            self.remove(old_label)
            color_state["c"] = KIND_COLORS[new_kind]
            return new_label

        # ---- Phase 1: plane slides all the way through the cone -----------
        # (level, theta=0) -- down through the apex (a single point) and on
        # to a circle on the second nappe, then back up to start the tilt.
        self.play(c_tracker.animate.set_value(1.0), run_time=0.8, rate_func=smooth)
        self.play(c_tracker.animate.set_value(0.0), run_time=0.9, rate_func=smooth)
        self.wait(0.4)
        self.play(c_tracker.animate.set_value(-1.0), run_time=0.9, rate_func=smooth)
        self.wait(0.2)
        self.play(c_tracker.animate.set_value(C_MID), run_time=0.9, rate_func=smooth)

        # ---- Phase 2: tilt from Circle through Ellipse to Parabola --------
        label = swap_label(label, "Ellipse")

        # tilt up to the point the ellipse's far end first exits the cone --
        # it still visibly reads as an open, disconnected arc from here on,
        # so the label flips to "Parabola" right at that moment
        self.play(theta_tracker.animate.set_value(THETA_DISCONNECT), run_time=1.3, rate_func=linear)
        label = swap_label(label, "Parabola")
        self.play(theta_tracker.animate.set_value(THETA_PARABOLA), run_time=1.3, rate_func=linear)
        self.wait(0.4)

        # ---- Phase 2b: still a parabola -- the plane slides, changing its
        # size/position, but the tilt (theta) stays locked at THETA_PARABOLA --
        self.play(c_tracker.animate.set_value(0.35), run_time=0.9, rate_func=smooth)
        self.play(c_tracker.animate.set_value(1.0), run_time=1.0, rate_func=smooth)
        self.play(c_tracker.animate.set_value(C_MID), run_time=0.7, rate_func=smooth)

        # ---- Phase 3: continue tilting into the Hyperbola regime ----------
        label = swap_label(label, "Hyperbola")

        self.play(
            theta_tracker.animate.set_value(THETA_END),
            c_tracker.animate.set_value(0.12),
            run_time=2.6, rate_func=linear,
        )
        self.wait(0.4)

        # ---- Phase 3b: still a hyperbola -- the tilt stays locked at
        # THETA_END, and the plane just slides sideways to reshape it -------
        self.play(c_tracker.animate.set_value(0.5), run_time=0.9, rate_func=smooth)
        self.play(c_tracker.animate.set_value(-0.35), run_time=1.0, rate_func=smooth)
        self.play(c_tracker.animate.set_value(0.15), run_time=0.7, rate_func=smooth)
        self.wait(0.4)

        self.stop_ambient_camera_rotation()
        self.wait(0.5)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        ConicSections().render()
