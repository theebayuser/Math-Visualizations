from manim import *

class AMGMProof(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        title = MathTex(r"\text{QM-AM-GM-HM Inequality}", 
                       font_size=44).set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.3)
        
        
        self.add(title)
        
        
        full_inequality = MathTex(
            r"\sqrt{\frac{x^2+y^2}{2}}", r"\geq", r"\frac{x+y}{2}", r"\geq", r"\sqrt{xy}", r"\geq", r"\frac{2}{\frac{1}{x}+\frac{1}{y}}",
            font_size=34, color=WHITE
        )
        full_inequality.move_to(ORIGIN)
        
        
        qm_label = Text("Quadratic Mean", font_size=16, color=ORANGE)
        qm_label.next_to(full_inequality[0], DOWN, buff=0.3)
        
        am_label = Text("Arithmetic Mean", font_size=16, color=GREEN)
        am_label.next_to(full_inequality[2], DOWN, buff=0.3)
        
        gm_label = Text("Geometric Mean", font_size=16, color=PURPLE)
        gm_label.next_to(full_inequality[4], DOWN, buff=0.3)
        
        hm_label = Text("Harmonic Mean", font_size=16, color=TEAL)
        hm_label.next_to(full_inequality[6], DOWN, buff=0.3)
        
        
        self.play(
            Write(full_inequality[0]),
            Write(qm_label),
            run_time=0.5
        )
        
        self.play(Write(full_inequality[1]), run_time=0.2)  
        
        self.play(
            Write(full_inequality[2]),
            Write(am_label),
            run_time=0.5
        )
        
        self.play(Write(full_inequality[3]), run_time=0.2)  
        
        self.play(
            Write(full_inequality[4]),
            Write(gm_label),
            run_time=0.5
        )
        
        self.play(Write(full_inequality[5]), run_time=0.2)  
        
        self.play(
            Write(full_inequality[6]),
            Write(hm_label),
            run_time=0.5
        )
        
        self.wait(0.3)
        
        
        
        am_gm_group = VGroup(full_inequality[2], full_inequality[3], full_inequality[4])
        highlight_box = SurroundingRectangle(am_gm_group, color=YELLOW, buff=0.1, stroke_width=3)
        
        self.play(Create(highlight_box))
        self.wait(0.5)
        
        
        new_title = MathTex(r"\text{AM-GM Inequality}", 
                           font_size=44).set_color_by_gradient(BLUE, RED)
        new_title.to_edge(UP, buff=0.3)
        
        
        self.play(
            FadeOut(full_inequality), FadeOut(highlight_box), 
            FadeOut(qm_label), FadeOut(am_label), FadeOut(gm_label), FadeOut(hm_label),
            Transform(title, new_title),
            run_time=1.0
        )
        
        
        x_val, y_val = 2.0, 1.5
        
        
        rect = Rectangle(width=x_val, height=y_val, 
                        fill_color=BLUE, fill_opacity=0.6, 
                        stroke_color=WHITE, stroke_width=2)
        rect.move_to(ORIGIN + DOWN * 0.2)  
        
        
        x_label = MathTex("x", color=YELLOW, font_size=32)
        x_label.next_to(rect, DOWN, buff=0.3)
        y_label = MathTex("y", color=YELLOW, font_size=32)
        y_label.next_to(rect, LEFT, buff=0.3)
        area_label = MathTex("xy", color=WHITE, font_size=28)
        area_label.move_to(rect.get_center())
        
        
        self.play(Create(rect))
        self.play(Write(x_label), Write(y_label))
        self.play(Write(area_label))
        self.wait(0.5)
        
        
        large_square_side = x_val + y_val
        center_offset = np.array([0, -0.2, 0])  
        
        
        rect1 = Rectangle(width=y_val, height=x_val, 
                         fill_color=BLUE, fill_opacity=0.6, 
                         stroke_color=WHITE, stroke_width=2)
        rect1.move_to(center_offset + np.array([-x_val/2, y_val/2, 0]))
        
        
        rect2 = Rectangle(width=x_val, height=y_val,
                         fill_color=GREEN, fill_opacity=0.6, 
                         stroke_color=WHITE, stroke_width=2)
        rect2.move_to(center_offset + np.array([y_val/2, x_val/2, 0]))
        
        
        rect3 = Rectangle(width=x_val, height=y_val,
                         fill_color=RED, fill_opacity=0.6, 
                         stroke_color=WHITE, stroke_width=2)
        rect3.move_to(center_offset + np.array([-y_val/2, -x_val/2, 0]))
        
        
        rect4 = Rectangle(width=y_val, height=x_val,
                         fill_color=PURPLE, fill_opacity=0.6, 
                         stroke_color=WHITE, stroke_width=2)
        rect4.move_to(center_offset + np.array([x_val/2, -y_val/2, 0]))
        
        
        self.play(
            Transform(rect, rect1),
            FadeIn(rect2),
            FadeIn(rect3),
            FadeIn(rect4),
            FadeOut(x_label), FadeOut(y_label), FadeOut(area_label),
            run_time=1
        )
        self.wait(0.5)
        
        
        xy_label1 = MathTex("xy", color=WHITE, font_size=24)
        xy_label1.move_to(rect1.get_center())
        
        xy_label2 = MathTex("xy", color=WHITE, font_size=24)
        xy_label2.move_to(rect2.get_center())
        
        xy_label3 = MathTex("xy", color=WHITE, font_size=24)
        xy_label3.move_to(rect3.get_center())
        
        xy_label4 = MathTex("xy", color=WHITE, font_size=24)
        xy_label4.move_to(rect4.get_center())
        
        self.play(
            Write(xy_label1),
            Write(xy_label2),
            Write(xy_label3),
            Write(xy_label4),
            run_time=1
        )
        self.wait(0.5)
        
        
        equation_position = UP * 2.4  
        
        
        plus1 = MathTex("+", color=WHITE, font_size=32)
        plus2 = MathTex("+", color=WHITE, font_size=32)
        plus3 = MathTex("+", color=WHITE, font_size=32)
        
        
        equation_group = VGroup(
            MathTex("xy", color=WHITE, font_size=32),
            plus1,
            MathTex("xy", color=WHITE, font_size=32),
            plus2,
            MathTex("xy", color=WHITE, font_size=32),
            plus3,
            MathTex("xy", color=WHITE, font_size=32)
        )
        equation_group.arrange(RIGHT, buff=0.3)
        equation_group.move_to(equation_position)
        
        
        self.play(
            xy_label1.animate.move_to(equation_group[0].get_center()),
            xy_label2.animate.move_to(equation_group[2].get_center()),
            xy_label3.animate.move_to(equation_group[4].get_center()),
            xy_label4.animate.move_to(equation_group[6].get_center()),
            Write(plus1.move_to(equation_group[1].get_center())),
            Write(plus2.move_to(equation_group[3].get_center())),
            Write(plus3.move_to(equation_group[5].get_center())),
            run_time=1
        )
        self.wait(0.5)
        
        
        equation_4xy = MathTex("4xy", color=WHITE, font_size=32)
        equation_4xy.move_to(equation_position)
        
        
        combined_labels = VGroup(xy_label1, xy_label2, xy_label3, xy_label4)
        old_equation = VGroup(xy_label1, xy_label2, xy_label3, xy_label4, plus1, plus2, plus3)
        
        self.play(
            ReplacementTransform(old_equation, equation_4xy),
            run_time=1
        )
        self.wait(0.3)
        
        
        top_position = UP * 2.8  
        area_4xy_eq = MathTex("\\text{Area} = 4xy", color=WHITE, font_size=32)
        area_4xy_eq.move_to(top_position)
        
        
        
        highlight1 = Rectangle(width=rect.get_width(), height=rect.get_height(),
                              fill_color=WHITE, fill_opacity=0.2, stroke_width=0)
        highlight1.move_to(rect.get_center())
        
        highlight2 = Rectangle(width=rect2.get_width(), height=rect2.get_height(),
                              fill_color=WHITE, fill_opacity=0.2, stroke_width=0)
        highlight2.move_to(rect2.get_center())
        
        highlight3 = Rectangle(width=rect3.get_width(), height=rect3.get_height(),
                              fill_color=WHITE, fill_opacity=0.2, stroke_width=0)
        highlight3.move_to(rect3.get_center())
        
        highlight4 = Rectangle(width=rect4.get_width(), height=rect4.get_height(),
                              fill_color=WHITE, fill_opacity=0.2, stroke_width=0)
        highlight4.move_to(rect4.get_center())
        
        rect_highlights = VGroup(highlight1, highlight2, highlight3, highlight4)
        
        self.play(
            Transform(equation_4xy, area_4xy_eq),
            Create(rect_highlights),
            run_time=1.0
        )
        self.wait(0.5)
        self.play(FadeOut(rect_highlights), run_time=0.4)
        
        
        area_outer_eq = MathTex("\\text{Area} = (x+y)^2", color=WHITE, font_size=32)
        area_outer_eq.move_to(top_position + DOWN * 0.6)
        
        
        bottom_label = MathTex("x+y", color=YELLOW, font_size=28)
        bottom_label.next_to(VGroup(rect3, rect4), DOWN, buff=0.3)
        
        right_label = MathTex("x+y", color=YELLOW, font_size=28)
        right_label.next_to(VGroup(rect2, rect4), RIGHT, buff=0.3)
        
        
        all_rectangles = VGroup(rect, rect2, rect3, rect4)
        highlight_total_area = Rectangle(
            width=all_rectangles.get_width() + 0.2,
            height=all_rectangles.get_height() + 0.2,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=0
        )
        highlight_total_area.move_to(all_rectangles.get_center())
        
        self.play(
            Write(area_outer_eq),
            Write(bottom_label), 
            Write(right_label),
            Create(highlight_total_area),
            run_time=1.0
        )
        self.wait(0.5)
        
        self.play(FadeOut(highlight_total_area), run_time=0.4)
        
        
        inner_square_side = abs(x_val - y_val)
        inner_square = Square(side_length=inner_square_side,
                             fill_color=YELLOW, fill_opacity=0.4,
                             stroke_color=YELLOW, stroke_width=3)
        
        inner_square.move_to(all_rectangles.get_center())
        
        
        inner_label = MathTex("|x-y|", color=YELLOW, font_size=24)  
        inner_label.move_to(inner_square.get_center() + DOWN * 0.5)
        
        
        area_combined_eq = MathTex("\\text{Area} = (x+y)^2 - |x-y|^2", color=WHITE, font_size=32)
        area_combined_eq.move_to(area_outer_eq.get_center())
        
        self.play(
            Create(inner_square),
            Write(inner_label),
            Transform(area_outer_eq, area_combined_eq),
            run_time=0.8
        )
        self.wait(0.4)
        
        
        combined_eq = MathTex("4xy = (x+y)^2 - |x-y|^2", color=WHITE, font_size=32)
        combined_eq.move_to(UP * 2.8)  
        
        self.play(
            ReplacementTransform(VGroup(equation_4xy, area_outer_eq), combined_eq),
            FadeOut(bottom_label),
            FadeOut(right_label),
            FadeOut(inner_label),
            run_time=1.0
        )
        self.wait(0.5)
        
        
        stipulation = MathTex("|x-y|^2 \\geq 0", color=ORANGE, font_size=28)
        stipulation.move_to(UP * 2.2)  
        
        self.play(Write(stipulation), run_time=0.6)
        self.wait(0.5)
        
        
        inequality_eq = MathTex("4xy \\leq (x+y)^2", color=WHITE, font_size=32)
        inequality_eq.move_to(combined_eq.get_center())
        
        self.play(
            Transform(combined_eq, inequality_eq),
            FadeOut(stipulation),
            run_time=0.5
        )
        self.wait(0.3)
        
        
        center_position = ORIGIN
        larger_inequality = MathTex("4xy \\leq (x+y)^2", color=WHITE, font_size=36)
        larger_inequality.move_to(center_position)
        
        fade_objects = [rect, rect2, rect3, rect4, inner_square]
        self.play(
            *[FadeOut(obj) for obj in fade_objects],
            Transform(combined_eq, larger_inequality),
            run_time=0.8
        )
        self.wait(0.3)
        
        
        sqrt_both_sides = MathTex("\\sqrt{4xy} \\leq \\sqrt{(x+y)^2}", color=WHITE, font_size=36)
        sqrt_both_sides.move_to(center_position)
        
        self.play(Transform(combined_eq, sqrt_both_sides), run_time=1)
        self.wait(0.3)
        
        
        simplified_sqrt = MathTex("2\\sqrt{xy} \\leq x+y", color=WHITE, font_size=36)
        simplified_sqrt.move_to(center_position)
        
        self.play(Transform(combined_eq, simplified_sqrt), run_time=1)
        self.wait(0.3)
        
        
        final_equation = MathTex("\\sqrt{xy} \\leq \\frac{x+y}{2}", color=BLUE, font_size=42)
        final_equation.move_to(center_position)
        
        
        highlight_box_final = SurroundingRectangle(
            final_equation, 
            color=TEAL, 
            buff=0.3, 
            stroke_width=4,
            corner_radius=0.1
        )
        
        
        step1 = MathTex("2\\sqrt{xy} \\leq x+y", color=WHITE, font_size=36)
        step1.move_to(center_position)
        
        step2 = MathTex("\\sqrt{xy} \\leq \\frac{x+y}{2}", color=WHITE, font_size=40)
        step2.move_to(center_position)
        
        step3 = MathTex("\\sqrt{xy} \\leq \\frac{x+y}{2}", color=TEAL, font_size=42)
        step3.move_to(center_position)
        
        
        self.play(
            Transform(combined_eq, step2),
            FadeOut(title),
            run_time=1
        )
        self.wait(0.2)
        
        self.play(
            Transform(combined_eq, step3),
            combined_eq.animate.set_color_by_gradient(TEAL, BLUE),
            Create(highlight_box_final),
            run_time=1
        )
        
        
        final_group = VGroup(combined_eq, highlight_box_final)
        self.play(
            final_group.animate.scale(1.1),
            run_time=0.6,
            rate_func=there_and_back
        )
        
        self.wait(1)
        
        
        self.play(
            final_group.animate.scale(0.8).set_opacity(0),
            run_time=1.2
        )
        
        self.wait(0.3)