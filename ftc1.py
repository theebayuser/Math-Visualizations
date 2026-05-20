"""
Fundamental Theorem of Calculus - Manim Animation
Run with: manim -pql ftc_part1.py FTC1Scene
For high quality: manim -pqh ftc_part1.py FTC1Scene
"""

from manim import *


class FTC1Scene(Scene):
    def construct(self):
        C_CURVE = "#00BFFF"
        C_AREA  = "#5533CC"
        C_STRIP = "#00DD66"
        C_T     = "#FF69B4"
        C_TH    = "#FFD700"

        
        
        
        title = Text(
            "𝔽undamental 𝕋heorem of 𝒞alculus",
            font_size=40, gradient=(BLUE, RED),
        )
        title.move_to(UP * 3.35)
        title.set_width(min(title.width, 5.5))

        
        
        
        axes = Axes(
            x_range=[0, 5.3, 1], y_range=[0, 4.0, 1],
            x_length=4.8, y_length=2.75,
            axis_config={
                "color": "#777777", "stroke_width": 2.2,
                "include_ticks": False,
                "tip_width": 0.14, "tip_height": 0.14,
            },
            tips=True,
        )
        axes.move_to(ORIGIN + DOWN * 0.25)   
        t_axis_lbl = MathTex("t", font_size=26, color="#999999")
        t_axis_lbl.next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
        y_axis_lbl = MathTex("y", font_size=26, color="#999999")
        y_axis_lbl.next_to(axes.y_axis.get_end(), UP, buff=0.10)

        def f(x):
            return 0.22 * (x - 0.4) * (x - 4.3) + 3.05

        curve = axes.plot(f, x_range=[0.15, 4.95], color=C_CURVE, stroke_width=3)
        peak_x = (0.4 + 4.3) / 2
        f_lbl = MathTex("f(t)", font_size=25, color=C_CURVE)
        f_lbl.next_to(axes.c2p(peak_x, f(peak_x)), UP, buff=0.20)

        self.play(
            Write(title),
            Create(axes), Write(t_axis_lbl), Write(y_axis_lbl),
            run_time=0.9,
        )
        self.play(Create(curve), Write(f_lbl), run_time=0.8)

        
        
        
        a_val = 0.45
        a_dot = Dot(axes.c2p(a_val, 0), color=WHITE, radius=0.065)
        a_lbl = MathTex("a", font_size=22, color=WHITE).next_to(
            axes.c2p(a_val, 0), DOWN, buff=0.15)

        t_val = 2.2
        t_dot = Dot(axes.c2p(t_val, 0), color=C_T, radius=0.08)
        t_lbl = MathTex("t", font_size=24, color=C_T).next_to(
            axes.c2p(t_val, 0), DOWN, buff=0.15)

        self.play(
            FadeIn(a_dot), Write(a_lbl),
            FadeIn(t_dot), Write(t_lbl),
            run_time=0.5,
        )

        area_base = axes.get_area(curve, x_range=[a_val, t_val],
                                  color=[C_AREA, PURPLE], opacity=0.50)
        At_lbl = MathTex("A(t)", font_size=21, color=WHITE)
        At_lbl.move_to(axes.c2p((a_val + t_val) / 2,
                                 f((a_val + t_val) / 2) * 0.28))

        def_eq = MathTex(r"A(t)=\int_a^t f(s)\,ds", font_size=27, color=WHITE)
        def_eq.move_to(UP * 2.30)   

        self.play(
            FadeIn(area_base), Write(At_lbl),
            Write(def_eq),
            run_time=0.8,
        )
        self.wait(0.4)

        
        
        
        h_init = 0.78
        th_val = t_val + h_init
        th_dot = Dot(axes.c2p(th_val, 0), color=C_TH, radius=0.08)
        th_lbl = MathTex("t{+}h", font_size=22, color=C_TH).next_to(
            axes.c2p(th_val, 0), DOWN, buff=0.15)

        area_full = axes.get_area(curve, x_range=[a_val, th_val],
                                  color=[C_AREA, C_STRIP], opacity=0.40)
        strip_area = axes.get_area(curve, x_range=[t_val, th_val],
                                   color=C_STRIP, opacity=0.65)

        Ath_lbl = MathTex("A(t{+}h)", font_size=19, color=WHITE)
        mid_x_full = (a_val + th_val) / 2
        Ath_lbl.next_to(axes.c2p(mid_x_full, f(mid_x_full)), UP, buff=0.30)

        self.play(
            FadeIn(th_dot), Write(th_lbl),
            FadeIn(area_full), FadeIn(strip_area),
            Write(Ath_lbl),
            run_time=0.7,
        )

        eq2 = MathTex(
            r"A(t{+}h)-A(t)",
            r"=\int_t^{t+h}\!f(s)\,ds",
            font_size=24, color=WHITE,
        )
        eq2.move_to(UP * 2.3)
        self.play(
            FadeOut(def_eq),
            Write(eq2),
            run_time=0.7,
        )
        self.wait(0.5)

        
        
        
        rw  = axes.c2p(th_val, 0)[0] - axes.c2p(t_val, 0)[0]
        rph = axes.c2p(0, f(t_val))[1] - axes.c2p(0, 0)[1]

        rect_outline = Rectangle(
            width=rw, height=rph,
            fill_color=C_STRIP, fill_opacity=0.0,
            stroke_color=C_TH, stroke_width=3.0,
        )
        rect_outline.move_to(axes.c2p(t_val, 0) + RIGHT * rw / 2 + UP * rph / 2)

        ft_dot = Dot(axes.c2p(t_val, f(t_val)), color=C_T, radius=0.09)
        ft_dashed = DashedLine(
            axes.c2p(t_val, f(t_val)), axes.c2p(th_val, f(t_val)),
            color=C_T, stroke_width=2.0,
        )
        height_arrow = DoubleArrow(
            axes.c2p(t_val - 0.18, 0),
            axes.c2p(t_val - 0.18, f(t_val)),
            color=C_T, buff=0, stroke_width=2.2, tip_length=0.12,
        )
        
        ht_lbl = MathTex(r"\underbrace{f(t)}_{\text{height}}", font_size=20, color=C_T)
        ht_lbl.next_to(height_arrow, LEFT, buff=0.10)
        ht_lbl.shift(UP * 0.18)   

        width_arrow = DoubleArrow(
            axes.c2p(t_val, -0.38),   
            axes.c2p(th_val, -0.38),
            color=C_TH, buff=0, stroke_width=2.2, tip_length=0.12,
        )
        wd_lbl = MathTex(r"\underbrace{h}_{\text{width}}", font_size=20, color=C_TH)
        wd_lbl.next_to(width_arrow, DOWN, buff=0.10)

        self.play(
            Create(rect_outline),
            FadeIn(ft_dot), Create(ft_dashed),
            Create(height_arrow), Write(ht_lbl),
            Create(width_arrow), Write(wd_lbl),
            run_time=0.9,
        )

        
        bot1 = MathTex(
            r"\int_t^{t+h}\!f(s)\,ds",
            r"\;\approx\;",
            r"f(t)",
            r"\cdot\,",
            r"h",
            font_size=25, color=WHITE,
        )
        bot1[2].set_color(C_T)
        bot1[4].set_color(C_TH)
        bot1.move_to(DOWN * 3.40)   
        self.play(Write(bot1), run_time=0.7)
        self.wait(0.7)

        
        
        
        s1 = MathTex(
            r"A(t{+}h) - A(t)",
            r"\;=\;",
            r"f(t)",
            r"\cdot\,",
            r"h",
            font_size=25, color=WHITE,
        )
        s1[2].set_color(C_T)
        s1[4].set_color(C_TH)
        s1.move_to(DOWN * 3.40)
        self.play(ReplacementTransform(bot1, s1), run_time=0.6)
        self.wait(0.4)

        s2 = MathTex(
            r"\frac{A(t{+}h) - A(t)}{",
            r"h",
            r"}",
            r"\;=\;",
            r"f(t)",
            font_size=25, color=WHITE,
        )
        s2[1].set_color(C_TH)
        s2[4].set_color(C_T)
        s2.move_to(DOWN * 3.40)
        self.play(ReplacementTransform(s1, s2), run_time=0.9)
        self.wait(0.5)

        
        
        
        h_tracker = ValueTracker(h_init)

        def get_strip():
            hv = max(h_tracker.get_value(), 0.004)
            return axes.get_area(curve, x_range=[t_val, t_val + hv],
                                 color=C_STRIP, opacity=0.65)

        def get_rect():
            hv = max(h_tracker.get_value(), 0.004)
            w  = axes.c2p(t_val + hv, 0)[0] - axes.c2p(t_val, 0)[0]
            ph = axes.c2p(0, f(t_val))[1]   - axes.c2p(0, 0)[1]
            r = Rectangle(
                width=max(w, 0.003), height=ph,
                fill_color=C_STRIP, fill_opacity=0.50,
                stroke_color=C_TH, stroke_width=2.5,
            )
            r.move_to(axes.c2p(t_val, 0) + RIGHT * w / 2 + UP * ph / 2)
            return r

        def get_th_dot():
            return Dot(axes.c2p(t_val + h_tracker.get_value(), 0),
                       color=C_TH, radius=0.08)

        def get_th_lbl():
            hv = h_tracker.get_value()
            return MathTex("t{+}h", font_size=22, color=C_TH).next_to(
                axes.c2p(t_val + hv, 0), DOWN, buff=0.15)

        def get_ft_line():
            hv = max(h_tracker.get_value(), 0.004)
            return DashedLine(
                axes.c2p(t_val, f(t_val)),
                axes.c2p(t_val + hv, f(t_val)),
                color=C_T, stroke_width=2.0,
            )

        def get_width_arrow():
            hv = max(h_tracker.get_value(), 0.004)
            return DoubleArrow(
                axes.c2p(t_val, -0.38),
                axes.c2p(t_val + hv, -0.38),
                color=C_TH, buff=0, stroke_width=2.2, tip_length=0.12,
            )

        strip_dyn       = always_redraw(get_strip)
        rect_dyn        = always_redraw(get_rect)
        thdot_dyn       = always_redraw(get_th_dot)
        thlbl_dyn       = always_redraw(get_th_lbl)
        ftline_dyn      = always_redraw(get_ft_line)
        width_arrow_dyn = always_redraw(get_width_arrow)

        self.remove(
            strip_area, area_full, th_dot, th_lbl,
            ft_dashed, rect_outline, width_arrow,
            Ath_lbl,
        )
        self.add(strip_dyn, rect_dyn, thdot_dyn, thlbl_dyn,
                 ftline_dyn, width_arrow_dyn)

        self.play(FadeOut(eq2), run_time=0.4)

        self.play(
            h_tracker.animate.set_value(0.015),
            FadeOut(wd_lbl),
            run_time=2.4, rate_func=smooth,
        )
        self.wait(0.4)

        
        
        
        def_eq2 = MathTex(r"A(t)=\int_a^t f(s)\,ds", font_size=27, color=WHITE)
        def_eq2.move_to(UP * 2.30)

        s3 = MathTex(
            r"\lim_{h\to 0}\frac{A(t{+}h)-A(t)}{",
            r"h",
            r"}",
            r"\;=\;",
            r"f(t)",
            font_size=24, color=WHITE,
        )
        s3[1].set_color(C_TH)
        s3[4].set_color(C_T)
        s3.move_to(DOWN * 3.40)

        self.play(
            Write(def_eq2),
            ReplacementTransform(s2, s3),
            run_time=0.8,
        )
        self.wait(0.5)

        
        
        
        
        

        
        s4 = MathTex(r"A'(t)", r"\;=\;", r"f(t)", font_size=30, color=WHITE)
        s4[0].set_color(C_T)
        s4[2].set_color(C_T)
        s4.move_to(DOWN * 3.40)
        self.play(ReplacementTransform(s3, s4), run_time=0.8)
        self.wait(0.5)

        
        self.play(
            s4.animate.set_color(YELLOW).scale(1.15),
            run_time=0.4, rate_func=there_and_back,
        )

        
        top_final = MathTex(
            r"\frac{d}{dt}\int_a^t\!f(s)\,ds \;=\; f(t)",
            font_size=38,
        )
        top_final.set_color_by_gradient(BLUE, RED)
        top_final.move_to(UP * 2.20)

        
        
        self.play(
            FadeOut(def_eq2),
            s4.animate.move_to(UP * 2.20).set_opacity(0),
            run_time=0.6,
        )
        
        self.play(
            Write(top_final),
            run_time=1.1,
        )

        self.wait(3.0)