from manim import *

class DerivativeLimitDefinition(Scene):
    def construct(self):
        # Set up the scene with black background
        self.camera.background_color = BLACK
        
        # Define the function - a nice parabola
        def f(x):
            return 0.3 * x**2 + 0.2 * x + 1
        
        # Define the derivative function
        def f_prime(x):
            return 0.6 * x + 0.2
        
        # Set up axes within the safe zone (center third)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 3, 1],
            x_length=6,
            y_length=4.5,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=True,
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x").set_color(GREY_B)
        y_label = axes.get_y_axis_label("y").set_color(GREY_B)
        
        # Create the function graph
        graph = axes.plot(f, color=BLUE, stroke_width=3, x_range=[-2.5, 2.5])
        
        # Add title
        title = MathTex(
            "\\text{Limit Definition of the Derivative } f'(x)",
            font_size=32
        ).set_color(WHITE).to_edge(UP, buff=0.3)
        
        # Define points
        x_val = 1.0  # Fixed point (changed from c to x)
        h_initial = 1.2  # Initial h value (delta x)
        
        # Create points on the curve
        P1 = axes.coords_to_point(x_val, f(x_val))
        P2_initial = axes.coords_to_point(x_val + h_initial, f(x_val + h_initial))
        
        # Create dots
        dot_P1 = Dot(P1, color=ORANGE, radius=0.08)
        dot_P2 = Dot(P2_initial, color=RED, radius=0.08)
        
        # Create dashed vertical lines
        dash_P1 = DashedLine(
            axes.coords_to_point(x_val, 0),
            P1,
            color=GREY_A,
            stroke_width=2
        )
        dash_P2 = DashedLine(
            axes.coords_to_point(x_val + h_initial, 0),
            P2_initial,
            color=RED_A,
            stroke_width=2
        )
        
        # Create delta x and delta y lines to form a right triangle
        delta_x_line = Line(
            axes.coords_to_point(x_val, f(x_val)),
            axes.coords_to_point(x_val + h_initial, f(x_val)),
            color=ORANGE,
            stroke_width=3
        )
        delta_y_line = Line(
            axes.coords_to_point(x_val + h_initial, f(x_val)),
            axes.coords_to_point(x_val + h_initial, f(x_val + h_initial)),
            color=RED,
            stroke_width=3
        )
        
        # Create extended secant line
        line_extension = 0.8  # How far to extend the line
        secant_slope = (f(x_val + h_initial) - f(x_val)) / h_initial
        secant_line = Line(
            axes.coords_to_point(x_val - line_extension, f(x_val) - secant_slope * line_extension),
            axes.coords_to_point(x_val + h_initial + line_extension, f(x_val + h_initial) + secant_slope * line_extension),
            color=RED,
            stroke_width=3
        )
        
        # Create labels
        label_x = MathTex("x", font_size=24).set_color(ORANGE)
        label_x.next_to(axes.coords_to_point(x_val, 0), DOWN)
        
        label_x_h = MathTex("x+\\Delta x", font_size=20).set_color(RED)
        label_x_h.next_to(axes.coords_to_point(x_val + h_initial, 0), DOWN)
        
        label_f_x = MathTex("f(x)", font_size=20).set_color(ORANGE)
        label_f_x.next_to(P1, LEFT, buff=0.1)
        
        label_f_x_h = MathTex("f(x+\\Delta x)", font_size=20).set_color(RED)
        label_f_x_h.next_to(P2_initial, RIGHT, buff=0.1)
        
        label_func = MathTex("y = f(x)", font_size=20).set_color(BLUE)
        label_func.next_to(axes.coords_to_point(-1.5, f(-1.5)), UP + LEFT)
        
        label_delta_x = MathTex("\\Delta x", font_size=18).set_color(ORANGE)
        label_delta_x.next_to(delta_x_line, DOWN, buff=0.1)
        
        label_delta_y = MathTex("\\Delta y", font_size=18).set_color(RED)
        label_delta_y.next_to(delta_y_line, RIGHT, buff=0.1)
        
        # Create initial formula
        initial_formula = MathTex(
            "\\frac{f(x+\\Delta x)-f(x)}{\\Delta x}",
            font_size=28
        ).set_color(WHITE)
        initial_formula.to_edge(DOWN, buff=0.5)
        
        # ANIMATION SEQUENCE
        
        # Initial Setup (0-3s)
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.play(
            Create(graph),
            Write(title),
            Write(label_func),
            run_time=1.5
        )
        
        # Introducing the Secant Line (3-8s)
        self.play(
            Create(dot_P1),
            Create(dash_P1),
            Write(label_x),
            Write(label_f_x),
            run_time=1
        )
        
        self.play(
            Create(dot_P2),
            Create(dash_P2),
            Write(label_x_h),
            Write(label_f_x_h),
            run_time=1
        )
        
        self.play(
            Create(delta_x_line),
            Create(delta_y_line),
            Write(label_delta_x),
            Write(label_delta_y),
            run_time=1
        )
        
        self.play(
            Create(secant_line),
            Write(initial_formula),
            run_time=2
        )
        
        # The Limit Process (8-15s)
        # Create value tracker for h (delta x)
        h_tracker = ValueTracker(h_initial)
        
        # Make elements update with h
        dot_P2.add_updater(lambda m: m.move_to(
            axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val + h_tracker.get_value()))
        ))
        
        dash_P2.add_updater(lambda m: m.become(
            DashedLine(
                axes.coords_to_point(x_val + h_tracker.get_value(), 0),
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val + h_tracker.get_value())),
                color=RED_A,
                stroke_width=2
            )
        ))
        
        label_x_h.add_updater(lambda m: m.next_to(
            axes.coords_to_point(x_val + h_tracker.get_value(), 0), DOWN
        ))
        
        label_f_x_h.add_updater(lambda m: m.next_to(
            axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val + h_tracker.get_value())), 
            RIGHT, buff=0.1
        ))
        
        delta_x_line.add_updater(lambda m: m.become(
            Line(
                axes.coords_to_point(x_val, f(x_val)),
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val)),
                color=ORANGE,
                stroke_width=3
            )
        ))
        
        delta_y_line.add_updater(lambda m: m.become(
            Line(
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val)),
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val + h_tracker.get_value())),
                color=RED,
                stroke_width=3
            )
        ))
        
        label_delta_x.add_updater(lambda m: m.next_to(
            Line(
                axes.coords_to_point(x_val, f(x_val)),
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val))
            ), DOWN, buff=0.1
        ))
        
        label_delta_y.add_updater(lambda m: m.next_to(
            Line(
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val)),
                axes.coords_to_point(x_val + h_tracker.get_value(), f(x_val + h_tracker.get_value()))
            ), RIGHT, buff=0.1
        ))
        
        # Extended secant line updater
        def update_secant_line(line):
            h_val = h_tracker.get_value()
            if h_val > 0.01:  # Avoid division by very small numbers
                slope = (f(x_val + h_val) - f(x_val)) / h_val
                new_line = Line(
                    axes.coords_to_point(x_val - line_extension, f(x_val) - slope * line_extension),
                    axes.coords_to_point(x_val + h_val + line_extension, f(x_val + h_val) + slope * line_extension),
                    color=RED,
                    stroke_width=3
                )
                line.become(new_line)
        
        secant_line.add_updater(update_secant_line)
        
        # Animate h approaching 0
        self.play(
            h_tracker.animate.set_value(0.02),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=7
        )
        
        # The Derivative (15-20s)
        # Create extended tangent line
        tangent_slope = f_prime(x_val)
        tangent_extension = 1.2
        tangent_line = Line(
            axes.coords_to_point(x_val - tangent_extension, f(x_val) - tangent_slope * tangent_extension),
            axes.coords_to_point(x_val + tangent_extension, f(x_val) + tangent_slope * tangent_extension),
            color=GOLD,
            stroke_width=4
        )
        
        # Create final formula
        final_formula = MathTex(
            "\\lim_{\\Delta x \\to 0} \\frac{f(x+\\Delta x)-f(x)}{\\Delta x} = f'(x)",
            font_size=26
        ).set_color(PINK)
        final_formula.to_edge(DOWN, buff=0.5)
        
        # Transform secant to tangent
        self.play(
            ReplacementTransform(secant_line, tangent_line),
            ReplacementTransform(initial_formula, final_formula),
            FadeOut(delta_x_line),
            FadeOut(delta_y_line),
            FadeOut(label_delta_x),
            FadeOut(label_delta_y),
            FadeOut(dot_P2),
            FadeOut(dash_P2),
            FadeOut(label_x_h),
            FadeOut(label_f_x_h),
            run_time=3
        )
        
        # Highlight the derivative
        self.play(
            final_formula[-4:].animate.set_color(YELLOW).scale(1.2),
            run_time=2
        )
        
        # Clean Exit (20-22s)
        self.wait(2)
        
        # Final fadeout
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        
        self.wait(0.5)