from manim import *
import math
import numpy as np

class TaylorSeriesExpanded(Scene):
    def construct(self):
        # Title (Enforced font_size=40)
        title = Tex(r"$\mathbb{T}$aylor $\mathbb{S}$eries", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Axis configuration with normally proportioned smaller tips
        ax_config = {
            "color": LIGHT_GREY, 
            "stroke_width": 2,
            "tip_width": 0.15,  # Increased width to normalize proportions
            "tip_length": 0.15  # Decreased length to remove the "tall/stretched" look
        }

        # Layout Setup - Explicitly positioned to spread out evenly vertically
        ax_top = Axes(
            x_range=[-5, 5, 1], y_range=[-2, 2, 1], 
            x_length=4.5, y_length=2.0,
            axis_config=ax_config
        )
        ax_bot = Axes(
            x_range=[-5, 5, 1], y_range=[-2, 2, 1], 
            x_length=4.5, y_length=2.0,
            axis_config=ax_config
        )
        
        # Placing them evenly on the screen
        ax_top.move_to(UP * 0.7)
        ax_bot.move_to(DOWN * 2.3)
        self.add(ax_top, ax_bot)

        # Translucent text box helper with visible background
        def create_boxed_tex(tex_string, target_ax):
            tex = MathTex(tex_string, font_size=20)
            box = SurroundingRectangle(
                tex, 
                corner_radius=0.15,
                color=BLUE, 
                fill_color="#1E1E1E", # Dark grey instead of black to be visible
                fill_opacity=0.95, 
                stroke_width=2.5, # Slightly thicker border
                buff=0.15
            )
            return VGroup(box, tex).next_to(target_ax, UP, buff=0.2)

        # Dynamic Bound Walker: perfectly cuts off graphs when they hit the y-axis boundaries
        def get_bounds(func, y_limit=2.0, x_bounds=(-5, 5), step=0.05):
            x_min, x_max = 0.0, 0.0
            for x in np.arange(0, x_bounds[1] + step, step):
                if abs(func(x)) > y_limit: break
                x_max = x
            for x in np.arange(0, x_bounds[0] - step, -step):
                if abs(func(x)) > y_limit: break
                x_min = x
            return [x_min, x_max]

        # ==========================================
        # PHASE 1: sin(x) and e^x
        # ==========================================
        
        # Base Functions (Dynamically clipped to the axes)
        sin_graph = ax_top.plot(np.sin, x_range=get_bounds(np.sin), color=RED, stroke_width=3)
        exp_graph = ax_bot.plot(np.exp, x_range=get_bounds(np.exp), color=YELLOW, stroke_width=3)
        self.add(sin_graph, exp_graph)

        def sin_poly(x, n):
            return sum([((-1)**k * x**(2*k + 1)) / math.factorial(2*k + 1) for k in range(n + 1)])

        def exp_poly(x, n):
            return sum([(x**k) / math.factorial(k) for k in range(n + 1)])

        def get_sin_tex(n):
            if n == 0: return r"\sin(x) \approx x"
            terms = ["x"]
            for k in range(1, min(n + 1, 3)): 
                sign = "-" if k % 2 != 0 else "+"
                terms.append(f"{sign} \\frac{{x^{{{2*k+1}}}}}{{{2*k+1}!}}")
            if n >= 3:
                sign = "-" if n % 2 != 0 else "+"
                terms.append(f"\\dots {sign} \\frac{{x^{{{2*n+1}}}}}{{{2*n+1}!}}")
            return r"\sin(x) \approx " + "".join(terms)

        def get_exp_tex(n):
            if n == 0: return r"e^x \approx 1"
            terms = ["1", "+ x"]
            for k in range(2, min(n + 1, 4)):
                terms.append(f"+ \\frac{{x^{{{k}}}}}{{{k}!}}")
            if n >= 4:
                terms.append(f"+ \\dots + \\frac{{x^{{{n}}}}}{{{n}!}}")
            return r"e^x \approx " + "".join(terms)

        # Initialize First Approximations (n=0)
        curr_top_graph = ax_top.plot(lambda x: sin_poly(x, 0), x_range=get_bounds(lambda x: sin_poly(x, 0)), color=ORANGE, stroke_width=3)
        curr_bot_graph = ax_bot.plot(lambda x: exp_poly(x, 0), x_range=get_bounds(lambda x: exp_poly(x, 0)), color=ORANGE, stroke_width=3)

        curr_top_tex = create_boxed_tex(get_sin_tex(0), ax_top)
        curr_bot_tex = create_boxed_tex(get_exp_tex(0), ax_bot)

        self.add(curr_top_graph, curr_bot_graph, curr_top_tex, curr_bot_tex)
        self.wait(1.5)

        # Iterations up to degree 10
        iterations = 11 
        for n in range(1, iterations):
            rt = max(0.2, 1.2 * (0.8 ** n)) 
            
            b_sin = get_bounds(lambda x: sin_poly(x, n))
            b_exp = get_bounds(lambda x: exp_poly(x, n))

            new_top_graph = ax_top.plot(lambda x: sin_poly(x, n), x_range=b_sin, color=ORANGE, stroke_width=3)
            new_bot_graph = ax_bot.plot(lambda x: exp_poly(x, n), x_range=b_exp, color=ORANGE, stroke_width=3)

            new_top_tex = create_boxed_tex(get_sin_tex(n), ax_top)
            new_bot_tex = create_boxed_tex(get_exp_tex(n), ax_bot)

            self.play(
                ReplacementTransform(curr_top_graph, new_top_graph),
                ReplacementTransform(curr_bot_graph, new_bot_graph),
                ReplacementTransform(curr_top_tex, new_top_tex),
                ReplacementTransform(curr_bot_tex, new_bot_tex),
                run_time=rt
            )
            
            curr_top_graph, curr_bot_graph = new_top_graph, new_bot_graph
            curr_top_tex, curr_bot_tex = new_top_tex, new_bot_tex

        # Infinity Summation Transition
        inf_sin_tex = create_boxed_tex(r"\sin(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!}", ax_top)
        inf_exp_tex = create_boxed_tex(r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}", ax_bot)

        self.play(
            ReplacementTransform(curr_top_tex, inf_sin_tex),
            ReplacementTransform(curr_bot_tex, inf_exp_tex),
            curr_top_graph.animate.set_color(GREEN_C),
            curr_bot_graph.animate.set_color(GREEN_C),
            run_time=1.5
        )
        self.wait(1)

        # ==========================================
        # TRANSITION TO PHASE 2: cos(x) and tan(x)
        # ==========================================
        
        self.play(
            FadeOut(curr_top_graph), FadeOut(curr_bot_graph),
            FadeOut(inf_sin_tex), FadeOut(inf_exp_tex),
            run_time=0.8
        )

        # New Base Functions strictly bounded to axes limits
        cos_graph = ax_top.plot(np.cos, x_range=get_bounds(np.cos), color=RED, stroke_width=3)
        tan_graph = ax_bot.plot(np.tan, x_range=get_bounds(np.tan, x_bounds=(-1.5, 1.5)), color=YELLOW, stroke_width=3)

        self.play(
            ReplacementTransform(sin_graph, cos_graph),
            ReplacementTransform(exp_graph, tan_graph),
            run_time=1.5
        )
        self.wait(0.5)

        def cos_poly(x, n):
            return sum([((-1)**k * x**(2*k)) / math.factorial(2*k) for k in range(n + 1)])

        tan_coeffs = [0, 1, 0, 1/3, 0, 2/15, 0, 17/315, 0, 62/2835, 0, 1382/155925, 0, 21844/6081075]
        def tan_poly(x, n):
            limit = min(2 * n + 2, len(tan_coeffs))
            return sum([tan_coeffs[i] * (x**i) for i in range(limit)])

        def get_cos_tex(n):
            if n == 0: return r"\cos(x) \approx 1"
            terms = ["1"]
            for k in range(1, min(n + 1, 3)):
                sign = "-" if k % 2 != 0 else "+"
                terms.append(f"{sign} \\frac{{x^{{{2*k}}}}}{{{2*k}!}}")
            if n >= 3:
                sign = "-" if n % 2 != 0 else "+"
                terms.append(f"\\dots {sign} \\frac{{x^{{{2*n}}}}}{{{2*n}!}}")
            return r"\cos(x) \approx " + "".join(terms)

        tan_terms_str = ["x", "+ \\frac{1}{3} x^3", "+ \\frac{2}{15} x^5", "+ \\frac{17}{315} x^7", "+ \\frac{62}{2835} x^9", "+ \\frac{1382}{155925} x^{11}"]
        def get_tan_tex(n):
            if n == 0: return r"\tan(x) \approx x"
            terms = [tan_terms_str[0]]
            for k in range(1, min(n + 1, 5)):
                terms.append(tan_terms_str[k])
            if n >= 5:
                terms.append(r"+ \dots")
            return r"\tan(x) \approx " + "".join(terms)

        # Initialize Phase 2 First Approximations (n=0)
        curr_top_graph = ax_top.plot(lambda x: cos_poly(x, 0), x_range=get_bounds(lambda x: cos_poly(x, 0)), color=GREEN_C, stroke_width=3)
        curr_bot_graph = ax_bot.plot(lambda x: tan_poly(x, 0), x_range=get_bounds(lambda x: tan_poly(x, 0), x_bounds=(-1.5, 1.5)), color=GREEN_C, stroke_width=3)

        curr_top_tex = create_boxed_tex(get_cos_tex(0), ax_top)
        curr_bot_tex = create_boxed_tex(get_tan_tex(0), ax_bot)

        self.play(
            Create(curr_top_graph), Create(curr_bot_graph),
            Write(curr_top_tex), Write(curr_bot_tex),
            run_time=1
        )
        
        # Iterations with Speed Ramp (Phase 2)
        for n in range(1, 6):
            rt = max(0.2, 1.2 * (0.8 ** n)) 
            
            b_cos = get_bounds(lambda x: cos_poly(x, n))
            b_tan = get_bounds(lambda x: tan_poly(x, n), x_bounds=(-1.5, 1.5))

            new_top_graph = ax_top.plot(lambda x: cos_poly(x, n), x_range=b_cos, color=GREEN_C, stroke_width=3)
            new_bot_graph = ax_bot.plot(lambda x: tan_poly(x, n), x_range=b_tan, color=GREEN_C, stroke_width=3)

            new_top_tex = create_boxed_tex(get_cos_tex(n), ax_top)
            new_bot_tex = create_boxed_tex(get_tan_tex(n), ax_bot)

            self.play(
                ReplacementTransform(curr_top_graph, new_top_graph),
                ReplacementTransform(curr_bot_graph, new_bot_graph),
                ReplacementTransform(curr_top_tex, new_top_tex),
                ReplacementTransform(curr_bot_tex, new_bot_tex),
                run_time=rt
            )
            
            curr_top_graph, curr_bot_graph = new_top_graph, new_bot_graph
            curr_top_tex, curr_bot_tex = new_top_tex, new_bot_tex

        # Infinity Summation Transition
        inf_cos_tex = create_boxed_tex(r"\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!}", ax_top)
        inf_tan_tex = create_boxed_tex(r"\tan(x) = \sum_{n=1}^{\infty} \frac{B_{2n} (-4)^n (1-4^n)}{(2n)!} x^{2n-1}", ax_bot)
        
        inf_tan_tex[1].set_font_size(18)

        self.play(
            ReplacementTransform(curr_top_tex, inf_cos_tex),
            ReplacementTransform(curr_bot_tex, inf_tan_tex),
            curr_top_graph.animate.set_color(BLUE_C),
            curr_bot_graph.animate.set_color(BLUE_C),
            run_time=1.5
        )

        self.wait(2)