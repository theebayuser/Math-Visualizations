from manim import *
from manim import TEAL_D, BLUE_D, BLUE_C, WHITE, BLACK, PURPLE, GRAY, TEAL, BLUE, ORIGIN, UP, DOWN, there_and_back

class QuadraticFormula(Scene):
    def construct(self):
        # Set mobile-friendly aspect ratio (9:16)
        self.camera.background_color = BLACK
        
        # Title with cool gradient effect - positioned for 9:16 crop
        title = Text("Quadratic Formula", font_size=42, gradient=(BLUE, TEAL))
        title.to_edge(UP, buff=0.6)
        
        # Subtitle
        subtitle = Text("From ax² + bx + c = 0", font_size=26, color=BLUE_C)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Animate title entrance (faster)
        self.play(
            Write(title, run_time=0.7),
            FadeIn(subtitle, shift=UP*0.5, run_time=0.7)
        )
        self.wait(0.3)
        
        # Fade out title and subtitle
        self.play(FadeOut(subtitle, run_time=0.5))
        self.wait(0.1)
        
        # Starting equation - centered and sized for mobile
        eq1 = MathTex("ax^2", "+", "bx", "+", "c", "=", "0", font_size=36)
        eq1.set_color_by_tex_to_color_map({
            "ax^2": BLUE,
            "bx": TEAL,
            "c": BLUE_C,
            "=": WHITE,
            "0": WHITE
        })
        eq1.move_to(ORIGIN + UP*1.5)
        
        # Step 1: Move constant to right side
        step1_text = Text("Move constant to right side", font_size=22, color=GRAY)
        step1_text.next_to(eq1, DOWN, buff=0.5)
        
        eq2 = MathTex("ax^2", "+", "bx", "=", "-c", font_size=36)
        eq2.set_color_by_tex_to_color_map({
            "ax^2": BLUE,
            "bx": TEAL,
            "-c": BLUE_C
        })
        eq2.move_to(ORIGIN + UP*1.5)
        
        self.play(Write(eq1, run_time=0.6))
        self.wait(0.2)
        self.play(Write(step1_text, run_time=0.4))
        self.wait(0.3)
        self.play(Transform(eq1, eq2, run_time=0.5))
        self.wait(0.2)
        
        # Clean up step 1
        self.play(FadeOut(step1_text, run_time=0.3))
        self.wait(0.1)
        
        # Step 2: Divide by 'a'
        step2_text = Text("Divide everything by 'a'", font_size=22, color=GRAY)
        step2_text.next_to(eq1, DOWN, buff=0.5)
        
        eq3 = MathTex("x^2", "+", "\\frac{b}{a}x", "=", "-\\frac{c}{a}", font_size=36)
        eq3.set_color_by_tex_to_color_map({
            "x^2": BLUE,
            "\\frac{b}{a}x": TEAL,
            "-\\frac{c}{a}": BLUE_C
        })
        eq3.move_to(ORIGIN + UP*1.5)
        
        self.play(Write(step2_text, run_time=0.4))
        self.wait(0.2)
        self.play(Transform(eq1, eq3, run_time=0.5))
        self.wait(0.3)
        
        # Clean up step 2
        self.play(FadeOut(step2_text, run_time=0.3))
        self.wait(0.1)
        
        # Step 3: Complete the square - WITH FORMULA DISPLAY
        step3_title = Text("Complete the Square", font_size=26, color=BLUE_C)
        step3_title.next_to(eq1, DOWN, buff=0.5)
        
        # Show the complete the square formula prominently
        complete_formula = MathTex("x^2 + bx + \\left(\\frac{b}{2}\\right)^2 = \\left(x + \\frac{b}{2}\\right)^2", font_size=24, color=PURPLE)
        complete_formula.next_to(step3_title, DOWN, buff=0.3)
        
        # Highlight the coefficient of x - properly aligned
        coefficient_highlight = SurroundingRectangle(eq1[2], color=PURPLE, buff=0.05)
        
        self.play(Write(step3_title, run_time=0.4))
        self.wait(0.2)
        self.play(Create(coefficient_highlight, run_time=0.3))
        self.wait(0.2)
        self.play(Write(complete_formula, run_time=0.6))
        self.wait(0.5)
        
        # Show the completing square process
        complete_square = MathTex("x^2", "+", "\\frac{b}{a}x", "+", "\\left(\\frac{b}{2a}\\right)^2", "=", "-\\frac{c}{a}", "+", "\\left(\\frac{b}{2a}\\right)^2", font_size=30)
        complete_square.set_color_by_tex_to_color_map({
            "x^2": BLUE,
            "\\frac{b}{a}x": TEAL,
            "\\left(\\frac{b}{2a}\\right)^2": PURPLE,
            "-\\frac{c}{a}": BLUE_C
        })
        complete_square.move_to(ORIGIN + UP*1.5)
        
        self.play(
            FadeOut(coefficient_highlight, run_time=0.3),
            FadeOut(complete_formula, run_time=0.3),
            Transform(eq1, complete_square, run_time=0.5)
        )
        self.wait(0.3)
        
        # Clean up step 3
        self.play(FadeOut(step3_title, run_time=0.3))
        self.wait(0.1)
        
        # Step 4: Factor left side
        step4_title = Text("Factor Perfect Square", font_size=26, color=BLUE_C)
        step4_title.next_to(eq1, DOWN, buff=0.5)
        
        # Show the perfect square pattern
        pattern_text = MathTex("a^2 + 2ab + b^2 = (a + b)^2", font_size=22, color=PURPLE)
        pattern_text.next_to(step4_title, DOWN, buff=0.3)
        
        # Highlight the left side terms - properly aligned
        left_highlight = SurroundingRectangle(VGroup(eq1[0], eq1[1], eq1[2], eq1[3], eq1[4]), color=BLUE_D, buff=0.05)
        
        self.play(Write(step4_title, run_time=0.4))
        self.wait(0.2)
        self.play(Create(left_highlight, run_time=0.3))
        self.wait(0.2)
        self.play(Write(pattern_text, run_time=0.5))
        self.wait(0.4)
        
        eq4 = MathTex("\\left(x + \\frac{b}{2a}\\right)^2", "=", "-\\frac{c}{a}", "+", "\\frac{b^2}{4a^2}", font_size=34)
        eq4.set_color_by_tex_to_color_map({
            "\\left(x + \\frac{b}{2a}\\right)^2": BLUE_D,
            "-\\frac{c}{a}": BLUE_C,
            "\\frac{b^2}{4a^2}": PURPLE
        })
        eq4.move_to(ORIGIN + UP*1.5)
        
        self.play(
            FadeOut(left_highlight, run_time=0.3),
            FadeOut(pattern_text, run_time=0.3),
            Transform(eq1, eq4, run_time=0.5)
        )
        self.wait(0.3)
        
        # Clean up step 4
        self.play(FadeOut(step4_title, run_time=0.3))
        self.wait(0.1)
        
        # Step 5: Simplify right side
        step5_title = Text("Combine Fractions", font_size=26, color=BLUE_C)
        step5_title.next_to(eq1, DOWN, buff=0.5)
        
        # Show the fraction combination process
        fraction_steps = MathTex("-\\frac{c}{a} + \\frac{b^2}{4a^2} = \\frac{b^2 - 4ac}{4a^2}", font_size=20, color=PURPLE)
        fraction_steps.next_to(step5_title, DOWN, buff=0.3)
        
        # Highlight the entire right side - properly aligned
        right_highlight = SurroundingRectangle(VGroup(eq1[2], eq1[3], eq4[4]), color=TEAL_D, buff=0.1)
        
        self.play(Write(step5_title, run_time=0.4))
        self.wait(0.2)
        self.play(Create(right_highlight, run_time=0.3))
        self.wait(0.2)
        self.play(Write(fraction_steps, run_time=0.5))
        self.wait(0.4)
        
        eq5 = MathTex("\\left(x + \\frac{b}{2a}\\right)^2", "=", "\\frac{b^2 - 4ac}{4a^2}", font_size=34)
        eq5.set_color_by_tex_to_color_map({
            "\\left(x + \\frac{b}{2a}\\right)^2": BLUE_D,
            "\\frac{b^2 - 4ac}{4a^2}": TEAL_D
        })
        eq5.move_to(ORIGIN + UP*1.5)
        
        self.play(
            FadeOut(right_highlight, run_time=0.3),
            FadeOut(fraction_steps, run_time=0.3),
            Transform(eq1, eq5, run_time=0.5)
        )
        self.wait(0.3)
        
        # Clean up step 5
        self.play(FadeOut(step5_title, run_time=0.3))
        self.wait(0.1)
        
        # Step 6: Take square root
        step6_title = Text("Take Square Root", font_size=26, color=BLUE_C)
        step6_title.next_to(eq1, DOWN, buff=0.5)
        
        # Show square root simplification
        sqrt_steps = MathTex("\\sqrt{\\frac{b^2 - 4ac}{4a^2}} = \\frac{\\sqrt{b^2 - 4ac}}{2a}", font_size=20, color=PURPLE)
        sqrt_steps.next_to(step6_title, DOWN, buff=0.3)
        
        self.play(Write(step6_title, run_time=0.4))
        self.wait(0.2)
        self.play(Write(sqrt_steps, run_time=0.5))
        self.wait(0.4)
        
        eq6 = MathTex("x + \\frac{b}{2a}", "=", "\\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}", font_size=34)
        eq6.set_color_by_tex_to_color_map({
            "x + \\frac{b}{2a}": BLUE_D,
            "\\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}": TEAL_D
        })
        eq6.move_to(ORIGIN + UP*1.5)
        
        self.play(
            FadeOut(sqrt_steps, run_time=0.3),
            Transform(eq1, eq6, run_time=0.5)
        )
        self.wait(0.3)
        
        # Clean up step 6
        self.play(FadeOut(step6_title, run_time=0.3))
        self.wait(0.1)
        
        # Step 7: Solve for x
        step7_title = Text("Solve for x", font_size=26, color=BLUE_C)
        step7_title.next_to(eq1, DOWN, buff=0.5)
        
        # Show the subtraction step
        subtract_steps = MathTex("x = \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a} - \\frac{b}{2a}", font_size=20, color=PURPLE)
        subtract_steps.next_to(step7_title, DOWN, buff=0.3)
        
        self.play(Write(step7_title, run_time=0.4))
        self.wait(0.2)
        self.play(Write(subtract_steps, run_time=0.5))
        self.wait(0.4)
        
        # Show final combination
        final_steps = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=22, color=PURPLE)
        final_steps.next_to(subtract_steps, DOWN, buff=0.3)
        
        self.play(Write(final_steps, run_time=0.5))
        self.wait(0.4)
        
        # Clean up step 7 - ensure it disappears before final reveal
        self.play(FadeOut(step7_title, run_time=0.3), FadeOut(title, run_time=0.3))
        self.wait(0.2)

        # Final formula with dramatic entrance - centered for mobile
        final_formula = MathTex("x", "=", "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=42)
        final_formula.set_color_by_tex_to_color_map({
            "x": WHITE,
            "=": WHITE,
            "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}": TEAL_D
        })
        final_formula.move_to(ORIGIN + UP*0.2)
        
        self.play(
            FadeOut(subtract_steps, run_time=0.3),
            FadeOut(final_steps, run_time=0.3),
            Transform(eq1, final_formula, run_time=0.7)
        )
        self.wait(0.3)
        
        # Add highlight box around final formula - properly aligned
        highlight_box = SurroundingRectangle(
            eq1, 
            color=TEAL_D, 
            buff=0.4, 
            corner_radius=0.2
        )
        highlight_box.set_stroke(width=5)
        
        # Final celebration
        self.play(Create(highlight_box, run_time=0.5))
        
        # Pulse effect on final formula
        self.play(
            eq1.animate.scale(1.1).set_color(BLUE_C),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        # End screen text
        end_text = Text("The Quadratic Formula!", font_size=28, color=TEAL_D)
        end_text.next_to(eq1, DOWN, buff=0.8)
        
        self.play(Write(end_text, run_time=0.5))
        self.wait(1.0)