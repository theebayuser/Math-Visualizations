"""
Eulerian & Hamiltonian — Path then Cycle
One-block executable for VSCode.

Run:
    manim -pql euler_vs_hamiltonian.py EulerHamiltonianShowcase
    manim -pqh euler_vs_hamiltonian.py EulerHamiltonianShowcase
"""

from manim import *
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# PALETTE
# ══════════════════════════════════════════════════════════════════════════════
BG        = BLACK
EULER_C   = "#00C8FF"   # sky-blue  — Eulerian  (all text this color)
HAM_C     = "#FF6060"   # coral-red — Hamiltonian (all text this color)

BASE_EDGE = WHITE       # unused edges are white
DIM_OP    = 0.12        # opacity of base edge after traversal
NODE_FILL = "#111122"

# Vertical shift applied to everything except titles
CONTENT_SHIFT_Y = 0.10

# ══════════════════════════════════════════════════════════════════════════════
# GRAPH LAYOUTS
# ══════════════════════════════════════════════════════════════════════════════
N = 5

def wheel_pos(cx=0.0, cy=0.0, r=1.25):
    """Node 0 at center; nodes 1–4 at corners of an axis-aligned square."""
    pts = [np.array([cx, cy, 0.0])]
    for i in range(4):
        angle = np.pi / 4 + i * np.pi / 2
        pts.append(np.array([cx + r * np.cos(angle),
                              cy + r * np.sin(angle), 0.0]))
    return pts

def penta_pos(cx=0.0, cy=0.0, r=1.30):
    """Standard regular pentagon."""
    return [
        np.array([cx + r * np.cos(np.pi/2 + 2*np.pi*i/N),
                  cy + r * np.sin(np.pi/2 + 2*np.pi*i/N), 0.0])
        for i in range(N)
    ]

ALL_EDGES = [(i, j) for i in range(N) for j in range(i+1, N)]

def eidx(a, b):
    if a > b: a, b = b, a
    return ALL_EDGES.index((a, b))

# ── Traversal sequences ────────────────────────────────────────────────────
EULER_CIRCUIT = [
    (0,1),(1,2),(2,3),(3,4),(4,0),
    (0,2),(2,4),(4,1),(1,3),(3,0),
]
EULER_PATH = EULER_CIRCUIT[:-1]   # drop last edge → open walk

HAM_PATH  = [(0,1),(1,2),(2,3),(3,4)]
HAM_CYCLE = [(0,1),(1,2),(2,3),(3,4),(4,0)]

NODE_NAMES = ["A", "B", "C", "D", "E"]

WHEEL_OFFSETS = [
    LEFT  * 0.28,
    UP    * 0.28 + RIGHT * 0.18,
    DOWN  * 0.28 + RIGHT * 0.18,
    DOWN  * 0.28 + LEFT  * 0.18,
    UP    * 0.28 + LEFT  * 0.18,
]
PENTA_OFFSETS = [
    UP    * 0.30,
    RIGHT * 0.32,
    RIGHT * 0.30 + DOWN * 0.10,
    LEFT  * 0.30 + DOWN * 0.10,
    LEFT  * 0.32,
]


