from manim import *


class TelescopingSeriesReel(Scene):
    """A fast-paced, vertical-friendly reel that introduces the idea of a telescoping series.

    Visual pacing is tuned for ~15–20-second Instagram Reels (9:16 layout):
    1. Flashy title.
    2. Present the general series \sum (1/k − 1/(k+1)).
    3. Expand first few terms, animate cancellations with striking color fades.
    4. Reveal the compact partial-sum formula (1 − 1/(n+1)).
    5. Let n→∞ and celebrate the limit 1 with a burst.
    """

    def construct(self):
        
        self.camera.background_color = BLACK  

        
        
        
        title = Text("TELESCOPING SERIES", font_size=68, gradient=(BLUE, GREEN))
        subtitle = Text("Why do the terms vanish?", font_size=40, color=GRAY_C)
        VGroup(title, subtitle).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.7)

        self.play(Write(title, run_time=0.6))
        self.play(FadeIn(subtitle, shift=DOWN * 0.3, run_time=0.4))
        self.wait(0.3)
        self.play(FadeOut(subtitle, run_time=0.3))

        
        
        
        series_general = MathTex(r"\displaystyle\sum_{k=1}^{n}\left(\frac{1}{k}-\frac{1}{k+1}\right)", font_size=60)
        series_general.set_color_by_tex_to_color_map({"1": YELLOW, "k": WHITE, "k+1": TEAL})
        series_general.next_to(title, DOWN, buff=0.9)

        self.play(Write(series_general, run_time=0.9))
        self.wait(0.4)

        
        
        
        expanded_terms = MathTex(
            r"\big(1 - \tfrac{1}{2}\big) + ",
            r"\big(\tfrac{1}{2} - \tfrac{1}{3}\big) + ",
            r"\big(\tfrac{1}{3} - \tfrac{1}{4}\big) + \dots + ",
            r"\big(\tfrac{1}{n} - \tfrac{1}{n+1}\big)",
            font_size=48
        )
        expanded_terms.set_color(TEAL_A)
        expanded_terms.next_to(series_general, DOWN, buff=0.9)

        
        self.play(TransformMatchingTex(series_general.copy(), expanded_terms, run_time=1.1))
        self.wait(0.3)

        
        
        cancel_parts = [
            *expanded_terms[0][7:10],   
            *expanded_terms[1][5:8],    
            *expanded_terms[1][9:12],   
            *expanded_terms[2][5:8],    
        ]  

        self.play(*(c.animate.set_color(RED).set_opacity(0.6) for c in cancel_parts), run_time=0.5)
        self.play(*(FadeOut(c) for c in cancel_parts), run_time=0.6)  

        
        self.play(expanded_terms.animate.set_opacity(0.35), run_time=0.3)

        
        
        
        partial_sum = MathTex(r"=\, 1 - \frac{1}{n+1}", font_size=60)
        partial_sum.set_color_by_tex_to_color_map({"1": YELLOW, "\frac{1}{n+1}": TEAL_A})
        partial_sum.next_to(expanded_terms, DOWN, buff=0.7, aligned_edge=LEFT)

        self.play(Write(partial_sum, run_time=0.8))
        self.wait(0.5)

        
        
        
        limit_expr = MathTex(r"\displaystyle\lim_{n\to\infty}\left(1 - \frac{1}{n+1}\right) = 1", font_size=60)
        limit_expr.set_color_by_tex_to_color_map({"1": YELLOW})
        limit_expr.next_to(partial_sum, DOWN, buff=0.9)

        self.play(Transform(partial_sum.copy(), limit_expr, run_time=1.0))
        self.wait(0.4)

        
        big_one = Text("1", font_size=160, gradient=(YELLOW, ORANGE)).move_to(limit_expr.get_center() + DOWN * 0.5)
        glow = SurroundingRectangle(big_one, color=ORANGE, buff=0.2)
        glow.set_stroke(width=8)

        self.play(
            FadeIn(big_one, scale=0.3, run_time=0.6),
            Create(glow, run_time=0.6)
        )
        self.play(big_one.animate.scale(1.15), rate_func=there_and_back, run_time=0.6)

        self.wait(1)



if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        TelescopingSeriesReel().render() 