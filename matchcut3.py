from manim import *
import random

class ExtendedIntegralMatchCut(Scene):
    def construct(self):
        # Set black background
        self.camera.background_color = BLACK
        
        # Background expressions for integrals
        self.background_expressions = [
            # Basic integral symbols and notation
            r"\int", r"\iint", r"\iiint", r"\oint", r"dx", r"dy", r"dz", r"dt", r"du", r"dv",
            r"dr", r"d\theta", r"ds", r"dA", r"dV", r"dS", r"d\mathbf{r}",
            
            # Variables and limits
            r"x", r"y", r"z", r"t", r"u", r"v", r"a", r"b", r"c", r"n", r"r", r"\theta",
            r"0", r"1", r"2", r"\pi", r"e", r"\infty", r"-\infty", r"\pi/2", r"2\pi",
            
            # Common functions in integrals
            r"x^2", r"x^3", r"x^n", r"\sqrt{x}", r"\frac{1}{x}", r"e^x", r"e^{-x}",
            r"\sin x", r"\cos x", r"\tan x", r"\ln x", r"x^{-1}", r"|x|",
            
            # Fractions and rational functions
            r"\frac{1}{x^2}", r"\frac{1}{x+1}", r"\frac{x}{x^2+1}", r"\frac{1}{\sqrt{x}}",
            r"\frac{dx}{x}", r"\frac{du}{u}", r"\frac{dt}{t}",
            
            # Trigonometric expressions
            r"\sin", r"\cos", r"\tan", r"\sec", r"\csc", r"\cot",
            r"\sin^2", r"\cos^2", r"\sin(2x)", r"\cos(3x)",
            
            # Exponential and logarithmic
            r"e^{ax}", r"a^x", r"\log x", r"\ln(x+1)", r"xe^x", r"x\ln x",
            
            # Integral bounds and limits
            r"_0^1", r"_0^\infty", r"_{-\infty}^\infty", r"_a^b", r"_0^\pi", r"_0^{2\pi}",
            
            # Multiple integral regions
            r"_D", r"_R", r"_V", r"_S", r"_C", r"_\Gamma", r"_{\partial D}",
            
            # Vector calculus
            r"\mathbf{F}", r"\mathbf{r}", r"\mathbf{n}", r"\nabla", r"\nabla \cdot", r"\nabla \times",
            
            # Greek letters
            r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\omega", r"\lambda",
            r"\mu", r"\sigma", r"\phi", r"\psi", r"\chi",
            
            # Operations and symbols
            r"+", r"-", r"\cdot", r"=", r"\neq", r"<", r">", r"\leq", r"\geq",
            r"\pm", r"\mp", r"\to", r"\rightarrow",
            
            # Special functions and constants
            r"\Gamma", r"B", r"J_n", r"Y_n", r"P_n", r"L_n", r"H_n",
            
            # Calculus expressions
            r"F(x)", r"f(x)", r"g(x)", r"h(x)", r"f'(x)", r"g'(x)",
            
            # Complex analysis
            r"z", r"w", r"i", r"\Re", r"\Im", r"|z|", r"\arg(z)",
            
            # Additional integral context
            r"C", r"C^1", r"C^\infty", r"L^1", r"L^2", r"L^p"
        ]
        
        # Comprehensive list of integral expressions organized by complexity
        integral_expressions = [
            # Basic indefinite integrals
            r"\int x \, dx",
            r"\int x^2 \, dx",
            r"\int x^3 \, dx",
            r"\int \frac{1}{x} \, dx",
            r"\int \sqrt{x} \, dx",
            r"\int x^{-1/2} \, dx",
            r"\int x^n \, dx",
            
            # Trigonometric integrals
            r"\int \sin(x) \, dx",
            r"\int \cos(x) \, dx",
            r"\int \tan(x) \, dx",
            r"\int \sec(x) \, dx",
            r"\int \csc(x) \, dx",
            r"\int \cot(x) \, dx",
            r"\int \sec^2(x) \, dx",
            r"\int \sin^2(x) \, dx",
            r"\int \cos^2(x) \, dx",
            r"\int \sin(x)\cos(x) \, dx",
            
            # Exponential and logarithmic
            r"\int e^x \, dx",
            r"\int e^{-x} \, dx",
            r"\int e^{ax} \, dx",
            r"\int a^x \, dx",
            r"\int \ln(x) \, dx",
            r"\int \log_a(x) \, dx",
            r"\int xe^x \, dx",
            r"\int x\ln(x) \, dx",
            
            # Definite integrals - simple
            r"\int_{0}^{1} x \, dx",
            r"\int_{0}^{1} x^2 \, dx",
            r"\int_{-1}^{1} x^3 \, dx",
            r"\int_{0}^{\pi} \sin(x) \, dx",
            r"\int_{0}^{2\pi} \cos(x) \, dx",
            r"\int_{0}^{\pi/2} \cos^2(x) \, dx",
            
            # Definite integrals - intermediate
            r"\int_{1}^{e} \frac{1}{x} \, dx",
            r"\int_{0}^{\infty} e^{-x} \, dx",
            r"\int_{-\infty}^{\infty} e^{-x^2} \, dx",
            r"\int_{0}^{1} \frac{1}{\sqrt{x}} \, dx",
            r"\int_{0}^{1} \frac{1}{\sqrt{1-x^2}} \, dx",
            
            # Rational functions
            r"\int \frac{1}{x^2+1} \, dx",
            r"\int \frac{1}{x^2-1} \, dx",
            r"\int \frac{x}{x^2+1} \, dx",
            r"\int \frac{1}{(x+1)^2} \, dx",
            r"\int \frac{2x+1}{x^2+x+1} \, dx",
            
            # Integration by parts examples
            r"\int x e^x \, dx",
            r"\int x \sin(x) \, dx",
            r"\int x^2 e^x \, dx",
            r"\int e^x \cos(x) \, dx",
            r"\int \ln(x) \, dx",
            
            # Substitution examples
            r"\int \sin(2x) \, dx",
            r"\int \cos(3x+1) \, dx",
            r"\int (2x+1)^5 \, dx",
            r"\int \frac{2x}{x^2+1} \, dx",
            r"\int x\sqrt{x^2+1} \, dx",
            
            # Multiple integrals
            r"\iint_D f(x,y) \, dA",
            r"\iint_D xy \, dA",
            r"\iint_R (x^2+y^2) \, dA",
            r"\iiint_V f(x,y,z) \, dV",
            r"\iiint_V xyz \, dV",
            r"\iiint_V \sqrt{x^2+y^2+z^2} \, dV",
            
            # Line integrals
            r"\oint_C f(x,y) \, ds",
            r"\oint_C \mathbf{F} \cdot d\mathbf{r}",
            r"\oint_C P \, dx + Q \, dy",
            r"\oint_C (x^2+y^2) \, ds",
            
            # Surface integrals
            r"\iint_S f(x,y,z) \, dS",
            r"\iint_S \mathbf{F} \cdot \mathbf{n} \, dS",
            r"\iint_S (x^2+y^2+z^2) \, dS",
            
            # Special functions and advanced
            r"\int_0^\infty \frac{\sin(x)}{x} \, dx",
            r"\int_0^1 \frac{\ln(x)}{\sqrt{1-x^2}} \, dx",
            r"\int_{-\infty}^{\infty} \frac{1}{1+x^2} \, dx",
            r"\int_0^{\pi/2} \sqrt{\sin(x)} \, dx",
            r"\int_0^{\infty} x^n e^{-x} \, dx",
            
            # Improper integrals
            r"\int_1^{\infty} \frac{1}{x^2} \, dx",
            r"\int_0^{\infty} \frac{1}{1+x^2} \, dx",
            r"\int_{-\infty}^{\infty} \frac{x}{1+x^4} \, dx",
            r"\int_0^1 \frac{1}{\sqrt{1-x}} \, dx",
            
            # Complex analysis
            r"\oint_C f(z) \, dz",
            r"\oint_C \frac{1}{z} \, dz",
            r"\oint_C \frac{1}{z-a} \, dz",
            r"\oint_C z^n \, dz",
            r"\oint_C e^z \, dz",
            
            # Vector calculus
            r"\oint_C \nabla f \cdot d\mathbf{r}",
            r"\iint_S \nabla \times \mathbf{F} \cdot \mathbf{n} \, dS",
            r"\iiint_V \nabla \cdot \mathbf{F} \, dV",
            
            # Parametric and polar
            r"\int_0^{2\pi} r^2 \, d\theta",
            r"\int_0^a \int_0^{\sqrt{a^2-x^2}} y \, dy \, dx",
            r"\int_0^{2\pi} \int_0^a r^3 \, dr \, d\theta",
            
            # Series and transforms
            r"\int_{-\infty}^{\infty} f(x) e^{-i\omega x} \, dx",
            r"\int_0^{\infty} f(t) e^{-st} \, dt",
            r"\sum_{n=0}^{\infty} \int_0^1 f_n(x) \, dx",
            
            # Calculus of variations
            r"\int_a^b F(x,y,y') \, dx",
            r"\int_a^b \sqrt{1+(y')^2} \, dx",
            
            # Final complex expressions
            r"\int_0^{\infty} \frac{x^{a-1}}{1+x} \, dx",
            r"\int_{-\infty}^{\infty} \frac{e^{-x^2/2}}{\sqrt{2\pi}} \, dx",
            r"\oint_{\partial D} \frac{\partial u}{\partial n} \, ds",
            r"\int_{\Gamma} \omega",
            r"\int_M \alpha \wedge \beta"
        ]
        
        # Color scheme - cycle through colors for visual variety
        colors = [WHITE, BLUE, GREEN, YELLOW, RED, PURPLE, ORANGE, PINK, 
                 BLUE_A, GREEN_A, GOLD, RED_A, TEAL_A, GRAY_A]
        
        # Track background expressions
        current_background = []
        
        # Create first integral with dramatic entrance
        current_integral = MathTex(integral_expressions[0], font_size=72, color=colors[0])
        
        # Position with fixed left edge for match cut
        FIXED_LEFT_POSITION = -2
        current_integral.move_to(ORIGIN)
        left_edge_x = current_integral.get_left()[0]
        shift_amount = FIXED_LEFT_POSITION - left_edge_x
        current_integral.shift([shift_amount, 0, 0])
        
        # Add initial background
        self.clear_and_add_dense_background(current_background)
        
        self.play(DrawBorderThenFill(current_integral), run_time=1.2)
        self.wait(0.3)
        
        # Match cut transitions through all expressions
        for i in range(1, len(integral_expressions)):
            # Create next integral
            color_index = i % len(colors)
            next_integral = MathTex(integral_expressions[i], font_size=72, color=colors[color_index])
            
            # Position for match cut - align integral symbols using fixed left edge
            next_integral.move_to(ORIGIN)
            left_edge_x = next_integral.get_left()[0]
            shift_amount = FIXED_LEFT_POSITION - left_edge_x
            next_integral.shift([shift_amount, 0, 0])
            
            # Clear and add new background
            self.clear_and_add_dense_background(current_background)
            
            # Vary timing for rhythm - faster for similar expressions, slower for big changes
            if i % 15 == 0:  # Pause every 15 expressions
                run_time = 1.2
                wait_time = 0.8
            elif any(symbol in integral_expressions[i] for symbol in ["iint", "oint", "iiint"]):
                run_time = 0.9  # Slightly slower for complex integrals
                wait_time = 0.4
            else:
                run_time = 0.6
                wait_time = 0.2
            
            # Transform with match cut effect
            self.play(
                Transform(current_integral, next_integral),
                run_time=run_time
            )
            self.wait(wait_time)
        
        # Final cleanup of background expressions
        self.clear_background(current_background)
        
        # Final dramatic sequence with ultra-dense background
        self.add_ultra_dense_background()
        self.wait(1)
        
        # Scale up final expression
        self.play(
            current_integral.animate.scale(1.5).set_color(GOLD),
            run_time=1.5
        )
        
        # Pulsing effect
        for _ in range(2):
            self.play(
                current_integral.animate.scale(1.1),
                run_time=0.3
            )
            self.play(
                current_integral.animate.scale(1/1.1),
                run_time=0.3
            )
        
        self.wait(0.5)
        
        # Transform to giant integral symbol
        giant_integral = MathTex(r"\int", font_size=250, color=WHITE)
        giant_integral.move_to(ORIGIN)
        self.play(
            Transform(current_integral, giant_integral),
            run_time=2
        )
        
        # Final rotation and color change
        self.play(
            Rotate(current_integral, 2*PI),
            current_integral.animate.set_color(GOLD),
            run_time=3
        )
        
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(current_integral), run_time=2)
    
    def clear_and_add_dense_background(self, current_background):
        """Clear current background and add dense integral expressions"""
        # Remove current background expressions
        self.clear_background(current_background)
        
        # Add dense background - 25-35 expressions per transition
        num_expressions = random.randint(25, 35)
        
        for _ in range(num_expressions):
            # Choose random integral expression
            expression = random.choice(self.background_expressions) 
            
            try:
                # Create expression with 70% opacity
                bg_expr = MathTex(expression, font_size=random.randint(12, 28), color=WHITE)
                bg_expr.set_opacity(0.7)  # Fixed 70% opacity
                
                # Position in horizontal center third only
                x_pos = random.uniform(-2.5, 2.5)  # Center third horizontally
                y_pos = random.uniform(-4, 4)  # Full screen height
                
                # Avoid the center area where main expression is
                if -2 < x_pos < 2 and -1 < y_pos < 1:
                    if random.choice([True, False]):
                        x_pos = random.uniform(-2.5, -2.2) if x_pos < 0 else random.uniform(2.2, 2.5)
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
                if -2.5 < x_pos < 2.5 and -1.5 < y_pos < 1.5:
                    # Push to edges within center third
                    if abs(x_pos) > abs(y_pos):
                        x_pos = random.uniform(-2.5, -2.7) if x_pos < 0 else random.uniform(2.7, 2.5)
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

