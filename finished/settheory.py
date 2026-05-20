from manim import *

class SetTheoryExploration(Scene):
    def construct(self):
        
        BG_COLOR = BLACK
        SET_A_COLOR = BLUE_C
        SET_B_COLOR = RED_C
        UNION_COLOR = PURPLE
        INTERSECTION_COLOR = GREEN_C
        DIFFERENCE_COLOR = ORANGE
        COMPLEMENT_COLOR = TEAL_C
        UNIVERSAL_COLOR = GREY_A
        SUBSET_COLOR = YELLOW
        DISJOINT_COLOR = PINK
        
        
        self.camera.background_color = BG_COLOR
        
        
        main_title = MathTex("\\mathbb{S}\\text{et}\\ \\mathbb{T}\\text{heory}", color=WHITE, font_size=72)
        main_title.set_color_by_gradient(BLUE_C, PURPLE, RED_C)
        main_title.move_to(UP * 3.2)  
        
        self.play(
            Write(main_title),
            run_time=0.8
        )
        self.wait(0.5)
        
        
        
        set_a = Circle(radius=1.0, color=SET_A_COLOR, fill_opacity=0.15)
        set_a.set_stroke(SET_A_COLOR, 4)
        set_a.move_to(LEFT * 0.8 + DOWN * 1.2)  
        set_a.set_glow_opacity(0.8)
        
        set_b = Circle(radius=1.0, color=SET_B_COLOR, fill_opacity=0.15)
        set_b.set_stroke(SET_B_COLOR, 4)
        set_b.move_to(RIGHT * 0.8 + DOWN * 1.2)  
        set_b.set_glow_opacity(0.8)
        
        
        label_a = MathTex("A", color=SET_A_COLOR, font_size=40)
        label_a.move_to(set_a.get_center() + LEFT * 0.7)  
        
        label_b = MathTex("B", color=SET_B_COLOR, font_size=40)
        label_b.move_to(set_b.get_center() + RIGHT * 0.7)  
        
        
        self.play(
            DrawBorderThenFill(set_a),
            DrawBorderThenFill(set_b),
            Write(label_a),
            Write(label_b),
            run_time=0.6
        )
        
        
        union_title = MathTex("A \\cup B", color=WHITE, font_size=48)
        union_title[0][0].set_color(SET_A_COLOR)
        union_title[0][2].set_color(SET_B_COLOR)
        union_title[0][1].set_color(UNION_COLOR)
        union_title.move_to(UP * 1.8)  
        
        union_word = Text("Union", color=UNION_COLOR, font_size=28)
        union_word.next_to(union_title, DOWN, buff=0.15)
        
        self.play(
            Write(union_title),
            Write(union_word),
            run_time=0.5
        )
        
        
        union_region = Union(set_a, set_b)
        union_region.set_fill(UNION_COLOR, opacity=0.4)
        union_region.set_stroke(UNION_COLOR, 6)
        union_region.set_glow_opacity(1.0)
        
        self.play(
            DrawBorderThenFill(union_region),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(union_region),
            FadeOut(union_title),
            FadeOut(union_word),
            run_time=0.4
        )
        
        
        intersection_title = MathTex("A \\cap B", color=WHITE, font_size=48)
        intersection_title[0][0].set_color(SET_A_COLOR)
        intersection_title[0][2].set_color(SET_B_COLOR)
        intersection_title[0][1].set_color(INTERSECTION_COLOR)
        intersection_title.move_to(UP * 1.8)  
        
        intersection_word = Text("Intersection", color=INTERSECTION_COLOR, font_size=28)
        intersection_word.next_to(intersection_title, DOWN, buff=0.15)
        
        self.play(
            Write(intersection_title),
            Write(intersection_word),
            run_time=0.5
        )
        
        
        intersection_region = Intersection(set_a, set_b)
        intersection_region.set_fill(INTERSECTION_COLOR, opacity=0.5)
        intersection_region.set_stroke(INTERSECTION_COLOR, 6)
        intersection_region.set_glow_opacity(1.0)
        
        self.play(
            DrawBorderThenFill(intersection_region),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(intersection_region),
            FadeOut(intersection_title),
            FadeOut(intersection_word),
            run_time=0.4
        )
        
        
        
        universal_set = Rectangle(
            width=5.0, height=3.0,  
            color=UNIVERSAL_COLOR,
            fill_opacity=0.1
        )
        universal_set.set_stroke(UNIVERSAL_COLOR, 3)
        universal_set.move_to(DOWN * 1.2)  
        
        universal_label = MathTex("U", color=UNIVERSAL_COLOR, font_size=36)
        universal_label.move_to(universal_set.get_corner(UP + LEFT) + DOWN * 0.3 + RIGHT * 0.3)
        
        self.play(
            DrawBorderThenFill(universal_set),
            Write(universal_label),
            run_time=0.5
        )
        
        complement_title = MathTex("A'", color=WHITE, font_size=48)
        complement_title[0][0].set_color(SET_A_COLOR)
        complement_title[0][1].set_color(COMPLEMENT_COLOR)
        complement_title.move_to(UP * 1.8)  
        
        complement_word = Text("Complement", color=COMPLEMENT_COLOR, font_size=28)
        complement_word.next_to(complement_title, DOWN, buff=0.15)
        
        self.play(
            Write(complement_title),
            Write(complement_word),
            run_time=0.5
        )
        
        
        complement_region = Difference(universal_set, set_a)
        complement_region.set_fill(COMPLEMENT_COLOR, opacity=0.3)
        complement_region.set_stroke(COMPLEMENT_COLOR, 6)
        complement_region.set_glow_opacity(1.0)
        
        self.play(
            DrawBorderThenFill(complement_region),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(complement_region),
            FadeOut(complement_title),
            FadeOut(complement_word),
            run_time=0.4
        )
        
        
        
        subset_title = MathTex("B \\subseteq A", color=WHITE, font_size=48)
        subset_title[0][0].set_color(SET_B_COLOR)
        subset_title[0][2].set_color(SET_A_COLOR)
        subset_title[0][1].set_color(SUBSET_COLOR)
        subset_title.move_to(UP * 1.8)  
        
        subset_word = Text("Subset", color=SUBSET_COLOR, font_size=28)
        subset_word.next_to(subset_title, DOWN, buff=0.15)
        
        self.play(
            Write(subset_title),
            Write(subset_word),
            run_time=0.5
        )
        
        
        subset_b = Circle(radius=0.6, color=SET_B_COLOR, fill_opacity=0.2)
        subset_b.set_stroke(SET_B_COLOR, 4)
        subset_b.move_to(set_a.get_center() + RIGHT * 0.2)
        subset_b.set_glow_opacity(0.8)
        
        
        new_label_b = MathTex("B", color=SET_B_COLOR, font_size=36)
        new_label_b.move_to(subset_b.get_center())
        
        self.play(
            Transform(set_b, subset_b),
            Transform(label_b, new_label_b),
            run_time=0.8
        )
        
        
        subset_highlight = subset_b.copy()
        subset_highlight.set_fill(SUBSET_COLOR, opacity=0.3)
        subset_highlight.set_stroke(SUBSET_COLOR, 6)
        subset_highlight.set_glow_opacity(1.0)
        
        self.play(
            DrawBorderThenFill(subset_highlight),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(subset_highlight),
            FadeOut(subset_title),
            FadeOut(subset_word),
            run_time=0.4
        )
        
        
        proper_subset_title = MathTex("B \\subsetneq A", color=WHITE, font_size=48)
        proper_subset_title[0][0].set_color(SET_B_COLOR)
        proper_subset_title[0][2].set_color(SET_A_COLOR)
        proper_subset_title[0][1].set_color(ORANGE)
        proper_subset_title.move_to(UP * 1.8)  
        
        proper_subset_word = Text("Proper Subset", color=ORANGE, font_size=28)
        proper_subset_word.next_to(proper_subset_title, DOWN, buff=0.15)
        
        self.play(
            Write(proper_subset_title),
            Write(proper_subset_word),
            run_time=0.5
        )
        
        
        proper_highlight = subset_b.copy()
        proper_highlight.set_fill(ORANGE, opacity=0.3)
        proper_highlight.set_stroke(ORANGE, 6)
        proper_highlight.set_glow_opacity(1.0)
        
        
        remaining_a = Difference(set_a, subset_b)
        remaining_a.set_fill(GREY_A, opacity=0.2)
        remaining_a.set_stroke(GREY_A, 3)
        
        self.play(
            DrawBorderThenFill(proper_highlight),
            DrawBorderThenFill(remaining_a),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(proper_highlight),
            FadeOut(remaining_a),
            FadeOut(proper_subset_title),
            FadeOut(proper_subset_word),
            run_time=0.4
        )
        
        
        superset_title = MathTex("A \\supseteq B", color=WHITE, font_size=48)
        superset_title[0][0].set_color(SET_A_COLOR)
        superset_title[0][2].set_color(SET_B_COLOR)
        superset_title[0][1].set_color(TEAL_C)
        superset_title.move_to(UP * 1.8)  
        
        superset_word = Text("Superset", color=TEAL_C, font_size=28)
        superset_word.next_to(superset_title, DOWN, buff=0.15)
        
        self.play(
            Write(superset_title),
            Write(superset_word),
            run_time=0.5
        )
        
        
        superset_highlight = set_a.copy()
        superset_highlight.set_fill(TEAL_C, opacity=0.2)
        superset_highlight.set_stroke(TEAL_C, 6)
        superset_highlight.set_glow_opacity(1.0)
        
        self.play(
            DrawBorderThenFill(superset_highlight),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(superset_highlight),
            FadeOut(superset_title),
            FadeOut(superset_word),
            run_time=0.4
        )
        
        
        
        original_set_a = Circle(radius=1.0, color=SET_A_COLOR, fill_opacity=0.15)
        original_set_a.set_stroke(SET_A_COLOR, 4)
        original_set_a.move_to(LEFT * 0.8 + DOWN * 1.2)  
        original_set_a.set_glow_opacity(0.8)
        
        original_set_b = Circle(radius=1.0, color=SET_B_COLOR, fill_opacity=0.15)
        original_set_b.set_stroke(SET_B_COLOR, 4)
        original_set_b.move_to(RIGHT * 0.8 + DOWN * 1.2)  
        original_set_b.set_glow_opacity(0.8)
        
        original_label_a = MathTex("A", color=SET_A_COLOR, font_size=40)
        original_label_a.move_to(original_set_a.get_center() + LEFT * 0.7)  
        
        original_label_b = MathTex("B", color=SET_B_COLOR, font_size=40)
        original_label_b.move_to(original_set_b.get_center() + RIGHT * 0.7)  
        
        self.play(
            Transform(set_a, original_set_a),
            Transform(set_b, original_set_b),
            Transform(label_a, original_label_a),
            Transform(label_b, original_label_b),
            run_time=0.8
        )
        
        membership_title = MathTex("x \\in A", color=WHITE, font_size=48)
        membership_title[0][0].set_color(YELLOW)
        membership_title[0][2].set_color(SET_A_COLOR)
        membership_title[0][1].set_color(GREEN_C)
        membership_title.move_to(UP * 1.8)  
        
        membership_word = Text("Membership", color=GREEN_C, font_size=28)
        membership_word.next_to(membership_title, DOWN, buff=0.15)
        
        self.play(
            Write(membership_title),
            Write(membership_word),
            run_time=0.5
        )
        
        
        element_x = Dot(color=YELLOW, radius=0.08)
        element_x.move_to(original_set_a.get_center() + LEFT * 0.2 + UP * 0.2)
        element_x.set_glow_opacity(1.0)
        
        element_label = MathTex("x", color=YELLOW, font_size=32)
        element_label.next_to(element_x, UP, buff=0.1)
        
        self.play(
            Create(element_x),
            Write(element_label),
            run_time=0.6
        )
        
        
        membership_circle = Circle(radius=0.15, color=GREEN_C, stroke_width=4)  
        membership_circle.move_to(element_x.get_center())
        membership_circle.set_fill(GREEN_C, opacity=0.3)
        
        self.play(
            DrawBorderThenFill(membership_circle),
            run_time=0.6
        )
        self.wait(0.5)
        
        
        self.play(
            FadeOut(element_x),
            FadeOut(element_label),
            FadeOut(membership_circle),
            FadeOut(membership_title),
            FadeOut(membership_word),
            run_time=0.4
        )
        
        
        
        final_elements = VGroup(set_a, set_b, label_a, label_b, universal_set, universal_label, main_title)
        
        self.play(
            FadeOut(final_elements),
            run_time=1.0
        )
        
        self.wait(0.3)