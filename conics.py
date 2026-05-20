import numpy as np
from manim import *

# Set the background to black for the final output video.
# To render, use the command: manim -pql your_script_name.py ConicSectionsRecreation
# config.background_color = BLACK

class ConicSectionsRecreation(ThreeDScene):
    """
    This Manim scene recreates a popular 3D visualization of conic sections.
    It shows how intersecting a double cone with a plane at different angles
    produces a circle, ellipse, parabola, and hyperbola, as well as their
    degenerate forms (point, line, two intersecting lines).

    The screen is split into two panels:
    - Left: A 3D view of the cone and the intersecting plane.
    - Right: A 2D view of the resulting intersection curve.
    """

    def construct(self):
        # 1. SETUP THE SCENE
        # -------------------
        # Split-screen setup with black on the left and white on the right.
        left_bg = Rectangle(
            height=config.frame_height, width=config.frame_width / 2,
            stroke_width=0, fill_color=BLACK, fill_opacity=1
        ).to_edge(LEFT, buff=0)
        right_bg = Rectangle(
            height=config.frame_height, width=config.frame_width / 2,
            stroke_width=0, fill_color=WHITE, fill_opacity=1
        ).to_edge(RIGHT, buff=0)
        self.add(left_bg, right_bg)

        # Set the 3D camera angle to match the source video.
        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES)

        # Define cone parameters. We use a slope of 2.
        cone_height = 4
        cone_radius = 2
        cone_slope = cone_height / cone_radius  # This is 'k' in the equations.

        # Create the double cone using the modern Manim API.
        # A single Cone object with a height now creates a double cone by default.
        double_cone = Cone(
            base_radius=cone_radius,
            height=cone_height,
            direction=Z_AXIS,
            resolution=48,
        )
        double_cone.set_style(fill_opacity=0.35, stroke_width=0)
        double_cone.set_color_by_gradient(PURPLE_D, TEAL_D)
        
        # Position the 3D cone on the left panel.
        scene_3d_origin = [-config.frame_width / 4, 0, 0]
        double_cone.move_to(scene_3d_origin)
        self.add(double_cone)


        # 2. CREATE KEYFRAME STATES
        # -------------------------
        # We define each conic section state (plane, 3D curve, 2D curve)
        # and then animate the transformations between them.
        
        # Parameters for the plane equation z = m*x + c
        # State 1: Point (degenerate circle)
        g_point_3d, g_point_2d = self.get_section_geometry(m=0, c=0.001, cone_slope=cone_slope, origin=scene_3d_origin)
        
        # State 2: Circle
        g_circle_3d, g_circle_2d = self.get_section_geometry(m=0, c=1.5, cone_slope=cone_slope, origin=scene_3d_origin)
        
        # State 3: Ellipse
        g_ellipse_3d, g_ellipse_2d = self.get_section_geometry(m=1.0, c=1.5, cone_slope=cone_slope, origin=scene_3d_origin)
        
        # State 4: Parabola
        g_parabola_3d, g_parabola_2d = self.get_section_geometry(m=2.0, c=1.5, cone_slope=cone_slope, origin=scene_3d_origin)
        
        # State 5: Hyperbola
        g_hyperbola_3d, g_hyperbola_2d = self.get_section_geometry(m=2.5, c=1.5, cone_slope=cone_slope, origin=scene_3d_origin)
        
        # State 6: Two Intersecting Lines (degenerate hyperbola)
        g_two_lines_3d, g_two_lines_2d = self.get_section_geometry(m=2.5, c=0.001, cone_slope=cone_slope, origin=scene_3d_origin)

        # State 7: One Line (degenerate parabola) - for the final jump cut
        g_one_line_3d, g_one_line_2d = self.get_section_geometry(m=2.0, c=0.001, cone_slope=cone_slope, origin=scene_3d_origin)


        # 3. ANIMATION SEQUENCE
        # ---------------------
        
        # Start with the point
        self.play(Create(g_point_3d), Create(g_point_2d), run_time=1)
        self.wait(0.5)

        # Point -> Circle
        self.play(
            Transform(g_point_3d, g_circle_3d),
            Transform(g_point_2d, g_circle_2d),
            run_time=2
        )
        self.wait(0.5)
        current_g3d, current_g2d = g_circle_3d, g_circle_2d

        # Circle -> Ellipse
        self.play(
            Transform(current_g3d, g_ellipse_3d),
            Transform(current_g2d, g_ellipse_2d),
            run_time=2
        )
        self.wait(0.5)
        current_g3d, current_g2d = g_ellipse_3d, g_ellipse_2d

        # Ellipse -> Parabola
        self.play(
            Transform(current_g3d, g_parabola_3d),
            Transform(current_g2d, g_parabola_2d),
            run_time=2
        )
        self.wait(0.5)
        current_g3d, current_g2d = g_parabola_3d, g_parabola_2d

        # Parabola -> Hyperbola
        self.play(
            Transform(current_g3d, g_hyperbola_3d),
            Transform(current_g2d, g_hyperbola_2d),
            run_time=2
        )
        self.wait(0.5)
        current_g3d, current_g2d = g_hyperbola_3d, g_hyperbola_2d

        # Hyperbola -> Two Intersecting Lines
        self.play(
            Transform(current_g3d, g_two_lines_3d),
            Transform(current_g2d, g_two_lines_2d),
            run_time=2
        )
        self.wait(1)
        
        # Replicating the jump cuts at the end of the video
        
        # Fade to One Line
        self.play(FadeOut(current_g3d, current_g2d))
        self.play(FadeIn(g_one_line_3d, g_one_line_2d))
        self.wait(1.5)

        # Fade to Point (re-creating it for a clean fade-in)
        self.play(FadeOut(g_one_line_3d, g_one_line_2d))
        g_final_point_3d, g_final_point_2d = self.get_section_geometry(m=0, c=0.001, cone_slope=cone_slope, origin=scene_3d_origin)
        self.play(FadeIn(g_final_point_3d, g_final_point_2d))
        self.wait(1.5)


    def get_section_geometry(self, m, c, cone_slope, origin):
        """
        Calculates and creates the geometry for a given conic section.

        Args:
            m (float): The slope of the intersecting plane (z = m*x + c).
            c (float): The z-intercept of the intersecting plane.
            cone_slope (float): The slope (k) of the cone walls.
            origin (list): The center of the 3D scene.

        Returns:
            tuple: A VGroup for the 3D objects (plane, 3D curve) and a
                   VGroup for the 2D curve.
        """
        # Define constants from parameters
        k = cone_slope
        k2 = k**2
        m2 = m**2

        # Create the intersecting plane
        # CORRECTION: u_range and v_range are now positional arguments.
        # CORRECTION: resolution is now a tuple for best practice.
        plane = Surface(
            lambda u, v: np.array([u, v, m * u + c]),
            [-5, 5], # u_range
            [-5, 5], # v_range
            resolution=(10, 10),
            fill_opacity=0.3,
            checkerboard_colors=[GRAY, DARK_GRAY],
            stroke_width=0
        )

        # Initialize containers for the curves
        curve_3d = VGroup()
        curve_2d = VGroup()

        # Handle degenerate cases first (when c is very close to zero)
        if abs(c) < 0.1:
            if abs(m2 - k2) > 0.1 and m2 < k2:  # Point
                curve_3d.add(Dot3D(point=ORIGIN, color=BLACK, radius=0.08))
                curve_2d.add(Dot(color=BLACK, radius=0.08))
            elif abs(m2 - k2) < 0.1:  # One Line
                line_3d = ParametricFunction(lambda t: [t, 0, m * t], t_range=[-4, 4], color=BLACK, stroke_width=6)
                curve_3d.add(line_3d)
                curve_2d.add(Line([-4, 0, 0], [4, 0, 0], color=BLACK, stroke_width=6))
            else:  # Two Intersecting Lines
                s_y = np.sqrt(m2 - k2) / k
                line1_3d = ParametricFunction(lambda t: [t, s_y * t, m * t], t_range=[-3, 3], color=BLACK, stroke_width=6)
                line2_3d = ParametricFunction(lambda t: [t, -s_y * t, m * t], t_range=[-3, 3], color=BLACK, stroke_width=6)
                curve_3d.add(line1_3d, line2_3d)
                
                line1_2d = Line(ORIGIN, [4, 4 * s_y, 0], color=BLACK, stroke_width=6)
                line2_2d = Line(ORIGIN, [4, -4 * s_y, 0], color=BLACK, stroke_width=6)
                lines_2d = VGroup(line1_2d.copy().rotate(PI, about_point=ORIGIN), line1_2d,
                                  line2_2d.copy().rotate(PI, about_point=ORIGIN), line2_2d)
                curve_2d.add(lines_2d)

        # Handle non-degenerate cases
        else:
            if abs(m2 - k2) > 0.1 and m2 < k2:  # Ellipse or Circle
                den = k2 - m2
                x0 = (m * c) / den
                a = abs(c * k) / den
                b = abs(c) / np.sqrt(den)
                
                func_2d = lambda t: [x0 + a * np.cos(t), b * np.sin(t), 0]
                func_3d = lambda t: [func_2d(t)[0], func_2d(t)[1], m * func_2d(t)[0] + c]
                curve_2d.add(ParametricFunction(func_2d, t_range=[0, TAU], color=BLACK, stroke_width=6))
                curve_3d.add(ParametricFunction(func_3d, t_range=[0, TAU], color=BLACK, stroke_width=6))

            elif abs(m2 - k2) < 0.1:  # Parabola
                func_2d = lambda t: [(k2 * t**2 - c**2) / (2 * m * c), t, 0]
                func_3d = lambda t: [func_2d(t)[0], func_2d(t)[1], m * func_2d(t)[0] + c]
                curve_2d.add(ParametricFunction(func_2d, t_range=[-4, 4], color=BLACK, stroke_width=6))
                curve_3d.add(ParametricFunction(func_3d, t_range=[-4, 4], color=BLACK, stroke_width=6))

            else:  # Hyperbola
                den = m2 - k2
                x0 = -m * c / den
                a = abs(c * k) / den
                b = abs(c) / np.sqrt(den)
                t_range = [-2.5, 2.5]

                # First branch
                func_2d_1 = lambda t: [x0 + a * np.cosh(t), b * np.sinh(t), 0]
                func_3d_1 = lambda t: [func_2d_1(t)[0], func_2d_1(t)[1], m * func_2d_1(t)[0] + c]
                # Second branch
                func_2d_2 = lambda t: [x0 - a * np.cosh(t), b * np.sinh(t), 0]
                func_3d_2 = lambda t: [func_2d_2(t)[0], func_2d_2(t)[1], m * func_2d_2(t)[0] + c]

                curve_2d.add(ParametricFunction(func_2d_1, t_range=t_range, color=BLACK, stroke_width=6),
                               ParametricFunction(func_2d_2, t_range=t_range, color=BLACK, stroke_width=6))
                curve_3d.add(ParametricFunction(func_3d_1, t_range=t_range, color=BLACK, stroke_width=6),
                               ParametricFunction(func_3d_2, t_range=t_range, color=BLACK, stroke_width=6))

        # Group and position the final geometry
        group_3d = VGroup(plane, curve_3d).move_to(origin)
        
        # Position the 2D curve on the right panel and scale it to fit.
        group_2d = VGroup(curve_2d)
        if group_2d.get_width() > 0 and group_2d.get_height() > 0:
            group_2d.scale_to_fit_height(3.5)
        group_2d.move_to([config.frame_width / 4, 0, 0])

        return group_3d, group_2d