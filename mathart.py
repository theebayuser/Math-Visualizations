from manim import *
import math
import numpy as np

class MathArtShowcase(Scene):
    def construct(self):
        title = Tex("Parameterized Functions", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        a_tracker = ValueTracker(-20.0)

        def get_a_label():
            val = a_tracker.get_value()
            txt = Tex(f"$a = {val:.1f}$", font_size=32, color=YELLOW)
            box = RoundedRectangle(
                corner_radius=0.2, fill_color=BLACK, fill_opacity=0.85, 
                stroke_color=WHITE, stroke_opacity=0.3, stroke_width=1
            )
            box.surround(txt, buff=0.2)
            return VGroup(box, txt).move_to(DOWN * 2.7)

        a_label = always_redraw(get_a_label)

        axes1 = NumberPlane(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], 
            x_length=4.2, y_length=4.2,
            background_line_style={"stroke_opacity": 0.15},
            axis_config={"stroke_opacity": 0.3, "include_ticks": False}
        ).move_to(ORIGIN)

        eq1_txt = MathTex(r"r = \sin\left(\frac{a}{5}\theta\right)", font_size=36, color=WHITE)
        eq1_box = RoundedRectangle(corner_radius=0.2, fill_color=BLACK, fill_opacity=0.85, stroke_opacity=0)
        eq1_box.surround(eq1_txt, buff=0.2)
        eq1 = VGroup(eq1_box, eq1_txt).move_to(UP * 2.3)

        def get_curve1():
            c = axes1.plot_parametric_curve(
                lambda t: np.array([
                    np.sin((a_tracker.get_value() / 5) * t) * np.cos(t),
                    np.sin((a_tracker.get_value() / 5) * t) * np.sin(t),
                    0
                ]),
                t_range=[0, 10 * PI, 0.05]
            )
            # Map hue to parameter 'a' for new range [-20, 20]
            alpha = (a_tracker.get_value() + 20) / 40
            base_color = interpolate_color(BLUE, PURPLE, alpha)
            c.set_color_by_gradient(base_color, WHITE)
            return c

        curve1 = always_redraw(get_curve1)

        self.play(FadeIn(axes1), FadeIn(eq1), FadeIn(a_label), Create(curve1), run_time=1.0)
        # Extended run time for slower parametrization (keeping total under 25s)
        self.play(a_tracker.animate.set_value(20.0), run_time=6.5, rate_func=linear)
        self.play(FadeOut(axes1), FadeOut(eq1), FadeOut(curve1), run_time=0.4)

        a_tracker.set_value(-30.0)
        
        axes2 = NumberPlane(
            x_range=[0, 3], y_range=[-2, 2], 
            x_length=4.2, y_length=4.2,
            background_line_style={"stroke_opacity": 0.15},
            axis_config={"stroke_opacity": 0.3}
        ).move_to(ORIGIN)

        eq2_txt = MathTex(r"y = x\sin(\ln(a!x))", font_size=36, color=WHITE)
        eq2_box = RoundedRectangle(corner_radius=0.2, fill_color=BLACK, fill_opacity=0.85, stroke_opacity=0)
        eq2_box.surround(eq2_txt, buff=0.2)
        eq2 = VGroup(eq2_box, eq2_txt).move_to(UP * 2.3)

        def get_curve2():
            def safe_gamma_ln(val, x_val):
                factorial_approx = math.gamma(abs(val) + 1)
                return x_val * np.sin(np.log(max(factorial_approx * x_val, 1e-9)))
            
            c = axes2.plot(lambda x: safe_gamma_ln(a_tracker.get_value(), x), x_range=[0.001, 3, 0.01])
            # Map hue to parameter 'a' for new range [-30, 30]
            alpha = (a_tracker.get_value() + 30) / 60
            base_color = interpolate_color(TEAL, ORANGE, alpha)
            c.set_color_by_gradient(base_color, WHITE)
            return c

        curve2 = always_redraw(get_curve2)

        self.play(FadeIn(axes2), FadeIn(eq2), Create(curve2), run_time=1.0)
        self.play(a_tracker.animate.set_value(30.0), run_time=6.5, rate_func=linear)
        self.play(FadeOut(axes2), FadeOut(eq2), FadeOut(curve2), run_time=0.4)

        a_tracker.set_value(-50.0)
        
        axes3 = NumberPlane(
            x_range=[-3, 3], y_range=[-55, 55], 
            x_length=4.2, y_length=4.2,
            background_line_style={"stroke_opacity": 0.15},
            axis_config={"stroke_opacity": 0.3}
        ).move_to(ORIGIN)

        eq3_txt = MathTex(r"y = \sin(ax) + a\sin(x)", font_size=36, color=WHITE)
        eq3_box = RoundedRectangle(corner_radius=0.2, fill_color=BLACK, fill_opacity=0.85, stroke_opacity=0)
        eq3_box.surround(eq3_txt, buff=0.2)
        eq3 = VGroup(eq3_box, eq3_txt).move_to(UP * 2.3)

        def get_curve3():
            c = axes3.plot(
                lambda x: np.sin(a_tracker.get_value() * x) + a_tracker.get_value() * np.sin(x),
                x_range=[-3, 3, 0.02]
            )
            alpha = (a_tracker.get_value() + 50) / 100
            base_color = interpolate_color(PINK, YELLOW, alpha)
            c.set_color_by_gradient(base_color, WHITE)
            return c

        curve3 = always_redraw(get_curve3)

        self.play(FadeIn(axes3), FadeIn(eq3), Create(curve3), run_time=1.0)
        self.play(a_tracker.animate.set_value(50.0), run_time=6.5, rate_func=linear)
        
        # Smooth Outro
        self.play(FadeOut(axes3), FadeOut(eq3), FadeOut(curve3), FadeOut(a_label), FadeOut(title), run_time=0.7)