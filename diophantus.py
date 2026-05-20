from manim import *

class DiophantusIdentity(Scene):
    def construct(self):
        # --- Config & Setup ---
        # Cool color scheme
        c_a = TEAL_D
        c_b = MAROON_D
        c_c = BLUE_D
        c_d = GOLD_D
        
        # Title with Mathbb and Gradient
        title = Tex(r"$\mathbb{D}$iophantus Identity", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.2)
        
        self.add(title)

        # --- Parameters ---
        # Using sqrt values so squares (a*c, etc) have nice side lengths
        val_a = 0.8
        val_b = 1.2
        val_c = 0.9
        val_d = 1.5
        
        # --- Step 1: Initial Rectangles (Representing Areas) ---
        # Create 4 initial rectangles based on "squared" dimensions input
        
        # Defining the 4 Initial Rectangles (Start)
        # Widths proportional to a^2, b^2. Heights c^2, d^2.
        w1, w2 = 2.0, 3.5 # relative widths a^2, b^2
        h1, h2 = 1.5, 3.0 # relative heights c^2, d^2
        
        r_ac = Rectangle(width=w1, height=h1).set_fill(c_a, 0.5).set_stroke(WHITE, 1)
        r_bc = Rectangle(width=w2, height=h1).set_fill(c_d, 0.5).set_stroke(WHITE, 1)
        r_ad = Rectangle(width=w1, height=h2).set_fill(c_c, 0.5).set_stroke(WHITE, 1)
        r_bd = Rectangle(width=w2, height=h2).set_fill(c_b, 0.5).set_stroke(WHITE, 1)
        
        # Group and Arrange
        top_row = VGroup(r_ac, r_bc).arrange(RIGHT, buff=0)
        bot_row = VGroup(r_ad, r_bd).arrange(RIGHT, buff=0)
        initial_grid = VGroup(top_row, bot_row).arrange(DOWN, buff=0).scale(0.6).move_to(ORIGIN)
        
        # Labels for Step 1
        l_ac = MathTex(r"a^2c^2").move_to(r_ac).scale(0.6)
        l_bc = MathTex(r"b^2c^2").move_to(r_bc).scale(0.6)
        l_ad = MathTex(r"a^2d^2").move_to(r_ad).scale(0.6)
        l_bd = MathTex(r"b^2d^2").move_to(r_bd).scale(0.6)
        labels_1 = VGroup(l_ac, l_bc, l_ad, l_bd)

        # Add braces to show the side lengths
        top_brace = Brace(top_row, UP, buff=0.05)
        top_label = MathTex(r"a^2+b^2").next_to(top_brace, UP, buff=0.00).scale(0.6)
        left_brace = Brace(VGroup(r_ac, r_ad), LEFT, buff=0.02)
        left_label = MathTex(r"c^2+d^2").scale(0.6).rotate(90 * DEGREES).next_to(left_brace, LEFT, buff=0.05)
        
        self.play(DrawBorderThenFill(initial_grid), Write(labels_1), run_time=1.5)
        self.play(GrowFromCenter(top_brace), Write(top_label),
                  GrowFromCenter(left_brace), Write(left_label))
        self.wait(0.5)

        # --- Step 2: Transform to Squares ---
        # Defining the 4 Squares (all touching at the same center point)
        s_ac = Square(side_length=val_a*val_c).set_fill(c_a, 0.5).set_stroke(WHITE, 1)
        s_bd = Square(side_length=val_b*val_d).set_fill(c_b, 0.5).set_stroke(WHITE, 1)
        s_ad = Square(side_length=val_a*val_d).set_fill(c_c, 0.5).set_stroke(WHITE, 1)
        s_bc = Square(side_length=val_b*val_c).set_fill(c_d, 0.5).set_stroke(WHITE, 1)
        
        # Position all four squares so they touch at a central point
        # AD: top-left (corner DR at center)
        # BC: bottom-right (corner UL at center)
        # AC: top-right (corner DL at center)
        # BD: bottom-left (corner UR at center)
        center_point = LEFT * 1
        s_ad.move_to(center_point, aligned_edge=DR)
        s_bc.move_to(center_point, aligned_edge=UL)
        s_ac.move_to(center_point, aligned_edge=DL)
        s_bd.move_to(center_point, aligned_edge=UR)
        
        squares_group = VGroup(s_ac, s_bc, s_ad, s_bd)
        
        # New Labels
        nl_ac = MathTex(r"(ac)^2").move_to(s_ac).scale(0.5)
        nl_bc = MathTex(r"(bc)^2").move_to(s_bc).scale(0.5)
        nl_ad = MathTex(r"(ad)^2").move_to(s_ad).scale(0.5)
        nl_bd = MathTex(r"(bd)^2").move_to(s_bd).scale(0.5)
        new_labels = VGroup(nl_ac, nl_bc, nl_ad, nl_bd)

        self.play(
            FadeOut(top_brace), FadeOut(top_label), FadeOut(left_brace), FadeOut(left_label),
            ReplacementTransform(initial_grid, squares_group),
            ReplacementTransform(labels_1, new_labels),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Step 3: Rearrangement (The Cut Prep) ---
        # AD and BC stay in place (they're already diagonal from each other)
        # Move AC and BD vertically on top of each other
        
        # Stack AC on BD (ac smaller, on top)
        # Position them at the same vertical level as AD and BC, centered
        s_ac_target = s_ac.generate_target()
        s_bd_target = s_bd.generate_target()
        
        # Stack them with AC on top, BD on bottom, aligned on left edge
        # Center the stack horizontally and vertically align with the center of AD/BC
        s_bd_target.move_to(ORIGIN, aligned_edge=ORIGIN)
        s_ac_target.next_to(s_bd_target, UP, buff=0, aligned_edge=LEFT)
        
        # Center the stack
        stack = VGroup(s_ac_target, s_bd_target)
        stack.move_to(RIGHT * 1.5 + ORIGIN)
        
        # Update label trackers
        nl_ac.add_updater(lambda m: m.move_to(s_ac))
        nl_bd.add_updater(lambda m: m.move_to(s_bd))

        self.play(
            MoveToTarget(s_ac), MoveToTarget(s_bd),
            run_time=1.5
        )
        
        # --- Step 4: The Geometric Cut ---
        # Get coords
        bd_corn = s_bd.get_corner(DL)
        ac_len = s_ac.width
        bd_len = s_bd.width
        
        # Create the two rectangles from the cut
        # Bottom piece: Width BD, Height AC (Area = ac*bd)
        rect_bottom = Rectangle(width=bd_len, height=ac_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_bottom.move_to(s_bd.get_corner(DL), aligned_edge=DL)
        
        # Top piece: Width AC, Height BD (Area = ac*bd)
        rect_vertical = Rectangle(width=ac_len, height=bd_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_vertical.move_to(s_ac.get_corner(UL), aligned_edge=UL)
        
        # The Difference Square
        diff_side = bd_len - ac_len
        sq_diff = Square(side_length=diff_side).set_fill(GRAY, 0.8).set_stroke(WHITE, 1)
        sq_diff.move_to(s_bd.get_corner(DR), aligned_edge=DR).shift(UP * ac_len)

        # Draw the cut lines
        cut_line_horiz = DashedLine(s_bd.get_corner(DL) + UP*ac_len, s_bd.get_corner(DR) + UP*ac_len)
        cut_line_vert = DashedLine(s_bd.get_corner(UL) + RIGHT*ac_len, s_bd.get_corner(DL) + RIGHT*ac_len)
        
        # Add temporary labels for the lengths
        # Label for bd (moved to left side and positioned lower)
        bd_top_label = MathTex("bd", font_size=20).next_to(rect_vertical, LEFT, buff=0.1).shift(DOWN * 0.5)
        
        self.play(Create(cut_line_horiz), Create(cut_line_vert), Write(bd_top_label))
        self.wait(0.3)
        
        # Labels for pieces with area and side dimensions
        l_abcd1 = MathTex("abcd", font_size=28).move_to(rect_bottom)
        l_abcd2 = MathTex("abcd", font_size=28).move_to(rect_vertical).shift(DOWN*0.2)
        
        # Add side labels for the rectangles
        side_label_ac = MathTex("ac", font_size=20).next_to(rect_bottom, DOWN, buff=0.1)
        side_label_bd1 = MathTex("bd", font_size=20).next_to(rect_bottom, LEFT, buff=0.1)
        side_label_bd2 = MathTex("bd", font_size=20).next_to(rect_vertical, UP, buff=0.1)
        side_label_ac2 = MathTex("ac", font_size=20).next_to(rect_vertical, RIGHT, buff=0.1)
        
        l_diff = MathTex(r"(bd-ac)^2", font_size=20).move_to(sq_diff)
        
        self.remove(nl_ac, nl_bd) # Remove old labels
        self.play(
            FadeOut(s_ac), FadeOut(s_bd),
            FadeOut(bd_top_label),
            FadeIn(rect_bottom), FadeIn(rect_vertical),
            Write(l_abcd1), Write(l_abcd2),
            Write(side_label_ac), Write(side_label_bd1),
            Write(side_label_bd2), Write(side_label_ac2),
            FadeIn(sq_diff), Write(l_diff)
        )
        self.wait(0.3)
        
        # Fade out the cut lines
        self.play(FadeOut(cut_line_horiz), FadeOut(cut_line_vert), run_time=0.5)
        self.wait(0.2)

        # --- Step 5: Final Assembly ---
        # Now adjust rectangles to fit perfectly
        
        # Target dimensions for final square of side (ad+bc)
        ad_len = s_ad.width
        bc_len = s_bc.width
        
        # Adjust rectangle dimensions: 
        # Bottom rectangle: width = ad, height = bc
        # Vertical rectangle: width = bc, height = ad
        rect_bottom_final = Rectangle(width=ad_len, height=bc_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_vertical_final = Rectangle(width=bc_len, height=ad_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        
        # Position for final square assembly
        # AD stays top-left
        # BC stays bottom-right
        # Place rectangles to complete the square
        s_ad.generate_target().move_to(ORIGIN + LEFT*0.8 + UP*0.8, aligned_edge=DR)
        s_bc.generate_target().move_to(s_ad.target.get_corner(DR), aligned_edge=UL)
        
        rect_vertical_final.next_to(s_ad.target, RIGHT, buff=0, aligned_edge=UP)
        rect_bottom_final.next_to(s_ad.target, DOWN, buff=0, aligned_edge=LEFT)
        
        # Ensure proper alignment
        rect_vertical_final.align_to(s_bc.target, RIGHT)
        rect_bottom_final.align_to(s_bc.target, DOWN)
        
        # Move the diff square to the side
        sq_diff.generate_target().next_to(s_bc.target, RIGHT, buff=0.5)
        l_diff.add_updater(lambda m: m.move_to(sq_diff))

        # Animations
        self.play(
            FadeOut(side_label_ac), FadeOut(side_label_bd1),
            FadeOut(side_label_bd2), FadeOut(side_label_ac2),
            MoveToTarget(s_ad), MoveToTarget(s_bc),
            ReplacementTransform(rect_vertical, rect_vertical_final),
            ReplacementTransform(rect_bottom, rect_bottom_final),
            MoveToTarget(sq_diff),
            l_abcd1.animate.move_to(rect_bottom_final),
            l_abcd2.animate.move_to(rect_vertical_final),
            nl_ad.animate.move_to(s_ad.target),
            nl_bc.animate.move_to(s_bc.target),
            run_time=2
        )
        
        # Final Brace
        final_group = VGroup(s_ad, s_bc, rect_vertical_final, rect_bottom_final)
        
        # Add side length labels for all sides of the final square (smaller)
        # Top side
        top_ad_label = MathTex("ad", font_size=20).next_to(s_ad.target, UP, buff=0.1)
        top_bc_label = MathTex("bc", font_size=20).next_to(rect_vertical_final, UP, buff=0.1)
        
        # Right side  
        right_bc_label = MathTex("bc", font_size=20).next_to(rect_vertical_final, RIGHT, buff=0.1)
        right_ad_label = MathTex("ad", font_size=20).next_to(s_bc.target, RIGHT, buff=0.1)
        
        # Bottom side
        bottom_bc_label = MathTex("bc", font_size=20).next_to(s_bc.target, DOWN, buff=0.1)
        bottom_ad_label = MathTex("ad", font_size=20).next_to(rect_bottom_final, DOWN, buff=0.1)
        
        # Left side
        left_ad_label = MathTex("ad", font_size=20).next_to(s_ad.target, LEFT, buff=0.1)
        left_bc_label = MathTex("bc", font_size=20).next_to(rect_bottom_final, LEFT, buff=0.1)
        
        side_labels = VGroup(top_ad_label, top_bc_label, right_bc_label, right_ad_label,
                             bottom_bc_label, bottom_ad_label, left_ad_label, left_bc_label)
        
        # Write individual side labels first
        self.play(Write(side_labels))
        self.wait(0.3)
        
        # Then add the final brace and label at the bottom
        brace = Brace(final_group, DOWN)
        final_text = MathTex(r"(ad+bc)^2").next_to(brace, DOWN).scale(0.8)
        
        self.play(GrowFromCenter(brace), Write(final_text))
        
        # Final Formula (2 lines)
        eq_line1 = MathTex(r"(a^2+b^2)(c^2+d^2)")
        eq_line2 = MathTex(r"= (ad+bc)^2 + (bd-ac)^2")
        eq = VGroup(eq_line1, eq_line2).arrange(DOWN, buff=0.2)
        eq.scale(0.7).to_edge(DOWN, buff=0.3)
        bg = BackgroundRectangle(eq, fill_color=BLACK, fill_opacity=0.8)
        
        self.play(FadeIn(bg), Write(eq))
        self.wait(2)