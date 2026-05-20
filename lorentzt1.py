from manim import *

class Scene2_LightClock(Scene):
    def construct(self):
        
        mirror_bottom = Line(LEFT, RIGHT, color=LIGHT_GREY).shift(DOWN * 2)
        mirror_top = Line(LEFT, RIGHT, color=LIGHT_GREY).shift(UP * 2)
        mirrors = VGroup(mirror_top, mirror_bottom)
        
        
        photon = Dot(color=YELLOW).move_to(mirror_bottom.get_center())
        
        self.play(Create(mirrors), FadeIn(photon))
        
        
        rest_equation = MathTex(r"\Delta t = \frac{2L}{c}").to_edge(LEFT)
        self.play(Write(rest_equation))
        
        
        self.play(photon.animate.move_to(mirror_top.get_center()), run_time=1)
        self.play(photon.animate.move_to(mirror_bottom.get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(rest_equation))
        
        
        
        clock_system = VGroup(mirrors, photon)
        moving_equation = MathTex(r"\Delta t' = \frac{\Delta t}{\sqrt{1-\frac{v^2}{c^2}}}").to_edge(LEFT)
        
        self.play(Write(moving_equation))
        
        
        
        target_top = mirror_top.get_center() + RIGHT * 2
        target_bottom = mirror_bottom.get_center() + RIGHT * 4
        
        self.play(
            mirrors.animate.shift(RIGHT * 2),
            photon.animate.move_to(target_top),
            run_time=1.5,
            rate_func=linear
        )
        self.play(
            mirrors.animate.shift(RIGHT * 2),
            photon.animate.move_to(target_bottom),
            run_time=1.5,
            rate_func=linear
        )
        
        self.wait(2)