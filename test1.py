from manim import *

class GaussSummationReel(MovingCameraScene):
    """
    A faster, vertically-oriented Manim scene demonstrating the Gauss Summation proof,
    optimized for social media formats like Instagram Reels.
    """
    def construct(self):
        
        
        self.camera.frame.set(width=8)

        
        intro_mobjects = self.play_intro()
        self.play(FadeOut(*intro_mobjects, run_time=0.5))
        self.wait(0.2)

        
        staircase_group, sum_text = self.build_staircase()
        
        
        main_figure = VGroup(staircase_group, sum_text).center().shift(UP * 0.5)
        self.play(FadeIn(main_figure, run_time=0.75))
        
        
        self.play(
            self.camera.frame.animate.scale(0.8).move_to(staircase_group),
            run_time=0.75
        )
        self.wait(0.25)
        
        
        braces_and_labels = self.add_braces(staircase_group)
        self.wait(0.5)

        
        self.play(FadeOut(sum_text, run_time=0.5))
        self.show_area_proof(staircase_group, braces_and_labels)
        
        self.wait(1.5)

    def play_intro(self):
        """Creates the fast-paced introductory animation."""
        
        title = Text("Gauss Summation", font_size=40).set_color_by_gradient(RED_A, PURPLE_A)
        title.to_edge(UP, buff=0.2)

        
        formula = MathTex(r"1 + 2 + \dots + n = \frac{n(n+1)}{2}", font_size=48)
        formula.next_to(title, DOWN, buff=0.5)
        
        why_text = Text("But why?", font_size=36).next_to(formula, DOWN, buff=0.75)

        self.play(Write(title, run_time=1))
        self.play(AddTextLetterByLetter(formula, run_time=1.5))
        self.wait(0.25)
        self.play(Write(why_text, run_time=0.75))
        self.wait(0.75)

        return VGroup(title, formula, why_text)

    def build_staircase(self):
        """Builds the staircase with faster, tighter animations."""
        n = 5
        square_size = 0.4  
        staircase_color = RED_D
        staircase_fill_color = RED_E

        staircase = VGroup()
        origin_point = ORIGIN
        
        
        sum_text = MathTex("1", font_size=36).next_to(origin_point, DOWN, buff=0.3)

        
        col_1 = Square(
            side_length=square_size,
            stroke_color=staircase_color,
            stroke_width=2.5,
            fill_color=staircase_fill_color,
            fill_opacity=0.6
        ).move_to(origin_point, aligned_edge=DL)
        
        staircase.add(VGroup(col_1)) 
        self.play(Create(col_1, run_time=0.3), Write(sum_text, run_time=0.3))
        self.wait(0.1)
        
        prev_column = staircase[0]
        
        
        for i in range(2, n + 1):
            column = VGroup(*[col_1.copy() for _ in range(i)]).arrange(UP, buff=0)
            column.next_to(prev_column, RIGHT, buff=0, aligned_edge=DOWN)
            staircase.add(column)
            prev_column = column
            
            tex_str = f"1+2+\\dots{'' if i < n else '+n'}" if i > 2 else "1+2"
            new_text = MathTex(tex_str, font_size=36).next_to(staircase, DOWN, buff=0.3)
            
            self.play(
                Create(column, run_time=0.3),
                Transform(sum_text, new_text, run_time=0.3)
            )
            self.wait(0.1)

        return staircase, sum_text

    def add_braces(self, staircase_obj):
        """Adds braces and labels to the staircase."""
        brace_b = Brace(staircase_obj, DOWN, buff=0.15)
        n_label_b = brace_b.get_tex("n", font_size=36)
        brace_h = Brace(staircase_obj, RIGHT, buff=0.15)
        n_label_h = brace_h.get_tex("n", font_size=36)
        
        braces_and_labels = VGroup(brace_b, n_label_b, brace_h, n_label_h)
        
        self.play(
            LaggedStart(
                GrowFromCenter(brace_b), Write(n_label_b),
                GrowFromCenter(brace_h), Write(n_label_h),
                lag_ratio=0.4, run_time=1
            )
        )
        return braces_and_labels

    def show_area_proof(self, staircase, braces_and_labels):
        """Shows the visual area proof with snappy animations."""
        bottom_brace = braces_and_labels[0]
        
        
        bl, br, ur = staircase.get_corner(DL), staircase.get_corner(DR), staircase.get_corner(UR)
        
        diagonal = Line(bl, ur, color=WHITE, stroke_width=2)
        large_triangle = Polygon(bl, br, ur, stroke_width=0, fill_color=PURPLE_D, fill_opacity=0.7)
        
        self.play(Create(diagonal), FadeIn(large_triangle), run_time=0.5)
        self.wait(0.2)
        
        
        formula_1 = MathTex(r"\frac{n^2}{2}", font_size=42).next_to(bottom_brace, DOWN, buff=0.3)
        self.play(Write(formula_1))
        self.wait(0.75)
        
        self.play(FadeOut(large_triangle, diagonal), run_time=0.5)
        
        
        half_squares = VGroup(*[
            Polygon(
                s[-1].get_corner(UL), s[-1].get_corner(UR), s[-1].get_corner(DR),
                stroke_width=1, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.8
            ) for s in staircase
        ])
        
        
        self.play(LaggedStart(*[Circumscribe(h, fade_out=True) for h in half_squares], lag_ratio=0.1, run_time=1.5))
        
        formula_2 = MathTex(r"\frac{n^2}{2}", r"+", r"\frac{n}{2}", font_size=42).move_to(formula_1)
        self.play(TransformMatchingTex(formula_1, formula_2))
        self.wait(1)
        
        formula_3 = MathTex(r"\frac{n(n+1)}{2}", font_size=42).move_to(formula_1)
        self.play(TransformMatchingTex(formula_2, formula_3))