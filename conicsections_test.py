from manim import *
import numpy as np


config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class ConicSectionsReel(ThreeDScene):
    def construct(self):
        
        self.camera.background_color = "#000510"  
        
        
        CONE_COLOR = BLUE_E
        PLANE_COLOR = TEAL_E
        HIGHLIGHT_COLOR = YELLOW
        TEXT_COLOR = WHITE
        
        
        
        
        OFFSET_3D = LEFT * 2.5
        OFFSET_2D = RIGHT * 2.1
        
        
        
        title = MathTex(
            r"\mathbb{C}\text{onic } \mathbb{S}\text{ections}",
            font_size=80
        )
        title.set_color_by_gradient(BLUE, RED)
        
        
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=1.5)
        
        
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=-90 * DEGREES, zoom=0.85)
        
        
        h = 3.5
        r = 3.0
        
        
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
        
        self.add(cone) 

        
        
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
        
        
        right_panel = VGroup(axes_2d)
        self.add_fixed_in_frame_mobjects(right_panel)
        
        
        label = Tex("", font_size=60, color=HIGHLIGHT_COLOR).to_edge(DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(label)
        
        
        
        def get_plane_and_curve_3d(name):
            """Returns (plane_surface, curve_3d_mobject) for the given conic type"""
            if name == "Circle":
                
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
                
                
                slope = 0.5
                intercept = 1.0
                plane = Surface(
                    lambda u, v: np.array([u, v, slope * v + intercept]),
                    u_range=[-3, 3], v_range=[-3, 3],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                
                
                curve = Ellipse(width=2.5, height=3.0, color=HIGHLIGHT_COLOR, stroke_width=8)
                curve.rotate(np.arctan(slope), RIGHT)
                curve.move_to(np.array([0, 0.6, 1.3])) 
                
            elif name == "Parabola":
                
                slope = h/r 
                intercept = 1.0
                plane = Surface(
                    lambda u, v: np.array([u, v, slope * v + intercept]),
                    u_range=[-3, 3], v_range=[-2.5, 2.5],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                
                curve = ParametricFunction(
                    lambda t: np.array([
                        t,
                        0.4 * t**2 - 0.5,
                        slope * (0.4 * t**2 - 0.5) + intercept
                    ]), t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=8
                )
                
            elif name == "Hyperbola":
                
                
                plane = Surface(
                    lambda u, v: np.array([1.2, u, v]), 
                    u_range=[-3, 3], v_range=[-3, 3],
                    fill_color=PLANE_COLOR, fill_opacity=0.2, stroke_width=0
                )
                
                
                
                
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

            
            plane.shift(OFFSET_3D)
            curve.shift(OFFSET_3D)
            return plane, curve

        def get_graph_2d(name):
            if name == "Circle":
                
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(2.0*np.cos(t), 2.0*np.sin(t)),
                    t_range=[0, TAU], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"x^2 + y^2 = r^2", font_size=40)
                
            elif name == "Ellipse":
                
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(3.0*np.cos(t), 2.0*np.sin(t)),
                    t_range=[0, TAU], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1", font_size=40)
                
            elif name == "Parabola":
                
                graph = ParametricFunction(
                    lambda t: axes_2d.c2p(t, 0.5*t**2 - 1),
                    t_range=[-3, 3], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                equation = MathTex(r"y = ax^2 + bx + c", font_size=40)
                
            elif name == "Hyperbola":
                
                
                
                
                graph1 = ParametricFunction(
                    lambda t: axes_2d.c2p(-1.5 * np.cosh(t), 1.0 * np.sinh(t)),
                    t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                
                graph2 = ParametricFunction(
                    lambda t: axes_2d.c2p(1.5 * np.cosh(t), 1.0 * np.sinh(t)),
                    t_range=[-2, 2], color=HIGHLIGHT_COLOR, stroke_width=6
                )
                graph = VGroup(graph1, graph2)
                equation = MathTex(r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1", font_size=40)
            
            
            
            equation.next_to(axes_2d, DOWN, buff=0.5)
            
            return graph, equation

        
        
        current_3d_group = VGroup()
        current_2d_group = VGroup()
        
        conic_types = ["Circle", "Ellipse", "Parabola", "Hyperbola"]
        
        for conic_name in conic_types:
            
            plane, curve_3d = get_plane_and_curve_3d(conic_name)
            graph_2d, eq_2d = get_graph_2d(conic_name)
            
            new_3d = VGroup(plane, curve_3d)
            new_2d = VGroup(graph_2d, eq_2d)
            
            
            new_label = Tex(conic_name, font_size=60, color=HIGHLIGHT_COLOR).to_edge(DOWN, buff=1.5)
            self.add_fixed_in_frame_mobjects(new_label) 
            
            
            if len(current_3d_group) == 0:
                
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
                
                self.play(
                    FadeOut(current_3d_group),
                    FadeIn(new_3d),
                    FadeOut(current_2d_group),
                    FadeIn(new_2d, shift=UP*0.2),
                    Transform(label, new_label),
                    run_time=1.5
                )
            
            self.remove(new_label) 
            current_3d_group = new_3d
            current_2d_group = new_2d
            
            self.wait(2.0)
            
        
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
