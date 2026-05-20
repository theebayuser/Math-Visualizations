from manim import *


C_RED = "#d13b3b"
C_ORANGE = "#e3882f"
C_GREEN = "#69a04a"
C_BLUE = "#4185f4"
C_WHITE = "#FFFFFF"

class SumOfCubesProof(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        unit_size = 0.35 
        
        special_text = Tex(r"$\mathbb{Y}$ear 2025 is $\mathbb{S}$pecial!", font_size=60)
        special_text.set_color_by_gradient(BLUE, RED)
        
        hook_eq = Tex(
            r"\begin{align*} 2025 &= 1^3+2^3+\dots+9^3 \\ &= (1+2+\dots+9)^2 \end{align*}",
            font_size=48
        )
        question_text = Tex("Or is it?", font_size=48)
        question_text.set_color_by_gradient(BLUE, RED)
        
        hook_eq.center()
        special_text.next_to(hook_eq, UP, buff=0.75)
        question_text.next_to(hook_eq, DOWN, buff=0.75)
        hook_group = VGroup(special_text, hook_eq, question_text)

        self.add(hook_eq)
        self.wait(0.5)
        
        self.play(Write(special_text), run_time=0.7)
        self.play(Write(question_text), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(hook_group))

        initial_cubes_pos = UP * 2.8
        cube1 = self.create_decomposed_cube(1, C_RED, unit_size)
        label1 = MathTex("1^3", color=C_WHITE).next_to(cube1, DOWN)
        cube2 = self.create_decomposed_cube(2, C_ORANGE, unit_size)
        label2 = MathTex("2^3", color=C_WHITE).next_to(cube2, DOWN)
        cube3 = self.create_decomposed_cube(3, C_GREEN, unit_size)
        label3 = MathTex("3^3", color=C_WHITE).next_to(cube3, DOWN)

        initial_row = VGroup(
            VGroup(cube1, label1), VGroup(cube2, label2), VGroup(cube3, label3)
        ).arrange(RIGHT, buff=unit_size * 1.5).move_to(initial_cubes_pos)
        
        self.play(
            LaggedStart(
                Create(cube1), Write(label1), Create(cube2), Write(label2), Create(cube3), Write(label3),
                lag_ratio=0.3, run_time=2
            )
        )
        self.wait(0.2)
        
        equation_p1 = MathTex("1^3 + 2^3 + 3^3", "=", "?").move_to(DOWN * 3.0)
        self.play(Write(equation_p1), run_time=0.5)
        self.wait(0.2)
        self.play(FadeOut(label1, label2, label3), run_time=0.5)

        final_square_2 = self.animate_gnomon_formation(2, cube2, cube1, unit_size)
        self.wait(0.2)
        final_square_3 = self.animate_gnomon_formation(3, cube3, final_square_2, unit_size)
        self.wait(0.2)

        brace = Brace(final_square_3, DOWN)
        bl1, bl2, bl3 = MathTex("1"), MathTex("2"), MathTex("3")
        brace_labels = VGroup(bl1, bl2, bl3).arrange(RIGHT, buff=unit_size*1.5).next_to(brace, DOWN)
        
        equation_p2 = MathTex("1^3 + 2^3 + 3^3", "=", "(1+2+3)^2").move_to(equation_p1.get_center())

        self.play(GrowFromCenter(brace), FadeIn(brace_labels, shift=UP), run_time=0.7)
        self.wait(0.5)
        self.play(TransformMatchingTex(equation_p1, equation_p2), run_time=0.7)
        self.wait(0.5)

        cube4 = self.create_decomposed_cube(4, C_BLUE, unit_size, direction=RIGHT)
        cube4.next_to(equation_p2, UP, buff=0.3)
        
        S_prev = sum(range(1, 4))
        S_curr = sum(range(1, 5))
        final_center = UP * 1.25
        tl_corner_total = final_center + (S_curr * unit_size / 2) * (UP + LEFT)
        new_center_for_existing = tl_corner_total + (S_prev * unit_size / 2) * (DOWN + RIGHT)
        shift_vector = new_center_for_existing - final_square_3.get_center()

        self.play(FadeIn(cube4, scale=0.8), run_time=0.5)
        
        self.play(
            final_square_3.animate.shift(shift_vector),
            brace.animate.shift(shift_vector),
            brace_labels.animate.shift(shift_vector),
            run_time=0.7
        )
        
        source_units = VGroup(*[unit for nxn_sq in cube4 for unit in nxn_sq])
        target_gnomon = self.create_gnomon_target_squares(4, S_prev, unit_size, C_BLUE, tl_corner_total)
        self.play(Transform(source_units, target_gnomon), run_time=1.0)
        final_square_4 = VGroup(final_square_3, source_units)
        self.wait(0.2)

        new_brace = Brace(final_square_4, DOWN)
        bl4 = MathTex("4")
        new_brace_labels = VGroup(bl1.copy(), bl2.copy(), bl3.copy(), bl4).arrange(RIGHT, buff=unit_size*2.25).next_to(new_brace, DOWN)

        self.play(
            Transform(brace, new_brace),
            Transform(brace_labels, new_brace_labels),
            run_time=0.7
        )
        self.wait(0.5)
        
        equation_p3 = MathTex("1^3 + 2^3 + 3^3 + 4^3", "=", "(1+2+3+4)^2", font_size=38).move_to(equation_p2.get_center())
        
        self.play(
            FadeOut(equation_p2, shift=DOWN*0.2), 
            FadeIn(equation_p3, shift=UP*0.2),
            run_time=0.7
        )
        self.wait(0.5)

        final_brace_label = MathTex("1+2+3+\\dots+n").next_to(brace, DOWN)
        self.play(Transform(brace_labels, final_brace_label), run_time=0.7)
        
        final_equation = MathTex("\\sum_{k=1}^{n} k^3", "=", "\\left( \\sum_{k=1}^{n} k \\right)^2").move_to(equation_p3.get_center())
        
        self.play(
            FadeOut(equation_p3, shift=DOWN*0.2),
            FadeIn(final_equation, shift=UP*0.2),
            run_time=0.7
        )
        self.wait(0.5)

        final_title = Text("Nicomachus's Theorem", font_size=48).to_edge(UP, buff=1.5)
        final_square_group = VGroup(final_square_4, brace, brace_labels)

        self.play(FadeOut(final_square_group), run_time=0.7)
        self.play(
            final_equation.animate.center().shift(UP*0.25),
            Write(final_title)
        )
        self.wait(2)

    def create_decomposed_cube(self, n, color, unit_size, direction=RIGHT):
        n_squares_group = VGroup()
        for _ in range(n):
            nxn_square = VGroup(*[
                Square(side_length=unit_size, fill_color=color, fill_opacity=1, stroke_width=1.5, stroke_color=self.camera.background_color)
                .move_to(np.array([j * unit_size, i * unit_size, 0]))
                for i in range(n) for j in range(n)
            ])
            nxn_square.center()
            n_squares_group.add(nxn_square)
        n_squares_group.arrange(direction, buff=unit_size / 2)
        return n_squares_group

    def create_gnomon_target_squares(self, n, S_prev, unit_size, color, tl_corner_total):
        target_squares = VGroup()
        S_curr = S_prev + n
        for i in range(S_prev):
            for j in range(n):
                pos = tl_corner_total + (np.array([(i + 0.5) * unit_size, -(S_prev + j + 0.5) * unit_size, 0]))
                target_squares.add(Square(unit_size, fill_color=color, fill_opacity=1, stroke_width=1.5, stroke_color=self.camera.background_color).move_to(pos))
        for i in range(n):
            for j in range(S_curr):
                pos = tl_corner_total + (np.array([(S_prev + i + 0.5) * unit_size, -(j + 0.5) * unit_size, 0]))
                target_squares.add(Square(unit_size, fill_color=color, fill_opacity=1, stroke_width=1.5, stroke_color=self.camera.background_color).move_to(pos))
        return target_squares

    def animate_gnomon_formation(self, n, source_cube, existing_square, unit_size):
        S_prev = sum(range(1, n))
        S_curr = sum(range(1, n + 1))
        final_center = UP * 1.25
        tl_corner_total = final_center + (S_curr * unit_size / 2) * (UP + LEFT)
        new_center_for_existing = tl_corner_total + (S_prev * unit_size / 2) * (DOWN + RIGHT)
        
        source_color = source_cube[0][0].get_color()
        target_gnomon = self.create_gnomon_target_squares(n, S_prev, unit_size, source_color, tl_corner_total)
        source_units = VGroup(*[unit for nxn_sq in source_cube for unit in nxn_sq])
        
        self.play(
            Transform(source_units, target_gnomon),
            existing_square.animate.move_to(new_center_for_existing),
            run_time=0.7
        )
        return VGroup(existing_square, source_units)
