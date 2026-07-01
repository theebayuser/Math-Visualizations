from manim import *

config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

class CramersRule(Scene):
    def construct(self):
        Y_TITLE = 5.4        
        Y_SYS   = 4.0        
        Y_MAT   = 2.2        
        Y_DET   = 0.0        
        Y_GRID  = -2.8       
        
        G_SCALE = 1.1        
        sc = 0.5             

        def animate_determinant(matrix, vals, colors, y_pos, final_val, label_str):
            form = MathTex(
                label_str + " = ", "a", "(", "d", ")", " - ", "b", "(", "c", ")",
                font_size=48
            ).move_to(UP * y_pos)
            
            self.play(Write(form), run_time=0.4)
            e = matrix.get_entries()
            
            self.play(Indicate(e[0], scale_factor=1.6, color=YELLOW), run_time=0.25)
            num_a = MathTex(vals[0], color=colors[0], font_size=48).move_to(form[1])
            self.play(form[1].animate.become(num_a), run_time=0.2)
            
            self.play(Indicate(e[3], scale_factor=1.6, color=YELLOW), run_time=0.25)
            num_d = MathTex(vals[3], color=colors[3], font_size=48).move_to(form[3])
            self.play(form[3].animate.become(num_d), run_time=0.2)
            
            self.play(Indicate(e[1], scale_factor=1.6, color=YELLOW), run_time=0.25)
            num_b = MathTex(vals[1], color=colors[1], font_size=48).move_to(form[6])
            self.play(form[6].animate.become(num_b), run_time=0.2)
            
            self.play(Indicate(e[2], scale_factor=1.6, color=YELLOW), run_time=0.25)
            num_c = MathTex(vals[2], color=colors[2], font_size=48).move_to(form[8])
            self.play(form[8].animate.become(num_c), run_time=0.2)
            
            self.wait(0.25)
            final_form = MathTex(
                f"{label_str} = {vals[0]}({vals[3]}) - {vals[1]}({vals[2]}) = {final_val}", 
                font_size=48
            ).move_to(UP * y_pos)
            
            self.play(ReplacementTransform(form, final_form), run_time=0.4)
            return final_form

        title = MathTex(r"\mathbb{C}\text{ramer's } \mathbb{R}\text{ule}", font_size=64)
        title.set_color_by_gradient(BLUE, RED).move_to(UP * Y_TITLE)
        
        eq1 = VGroup(MathTex("2", color=BLUE), MathTex("x + "), MathTex("1", color=GREEN), MathTex("y = "), MathTex("3", color=PINK)).arrange(RIGHT, buff=0.15)
        eq2 = VGroup(MathTex("1", color=BLUE), MathTex("x + "), MathTex("3", color=GREEN), MathTex("y = "), MathTex("5", color=PINK)).arrange(RIGHT, buff=0.15)
        system = VGroup(eq1, eq2).arrange(DOWN, buff=0.25).move_to(UP * Y_SYS).scale(G_SCALE)

        self.add(title, system)
        self.wait(0.5)

        A_mat = Matrix([["2", "1"], ["1", "3"]], bracket_h_buff=0.2)
        e = A_mat.get_entries()
        e[0].set_color(BLUE); e[1].set_color(GREEN)
        e[2].set_color(BLUE); e[3].set_color(GREEN)
        
        b_vec = Matrix([["3"], ["5"]])
        for entry in b_vec.get_entries(): entry.set_color(PINK)
        
        mat_eq = VGroup(A_mat, MathTex(r"\mathbf{x}"), MathTex("="), b_vec).arrange(RIGHT, buff=0.3)
        mat_eq.move_to(UP * Y_MAT).scale(G_SCALE)

        self.play(ReplacementTransform(system, mat_eq), run_time=0.5)
        self.wait(0.25)
        
        det_A_eq = animate_determinant(A_mat, ["2", "1", "1", "3"], [BLUE, GREEN, BLUE, GREEN], Y_DET, "5", r"\det(A)")
        self.wait(0.25)

        grid = NumberPlane(x_range=[-1, 6], y_range=[-1, 7], background_line_style={"stroke_opacity": 0.2}).scale(sc).move_to(UP * Y_GRID)
        def p(x, y): return grid.c2p(x, y)
        orig = p(0,0)

        arr_a = Arrow(orig, p(2,1), color=BLUE, buff=0, stroke_width=6)
        arr_b = Arrow(orig, p(1,3), color=GREEN, buff=0, stroke_width=6)
        para_ab = Polygon(orig, p(2,1), p(3,4), p(1,3), color=WHITE, fill_color=WHITE, fill_opacity=0.15, stroke_width=2)
        
        area_A = MathTex(r"\text{Area} = 5", font_size=36).move_to(p(1.5, -0.8))

        self.play(FadeIn(grid), GrowArrow(arr_a), GrowArrow(arr_b), run_time=0.5)
        self.play(Create(para_ab), FadeIn(area_A), run_time=0.4)
        self.wait(0.5)

        arr_c = Arrow(orig, p(3,5), color=PINK, buff=0, stroke_width=6)
        label_c = MathTex("c", color=PINK, font_size=40).next_to(arr_c.get_end(), UP, buff=0.1)
        self.play(GrowArrow(arr_c), FadeIn(label_c), run_time=0.4)
        
        col_1_center = VGroup(e[0], e[2]).get_center()
        c_copy = label_c.copy()
        self.play(
            c_copy.animate.move_to(col_1_center).scale(1.5), 
            FadeOut(area_A, para_ab, arr_a), 
            run_time=0.5
        )
        
        Ax_mat = Matrix([["3", "1"], ["5", "3"]], bracket_h_buff=0.2).scale(G_SCALE).move_to(A_mat)
        Ax_e = Ax_mat.get_entries()
        Ax_e[0].set_color(PINK); Ax_e[1].set_color(GREEN)
        Ax_e[2].set_color(PINK); Ax_e[3].set_color(GREEN)
        
        self.play(FadeOut(A_mat, c_copy, det_A_eq), FadeIn(Ax_mat), run_time=0.3)
        
        det_Ax_eq = animate_determinant(Ax_mat, ["3", "1", "5", "3"], [PINK, GREEN, PINK, GREEN], Y_DET, "4", r"\det(A_x)")

        para_cb = Polygon(orig, p(3,5), p(4,8), p(1,3), color=PINK, fill_color=PINK, fill_opacity=0.25, stroke_width=2)
        
        area_X = MathTex(r"\text{Area} = 4", color=PINK, font_size=36).move_to(p(2.0, -0.8))
        
        x_title = Tex("Cramer's Rule for $x$:", font_size=36, color=WHITE).move_to(UP * (Y_DET - 0.9))
        x_form = MathTex(r"x = \frac{\det(A_x)}{\det(A)} = \frac{4}{5}", font_size=52).next_to(x_title, DOWN, buff=0.2)
        x_group = VGroup(x_title, x_form)
        x_box = SurroundingRectangle(x_group, color=BLUE, fill_color=BLUE, fill_opacity=0.25, corner_radius=0.15, buff=0.25)

        self.play(Create(para_cb), FadeIn(area_X), run_time=0.4)
        self.play(Create(x_box), Write(x_group), run_time=0.5)
        self.wait(0.75)

        col_2_center = VGroup(e[1], e[3]).get_center()
        c_copy_2 = label_c.copy()
        
        self.play(
            FadeOut(Ax_mat, det_Ax_eq, para_cb, area_X, arr_b, x_group, x_box), 
            FadeIn(A_mat, arr_a), 
            run_time=0.4
        )
        self.play(c_copy_2.animate.move_to(col_2_center).scale(1.5), run_time=0.5)

        Ay_mat = Matrix([["2", "3"], ["1", "5"]], bracket_h_buff=0.2).scale(G_SCALE).move_to(A_mat)
        Ay_e = Ay_mat.get_entries()
        Ay_e[0].set_color(BLUE); Ay_e[1].set_color(PINK)
        Ay_e[2].set_color(BLUE); Ay_e[3].set_color(PINK)
        
        self.play(FadeOut(A_mat, c_copy_2), FadeIn(Ay_mat), run_time=0.3)
        det_Ay_eq = animate_determinant(Ay_mat, ["2", "3", "1", "5"], [BLUE, PINK, BLUE, PINK], Y_DET, "7", r"\det(A_y)")

        para_ac = Polygon(orig, p(2,1), p(5,6), p(3,5), color=GREEN, fill_color=GREEN, fill_opacity=0.25, stroke_width=2)
        
        area_Y = MathTex(r"\text{Area} = 7", color=GREEN, font_size=36).move_to(p(3.0, -0.8))
        
        y_title = Tex("Cramer's Rule for $y$:", font_size=36, color=WHITE).move_to(UP * (Y_DET - 0.9))
        y_form = MathTex(r"y = \frac{\det(A_y)}{\det(A)} = \frac{7}{5}", font_size=52).next_to(y_title, DOWN, buff=0.2)
        y_group = VGroup(y_title, y_form)
        y_box = SurroundingRectangle(y_group, color=BLUE, fill_color=BLUE, fill_opacity=0.25, corner_radius=0.15, buff=0.25)

        self.play(Create(para_ac), FadeIn(area_Y), run_time=0.4)
        self.play(Create(y_box), Write(y_group), run_time=0.5)
        self.wait(0.75)

        self.play(
            FadeOut(grid, arr_a, arr_c, label_c, para_ac, area_Y, Ay_mat, mat_eq[1:], det_Ay_eq, y_group, y_box), 
            run_time=0.5
        )
        
        sys_title = Tex("General System:", font_size=36, color=WHITE)
        gen_sys = MathTex(r"\begin{cases} a x + b y = e \\ c x + d y = f \end{cases}", font_size=52)
        sys_inner = VGroup(sys_title, gen_sys).arrange(DOWN, buff=0.2)
        sys_box = SurroundingRectangle(sys_inner, color=BLUE, fill_color=BLUE, fill_opacity=0.25, corner_radius=0.15, buff=0.3)
        sys_comp = VGroup(sys_box, sys_inner)

        x_gen_title = Tex("Formula for $x$:", font_size=36, color=WHITE)
        gen_form_x = MathTex(r"x = \frac{ed - bf}{ad - bc}", font_size=52)
        x_inner = VGroup(x_gen_title, gen_form_x).arrange(DOWN, buff=0.2)
        gen_x_box = SurroundingRectangle(x_inner, color=BLUE, fill_color=BLUE, fill_opacity=0.25, corner_radius=0.15, buff=0.3)
        gen_x_comp = VGroup(gen_x_box, x_inner)

        y_gen_title = Tex("Formula for $y$:", font_size=36, color=WHITE)
        gen_form_y = MathTex(r"y = \frac{af - ec}{ad - bc}", font_size=52)
        y_inner = VGroup(y_gen_title, gen_form_y).arrange(DOWN, buff=0.2)
        gen_y_box = SurroundingRectangle(y_inner, color=BLUE, fill_color=BLUE, fill_opacity=0.25, corner_radius=0.15, buff=0.3)
        gen_y_comp = VGroup(gen_y_box, y_inner)

        final_layout = VGroup(sys_comp, gen_x_comp, gen_y_comp).arrange(DOWN, buff=0.8).move_to(ORIGIN)

        self.play(FadeIn(final_layout, shift=UP*0.3), run_time=0.8)
        self.wait(1.5)

        # Graceful exit
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.75)
        self.wait(0.25)