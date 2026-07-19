import numpy as np
from manim import *

# ----------------------------------------------------------------------
#  Logic Gate Symbols -- all 8 standard gates side by side, wired to the
#  SAME two shared inputs A, B.  As (A, B) steps through every combination
#  (Gray-code order, so only one bit flips at a time), every gate reacts
#  simultaneously -- so instead of 8 isolated truth tables you watch all
#  8 gates respond live to the same signal (same comparison spirit as
#  riemann.py's shared-parameter grid of panels).
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

C_ON = YELLOW
C_OFF = GREY_D
C_WIRE = GREY_B
C_BUBBLE_STROKE = WHITE

GATE_W = 1.5
GATE_H = 1.05

# layout tuned to the real Reels safe zone (1080x1920 -> 8.0x14.22 units,
# ~0.0074 units/px): top margin 220px -> y<+5.48, bottom margin 320px ->
# y>-4.74.  We fill that zone.
TITLE_Y = 4.85
TOGGLE_Y = 3.55
GRID_TOP = 2.35
ROW_PITCH = 1.98
COL_X = 1.65           # +/- this, the two cells in a row


def quad_bezier(p0, p1, p2, n):
    t = np.linspace(0, 1, n)
    p0, p1, p2 = np.array(p0), np.array(p1), np.array(p2)
    return (1 - t)[:, None] ** 2 * p0 + 2 * (1 - t)[:, None] * t[:, None] * p1 + t[:, None] ** 2 * p2


def and_points(w=GATE_W, h=GATE_H, n_arc=20):
    x0 = -w / 2
    r = h / 2
    xm = x0 + (w - r)
    pts = [(x0, -h / 2), (x0, h / 2), (xm, h / 2)]
    for i in range(n_arc + 1):
        t = np.pi / 2 - i * (np.pi / n_arc)
        pts.append((xm + r * np.cos(t), r * np.sin(t)))
    pts.append((xm, -h / 2))
    return np.array(pts)


def or_points(w=GATE_W, h=GATE_H, n=18):
    x0, xf = -w / 2, w / 2
    back_top, back_bot = (x0, h / 2), (x0, -h / 2)
    tip = (xf, 0)
    back_ctrl = (x0 + 0.28 * w, 0)
    top_ctrl = (x0 + 0.62 * w, h / 2 * 1.05)
    bot_ctrl = (x0 + 0.62 * w, -h / 2 * 1.05)
    top = quad_bezier(back_top, top_ctrl, tip, n)
    bot = quad_bezier(tip, bot_ctrl, back_bot, n)
    back = quad_bezier(back_bot, back_ctrl, back_top, n)
    return np.concatenate([top, bot, back])


def or_back_arc(w=GATE_W, h=GATE_H, n=18, offset=0.14):
    x0 = -w / 2 - offset
    back_top, back_bot = (x0, h / 2), (x0, -h / 2)
    back_ctrl = (x0 + 0.28 * w, 0)
    return quad_bezier(back_bot, back_ctrl, back_top, n)


def triangle_points(w=GATE_W, h=GATE_H):
    return np.array([(-w / 2, h / 2), (-w / 2, -h / 2), (w / 2, 0)])


def to_3d(pts):
    return [np.array([x, y, 0.0]) for x, y in pts]


def make_gate_body(kind):
    """The filled silhouette polygon for a gate 'kind' (and/or/xor/buffer/not,
    without regard to negation -- the bubble is added separately)."""
    if kind == "and":
        pts = and_points()
    elif kind in ("or", "xor"):
        pts = or_points()
    else:  # buffer / not
        pts = triangle_points()
    return Polygon(*to_3d(pts), stroke_color=C_WIRE, stroke_width=4, fill_opacity=0)


GATES = [
    # (name, kind, negated, logic_fn)
    ("OR", "or", False, lambda a, b: a or b),
    ("NOR", "or", True, lambda a, b: not (a or b)),
    ("AND", "and", False, lambda a, b: a and b),
    ("NAND", "and", True, lambda a, b: not (a and b)),
    ("XOR", "xor", False, lambda a, b: a != b),
    ("XNOR", "xor", True, lambda a, b: a == b),
    ("BUFFER", "buffer", False, lambda a, b: a),
    ("NOT", "buffer", True, lambda a, b: not a),
]

