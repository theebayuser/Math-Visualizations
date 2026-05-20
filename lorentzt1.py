from manim import *

class Scene2_LightClock(Scene):
    def construct(self):
        # 1. Setup the Mirrors
        mirror_bottom = Line(LEFT, RIGHT, color=LIGHT_GREY).shift(DOWN * 2)
        mirror_top = Line(LEFT, RIGHT, color=LIGHT_GREY).shift(UP * 2)
        mirrors = VGroup(mirror_top, mirror_bottom)
        
        # 2. Setup the Photon
        photon = Dot(color=YELLOW).move_to(mirror_bottom.get_center())
        
        self.play(Create(mirrors), FadeIn(photon))
        
        # 3. Rest Frame (Observer A)
        rest_equation = MathTex(r"\Delta t = \frac{2L}{c}").to_edge(LEFT)
        self.play(Write(rest_equation))
        
        # Photon bounces up and down
        self.play(photon.animate.move_to(mirror_top.get_center()), run_time=1)
        self.play(photon.animate.move_to(mirror_bottom.get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(rest_equation))
        
        # 4. Moving Frame (Observer B)
        # We group them so the mirrors move while the photon bounces
        clock_system = VGroup(mirrors, photon)
        moving_equation = MathTex(r"\Delta t' = \frac{\Delta t}{\sqrt{1-\frac{v^2}{c^2}}}").to_edge(LEFT)
        
        self.play(Write(moving_equation))
        
        # Animate the diagonal bounce (Velocity v to the right)
        # We use a path that creates the diagonal 'D' shape
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