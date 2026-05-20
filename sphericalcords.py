from manim import *
import numpy as np

class SphericalCoordinateSystem(ThreeDScene):
    def construct(self):
        
        
        title = MathTex(
            r"\mathbb{S}\mathrm{pherical} \ \mathbb{C}\mathrm{oordinate} \ \mathbb{S}\mathrm{ystem}",
            font_size=40
        )
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.3)
        
        
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES, zoom=0.75)
        self.camera.frame_center = [0, 0, -0.2]  
        
        axes = ThreeDAxes(
            x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4],
            x_length=8, y_length=8, z_length=8
        )
        
        lab_x = axes.get_x_axis_label(MathTex("x", color=RED))
        lab_y = axes.get_y_axis_label(MathTex("y", color=GREEN))
        lab_z = axes.get_z_axis_label(MathTex("z", color=BLUE))
        
        
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), Create(axes, lag_ratio=0.1), FadeIn(lab_x), FadeIn(lab_y), FadeIn(lab_z), run_time=2, rate_func=smooth)

        
        r_val = 3.0
        sphere = Surface(
            lambda u, v: np.array([
                r_val * np.cos(u) * np.sin(v),
                r_val * np.sin(u) * np.sin(v),
                r_val * np.cos(v)
            ]),
            v_range=[0, PI],
            u_range=[0, 2 * PI],
            resolution=(24, 24),
            fill_opacity=0.1,
            stroke_width=0.5,
            stroke_opacity=0.2,
            checkerboard_colors=[GRAY_D, GRAY_E]
        )
        self.play(FadeIn(sphere), run_time=1.5, rate_func=smooth)

        
        theta_val = 60 * DEGREES
        phi_val = 50 * DEGREES

        
        x = r_val * np.sin(phi_val) * np.cos(theta_val)
        y = r_val * np.sin(phi_val) * np.sin(theta_val)
        z = r_val * np.cos(phi_val)
        point = np.array([x, y, z])
        proj = np.array([x, y, 0])
        origin = np.array([0, 0, 0])

        
        r_line = Line3D(origin, point, color=GOLD)
        r_label = MathTex(r"\rho", font_size=36).move_to(r_line.get_center() + UP * 0.3)
        
        
        
        r_label.rotate(90*DEGREES, axis=RIGHT).rotate(90*DEGREES, axis=OUT) 

        dot = Dot3D(point=point, color=ORANGE, radius=0.1)
        p_label = MathTex(r"P(\rho, \theta, \varphi)", color=ORANGE, font_size=30).next_to(dot, RIGHT)
        
        
        p_label.rotate(90*DEGREES, axis=RIGHT)
        
        p_label.rotate(45*DEGREES, axis=OUT) 

        self.play(Create(r_line), FadeIn(dot), run_time=1)
        self.add(r_label, p_label) 

        
        
        drop_line = DashedLine(point, proj, color=BLUE_D)
        proj_line = Line(origin, proj, color=BLUE_D)
        
        self.play(Create(drop_line), Create(proj_line), run_time=1, rate_func=smooth)

        
        
        proj_len = np.linalg.norm(proj)
        
        
        
        theta_line = Line(origin, [proj_len, 0, 0], color=RED, stroke_width=4)
        self.play(Create(theta_line), run_time=0.5, rate_func=smooth)
        
        
        self.play(
            Rotate(theta_line, angle=theta_val, axis=OUT, about_point=origin),
            run_time=2, rate_func=smooth
        )
        
        
        theta_sector = Sector(radius=0.8, start_angle=0, angle=theta_val, color=RED, fill_opacity=0.5)
        theta_text = MathTex(r"\theta", color=RED).move_to(
            1.0 * np.array([np.cos(theta_val/2), np.sin(theta_val/2), 0])
        )
        self.play(FadeIn(theta_sector), Write(theta_text), rate_func=smooth)
        
        
        
        
        
        
        phi_line = Line(origin, [0, 0, r_val], color=PINK, stroke_width=4)
        self.play(Create(phi_line), run_time=0.5, rate_func=smooth)
        
        
        rot_axis = np.array([-np.sin(theta_val), np.cos(theta_val), 0])
        
        self.play(
            Rotate(phi_line, angle=phi_val, axis=rot_axis, about_point=origin),
            run_time=2, rate_func=smooth
        )
        
        
        
        
        
        arc_radius = 1.2
        num_points = 20
        arc_points = []
        for i in range(num_points + 1):
            angle = i * phi_val / num_points
            arc_point = arc_radius * np.array([
                np.sin(angle) * np.cos(theta_val),
                np.sin(angle) * np.sin(theta_val),
                np.cos(angle)
            ])
            arc_points.append(arc_point)
        
        
        phi_arc = VMobject(color=PINK, stroke_width=4)
        phi_arc.set_points_as_corners(arc_points)
        phi_arc.make_smooth()
        
        
        sector_points = [origin] + arc_points + [origin]
        phi_sector = VMobject(fill_color=PINK, fill_opacity=0.3, stroke_width=0)
        phi_sector.set_points_as_corners(sector_points)
        
        phi_text_pos = 1.5 * np.array([
            np.sin(phi_val/2) * np.cos(theta_val),
            np.sin(phi_val/2) * np.sin(theta_val),
            np.cos(phi_val/2)
        ])
        phi_text = MathTex(r"\varphi", color=PINK).move_to(phi_text_pos)
        
        phi_text.rotate(90*DEGREES, axis=RIGHT)
        
        self.play(FadeIn(phi_sector), Create(phi_arc), Write(phi_text), rate_func=smooth)

        
        
        
        eq1 = MathTex(r"x", r"=", r"\rho", r"\sin", r"\varphi", r"\cos", r"\theta", font_size=34)
        eq2 = MathTex(r"y", r"=", r"\rho", r"\sin", r"\varphi", r"\sin", r"\theta", font_size=34)
        eq3 = MathTex(r"z", r"=", r"\rho", r"\cos", r"\varphi", font_size=34)
        
        formulas = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        
        box = SurroundingRectangle(formulas, color=WHITE, fill_color=BLACK, fill_opacity=0.7, corner_radius=0.2)
        group = VGroup(box, formulas).to_edge(DOWN, buff=2.0) 
        
        
        self.add_fixed_in_frame_mobjects(group)
        
        
        self.play(
            FadeIn(box),
            Write(formulas),
            run_time=1.5
        )
        
        
        
        self.play(
            Indicate(r_line, scale_factor=1.1, color=GOLD),
            Indicate(r_label, scale_factor=1.3, color=GOLD),
            Indicate(eq1[2], scale_factor=1.3, color=GOLD),  
            Indicate(phi_text, scale_factor=1.3, color=PINK),
            Indicate(eq1[4], scale_factor=1.3, color=PINK),  
            Indicate(theta_text, scale_factor=1.3, color=RED),
            Indicate(eq1[6], scale_factor=1.3, color=RED),  
            run_time=1
        )
        
        
        self.play(
            Indicate(r_line, scale_factor=1.1, color=GOLD),
            Indicate(r_label, scale_factor=1.3, color=GOLD),
            Indicate(eq2[2], scale_factor=1.3, color=GOLD),  
            Indicate(phi_text, scale_factor=1.3, color=PINK),
            Indicate(eq2[4], scale_factor=1.3, color=PINK),  
            Indicate(theta_text, scale_factor=1.3, color=RED),
            Indicate(eq2[6], scale_factor=1.3, color=RED),  
            run_time=1
        )
        
        
        self.play(
            Indicate(r_line, scale_factor=1.1, color=GOLD),
            Indicate(r_label, scale_factor=1.3, color=GOLD),
            Indicate(eq3[2], scale_factor=1.3, color=GOLD),  
            Indicate(phi_text, scale_factor=1.3, color=PINK),
            Indicate(eq3[4], scale_factor=1.3, color=PINK),  
            run_time=1
        )

        self.wait(1)

        self.wait(1)

        
        pyth_eq = MathTex(r"\rho^2 = x^2 + y^2 + z^2", font_size=40)
        pyth_eq.set_color_by_tex("rho", GOLD)
        pyth_eq.set_color_by_tex("x", RED)
        pyth_eq.set_color_by_tex("y", GREEN)
        pyth_eq.set_color_by_tex("z", BLUE)
        
        pyth_box = SurroundingRectangle(pyth_eq, color=WHITE, fill_color=BLACK, fill_opacity=0.7, corner_radius=0.2)
        pyth_group = VGroup(pyth_box, pyth_eq).next_to(group, DOWN, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(pyth_group)
        self.play(FadeIn(pyth_box), Write(pyth_eq), run_time=1.5)
        
        self.wait(3)