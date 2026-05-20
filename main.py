from manim import *
import numpy as np
import math

class TaylorSeriesExponential(Scene):
    def construct(self):
        
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 7, 1],
            x_length=4,  
            y_length=2.5,  
            axis_config={
                "color": WHITE, 
                "stroke_width": 2, 
                "include_ticks": False,
                "tip_length": 0.15,  
                "tip_width": 0.15    
            },
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        )
        axes.move_to(ORIGIN)  
        
        
        title = MathTex(r"\mathbb{T}\text{aylor }\mathbb{S}\text{eries of }e^x", font_size=32, color="#4A90E2")
        title.move_to(UP * 2)
        
        
        exp_func = axes.plot(lambda x: np.exp(x), color="#E67E22", stroke_width=2, stroke_opacity=0.8)
        exp_label = MathTex(r"e^x", color="#E67E22", font_size=36)  
        exp_label.next_to(exp_func.get_end(), UP)
        
        
        def taylor_term(x, n):
            result = 0
            for k in range(n + 1):
                result += (x**k) / math.factorial(k)
            return result
        
        
        def get_gradient_color(progress):
            
            
            purple = np.array([142, 68, 173]) / 255
            orange = np.array([230, 126, 34]) / 255
            color = purple * (1 - progress) + orange * progress
            return rgb_to_hex(color)
        
        
        self.play(
            Create(axes),
            Write(title),
            run_time=1.5
        )
        
        
        self.play(
            Create(exp_func),
            Write(exp_label),
            run_time=1.5
        )
        
        
        intro_text = MathTex(
            r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
            font_size=30,
            color="#E74C3C"
        )
        intro_text.move_to(DOWN * 2)
        self.play(Write(intro_text), run_time=1.5)
        
        
        self.wait(0.5)
        
        
        self.play(FadeOut(intro_text), run_time=0.5)
        
        
        base_part = MathTex(r"P_0(x) = 1", color=get_gradient_color(0), font_size=22)
        base_part.move_to(DOWN * 2.2)
        
        
        current_approx = axes.plot(
            lambda x: taylor_term(x, 0),
            color=get_gradient_color(0),
            stroke_width=4,
            x_range=[-2, 2]
        )
        
        
        self.play(
            Create(current_approx),
            Write(base_part),
            run_time=1.0
        )
        self.wait(0.5)
        
        
        
        new_approx = axes.plot(lambda x: taylor_term(x, 1), color=get_gradient_color(0.1), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_1(x) = 1 + x", color=get_gradient_color(0.1), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.8
        )
        self.wait(0.4)
        
        
        new_approx = axes.plot(lambda x: taylor_term(x, 2), color=get_gradient_color(0.2), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_2(x) = 1 + x + \frac{x^2}{2}", color=get_gradient_color(0.2), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.7
        )
        self.wait(0.3)
        
        
        new_approx = axes.plot(lambda x: taylor_term(x, 3), color=get_gradient_color(0.3), stroke_width=4, x_range=[-2, 2])
        new_equation = MathTex(r"P_3(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6}", color=get_gradient_color(0.3), font_size=22)
        new_equation.move_to(DOWN * 2.2)
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, new_equation),
            run_time=0.6
        )
        self.wait(0.25)
        
        
        static_base = MathTex(r"P_4(x) = 1 + x + \frac{x^2}{2} + \cdots + ", color=get_gradient_color(0.4), font_size=22)
        changing_term = MathTex(r"\frac{x^4}{24}", color=get_gradient_color(0.4), font_size=22)
        
        
        static_base.move_to(DOWN * 2.2)
        changing_term.next_to(static_base, RIGHT, buff=0.05)
        
        
        equation_group = VGroup(static_base, changing_term)
        equation_group.move_to(DOWN * 2.2)
        
        
        new_approx = axes.plot(lambda x: taylor_term(x, 4), color=get_gradient_color(0.4), stroke_width=4, x_range=[-2, 2])
        
        self.play(
            Transform(current_approx, new_approx),
            Transform(base_part, equation_group),
            run_time=0.5
        )
        self.wait(0.2)
        
        
        for n in range(5, 16):
            
            progress = n / 15  
            color = get_gradient_color(progress)
            
            new_approx = axes.plot(
                lambda x: taylor_term(x, n),
                color=color,
                stroke_width=4,
                x_range=[-2, 2]
            )
            
            
            new_static_base = MathTex(f"P_{{{n}}}(x) = 1 + x + \\frac{{x^2}}{{2}} + \\cdots + ", color=color, font_size=22)
            
            
            factorial_n = math.factorial(n)
            new_changing_term = MathTex(f"\\frac{{x^{{{n}}}}}{{{factorial_n}}}", color=color, font_size=22)
            
            
            new_static_base.move_to(DOWN * 2.2)
            new_changing_term.next_to(new_static_base, RIGHT, buff=0.02)
            
            
            new_equation_group = VGroup(new_static_base, new_changing_term)
            new_equation_group.move_to(DOWN * 2.2)
            
            
            run_time = max(0.1, 0.4 - (n-5) * 0.03)
            wait_time = max(0.02, 0.15 - (n-5) * 0.01)
            
            self.play(
                Transform(current_approx, new_approx),
                Transform(base_part, new_equation_group),
                run_time=run_time
            )
            self.wait(wait_time)
        
        
        self.wait(0.5)
        
        
        self.play(
            FadeOut(title),
            FadeOut(axes),
            FadeOut(exp_func),
            FadeOut(exp_label),
            FadeOut(base_part),
            FadeOut(current_approx),  
            run_time=0.8
        )
        
        
        self.wait(0.2)
        
        
        final_formula = MathTex(
            r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
            color="#E67E22",  
            font_size=48  
        )
        final_formula.move_to(ORIGIN)  
        
        
        self.play(
            FadeIn(final_formula, scale=0.8),
            run_time=1.0
        )
        
        
        self.wait(1.0)
        
        
        self.play(
            FadeOut(final_formula),
            run_time=1.0
        )
        
        
        self.wait(0.5)