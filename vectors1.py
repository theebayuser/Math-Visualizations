



import numpy as np
from manim import *
from manim.utils.space_ops import normalize


COLOR_A_TXT = "#a1b4ff"  
COLOR_B_TXT = "#ffdc64"  
COLOR_CROSS_TXT = PURPLE 

class CrossProductRecreation(ThreeDScene):
    """
    A Manim scene that visualizes the cross product of two vectors,
    recreating the animation with proper 3D perspective and flat circle.
    """
    def construct(self):
        
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES, distance=8)

        
        title = MathTex(
            r"\mathbb{C}ross\ \mathbb{P}roduct\ \mathbb{V}isualization",
            font_size=36,
            color=WHITE
        ).to_edge(UP, buff=0.5)
        
        
        plane_circle = Circle(
            radius=3, 
            stroke_color=GRAY, 
            stroke_opacity=0.6,
            stroke_width=2,
            fill_opacity=0.05,
            fill_color=GRAY
        )  
        
        
        grid_lines = VGroup()
        for i in range(-3, 4):
            if i != 0:  
                
                grid_lines.add(Line(
                    [i, -3, 0], [i, 3, 0], 
                    stroke_color=GRAY, stroke_opacity=0.3, stroke_width=1
                ))
                
                grid_lines.add(Line(
                    [-3, i, 0], [3, i, 0], 
                    stroke_color=GRAY, stroke_opacity=0.3, stroke_width=1
                ))
        
        
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"stroke_width": 2, "stroke_opacity": 0.7}
        )
        
        
        x_label = MathTex("x", font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y", font_size=24).next_to(axes.y_axis.get_end(), UP)
        z_label = MathTex("z", font_size=24).next_to(axes.z_axis.get_end(), OUT)
        
        
        angle_a = ValueTracker(PI / 4) 
        
        
        def create_3d_vector(direction, color, thickness=0.05):
            """Create a proper 3D arrow with cylindrical shaft and conical tip"""
            length = np.linalg.norm(direction)
            if length == 0:
                return VGroup()
            
            unit_dir = direction / length
            
            
            shaft_length = length * 0.85
            shaft = Cylinder(
                radius=thickness,
                height=shaft_length,
                direction=unit_dir,
                color=color,
                fill_opacity=0.9
            ).shift(unit_dir * shaft_length / 2)
            
            
            tip_length = length * 0.15
            tip = Cone(
                base_radius=thickness * 2.5,
                height=tip_length,
                direction=unit_dir,
                color=color,
                fill_opacity=0.9
            ).shift(unit_dir * (shaft_length + tip_length / 2))
            
            return VGroup(shaft, tip)
        
        vec_a = create_3d_vector([2, 0, 0], RED)
        vec_b = create_3d_vector([2.5, 0, 0], BLUE)  
        cross_prod = create_3d_vector([0, 0, 1], PURPLE) 

        
        side_len = 0.4
        angle_marker = VGroup(
            Line(ORIGIN, side_len * RIGHT),
            Line(side_len * RIGHT, side_len * (RIGHT + UP)),
            Line(side_len * (RIGHT + UP), side_len * UP)
        ).set_stroke(color=YELLOW, width=4).set_opacity(0)

        
        
        
        def update_vec_a(m):
            angle = angle_a.get_value()
            direction = np.array([2 * np.cos(angle), 2 * np.sin(angle), 0])
            new_vec = create_3d_vector(direction, RED)
            m.become(new_vec)
            
        
        def update_cross_product(m):
            angle = angle_a.get_value()
            a_vec = np.array([2 * np.cos(angle), 2 * np.sin(angle), 0])
            b_vec = np.array([2.5, 0, 0])
            
            cross_vec = np.cross(a_vec, b_vec) * 0.8
            
            
            if np.linalg.norm(cross_vec) > 0.01:
                new_cross = create_3d_vector(cross_vec, PURPLE)
                m.become(new_cross)
            else:
                m.become(VGroup())  
        
        
        def update_angle_marker(m):
            angle = angle_a.get_value()
            a_unit = normalize(np.array([np.cos(angle), np.sin(angle), 0]))
            b_unit = normalize(np.array([1, 0, 0]))
            
            dot_product = np.dot(a_unit, b_unit)
            
            opacity = max(0, 1 - 25 * abs(dot_product))
            m.set_opacity(opacity)
            
            if opacity > 0.1:
                new_marker = VGroup(
                    Line(ORIGIN, side_len * a_unit),
                    Line(side_len * a_unit, side_len * (a_unit + b_unit)),
                    Line(side_len * (a_unit + b_unit), side_len * b_unit)
                ).set_stroke(color=YELLOW, width=4)
                m.become(new_marker)

        
        vec_a.add_updater(update_vec_a)
        cross_prod.add_updater(update_cross_product)
        angle_marker.add_updater(update_angle_marker)
        
        
        
        tex_config = {"font_size": 42}
        
        
        perp_line1 = MathTex(
            r"\mathbf{a} \perp \mathbf{b}",
            tex_to_color_map={r"\mathbf{a}": COLOR_A_TXT, r"\mathbf{b}": COLOR_B_TXT},
            **tex_config
        )
        perp_line2 = MathTex(
            r"|\mathbf{a} \times \mathbf{b}| = |\mathbf{a}| |\mathbf{b}|",
            tex_to_color_map={r"\mathbf{a}": COLOR_A_TXT, r"\mathbf{b}": COLOR_B_TXT, r"\times": COLOR_CROSS_TXT},
            **tex_config
        )
        perp_text = VGroup(perp_line1, perp_line2).arrange(DOWN, buff=0.3)

        
        para_line1 = MathTex(
            r"\mathbf{a} \parallel \mathbf{b}",
            tex_to_color_map={r"\mathbf{a}": COLOR_A_TXT, r"\mathbf{b}": COLOR_B_TXT},
            **tex_config
        )
        para_line2 = MathTex(
            r"|\mathbf{a} \times \mathbf{b}| = 0",
            tex_to_color_map={r"\mathbf{a}": COLOR_A_TXT, r"\mathbf{b}": COLOR_B_TXT, r"\times": COLOR_CROSS_TXT},
            **tex_config
        )
        para_text = VGroup(para_line1, para_line2).arrange(DOWN, buff=0.3)

        
        label_a = MathTex(r"\mathbf{a}", color=COLOR_A_TXT, font_size=32)
        label_b = MathTex(r"\mathbf{b}", color=COLOR_B_TXT, font_size=32)
        label_cross = MathTex(r"\mathbf{a} \times \mathbf{b}", 
                             tex_to_color_map={r"\mathbf{a}": COLOR_A_TXT, r"\mathbf{b}": COLOR_B_TXT, r"\times": COLOR_CROSS_TXT},
                             font_size=28)

        
        
        
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        
        
        self.add(axes, x_label, y_label, z_label)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.add(plane_circle, grid_lines)
        self.play(Create(plane_circle), Create(grid_lines))
        self.wait(0.5)
        
        
        self.add(vec_b, vec_a)
        self.play(Create(vec_b), Create(vec_a))
        
        
        label_b.next_to([2.5, 0, 0], RIGHT + UP)
        self.add_fixed_in_frame_mobjects(label_b)
        self.play(Write(label_b))
        
        
        self.play(angle_a.animate.set_value(PI / 2), run_time=2)
        self.add(cross_prod, angle_marker)
        
        
        label_a.next_to([0, 2, 0], UP + RIGHT)
        label_cross.next_to([0, 0, 2], RIGHT)
        self.add_fixed_in_frame_mobjects(label_a, label_cross)
        self.play(Write(label_a), Write(label_cross))
        self.wait(1)

        
        
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        
        perp_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(perp_text)
        self.play(Write(perp_text))
        self.wait(3)
        self.play(Unwrite(perp_text))
        self.remove_fixed_in_frame_mobjects(perp_text)
        
        
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.wait(0.5)
        
        
        self.play(angle_a.animate.set_value(PI), run_time=3)
        
        para_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(para_text)
        self.play(Write(para_text))
        self.wait(3)
        self.play(Unwrite(para_text))
        self.remove_fixed_in_frame_mobjects(para_text)
        self.wait(0.5)
        
        
        self.play(angle_a.animate.set_value(3 * PI / 2), run_time=3)
        
        
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        
        perp_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(perp_text)
        self.play(Write(perp_text))
        self.wait(3)
        self.play(Unwrite(perp_text))
        self.remove_fixed_in_frame_mobjects(perp_text)
        
        
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.wait(0.5)
        
        
        self.play(angle_a.animate.set_value(2 * PI), run_time=3)
        
        para_text.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(para_text)
        self.play(Write(para_text))
        self.wait(3)
        self.play(Unwrite(para_text))
        self.remove_fixed_in_frame_mobjects(para_text)
        self.wait(1)
        
        
        self.play(angle_a.animate.set_value(4 * PI), run_time=6)
        self.wait(2)
        
        
        self.play(
            *[FadeOut(mob) for mob in [
                plane_circle, grid_lines, axes, x_label, y_label, z_label,
                vec_a, vec_b, cross_prod, angle_marker
            ]], 
            run_time=2
        )
        self.remove_fixed_in_frame_mobjects(title, label_a, label_b, label_cross)
        self.play(FadeOut(title), FadeOut(label_a), FadeOut(label_b), FadeOut(label_cross))
        self.wait(1)