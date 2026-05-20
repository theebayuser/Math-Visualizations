from manim import *
from graphtheory import EulerHamiltonianShowcase

class DebugScene(EulerHamiltonianShowcase):
    def construct(self):
        try:
            super().construct()
        except Exception as e:
            for i, m in enumerate(self.mobjects):
                if type(m) == Mobject:
                    print(f"[{i}] it's a Mobject! Dict: {m.__dict__}")
                    print(f"[{i}] Submobjects: {m.submobjects}")
