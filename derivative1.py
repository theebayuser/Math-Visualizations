from manim import *
import numpy as np


GREEN_C = "#2ECC71"
CYAN_C = "#5DADE2"
RED_C = "#E74C3C"
BLUE_C = "#3498DB"
CREAM_C = "#F7F9F9"
RED = "#E74C3C"
BLUE = "#3498DB"

class DifferentiationConcept(Scene):
    def construct(self):
        
        self.camera.background_color = "#000000"

        
        cancel_template = TexTemplate()
        cancel_template.add_to_preamble(r"\usepackage{cancel}")

        
        title = MathTex(r"\mathbb{L}\text{imit } \mathbb{D}\text{efinition of a } \mathbb{D}\text{erivative}", color=CREAM_C, font_size=40)
        title.set_color_by_gradient(RED, BLUE)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
         
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 12, 2],
            x_length=4.5, y_length=3.0,
            axis_config={"color": CREAM_C, "stroke_width": 2},
        ).next_to(title, DOWN, buff=0.5)
         
        def func(x):
            return -0.1 * x**3 + 1.2 * x**2 - 3*x + 7

        graph = axes.plot(func, color=GREEN_C, x_range=[0.5, 9])
        self.play(Create(axes), Create(graph))
        self.wait(0.5)

        
        x1_val, x2_val = 2.0, 7.0
         
        dot1 = Dot(axes.c2p(x1_val, func(x1_val)), color=RED_C)
        dot2 = Dot(axes.c2p(x2_val, func(x2_val)), color=RED_C)
         
        label1 = MathTex("(x_1, y_1)", color=CREAM_C, font_size=30).next_to(dot1, UL, buff=0.1)
        label2 = MathTex("(x_2, y_2)", color=CREAM_C, font_size=30).next_to(dot2, UP, buff=0.15)

        self.play(Create(dot1), Create(dot2), Write(label1), Write(label2))
        self.wait(0.5)

        point1_coords = dot1.get_center()
        point2_coords = dot2.get_center()
        direction = point2_coords - point1_coords
        extension_factor = 0.5
        secant_line = Line(point1_coords - direction * extension_factor, point2_coords + direction * extension_factor, color=BLUE_C, stroke_width=3)
        self.play(Create(secant_line))
        self.wait(0.5)

        formula_position = DOWN * 2.1
        slope_formula = MathTex(r"\text{Slope} = \frac{y_2 - y_1}{x_2 - x_1}", font_size=36).move_to(formula_position)
        slope_box = SurroundingRectangle(slope_formula, buff=0.2, color=CYAN_C)
        self.play(Write(VGroup(slope_formula, slope_box)))
        self.wait(1)

        
        h_val = x2_val - x1_val
        label1_new = MathTex("(x, f(x))", color=CREAM_C, font_size=30).next_to(dot1, UL, buff=0.1)
        label2_new = MathTex("(x+h, f(x+h))", color=CREAM_C, font_size=30).next_to(dot2, UP, buff=0.15)
        self.play(ReplacementTransform(label1, label1_new), ReplacementTransform(label2, label2_new))
        self.wait(0.5)
         
        lines_1 = axes.get_lines_to_point(dot1.get_center(), color=CREAM_C)
        lines_2 = axes.get_lines_to_point(dot2.get_center(), color=CREAM_C)
         
        x_label = MathTex("x", font_size=28).next_to(axes.c2p(x1_val, 0), DOWN, buff=0.5)
        xh_label = MathTex("x+h", font_size=28).next_to(axes.c2p(x2_val, 0), DOWN, buff=0.5)
         
        self.play(Create(lines_1), Create(lines_2), Write(x_label), Write(xh_label))
         
        brace = Brace(Line(axes.c2p(x1_val, 0), axes.c2p(x2_val, 0)), direction=DOWN, color=CREAM_C)
        h_label = MathTex("h", font_size=28).next_to(brace, DOWN, buff=0.3)
        self.play(GrowFromCenter(brace), Write(h_label))
        self.wait(1)
         
        
        formula_functional_long = MathTex(r"\text{Slope} = \frac{f(x+h) - f(x)}{(x+h) - x}", font_size=36).move_to(formula_position)
        box_long = SurroundingRectangle(formula_functional_long, buff=0.2, color=CYAN_C)
        self.play(ReplacementTransform(slope_formula, formula_functional_long), ReplacementTransform(slope_box, box_long))
        self.wait(1)

        formula_cancelled = MathTex(
            r"\text{Slope} = \frac{f(x+h) - f(x)}{(\cancel{x}+h) - \cancel{x}}",
            font_size=36,
            tex_template=cancel_template
        )
        formula_functional_short = MathTex(r"\text{Slope} = \frac{f(x+h) - f(x)}{h}", font_size=36)

        stable_anchor_point = formula_functional_long.get_part_by_tex("=").get_center()
        
        cancelled_offset = formula_cancelled.get_part_by_tex("=").get_center() - formula_cancelled.get_center()
        short_offset = formula_functional_short.get_part_by_tex("=").get_center() - formula_functional_short.get_center()
        
        formula_cancelled.move_to(stable_anchor_point - cancelled_offset)
        formula_functional_short.move_to(stable_anchor_point - short_offset)
        
        box_short = SurroundingRectangle(formula_functional_short, buff=0.2, color=CYAN_C)

        self.play(TransformMatchingTex(formula_functional_long, formula_cancelled), run_time=0.6)
        
        self.play(
            TransformMatchingTex(formula_cancelled, formula_functional_short),
            Transform(box_long, box_short),
            run_time=0.6
        )
        self.wait(0.5)
         
        
        h_tracker = ValueTracker(h_val)
         
        dot2.add_updater(lambda d: d.move_to(axes.c2p(x1_val + h_tracker.get_value(), func(x1_val + h_tracker.get_value()))))
        
        
        label2_new.add_updater(
            lambda m: m.next_to(dot2, UP, buff=0.15).set_opacity(np.clip(h_tracker.get_value() / 2.0, 0, 1))
        )
        
        lines_2.add_updater(lambda l: l.become(axes.get_lines_to_point(dot2.get_center(), color=CREAM_C)))
         
        xh_label.add_updater(lambda m: m.next_to(axes.c2p(x1_val + h_tracker.get_value(), 0), DOWN, buff=0.5).set_opacity(np.clip(h_tracker.get_value() / 2.0, 0, 1)))
        h_label.add_updater(lambda m: m.next_to(brace, DOWN, buff=0.3).set_opacity(np.clip(h_tracker.get_value() / 2.0, 0, 1)))
        brace.add_updater(lambda b: b.become(Brace(Line(axes.c2p(x1_val, 0), axes.c2p(x1_val + h_tracker.get_value(), 0)), direction=DOWN, color=CREAM_C)).set_opacity(np.clip(h_tracker.get_value() / 2.0, 0, 1)))

        def update_secant_line(s):
            p1 = dot1.get_center()
            p2 = dot2.get_center()
            direction = p2 - p1
            if np.linalg.norm(direction) > 1e-6:
                direction /= np.linalg.norm(direction)
            s.become(Line(p1 - direction * extension_factor * 2, p2 + direction * extension_factor * 2, color=BLUE_C, stroke_width=3))
         
        secant_line.add_updater(update_secant_line)

        self.play(h_tracker.animate.set_value(0.01), run_time=3, rate_func=smooth)
        self.wait(0.5)
         
        mobjects_to_clear = [dot2, label2_new, secant_line, lines_2, xh_label, brace, h_label, x_label]
        for mobj in mobjects_to_clear:
            mobj.clear_updaters(recursive=True)

        
        limit_formula = MathTex(r"\text{Slope} = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}", font_size=40).move_to(formula_position)
        box_final = SurroundingRectangle(limit_formula, buff=0.2, color=CYAN_C)
        self.play(
            ReplacementTransform(formula_functional_short, limit_formula),
            ReplacementTransform(box_long, box_final),
            FadeOut(brace, h_label, lines_2, x_label, xh_label)
        )
        self.wait(0.5)

        
        
        graph_elements = VGroup(
            axes, graph, dot1, dot2, label1_new, label2_new, secant_line, lines_1
        )
        slope_expression = VGroup(limit_formula, box_final)

        
        self.play(FadeOut(graph_elements))
        
        self.play(slope_expression.animate.move_to(ORIGIN))
        self.wait(0.5)

        
        derivative_formula = MathTex(r"\frac{d}{dx}f(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}", font_size=40).move_to(ORIGIN)
        
        derivative_box = SurroundingRectangle(derivative_formula, buff=0.2, color=CYAN_C)

        
        self.play(
            TransformMatchingTex(limit_formula, derivative_formula, key_map={"Slope": r"\frac{d}{dx}f(x)"}),
            ReplacementTransform(box_final, derivative_box)
        )
        self.wait(2)