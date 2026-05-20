from manim import *

class TestScene(Scene):
    def construct(self):
        cos_eq0 = MathTex(
            r"\cos", r"\theta", r"=",
            r"\frac{{\color{%s}\text{adj}}}{{\color{%s}\text{hyp}}}" % ("3dc6af", "ff9040"),
            font_size=28
        )
        self.play(Write(cos_eq0))
