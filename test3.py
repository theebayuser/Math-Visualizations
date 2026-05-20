from manim import *

class LimitIntegral(Scene):
    def construct(self):
        # --- Aesthetics ---
        BG_COLOR = "#000510" # Deepest Blue/Black
        self.camera.background_color = BG_COLOR
        
        # Neon Palette
        AXIS_COLOR = GRAY_C
        GRAPH_COLOR = "#00EEFF"     # Neon Cyan
        RECT_COLOR =  "#00AAAA"     # Teal
        HIGHLIGHT_DX = "#FFFF00"    # Neon Yellow
        HIGHLIGHT_FX = "#FF00FF"    # Neon Magenta
        TEXT_COLOR = WHITE
        
        # --- 1. Title Sequence ---
        # "Riemann to Integral" with Gradient
        title = MathTex(
            r"\mathbb{R}\text{iemann } \to \mathbb{I}\text{ntegral}",
            font_size=50
        )
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.8)
        
        # Background for title to ensure visibility
        title_bg = BackgroundRectangle(title, color=BG_COLOR, fill_opacity=0.6, buff=0.2)
        
        self.play(FadeIn(title_bg), Write(title), run_time=1.5)
        self.wait(0.5)
        
        # --- 2. Geometric Setup ---
        # Graph system centered
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=4.5,
            y_length=3.5,
            axis_config={
                "color": AXIS_COLOR, 
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        )
        ax.center().shift(DOWN * 0.5)
        
        # Function
        func_fn = lambda x: 0.1*(x-2.5)**2 + 1.5 + 0.3*np.sin(x)
        graph = ax.plot(func_fn, color=GRAPH_COLOR, x_range=[0.5, 4.5], stroke_width=4)
        
        # Labels
        labels = ax.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(ax), Create(labels), run_time=1.0)
        self.play(Create(graph), run_time=1.0)
        
        # --- 3. Dynamic Formula Setup ---
        # We need a dynamic integer for 'n' in the formula.
        
        n_tracker = ValueTracker(4)
        
        # Construct formula with updating n
        # \sum_{i=1}^{n} f(x_i) \Delta x
        
        # Static parts
        part1 = MathTex(r"\sum_{i=1}^{", font_size=36)
        part3 = MathTex(r"}", r"f(x_i)", r"\cdot", r"\Delta x", font_size=36)
        
        # Dynamic Integer
        n_decimal = Integer(4, font_size=28, color=RED).set_valign(UP)
        n_decimal.add_updater(lambda m: m.set_value(n_tracker.get_value()))
        
        # Color the terms in part3
        part3.set_color_by_tex("f(x_i)", HIGHLIGHT_FX)
        part3.set_color_by_tex(r"\Delta x", HIGHLIGHT_DX)
        
        # Combine into a group that arranges itself
        formula_group = VGroup()
        
        def update_formula_layout(mob):
            # Re-arrange parts
            # part1 | n_decimal | part3
            # n_decimal needs to be small and high up relative to sigma
            # But standard math format is usually superscript.
            # Let's approximate position:
            
            # Reset positions
            part1.move_to(ORIGIN)
            # Superscript pos
            superscript_pos = part1.get_corner(UR) + LEFT*0.15 + UP*0.1
            n_decimal.move_to(superscript_pos)
            
            # Part 3 follows Sigma
            part3.next_to(part1, RIGHT, buff=0.1, aligned_edge=DOWN)
            
            mob.move_to(title.get_bottom() + DOWN * 0.8)

        # Wrap dynamic logic
        formula_content = VGroup(part1, n_decimal, part3)
        formula_content.add_updater(update_formula_layout)
        
        # Background
        formula_bg = BackgroundRectangle(formula_content, color=BG_COLOR, fill_opacity=0.8, buff=0.2)
        
        # Initial create
        self.add(formula_bg) # Add BG first silently or fade in
        update_formula_layout(formula_content) # Init pos
        self.play(FadeIn(formula_bg), Write(formula_content))
        
        # --- 4. Rectangles & Highlights ---
        
        def get_rects():
            dx = (4.5 - 0.5) / n_tracker.get_value()
            return ax.get_riemann_rectangles(
                graph,
                x_range=[0.5, 4.5],
                dx=dx,
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=0.5,
                color=[RECT_COLOR, BLUE_D]
            )
        
        rects = get_rects()
        self.play(Create(rects), run_time=1.0)
        
        # Highlights
        # 2nd rectangle
        sample_idx = 1
        current_n = 4
        current_dx = (4.5 - 0.5) / current_n
        x_start = 0.5 + sample_idx * current_dx
        x_end = x_start + current_dx
        
        p1 = ax.c2p(x_start, 0)
        p2 = ax.c2p(x_end, 0)
        p_top = ax.c2p(x_start, func_fn(x_start))

        brace_dx = Brace(Line(p1, p2), DOWN, buff=0.05)
        text_dx = brace_dx.get_text(r"$\Delta x$", buff=0.05).set_color(HIGHLIGHT_DX).scale(0.6)
        
        brace_fx = Brace(Line(p1, p_top), LEFT, buff=0.05)
        text_fx = brace_fx.get_text(r"$f(x_i)$", buff=0.05).set_color(HIGHLIGHT_FX).scale(0.6)
        
        self.play(
            FadeIn(brace_dx), Write(text_dx),
            part3[3].animate.scale(1.3).set_color(HIGHLIGHT_DX), # Highlight dx term (index 3)
            run_time=0.6
        )
        self.play(
            FadeIn(brace_fx), Write(text_fx),
            part3[1].animate.scale(1.3).set_color(HIGHLIGHT_FX), # Highlight f(x) term (index 1)
            part3[3].animate.scale(1/1.3),
            run_time=0.6
        )
        self.wait(1.0)
        
        # Clear highlights
        self.play(
            FadeOut(brace_dx), FadeOut(text_dx),
            FadeOut(brace_fx), FadeOut(text_fx),
            part3[1].animate.scale(1/1.3),
            run_time=0.5
        )
        
        # --- 5. Convergence ---
        
        # Add updater to rects
        rects.add_updater(lambda m: m.become(get_rects()))
        
        # Prepare final formula
        # \int_{a}^{b} f(x) dx
        integral_tex = MathTex(
            r"\int_{a}^{b} f(x) \, dx",
            font_size=40
        )
        integral_tex.set_color_by_tex("f(x)", HIGHLIGHT_FX)
        integral_tex.set_color_by_tex("dx", HIGHLIGHT_DX)
        integral_tex.move_to(formula_content)
        
        # Animate N
        self.play(
            n_tracker.animate.set_value(100),
            run_time=4.0,
            rate_func=linear
        )
        
        # Switch to Integral
        self.play(
            FadeOut(formula_content),
            FadeIn(integral_tex),
            run_time=1.0
        )
        
        # Final Area Glow
        area = ax.get_area(graph, x_range=[0.5, 4.5], color=GRAPH_COLOR, opacity=0.6)
        self.play(
            FadeOut(rects),
            FadeIn(area),
            run_time=1.0
        )
        
        # End
        end_text = Text("Area Found", font_size=32, color=WHITE)
        bg_end = BackgroundRectangle(end_text, color=BG_COLOR, fill_opacity=0.8)
        end_group = VGroup(bg_end, end_text).move_to(ax.get_center())
        
        self.play(Write(end_group), run_time=1.0)
        self.wait(2)

