from manim import *

class TestFix(Scene):
    def construct(self):
        # We add spaces to disable brace splitting, OR put 3 braces, OR use xcolor!
        # Remember the template doesn't load xcolor, so wait... how to use hex colors?
        # Let's use set_color_by_tex or [x].set_color() instead!
        cos_eq0 = MathTex(
            r"\cos", r"\theta", r"=",
            r"\frac{\text{adj}}{\text{hyp}}",
            font_size=28
        )
        cos_eq0[1].set_color(YELLOW_D)
        
        # In manim you can color specific substrings if they are isolated.
        # But wait, the original code had:
        # r"\frac{{\color{%s}\text{adj}}}{{\color{%s}\text{hyp}}}" % ("3dc6af", "ff9040")
        pass