STATES = [(0, 0), (1, 0), (1, 1), (0, 1)]   # Gray code: one bit flips per step


class GateCell:
    def __init__(self, name, kind, negated, logic_fn, center):
        self.name, self.kind, self.negated, self.logic_fn = name, kind, negated, logic_fn
        cx, cy = center
        self.center = np.array([cx, cy, 0.0])

        self.body = make_gate_body(kind).shift(self.center)
        parts = [self.body]

        tip_x = self.center[0] + GATE_W / 2
        out_start_x = tip_x
        if negated:
            self.bubble = Circle(radius=0.095, stroke_color=C_BUBBLE_STROKE, stroke_width=3,
                                 fill_color=BLACK, fill_opacity=1)
            self.bubble.move_to([tip_x + 0.095, self.center[1], 0])
            parts.append(self.bubble)
            out_start_x = tip_x + 0.19
        else:
            self.bubble = None

        if kind == "xor":
            extra = Polygon(*to_3d(or_back_arc()), stroke_color=C_WIRE, stroke_width=3.5, fill_opacity=0)
            extra.shift(self.center)
            parts.append(extra)

        back_x = self.center[0] - GATE_W / 2
        y_hi, y_lo = self.center[1] + GATE_H * 0.28, self.center[1] - GATE_H * 0.28
        stub_len = 0.4
        self.in_dots = []
        self.in_stubs = VGroup()
        input_ys = [y_hi, y_lo] if kind != "buffer" else [self.center[1]]
        for y in input_ys:
            stub = Line([back_x - stub_len, y, 0], [back_x, y, 0], color=C_WIRE, stroke_width=3.5)
            dot = Dot([back_x - stub_len, y, 0], radius=0.085, color=C_OFF)
            self.in_stubs.add(stub)
            self.in_dots.append(dot)

        out_stub = Line([out_start_x, self.center[1], 0],
                        [out_start_x + stub_len, self.center[1], 0], color=C_WIRE, stroke_width=3.5)
        self.out_dot = Dot([out_start_x + stub_len, self.center[1], 0], radius=0.085, color=C_OFF)

        label = Text(name, font_size=22, color=C_WIRE, weight=BOLD)
        label.next_to(self.body, DOWN, buff=0.16)

        self.group = VGroup(*parts, self.in_stubs, *self.in_dots, out_stub, self.out_dot, label)

    def plan_update(self, a, b):
        """Compute (once per state!) everything needed to animate this cell's
        reaction to (a, b): the input-dot anims, the output-dot/fill anims,
        and whether the output actually changed from last time. Call this
        exactly once per state -- it has side effects (records the new output
        as "last") so calling it twice for the same state would corrupt the
        changed-detection on the second call."""
        in_vals = [a] if self.kind == "buffer" else [a, b]
        in_anims = [dot.animate.set_fill(C_ON if v else C_OFF, opacity=1)
                    for dot, v in zip(self.in_dots, in_vals)]

        out_val = bool(self.logic_fn(bool(a), bool(b)))
        prev = getattr(self, "_last_out", None)
        changed = prev is not None and prev != out_val
        self._last_out = out_val

        out_color = C_ON if out_val else C_OFF
        out_anim = self.out_dot.animate.set_fill(out_color, opacity=1)
        fill_anim = self.body.animate.set_fill(C_ON, opacity=0.35 if out_val else 0.0)
        return in_anims, fill_anim, out_anim, changed

    def apply_state_instant(self, a, b):
        """Set the cell's colours directly (no animation), so the whole grid
        can start already showing the first input state -- negated gates
        (NOR/NAND/XNOR/NOT) already lit at output=1 for A=0,B=0."""
        in_vals = [a] if self.kind == "buffer" else [a, b]
        for dot, v in zip(self.in_dots, in_vals):
            dot.set_fill(C_ON if v else C_OFF, opacity=1)
        out_val = bool(self.logic_fn(bool(a), bool(b)))
        self._last_out = out_val
        self.out_dot.set_fill(C_ON if out_val else C_OFF, opacity=1)
        self.body.set_fill(C_ON, opacity=0.35 if out_val else 0.0)


