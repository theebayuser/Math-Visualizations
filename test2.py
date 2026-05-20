from manim import *
import numpy as np

# Configure for Instagram Reel (Vertical 9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class ConicSectionsReel(ThreeDScene):
    def construct(self):
        # --- Aesthetics ---
        self.camera.background_color = "#000510"  # Deep dark blue/black
        
        # Colors
        CONE_COLOR = BLUE_E
        PLANE_COLOR = TEAL_E
        HIGHLIGHT_COLOR = YELLOW
        TEXT_COLOR = WHITE
        
        # --- Layout Config ---
        # 3D objects shifted LEFT
        # 2D objects shifted RIGHT (in fixed frame)
        OFFSET_3D = LEFT * 2.5
        OFFSET_2D = RIGHT * 2.1
        
        # --- Title Sequence ---
        # Title with mathbb first letters and gradient
        title = MathTex(
            r"\mathbb{C}\text{onic } \mathbb{S}\text{ections}",
            font_size=80
        )
        title.set_color_by_gradient(BLUE, RED)
        
        # Fix title to camera
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=1.5)
        
        # --- 3D Setup (Left Side) ---
        # Camera Orientation: Static, Front View
        self.set_camera_orientation(phi=75 * DEGREES, theta=-90 * DEGREES, zoom=0.85)
        
        # Cone Parameters
        h = 3.5
        r = 3.0
        
        # Create Cone Surface
        cone = Surface(
            lambda u, v: np.array([
                (r * u / h) * np.cos(v),
                (r * u / h) * np.sin(v),
                u
            ]),
            u_range=[-h, h],
            v_range=[0, TAU],
            resolution=(32, 32),
            checkerboard_colors=[CONE_COLOR, CONE_COLOR],
            fill_opacity=0.4,
            stroke_color=BLUE_A,
            stroke_width=0.5,
        )
        cone.shift(OFFSET_3D)
        
        self.add(cone) # Start with cone visible

        # --- 2D Setup (Right Side) ---
        # Coordinate System for 2D graphs
        axes_2d = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={
                "include_tip": True, 
                "tip_width": 0.2, 
                "tip_height": 0.2,
                "color": GRAY_C
            }
        )
        axes_2d.shift(OFFSET_2D)
        
        # Container for 2D elements
        right_panel = VGroup(axes_2d)
        self.add_fixed_in_frame_mobjects(right_panel)
        
        # Label setup
        label = Tex("", font_size=60, color=HIGHLIGHT_COLOR).to_edge(DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(label)
        
        # --- Animation Functions ---
        
        def get_plane_and_curve_3d(name):
            """Returns (plane_surface, curve_3d_mobject) for the given conic type"""
            if name == "Circle":
                # Plane z = 1.0 (Horizontal)
                plane = Surface(
                    lambda u, v: np.array([u, v, 1.0]),
                    u_range=[-3, 3], v_range=[-3, 3],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                curve = ParametricFunction(
                    lambda t: np.array([
                        (r * 1.0 / h) * np.cos(t),
                        (r * 1.0 / h) * np.sin(t),
                        1.0
                    ]), t_range=[0, TAU], color=HIGHLIGHT_COLOR, stroke_width=8
                )
            
            elif name == "Ellipse":
                # Plane z = 0.5y + 1.0 (Tilted)
                # slope m = 0.5. Angle = arctan(0.5)
                slope = 0.5
                intercept = 1.0
                plane = Surface(
                    lambda u, v: np.array([u, v, slope * v + intercept]),
                    u_range=[-3, 3], v_range=[-3, 3],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                # Visually approximate curve for 3D view (stable rendering)
                # An Ellipse in 2D rotated in 3D
                curve = Ellipse(width=2.5, height=3.0, color=HIGHLIGHT_COLOR, stroke_width=8)
                curve.rotate(np.arctan(slope), RIGHT)
                curve.move_to(np.array([0, 0.6, 1.3])) 
                
            elif name == "Parabola":
                # Plane z = 1.16 y + 1.0 (Parallel to generator slope ~1.16)
                slope = h/r # 3.5/3.0 = 1.166
                intercept = 1.0
                plane = Surface(
                    lambda u, v: np.array([u, v, slope * v + intercept]),
                    u_range=[-3, 3], v_range=[-2.5, 2.5],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                # Visual Parabola
                curve = ParametricFunction(
                    lambda t: np.array([
                        t,
                        0.4 * t**2 - 0.5,
                        slope * (0.4 * t**2 - 0.5) + intercept
                    ]), t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=8
                )
                
            elif name == "Hyperbola":
                # Plane x = 1.2 (Vertical)
                # Simple vertical cut
                plane = Surface(
                    lambda u, v: np.array([1.2, u, v]), # x=1.2, spread in y/z
                    u_range=[-3, 3], v_range=[-3, 3],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                # Hyperbola curve in 3D: x=1.2. 
                # Cone: x^2 + y^2 = (z*r/h)^2 ==> 1.44 + y^2 = k^2 z^2
                # k^2 z^2 - y^2 = 1.44
                # z = +/- sqrt((1.44 + y^2))/k
                k = r/h
                curve = ParametricFunction(
                    lambda t: np.array([
                        1.2,
                        t,
                        np.sqrt(1.2**2 + t**2) / k
                    ]), t_range=[-2.5, 2.5], color=HIGHLIGHT_COLOR, stroke_width=8
                )
                curve2 = ParametricFunction(
                    lambda t: np.array([
                        1.2,
                        t,
                        -np.sqrt(1.2**2 + t**2) / k
                    ]), t_range=[-2.5, 2.5], color=HIGHLIGHT_COLOR, stroke_width=8
                )
                curve = VGroup(curve, curve2)

            # Apply offset to everything
            plane.shift(OFFSET_3D)
            curve.shift(OFFSET_3D)
            return plane, curve

        def get_graph_2d(name):
            if name == "Circle":
                # Parametric Circle
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(2.0*np.cos(t), 2.0*np.sin(t)),
                    t_range=[0, TAU], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"x^2 + y^2 = r^2", font_size=40)
                
            elif name == "Ellipse":
                # Parametric Ellipse
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(3.0*np.cos(t), 2.0*np.sin(t)),
                    t_range=[0, TAU], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1", font_size=40)
                
            elif name == "Parabola":
                # Parametric Parabola (y = 0.5x^2 - 1)
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(t, 0.5*t**2 - 1),
                    t_range=[-3, 3], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"y = ax^2 + bx + c", font_size=40)
                
            elif name == "Hyperbola":
                # Parametric Hyperbola (East-West)
                # x = a sec t, y = b tan t
                # a=1, b=0.8
                # Left Branch
                graph1 = ParametricFunction(
                    lambda t: axes_2d.c2p(-1.5 * np.cosh(t), 1.0 * np.sinh(t)),
                    t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                # Right Branch
                graph2 = ParametricFunction(
                    lambda t: axes_2d.c2p(1.5 * np.cosh(t), 1.0 * np.sinh(t)),
                    t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                graph = VGroup(graph1, graph2)
                equation = MathTex(r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1", font_size=40)
            
            # Note: graph is already mapped to axes coordinates via c2p
            # Center the equation below axes
            equation.next_to(axes_2d, DOWN, buff=0.5)
            # Add to fixed frame group
            return graph, equation

        # --- Sequencing ---
        
        current_3d_group = VGroup()
        current_2d_group = VGroup()
        
        conic_types = ["Circle", "Ellipse", "Parabola", "Hyperbola"]
        
        for conic_name in conic_types:
            # Prepare new objects
            plane, curve_3d = get_plane_and_curve_3d(conic_name)
            graph_2d, eq_2d = get_graph_2d(conic_name)
            
            new_3d = VGroup(plane, curve_3d)
            new_2d = VGroup(graph_2d, eq_2d)
            
            # Update Label
            new_label = Tex(conic_name, font_size=60, color=HIGHLIGHT_COLOR).to_edge(DOWN, buff=1.5)
            self.add_fixed_in_frame_mobjects(new_label) # Add temporarily to fade
            
            # Transition
            if len(current_3d_group) == 0:
                # First one
                self.play(
                    Create(plane),
                    Create(curve_3d),
                    Create(graph_2d),
                    Write(eq_2d),
                    Write(label),
                    run_time=1.5
                )
                self.play(Transform(label, new_label), run_time=0.5)
            else:
                # Morph / Fade swap
                self.play(
                    FadeOut(current_3d_group),
                    FadeIn(new_3d),
                    FadeOut(current_2d_group),
                    FadeIn(new_2d, shift=UP*0.2),
                    Transform(label, new_label),
                    run_time=1.5
                )
            
            self.remove(new_label) # Clean up temp
            current_3d_group = new_3d
            current_2d_group = new_2d
            
            self.wait(2.0)
            
        # End
        end_text = Tex("Geometry is Beautiful", font_size=50)
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(
            FadeOut(current_3d_group),
            FadeOut(current_2d_group),
            FadeOut(label),
            FadeOut(right_panel),
            FadeOut(cone),
            Write(end_text),
            run_time=2
        )
        self.wait(1)
