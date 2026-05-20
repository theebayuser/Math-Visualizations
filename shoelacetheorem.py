from manim import *

class ShoelaceTheorem(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        vertices = [
            np.array([2, 1, 0]),
            np.array([1, 3, 0]),
            np.array([-1, 2, 0]),
            np.array([-2, -1, 0])
        ]
        
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY_B, "stroke_width": 1}
        )
        
        
        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GREY_B, "stroke_width": 0.5, "stroke_opacity": 0.3}
        )
        
        
        self.play(Create(grid), Create(axes), run_time=1)
        
        
        polygon = Polygon(*vertices, color=WHITE, stroke_width=3, fill_opacity=0)
        vertex_dots = VGroup(*[Dot(v, color=WHITE, radius=0.08) for v in vertices])
        
        
        first_vertex = Dot(vertices[0], color=BLUE_C, radius=0.1)
        
        self.play(
            Create(polygon),
            Create(vertex_dots),
            Transform(vertex_dots[0], first_vertex),
            run_time=1.5
        )
        
        
        area_question = MathTex("A = ?", color=WHITE).scale(1.2)
        area_question.move_to(polygon.get_center())
        self.play(Write(area_question), run_time=1)
        self.wait(1)
        
        
        self.play(FadeOut(area_question), run_time=0.5)
        
        
        coord_labels = VGroup()
        coord_values = [(2, 1), (1, 3), (-1, 2), (-2, -1)]
        
        for i, (vertex, (x, y)) in enumerate(zip(vertices, coord_values)):
            label = MathTex(f"({x}, {y})", color=WHITE).scale(0.7)
            label.next_to(vertex, UP + RIGHT * 0.3)
            coord_labels.add(label)
            
            
            x_line = DashedLine(vertex, [vertex[0], 0, 0], color=GREY_B, stroke_width=1)
            y_line = DashedLine(vertex, [0, vertex[1], 0], color=GREY_B, stroke_width=1)
            
            self.play(
                Create(x_line),
                Create(y_line),
                Write(label),
                run_time=0.6
            )
            self.play(FadeOut(x_line), FadeOut(y_line), run_time=0.3)
        
        
        origin_dot = Dot(ORIGIN, color=WHITE, radius=0.1)
        origin_dot.set_glow_opacity(0.8)
        self.play(Create(origin_dot), run_time=0.5)
        
        
        triangle_areas = []
        triangle_shapes = VGroup()
        diagonal_lines = VGroup()
        
        
        for i in range(len(vertices)):
            j = (i + 1) % len(vertices)
            v1, v2 = vertices[i], vertices[j]
            
            
            triangle = Polygon(ORIGIN, v1, v2, stroke_width=0)
            
            
            x1, y1 = v1[0], v1[1]
            x2, y2 = v2[0], v2[1]
            signed_area = 0.5 * (x1 * y2 - x2 * y1)
            
            
            if signed_area > 0:
                triangle.set_fill(BLUE, opacity=0.4)
            else:
                triangle.set_fill(ORANGE, opacity=0.4)
            
            triangle.set_glow_opacity(0.6)
            triangle_areas.append(signed_area)
            triangle_shapes.add(triangle)
            
            
            line1 = Line(ORIGIN, v1, color=WHITE, stroke_width=2)
            line2 = Line(ORIGIN, v2, color=WHITE, stroke_width=2)
            
            
            diagonal = Line(v1, v2, color=GREEN_C if signed_area > 0 else RED_C, stroke_width=3)
            diagonal.set_glow_opacity(0.8)
            diagonal_lines.add(diagonal)
            
            
            self.play(Create(line1), Create(line2), run_time=0.4)
            self.play(Create(diagonal), run_time=0.4)
            self.play(FadeIn(triangle), run_time=0.6)
            
            
            area_text = MathTex(f"\\frac{{1}}{{2}}({x1} \\cdot {y2} - {x2} \\cdot {y1})", color=WHITE).scale(0.6)
            area_text.next_to(triangle.get_center(), DOWN)
            self.play(Write(area_text), run_time=0.8)
            self.play(FadeOut(area_text), run_time=0.4)
            
            
            self.play(FadeOut(line1), FadeOut(line2), run_time=0.3)
        
        
        self.wait(1)
        
        
        overlap_group = VGroup()
        for i, triangle in enumerate(triangle_shapes):
            overlap_group.add(triangle)
        
        
        self.play(
            *[triangle.animate.set_fill_opacity(0.6) for triangle in triangle_shapes],
            run_time=1
        )
        
        
        
        final_polygon_fill = polygon.copy()
        final_polygon_fill.set_fill(PURPLE_C, opacity=0.6)
        final_polygon_fill.set_glow_opacity(0.8)
        
        self.play(
            *[FadeOut(triangle) for triangle in triangle_shapes],
            FadeOut(diagonal_lines),
            FadeIn(final_polygon_fill),
            run_time=1.5
        )
        
        
        formula = MathTex(
            r"A = \frac{1}{2} \left| \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i) \right|",
            color=WHITE
        ).scale(0.9)
        formula.to_edge(DOWN, buff=0.5)
        
        
        formula_colored = MathTex(
            r"A = \frac{1}{2} \left| \sum_{i=1}^{n} (",
            r"x_i y_{i+1}",
            r" - ",
            r"x_{i+1} y_i",
            r") \right|",
            color=WHITE
        ).scale(0.9)
        formula_colored[1].set_color(GREEN_C)
        formula_colored[3].set_color(RED_C)
        formula_colored.to_edge(DOWN, buff=0.5)
        
        self.play(Write(formula), run_time=2)
        self.play(Transform(formula, formula_colored), run_time=1.5)
        
        
        title = MathTex("\\text{Shoelace Theorem}", color=GOLD).scale(1.3)
        title.to_edge(UP, buff=0.5)
        title.set_glow_opacity(0.8)
        
        self.play(Write(title), run_time=1.5)
        
        
        self.play(
            final_polygon_fill.animate.set_glow_opacity(1.0),
            title.animate.set_glow_opacity(1.0),
            run_time=1
        )
        
        
        self.wait(2)
        
        
        all_objects = VGroup(
            grid, axes, polygon, vertex_dots, coord_labels, 
            origin_dot, final_polygon_fill, formula, title
        )
        
        self.play(
            FadeOut(all_objects),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        self.wait(0.5)

