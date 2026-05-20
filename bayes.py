from manim import *


WHEAT = "#F5DEB3"
SKY_BLUE = "#87CEEB"
SOIL_BROWN = "#5C4033"
FOREST_GREEN = "#228B22"

class BayesTheoremVisual(Scene):
    """
    A scene that visually explains the core intuition behind Bayes' Theorem.
    It shows how a prior belief is updated with new evidence to form a
    posterior belief.
    """
    def construct(self):
        
        
        self.camera.background_color = SOIL_BROWN
        
        
        
        hook = Tex("How do we update our beliefs?", font_size=60, color=WHEAT)

        
        title = MathTex(r"\mathbb{B}\text{ayes' }\mathbb{T}\text{heorem}", font_size=96)
        title.set_color_by_gradient(SKY_BLUE, WHEAT)
        title.to_edge(UP, buff=0.5)

        self.play(Write(hook))
        self.wait(1)
        
        self.play(ReplacementTransform(hook, title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title))

        
        
        
        content_group = VGroup().move_to(ORIGIN)

        
        prior_circle = Circle(radius=1.5, color=SKY_BLUE, fill_opacity=0.6)
        prior_circle.move_to(LEFT * 1.2)
        prior_label = MathTex("P(A)", color=SKY_BLUE).next_to(prior_circle, UP, buff=0.2)
        
        content_group.add(prior_circle, prior_label)

        self.play(
            Create(prior_circle), 
            Write(prior_label), 
            run_time=1.5
        )
        self.wait(0.5)

        
        evidence_circle = Circle(radius=1.8, color=WHEAT, fill_opacity=0.6)
        evidence_circle.move_to(RIGHT * 1.2)
        evidence_label = MathTex("P(B)", color=WHEAT).next_to(evidence_circle, UP, buff=0.2)
        
        content_group.add(evidence_circle, evidence_label)

        self.play(
            Create(evidence_circle), 
            Write(evidence_label), 
            run_time=1.5
        )
        self.wait(1)

        
        intersection_area = Intersection(
            prior_circle, evidence_circle, color=FOREST_GREEN, fill_opacity=0.7
        )
        content_group.add(intersection_area)

        self.play(FadeIn(intersection_area))
        self.wait(1)
        
        
        self.play(content_group.animate.scale(0.8).to_edge(DOWN, buff=1.0))
        self.wait(0.5)

        
        formula = MathTex(
            r"P(A|B)", r"=", r"\frac{P(B|A) P(A)}{P(B)}",
            font_size=72
        ).to_edge(UP, buff=1.5)
        
        self.play(Write(formula))
        self.wait(1)

        
        
        self.play(Indicate(formula.get_part_by_tex("P(A)"), color=SKY_BLUE), Indicate(prior_circle, color=SKY_BLUE))
        self.wait(0.5)

        self.play(Indicate(formula.get_part_by_tex("P(B)"), color=WHEAT), Indicate(evidence_circle, color=WHEAT))
        self.wait(0.5)

        
        
        temp_highlight_A = prior_circle.copy().set_fill(SKY_BLUE, opacity=0.9)
        self.play(Indicate(formula.get_part_by_tex("P(B|A)"), color=FOREST_GREEN))
        self.play(FadeIn(temp_highlight_A, scale=1.05), run_time=0.5)
        self.play(Transform(temp_highlight_A, intersection_area.copy().set_color(FOREST_GREEN)), run_time=1)
        self.play(FadeOut(temp_highlight_A), run_time=0.5)
        self.wait(0.5)

        
        
        self.play(Indicate(formula.get_part_by_tex("P(A|B)"), color=FOREST_GREEN))
        self.wait(0.5)

        
        
        
        self.play(
            FadeOut(prior_label),
            FadeOut(evidence_label),
            Transform(prior_circle, intersection_area.copy()), 
            run_time=1.5
        )
        self.wait(0.5)
        
        
        evidence_highlight = evidence_circle.copy().set_stroke(WHEAT, width=8)
        self.play(Create(evidence_highlight))
        self.wait(0.5)

        
        final_posterior_area = prior_circle 
        self.play(final_posterior_area.animate.set_fill(FOREST_GREEN, opacity=1.0).scale(1.1))
        
        
        final_label = MathTex("P(A|B)", color=WHITE).move_to(final_posterior_area.get_center())
        self.play(Write(final_label))
        self.wait(2)

        
        
        self.play(FadeOut(*self.mobjects))
        self.wait(1)

