from manim import *

class RiemannToIntegral(Scene):
    def construct(self):
        
        
        bg_color = BLACK
        self.camera.background_color = bg_color
        
        
        
        title = Tex(
            r"$\mathbb{L}$imit $\mathbb{D}$efinition of $\mathbb{I}$ntegral", 
            font_size=40
        )
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.1)
        
        
        
        
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=4.5,
            y_length=2.5,
            axis_config={
                "include_tip": True, 
                "tip_shape": ArrowTriangleFilledTip,
                "tip_width": 0.15,
                "tip_height": 0.15
            }
        ).shift(UP * 1.8)

        labels = ax.get_axis_labels(x_label="x", y_label="y").set_opacity(0) 

        
        def func(x):
            return 0.15 * (x - 1)**2 + 1

        graph = ax.plot(func, color=WHITE, x_range=[0.5, 5.5])
        
        graph_label = ax.get_graph_label(graph, label="y=f(x)", x_val=5, direction=UP/2).set_color(WHITE).scale(0.6)

        
        a, b = 1, 5
        label_a = MathTex("a", color=TEAL, font_size=28).next_to(ax.c2p(a, 0), DOWN, buff=0.15)
        label_b = MathTex("b", color=TEAL, font_size=28).next_to(ax.c2p(b, 0), DOWN, buff=0.15)
        
        
        self.play(
            Write(title),
            Create(ax),
            Create(graph),
            Write(graph_label, run_time=0.8),
            Write(label_a, run_time=0.8),
            Write(label_b, run_time=0.8),
            run_time=1.5
        )

        
        n_tracker = ValueTracker(4)
        
        
        def get_rects(n):
            return ax.get_riemann_rectangles(
                graph,
                x_range=[a, b],
                dx=(b-a)/n,
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=0.6,
                input_sample_type="right", 
                color=BLUE
            )

        rects = get_rects(4)
        
        
        
        def get_sum_tex(n_val):
            upper_limit = str(n_val) if n_val < 1000 else r"\infty"
            return MathTex(
                r"\text{Area}", r"=", r"\sum_{i=1}^{" + upper_limit + r"} f(x_i) \Delta x",
                color=BLUE_A,
                font_size=32
            ).move_to(ORIGIN).shift(DOWN * 0.9)

        sum_tex = get_sum_tex(4)

        
        self.play(Create(rects), run_time=1)
        
        
        
        
        
        area_text_1 = MathTex(r"\text{Area}", r"=", r"\text{base}", r"\times", r"\text{height}", font_size=32)
        area_text_1.move_to(ORIGIN).shift(DOWN * 0.9)
        
        area_box_1 = SurroundingRectangle(
            area_text_1,
            color=BLUE,
            fill_opacity=0.15,
            stroke_width=3,
            buff=0.15,
            corner_radius=0.15
        )

        self.play(
            FadeIn(area_box_1),
            Write(area_text_1),
            run_time=0.8
        )

        
        one_rect = rects[1].copy().set_color(GREEN).set_opacity(0.8)
        
        
        
        brace_dx = Brace(one_rect, DOWN, buff=0.1, color=GREEN, sharpness=1.5).scale(0.8)
        
        brace_dx.next_to(one_rect, DOWN, buff=0.1)
        txt_dx = brace_dx.get_text(r"$\Delta x$").set_color(GREEN).scale(0.55)
        
        brace_h = Brace(one_rect, RIGHT, buff=0.1, color=GREEN, sharpness=1.5).scale(0.8)
        brace_h.next_to(one_rect, RIGHT, buff=0.1)
        txt_h = brace_h.get_text(r"$f(x_i)$").set_color(GREEN).scale(0.55)

        
        self.play(
            FadeIn(one_rect, scale=1.05),
            FadeIn(brace_dx),
            Write(txt_dx),
            FadeIn(brace_h),
            Write(txt_h),
            run_time=1.0
        )
        
        
        
        self.play(
            Indicate(area_text_1[2], color=GREEN, scale_factor=1.3),  
            Indicate(txt_dx, color=GREEN, scale_factor=1.3),           
            run_time=0.6
        )
        
        
        self.play(
            Indicate(area_text_1[4], color=GREEN, scale_factor=1.3),  
            Indicate(txt_h, color=GREEN, scale_factor=1.3),            
            run_time=0.6
        )

        
        area_text_2 = MathTex(r"\text{Area}", r"=", r"f(x_i)", r"\cdot", r"\Delta x", font_size=32, color=GREEN)
        area_text_2.move_to(area_text_1)
        
        area_box_2 = SurroundingRectangle(
            area_text_2,
            color=GREEN,
            fill_opacity=0.15,
            stroke_width=3,
            buff=0.15,
            corner_radius=0.15
        )

        self.play(
            Transform(area_box_1, area_box_2),
            TransformMatchingTex(area_text_1, area_text_2),
            run_time=0.8
        )

        
        top_definitions = VGroup(
            MathTex(r"\Delta x = \frac{b-a}{n}", font_size=28, color=ORANGE),
            MathTex(r"x_i = a + i \Delta x", font_size=28, color=ORANGE)
        ).arrange(RIGHT, buff=0.5).next_to(area_text_2, DOWN, buff=0.75) 
        
        
        definitions_box = SurroundingRectangle(
            top_definitions, 
            color=ORANGE, 
            fill_opacity=0.2,
            stroke_width=4,
            buff=0.2,
            corner_radius=0.2
        )

        self.play(
            FadeIn(definitions_box),
            Write(top_definitions),
            run_time=0.8
        )
        
        
        
        self.play(
            Indicate(top_definitions[0], color=GREEN, scale_factor=1.2),
            Indicate(txt_dx, color=GREEN, scale_factor=1.3),
            run_time=0.6
        )
        
        
        self.play(
            Indicate(top_definitions[1], color=GREEN, scale_factor=1.2),
            Indicate(txt_h, color=GREEN, scale_factor=1.3),
            run_time=0.6
        )

        self.wait(0.8)

        
        
        
        self.play(
            ReplacementTransform(area_text_2, sum_tex),
            FadeOut(area_box_1),
            FadeOut(one_rect),
            FadeOut(brace_dx),
            FadeOut(txt_dx),
            FadeOut(brace_h),
            FadeOut(txt_h),
            run_time=1.0
        )

        
        
        n_tracker = ValueTracker(4)
        
        
        
        self.remove(rects, sum_tex)
        
        smooth_rects = always_redraw(
            lambda: get_rects(int(n_tracker.get_value()))
        )
        smooth_sum_tex = always_redraw(
            lambda: get_sum_tex(int(n_tracker.get_value()))
        )
        
        self.add(smooth_rects, smooth_sum_tex)
        
        
        
        def speed_ramp(t):
            
            return t ** 2
        
        self.play(
            n_tracker.animate.set_value(100),
            run_time=2.0,
            rate_func=speed_ramp
        )
        
        
        
        final_n = 100
        static_rects = get_rects(final_n)
        static_sum_tex = get_sum_tex(final_n)
        
        self.remove(smooth_rects, smooth_sum_tex)
        self.add(static_rects, static_sum_tex)
        
        
        rects = static_rects
        sum_tex = static_sum_tex

        self.wait(0.8)

        
        
        inf_rects = ax.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.8)
        inf_sum_tex = get_sum_tex(9999) 

        
        self.play(
            FadeOut(rects),
            FadeIn(inf_rects),
            Transform(sum_tex, inf_sum_tex),
            FadeOut(definitions_box),
            FadeOut(top_definitions),
            run_time=0.8
        )

        
        
        
        limit_part = MathTex(r"\lim_{n \to \infty}", color=TEAL, font_size=32)
        
        limit_part.next_to(sum_tex[1], RIGHT, buff=0.05)
        
        
        summation_part = sum_tex[2]  
        
        self.play(
            summation_part.animate.shift(RIGHT * 1.0),
            Write(limit_part),
            run_time=1.0
        )
        
        
        full_limit_expr = VGroup(sum_tex, limit_part)
        
        
        
        
        integral_tex = MathTex(
            r"=", r"\int_a^b f(x) \, dx",
            color=PURPLE_B,
            font_size=36
        )
        
        
        
        integral_tex.move_to(sum_tex[1].get_center() + DOWN * 0.8, aligned_edge=LEFT)
        
        
        final_area = ax.get_area(graph, x_range=[a, b], color=PURPLE_B, opacity=0.6)

        
        self.play(
            FadeOut(inf_rects),
            FadeIn(final_area),
            Write(integral_tex),
            run_time=1.0
        )

        
        both_expressions = VGroup(full_limit_expr, integral_tex)
        self.play(
            both_expressions.animate.move_to(ORIGIN).shift(DOWN * 1.0),
            run_time=0.4
        )

        
        box = SurroundingRectangle(
            both_expressions,
            color=PURPLE_B, 
            fill_opacity=0.15,
            stroke_width=3,
            buff=0.25,
            corner_radius=0.15
        )
        self.play(Create(box), run_time=0.5)

        
        self.wait(3.0)