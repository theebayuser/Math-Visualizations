from manim import *

class TestFixScene(Scene):
    def construct(self):
        # original colors
        color_adj = "#3dc6af"
        color_hyp = "#ff9040"
        color_emp = YELLOW_D
        
        cos_eq0 = MathTex(
            r"\cos", r"\theta", r"=",
            r"\frac{", r"\text{adj}", r"}{", r"\text{hyp}", r"}",
            font_size=28
        )
        cos_eq0[1].set_color(color_emp)
        cos_eq0[4].set_color(color_adj)
        cos_eq0[6].set_color(color_hyp)
        
        self.add(cos_eq0)
        
        cos_eq1 = MathTex(
            r"\text{hyp}", r"\cdot", r"\cos", r"\theta", r"=", r"\text{adj}",
            font_size=28
        )
        cos_eq1[0].set_color(color_hyp)
        cos_eq1[3].set_color(color_emp)
        cos_eq1[5].set_color(color_adj)
        
        cos_eq1.shift(DOWN)
        self.add(cos_eq1)

        self.play(TransformMatchingTex(cos_eq0.copy(), cos_eq1))
        self.wait()
