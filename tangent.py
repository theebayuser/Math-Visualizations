
from manim import *


config.background_color = "#000000"

class HalfAngleTangentVisual(Scene):
    def construct(self):
        
        
        
        C_MAIN = WHITE
        C_SIN = GREEN_B
        C_COS = YELLOW_B
        C_HYPOT = BLUE_B
        C_ANGLE = RED_B
        C_TRI_1 = BLUE_D
        C_TRI_2 = GREEN_D
        C_FORMULA = WHITE
        
        
        radius = 2.4  
        origin_point = ORIGIN + DOWN * 0.4 
        theta_value = 70 * DEGREES  
        label_font_size = 26 

        
        
        
        title = MathTex(
            r"\mathbb{T}\text{angent } \mathbb{H}\text{alf-Angle } \mathbb{I}\text{dentity}",
            font_size=39 
        )
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.1) 
        
        
        self.add(title)
        self.wait(0.5) 

        
        
        
        center_dot = Dot(origin_point, color=C_MAIN)
        diameter = Line(
            origin_point + LEFT * radius, 
            origin_point + RIGHT * radius, 
            color=C_MAIN,
            stroke_width=3
        )
        
        
        left_radius_label = MathTex("1", color=C_MAIN, font_size=label_font_size)
        left_radius_label.next_to(origin_point + LEFT * (radius / 2), DOWN, buff=0.16) 
        
        
        self.play(
            FadeIn(center_dot, scale=0.5), 
            Create(diameter),
            Write(left_radius_label),
            run_time=1.0
        )
        
        

        
        sweeping_radius = Line(origin_point, origin_point + RIGHT * radius, color=C_HYPOT, stroke_width=2)
        sweeping_label = MathTex("1", color=C_HYPOT, font_size=label_font_size)
        sweeping_label.add_updater(
            lambda m: m.next_to(
                sweeping_radius.get_center(),
                normalize(sweeping_radius.get_vector()),
                buff=0.28 
            )
        )
        semicircle = Arc(
            radius=radius, 
            start_angle=0, 
            angle=PI, 
            color=C_MAIN,
            stroke_width=3
        ).move_arc_center_to(origin_point)
        
        self.play(Create(sweeping_radius), Write(sweeping_label), run_time=0.5)
        
        
        self.play(
            Rotate(sweeping_radius, angle=PI, about_point=origin_point),
            Create(semicircle),
            run_time=1.0
        )
        
        
        self.play(FadeOut(sweeping_radius), FadeOut(sweeping_label), run_time=0.5)
        
        
        
        self.play(FadeOut(title, shift=UP), run_time=0.5)


        
        
        
        endpoint = semicircle.point_from_proportion(theta_value / PI)
        cos_point = np.array([endpoint[0], origin_point[1], 0])
        left_end_point = origin_point + LEFT * radius
        right_end_point = origin_point + RIGHT * radius

        
        radius_line = Line(origin_point, endpoint, color=C_HYPOT)
        
        
        one_label = MathTex("1", color=C_HYPOT, font_size=label_font_size)
        
        perp_vector = rotate_vector(radius_line.get_vector(), 90 * DEGREES)
        one_label.move_to(radius_line.get_center()).shift(normalize(perp_vector) * 0.32) 

        
        
        theta_arc = Arc(
            radius=0.56, 
            start_angle=0, 
            angle=theta_value, 
            color=C_ANGLE,
            arc_center=origin_point
        )
        theta_label = MathTex(r"\theta", color=C_ANGLE, font_size=label_font_size)
        theta_label.move_to(
            Arc(radius=0.8, angle=theta_value, arc_center=origin_point).point_from_proportion(0.5) 
        )
        
        
        self.play(
            Create(radius_line),
            Write(one_label),
            run_time=1.0
        )
        self.play(
            Create(theta_arc),
            Write(theta_label),
            run_time=1.0
        )

        
        
        
        sin_line = Line(endpoint, cos_point, color=C_SIN)
        sin_label = MathTex(r"\sin(\theta)", color=C_SIN, font_size=label_font_size)
        sin_label.next_to(sin_line, RIGHT, buff=0.16) 
        
        
        cos_line = Line(origin_point, cos_point, color=C_COS)
        cos_label = MathTex(r"\cos(\theta)", color=C_COS, font_size=label_font_size)
        cos_label.next_to(cos_line, DOWN, buff=0.16) 
        
        self.play(
            Create(sin_line),
            Create(cos_line),
            run_time=1.0
        )
        self.play(
            Write(sin_label),
            Write(cos_label),
            run_time=1.0
        )

        
        
        
        one_minus_cos_line = Line(cos_point, right_end_point, color=C_COS, stroke_width=6)
        one_minus_cos_label = MathTex(r"1 - \cos(\theta)", color=C_COS, font_size=label_font_size)
        one_minus_cos_label.next_to(one_minus_cos_line, DOWN, buff=0.16) 
        
        self.play(Create(one_minus_cos_line), run_time=1.0)
        self.play(Write(one_minus_cos_label), run_time=1.0)

        
        
        iso_line = Line(left_end_point, endpoint, color=C_TRI_1)
        iso_tri = Polygon(
            left_end_point, 
            origin_point, 
            endpoint, 
            fill_color=C_TRI_1, 
            fill_opacity=0.4, 
            stroke_color=C_TRI_1
        )
        
        self.play(FadeIn(iso_tri), Create(iso_line), run_time=1.0)
        
        
        half_theta_arc = Arc(
            radius=0.8, 
            start_angle=0, 
            angle=theta_value / 2, 
            color=C_ANGLE,
            arc_center=left_end_point
        )
        half_theta_label = MathTex(r"\frac{\theta}{2}", color=C_ANGLE, font_size=label_font_size)
        
        half_theta_label.move_to(
            Arc(radius=1.12, angle=theta_value / 2, arc_center=left_end_point).point_from_proportion(0.5) 
        )
        
        self.play(Create(half_theta_arc), Write(half_theta_label), run_time=1.5)

        
        
        thales_line = Line(right_end_point, endpoint, color=C_MAIN, stroke_width=2)
        self.play(Create(thales_line), run_time=1.0)


        
        
        
        formula_1 = MathTex(
            r"\tan\left(\frac{\theta}{2}\right)", "=", r"{\sin(\theta) \over 1 + \cos(\theta)}",
            color=C_FORMULA,
            font_size=32 
        )
        formula_2 = MathTex(
            r"=", r"{1 - \cos(\theta) \over \sin(\theta)}",
            color=C_FORMULA,
            font_size=32 
        )
        
        
        formula_1.get_part_by_tex(r"\sin(\theta)").set_color(C_SIN)
        formula_1.get_part_by_tex(r"\cos(\theta)").set_color(C_COS)
        formula_2.get_part_by_tex(r"\cos(\theta)").set_color(C_COS)
        formula_2.get_part_by_tex(r"\sin(\theta)").set_color(C_SIN)
        
        
        formula_group = VGroup(formula_1, formula_2).arrange(RIGHT, buff=0.16) 
        
        formula_group.to_edge(DOWN, buff=1.2) 
        

        big_right_tri = Polygon(
            left_end_point, 
            cos_point, 
            endpoint, 
            fill_color=C_TRI_2, 
            fill_opacity=0.4, 
            stroke_color=C_TRI_2
        )
        
        opp_1 = sin_line.copy().set_stroke(color=C_SIN, width=6)
        adj_1 = Line(left_end_point, cos_point, color=C_COS, stroke_width=6)
        
        self.play(FadeOut(iso_tri), FadeIn(big_right_tri), run_time=0.5)
        self.play(Create(opp_1), Create(adj_1), run_time=1.0)
        
        
        self.play(Write(formula_1), run_time=1.0)
        self.play(FadeOut(opp_1), FadeOut(adj_1), run_time=0.5)

        
        
        small_right_tri = Polygon(
            cos_point, 
            right_end_point, 
            endpoint, 
            fill_color=C_TRI_1, 
            fill_opacity=0.5, 
            stroke_color=C_TRI_1
        )
        
        opp_2 = one_minus_cos_line.copy().set_stroke(color=C_COS, width=6)
        adj_2 = sin_line.copy().set_stroke(color=C_SIN, width=6)
        
        self.play(FadeOut(big_right_tri), FadeIn(small_right_tri), run_time=0.5)
        self.play(Create(opp_2), Create(adj_2), run_time=1.0)
        
        
        self.play(Write(formula_2), run_time=1.0)
        self.play(FadeOut(opp_2), FadeOut(adj_2), FadeOut(small_right_tri), run_time=0.5)

        
        self.wait(0.5)
        
        
        figure_group = VGroup(
            center_dot, diameter, left_radius_label, semicircle, 
            radius_line, one_label, theta_arc, theta_label, 
            sin_line, sin_label, cos_line, cos_label, 
            one_minus_cos_line, one_minus_cos_label, 
            iso_line, half_theta_arc, half_theta_label, thales_line
        )
        
        
        self.play(FadeOut(figure_group), run_time=1.0)
        self.play(formula_group.animate.move_to(ORIGIN), run_time=1.0)
        self.wait(1.0)