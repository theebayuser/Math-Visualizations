from manim import *
import numpy as np

# A cool, modern color scheme
SIN_COLOR = BLUE_D
COS_COLOR = TEAL_D
SUM_COLOR = GOLD_D
BACKGROUND_COLOR = BLACK
AXES_COLOR = WHITE

class PythagoreanTrigIdentity(MovingCameraScene):
    def construct(self):
        # Set background and create a value tracker for x
        self.camera.background_color = BACKGROUND_COLOR
        x_tracker = ValueTracker(0)
        
        # --- 1. Title ---
        title = Text("The Pythagorean Identity", font_size=34).set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.2)
        
        # --- 2. Compact Axes with Extended Range for Arrow Tips ---
        axes = Axes(
            x_range=[0, 4.5 * PI, PI],  # Extended x-range to place tips beyond last tick
            y_range=[-1.4, 1.4, 0.5],   # Extended y-range to place tips beyond ticks
            x_length=4.5,
            y_length=1.8,
            axis_config={
                "color": AXES_COLOR, 
                "stroke_width": 2,
                "include_tip": True
            },
            x_axis_config={
                "numbers_to_include": [],
                "tip_length": 0.15,
                "tip_width": 0.15
            }, 
            y_axis_config={
                "numbers_to_exclude": [0],
                "tip_length": 0.15,
                "tip_width": 0.15
            },
        )
        
        # Scale down the arrow tips for better proportions
        axes.x_axis.tip.scale(0.6)
        axes.y_axis.tip.scale(0.6)
        
        axes.shift(UP * 0.1)  # Positioned slightly lower to make room for labels

        # X-axis labels (only for visible tick marks)
        x_labels = VGroup()
        for i in range(1, 5):
            val = i * PI
            label_text = f"{i}\\pi" if i > 1 else "\\pi"
            label = MathTex(label_text, font_size=18).next_to(axes.c2p(val, 0), DOWN, buff=0.1)
            x_labels.add(label)
        
        # Y-axis labels
        y_labels = VGroup()
        for val in [-1, 0.5, 1.0]:
            if val != 0:
                label = MathTex(f"{val}" if val != 0.5 else "0.5", font_size=18).next_to(axes.c2p(0, val), LEFT, buff=0.1)
                y_labels.add(label)
        
        self.play(GrowFromCenter(title))
        self.play(Create(axes), Write(x_labels), Write(y_labels), run_time=2)

        # --- 3. Initial Graphs (sin and cos) ---
        sin_graph = axes.plot(
            lambda x: np.sin(x), 
            x_range=[0, 4*PI], 
            color=SIN_COLOR,
            stroke_width=3
        )
        
        cos_graph = axes.plot(
            lambda x: np.cos(x), 
            x_range=[0, 4*PI], 
            color=COS_COLOR,
            stroke_width=3
        )
        
        # Labels positioned between title and graph - CENTERED
        sin_label_initial = MathTex("\\sin(x)", color=SIN_COLOR, font_size=35)
        cos_label_initial = MathTex("\\cos(x)", color=COS_COLOR, font_size=35)
        
        # Position labels centered between title and graph
        label_y_position = title.get_bottom()[1] - 1.5  # Below title
        axes_center_x = axes.get_center()[0]  # Get the center x-coordinate of the axes
        
        sin_label_initial.move_to([axes_center_x - 1.0, label_y_position, 0])
        cos_label_initial.move_to([axes_center_x + 1.0, label_y_position, 0])
        
        # Show initial sin and cos graphs
        self.play(
            Create(sin_graph),
            Create(cos_graph),
            Write(sin_label_initial),
            Write(cos_label_initial),
            run_time=2
        )
        
        self.wait(0.5)

        # --- 4. Transform to Squared Versions ---
        
        # Create squared versions
        sin_sq_graph = axes.plot(
            lambda x: np.sin(x)**2, 
            x_range=[0, 4*PI], 
            color=SIN_COLOR,
            stroke_width=3
        )
        
        cos_sq_graph = axes.plot(
            lambda x: np.cos(x)**2, 
            x_range=[0, 4*PI], 
            color=COS_COLOR,
            stroke_width=3
        )
        
        # New labels for squared versions (same centered position)
        sin_label_sq = MathTex("\\sin^2(x)", color=SIN_COLOR, font_size=35)
        cos_label_sq = MathTex("\\cos^2(x)", color=COS_COLOR, font_size=35)
        
        sin_label_sq.move_to([axes_center_x - 1.0, label_y_position, 0])
        cos_label_sq.move_to([axes_center_x + 1.0, label_y_position, 0])
        
        # Transform graphs and labels
        self.play(
            Transform(sin_graph, sin_sq_graph),
            Transform(cos_graph, cos_sq_graph),
            Transform(sin_label_initial, sin_label_sq),
            Transform(cos_label_initial, cos_label_sq),
            run_time=2
        )
        
        self.wait(0.5)

        # --- 5. Pythagorean Identity Display ---
        identity_eq = MathTex(
            "\\sin^2(\\theta) + \\cos^2(\\theta) = 1",
            font_size=40
        )
        identity_eq.shift(DOWN * 1.4)  # Adjusted for smaller graph
        
        identity_eq[0][0:6].set_color(SIN_COLOR)  # sin^2(θ)
        identity_eq[0][7:13].set_color(COS_COLOR)  # cos^2(θ)
        identity_eq[0][14].set_color(SUM_COLOR)   # 1

        self.play(Write(identity_eq), run_time=1.5)

        # --- 6. Live Counter (Fixed Positioning) ---
        # Create positioned decimal numbers
        sin_val = DecimalNumber(
            0,
            num_decimal_places=3,
            color=SIN_COLOR,
            font_size=30
        )
        
        cos_val = DecimalNumber(
            0,
            num_decimal_places=3,
            color=COS_COLOR,
            font_size=30
        )
        
        sum_val = DecimalNumber(
            1,
            num_decimal_places=3,
            color=SUM_COLOR,
            font_size=30
        )

        # Static symbols
        plus_live = MathTex("+", font_size=30)
        equals_live = MathTex("=", font_size=30)
        
        # Create and position the live equation
        live_equation = VGroup(sin_val, plus_live, cos_val, equals_live, sum_val)
        live_equation.arrange(RIGHT, buff=0.3)
        live_equation.shift(DOWN * 2.4)  # Adjusted for smaller graph
        
        # Add updaters to the decimal numbers
        sin_val.add_updater(lambda m: m.set_value(np.sin(x_tracker.get_value())**2))
        cos_val.add_updater(lambda m: m.set_value(np.cos(x_tracker.get_value())**2))
        sum_val.add_updater(lambda m: m.set_value(np.sin(x_tracker.get_value())**2 + np.cos(x_tracker.get_value())**2))
        
        self.add(live_equation)

        # --- 7. Unit Circle Setup (initially hidden) ---
        circle_center = np.array([axes_center_x, label_y_position, 0])  # Same position as the labels
        
        # Unit circle
        unit_circle = Circle(radius=0.8, color=WHITE, stroke_width=2)
        unit_circle.move_to(circle_center)
        
        # Circle axes (x and y)
        circle_x_axis = Line(
            start=circle_center + LEFT * 0.9,
            end=circle_center + RIGHT * 0.9,
            color=AXES_COLOR,
            stroke_width=1
        )
        circle_y_axis = Line(
            start=circle_center + DOWN * 0.9,
            end=circle_center + UP * 0.9,
            color=AXES_COLOR,
            stroke_width=1
        )
        
        # Dynamic elements that depend on x_tracker
        radius_line = always_redraw(lambda: Line(
            start=circle_center,
            end=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), np.sin(x_tracker.get_value()), 0]),
            color=WHITE,
            stroke_width=2
        ))
        
        # Point on circle
        circle_dot = always_redraw(lambda: Dot(
            point=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), np.sin(x_tracker.get_value()), 0]),
            color=WHITE,
            radius=0.04
        ))
        
        # Right triangle components
        cos_line = always_redraw(lambda: Line(
            start=circle_center,
            end=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), 0, 0]),
            color=COS_COLOR,
            stroke_width=3
        ))
        
        sin_line = always_redraw(lambda: Line(
            start=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), 0, 0]),
            end=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), np.sin(x_tracker.get_value()), 0]),
            color=SIN_COLOR,
            stroke_width=3
        ))
        
        # Revolutionary Right Angle Symbol - Vector-based positioning
        right_angle_symbol = always_redraw(lambda: self.create_perfect_right_angle_symbol(
            circle_center,
            x_tracker.get_value(),
            size=0.08
        ))
        
        # Small labels for cos and sin on the circle
        cos_circle_label = always_redraw(lambda: MathTex(
            "\\cos", 
            color=COS_COLOR, 
            font_size=20
        ).next_to(
            circle_center + 0.4 * np.array([np.cos(x_tracker.get_value()), 0, 0]), 
            DOWN, 
            buff=0.1
        ))
        
        sin_circle_label = always_redraw(lambda: MathTex(
            "\\sin", 
            color=SIN_COLOR, 
            font_size=20
        ).next_to(
            circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), 0.5 * np.sin(x_tracker.get_value()), 0]), 
            RIGHT if np.sin(x_tracker.get_value()) > 0 else LEFT, 
            buff=0.1
        ))
        
        # Fixed angle arc - properly positioned at circle center
        angle_arc = always_redraw(lambda: Arc(
            start_angle=0,
            angle=x_tracker.get_value() % (2*PI),
            radius=0.3,
            color=RED,
            stroke_width=2,
            arc_center=circle_center
        ))

        # --- 8. Dynamic Tracking Elements ---
        dot_sin = always_redraw(lambda: Dot(
            point=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            color=SIN_COLOR,
            radius=0.05  # Slightly smaller for compact graph
        ))
        
        dot_cos = always_redraw(lambda: Dot(
            point=axes.c2p(x_tracker.get_value(), np.cos(x_tracker.get_value())**2),
            color=COS_COLOR,
            radius=0.05  # Slightly smaller for compact graph
        ))
        
        bar_sin = always_redraw(lambda: Line(
            start=axes.c2p(x_tracker.get_value(), 0),
            end=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            stroke_width=4,  # Reduced for compact graph
            color=SIN_COLOR,
            stroke_opacity=0.7
        ))
        
        bar_cos = always_redraw(lambda: Line(
            start=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            end=axes.c2p(x_tracker.get_value(), 1),
            stroke_width=4,  # Reduced for compact graph
            color=COS_COLOR,
            stroke_opacity=0.7
        ))
        
        # Vertical line tracker
        vertical_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(x_tracker.get_value(), -0.1),
            end=axes.c2p(x_tracker.get_value(), 1.1),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.5
        ))
        
        # Small dynamic labels that move with dots - positioned to avoid overlap
        sin_dot_label = always_redraw(lambda: MathTex(
            "\\sin^2", 
            color=SIN_COLOR, 
            font_size=18  # Smaller for compact graph
        ).next_to(dot_sin.get_center(), UR, buff=0.08))
        
        cos_dot_label = always_redraw(lambda: MathTex(
            "\\cos^2", 
            color=COS_COLOR, 
            font_size=18  # Smaller for compact graph
        ).next_to(dot_cos.get_center(), DR, buff=0.08))

        # --- 9. Main Tracking Animation ---
        
        # Add initial dynamic tracking elements
        self.add(vertical_line, dot_sin, dot_cos, bar_sin, bar_cos, sin_dot_label, cos_dot_label)
        
        # Fade out the large labels and introduce the unit circle
        self.play(
            FadeOut(sin_label_initial),
            FadeOut(cos_label_initial),
            FadeIn(unit_circle),
            FadeIn(circle_x_axis),
            FadeIn(circle_y_axis),
            run_time=1.5
        )
        
        # Add the unit circle dynamic elements (including revolutionary right angle symbol)
        self.add(radius_line, circle_dot, cos_line, sin_line, right_angle_symbol, cos_circle_label, sin_circle_label, angle_arc)
        
        # Main animation - sweep across the domain
        self.play(
            x_tracker.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear
        )
        
        # --- 10. Finale ---
        
        # Pause to observe the final state
        self.wait(1)
        
        # Highlight the constant sum
        self.play(
            Indicate(sum_val, color=GOLD, scale_factor=1.2),
            Indicate(identity_eq[0][14], color=GOLD, scale_factor=1.2),
            run_time=2
        )
        
        # Final emphasis on the identity
        self.play(
            identity_eq.animate.set_color_by_gradient(GOLD, WHITE).scale(1.05),
            run_time=1.5
        )
        
        self.wait(3)
    
    def create_perfect_right_angle_symbol(self, circle_center, theta, size=0.08):
        """
        Revolutionary approach: Use vector math to position the right angle symbol
        perfectly inside the triangle for all quadrants by finding the intersection
        of perpendicular unit vectors from each triangle edge.
        """
        
        # Get current trig values
        cos_val = np.cos(theta)
        sin_val = np.sin(theta)
        
        # Skip drawing when very close to axis intersections to avoid visual artifacts
        if abs(cos_val) < 0.01 or abs(sin_val) < 0.01:
            return Rectangle(width=0, height=0, fill_opacity=0, stroke_opacity=0)
        
        # Define the three vertices of the right triangle
        origin = circle_center  # Center of circle
        x_vertex = circle_center + 0.8 * np.array([cos_val, 0, 0])  # End of cos line
        y_vertex = circle_center + 0.8 * np.array([cos_val, sin_val, 0])  # Point on circle
        
        # Create unit vectors along each edge of the triangle
        # Vector from origin to x_vertex (along cos line)
        cos_direction = np.array([np.sign(cos_val), 0, 0])
        
        # Vector from x_vertex to y_vertex (along sin line)
        sin_direction = np.array([0, np.sign(sin_val), 0])
        
        # Position the right angle square using these unit vectors
        # The square should be positioned inward from the right angle corner
        corner_offset = size * 0.5  # Half the size of the square
        
        # The square center is displaced from the right angle corner (x_vertex)
        # by moving inward along both triangle edges
        square_center = x_vertex + corner_offset * (cos_direction + sin_direction)
        
        # Create the right angle square
        square = Rectangle(
            width=size,
            height=size,
            color=WHITE,
            stroke_width=1.5,
            fill_opacity=0,
            stroke_opacity=0.8
        )
        square.move_to(square_center)
        
        return square