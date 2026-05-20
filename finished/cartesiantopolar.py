from manim import *
import numpy as np

class CartesianToPolarBend(Scene):
    def construct(self):
        # Constants for consistent spacing and sizing - shrunk overall
        SCALE = 0.6  # Reduced from 0.7 for more compact visualization
        GRID_OPACITY = 0.6
        MAIN_AXIS_WIDTH = 2.5  # Slightly thinner
        GRID_LINE_WIDTH = 0.8  # Slightly thinner
        CURVE_WIDTH = 3.5  # Slightly thinner
        
        # Coordinate system bounds - expanded to fit the function better
        X_MIN, X_MAX = -4, 4
        Y_MIN, Y_MAX = -3.5, 3.5
        GRID_SPACING = 0.5
        
        # Vertical spacing adjustments - moved coordinate system to bottom
        TITLE_Y = 3.8  # Moved higher
        FUNC_LABEL_Y = 2.9  # Moved down further from title
        DOMAIN_LABEL_Y = 2  # For domain information - moved down further
        GRID_CENTER_Y = -1.2  # Moved grid even lower
        
        # Title - larger and more prominent, starts in center
        title = MathTex("\\text{Cartesian to Polar Transformation}", font_size=38)
        title.set_color_by_gradient(BLUE, RED)
        title.move_to(ORIGIN)  # Start in center
        
        # Function: y = sin(6x) + 2
        def cartesian_func(x):
            return np.sin(6 * x) + 2
        
        def create_cartesian_grid():
            """Create a clean, evenly spaced Cartesian grid"""
            grid = VGroup()
            
            # Vertical grid lines
            for x in np.arange(X_MIN, X_MAX + GRID_SPACING, GRID_SPACING):
                if abs(x) < 0.01:  # Skip x = 0 (main axis)
                    continue
                line = Line(
                    start=[x * SCALE, (Y_MIN * SCALE) + GRID_CENTER_Y, 0],
                    end=[x * SCALE, (Y_MAX * SCALE) + GRID_CENTER_Y, 0],
                    stroke_color=GRAY,
                    stroke_width=GRID_LINE_WIDTH,
                    stroke_opacity=GRID_OPACITY
                )
                grid.add(line)
            
            # Horizontal grid lines
            for y in np.arange(Y_MIN, Y_MAX + GRID_SPACING, GRID_SPACING):
                if abs(y) < 0.01:  # Skip y = 0 (main axis)
                    continue
                line = Line(
                    start=[X_MIN * SCALE, (y * SCALE) + GRID_CENTER_Y, 0],
                    end=[X_MAX * SCALE, (y * SCALE) + GRID_CENTER_Y, 0],
                    stroke_color=GRAY,
                    stroke_width=GRID_LINE_WIDTH,
                    stroke_opacity=GRID_OPACITY
                )
                grid.add(line)
            
            # Main axes - centered and properly sized
            x_axis = Line(
                [X_MIN * SCALE, GRID_CENTER_Y, 0], 
                [X_MAX * SCALE, GRID_CENTER_Y, 0], 
                stroke_color=WHITE, 
                stroke_width=MAIN_AXIS_WIDTH
            )
            y_axis = Line(
                [0, (Y_MIN * SCALE) + GRID_CENTER_Y, 0], 
                [0, (Y_MAX * SCALE) + GRID_CENTER_Y, 0], 
                stroke_color=WHITE, 
                stroke_width=MAIN_AXIS_WIDTH
            )
            grid.add(x_axis, y_axis)
            
            # Axis tick marks - evenly spaced
            for x in range(int(X_MIN), int(X_MAX) + 1):
                if x == 0:
                    continue
                tick = Line(
                    [x * SCALE, (-0.1 * SCALE) + GRID_CENTER_Y, 0],
                    [x * SCALE, (0.1 * SCALE) + GRID_CENTER_Y, 0],
                    stroke_color=WHITE,
                    stroke_width=2
                )
                grid.add(tick)
            
            for y in range(int(Y_MIN), int(Y_MAX) + 1):
                if y == 0:
                    continue
                tick = Line(
                    [(-0.1 * SCALE), (y * SCALE) + GRID_CENTER_Y, 0],
                    [(0.1 * SCALE), (y * SCALE) + GRID_CENTER_Y, 0],
                    stroke_color=WHITE,
                    stroke_width=2
                )
                grid.add(tick)
            
            return grid
        
        def create_cartesian_labels():
            """Create properly positioned and sized labels"""
            x_label = MathTex("x", font_size=32).move_to([X_MAX * SCALE + 0.25, GRID_CENTER_Y - 0.25, 0])
            y_label = MathTex("y", font_size=32).move_to([-0.25, (Y_MAX * SCALE) + GRID_CENTER_Y + 0.25, 0])
            
            return VGroup(x_label, y_label)
        
        def create_cartesian_curve():
            """Create the original function curve"""
            curve = ParametricFunction(
                lambda t: np.array([t * SCALE, (cartesian_func(t) * SCALE) + GRID_CENTER_Y, 0]),
                t_range=[-PI, PI, 0.01],
                stroke_color=RED,
                stroke_width=CURVE_WIDTH
            )
            return curve
        
        def create_diagonal_line():
            """Create y = x reference line with smaller arrowheads on both ends"""
            line_range = min(abs(X_MIN), abs(Y_MIN), X_MAX, Y_MAX) * 1
            
            # Create a double arrow with smaller tips
            diagonal = DoubleArrow(
                start=[(-line_range * SCALE), (-line_range * SCALE) + GRID_CENTER_Y, 0],
                end=[(line_range * SCALE), (line_range * SCALE) + GRID_CENTER_Y, 0],
                stroke_color=BLUE,
                stroke_width=2,
                stroke_opacity=0.8,
                buff=0,
                max_tip_length_to_length_ratio=0.03  # Made smaller (was 0.05)
            )
            label = MathTex("y = x", font_size=24, color=BLUE)
            label.next_to(diagonal, UR, buff=0.1)
            return VGroup(diagonal, label)
        
        def create_reflected_curve():
            """Create the reflected curve (x and y swapped)"""
            curve = ParametricFunction(
                lambda t: np.array([(cartesian_func(t) * SCALE), (t * SCALE) + GRID_CENTER_Y, 0]),
                t_range=[-PI, PI, 0.01],
                stroke_color=RED,
                stroke_width=CURVE_WIDTH
            )
            return curve
        
        def polar_transform_point(point, t):
            """Transform point from Cartesian to polar coordinates"""
            if t == 0:
                return point
            
            x, y, z = point
            x_calc = x / SCALE
            y_calc = (y - GRID_CENTER_Y) / SCALE
            
            # x-coordinate becomes radius, y-coordinate becomes angle
            r = x_calc
            theta = y_calc
            
            # Handle negative radii
            if r < 0:
                r = abs(r)
                theta += PI
            
            # Convert to Cartesian for display
            if abs(r) < 0.001:
                polar_x = polar_y = 0
            else:
                polar_x = r * np.cos(theta) * SCALE
                polar_y = (r * np.sin(theta) * SCALE) + GRID_CENTER_Y
            
            # Smooth interpolation
            ease_t = smooth(t)
            final_x = (1 - ease_t) * x + ease_t * polar_x
            final_y = (1 - ease_t) * y + ease_t * polar_y
            
            return [final_x, final_y, z]
        
        def create_transformed_curve(t):
            """Create curve at transformation parameter t"""
            points = []
            param_vals = np.linspace(-PI, PI, 500)
            
            for param in param_vals:
                x_orig = param
                y_orig = cartesian_func(param)
                x_refl = y_orig * SCALE
                y_refl = (x_orig * SCALE) + GRID_CENTER_Y
                
                transformed_point = polar_transform_point([x_refl, y_refl, 0], t)
                points.append(transformed_point)
            
            curve = VMobject()
            curve.set_points_smoothly(points)
            curve.set_stroke(RED, width=CURVE_WIDTH)
            return curve
        
        def create_transformed_grid(t):
            """Create grid at transformation parameter t with seamless axis transitions"""
            grid = VGroup()
            MAX_RADIUS = 4.0  # Increased to match expanded bounds
            
            # Concentric circles (from vertical lines) - expanded range
            for r in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
                circle_points = []
                theta_vals = np.linspace(0, 2*PI, 150)
                
                for theta in theta_vals:
                    y_val = theta - PI
                    original_point = [r * SCALE, (y_val * SCALE) + GRID_CENTER_Y, 0]
                    transformed_point = polar_transform_point(original_point, t)
                    circle_points.append(transformed_point)
                
                circle_points.append(circle_points[0])  # Close the circle
                
                line = VMobject()
                line.set_points_smoothly(circle_points)
                line.set_stroke(GRAY, width=GRID_LINE_WIDTH, opacity=GRID_OPACITY)
                grid.add(line)
            
            # Radial lines (from horizontal lines)
            num_radial_lines = 12
            for i in range(num_radial_lines):
                angle = 2 * PI * i / num_radial_lines
                y_val = angle - PI
                
                radial_points = []
                r_vals = np.linspace(-MAX_RADIUS, MAX_RADIUS, 150)
                
                for r_val in r_vals:
                    original_point = [r_val * SCALE, (y_val * SCALE) + GRID_CENTER_Y, 0]
                    transformed_point = polar_transform_point(original_point, t)
                    radial_points.append(transformed_point)
                
                line = VMobject()
                line.set_points_smoothly(radial_points)
                line.set_stroke(GRAY, width=GRID_LINE_WIDTH, opacity=GRID_OPACITY)
                grid.add(line)
            
            # Seamless X-axis transition (becomes radial line at θ=0)
            x_axis_points = []
            r_vals = np.linspace(-MAX_RADIUS, MAX_RADIUS, 100)
            for r_val in r_vals:
                original_point = [r_val * SCALE, GRID_CENTER_Y, 0]
                transformed_point = polar_transform_point(original_point, t)
                x_axis_points.append(transformed_point)
            
            x_axis = VMobject()
            x_axis.set_points_smoothly(x_axis_points)
            # Fade out x-axis gradually as it becomes less significant
            x_axis_opacity = max(0.3, 1 - 0.7 * t)  # Fade from 1 to 0.3
            x_axis.set_stroke(WHITE, width=MAIN_AXIS_WIDTH, opacity=x_axis_opacity)
            grid.add(x_axis)
            
            # Seamless Y-axis transition with smooth fading
            y_axis_points = []
            y_vals = np.linspace(Y_MIN, Y_MAX, 100)
            for y_val in y_vals:
                original_point = [0, (y_val * SCALE) + GRID_CENTER_Y, 0]
                transformed_point = polar_transform_point(original_point, t)
                y_axis_points.append(transformed_point)
            
            y_axis = VMobject()
            y_axis.set_points_smoothly(y_axis_points)
            # Y-axis fades out completely as it converges to origin
            y_axis_opacity = max(0, 1 - 1.5 * t)  # Fade out faster than x-axis
            y_axis.set_stroke(WHITE, width=MAIN_AXIS_WIDTH, opacity=y_axis_opacity)
            grid.add(y_axis)
            
            # Origin circle appears gradually as y-axis fades
            if t > 0.2:  # Start appearing earlier for smoother transition
                origin_circle = Circle(
                    radius=0.05 + 0.03 * smooth(t),  # Slightly grow as it appears
                    color=WHITE, 
                    stroke_width=MAIN_AXIS_WIDTH
                ).move_to([0, GRID_CENTER_Y, 0])
                # Fade in origin circle as y-axis fades out
                circle_opacity = min(1, 2 * (t - 0.2))  # Start at t=0.2, full opacity at t=0.7
                origin_circle.set_stroke(opacity=circle_opacity)
                grid.add(origin_circle)
            
            return grid
        
        # Create all elements with updated positioning
        cartesian_grid = create_cartesian_grid()
        cartesian_labels = create_cartesian_labels()
        origin_dot = Dot([0, GRID_CENTER_Y, 0], color=RED, radius=0.05)  # Slightly smaller
        cartesian_graph = create_cartesian_curve()
        
        # Function label tracker that will change throughout animation - positioned with more space
        func_label = MathTex("y = \\sin(6x) + 2", font_size=24)  # Smaller font
        func_label.set_color(RED)
        func_label.move_to([0, FUNC_LABEL_Y, 0])  # Better vertical spacing
        
        # Domain labels that will update with the transformation
        domain_label = MathTex("x \\in [-\\pi, \\pi], \\quad y \\in [1, 3]", font_size=20)
        domain_label.set_color(YELLOW)
        domain_label.move_to([0, DOMAIN_LABEL_Y, 0])
        
        diagonal_elements = create_diagonal_line()
        reflected_graph = create_reflected_curve()
        
        # Animation sequence with consistent timing
        # Title starts in center, then moves up and gets smaller
        self.play(Write(title), run_time=1)
        self.wait(0.3)
        # Create smaller version of title with better spacing
        title_small = MathTex("\\text{Cartesian to Polar Transformation}", font_size=30)
        title_small.set_color_by_gradient(BLUE, RED)
        title_small.move_to([0, TITLE_Y, 0])  # Better positioned
        self.play(Transform(title, title_small), run_time=1)
        self.wait(0.3)
        
        # Show Cartesian setup
        self.play(
            Create(cartesian_grid),
            Write(cartesian_labels),
            Create(origin_dot),
            run_time=3
        )
        self.wait(0.5)
        
        # Plot original function
        self.play(Create(cartesian_graph), run_time=2.5)
        
        # Show function equation above the curve
        self.play(Write(func_label), run_time=1)
        
        # Show domain information
        self.play(Write(domain_label), run_time=1)
        self.wait(0.5)
        
        # Show y=x line
        self.play(Create(diagonal_elements), run_time=1)
        self.wait(0.5)
        
        # Reflect over y=x line and update equation
        new_func_label = MathTex("x = \\sin(6y) + 2", font_size=24)
        new_func_label.set_color(RED)
        new_func_label.move_to([0, FUNC_LABEL_Y, 0])  # Same position
        
        new_domain_label = MathTex("y \\in [-\\pi, \\pi], \\quad x \\in [1, 3]", font_size=20)
        new_domain_label.set_color(YELLOW)
        new_domain_label.move_to([0, DOMAIN_LABEL_Y, 0])
        
        self.play(
            Transform(cartesian_graph, reflected_graph),
            Transform(func_label, new_func_label),
            Transform(domain_label, new_domain_label),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # Remove diagonal line (no longer needed)
        self.play(FadeOut(diagonal_elements), run_time=0.75)
        self.wait(0.25)
        
        # Clean transition: fade out static labels and origin dot that won't transform
        self.play(
            FadeOut(cartesian_labels),
            FadeOut(origin_dot),
            run_time=0.75
        )
        self.wait(0.5)
        
        # Set up transformation with updaters
        t_tracker = ValueTracker(0)
        
        def update_curve(mob):
            t = t_tracker.get_value()
            new_curve = create_transformed_curve(t)
            mob.become(new_curve)
        
        def update_grid(mob):
            t = t_tracker.get_value()
            new_grid = create_transformed_grid(t)
            mob.become(new_grid)
        
        # Apply updaters to existing objects (no fade out/in needed)
        cartesian_graph.add_updater(update_curve)
        cartesian_grid.add_updater(update_grid)
        
        # Create polar equation and domain that will appear after transformation
        polar_func_label = MathTex("r(\\theta) = \\sin(6\\theta) + 2", font_size=24)
        polar_func_label.set_color(RED)
        polar_func_label.move_to([0, FUNC_LABEL_Y, 0])  # Same position
        
        # Changed domain to [0, 2π] instead of [-π, π]
        polar_domain_label = MathTex("\\theta \\in [0, 2\\pi], \\quad r \\in [1, 3]", font_size=20)
        polar_domain_label.set_color(YELLOW)
        polar_domain_label.move_to([0, DOMAIN_LABEL_Y, 0])
        
        # SEPARATE TIMING: Transform equations quickly (2 seconds) then continue coordinate transformation
        # First, transform the equations and domain quickly
        self.play(
            Transform(func_label, polar_func_label),
            Transform(domain_label, polar_domain_label),
            run_time=1,  # Fast equation transformation
            rate_func=smooth
        )
        
        # Now continue with the coordinate system transformation for the remaining 6 seconds
        self.play(
            t_tracker.animate.set_value(1),
            run_time=4,  # Remaining time for coordinate transformation
            rate_func=linear  # Linear progression for consistent bending speed
        )
        
        # Clean up updaters
        cartesian_graph.clear_updaters()
        cartesian_grid.clear_updaters()
        
        self.wait(0.5)
        
        # Highlight final result with subtle pulse
        self.play(
            cartesian_graph.animate.set_stroke(width=CURVE_WIDTH + 1),
            run_time=0.5
        )
        self.play(
            cartesian_graph.animate.set_stroke(width=CURVE_WIDTH),
            run_time=0.5
        )
        
        self.wait(2)
        
        # Fade everything out at the end
        self.play(
            FadeOut(title),
            FadeOut(func_label),
            FadeOut(domain_label),
            FadeOut(cartesian_grid),
            FadeOut(cartesian_graph),
            run_time=2
        )
        
        self.wait(1)