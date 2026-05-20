from manim import *

class LorentzTransformationDerivation(Scene):
    def construct(self):
        
        Tex.set_default(color=WHITE)
        MathTex.set_default(color=WHITE)

        
        title = Tex("Elegant Derivation of the", "Lorentz Transformation")
        title[0].scale(1.2)
        title[1].scale(1.5).next_to(title[0], DOWN).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.wait(1)

        
        self.show_light_clock()
        self.show_moving_light_clock()

        
        self.derive_time_dilation()

        
        self.derive_x_prime()
        self.derive_t_prime()

        
        self.show_final_equations()
        
        self.wait(3)

    def show_light_clock(self):
        """Scene 1: The Light Clock in the stationary frame S."""
        title = Tex("Part 1: The Light Clock (Stationary Frame S)").to_edge(UP)
        
        
        mirror_top = Line(LEFT * 2, RIGHT * 2, color=GRAY_A).shift(UP * 2)
        mirror_bottom = Line(LEFT * 2, RIGHT * 2, color=GRAY_A).shift(DOWN * 2)
        mirrors = VGroup(mirror_top, mirror_bottom)
        
        
        distance_label = Brace(Line(mirror_top.get_right(), mirror_bottom.get_right()), RIGHT)
        L_label = distance_label.get_tex("L")

        self.play(Write(title))
        self.play(Create(mirrors), Create(distance_label), Write(L_label))
        self.wait(1)

        
        photon = Dot(mirror_bottom.get_center(), color=YELLOW, radius=0.1)
        self.play(FadeIn(photon))
        
        
        equation = MathTex(r"\Delta t = \frac{2L}{c}").next_to(mirrors, DOWN, buff=1)

        
        self.play(photon.animate.move_to(mirror_top.get_center()), run_time=1)
        self.play(photon.animate.move_to(mirror_bottom.get_center()), run_time=1)
        self.play(Write(equation))
        self.wait(2)

        self.play(
            FadeOut(title), FadeOut(mirrors), FadeOut(distance_label),
            FadeOut(L_label), FadeOut(photon), FadeOut(equation)
        )
        self.wait(1)

    def show_moving_light_clock(self):
        """Scene 2: The Light Clock in the moving frame S'."""
        title = Tex("The Light Clock (Moving Frame S')").to_edge(UP)
        self.play(Write(title))

        
        start_pos = LEFT * 4
        end_pos = RIGHT * 4
        
        mirror_top = Line(start_pos + LEFT, start_pos + RIGHT, color=BLUE).shift(UP * 2)
        mirror_bottom = Line(start_pos + LEFT, start_pos + RIGHT, color=BLUE).shift(DOWN * 2)
        mirrors = VGroup(mirror_top, mirror_bottom)

        photon = Dot(mirror_bottom.get_center(), color=YELLOW, radius=0.1)
        
        
        path_up = Line(mirror_bottom.get_start(), mirror_top.get_center())
        path_down = Line(mirror_top.get_center(), mirror_bottom.get_end())
        
        self.play(FadeIn(mirrors, photon))
        self.wait(1)

        
        self.play(
            mirrors.animate.move_to(end_pos),
            photon.animate.move_to(mirror_top.get_center()),
            run_time=2
        )
        self.play(
            mirrors.animate.move_to(start_pos),
            photon.animate.move_to(mirror_bottom.get_center()),
            run_time=2
        )
        self.play(FadeOut(photon))
        
        
        mirrors.move_to(ORIGIN) 
        triangle = Polygon(
            mirror_bottom.get_left(), 
            mirror_top.get_center(), 
            mirror_bottom.get_right(),
            stroke_color=WHITE,
            stroke_width=3
        )
        
        
        base = Line(mirror_bottom.get_left(), mirror_bottom.get_right())
        height = DashedLine(mirror_top.get_center(), mirror_bottom.get_center())
        hypotenuse = Line(mirror_bottom.get_left(), mirror_top.get_center())

        label_L = MathTex("L").next_to(height, RIGHT)
        label_v = MathTex(r"\frac{1}{2} v \Delta t'").next_to(base, DOWN)
        label_D = MathTex("D = \\frac{1}{2} c \\Delta t'").next_to(hypotenuse, UP + LEFT, buff=-0.5)

        self.play(
            FadeOut(mirrors),
            Create(triangle), Create(height),
            Write(label_L), Write(label_v), Write(label_D)
        )
        self.wait(3)
        self.clear()

    def derive_time_dilation(self):
        """Scene 3: Derivation of the Time Dilation formula."""
        title = Tex("Part 2: Deriving Time Dilation").to_edge(UP)
        self.play(Write(title))

        
        pythag_eq = MathTex("D^2", "=", "L^2", "+", r"\left(\frac{v \Delta t'}{2}\right)^2")
        self.play(Write(pythag_eq))
        self.wait(1)

        
        sub_eq_1 = MathTex(r"\left(\frac{c \Delta t'}{2}\right)^2", "=", r"\left(\frac{c \Delta t}{2}\right)^2", "+", r"\left(\frac{v \Delta t'}{2}\right)^2")
        sub_eq_1.shift(DOWN*1.5)
        
        self.play(TransformMatchingTex(pythag_eq.copy(), sub_eq_1, path_arc=PI/2))
        self.wait(2)
        
        
        step_1 = MathTex(r"c^2 (\Delta t')^2 = c^2 (\Delta t)^2 + v^2 (\Delta t')^2")
        self.play(FadeOut(pythag_eq), Transform(sub_eq_1, step_1.move_to(ORIGIN)))
        self.wait(2)
        
        step_2 = MathTex(r"(\Delta t')^2 (c^2 - v^2) = c^2 (\Delta t)^2")
        self.play(Transform(sub_eq_1, step_2.move_to(ORIGIN)))
        self.wait(2)

        step_3 = MathTex(r"(\Delta t')^2 = \frac{c^2 (\Delta t)^2}{c^2 - v^2} = \frac{(\Delta t)^2}{1 - v^2/c^2}")
        self.play(Transform(sub_eq_1, step_3.move_to(ORIGIN)))
        self.wait(3)

        
        final_eq = MathTex(r"\Delta t' = \frac{\Delta t}{\sqrt{1 - v^2/c^2}}")
        result_box = SurroundingRectangle(final_eq, color=BLUE, buff=0.2)
        
        
        gamma = MathTex(r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}").shift(DOWN * 2)
        gamma_result = MathTex(r"\Delta t' = \gamma \Delta t").move_to(final_eq.get_center())
        gamma_box = SurroundingRectangle(gamma_result, color=BLUE, buff=0.2)
        
        self.play(Transform(sub_eq_1, final_eq))
        self.play(Create(result_box))
        self.wait(1)

        self.play(Write(gamma))
        self.wait(2)
        
        self.play(
            FadeOut(result_box),
            Transform(sub_eq_1, gamma_result)
        )
        self.play(Create(gamma_box))
        self.wait(3)

        self.clear()

    def derive_x_prime(self):
        """Scene 4: Derive the Lorentz Transformation for x'."""
        title = Tex("Part 3: Deriving the Transformation for ", r"$x'$").to_edge(UP)
        self.play(Write(title))

        
        ax_S = Axes(x_range=[-1, 5], y_range=[-1, 3], tips=False).add_coordinates()
        label_S = MathTex("S").next_to(ax_S.y_axis, UP, buff=0.2)
        
        ax_Sp = Axes(x_range=[-1, 5], y_range=[-1, 3], tips=False, axis_config={"color": BLUE}).add_coordinates()
        label_Sp = MathTex("S'", color=BLUE).next_to(ax_Sp.y_axis, UP, buff=0.2)
        ax_Sp.shift(RIGHT * 2.5) 

        
        event = Dot(ax_S.c2p(4, 2), color=YELLOW)
        event_label = Tex("Event").next_to(event, DOWN)
        
        brace_x = Brace(Line(ax_S.c2p(0,0), ax_S.c2p(4,0)), DOWN)
        label_x = brace_x.get_tex("x")

        brace_vt = Brace(Line(ax_S.c2p(0,0), ax_Sp.c2p(0,0)), UP)
        label_vt = brace_vt.get_tex("vt")

        brace_xp = Brace(Line(ax_Sp.c2p(0,0), ax_Sp.c2p(1.5,0)), DOWN, color=BLUE)
        label_xp = brace_xp.get_tex("x'").set_color(BLUE)

        self.play(
            Create(ax_S), Write(label_S),
            Create(ax_Sp), Write(label_Sp),
            Create(event), Write(event_label)
        )
        self.play(
            Create(brace_x), Write(label_x),
            Create(brace_vt), Write(label_vt),
            Create(brace_xp), Write(label_xp)
        )
        self.wait(3)

        
        visuals = VGroup(
            ax_S, label_S, ax_Sp, label_Sp, event, event_label,
            brace_x, label_x, brace_vt, label_vt, brace_xp, label_xp
        )
        self.play(visuals.animate.scale(0.5).to_corner(UL))

        
        
        
        eq1 = MathTex("x - vt", "=", r"\frac{x'}{\gamma}").to_edge(RIGHT, buff=1).shift(UP*1)
        self.play(Write(eq1))
        self.wait(2)
        
        eq2 = MathTex("x'", "=", r"\gamma(x-vt)")
        eq2.move_to(eq1.get_center())
        box2 = SurroundingRectangle(eq2, color=BLUE, buff=0.2)

        self.play(Transform(eq1, eq2))
        self.play(Create(box2))
        self.wait(3)
        
        self.clear()

    def derive_t_prime(self):
        """Scene 5: Derive the Lorentz Transformation for t'."""
        title = Tex("Deriving the Transformation for ", r"$t'$").to_edge(UP)
        self.play(Write(title))

        eq_x = MathTex("x", "=", r"\gamma(x' + vt')").shift(UP*2)
        eq_xp = MathTex("x'", "=", r"\gamma(x - vt)").shift(UP*1)
        self.play(Write(eq_x), Write(eq_xp))
        self.wait(2)

        
        step1 = MathTex("x", "=", r"\gamma(\gamma(x-vt) + vt')")
        self.play(
            TransformMatchingTex(VGroup(eq_x, eq_xp).copy(), step1.move_to(ORIGIN))
        )
        self.wait(2)

        step2 = MathTex(r"\frac{x}{\gamma}", "=", r"\gamma x - \gamma vt + vt'")
        self.play(Transform(step1, step2))
        self.wait(2)

        step3 = MathTex(r"vt'", "=", r"\frac{x}{\gamma} - \gamma x + \gamma vt")
        self.play(Transform(step1, step3))
        self.wait(2)

        step4 = MathTex(r"t'", "=", r"\frac{x}{\gamma v} - \frac{\gamma x}{v} + \gamma t")
        self.play(Transform(step1, step4))
        self.wait(2)
        
        step5 = MathTex(r"t'", "=", r"\gamma t + \frac{x}{v} (\frac{1}{\gamma} - \gamma)")
        self.play(Transform(step1, step5))
        self.wait(2)

        
        sub_derivation = MathTex(
            r"\frac{1}{\gamma} - \gamma = \sqrt{1-\frac{v^2}{c^2}} - \frac{1}{\sqrt{1-\frac{v^2}{c^2}}} = \frac{1 - v^2/c^2 - 1}{\sqrt{1-v^2/c^2}} = \frac{-v^2/c^2}{\sqrt{1-v^2/c^2}} = -\gamma \frac{v^2}{c^2}"
        ).scale(0.7).to_edge(DOWN)
        self.play(Write(sub_derivation))
        self.wait(3)

        step6 = MathTex(r"t'", "=", r"\gamma t + \frac{x}{v} (-\gamma \frac{v^2}{c^2})")
        self.play(Transform(step1, step6))
        self.wait(2)

        
        final_eq = MathTex(r"t'", "=", r"\gamma \left(t - \frac{vx}{c^2}\right)")
        box_final = SurroundingRectangle(final_eq, color=BLUE, buff=0.2)

        self.play(FadeOut(sub_derivation), Transform(step1, final_eq))
        self.play(Create(box_final))
        self.wait(3)

        self.clear()


    def show_final_equations(self):
        """Scene 6: Show the complete set of Lorentz Transformations."""
        title = Tex("The Lorentz Transformation").to_edge(UP)
        self.play(Write(title))

        
        eq_t = MathTex(r"t'", "=", r"\gamma \left(t - \frac{vx}{c^2}\right)")
        eq_x = MathTex(r"x'", "=", r"\gamma (x-vt)")
        eq_y = MathTex(r"y'", "=", r"y")
        eq_z = MathTex(r"z'", "=", r"z")
        
        equations = VGroup(eq_t, eq_x, eq_y, eq_z).arrange(DOWN, buff=0.5).shift(LEFT * 3)
        self.play(Write(equations))
        self.wait(2)

        
        matrix_lhs = MathTex(r"\begin{pmatrix} ct' \\ x' \\ y' \\ z' \end{pmatrix}")
        equals = MathTex("=").next_to(matrix_lhs, RIGHT)
        
        gamma_str = r"\gamma"
        beta_gamma_str = r"-\beta\gamma"
        matrix_transform = MathTex(
            r"\begin{pmatrix} " +
            gamma_str + r" & " + beta_gamma_str + r" & 0 & 0 \\ " +
            beta_gamma_str + r" & " + gamma_str + r" & 0 & 0 \\ " +
            r"0 & 0 & 1 & 0 \\ " +
            r"0 & 0 & 0 & 1" +
            r"\end{pmatrix}"
        ).next_to(equals, RIGHT)

        matrix_rhs = MathTex(r"\begin{pmatrix} ct \\ x \\ y \\ z \end{pmatrix}").next_to(matrix_transform, RIGHT)

        matrix_group = VGroup(matrix_lhs, equals, matrix_transform, matrix_rhs).scale(0.9).shift(RIGHT * 3)
        beta_def = MathTex(r"\text{where } \beta = \frac{v}{c} \text{ and } \gamma = \frac{1}{\sqrt{1-\beta^2}}").next_to(matrix_group, DOWN, buff=0.5)

        self.play(Write(matrix_group), Write(beta_def))
        self.wait(4)

        
        final_group = VGroup(title, equations, matrix_group, beta_def)
        self.play(FadeOut(final_group))