# ══════════════════════════════════════════════════════════════════════════════
class EulerHamiltonianShowcase(Scene):
# ══════════════════════════════════════════════════════════════════════════════

    def construct(self):
        self.camera.background_color = BG

        # Graph centers — sides pulled close together
        LX = -1.85
        RX =  1.85
        # Title centre Y ≈ 3.35, box centre Y ≈ BOX_Y below.
        # Graph centre sits midway between them.
        GY = 0.70   # vertically centered between title and bottom box

        lpos = penta_pos(LX, GY)
        rpos = penta_pos(RX, GY)

        lgraph = self._build_graph(lpos, EULER_C)
        rgraph = self._build_graph(rpos, HAM_C)

        l_nlbls = self._node_labels(lpos, EULER_C, PENTA_OFFSETS)
        r_nlbls = self._node_labels(rpos, HAM_C,   PENTA_OFFSETS)

        # Titles — fixed near top
        TY = 3.35
        t_euler = self._title("Eulerian Path",    EULER_C, LX, TY)
        t_ham   = self._title("Hamiltonian Path", HAM_C,   RX, TY)

        # Bottom boxes — sit below the graph
        BOX_Y = -2.00 + CONTENT_SHIFT_Y   # ≈ -1.90

        box_l = self._box(
            ["Traverse every edge exactly once"],
            EULER_C, LX, BOX_Y
        )
        box_r = self._box(
            ["Visit every vertex exactly once"],
            HAM_C, RX, BOX_Y
        )

        # ── Everything appears immediately ────────────────────────────────────
        self.add(
            *lgraph["edges"], *rgraph["edges"],
            *lgraph["nodes"], *rgraph["nodes"],
            *l_nlbls, *r_nlbls,
            t_euler, t_ham,
            box_l, box_r,
        )
        self.wait(0.5)

        # ══ PHASE 1: Eulerian Path  +  Hamiltonian Path ═══════════════════════
        l_hls, r_hls = self._animate_dual(
            lpos, lgraph, EULER_PATH,  False, EULER_C,
            rpos, rgraph, HAM_PATH,    True,  HAM_C,
        )
        self.wait(1.2)

        # ══ TRANSITION → Circuit / Cycle ══════════════════════════════════════
        t_euler2 = self._title("Eulerian Circuit",  EULER_C, LX, TY)
        t_ham2   = self._title("Hamiltonian Cycle", HAM_C,   RX, TY)  # LX/RX already in scope

        box_l2 = self._box(
            ["Traverse all edges exactly once",
             "begin and end at same vertex"],
            EULER_C, LX, BOX_Y
        )
        box_r2 = self._box(
            ["Visit every vertex exactly once",
             "begin and end at same vertex"],
            HAM_C, RX, BOX_Y
        )

        self.play(
            ReplacementTransform(t_euler, t_euler2),
            ReplacementTransform(t_ham,   t_ham2),
            ReplacementTransform(box_l,   box_l2),
            ReplacementTransform(box_r,   box_r2),
            *[FadeOut(h) for h in l_hls],
            *[FadeOut(h) for h in r_hls],
            *[e.animate.set_stroke(WHITE, opacity=0.55) for e in lgraph["edges"]],
            *[e.animate.set_stroke(WHITE, opacity=0.55) for e in rgraph["edges"]],
            *[n.animate.set_fill(NODE_FILL)  for n in lgraph["nodes"]],
            *[n.animate.set_fill(NODE_FILL)  for n in rgraph["nodes"]],
            run_time=0.65,
        )

        # ══ PHASE 2: Eulerian Circuit  +  Hamiltonian Cycle ═══════════════════
        _, _ = self._animate_dual(
            lpos, lgraph, EULER_CIRCUIT, False, EULER_C,
            rpos, rgraph, HAM_CYCLE,     True,  HAM_C,
        )

        # Pulse start nodes to show "returned home"
        self.play(
            lgraph["nodes"][EULER_CIRCUIT[0][0]].animate
                .scale(1.5).set_fill(EULER_C).set_stroke(WHITE, width=3),
            rgraph["nodes"][HAM_CYCLE[0][0]].animate
                .scale(1.5).set_fill(HAM_C).set_stroke(WHITE, width=3),
            run_time=0.35,
        )
        self.play(
            lgraph["nodes"][EULER_CIRCUIT[0][0]].animate
                .scale(1/1.5).set_stroke(EULER_C, width=2.2),
            rgraph["nodes"][HAM_CYCLE[0][0]].animate
                .scale(1/1.5).set_stroke(HAM_C, width=2.2),
            run_time=0.35,
        )
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    # ══════════════════════════════════════════════════════════════════════════
    # DUAL ANIMATION
    # ══════════════════════════════════════════════════════════════════════════
    def _animate_dual(
        self,
        lpos, lg, l_edges, is_node_mode_l, col_l,
        rpos, rg, r_edges, is_node_mode_r, col_r,
    ):
        STEP = 0.46

        def make_hls(pos, seq, c):
            return [Line(pos[a], pos[b], stroke_color=c,
                         stroke_width=5.5, z_index=5)
                    for (a, b) in seq]

        lhls = make_hls(lpos, l_edges, col_l)
        rhls = make_hls(rpos, r_edges, col_r)

        lc = Dot(lpos[l_edges[0][0]], radius=0.17, color=col_l, z_index=10)
        rc = Dot(rpos[r_edges[0][0]], radius=0.17, color=col_r, z_index=10)
        lg["nodes"][l_edges[0][0]].set_fill(col_l)
        rg["nodes"][r_edges[0][0]].set_fill(col_r)
        self.add(lc, rc)

        max_steps = max(len(lhls), len(rhls))
        for step in range(max_steps):
            anims = []

            if step < len(lhls):
                ei, ej = l_edges[step]
                base_l = lg["edges"][eidx(ei, ej)]
                anims += [
                    Create(lhls[step], run_time=STEP),
                    lc.animate(run_time=STEP).move_to(lpos[ej]),
                    base_l.animate(run_time=STEP).set_stroke(opacity=DIM_OP),
                ]
                if is_node_mode_l:
                    anims.append(
                        lg["nodes"][ej % N].animate(run_time=STEP)
                        .set_fill(col_l).set_stroke(col_l, width=2.5)
                    )

            if step < len(rhls):
                ei, ej = r_edges[step]
                base_r = rg["edges"][eidx(ei, ej % N)]
                anims += [
                    Create(rhls[step], run_time=STEP),
                    rc.animate(run_time=STEP).move_to(rpos[ej % N]),
                    base_r.animate(run_time=STEP).set_stroke(opacity=DIM_OP),
                ]
                if is_node_mode_r:
                    anims.append(
                        rg["nodes"][ej % N].animate(run_time=STEP)
                        .set_fill(col_r).set_stroke(col_r, width=2.5)
                    )

            if anims:
                self.play(*anims, run_time=STEP)

        self.play(FadeOut(lc), FadeOut(rc), run_time=0.2)
        return lhls, rhls

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    def _title(self, text, col, cx, cy):
        """
        \mathbb{First} + \text{rest}, both in col, baseline-aligned.
        The mathbb glyph sits slightly high in TeX; we nudge it down manually.
        """
        first = text[0]
        rest  = text[1:]

        bb   = MathTex(rf"\mathbb{{{first}}}", color=col, font_size=46)
        body = MathTex(rf"\text{{{rest}}}",    color=col, font_size=38)

        # Arrange right, then correct the mathbb vertical drift
        grp = VGroup(bb, body).arrange(RIGHT, buff=0.07)

        # Align both to a common baseline: snap bottoms, then shift bb down
        # so its cap-height aligns with the text capline rather than floating.
        body_bottom = body.get_bottom()[1]
        bb_bottom   = bb.get_bottom()[1]
        bb.shift(DOWN * (bb_bottom - body_bottom))   # level the bottoms first
        # Then push bb up just a touch so the letter sits on the same cap line
        # (mathbb cap > text cap by roughly this amount at these font sizes)
        bb.shift(UP * 0.03)

        grp.move_to([cx, cy, 0])
        return grp

    def _build_graph(self, positions, accent):
        nodes, edges = [], []
        for pos in positions:
            c = Circle(radius=0.12)
            c.set_fill(NODE_FILL, opacity=1)
            c.set_stroke(accent, width=2.2)
            c.move_to(pos)
            nodes.append(c)
        for (i, j) in ALL_EDGES:
            ln = Line(positions[i], positions[j],
                      stroke_color=BASE_EDGE,   # WHITE
                      stroke_width=1.5,
                      stroke_opacity=0.55)      # slightly dimmed so traversal pop is clear
            edges.append(ln)
        return {"nodes": nodes, "edges": edges}

    def _node_labels(self, positions, col, offsets):
        labels = []
        for i, (pos, off) in enumerate(zip(positions, offsets)):
            lbl = MathTex(NODE_NAMES[i], color=col, font_size=22)
            lbl.move_to(pos + off)
            labels.append(lbl)
        return labels

    def _box(self, lines_list, col, cx, cy):
        """
        Bottom box: one or two plain-text lines, centered, in col.
        lines_list: list of strings (1 or 2 items).
        """
        text_mobs = [Text(s, font_size=15, color=col) for s in lines_list]
        content   = VGroup(*text_mobs).arrange(DOWN, buff=0.13, aligned_edge=LEFT)

        box = SurroundingRectangle(
            content, color=col, buff=0.22,
            corner_radius=0.14, stroke_width=1.8,
        )
        box.set_fill(BLACK, opacity=0.88)
        grp = VGroup(box, content).move_to([cx, cy, 0])
        return grp