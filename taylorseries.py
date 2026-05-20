from manim import *
import numpy as np

class TaylorSeriesEx(Scene):
    def construct(self):
        
        self.camera.background_color = WHITE
        
        
        title = MathTex(r"\text{Taylor Series for } e^x", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        
        taylor_general = MathTex(
            r"f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \frac{f'''(0)}{3!}x^3 + \cdots",
            font_size=32,
            color=DARK_BLUE
        )
        taylor_general.move_to(UP * 2.5)
        
        self.play(Write(taylor_general), run_time=1.5)
        self.wait(0.5)
        
        
        derivatives_text = MathTex(
            r"\text{For } f(x) = e^x:",
            font_size=28,
            color=BLACK
        )
        derivatives_text.move_to(UP * 1.8 + LEFT * 3)
        
        derivatives = VGroup(
            MathTex(r"f(x) = e^x", font_size=24, color=GREEN),
            MathTex(r"f'(x) = e^x", font_size=24, color=GREEN),
            MathTex(r"f''(x) = e^x", font_size=24, color=GREEN),
            MathTex(r"f'''(x) = e^x", font_size=24, color=GREEN),
            MathTex(r"\vdots", font_size=24, color=GREEN)
        )
        
        for i, deriv in enumerate(derivatives):
            deriv.move_to(UP * (1.4 - i * 0.25) + LEFT * 3)
        
        self.play(Write(derivatives_text), run_time=0.8)
        self.play(Write(derivatives), run_time=1.2)
        self.wait(0.5)
        
        
        at_zero = MathTex(
            r"\text{At } x = 0: \quad f(0) = f'(0) = f''(0) = \cdots = 1",
            font_size=28,
            color=RED
        )
        at_zero.move_to(UP * 0.2 + LEFT * 3)
        
        self.play(Write(at_zero), run_time=1)
        self.wait(0.5)
        
        
        taylor_series = MathTex(
            r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots",
            font_size=32,
            color=PURPLE
        )
        taylor_series.move_to(DOWN * 0.5 + LEFT * 3)
        
        self.play(Write(taylor_series), run_time=1.5)
        self.wait(1)
        
        
        self.play(
            FadeOut(derivatives_text),
            FadeOut(derivatives),
            FadeOut(at_zero),
            FadeOut(taylor_series),
            run_time=1
        )
        
        
        axes = Axes(
            x_range=[-1, 3, 0.5],
            y_range=[-1, 8, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": BLACK, "stroke_width": 2},
            tips=True
        )
        axes.center()
        axes.shift(DOWN * 0.5)
        
        
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.1)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.1)
        x_label.set_color(BLACK)
        y_label.set_color(BLACK)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1)
        
        
        def exp_function(x):
            return np.exp(x)
        
        exp_graph = axes.plot(
            exp_function,
            x_range=[-1, 2.5],
            color=RED,
            stroke_width=4
        )
        exp_label = MathTex(r"e^x", font_size=24, color=RED)
        exp_label.next_to(exp_graph.get_end(), UP + RIGHT, buff=0.2)
        
        self.play(Create(exp_graph), Write(exp_label), run_time=1.2)
        
        
        series_formula = MathTex(
            r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
            font_size=36,
            color=PURPLE
        )
        series_formula.move_to(UP * 2.2 + LEFT * 2.5)
        
        self.play(Write(series_formula), run_time=1)
        self.wait(0.5)
        
        
        def taylor_poly(x, n_terms):
            result = np.zeros_like(x)
            for n in range(n_terms):
                result += (x ** n) / np.math.factorial(n)
            return result
        
        
        colors = [BLUE, GREEN, ORANGE, PINK, YELLOW, TEAL]
        
        
        polynomials = []
        labels = []
        
        for n in range(1, 7):
            
            poly_func = lambda x, n=n: taylor_poly(x, n)
            
            
            poly_graph = axes.plot(
                poly_func,
                x_range=[-1, 2.5 if n > 3 else 1.5],
                color=colors[n-1],
                stroke_width=3
            )
            
            
            terms = []
            for i in range(min(n, 4)):  
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                elif i == 2:
                    terms.append(r"\frac{x^2}{2}")
                elif i == 3:
                    terms.append(r"\frac{x^3}{6}")
            
            if n > 4:
                terms.append(r"\cdots")
            
            poly_text = " + ".join(terms)
            poly_label = MathTex(f"P_{n-1}(x) = {poly_text}", font_size=20, color=colors[n-1])
            poly_label.move_to(UP * (2.8 - n * 0.3) + RIGHT * 3)
            
            polynomials.append(poly_graph)
            labels.append(poly_label)
            
            
            self.play(
                Create(poly_graph),
                Write(poly_label),
                run_time=0.8
            )
            self.wait(0.3)
        
        
        convergence_text = MathTex(
            r"\text{As } n \to \infty, \quad P_n(x) \to e^x",
            font_size=28,
            color=DARK_BLUE
        )
        convergence_text.move_to(DOWN * 2.8)
        
        self.play(Write(convergence_text), run_time=1)
        self.wait(1)
        
        
        fade_out_objects = []
        for i in range(3):  
            fade_out_objects.extend([polynomials[i], labels[i]])
        
        self.play(
            *[FadeOut(obj) for obj in fade_out_objects],
            run_time=1
        )
        
        
        test_point = 1
        dot = Dot(axes.coords_to_point(test_point, np.exp(test_point)), color=RED, radius=0.08)
        
        
        convergence_table = VGroup(
            MathTex(r"\text{At } x = 1:", font_size=24, color=BLACK),
            MathTex(r"P_5(1) = 2.7167", font_size=20, color=colors[5]),
            MathTex(r"e^1 = 2.7183", font_size=20, color=RED),
            MathTex(r"\text{Error} \approx 0.0016", font_size=20, color=DARK_BLUE)
        )
        
        for i, text in enumerate(convergence_table):
            text.move_to(DOWN * (2 + i * 0.3) + LEFT * 4)
        
        self.play(Create(dot), run_time=0.5)
        self.play(Write(convergence_table), run_time=1.2)
        
        self.wait(3)