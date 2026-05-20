from manim import *
import random

class ExtendedDerivativeMatchCut(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        self.background_expressions = [
            
            r"f'(x)", r"g'(t)", r"h'(u)", r"y'", r"z'", r"\frac{dy}{dx}", r"\frac{df}{dt}",
            
            r"x^2", r"x^3", r"2x", r"3x^2", r"nx^{n-1}", r"\frac{1}{x}", r"\sqrt{x}",
            
            r"\sin x", r"\cos x", r"\tan x", r"\cos x", r"-\sin x", r"\sec^2 x",
            
            r"e^x", r"e^x", r"a^x \ln a", r"\ln x", r"\frac{1}{x}", r"x e^x",
            
            r"f(g(x))", r"f'(g(x))g'(x)", r"u'v + uv'", r"\frac{du}{dx}",
            
            r"uv", r"u'v + uv'", r"fg", r"f'g + fg'",
            
            r"\frac{u}{v}", r"\frac{u'v - uv'}{v^2}", r"\frac{f}{g}", r"\frac{f'g - fg'}{g^2}",
            
            r"f''(x)", r"f'''(x)", r"\frac{d^2y}{dx^2}", r"\frac{d^3y}{dx^3}",
            
            r"\frac{\partial f}{\partial x}", r"\frac{\partial f}{\partial y}", r"\nabla f", r"\frac{\partial^2 f}{\partial x^2}",
            
            r"\int f'(x)dx = f(x)", r"\int", r"\int_a^b", r"\oint",
            
            r"\lim_{h \to 0}", r"\frac{f(x+h) - f(x)}{h}", r"\lim", r"h \to 0",
            
            r"\sin", r"\cos", r"\tan", r"\ln", r"\log", r"e", r"\pi",
            
            r"x", r"y", r"t", r"u", r"v", r"a", r"b", r"c", r"n", r"h",
            
            r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\theta", r"\lambda", r"\mu",
            
            r"x^2 + 1", r"x^3 - 2x", r"e^{x^2}", r"\sin(2x)", r"\cos(x^2)", r"x \sin x",
            r"\frac{x^2}{x+1}", r"\sqrt{x^2+1}", r"x^2 e^x", r"\ln(x^2)", r"(x+1)^3",
            
            r"2x", r"3x^2", r"e^x", r"\cos x", r"-\sin x", r"\frac{1}{x}",
            
            r"x^n", r"a^x", r"\sin(ax)", r"\cos(bx)", r"e^{ax}", r"\ln(ax)",
            r"x^2 + y^2", r"xy", r"x^2y", r"xyz", r"\sin(xy)", r"e^{xy}",
            
            r"f'(x) = 0", r"\text{max}", r"\text{min}", r"f''(x) > 0", r"f''(x) < 0",
            
            r"\frac{dx}{dt}", r"\frac{dy}{dt}", r"\frac{dV}{dt}", r"\frac{dA}{dt}",
            
            r"x^2 + y^2 = 1", r"xy = c", r"x^2 + y^2 = r^2",
            
            r"0", r"1", r"2", r"3", r"4", r"5", r"+", r"-", r"=", r"<", r">",
            r"dx", r"dy", r"dt", r"du", r"dv", r"dr", r"d\theta",
            r"x_0", r"x_1", r"y_0", r"y_1", r"t_0", r"t_1",
            r"a_n", r"b_n", r"c_n", r"f_n", r"g_n",
            r"\infty", r"\pm", r"\mp", r"\cdot", r"\times", r"\div",
            r"x'", r"y'", r"z'", r"u'", r"v'", r"w'",
            r"\Delta x", r"\Delta y", r"\Delta t", r"\delta", r"\epsilon",
        ]
        
        
        lagrange_basic = [
            r"f'(x)", r"(x)'", r"(x^2)'", r"(x^3)'", r"(x^n)'", 
            r"(\sqrt{x})'", r"(x^{-1})'", r"(\frac{1}{x})'", r"(x^{1/2})'", r"(x^{-1/2})'",
        ]
        
        lagrange_trig = [
            r"(\sin x)'", r"(\cos x)'", r"(\tan x)'", r"(\sec x)'", r"(\csc x)'", 
            r"(\cot x)'", r"(\sin^2 x)'", r"(\cos^2 x)'", r"(\tan^2 x)'", 
            r"(\sin(2x))'", r"(\cos(3x))'",
        ]
        
        lagrange_advanced = [
            r"(e^x)'", r"(e^{-x})'", r"(e^{ax})'", r"(\ln x)'", r"(x e^x)'", 
            r"(x \sin x)'", r"(x^2 e^x)'", r"(\frac{x}{\sin x})'",  
            r"(\sin(x^2))'", r"((x^2+1)^3)'", r"(\sqrt{x^2+1})'",
        ]
        
        lagrange_higher = [
            r"f''(x)", r"f'''(x)", r"f^{(4)}(x)", r"f^{(n)}(x)", 
            r"(x^4)''", r"(\sin x)''", r"(e^x)'''", r"(\ln x)''",
        ]
        
        leibniz_basic = [
            r"\frac{d}{dx}x", r"\frac{d}{dx}x^2", r"\frac{d}{dx}x^3", r"\frac{d}{dx}x^n", 
            r"\frac{d}{dx}\sqrt{x}", r"\frac{d}{dx}\frac{1}{x}", r"\frac{d}{dx}x^{1/2}", 
            r"\frac{d}{dx}x^{-1}", r"\frac{d}{dx}x^{-1/2}", r"\frac{dy}{dx}",
        ]
        
        leibniz_trig = [
            r"\frac{d}{dx}\sin x", r"\frac{d}{dx}\cos x", r"\frac{d}{dx}\tan x", 
            r"\frac{d}{dx}\sec x", r"\frac{d}{dx}\csc x", r"\frac{d}{dx}\cot x", 
            r"\frac{d}{dx}\sin^2 x", r"\frac{d}{dx}\cos^2 x", r"\frac{d}{dx}\sin(2x)", 
            r"\frac{d}{dx}\cos(3x)", r"\frac{d}{dx}\tan(x^2)",
        ]
        
        leibniz_advanced = [
            r"\frac{d}{dx}e^x", r"\frac{d}{dx}e^{-x}", r"\frac{d}{dx}e^{ax}", 
            r"\frac{d}{dx}\ln x", r"\frac{d}{dx}(x e^x)", r"\frac{d}{dx}(x \sin x)", 
            r"\frac{d}{dx}(x^2 e^x)", r"\frac{d}{dx}\frac{x}{\sin x}", 
            r"\frac{d}{dx}\sin(x^2)", r"\frac{d}{dx}(x^2+1)^3", r"\frac{d}{dx}\sqrt{x^2+1}",
        ]
        
        leibniz_higher = [
            r"\frac{d^2y}{dx^2}", r"\frac{d^3y}{dx^3}", r"\frac{d^4y}{dx^4}", 
            r"\frac{d^ny}{dx^n}", r"\frac{d^2}{dx^2}x^4", r"\frac{d^2}{dx^2}\sin x", 
            r"\frac{d^3}{dx^3}e^x", r"\frac{d^2}{dx^2}\ln x",
        ]
        
        partial_derivatives = [
            r"\frac{\partial f}{\partial x}", r"\frac{\partial f}{\partial y}", r"\frac{\partial f}{\partial z}", 
            r"\frac{\partial}{\partial x}(x^2 + y^2)", r"\frac{\partial}{\partial y}(xy^2)", 
            r"\frac{\partial}{\partial z}(xyz)", r"\frac{\partial^2 f}{\partial x^2}", 
            r"\frac{\partial^2 f}{\partial x \partial y}", r"\frac{\partial^2 f}{\partial y^2}", 
            r"\nabla f", r"\nabla^2 f",
        ]
        
        special_notation = [
            r"D_x f", r"D^2_x f", r"D_x D_y f", r"\delta'(x)", 
            r"\frac{d\mathbf{r}}{dt}", r"\mathbf{r}'(t)", r"\frac{d}{dt}(x(t), y(t))", 
            r"\frac{dy/dt}{dx/dt}",
        ]
        
        
        sections = [
            ("Basic Lagrange", lagrange_basic, BLUE, "prime"),
            ("Trig Lagrange", lagrange_trig, GREEN, "prime"), 
            ("Advanced Lagrange", lagrange_advanced, RED, "prime"),
            ("Higher Lagrange", lagrange_higher, YELLOW, "prime"),
            ("Basic Leibniz", leibniz_basic, PURPLE, "fraction"),
            ("Trig Leibniz", leibniz_trig, ORANGE, "fraction"),
            ("Advanced Leibniz", leibniz_advanced, PINK, "fraction"),
            ("Higher Leibniz", leibniz_higher, TEAL_A, "fraction"),
            ("Partial Derivatives", partial_derivatives, GOLD, "partial"),
            ("Special Notation", special_notation, GRAY_A, "special")
        ]
        
        current = None
        current_background = []  
        
        for section_name, expressions, color, notation_type in sections:
            for i, expr in enumerate(expressions):
                next_derivative = MathTex(expr, font_size=72, color=color)
                next_derivative.move_to(ORIGIN)
                
                
                self.clear_and_add_dense_background(current_background)
                
                if current is None:
                    
                    current = next_derivative
                    self.play(DrawBorderThenFill(current), run_time=1.2)
                    self.wait(0.3)
                else:
                    
                    self.align_derivative_symbols(current, next_derivative, notation_type)
                    
                    
                    if i == 0:  
                        run_time = 1.0
                        wait_time = 0.6
                    else:  
                        run_time = 0.6
                        wait_time = 0.2
                    
                    self.play(
                        Transform(current, next_derivative),
                        run_time=run_time
                    )
                    self.wait(wait_time)
        
        
        self.clear_background(current_background)
        
        
        self.add_ultra_dense_background()
        self.wait(1)
        
        
        self.play(
            current.animate.scale(1.4).move_to(ORIGIN).set_color(GOLD),
            run_time=1.5
        )
        
        
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
        
        
        lagrange_symbol = MathTex(r"f'", font_size=200, color=BLUE)
        lagrange_symbol.move_to(ORIGIN)
        self.play(
            Transform(current, lagrange_symbol),
            run_time=1.5
        )
        self.wait(1)
        
        
        leibniz_symbol = MathTex(r"\frac{d}{dx}", font_size=200, color=RED)
        leibniz_symbol.move_to(ORIGIN)
        self.play(
            Transform(current, leibniz_symbol),
            run_time=1.5
        )
        self.wait(1)
        
        
        partial_symbol = MathTex(r"\frac{\partial}{\partial x}", font_size=200, color=GREEN)
        partial_symbol.move_to(ORIGIN)
        self.play(
            Transform(current, partial_symbol),
            run_time=1.5
        )
        
        
        self.play(
            Rotate(current, 2*PI, about_point=ORIGIN),
            current.animate.set_color(GOLD),
            run_time=3
        )
        
        self.wait(2)
        
        
        self.play(FadeOut(current), run_time=2)
    
    def align_derivative_symbols(self, current_expr, next_expr, notation_type):
        """Align derivative symbols based on notation type"""
        try:
            if notation_type == "prime":
                
                current_bbox = current_expr.get_bounding_box()
                next_bbox = next_expr.get_bounding_box()
                
                
                current_right = current_bbox[1][0]  
                next_right = next_bbox[1][0]
                
                
                offset_x = current_right - next_right
                next_expr.shift(RIGHT * offset_x * 0.3)  
                
            elif notation_type == "fraction":
                
                current_left = current_expr.get_left()
                next_left = next_expr.get_left()
                
                
                offset = current_left - next_left
                next_expr.shift(offset * 0.5)  
                
            elif notation_type == "partial":
                
                current_left = current_expr.get_left()
                next_left = next_expr.get_left()
                
                offset = current_left - next_left
                next_expr.shift(offset * 0.4)  
                
            elif notation_type == "special":
                
                next_expr.move_to(ORIGIN)
                
            
            final_center = next_expr.get_center()
            if abs(final_center[0]) > 0.5 or abs(final_center[1]) > 0.5:
                next_expr.move_to(ORIGIN)
                
        except Exception:
            
            next_expr.move_to(ORIGIN)
    
    def clear_and_add_dense_background(self, current_background):
        """Clear current background and add very dense calculus expressions"""
        
        self.clear_background(current_background)
        
        
        num_expressions = random.randint(25, 35)
        
        for _ in range(num_expressions):
            
            expression = random.choice(self.background_expressions) 
            
            try:
                
                bg_expr = MathTex(expression, font_size=random.randint(12, 28), color=WHITE)
                bg_expr.set_opacity(0.7)  
                
                
                x_pos = random.uniform(-2.5, 2.5)  
                y_pos = random.uniform(-4, 4)  
                
                
                if -1.5 < x_pos < 1.5 and -1 < y_pos < 1:
                    if random.choice([True, False]):
                        x_pos = random.uniform(-2.5, -1.8) if x_pos < 0 else random.uniform(1.8, 2.5)
                    else:
                        y_pos = random.uniform(-4, -1.5) if y_pos < 0 else random.uniform(1.5, 4)
                
                bg_expr.move_to([x_pos, y_pos, 0])
                
                
                if random.random() < 0.3:  
                    bg_expr.rotate(random.uniform(-0.2, 0.2))
                
                
                self.add(bg_expr)
                current_background.append(bg_expr)
                
            except:
                
                continue
    
    def add_ultra_dense_background(self):
        """Add ultra-dense background for finale"""
        num_expressions = 50  
        
        for _ in range(num_expressions):
            expression = random.choice(self.background_expressions)
            
            try:
                bg_expr = MathTex(expression, font_size=random.randint(10, 24), color=WHITE)
                bg_expr.set_opacity(0.7)  
                
                
                x_pos = random.uniform(-2.5, 2.5)  
                y_pos = random.uniform(-4.5, 4.5)
                
                
                if -2 < x_pos < 2 and -1.5 < y_pos < 1.5:
                    
                    if abs(x_pos) > abs(y_pos):
                        x_pos = random.uniform(-2.5, -2.2) if x_pos < 0 else random.uniform(2.2, 2.5)
                    else:
                        y_pos = random.uniform(-4.5, -2) if y_pos < 0 else random.uniform(2, 4.5)
                
                bg_expr.move_to([x_pos, y_pos, 0])
                
                
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

class DerivativeNotationSections(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        self.background_expressions = [
            r"f'(x)", r"\frac{dy}{dx}", r"g'(t)", r"\frac{df}{dt}", r"h'(u)",
            r"x^2", r"2x", r"3x^2", r"nx^{n-1}", r"\sin x", r"\cos x", r"-\sin x",
            r"e^x", r"\frac{1}{x}", r"\ln x", r"f'(g(x))g'(x)", r"u'v + uv'",
            r"\frac{\partial f}{\partial x}", r"\nabla f", r"f''(x)", r"\lim_{h \to 0}",
            r"x", r"y", r"t", r"u", r"v", r"\alpha", r"\beta", r"\theta",
            r"e", r"\pi", r"\sin", r"\cos", r"\tan", r"\ln", r"\int",
            r"dx", r"dy", r"dt", r"du", r"0", r"1", r"2", r"3", r"+", r"-", r"="
        ]
        
        
        sections = {
            "Lagrange Notation": {
                "expressions": [
                    r"f'(x)", r"(x^2)'", r"(\sin x)'", r"(e^x)'", 
                    r"(x \sin x)'", r"f''(x)", r"f'''(x)"
                ],
                "color": BLUE,
                "symbol": r"f'(x)"
            },
            "Leibniz Notation": {
                "expressions": [
                    r"\frac{dy}{dx}", r"\frac{d}{dx}x^2", r"\frac{d}{dx}\sin x", 
                    r"\frac{d}{dx}e^x", r"\frac{d}{dx}(x \sin x)", 
                    r"\frac{d^2y}{dx^2}", r"\frac{d^3y}{dx^3}"
                ],
                "color": RED,
                "symbol": r"\frac{dy}{dx}"
            },
            "Partial Derivatives": {
                "expressions": [
                    r"\frac{\partial f}{\partial x}", r"\frac{\partial f}{\partial y}",
                    r"\frac{\partial^2 f}{\partial x^2}", r"\frac{\partial^2 f}{\partial x \partial y}",
                    r"\nabla f", r"\nabla^2 f"
                ],
                "color": GREEN,
                "symbol": r"\frac{\partial f}{\partial x}"
            }
        }
        
        
        title = Text("Derivative Notations", font_size=48, color=WHITE)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title))
        
        current = None
        background_mobjects = []
        
        for section_name, section_data in sections.items():
            
            section_title = Text(section_name, font_size=36, color=section_data["color"])
            section_title.to_edge(UP)
            self.play(FadeIn(section_title), run_time=0.8)
            
            
            self.add_dense_background_symbols(background_mobjects)
            
            
            if current is None:
                current = MathTex(section_data["symbol"], font_size=100, color=section_data["color"])
                current.move_to(ORIGIN)
                self.play(DrawBorderThenFill(current), run_time=1)
            else:
                section_symbol = MathTex(section_data["symbol"], font_size=100, color=section_data["color"])
                section_symbol.move_to(ORIGIN)
                self.play(Transform(current, section_symbol), run_time=1)
            
            self.wait(0.5)
            
            
            for expr in section_data["expressions"]:
                next_expr = MathTex(expr, font_size=80, color=section_data["color"])
                next_expr.move_to(ORIGIN)
                
                
                if random.random() < 0.4:
                    self.add_dense_background_symbols(background_mobjects)
                
                self.play(Transform(current, next_expr), run_time=0.7)
                self.wait(0.3)
            
            self.play(FadeOut(section_title), run_time=0.5)
            self.wait(0.5)
            
            
            if len(background_mobjects) > 15:
                self.fade_background_symbols(background_mobjects)
        
        
        if background_mobjects:
            self.play(*[FadeOut(mob) for mob in background_mobjects], run_time=1)
        
        
        self.play(
            current.animate.scale(1.5).set_color(GOLD),
            run_time=1.5
        )
        self.wait(1)
        
        
        lagrange = MathTex(r"f'", font_size=100, color=BLUE)
        leibniz = MathTex(r"\frac{dy}{dx}", font_size=100, color=RED) 
        partial = MathTex(r"\frac{\partial f}{\partial x}", font_size=100, color=GREEN)
        
        lagrange.shift(LEFT * 3)
        leibniz.move_to(ORIGIN)
        partial.shift(RIGHT * 3)
        
        all_notations = VGroup(lagrange, leibniz, partial)
        
        self.play(Transform(current, all_notations), run_time=2)
        self.play(Rotate(current, PI, about_point=ORIGIN), run_time=2)
        self.wait(2)
    
    def add_dense_background_symbols(self, background_mobjects):
        """Add many dense background symbols"""
        num_symbols = random.randint(8, 15)  
        
        for _ in range(num_symbols):
            symbol = random.choice(self.background_expressions)
            
            try:
                bg_symbol = MathTex(symbol, font_size=random.randint(16, 32), color=WHITE)
                
                
                x_pos = random.uniform(-2.5, 2.5)  
                y_pos = random.uniform(-3.5, 3.5)
                
                
                if -2 < x_pos < 2 and -2 < y_pos < 2:
                    
                    if random.choice([True, False]):
                        x_pos = random.uniform(-2.5, -2.2) if x_pos < 0 else random.uniform(2.2, 2.5)
                    else:
                        y_pos = random.uniform(-3.5, -2.5) if y_pos < 0 else random.uniform(2.5, 3.5)
                
                bg_symbol.move_to([x_pos, y_pos, 0])
                bg_symbol.set_opacity(0.7)  
                
                
                if random.random() < 0.25:
                    bg_symbol.rotate(random.uniform(-0.15, 0.15))
                
                self.add(bg_symbol)  
                background_mobjects.append(bg_symbol)
                
            except:
                continue
    
    def fade_background_symbols(self, background_mobjects):
        """Fade out some background symbols"""
        if len(background_mobjects) > 8:
            symbols_to_remove = background_mobjects[:5]  
            for mob in symbols_to_remove:
                self.remove(mob)
                background_mobjects.remove(mob)