class IntegralCategoriesMatchCut(Scene):
    def construct(self):
        # Alternative version organized by mathematical categories
        self.camera.background_color = BLACK
        
        categories = {
            "Basic Powers": [
                r"\int x \, dx",
                r"\int x^2 \, dx", 
                r"\int x^3 \, dx",
                r"\int x^n \, dx",
                r"\int \frac{1}{x} \, dx",
                r"\int \sqrt{x} \, dx"
            ],
            "Trigonometric": [
                r"\int \sin(x) \, dx",
                r"\int \cos(x) \, dx",
                r"\int \tan(x) \, dx",
                r"\int \sin^2(x) \, dx",
                r"\int \cos^2(x) \, dx",
                r"\int \sec^2(x) \, dx"
            ],
            "Exponential": [
                r"\int e^x \, dx",
                r"\int e^{-x} \, dx",
                r"\int xe^x \, dx",
                r"\int e^{ax} \, dx"
            ],
            "Definite": [
                r"\int_0^1 x^2 \, dx",
                r"\int_0^\pi \sin(x) \, dx",
                r"\int_{-\infty}^{\infty} e^{-x^2} \, dx",
                r"\int_0^{\infty} e^{-x} \, dx"
            ],
            "Multiple": [
                r"\iint_D f(x,y) \, dA",
                r"\iiint_V f(x,y,z) \, dV",
                r"\oint_C f(z) \, dz",
                r"\iint_S \mathbf{F} \cdot \mathbf{n} \, dS"
            ]
        }
        
        category_colors = {
            "Basic Powers": BLUE,
            "Trigonometric": GREEN, 
            "Exponential": RED,
            "Definite": YELLOW,
            "Multiple": PURPLE
        }
        
        # Title sequence
        title = Text("Mathematical Integration", font_size=48, color=WHITE)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title))
        
        current = None
        
        for category_name, expressions in categories.items():
            # Category title
            category_title = Text(category_name, font_size=36, color=category_colors[category_name])
            category_title.to_edge(UP)
            self.play(FadeIn(category_title), run_time=0.8)
            
            for i, expr in enumerate(expressions):
                next_integral = MathTex(expr, font_size=70, color=category_colors[category_name])
                
                if current is None:
                    current = next_integral
                    self.play(FadeIn(current), run_time=1)
                else:
                    # Match cut alignment
                    next_integral.move_to(current.get_center())
                    try:
                        if len(current[0]) > 0 and len(next_integral[0]) > 0:
                            offset = current[0][0].get_center() - next_integral[0][0].get_center()
                            next_integral.shift(offset)
                    except (IndexError, AttributeError):
                        pass
                    
                    self.play(Transform(current, next_integral), run_time=0.7)
                
                self.wait(0.4)
            
            self.play(FadeOut(category_title), run_time=0.5)
            self.wait(0.3)
        
        # Grand finale
        self.play(
            current.animate.scale(2).move_to(ORIGIN).set_color(GOLD),
            run_time=2
        )
        self.wait(1)
        
        final_symbol = MathTex(r"\int", font_size=300, color=GOLD)
        self.play(Transform(current, final_symbol), run_time=2)
        self.play(Rotate(current, PI), run_time=2)
        self.wait(2)

# To render these animations:
# manim -pql filename.py ExtendedIntegralMatchCut
# manim -pql filename.py IntegralCategoriesMatchCut
#
# For high quality:
# manim -pqh filename.py ExtendedIntegralMatchCut