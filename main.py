from manim import *
import numpy as np
import math

class TaylorSeriesExponential(Scene):
    def construct(self):
        # Set up the coordinate system - smaller and centered with sleek gradient aesthetic
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 7, 1],
            x_length=4,  # Reduced from 8
            y_length=2.5,  # Reduced from 5
            axis_config={
                "color": WHITE, 
                "stroke_width": 2, 
                "include_ticks": False,
                "tip_length": 0.15,  # Make arrow tips smaller
                "tip_width": 0.15    # Make arrow tips smaller
            },
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        )
        axes.move_to(ORIGIN)  # Center the axes
        
        # Title - positioned in center third with original blue color and double struck font for first letters
        title = MathTex(r"\mathbb{T}\text{aylor }\mathbb{S}\text{eries of }e^x", font_size=32, color="#4A90E2")
        title.move_to(UP * 2)
        
        # The actual exponential function - start with ending gradient color
        exp_func = axes.plot(lambda x: np.exp(x), color="#E67E22", stroke_width=2, stroke_opacity=0.8)
        exp_label = MathTex(r"e^x", color="#E67E22", font_size=36)  # Made bigger as requested
        exp_label.next_to(exp_func.get_end(), UP)
        
        # Taylor series terms
        def taylor_term(x, n):
            result = 0
            for k in range(n + 1):
                result += (x**k) / math.factorial(k)
            return result
        
        # Function to get gradient color based on progress (purple to orange)
        def get_gradient_color(progress):
            # Progress from 0 to 1
            # Purple: #8E44AD, Orange: #E67E22
            purple = np.array([142, 68, 173]) / 255
            orange = np.array([230, 126, 34]) / 255
            color = purple * (1 - progress) + orange * progress
            return rgb_to_hex(color)
        
        # Setup scene - slower for 20 second total
        self.play(
            Create(axes),
            Write(title),
            run_time=1.5
        )
        
        # Show target function
        self.play(
            Create(exp_func),
            Write(exp_label),
            run_time=1.5
        )
        
        # Show initial formula with red color from reference
        intro_text = MathTex(
            r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
            font_size=30,
            color="#E74C3C"
        )
        intro_text.move_to(DOWN * 2)
        self.play(Write(intro_text), run_time=1.5)
        
        # Wait before starting approximations
        self.wait(0.5)
        
        # Remove intro text
        self.play(FadeOut(intro_text), run_time=0.5)
        
        # Create static base part that won't change
        base_part = MathTex(r"P_0(x) = 1", color=get_gradient_color(0), font_size=22)
        base_part.move_to(DOWN * 2.2)
        
        # Initialize with first approximation
        current_approx = axes.plot(
            lambda x: taylor_term(x, 0),
            color=get_gradient_color(0),
            stroke_width=4,
            x_range=[-2, 2]
        )
        
        # Show first approximation
        self.play(
            Create(current_approx),
            Write(base_part),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Now we'll build up the equation smoothly
        # P_1: 1 + x
        new_approx = axes.plot(lambda x: taylor_term(x, 1), color=get_gradient_color(0.1), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_1(x) = 1 + x", color=get_gradient_color(0.1), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.8
        )
        self.wait(0.4)
        
        # P_2: 1 + x + x²/2
        new_approx = axes.plot(lambda x: taylor_term(x, 2), color=get_gradient_color(0.2), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_2(x) = 1 + x + \frac{x^2}{2}", color=get_gradient_color(0.2), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.7
        )
        self.wait(0.3)
        
        # P_3: 1 + x + x²/2 + x³/6
        new_approx = axes.plot(lambda x: taylor_term(x, 3), color=get_gradient_color(0.3), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_3(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6}", color=get_gradient_color(0.3), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.6
        )
        self.wait(0.25)
        
        # Now create the base part that stays constant with shorter notation
        static_base = MathTex(r"P_4(x) = 1 + x + \frac{x^2}{2} + \cdots + ", color=get_gradient_color(0.4), font_size=22)
        changing_term = MathTex(r"\frac{x^4}{24}", color=get_gradient_color(0.4), font_size=22)
        
        # Position them to form one equation
        static_base.move_to(DOWN * 2.2)
        changing_term.next_to(static_base, RIGHT, buff=0.05)
        
        # Create equation group
        equation_group = VGroup(static_base, changing_term)
        equation_group.move_to(DOWN * 2.2)
        
        # P_4 with the new format
        new_approx = axes.plot(lambda x: taylor_term(x, 4), color=get_gradient_color(0.4), stroke_width=4, x_range=[-2, 2])
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, equation_group),
            run_time=0.5
        )
        self.wait(0.2)
        
        # Now smoothly morph only the changing parts for P_5 through P_15
        for n in range(5, 16):
            # Create new approximation with gradient color
            progress = n / 15  # Progress from 0 to 1
            color = get_gradient_color(progress)
            
            new_approx = axes.plot(
                lambda x: taylor_term(x, n),
                color=color,
                stroke_width=4,
                x_range=[-2, 2]
            )
            
            # Create new static part with updated P_n - use compact notation and consistent font size
            new_static_base = MathTex(f"P_{{{n}}}(x) = 1 + x + \\frac{{x^2}}{{2}} + \\cdots + ", color=color, font_size=22)
            
            # Generate factorial for the last term
            factorial_n = math.factorial(n)
            new_changing_term = MathTex(f"\\frac{{x^{{{n}}}}}{{{factorial_n}}}", color=color, font_size=22)
            
            # Position them
            new_static_base.move_to(DOWN * 2.2)
            new_changing_term.next_to(new_static_base, RIGHT, buff=0.02)
            
            # Create new equation group
            new_equation_group = VGroup(new_static_base, new_changing_term)
            new_equation_group.move_to(DOWN * 2.2)
            
            # Morph with decreasing time
            run_time = max(0.1, 0.4 - (n-5) * 0.03)
            wait_time = max(0.02, 0.15 - (n-5) * 0.01)
            
            self.play(
                Transform(current_approx, new_approx),
                Transform(base_part, new_equation_group),
                run_time=run_time
            )
            self.wait(wait_time)
        
        # Dramatic pause
        self.wait(0.5)
        
        # Fade out ALL elements including the final approximation curve
        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(exp_func),
            FadeOut(exp_label),
            FadeOut(base_part),
            FadeOut(current_approx),  # Added this line to fade out the last graph
            run_time=0.8
        )
        
        # Brief pause for dramatic effect
        self.wait(0.2)
        
        # Final reveal - centered in middle of screen with proper sizing
        final_formula = MathTex(
            r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
            color="#E67E22",  # Final orange color
            font_size=48  # Larger for dramatic effect
        )
        final_formula.move_to(ORIGIN)  # Center of screen
        
        # Dramatic entrance of the final formula
        self.play(
            FadeIn(final_formula, scale=0.8),
            run_time=1.0
        )
        
        # Hold the final result
        self.wait(1.0)
        
        # Fade everything to black
        self.play(
            FadeOut(final_formula),
            run_time=1.0
        )
        
        # Final black screen
        self.wait(0.5)