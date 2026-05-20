from manim import *
import numpy as np

class SqueezeTheoremProof(Scene):
    def construct(self):
        # Set up the scene to use middle third of screen vertically
        self.camera.frame_width = 14
        self.camera.frame_height = 8
        
        # Title components - reordered: limit expression first, then texts
        limit_expr = MathTex(r"\lim_{x \to 0} \frac{\sin x}{x} = 1", font_size=40)
        limit_expr.set_color_by_gradient(BLUE, RED)
        proof_text = Text("Proof of", font_size=32, color=WHITE)
        squeeze_text = Text("Using the Squeeze Theorem", font_size=32, color=WHITE)
        
        # Position title components in center
        limit_expr.move_to(ORIGIN)
        proof_text.move_to(UP * 0.8)
        squeeze_text.move_to(DOWN * 0.8)
        
        # Show title sequence: limit expression first, then text
        self.play(
            Write(limit_expr),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            Write(proof_text),
            Write(squeeze_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Fade out supplementary text and move limit to top
        self.play(
            FadeOut(proof_text),
            FadeOut(squeeze_text),
            limit_expr.animate.move_to(UP * 3.2),
            run_time=1
        )
        self.wait(0.5)
        
        # Set up coordinate system with normal-sized arrows
        unit_length = 1.2  # Unit length in Manim units
        
        # Create axes with built-in tips using different approach
        axes = Axes(
            x_range=[-1.5, 1.5, 1.0],
            y_range=[-1.5, 1.5, 1.0],
            x_length=3.0 * unit_length,  # Equal length for x-axis
            y_length=3.0 * unit_length,  # Equal length for y-axis
            axis_config={
                "color": GRAY, 
                "stroke_width": 2,
                "tip_width": 0.15,
                "tip_height": 0.15
            },
            tips=True
        ).shift(DOWN * 1.5)  # Moved slightly higher
        
        # Add axis labels with 1 and -1
        x_pos_label = MathTex("1", font_size=18, color=WHITE)
        x_pos_label.next_to(axes.c2p(1, 0), DOWN, buff=0.1)
        x_neg_label = MathTex("-1", font_size=18, color=WHITE)
        x_neg_label.next_to(axes.c2p(-1, 0), DOWN, buff=0.1)
        
        y_pos_label = MathTex("1", font_size=18, color=WHITE)
        y_pos_label.next_to(axes.c2p(0, 1), LEFT, buff=0.1)
        y_neg_label = MathTex("-1", font_size=18, color=WHITE)
        y_neg_label.next_to(axes.c2p(0, -1), LEFT, buff=0.1)
        
        # TRUE unit circle with radius = unit_length in Manim space
        circle = Circle(radius=unit_length, color=WHITE, stroke_width=3)
        circle.move_to(axes.c2p(0, 0))
        
        # Initial angle 
        theta_value = ValueTracker(PI/3)
        
        # Key points
        def get_angle():
            return theta_value.get_value()
        
        def get_circle_point():
            theta = get_angle()
            return axes.c2p(np.cos(theta), np.sin(theta))
        
        def get_unit_point():
            return axes.c2p(1, 0)
        
        def get_origin():
            return axes.c2p(0, 0)
        
        # Key lines with matching colors
        radius_line = always_redraw(lambda: Line(
            get_origin(), get_circle_point(), 
            color=GREEN, stroke_width=3  # Green like triangle
        ))
        
        # Line from origin to (1,0)
        unit_radius = always_redraw(lambda: Line(
            get_origin(), get_unit_point(),
            color=GREEN, stroke_width=3  # Green like triangle
        ))
        
        # Line from (1,0) to point on circle (hypotenuse)
        chord_line = always_redraw(lambda: Line(
            get_unit_point(), get_circle_point(),
            color=GREEN, stroke_width=3  # Green like triangle
        ))
        
        # Tangent line at (1,0) - consistent thickness
        tangent_line = always_redraw(lambda: Line(
            get_unit_point(), axes.c2p(1, np.tan(get_angle())),
            color=BLUE, stroke_width=3  # Same thickness as other lines
        ))
        
        # Line from origin to top of blue triangle
        hypotenuse_line = always_redraw(lambda: Line(
            get_origin(), axes.c2p(1, np.tan(get_angle())),
            color=BLUE, stroke_width=3
        ))
        
        # GREEN triangle: Origin -> (1,0) -> Point on circle (initially not filled)
        green_triangle = always_redraw(lambda: Polygon(
            get_origin(), get_unit_point(), get_circle_point(),
            fill_color=GREEN, fill_opacity=0, stroke_width=0
        ))
        
        # PINK sector: From origin along the arc (initially not filled)
        def create_sector():
            theta = get_angle()
            if theta < 0.01:  # Avoid degenerate case
                return VMobject()
            points = [get_origin()]
            # Create arc points
            for t in np.linspace(0, theta, max(10, int(20*theta))):
                points.append(axes.c2p(np.cos(t), np.sin(t)))
            points.append(get_origin())
            return Polygon(*points, fill_color=PINK, fill_opacity=0, stroke_width=0)
        
        sector = always_redraw(create_sector)
        
        # BLUE triangle: Origin -> (1,0) -> (1, tan(x)) (initially not filled)
        blue_triangle = always_redraw(lambda: Polygon(
            get_origin(), get_unit_point(), axes.c2p(1, np.tan(get_angle())),
            fill_color=BLUE, fill_opacity=0, stroke_width=0
        ))
        
        # Show the geometric setup - faster
        self.play(
            Create(axes),
            Write(x_pos_label),
            Write(x_neg_label),
            Write(y_pos_label),
            Write(y_neg_label),
            Create(circle),
            run_time=1
        )
        
        self.play(
            Create(radius_line),
            Create(unit_radius),
            Create(chord_line),
            Create(tangent_line),
            Create(hypotenuse_line),
            run_time=1
        )
        
        # Show the three areas without filling initially
        self.play(
            FadeIn(green_triangle),
            FadeIn(sector), 
            FadeIn(blue_triangle),
            run_time=1
        )
        
        # CENTERED AREA EXPRESSIONS WITH LABELS
        
        # Create the three area expressions with labels, centered and evenly spaced
        area_triangle1_full = MathTex(r"\text{Area}_{\text{triangle1}} = \frac{1}{2} \cdot 1 \cdot \sin x", font_size=24, color=GREEN)
        area_sector_full = MathTex(r"\text{Area}_{\text{sector}} = \frac{1}{2} \cdot 1^2 \cdot x", font_size=24, color=PINK)
        area_triangle2_full = MathTex(r"\text{Area}_{\text{triangle2}} = \frac{1}{2} \cdot 1 \cdot \tan x", font_size=24, color=BLUE)
        
        # Position them centered and evenly spaced
        area_triangle1_full.move_to(UP * 2.2)
        area_sector_full.move_to(UP * 1.6)
        area_triangle2_full.move_to(UP * 1.0)
        
        # Extract just the expression parts for later animation
        area_triangle1_expr = MathTex(r"\frac{1}{2} \cdot 1 \cdot \sin x", font_size=24, color=GREEN)
        area_sector_expr = MathTex(r"\frac{1}{2} \cdot 1^2 \cdot x", font_size=24, color=PINK)
        area_triangle2_expr = MathTex(r"\frac{1}{2} \cdot 1 \cdot \tan x", font_size=24, color=BLUE)
        
        # Show triangle 1 area with fill and labels - SHADE IMMEDIATELY
        self.play(
            green_triangle.animate.set_fill_opacity(0.4),
            Write(area_triangle1_full),
            run_time=1
        )
        
        # Show labels for green triangle
        altitude_line = always_redraw(lambda: Line(
            get_circle_point(), axes.c2p(np.cos(get_angle()), 0),
            color=YELLOW, stroke_width=2, stroke_opacity=0.8
        ))
        
        altitude_label = always_redraw(lambda: MathTex("1", font_size=20, color=YELLOW).next_to(
            Line(get_circle_point(), axes.c2p(np.cos(get_angle()), 0)).get_center(), 
            LEFT, buff=0.1
        ))
        
        base_label = always_redraw(lambda: MathTex(r"\sin x", font_size=20, color=YELLOW).next_to(
            Line(axes.c2p(np.cos(get_angle()), 0), get_unit_point()).get_center(),
            DOWN, buff=0.1
        ))
        
        self.play(
            Create(altitude_line),
            Write(altitude_label),
            Write(base_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Fade out labels but KEEP triangle shaded
        self.play(
            FadeOut(altitude_line),
            FadeOut(altitude_label), 
            FadeOut(base_label),
            run_time=0.5
        )
        
        # Show sector area with fill and labels - SHADE IMMEDIATELY
        self.play(
            sector.animate.set_fill_opacity(0.4),
            Write(area_sector_full),
            run_time=1
        )
        
        # Simple "x" label for angle - no arc symbol
        angle_label = always_redraw(lambda: MathTex("x", font_size=20, color=YELLOW).move_to(
            get_origin() + 0.4 * RIGHT + 0.15 * UP
        ))
        
        radius_label = always_redraw(lambda: MathTex("1", font_size=20, color=YELLOW).next_to(
            Line(get_origin(), get_circle_point()).get_center(), 
            UP + RIGHT, buff=0.05
        ))
        
        self.play(
            Write(angle_label),
            Write(radius_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Fade out labels but KEEP sector shaded
        self.play(
            FadeOut(angle_label),
            FadeOut(radius_label),
            run_time=0.5
        )
        
        # Show triangle 2 area with fill and labels - SHADE IMMEDIATELY
        self.play(
            blue_triangle.animate.set_fill_opacity(0.4),
            Write(area_triangle2_full),
            run_time=1
        )
        
        # Labels for blue triangle
        tanx_label = always_redraw(lambda: MathTex(r"\tan x", font_size=20, color=YELLOW).next_to(
            Line(get_unit_point(), axes.c2p(1, np.tan(get_angle()))).get_center(),
            RIGHT, buff=0.1
        ))
        
        base_1_label = always_redraw(lambda: MathTex("1", font_size=20, color=YELLOW).next_to(
            Line(get_origin(), get_unit_point()).get_center(),
            DOWN, buff=0.1
        ))
        
        self.play(
            Write(tanx_label),
            Write(base_1_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Fade out labels but KEEP triangle shaded
        self.play(
            FadeOut(tanx_label),
            FadeOut(base_1_label),
            run_time=0.5
        )
        
        # Now animate the expressions moving to form the inequality
        # Keep all shapes filled
        
        # Create the complete inequality
        eq1_complete = MathTex(
            r"\frac{1}{2} \cdot 1 \cdot \sin x", r"\leq", r"\frac{1}{2} \cdot 1^2 \cdot x", r"\leq", r"\frac{1}{2} \cdot 1 \cdot \tan x",
            font_size=26
        )
        eq1_complete.move_to(UP * 2.4)
        eq1_complete[0].set_color(GREEN)  # First part green
        eq1_complete[2].set_color(PINK)   # Middle part pink  
        eq1_complete[4].set_color(BLUE)   # Last part blue
        
        # Position the individual expressions to match the full expressions for smooth transition
        area_triangle1_expr.move_to(area_triangle1_full[-1].get_center())  # Expression part
        area_sector_expr.move_to(area_sector_full[-1].get_center())
        area_triangle2_expr.move_to(area_triangle2_full[-1].get_center())
        
        # Animate the expressions moving to their positions in the inequality
        self.play(
            # Transform full expressions to just the math parts
            Transform(area_triangle1_full, area_triangle1_expr),
            Transform(area_sector_full, area_sector_expr), 
            Transform(area_triangle2_full, area_triangle2_expr),
            run_time=1
        )
        
        # Now move them to inequality positions and add inequality symbols
        self.play(
            Transform(area_triangle1_full, eq1_complete[0]),
            Transform(area_sector_full, eq1_complete[2]),
            Transform(area_triangle2_full, eq1_complete[4]),
            Write(eq1_complete[1]),  # ≤ symbol
            Write(eq1_complete[3]),  # ≤ symbol
            run_time=1.5
        )
        self.wait(1)
        
        # Continue with the rest of the proof...
        # Step 2: Write sinx/2 <= x/2 <= tanx/2 below that
        eq2 = MathTex(r"\frac{\sin x}{2}", r"\leq", r"\frac{x}{2}", r"\leq", r"\frac{\tan x}{2}", font_size=24)
        eq2.move_to(UP * 1.9)
        eq2[0].set_color(GREEN)
        eq2[2].set_color(PINK)
        eq2[4].set_color(BLUE)
        
        self.play(Write(eq2), run_time=1)
        self.wait(1)
        
        # Step 3: Morph that into sinx <= x <= tanx (keep in same position)
        eq3 = MathTex(r"\sin x", r"\leq", r"x", r"\leq", r"\tan x", font_size=26)
        eq3.move_to(UP * 1.9)  # Same position as eq2
        eq3[0].set_color(GREEN)
        eq3[2].set_color(PINK)
        eq3[4].set_color(BLUE)
        
        self.play(Transform(eq2, eq3), run_time=1)
        self.wait(1)
        
        # Step 4: Write sinx/sinx <= x/sinx <= tanx/sinx below that
        eq4 = MathTex(r"\frac{\sin x}{\sin x}", r"\leq", r"\frac{x}{\sin x}", r"\leq", r"\frac{\tan x}{\sin x}", font_size=24)
        eq4.move_to(UP * 1.4)
        eq4[0].set_color(GREEN)
        eq4[2].set_color(PINK)
        eq4[4].set_color(BLUE)
        
        self.play(Write(eq4), run_time=1)
        self.wait(1)
        
        # Step 5: Morph that into 1 <= x/sinx <= 1/cosx (keep in same position)
        eq5 = MathTex(r"1", r"\leq", r"\frac{x}{\sin x}", r"\leq", r"\frac{1}{\cos x}", font_size=26)
        eq5.move_to(UP * 1.4)  # Same position as eq4
        eq5[0].set_color(GREEN)
        eq5[2].set_color(PINK)
        eq5[4].set_color(BLUE)
        
        self.play(Transform(eq4, eq5), run_time=1)
        self.wait(1)
        
        # Step 6: Write cosx <= sinx/x <= 1 below that (reciprocal with flipped inequalities)
        eq6 = MathTex(r"\cos x", r"\leq", r"\frac{\sin x}{x}", r"\leq", r"1", font_size=26)
        eq6.move_to(UP * 0.7)  # Better spacing
        eq6[0].set_color(BLUE)   # cos x comes from 1/cos x (blue)
        eq6[2].set_color(PINK)   # sin x/x stays pink
        eq6[4].set_color(GREEN)  # 1 comes from the green side
        
        self.play(Write(eq6), run_time=1)
        self.wait(1)
        
        # Step 7: Fade everything else out and move that equation to the top
        everything_to_delete = VGroup(
            axes, x_pos_label, x_neg_label, y_pos_label, y_neg_label, circle, radius_line, unit_radius, 
            chord_line, tangent_line, hypotenuse_line, green_triangle, 
            sector, blue_triangle, area_triangle1_full, area_sector_full, area_triangle2_full, 
            eq1_complete[1], eq1_complete[3], eq2, eq4, limit_expr
        )
        
        self.play(
            FadeOut(everything_to_delete),
            eq6.animate.move_to(UP * 2),
            run_time=1.5
        )
        self.wait(1)
        
        # Step 8: Morph the cosx <= sinx/x <= 1 equation into the limit form
        eq7 = MathTex(
            r"\lim_{x \to 0} \cos x \leq \lim_{x \to 0} \frac{\sin x}{x} \leq \lim_{x \to 0} 1",
            font_size=26
        )
        eq7.move_to(UP * 2)  # Same position as eq6
        eq7.set_color(YELLOW)
        
        self.play(Transform(eq6, eq7), run_time=1)
        self.wait(0.5)
        
        # Step 9: Write below it the equation 1 <= lim sinx/x <= 1 and move it up
        eq8 = MathTex(r"1 \leq \lim_{x \to 0} \frac{\sin x}{x} \leq 1", font_size=28)
        eq8.move_to(UP * 1.2)  # Moved up to compensate
        eq8.set_color(GOLD)
        
        self.play(Write(eq8), run_time=1)
        self.wait(0.5)
        
        # Create squeeze theorem visualization graph - SMALLER and HIGHER
        graph_axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[0, 1.2, 0.2],
            x_length=4,  # Reduced from 6
            y_length=2,  # Reduced from 3
            axis_config={"color": GRAY, "stroke_width": 1},
            tips=False
        ).shift(DOWN * 0.5)  # Moved up from DOWN * 1.8
        
        # Functions for the squeeze theorem
        def cos_func(x):
            if abs(x) < 0.001:  # Avoid division by zero
                return 1
            return np.cos(x)
            
        def sinc_func(x):
            if abs(x) < 0.001:  # sin(x)/x approaches 1 as x approaches 0
                return 1
            return np.sin(x) / x
            
        def one_func(x):
            return 1
        
        # Create the function graphs
        cos_graph = graph_axes.plot(cos_func, x_range=[-1.5, 1.5], color=BLUE, stroke_width=3)
        sinc_graph = graph_axes.plot(sinc_func, x_range=[-1.5, 1.5], color=PINK, stroke_width=3)
        one_graph = graph_axes.plot(one_func, x_range=[-1.5, 1.5], color=GREEN, stroke_width=3)
        
        # Add labels for the graphs
        cos_label = MathTex(r"\cos x", font_size=16, color=BLUE).next_to(graph_axes.c2p(-1.2, 0.5), UP)
        sinc_label = MathTex(r"\frac{\sin x}{x}", font_size=16, color=PINK).next_to(graph_axes.c2p(0, 1), UP + RIGHT, buff=0.1)
        one_label = MathTex(r"1", font_size=16, color=GREEN).next_to(graph_axes.c2p(1.2, 1), UP)
        
        # Add vertical line at x = 0 to show convergence
        vertical_line = DashedLine(
            graph_axes.c2p(0, 0), graph_axes.c2p(0, 1.1),
            color=WHITE, stroke_width=2
        )
        
        # Show the squeeze theorem graph
        self.play(
            Create(graph_axes),
            Create(cos_graph),
            Create(sinc_graph),
            Create(one_graph),
            run_time=1
        )
        
        self.play(
            Write(cos_label),
            Write(sinc_label), 
            Write(one_label),
            Create(vertical_line),
            run_time=1
        )
        self.wait(1)
        
        # Fade out the top equation and the squeeze theorem graph, keep only the middle limit expression
        graph_elements = VGroup(graph_axes, cos_graph, sinc_graph, one_graph, cos_label, sinc_label, one_label, vertical_line)
        
        self.play(
            FadeOut(eq6),  # Top equation
            FadeOut(graph_elements),  # Squeeze theorem graph
            run_time=1
        )
        
        # Make the middle limit expression bigger and center it
        final_limit = MathTex(r"\lim_{x \to 0} \frac{\sin x}{x} = 1", font_size=48)
        final_limit.set_color_by_gradient(BLUE, RED)
        final_limit.move_to(ORIGIN)
        
        self.play(
            Transform(eq8, final_limit),
            run_time=2
        )
        
        self.wait(1)