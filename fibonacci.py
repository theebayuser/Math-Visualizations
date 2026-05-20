from manim import *

class FibonacciProofFinal(Scene):
    def construct(self):
        # --- 1. Aesthetic Configuration ---
        self.camera.background_color = BLACK
        
        # Custom Palette
        C_BLUE = "#38BDF8"   # Light Blue
        C_TEAL = "#2DD4BF"   # Teal
        C_GREEN = "#A3E635"  # Lime Green
        C_YELLOW = "#FACC15" # Warm Yellow
        C_ORANGE = "#FB923C" # Orange
        C_RED = "#F87171"    # Soft Red
        C_PURPLE = "#C084FC" # Purple
        
        HIGHLIGHT = "#00E5FF" # Cyan Highlight
        
        colors = [C_BLUE, C_TEAL, C_GREEN, C_YELLOW, C_ORANGE, C_RED, C_PURPLE, C_BLUE]
        fib_seq = [1, 1, 2, 3, 5, 8, 13, 21]
        scale_factor = 0.135
        
        directions = [RIGHT, UP, LEFT, DOWN]
        alignments = [DOWN, RIGHT, UP, LEFT]

        # --- 2. Title (Top Edge) ---
        title = MathTex(r"\mathbb{F}\text{ibonacci } \mathbb{I}\text{dentity}", font_size=64)
        title.set_color_by_gradient(C_BLUE, C_RED)
        title.to_edge(UP, buff=0.1)
        self.add(title)

        # --- 3. Geometry Position Calculation ---
        shadow_group = VGroup()
        s1_shadow = Square(side_length=fib_seq[0] * scale_factor)
        shadow_group.add(s1_shadow)
        agg_shadow = VGroup(s1_shadow.copy())
        
        for i in range(1, len(fib_seq)):
            n = fib_seq[i]
            d_idx = (i - 1) % 4
            sq = Square(side_length=n * scale_factor)
            sq.next_to(agg_shadow, directions[d_idx], buff=0, aligned_edge=alignments[d_idx])
            agg_shadow.add(sq)

        # Shift Logic: Move Figure DOWN significantly to make room for equations above
        center_shift = ORIGIN - agg_shadow.get_center() + DOWN * 1.0 + LEFT * 0.3

        # --- 4. Geometry Animation ---
        squares = []
        
        # -- First Square (1) --
        s1 = Square(side_length=fib_seq[0] * scale_factor)
        s1.move_to(center_shift)
        s1.set_fill(colors[0], 0.6).set_stroke(WHITE, 1.5)
        
        # Double Arrow Label
        arrow_s1 = DoubleArrow(
            start=s1.get_corner(UL), 
            end=s1.get_corner(UR), 
            buff=0.05, 
            color=WHITE, 
            stroke_width=1.5,
            tip_length=0.05
        )
        lbl_s1_arrow = Integer(1, font_size=14).next_to(arrow_s1, UP, buff=0.02)
        
        self.play(DrawBorderThenFill(s1), GrowFromCenter(arrow_s1), Write(lbl_s1_arrow), run_time=1.0)
        self.play(FadeOut(arrow_s1), FadeOut(lbl_s1_arrow), run_time=0.2)
        
        l1 = Integer(1, font_size=16, color=WHITE).move_to(s1)
        self.add(l1)
        squares.append(s1)
        
        current_shape = VGroup(s1)

        # -- Loop for Remaining Squares --
        for i in range(1, len(fib_seq)):
            n = fib_seq[i]
            d_idx = (i - 1) % 4
            color = colors[i % len(colors)]
            
            sq = Square(side_length=n * scale_factor)
            sq.set_fill(color, 0.6).set_stroke(WHITE, 1.5)
            sq.next_to(current_shape, directions[d_idx], buff=0, aligned_edge=alignments[d_idx])
            
            f_size = min(16 + n*1.5, 42)
            lbl = Integer(n, font_size=f_size, color=WHITE).move_to(sq)
            
            self.play(FadeIn(sq, shift=directions[d_idx]*0.2), Write(lbl), run_time=0.6)
            
            current_shape.add(sq)
            squares.append(sq)

        # --- 5. Dimension Morphing ---
        last_sq = squares[-1]      # 21
        prev_sq = squares[-2]      # 13
        prev2_sq = squares[-3]     # 8
        rest_group = VGroup(*squares[:-1])

        # Width Morph
        brace_w_rest = Brace(rest_group, DOWN, buff=0.05)
        lbl_w_rest = MathTex("13", font_size=24).next_to(brace_w_rest, DOWN, buff=0.05)
        brace_w_last = Brace(last_sq, DOWN, buff=0.05)
        lbl_w_last = MathTex("21", font_size=24).next_to(brace_w_last, DOWN, buff=0.05)
        
        self.play(Create(brace_w_rest), Write(lbl_w_rest), Create(brace_w_last), Write(lbl_w_last))
        
        brace_width_final = Brace(current_shape, DOWN, buff=0.35)
        lbl_width_final = MathTex("34", font_size=36, color=HIGHLIGHT).next_to(brace_width_final, DOWN)
        
        self.play(
            ReplacementTransform(VGroup(brace_w_rest, brace_w_last), brace_width_final),
            ReplacementTransform(VGroup(lbl_w_rest, lbl_w_last), lbl_width_final),
            run_time=1
        )

        # Height Morph
        brace_h_8 = Brace(prev2_sq, RIGHT, buff=0.05)
        lbl_h_8 = MathTex("8", font_size=24).next_to(brace_h_8, RIGHT, buff=0.05)
        brace_h_13 = Brace(prev_sq, RIGHT, buff=0.05)
        lbl_h_13 = MathTex("13", font_size=24).next_to(brace_h_13, RIGHT, buff=0.05)
        
        self.play(Create(brace_h_8), Write(lbl_h_8), Create(brace_h_13), Write(lbl_h_13))
        
        brace_height_final = Brace(current_shape, RIGHT, buff=0.35)
        lbl_height_final = MathTex("21", font_size=36, color=HIGHLIGHT).next_to(brace_height_final, RIGHT)
        
        self.play(
            ReplacementTransform(VGroup(brace_h_8, brace_h_13), brace_height_final),
            ReplacementTransform(VGroup(lbl_h_8, lbl_h_13), lbl_height_final),
            run_time=1
        )

        # --- 6. Equation Line 1: Summation (MOVED UP) ---
        
        eq_group = VGroup()
        plus_symbol = MathTex("+", font_size=28)
        terms_mobjects = []
        
        for i, val in enumerate(fib_seq):
            term = MathTex(f"{val}^2", font_size=28)
            eq_group.add(term)
            terms_mobjects.append(term)
            if i < len(fib_seq) - 1:
                p = plus_symbol.copy()
                eq_group.add(p)

        eq_group.arrange(RIGHT, buff=0.15)
        eq_group.center()
        
        # Move Equation UP (Between Title and Figure)
        eq_group.move_to(UP * 2.0)
        
        for i, term in enumerate(terms_mobjects):
            sq = squares[i]
            self.play(Write(term), run_time=0.2)
            
            self.play(
                sq.animate.set_fill(WHITE, opacity=0.9),
                run_time=0.1
            )
            self.play(sq.animate.set_fill(colors[i % len(colors)], opacity=0.6), run_time=0.1)
            
            if i < len(fib_seq) - 1:
                plus_idx = i * 2 + 1
                self.play(FadeIn(eq_group[plus_idx]), run_time=0.05)
                
        self.wait(0.8)

        # --- 7. Equation Line 2: Result ---
        equals_sign = MathTex("=", font_size=36)
        val_21 = MathTex("21", font_size=36, color=HIGHLIGHT)
        dot = MathTex(r"\cdot", font_size=36)
        val_34 = MathTex("34", font_size=36, color=HIGHLIGHT)
        
        temp_group = VGroup(equals_sign, val_21, dot, val_34).arrange(RIGHT, buff=0.2)
        # Position directly below the summation equation
        temp_group.next_to(eq_group, DOWN, buff=0.3)
        
        self.play(Write(equals_sign))
        
        self.play(
            Write(val_21),
            Indicate(lbl_height_final, color=HIGHLIGHT, scale_factor=1.2),
            run_time=0.8
        )
        
        self.play(Write(dot), run_time=0.2)
        
        self.play(
            Write(val_34),
            Indicate(lbl_width_final, color=HIGHLIGHT, scale_factor=1.2),
            run_time=0.8
        )
        
        self.wait(1)

        # --- 8. The General Reveal ---
        
        gen_width = MathTex("F_{n+1}", font_size=36, color=HIGHLIGHT).move_to(lbl_width_final)
        gen_height = MathTex("F_n", font_size=36, color=HIGHLIGHT).move_to(lbl_height_final)
        
        self.play(
            ReplacementTransform(lbl_width_final, gen_width),
            ReplacementTransform(lbl_height_final, gen_height),
            run_time=1
        )
        
        final_formula = MathTex(
            r"\sum_{i=1}^n F_i^2", r"=", r"F_n \cdot F_{n+1}", 
            font_size=48
        )
        visual_center_of_math = VGroup(eq_group, temp_group).get_center()
        final_formula.move_to(visual_center_of_math)
        final_formula[2].set_color(HIGHLIGHT)
        
        self.play(
            FadeOut(VGroup(eq_group, equals_sign, val_21, dot, val_34), shift=UP * 0.2),
            FadeIn(final_formula, shift=UP * 0.2),
            run_time=1.5
        )
        
        box = SurroundingRectangle(final_formula, color=C_TEAL, buff=0.2)
        self.play(Create(box))
        
        self.wait(3)