from manim import *
from graphtheory import build_graph_mobjects, node_label, NODE_NAMES, \
    EP_POSITIONS_RAW, EP_EDGES, EP_TRAVERSAL, \
    HP_POSITIONS_RAW, HP_EDGES, HP_TRAVERSAL_NODES, \
    shift_positions, EULER_C, HAM_C, EulerHamiltonianShowcase, BG

class DebugScene(EulerHamiltonianShowcase):
    def construct(self):
        try:
            super().construct()
        except Exception as e:
            for i, m in enumerate(self.mobjects):
                print(f"[{i}] type: {type(m)}, object: {m}")
