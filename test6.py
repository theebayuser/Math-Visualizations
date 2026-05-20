from manim import *

class LawOfCosines(Scene):
    def construct(self):
        # 1. Title with mathbb first letters and Gradient
        title = MathTex(r"\mathbb{L}\text{aw of }\mathbb{C}\text{osines}", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.75)
        self.play(Write(title), run_time=1.5)

        # 2. Geometric Setup (Confined to Middle Third)
        # Shifted up slightly to leave lower half for derivation equations
        A_pos = np.array([-1.5, 0.8, 0])
        B_pos = np.array([1.5, 0.8, 0])
        C_pos = np.array([-0.2, 2.5, 0])
        H_pos = np.array([-0.2, 0.8, 0])

        triangle = Polygon(A_pos, B_pos, C_pos, color=BLUE, stroke_width=5)
        
        lbl_A = MathTex("A", font_size=30).next_to(A_pos, DOWN+LEFT, buff=0.1)
        lbl_B = MathTex("B", font_size=30).next_to(B_pos, DOWN+RIGHT, buff=0.1)
        lbl_C = MathTex("C", font_size=30).next_to(C_pos, UP, buff=0.1)
        
        lbl_a = MathTex("a", font_size=32).next_to(Line(C_pos, B_pos).get_center(), UP+RIGHT, buff=0.1)
        lbl_b = MathTex("b", font_size=32).next_to(Line(A_pos, C_pos).get_center(), UP+LEFT, buff=0.1)
        lbl_c = MathTex("c", font_size=32).next_to(Line(A_pos, B_pos).get_center(), DOWN, buff=0.1)

        self.play(
            Create(triangle), 
            FadeIn(VGroup(lbl_A, lbl_B, lbl_C, lbl_a, lbl_b, lbl_c)), 
            run_time=1.5
        )

        # 3. Drop Height and Split the Base
        h_line = DashedLine(C_pos, H_pos, color=YELLOW)
        lbl_h = MathTex("h", font_size=32, color=YELLOW).next_to(h_line, RIGHT, buff=0.1)
        
        lbl_x = MathTex("x", font_size=32).next_to(Line(A_pos, H_pos).get_center(), DOWN, buff=0.1)
        lbl_cx = MathTex("c-x", font_size=32).next_to(Line(H_pos, B_pos).get_center(), DOWN, buff=0.1)
        
        self.play(Create(h_line), FadeIn(lbl_h), run_time=1)
        self.play(ReplacementTransform(lbl_c, VGroup(lbl_x, lbl_cx)), run_time=1)

        # 4. Derivation Equations (Stepping down vertically)
        math_kwargs = {"font_size": 36}
        
        eq1 = MathTex(r"\cos A = \frac{x}{b} \implies x = b \cos A", **math_kwargs).shift(DOWN * 0.2)
        eq2_left = MathTex(r"h^2 = b^2 - x^2", **math_kwargs).shift(DOWN * 1.2)
        eq2_right = MathTex(r"a^2 = h^2 + (c-x)^2", **math_kwargs).shift(DOWN * 2.2)

        # Initial Pythagorean setups
        self.play(Write(eq1), run_time=1.5)
        self.play(Write(eq2_left), run_time=1.5)
        self.play(Write(eq2_right), run_time=1.5)

        self.wait(0.5)

        # 5. Substitution 1: Replace h^2
        eq3 = MathTex(r"a^2 = (b^2 - x^2) + (c^2 - 2cx + x^2)", **math_kwargs).move_to(eq2_right.get_center())
        self.play(
            ReplacementTransform(eq2_right, eq3), 
            Indicate(eq2_left, color=YELLOW), 
            run_time=1.5
        )
        self.wait(0.5)

        # 6. Cancellation of x^2 terms
        eq4 = MathTex(r"a^2 = b^2 + c^2 - 2cx", **math_kwargs).move_to(eq3.get_center())
        self.play(ReplacementTransform(eq3, eq4), run_time=1.5)
        self.wait(0.5)

        # 7. Final Substitution: Replace x with b*cos(A)
        eq5 = MathTex(r"a^2 = b^2 + c^2 - 2bc \cos A", font_size=40, color=YELLOW).move_to(eq4.get_center())
        final_box = SurroundingRectangle(eq5, color=RED, buff=0.2).add_background_rectangle(opacity=0.1)
        
        self.play(
            ReplacementTransform(eq4, eq5), 
            Indicate(eq1, color=YELLOW), 
            run_time=1.5
        )
        self.play(Create(final_box), run_time=1)
        
        # Hold on screen
        self.wait(2.5)