class LogicGates(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{L}$ogic $\mathbb{G}$ates", font_size=70)
        title.set_color_by_gradient(PINK, YELLOW, GREEN, TEAL)
        title.move_to(UP * TITLE_Y)

        # ---- shared A / B toggles (start at state (0, 0) -> both OFF) ----
        toggle_a = Circle(radius=0.22, stroke_color=WHITE, stroke_width=4, fill_color=C_OFF, fill_opacity=1)
        toggle_b = Circle(radius=0.22, stroke_color=WHITE, stroke_width=4, fill_color=C_OFF, fill_opacity=1)
        lab_a = Tex("A", font_size=34).next_to(toggle_a, LEFT, buff=0.2)
        lab_b = Tex("B", font_size=34).next_to(toggle_b, LEFT, buff=0.2)
        toggles = VGroup(VGroup(lab_a, toggle_a), VGroup(lab_b, toggle_b)).arrange(RIGHT, buff=1.2)
        toggles.move_to(UP * TOGGLE_Y + LEFT * 1.0)

        readout = MathTex("A{=}0,\\ B{=}0", font_size=38)
        readout.next_to(toggles, RIGHT, buff=0.6)

        # ---- the 8-gate grid ----
        rows = [GATES[0:2], GATES[2:4], GATES[4:6], GATES[6:8]]
        cells = []
        for r, row in enumerate(rows):
            y = GRID_TOP - r * ROW_PITCH
            for c, (name, kind, negated, fn) in enumerate(row):
                x = -COL_X if c == 0 else COL_X
                cells.append(GateCell(name, kind, negated, fn, (x, y)))

        # everything is present from frame one, already showing state (0, 0):
        # NOR / NAND / XNOR / NOT already lit (output = 1)
        prev_a, prev_b = STATES[0]
        for cell in cells:
            cell.apply_state_instant(prev_a, prev_b)
        self.add(title, toggles, readout, *[cell.group for cell in cells])

        # opening beat: pulse the gates that are already ON, so the eye lands
        # on the "negated gates fire on 0,0" idea right away
        on_dots = [cell.out_dot for cell in cells if cell._last_out]
        self.wait(0.5)
        self.play(*[Indicate(d, color=WHITE, scale_factor=1.6) for d in on_dots], run_time=0.7)
        self.wait(0.5)

        for a, b in STATES[1:]:
            # 1. flip whichever toggle changed
            flip_anims = []
            if a != prev_a:
                flip_anims.append(toggle_a.animate.set_fill(C_ON if a else C_OFF, opacity=1))
            if b != prev_b:
                flip_anims.append(toggle_b.animate.set_fill(C_ON if b else C_OFF, opacity=1))
            new_readout = MathTex(f"A{{=}}{a},\\ B{{=}}{b}", font_size=38).move_to(readout)
            self.play(*flip_anims, Transform(readout, new_readout), run_time=0.35)

            # compute each cell's reaction exactly once for this state
            all_in_anims, out_anims, fill_anims, changed_bodies = [], [], [], []
            for cell in cells:
                in_anims, fill_anim, out_anim, changed = cell.plan_update(a, b)
                all_in_anims.extend(in_anims)
                out_anims.append(out_anim)
                fill_anims.append(fill_anim)
                if changed:
                    changed_bodies.append(cell.body)

            # 2. inputs update in sync, then 3. each gate's logic fires a beat later
            self.play(*all_in_anims, run_time=0.3)
            self.play(*out_anims, *fill_anims, run_time=0.4)
            if changed_bodies:
                self.play(*[Indicate(b, color=WHITE, scale_factor=1.08) for b in changed_bodies],
                          run_time=0.45)

            prev_a, prev_b = a, b
            self.wait(0.7)

        self.wait(1.0)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        LogicGates().render()
