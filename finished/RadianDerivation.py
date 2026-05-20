from manim import *

class ElegantRadianAnimation(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        title = MathTex("\\mathbb{D}\\text{erivation of a }\\mathbb{R}\\text{adian}", 
                       color=TEAL_C, font_size=28)
        title.to_edge(UP, buff=0.6)
        title.set_glow_opacity(0.6)
        
        
        self.play(
            Write(title, run_time=2),
            rate_func=smooth
        )
        
        
        radius_line = Line(ORIGIN, RIGHT * 1.0, color=ORANGE, stroke_width=4)
        radius_line.set_glow_opacity(0.8)
        
        
        radius_label = MathTex("1~\\text{radius}", color=ORANGE, font_size=20)
        radius_label.next_to(radius_line, DOWN, buff=0.2)
        radius_label.set_glow_opacity(0.8)
        
        self.play(
            DrawBorderThenFill(radius_line, run_time=1.5),
            FadeIn(radius_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        circle = Circle(radius=1.0, color=GREY_B, stroke_width=2, stroke_opacity=0.5)
        
        
        rotating_radius = radius_line.copy()
        
        
        self.play(
            Create(circle, run_time=2),
            Rotate(rotating_radius, angle=2*PI, about_point=ORIGIN, run_time=2),
            rate_func=smooth
        )
        
        
        self.remove(rotating_radius)
        
        
        axes = Axes(
            x_range=[-0.6, 0.6, 0.5],
            y_range=[-0.6, 0.6, 0.5],
            x_length=4,
            y_length=4,
            axis_config={
                "color": GREY_B, 
                "stroke_width": 1, 
                "stroke_opacity": 0.4,
                "tip_length": 0.02,
                "tip_width": 0.04
            }
        )
        
        self.play(
            FadeIn(axes, run_time=1),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        
        tangent_line = Line(RIGHT * 1.0, RIGHT * 1.0 + UP * 1.0, color=ORANGE, stroke_width=4)
        tangent_line.set_glow_opacity(0.8)
        
        
        self.play(
            Transform(radius_line, tangent_line, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        
        target_arc = Arc(
            radius=1.0,
            start_angle=0,
            angle=1,
            color=BLUE_C,
            stroke_width=5
        )
        target_arc.set_glow_opacity(0.8)
        
        
        self.play(
            Transform(radius_line, target_arc, run_time=2.5),
            rate_func=smooth
        )
        
        
        blue_arc = radius_line
        
        self.wait(0.5)
        
        
        
        angle_label_position = LEFT * 1.3 + DOWN * 0.8
        
        
        first_sector = Sector(
            angle=1,
            radius=1.0,
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        
        angle_mark_1 = Arc(
            radius=0.3,
            start_angle=0,
            angle=1,
            color=BLUE_C,
            stroke_width=2
        )
        angle_mark_1.set_glow_opacity(0.8)
        
        
        one_radian_label = MathTex("1~\\text{radian}", color=BLUE_C, font_size=20)
        one_radian_label.move_to(angle_label_position)
        one_radian_label.set_glow_opacity(0.8)
        
        
        self.play(
            radius_label.animate.move_to(angle_label_position).set_color(BLUE_C),
            FadeIn(first_sector, run_time=1),
            Create(angle_mark_1, run_time=1),
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        
        self.play(
            Transform(radius_label, one_radian_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        second_arc = Arc(
            radius=1.0,
            start_angle=1,
            angle=1,
            color=GREEN_C,
            stroke_width=5
        )
        second_arc.set_glow_opacity(0.8)
        
        second_sector = Sector(
            angle=1,
            radius=1.0,
            start_angle=1,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        
        angle_mark_2 = Arc(
            radius=0.3,
            start_angle=1,
            angle=1,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_2.set_glow_opacity(0.8)
        
        
        count_label_2 = MathTex("2~\\text{radians}", color=GREEN_C, font_size=20)
        count_label_2.move_to(angle_label_position)
        count_label_2.set_glow_opacity(0.8)
        
        self.play(
            Create(second_arc, run_time=1.5),
            FadeIn(second_sector, run_time=1.5),
            Create(angle_mark_2, run_time=1.5),
            Transform(radius_label, count_label_2, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        third_arc = Arc(
            radius=1.0,
            start_angle=2,
            angle=1,
            color=GREEN_C,
            stroke_width=5
        )
        third_arc.set_glow_opacity(0.8)
        
        third_sector = Sector(
            angle=1,
            radius=1.0,
            start_angle=2,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        
        angle_mark_3 = Arc(
            radius=0.3,
            start_angle=2,
            angle=1,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_3.set_glow_opacity(0.8)
        
        
        count_label_3 = MathTex("3~\\text{radians}", color=GREEN_C, font_size=20)
        count_label_3.move_to(angle_label_position)
        count_label_3.set_glow_opacity(0.8)
        
        self.play(
            Create(third_arc, run_time=1.5),
            FadeIn(third_sector, run_time=1.5),
            Create(angle_mark_3, run_time=1.5),
            Transform(radius_label, count_label_3, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        
        
        final_gap_arc = Arc(
            radius=1.0,
            start_angle=3,
            angle=PI - 3,  
            color=GREEN_C,
            stroke_width=5
        )
        final_gap_arc.set_glow_opacity(0.8)
        
        final_gap_sector = Sector(
            angle=PI - 3,
            radius=1.0,
            start_angle=3,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        
        angle_mark_final = Arc(
            radius=0.3,
            start_angle=3,
            angle=PI - 3,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_final.set_glow_opacity(0.8)
        
        
        pi_label = MathTex("\\pi~\\text{radians}", color=GREEN_C, font_size=20)
        pi_label.move_to(angle_label_position)
        pi_label.set_glow_opacity(0.8)
        
        self.play(
            Create(final_gap_arc, run_time=1.5),
            FadeIn(final_gap_sector, run_time=1.5),
            Create(angle_mark_final, run_time=1.5),
            Transform(radius_label, pi_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(1)
        
        
        
        second_half_arc = Arc(
            radius=1.0,
            start_angle=PI,
            angle=PI,
            color=GREEN_C,
            stroke_width=5
        )
        second_half_arc.set_glow_opacity(0.8)
        
        second_half_sector = Sector(
            angle=PI,
            radius=1.0,
            start_angle=PI,
            color=GREEN_C,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        
        second_half_angle_mark = Arc(
            radius=0.3,
            start_angle=PI,
            angle=PI,
            color=GREEN_C,
            stroke_width=2
        )
        second_half_angle_mark.set_glow_opacity(0.8)
        
        
        two_pi_label = MathTex("2\\pi~\\text{radians}", color=GREEN_C, font_size=20)
        two_pi_label.move_to(angle_label_position)
        two_pi_label.set_glow_opacity(0.8)
        
        
        self.play(
            Create(second_half_arc, run_time=1.5),
            FadeIn(second_half_sector, run_time=1.5),
            Create(second_half_angle_mark, run_time=1.5),
            Transform(radius_label, two_pi_label, run_time=1.5),
            rate_func=smooth
        )
        
        
        self.wait(3)
        
        
        self.play(
            FadeOut(VGroup(
                axes, circle, blue_arc, second_arc, third_arc, final_gap_arc, 
                first_sector, second_sector, third_sector, final_gap_sector,
                second_half_arc, second_half_sector, angle_mark_1, angle_mark_2, 
                angle_mark_3, angle_mark_final, second_half_angle_mark, 
                radius_label, title
            ), run_time=2),
            rate_func=smooth
        )
        
        self.wait(1)