from manim import *
import random

class LimitMatchCutAnimation(Scene):
    def construct(self):
        # Set black background
        self.camera.background_color = BLACK
        
        # Comprehensive background expressions for limits in calculus
        self.background_expressions = [
            # Basic limit notation
            r"\lim", r"\lim_{x \to a}", r"\lim_{x \to 0}", r"\lim_{x \to \infty}", r"\lim_{x \to -\infty}",
            r"\lim_{h \to 0}", r"\lim_{t \to 0}", r"\lim_{n \to \infty}", r"\lim_{x \to c}",
            
            # Specific limit values
            r"x \to 0", r"x \to 1", r"x \to \infty", r"x \to -\infty", r"x \to a", r"x \to c",
            r"h \to 0", r"t \to 0", r"n \to \infty", r"u \to a", r"v \to b",
            
            # Common limit expressions
            r"\frac{\sin x}{x}", r"\frac{1-\cos x}{x}", r"\frac{e^x - 1}{x}", r"\frac{\ln(1+x)}{x}",
            r"\frac{x^2 - 1}{x - 1}", r"\frac{x^3 - 8}{x - 2}", r"\frac{\sqrt{x} - 1}{x - 1}",
            
            # Infinity expressions
            r"\infty", r"-\infty", r"+\infty", r"\frac{1}{\infty}", r"\frac{\infty}{\infty}",
            r"0 \cdot \infty", r"\infty - \infty", r"1^\infty", r"0^0", r"\infty^0",
            
            # L'Hôpital related
            r"\frac{0}{0}", r"\frac{\infty}{\infty}", r"f'(x)", r"g'(x)", r"\frac{f'(x)}{g'(x)}",
            
            # Continuity and limits
            r"f(a)", r"f(x)", r"g(x)", r"h(x)", r"f(a^-)", r"f(a^+)",
            r"\epsilon", r"\delta", r"|x - a|", r"|f(x) - L|", r"< \epsilon", r"< \delta",
            
            # Sequences and series
            r"a_n", r"b_n", r"s_n", r"\{a_n\}", r"\sum_{n=1}^{\infty}", r"\sum a_n",
            r"n \to \infty", r"n = 1, 2, 3, ...", r"a_{n+1}", r"a_1, a_2, a_3, ...",
            
            # Squeeze theorem
            r"g(x) \leq f(x) \leq h(x)", r"g(x)", r"h(x)", r"f(x)",
            
            # Common functions in limits
            r"\sin x", r"\cos x", r"\tan x", r"e^x", r"\ln x", r"x^n", r"\sqrt{x}",
            r"\frac{1}{x}", r"\frac{1}{x^2}", r"x^2", r"x^3", r"|x|", r"\sqrt[n]{x}",
            
            # Trigonometric limits
            r"\sin", r"\cos", r"\tan", r"\sec", r"\csc", r"\cot",
            r"\sin(x)", r"\cos(x)", r"\sin(2x)", r"\cos(3x)", r"\tan(x/2)",
            
            # Variables and constants
            r"x", r"y", r"t", r"h", r"u", r"v", r"a", r"b", r"c", r"L", r"M",
            r"0", r"1", r"2", r"3", r"-1", r"-2", r"\pi", r"e",
            
            # Greek letters common in limits
            r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\theta", r"\lambda",
            
            # Operations and symbols
            r"+", r"-", r"\cdot", r"\times", r"\div", r"=", r"\neq", r"<", r">", r"\leq", r"\geq",
            r"\pm", r"\mp", r"\to", r"\rightarrow", r"\leftarrow", r"\mapsto",
            
            # Absolute values and norms
            r"|x|", r"|f(x)|", r"||x||", r"|a_n|", r"|\sin x|", r"|\cos x|",
            
            # Rational functions
            r"\frac{1}{x}", r"\frac{x}{x+1}", r"\frac{x^2}{x-1}", r"\frac{1}{x^2+1}",
            r"\frac{x^2-1}{x+1}", r"\frac{2x+1}{x-3}", r"\frac{x^3+1}{x^2-4}",
            
            # Exponential and logarithmic
            r"e^x", r"e^{-x}", r"2^x", r"a^x", r"\ln x", r"\log x", r"\log_2 x",
            r"e^{1/x}", r"\ln(x+1)", r"x e^x", r"\frac{\ln x}{x}",
            
            # Powers and roots
            r"x^2", r"x^3", r"x^n", r"x^{1/2}", r"x^{-1}", r"x^{1/n}",
            r"\sqrt{x}", r"\sqrt{x+1}", r"\sqrt{x^2+1}", r"\sqrt[3]{x}", r"\sqrt[n]{x}",
            
            # Piecewise and step functions
            r"f(x) = \begin{cases}", r"\text{if } x > 0", r"\text{if } x < 0", r"\text{if } x = 0",
            
            # Additional limit context
            r"DNE", r"\text{undefined}", r"\text{exists}", r"\text{continuous}",
            r"L", r"M", r"K", r"C", r"A", r"B"
        ]
        
        # Organize limit expressions by type and complexity
        
        # Section 1: Basic limit notation
        basic_limits = [
            r"\lim_{x \to 0} f(x)",
            r"\lim_{x \to 1} g(x)", 
            r"\lim_{x \to a} h(x)",
            r"\lim_{t \to 0} f(t)",
            r"\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"\lim_{n \to \infty} a_n",
            r"\lim_{x \to c} (ax + b)",
            r"\lim_{x \to 0^+} f(x)",
            r"\lim_{x \to 0^-} g(x)",
        ]
        
        # Section 2: Infinity limits
        infinity_limits = [
            r"\lim_{x \to \infty} f(x)",
            r"\lim_{x \to -\infty} g(x)",
            r"\lim_{x \to \infty} \frac{1}{x}",
            r"\lim_{x \to \infty} \frac{x^2}{x^3 + 1}",
            r"\lim_{n \to \infty} \frac{1}{n}",
            r"\lim_{x \to \infty} e^{-x}",
            r"\lim_{x \to \infty} \frac{\sin x}{x}",
            r"\lim_{x \to \infty} (1 + \frac{1}{x})^x",
        ]
        
        # Section 3: Indeterminate forms 0/0
        zero_over_zero = [
            r"\lim_{x \to 0} \frac{\sin x}{x}",
            r"\lim_{x \to 0} \frac{1 - \cos x}{x^2}",
            r"\lim_{x \to 0} \frac{e^x - 1}{x}",
            r"\lim_{x \to 0} \frac{\ln(1+x)}{x}",
            r"\lim_{x \to 1} \frac{x^2 - 1}{x - 1}",
            r"\lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}",
            r"\lim_{x \to 2} \frac{x^3 - 8}{x - 2}",
            r"\lim_{x \to 0} \frac{\tan x}{x}",
        ]
        
        # Section 4: Indeterminate forms ∞/∞
        infinity_over_infinity = [
            r"\lim_{x \to \infty} \frac{3x^2 + 1}{2x^2 - x}",
            r"\lim_{x \to \infty} \frac{x^3}{e^x}",
            r"\lim_{x \to \infty} \frac{\ln x}{x}",
            r"\lim_{x \to \infty} \frac{x^n}{e^x}",
            r"\lim_{x \to \infty} \frac{2x^3 - x}{x^3 + 5}",
            r"\lim_{x \to \infty} \frac{\sqrt{x}}{x}",
            r"\lim_{x \to \infty} \frac{x^2 + 3x}{2x^2 + 1}",
        ]
        
        # Section 5: Trigonometric limits
        trig_limits = [
            r"\lim_{x \to 0} \frac{\sin x}{x}",
            r"\lim_{x \to 0} \frac{\tan x}{x}",
            r"\lim_{x \to 0} \frac{1 - \cos x}{x^2}",
            r"\lim_{x \to 0} \frac{\sin(3x)}{x}",
            r"\lim_{x \to \pi} \frac{\sin x}{x - \pi}",
            r"\lim_{x \to 0} \frac{\sin(ax)}{\sin(bx)}",
            r"\lim_{x \to 0} \cos x",
            r"\lim_{x \to \infty} \sin x",
        ]
        
        # Section 6: Exponential and logarithmic limits
        exp_log_limits = [
            r"\lim_{x \to 0} \frac{e^x - 1}{x}",
            r"\lim_{x \to \infty} e^{-x}",
            r"\lim_{x \to 0^+} x \ln x",
            r"\lim_{x \to \infty} \frac{\ln x}{x}",
            r"\lim_{x \to 1} \frac{\ln x}{x - 1}",
            r"\lim_{x \to \infty} (1 + \frac{1}{x})^x",
            r"\lim_{x \to 0} (1 + x)^{1/x}",
            r"\lim_{x \to \infty} x e^{-x}",
        ]
        
        # Section 7: Squeeze theorem examples
        squeeze_limits = [
            r"\lim_{x \to 0} x^2 \sin(\frac{1}{x})",
            r"\lim_{x \to \infty} \frac{\sin x}{x}",
            r"\lim_{x \to 0} x \cos(\frac{1}{x})",
            r"\lim_{n \to \infty} \frac{\sin n}{n}",
            r"\lim_{x \to 0} \sqrt{x} \sin(\frac{1}{x})",
        ]
        
        # Section 8: One-sided limits
        one_sided_limits = [
            r"\lim_{x \to 0^+} \frac{1}{x}",
            r"\lim_{x \to 0^-} \frac{1}{x}",
            r"\lim_{x \to 0^+} \ln x",
            r"\lim_{x \to 1^-} \frac{1}{x-1}",
            r"\lim_{x \to 2^+} \frac{x}{x-2}",
            r"\lim_{x \to 0^+} \sqrt{x}",
        ]
        
        # Section 9: Piecewise function limits
        piecewise_limits = [
            r"\lim_{x \to 0} |x|",
            r"\lim_{x \to 0} \frac{|x|}{x}",
            r"\lim_{x \to 1} \text{floor}(x)",
            r"\lim_{x \to 0} \text{sgn}(x)",
        ]
        
        # Section 10: Special limits
        special_limits = [
            r"\lim_{n \to \infty} \sqrt[n]{n}",
            r"\lim_{n \to \infty} \frac{n!}{n^n}",
            r"\lim_{x \to 0} \frac{\sin x - x}{x^3}",
            r"\lim_{x \to \infty} x(\sqrt{x+1} - \sqrt{x})",
            r"\lim_{n \to \infty} (1 + \frac{1}{n})^n",
        ]
        
        # Combine all sections with their properties
        sections = [
            ("Basic Limits", basic_limits, BLUE, "basic"),
            ("Infinity Limits", infinity_limits, GREEN, "infinity"), 
            ("Zero Over Zero", zero_over_zero, RED, "indeterminate"),
            ("Infinity Over Infinity", infinity_over_infinity, YELLOW, "indeterminate"),
            ("Trigonometric Limits", trig_limits, PURPLE, "trigonometric"),
            ("Exponential/Log Limits", exp_log_limits, ORANGE, "exponential"),
            ("Squeeze Theorem", squeeze_limits, PINK, "squeeze"),
            ("One-Sided Limits", one_sided_limits, TEAL_A, "one_sided"),
            ("Piecewise Limits", piecewise_limits, GOLD, "piecewise"),
            ("Special Limits", special_limits, GRAY_A, "special")
        ]
        
        current = None
        current_background = []  # Track current background expressions
        
        for section_name, expressions, color, limit_type in sections:
            for i, expr in enumerate(expressions):
                next_limit = MathTex(expr, font_size=72, color=color)
                
                # Clear previous background and add new dense one focused on limits
                self.clear_and_add_dense_background(current_background)
                
                if current is None:
                    # First expression overall - align left edge to fixed position
                    FIXED_LEFT_POSITION = -2.0
                    next_limit.move_to(ORIGIN)
                    left_edge_x = next_limit.get_left()[0]
                    shift_amount = FIXED_LEFT_POSITION - left_edge_x
                    next_limit.shift([shift_amount, 0, 0])
                    
                    current = next_limit
                    self.play(DrawBorderThenFill(current), run_time=1.2)
                    self.wait(0.3)
                else:
                    # Create perfect match cut by aligning the "lim" symbol position
                    self.align_limit_symbol(current, next_limit)
                    
                    # Vary timing within sections
                    if i == 0:  # First in new section
                        run_time = 1.0
                        wait_time = 0.6
                    else:  # Within section
                        run_time = 0.6
                        wait_time = 0.2
                    
                    self.play(
                        Transform(current, next_limit),
                        run_time=run_time
                    )
                    self.wait(wait_time)
        
        # Final cleanup of background expressions
        self.clear_background(current_background)
        
        # Final dramatic sequence with ultra-dense background
        self.add_ultra_dense_background()
        self.wait(1)
        
        # Scale up final expression - keep centered
        self.play(
            current.animate.scale(1.4).move_to(ORIGIN).set_color(GOLD),
            run_time=1.5
        )
        
        # Pulsing effect - maintain center
        for _ in range(3):
            self.play(
                current.animate.scale(1.15).move_to(ORIGIN),
                run_time=0.25
            )
            self.play(
                current.animate.scale(1/1.15).move_to(ORIGIN),
                run_time=0.25
            )
        
        self.wait(0.5)
        
        # Transform to showcase main limit notations
        basic_limit = MathTex(r"\lim_{x \to a}", font_size=200, color=BLUE)
        basic_limit.move_to(ORIGIN)
        self.play(
            Transform(current, basic_limit),
            run_time=1.5
        )
        self.wait(1)
        
        # Switch to infinity limit
        infinity_limit = MathTex(r"\lim_{x \to \infty}", font_size=200, color=RED)
        infinity_limit.move_to(ORIGIN)
        self.play(
            Transform(current, infinity_limit),
            run_time=1.5
        )
        self.wait(1)
        
        # Switch to derivative definition limit
        derivative_limit = MathTex(r"\lim_{h \to 0}", font_size=200, color=GREEN)
        derivative_limit.move_to(ORIGIN)
        self.play(
            Transform(current, derivative_limit),
            run_time=1.5
        )
        
        # Final rotation and color effects
        self.play(
            Rotate(current, 2*PI, about_point=ORIGIN),
            current.animate.set_color(GOLD),
            run_time=3
        )
        
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(current), run_time=2)
    
    def align_limit_symbol(self, current_expr, next_expr):
        """Position expressions consistently for match cut effect"""
        # Simple approach: just position all expressions with their left edge 
        # at the same fixed position. This keeps "lim" symbols aligned.
        FIXED_LEFT_POSITION = -2.0  # Fixed x-coordinate for left edge
        
        # Get the left edge of the next expression
        next_expr.move_to(ORIGIN)  # Reset position first
        left_edge_x = next_expr.get_left()[0]
        
        # Calculate how much to shift to align the left edges
        shift_amount = FIXED_LEFT_POSITION - left_edge_x
        next_expr.shift([shift_amount, 0, 0])
    
    def clear_and_add_dense_background(self, current_background):
        """Clear current background and add dense limit expressions"""
        # Remove current background expressions
        self.clear_background(current_background)
        
        # Add dense background - 25-35 expressions per transition
        num_expressions = random.randint(25, 35)
        
        for _ in range(num_expressions):
            # Choose random limit expression
            expression = random.choice(self.background_expressions) 
            
            try:
                # Create expression with 70% opacity
                bg_expr = MathTex(expression, font_size=random.randint(12, 28), color=WHITE)
                bg_expr.set_opacity(0.7)  # Fixed 70% opacity
                
                # Position in horizontal center third only
                x_pos = random.uniform(-2.5, 2.5)  # Center third horizontally
                y_pos = random.uniform(-4, 4)  # Full screen height
                
                # Avoid the center area where main expression is
                if -1.5 < x_pos < 1.5 and -1 < y_pos < 1:
                    if random.choice([True, False]):
                        x_pos = random.uniform(-2.5, -1.8) if x_pos < 0 else random.uniform(1.8, 2.5)
                    else:
                        y_pos = random.uniform(-4, -1.5) if y_pos < 0 else random.uniform(1.5, 4)
                
                bg_expr.move_to([x_pos, y_pos, 0])
                
                # Add random slight rotation for more dynamic look
                if random.random() < 0.3:  # 30% chance
                    bg_expr.rotate(random.uniform(-0.2, 0.2))
                
                # Add instantly without animation for synchronization
                self.add(bg_expr)
                current_background.append(bg_expr)
                
            except:
                # Skip if expression causes issues
                continue
    
    def add_ultra_dense_background(self):
        """Add ultra-dense background for finale"""
        num_expressions = 50  # Maximum density
        
        for _ in range(num_expressions):
            expression = random.choice(self.background_expressions)
            
            try:
                bg_expr = MathTex(expression, font_size=random.randint(10, 24), color=WHITE)
                bg_expr.set_opacity(0.7)  # Fixed 70% opacity
                
                # Cover horizontal center third only
                x_pos = random.uniform(-2.5, 2.5)  # Center third horizontally
                y_pos = random.uniform(-4.5, 4.5)
                
                # Create exclusion zones around center
                if -2 < x_pos < 2 and -1.5 < y_pos < 1.5:
                    # Push to edges within center third
                    if abs(x_pos) > abs(y_pos):
                        x_pos = random.uniform(-2.5, -2.2) if x_pos < 0 else random.uniform(2.2, 2.5)
                    else:
                        y_pos = random.uniform(-4.5, -2) if y_pos < 0 else random.uniform(2, 4.5)
                
                bg_expr.move_to([x_pos, y_pos, 0])
                
                # More rotation variety for finale
                if random.random() < 0.4:
                    bg_expr.rotate(random.uniform(-0.3, 0.3))
                
                self.add(bg_expr)
                
            except:
                continue
    
    def clear_background(self, current_background):
        """Remove all current background expressions instantly"""
        for expr in current_background:
            self.remove(expr)
        current_background.clear()