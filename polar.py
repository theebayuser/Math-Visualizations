from manim import *
import numpy as np

class PolarCoordinatesAnimation(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = BLACK
        
        # Define safe zone boundaries (6x6 centered at origin)
        SAFE_ZONE_SIZE = 6
        
        # Color palette
        AXES_COLOR = GREY_B
        POINT_COLOR = WHITE
        RADIUS_COLOR = BLUE_C
        ANGLE_COLOR = RED_C
        PROJECTION_COLOR = GREY_A
        X_COLOR = YELLOW_C
        Y_COLOR = TEAL_C
        CIRCLE_COLOR = GREEN_C
        SPIRAL_COLOR = PURPLE
        
        # Create coordinate system
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": AXES_COLOR, "stroke_width": 2},
            tips=False
        )
        
        # Add axis labels
        x_label = MathTex("x", color=X_COLOR).next_to(axes.x_axis.get_end(), DOWN)
        y_label = MathTex("y", color=Y_COLOR).next_to(axes.y_axis.get_end(), LEFT)
        
        # Introduction: Point on Cartesian Plane (0-7s)
        self.play(Create(axes), run_time=1.5)
        self.play(Write(x_label), Write(y_label), run_time=1)
        
        # Place point P at (2, 1.5)
        p_coords = np.array([2, 1.5, 0])
        point_p = Dot(axes.coords_to_point(2, 1.5), color=POINT_COLOR, radius=0.08)
        
        self.play(Create(point_p), run_time=1)
        
        # Create dashed projection lines
        x_proj_line = DashedLine(
            axes.coords_to_point(2, 0),
            axes.coords_to_point(2, 1.5),
            color=PROJECTION_COLOR,
            stroke_width=2
        )
        y_proj_line = DashedLine(
            axes.coords_to_point(0, 1.5),
            axes.coords_to_point(2, 1.5),
            color=PROJECTION_COLOR,
            stroke_width=2
        )
        
        # Labels for x and y coordinates
        x_coord_label = MathTex("x", color=X_COLOR).next_to(axes.coords_to_point(2, -0.3), DOWN)
        y_coord_label = MathTex("y", color=Y_COLOR).next_to(axes.coords_to_point(-0.3, 1.5), LEFT)
        
        self.play(
            Create(x_proj_line),
            Create(y_proj_line),
            Write(x_coord_label),
            Write(y_coord_label),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Display (x, y) notation
        cartesian_label = MathTex("(", "x", ",", "y", ")", color=WHITE)
        cartesian_label[1].set_color(X_COLOR)
        cartesian_label[3].set_color(Y_COLOR)
        cartesian_label.next_to(point_p, UR, buff=0.3)
        
        self.play(Write(cartesian_label), run_time=1.5)
        self.wait(0.5)
        
        # Transition to Polar Representation (7-15s)
        self.play(
            FadeOut(x_proj_line),
            FadeOut(y_proj_line),
            FadeOut(x_coord_label),
            FadeOut(y_coord_label),
            FadeOut(cartesian_label),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Create radius line
        radius_line = Line(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(2, 1.5),
            color=RADIUS_COLOR,
            stroke_width=4
        )
        radius_line.set_glow_opacity(0.8)
        
        # Create angle arc
        angle_arc = Arc(
            start_angle=0,
            angle=np.arctan(1.5/2),
            radius=0.8,
            color=ANGLE_COLOR,
            stroke_width=3
        )
        angle_arc.set_glow_opacity(0.8)
        
        # Labels for r and theta
        r_label = MathTex("r", color=RADIUS_COLOR).next_to(
            axes.coords_to_point(1, 0.75), UL, buff=0.1
        )
        theta_label = MathTex("\\theta", color=ANGLE_COLOR).next_to(
            axes.coords_to_point(1.2, 0.3), UR, buff=0.1
        )
        
        self.play(
            Create(radius_line),
            Create(angle_arc),
            Write(r_label),
            Write(theta_label),
            run_time=2.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Display (r, θ) notation
        polar_label = MathTex("(", "r", ",", "\\theta", ")", color=WHITE)
        polar_label[1].set_color(RADIUS_COLOR)
        polar_label[3].set_color(ANGLE_COLOR)
        polar_label.next_to(point_p, UR, buff=0.3)
        
        self.play(Write(polar_label), run_time=1.5)
        self.wait(1)
        
        # Conversion (Polar to Cartesian) - Visual & Notational (15-22s)
        # Bring back projection lines
        self.play(
            Create(x_proj_line),
            Create(y_proj_line),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Create right triangle
        triangle = Polygon(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(2, 0),
            axes.coords_to_point(2, 1.5),
            color=PROJECTION_COLOR,
            stroke_width=2,
            fill_opacity=0.1
        )
        
        self.play(Create(triangle), run_time=1)
        
        # Display conversion formulas
        x_formula = MathTex("x", "=", "r", "\\cos", "(", "\\theta", ")", color=WHITE)
        y_formula = MathTex("y", "=", "r", "\\sin", "(", "\\theta", ")", color=WHITE)
        x_formula[2].set_color(RADIUS_COLOR)
        x_formula[5].set_color(ANGLE_COLOR)
        y_formula[2].set_color(RADIUS_COLOR)
        y_formula[5].set_color(ANGLE_COLOR)
        
        formulas = VGroup(x_formula, y_formula).arrange(DOWN, buff=0.3)
        formulas.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        
        self.play(Write(x_formula), run_time=1.5)
        self.play(Write(y_formula), run_time=1.5)
        self.wait(1)
        
        # Plotting Points: Dynamic Example (22-30s)
        self.play(
            FadeOut(polar_label),
            FadeOut(x_proj_line),
            FadeOut(y_proj_line),
            FadeOut(triangle),
            FadeOut(r_label),
            FadeOut(theta_label),
            FadeOut(x_formula),
            FadeOut(y_formula),
            run_time=1.5
        )
        
        # Remove the original point
        self.play(FadeOut(point_p), FadeOut(radius_line), FadeOut(angle_arc), run_time=1)
        
        # Create rotating radar arm
        radar_length = 2.5
        radar_angle = ValueTracker(0)
        
        def get_radar_line():
            angle = radar_angle.get_value()
            end_point = axes.coords_to_point(
                radar_length * np.cos(angle),
                radar_length * np.sin(angle)
            )
            return Line(
                axes.coords_to_point(0, 0),
                end_point,
                color=RADIUS_COLOR,
                stroke_width=4
            ).set_glow_opacity(0.8)
        
        def get_radar_dot():
            angle = radar_angle.get_value()
            return Dot(
                axes.coords_to_point(
                    radar_length * np.cos(angle),
                    radar_length * np.sin(angle)
                ),
                color=POINT_COLOR,
                radius=0.06
            )
        
        radar_line = always_redraw(get_radar_line)
        radar_dot = always_redraw(get_radar_dot)
        
        self.add(radar_line, radar_dot)
        
        # Rotate to 60 degrees
        target_angle = 60 * DEGREES
        
        self.play(
            radar_angle.animate.set_value(target_angle),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Display example polar coordinates
        example_label = MathTex("(2.5, 60°)", color=WHITE)
        example_label.next_to(radar_dot.get_center(), UR, buff=0.3)
        self.play(Write(example_label), run_time=1)
        self.wait(1)
        
        # Plotting Curves: Circle & Spiral (30-40s)
        self.play(FadeOut(example_label), run_time=0.5)
        
        # Circle: r = constant
        circle_radius = 2
        circle_path = TracedPath(
            lambda: axes.coords_to_point(
                circle_radius * np.cos(radar_angle.get_value()),
                circle_radius * np.sin(radar_angle.get_value())
            ),
            stroke_color=CIRCLE_COLOR,
            stroke_width=3
        ).set_glow_opacity(0.8)
        
        self.add(circle_path)
        
        # Update radar for circle
        def get_circle_radar():
            angle = radar_angle.get_value()
            end_point = axes.coords_to_point(
                circle_radius * np.cos(angle),
                circle_radius * np.sin(angle)
            )
            return Line(
                axes.coords_to_point(0, 0),
                end_point,
                color=RADIUS_COLOR,
                stroke_width=4
            ).set_glow_opacity(0.8)
        
        def get_circle_dot():
            angle = radar_angle.get_value()
            return Dot(
                axes.coords_to_point(
                    circle_radius * np.cos(angle),
                    circle_radius * np.sin(angle)
                ),
                color=POINT_COLOR,
                radius=0.06
            )
        
        radar_line.become(always_redraw(get_circle_radar))
        radar_dot.become(always_redraw(get_circle_dot))
        
        # Rotate full circle
        self.play(
            radar_angle.animate.set_value(target_angle + 2 * PI),
            run_time=3,
            rate_func=rate_functions.linear
        )
        
        # Label circle equation
        circle_equation = MathTex("r = c", color=CIRCLE_COLOR).to_edge(RIGHT, buff=1).shift(UP * 1.5)
        self.play(Write(circle_equation), run_time=1)
        self.wait(1)
        
        # Clear circle and create spiral
        self.play(
            FadeOut(circle_path),
            FadeOut(circle_equation),
            run_time=1
        )
        
        # Reset angle
        radar_angle.set_value(0)
        
        # Spiral: r = 0.3 * θ
        spiral_path = TracedPath(
            lambda: axes.coords_to_point(
                0.3 * radar_angle.get_value() * np.cos(radar_angle.get_value()),
                0.3 * radar_angle.get_value() * np.sin(radar_angle.get_value())
            ),
            stroke_color=SPIRAL_COLOR,
            stroke_width=3
        ).set_glow_opacity(0.8)
        
        self.add(spiral_path)
        
        # Update radar for spiral
        def get_spiral_radar():
            angle = radar_angle.get_value()
            radius = 0.3 * angle
            end_point = axes.coords_to_point(
                radius * np.cos(angle),
                radius * np.sin(angle)
            )
            return Line(
                axes.coords_to_point(0, 0),
                end_point,
                color=RADIUS_COLOR,
                stroke_width=4
            ).set_glow_opacity(0.8)
        
        def get_spiral_dot():
            angle = radar_angle.get_value()
            radius = 0.3 * angle
            return Dot(
                axes.coords_to_point(
                    radius * np.cos(angle),
                    radius * np.sin(angle)
                ),
                color=POINT_COLOR,
                radius=0.06
            )
        
        radar_line.become(always_redraw(get_spiral_radar))
        radar_dot.become(always_redraw(get_spiral_dot))
        
        # Create spiral
        self.play(
            radar_angle.animate.set_value(6 * PI),
            run_time=4,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Label spiral equation
        spiral_equation = MathTex("r = \\theta", color=SPIRAL_COLOR).to_edge(RIGHT, buff=1).shift(UP * 1.5)
        self.play(Write(spiral_equation), run_time=1)
        self.wait(1)
        
        # Conclusion & Final Thought (40-45s)
        self.play(
            FadeOut(spiral_path),
            FadeOut(spiral_equation),
            FadeOut(radar_line),
            FadeOut(radar_dot),
            run_time=1.5
        )
        
        # Final message
        final_text = Text("Polar Coordinates: Angle and Distance", color=WHITE, font_size=36)
        final_text.move_to(ORIGIN)
        
        self.play(Write(final_text), run_time=2)
        self.wait(1.5)
        
        # Fade out all elements
        self.play(
            FadeOut(final_text),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        self.wait(0.5)