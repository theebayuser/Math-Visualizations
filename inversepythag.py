from manim import *

class InversePythagorean(Scene):
    def construct(self):
        # Color scheme - modern vibrant colors
        leg_a_color = "#00D9FF"  # Cyan
        leg_b_color = "#00FF88"  # Mint green
        hyp_color = "#FF0080"    # Hot pink
        alt_color = "#FFD700"    # Gold
        
        # Title as one text object
        title = Tex(r"$\mathbb{I}$nverse $\mathbb{P}$ythagorean $\mathbb{T}$heorem", font_size=40)
        title.set_color_by_gradient(BLUE, PURPLE, RED)
        title.to_edge(UP, buff=0.2)
        
        self.play(
            FadeIn(title, shift=DOWN*0.3),
            run_time=1.2
        )
        self.wait(0.2)
        
        # Create initial right triangle - centered and pushed up
        a_len, b_len = 2.0, 1.3
        c_len = np.sqrt(a_len**2 + b_len**2)
        
        A = LEFT * 1.0 + UP * 1.0
        B = A + RIGHT * a_len
        C = A + UP * b_len
        
        triangle = Polygon(A, B, C, color=WHITE, stroke_width=4, fill_opacity=0.1, fill_color=BLUE)
        
        # Right angle indicator at A
        right_angle_at_A = RightAngle(Line(A, B), Line(A, C), length=0.2, stroke_width=2, color=WHITE)
        
        # Vertex labels
        vertex_A = MathTex("A", font_size=32, color=WHITE).next_to(A, DOWN + LEFT, buff=0.15)
        vertex_B = MathTex("B", font_size=32, color=WHITE).next_to(B, DOWN + RIGHT, buff=0.15)
        vertex_C = MathTex("C", font_size=32, color=WHITE).next_to(C, UP + LEFT, buff=0.15)
        
        # Labels for sides with better positioning
        label_a = MathTex("a", color=leg_a_color, font_size=36).next_to(Line(A, B).get_center(), DOWN, buff=0.25)
        label_b = MathTex("b", color=leg_b_color, font_size=36).next_to(Line(A, C).get_center(), LEFT, buff=0.25)
        label_c = MathTex("c", color=hyp_color, font_size=36).move_to(Line(B, C).get_center() + normalize(RIGHT + UP) * 0.4)
        
        self.play(
            DrawBorderThenFill(triangle),
            Create(right_angle_at_A),
            run_time=1
        )
        self.play(
            LaggedStart(
                FadeIn(vertex_A, scale=0.7),
                FadeIn(vertex_B, scale=0.7),
                FadeIn(vertex_C, scale=0.7),
                FadeIn(label_a, scale=0.7),
                FadeIn(label_b, scale=0.7),
                FadeIn(label_c, scale=0.7),
                lag_ratio=0.15
            ),
            run_time=0.8
        )
        self.wait(0.2)
        
        # Draw altitude h to hypotenuse c with correct orientation
        h_val = (a_len * b_len) / c_len
        # Vector along hypotenuse from B to C
        BC_vec = C - B
        BC_len = np.linalg.norm(BC_vec)
        BC_unit = BC_vec / BC_len
        # Project A onto line BC
        BA_vec = A - B
        proj_scalar = np.dot(BA_vec, BC_unit)
        foot = B + BC_unit * proj_scalar
        
        altitude = Line(A, foot, color=alt_color, stroke_width=4)
        altitude_glow = Line(A, foot, color=alt_color, stroke_width=12, stroke_opacity=0.3)
        
        # Right angle indicator at foot - properly oriented perpendicular to hypotenuse
        right_angle_size = 0.15
        # Direction from foot to A (altitude direction)
        altitude_dir = normalize(A - foot)
        # Direction along hypotenuse
        hyp_dir = BC_unit
        
        # Create right angle square
        corner_point1 = foot + altitude_dir * right_angle_size
        corner_point2 = corner_point1 + hyp_dir * right_angle_size
        
        corner = Polygon(
            foot,
            corner_point1,
            corner_point2,
            foot + hyp_dir * right_angle_size,
            stroke_width=2,
            color=alt_color,
            fill_opacity=0
        )
        
        # Position h label on the RIGHT side of the altitude
        label_h = MathTex("h", color=alt_color, font_size=32).move_to(altitude.get_center() + RIGHT * 0.35)
        
        self.play(
            Create(altitude_glow),
            Create(altitude),
            Create(corner),
            run_time=0.8
        )
        self.play(FadeIn(label_h, scale=0.7), run_time=0.4)
        self.wait(0.2)
        
        # Show area formula at bottom - centered
        area_formula = MathTex(
            r"[ABC] = \frac{1}{2}bh = \frac{1}{2}", "ab", r" = \frac{1}{2}", "ch",
            font_size=30,
            color=WHITE
        ).to_edge(DOWN, buff=1.2)
        
        formula_bg = SurroundingRectangle(
            area_formula, 
            color=BLUE, 
            fill_opacity=0.15, 
            buff=0.15, 
            corner_radius=0.1,
            stroke_width=2
        )
        
        self.play(
            FadeIn(formula_bg),
            Write(area_formula),
            run_time=1.2
        )
        
        # Highlight a and b when showing 1/2ab
        self.play(
            Indicate(label_a, scale_factor=1.3, color=leg_a_color),
            Indicate(label_b, scale_factor=1.3, color=leg_b_color),
            Indicate(area_formula[1], scale_factor=1.2),
            run_time=0.6
        )
        self.wait(0.2)
        
        # Highlight c and h when showing 1/2ch
        self.play(
            Indicate(label_c, scale_factor=1.3, color=hyp_color),
            Indicate(label_h, scale_factor=1.3, color=alt_color),
            Indicate(area_formula[3], scale_factor=1.2),
            run_time=0.6
        )
        self.wait(0.3)
        
        # Cancel to get ab = ch at bottom
        area_simplified = MathTex(
            r"ab = ch",
            font_size=38,
            color=alt_color
        ).to_edge(DOWN, buff=0.4)
        
        simplified_bg = SurroundingRectangle(
            area_simplified,
            color=alt_color,
            fill_opacity=0.2,
            buff=0.15,
            corner_radius=0.1,
            stroke_width=3
        )
        
        self.play(
            FadeIn(simplified_bg),
            TransformFromCopy(area_formula, area_simplified),
            run_time=1
        )
        self.wait(0.3)
        
        # Create smaller triangle BELOW the first by morphing a copy
        triangle_copy = triangle.copy()
        scale_factor = 0.55
        # Position below the first triangle - shifted LEFT
        A2 = DOWN * 0.8 + LEFT * 0.8
        B2 = A2 + RIGHT * a_len * scale_factor
        C2 = A2 + UP * b_len * scale_factor
        
        small_triangle = Polygon(A2, B2, C2, color=ORANGE, stroke_width=4, fill_opacity=0.15, fill_color=ORANGE)
        
        # Right angle indicator for small triangle at A2
        right_angle_at_A2 = RightAngle(Line(A2, B2), Line(A2, C2), length=0.15, stroke_width=2, color=ORANGE)
        
        # Labels for scaled triangle
        label_a_scaled = MathTex(r"\frac{a}{ab}", font_size=28, color=leg_a_color).next_to(Line(A2, B2).get_center(), DOWN, buff=0.2)
        label_b_scaled = MathTex(r"\frac{b}{ab}", font_size=28, color=leg_b_color).next_to(Line(A2, C2).get_center(), LEFT, buff=0.2)
        label_c_scaled = MathTex(r"\frac{c}{ab}", font_size=28, color=hyp_color).move_to(Line(B2, C2).get_center() + normalize(RIGHT + UP) * 0.32)
        
        self.play(
            ReplacementTransform(triangle_copy, small_triangle),
            FadeIn(right_angle_at_A2),
            run_time=1.2
        )
        self.play(
            LaggedStart(
                FadeIn(label_a_scaled, shift=UP*0.2),
                FadeIn(label_b_scaled, shift=RIGHT*0.2),
                FadeIn(label_c_scaled, shift=DOWN*0.2),
                lag_ratio=0.2
            ),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Highlight ab=ch with pulse effect
        self.play(
            Indicate(simplified_bg, scale_factor=1.1, color=YELLOW),
            Indicate(area_simplified, scale_factor=1.05),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Replace c/ab with c/ch
        label_c_ch = MathTex(r"\frac{c}{ch}", font_size=28, color=ORANGE).move_to(label_c_scaled.get_center())
        self.play(
            ReplacementTransform(label_c_scaled, label_c_ch),
            run_time=0.8
        )
        label_c_scaled = label_c_ch
        self.wait(0.2)
        
        # Replace c/ch with 1/h
        label_1h = MathTex(r"\frac{1}{h}", font_size=28, color=alt_color).move_to(label_c_scaled.get_center())
        self.play(
            ReplacementTransform(label_c_scaled, label_1h),
            run_time=0.8
        )
        label_c_scaled = label_1h
        self.wait(0.2)
        
        # Simplify other labels to 1/b and 1/a
        label_1b = MathTex(r"\frac{1}{b}", font_size=28, color=leg_b_color).move_to(label_a_scaled.get_center())
        label_1a = MathTex(r"\frac{1}{a}", font_size=28, color=leg_a_color).move_to(label_b_scaled.get_center())
        
        self.play(
            ReplacementTransform(label_a_scaled, label_1b),
            ReplacementTransform(label_b_scaled, label_1a),
            run_time=0.8
        )
        label_a_scaled = label_1b
        label_b_scaled = label_1a
        self.wait(0.4)
        
        # Fade out first triangle with elegant animation
        self.play(
            FadeOut(triangle, shift=UP*0.3),
            FadeOut(right_angle_at_A, shift=UP*0.3),
            FadeOut(vertex_A, shift=UP*0.3),
            FadeOut(vertex_B, shift=UP*0.3),
            FadeOut(vertex_C, shift=UP*0.3),
            FadeOut(label_a, shift=UP*0.3),
            FadeOut(label_b, shift=UP*0.3),
            FadeOut(label_c, shift=UP*0.3),
            FadeOut(altitude, shift=UP*0.3),
            FadeOut(altitude_glow, shift=UP*0.3),
            FadeOut(corner, shift=UP*0.3),
            FadeOut(label_h, shift=UP*0.3),
            FadeOut(area_formula),
            FadeOut(formula_bg),
            FadeOut(area_simplified),
            FadeOut(simplified_bg),
            run_time=1
        )
        
        # Scale and center the small triangle - MUCH BIGGER (changed from 1.3 to 2.0)
        # Calculate new positions before animation
        small_triangle_group = VGroup(small_triangle, right_angle_at_A2)
        target_position = UP * 0.5
        current_center = small_triangle_group.get_center()
        shift_amount = target_position - current_center
        
        # Calculate where the triangle vertices will be after scaling and shifting
        # We need to manually calculate this for label positioning
        scale_val = 2.0
        A2_scaled = (A2 - current_center) * scale_val + current_center + shift_amount
        B2_scaled = (B2 - current_center) * scale_val + current_center + shift_amount
        C2_scaled = (C2 - current_center) * scale_val + current_center + shift_amount
        
        # Create new labels at the correct positions for the scaled triangle
        new_label_1b = MathTex(r"\frac{1}{b}", font_size=42, color=leg_b_color).next_to(Line(A2_scaled, B2_scaled).get_center(), DOWN, buff=0.3)
        new_label_1a = MathTex(r"\frac{1}{a}", font_size=42, color=leg_a_color).next_to(Line(A2_scaled, C2_scaled).get_center(), LEFT, buff=0.3)
        new_label_1h = MathTex(r"\frac{1}{h}", font_size=42, color=alt_color).move_to(Line(B2_scaled, C2_scaled).get_center() + normalize(RIGHT + UP) * 0.5)
        
        # Animate triangle scaling and label transformation simultaneously
        self.play(
            small_triangle_group.animate.scale(scale_val).shift(shift_amount),
            ReplacementTransform(label_a_scaled, new_label_1b),
            ReplacementTransform(label_b_scaled, new_label_1a),
            ReplacementTransform(label_c_scaled, new_label_1h),
            run_time=1
        )
        
        # Update references
        label_a_scaled = new_label_1b
        label_b_scaled = new_label_1a
        label_c_scaled = new_label_1h
        
        # Create the final theorem structure with placeholders
        final_theorem = MathTex(
            r"\left(\frac{1}{a}\right)^2",  # [0]
            r"+",                            # [1]
            r"\left(\frac{1}{b}\right)^2",  # [2]
            r"=",                            # [3]
            r"\left(\frac{1}{h}\right)^2",  # [4]
            font_size=40,
            color=alt_color
        ).to_edge(DOWN, buff=1.2)
        
        theorem_box = SurroundingRectangle(
            final_theorem,
            color=alt_color,
            fill_opacity=0.15,
            buff=0.2,
            corner_radius=0.15,
            stroke_width=3
        )
        
        # Show the box and operators first (+ and =)
        self.play(
            FadeIn(theorem_box, scale=0.9),
            FadeIn(final_theorem[1]),  # +
            FadeIn(final_theorem[3]),  # =
            run_time=0.8
        )
        self.wait(0.3)
        
        # Create copies of the triangle labels for animation
        label_1a_copy = label_b_scaled.copy()
        label_1b_copy = label_a_scaled.copy()
        label_1h_copy = label_c_scaled.copy()
        
        # Animate 1/a moving into position and transforming to (1/a)^2
        self.play(
            label_1a_copy.animate.move_to(final_theorem[0].get_center()).set_opacity(0),
            TransformFromCopy(label_b_scaled, final_theorem[0]),
            run_time=1
        )
        self.wait(0.2)
        
        # Animate 1/b moving into position and transforming to (1/b)^2
        self.play(
            label_1b_copy.animate.move_to(final_theorem[2].get_center()).set_opacity(0),
            TransformFromCopy(label_a_scaled, final_theorem[2]),
            run_time=1
        )
        self.wait(0.2)
        
        # Animate 1/h moving into position and transforming to (1/h)^2
        self.play(
            label_1h_copy.animate.move_to(final_theorem[4].get_center()).set_opacity(0),
            TransformFromCopy(label_c_scaled, final_theorem[4]),
            run_time=1
        )
        self.wait(1.2)
        
        # Elegant fade out
        self.play(
            *[FadeOut(mob, shift=DOWN*0.2) for mob in self.mobjects],
            run_time=1
        )