from manim import *
import numpy as np

class SineCosineUnitCircle(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        title = MathTex(r"\mathbb{U}\text{nit}\ \mathbb{C}\text{ircle}\ \mathbb{G}\text{raphs}", font_size=48)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.1)
        
        
        cos_axes = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-1, 1, 1],
            x_length=3.2,
            y_length=1.4,
            axis_config={"color": GREY},
            tips=False,
        ).shift(UP * 1.2)  
        
        sin_axes = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-1, 1, 1],
            x_length=3.2,
            y_length=1.4,
            axis_config={"color": GREY},
            tips=False,
        ).shift(DOWN * 0.6)  
        
        
        for axes in [cos_axes, sin_axes]:
            axes.add(axes.get_x_axis().get_tick_marks())
            axes.add(axes.get_y_axis().get_tick_marks())
            x_lines = VGroup()
            y_lines = VGroup()
            for x in np.arange(0, 2*PI + 0.1, PI/2):
                x_lines.add(Line(axes.c2p(x, -1), axes.c2p(x, 1), stroke_width=1, stroke_color=GREY, stroke_opacity=0.6))
            for y in np.arange(-1, 1.1, 1):
                y_lines.add(Line(axes.c2p(0, y), axes.c2p(2*PI, y), stroke_width=1, stroke_color=GREY, stroke_opacity=0.6))
            axes.add(x_lines, y_lines)
        
        
        cos_x_labels = VGroup()
        sin_x_labels = VGroup()
        for axes, labels_group in [(cos_axes, cos_x_labels), (sin_axes, sin_x_labels)]:
            labels_group.add(MathTex(r"\pi", font_size=24).next_to(axes.c2p(PI, 0), DOWN, buff=0.1))
            labels_group.add(MathTex(r"2\pi", font_size=24).next_to(axes.c2p(2*PI, 0), DOWN, buff=0.1))
            labels_group.add(MathTex(r"1", font_size=24).next_to(axes.c2p(0, 1), LEFT, buff=0.1))
            labels_group.add(MathTex(r"-1", font_size=24).next_to(axes.c2p(0, -1), LEFT, buff=0.1))
        
        
        cos_label = MathTex(r"\cos\theta", color=BLUE, font_size=32).next_to(cos_axes, UP, buff=0.2)
        sin_label = MathTex(r"\sin\theta", color=RED, font_size=32).next_to(sin_axes, DOWN, buff=0.2)
        
        
        circle_center = sin_axes.get_origin() + RIGHT * (sin_axes.x_length + 1.4)
        unit_circle = Circle(radius=0.8, color=GREEN, stroke_width=2.5).move_to(circle_center)
        
        
        circle_axes = Axes(
            x_range=[-1, 1, 1],
            y_range=[-1, 1, 1],
            x_length=1.6,  
            y_length=1.6,
            axis_config={"color": GREY, "stroke_width": 1.5},
            tips=False,
        ).move_to(circle_center)
        
        
        circle_x_labels = VGroup(
            MathTex(r"1", font_size=20).next_to(circle_axes.c2p(1, 0), RIGHT, buff=0.1),
            MathTex(r"-1", font_size=20).next_to(circle_axes.c2p(-1, 0), LEFT, buff=0.1)
        )
        circle_y_labels = VGroup(
            MathTex(r"1", font_size=20).next_to(circle_axes.c2p(0, 1), UP, buff=0.1),
            MathTex(r"-1", font_size=20).next_to(circle_axes.c2p(0, -1), DOWN, buff=0.1)
        )
        
        
        theta_tracker = ValueTracker(0)
        
        
        theta_display = always_redraw(lambda: 
            MathTex(rf"\theta = {theta_tracker.get_value() * 180 / PI:.0f}°", font_size=28, color=ORANGE)
            .next_to(cos_axes, UP, buff=0.7)
        )
        
        
        diagram_group = VGroup(
            cos_axes, sin_axes,
            cos_x_labels, sin_x_labels,
            cos_label, sin_label,
            unit_circle, circle_axes, circle_x_labels, circle_y_labels
        )
        
        
        diagram_group.move_to(ORIGIN + DOWN * 0.3)  
        
        
        cos_dot = always_redraw(lambda: Dot(
            cos_axes.c2p(theta_tracker.get_value(), np.cos(theta_tracker.get_value())),
            color=BLUE, radius=0.06
        ))
        sin_dot = always_redraw(lambda: Dot(
            sin_axes.c2p(theta_tracker.get_value(), np.sin(theta_tracker.get_value())),
            color=RED, radius=0.06
        ))
        circle_dot = always_redraw(lambda: Dot(
            unit_circle.point_at_angle(theta_tracker.get_value()),
            color=GREEN, radius=0.06
        ))
        
        
        cos_path = TracedPath(cos_dot.get_center, stroke_color=BLUE, stroke_width=3)
        sin_path = TracedPath(sin_dot.get_center, stroke_color=RED, stroke_width=3)
        
        
        radius_line = always_redraw(lambda: Line(
            unit_circle.get_center(), circle_dot.get_center(), color=GREEN, stroke_width=1.5,
        ))
        
        
        cos_component = always_redraw(lambda: Line(
            unit_circle.get_center(),
            [circle_dot.get_center()[0], unit_circle.get_center()[1], 0],
            color=BLUE, stroke_width=2.5
        ))
        
        sin_component = always_redraw(lambda: Line(
            [circle_dot.get_center()[0], unit_circle.get_center()[1], 0],
            circle_dot.get_center(),
            color=RED, stroke_width=2.5
        ))
        
        
        horizontal_tangent = Line(
            start=[cos_axes.get_origin()[0], unit_circle.get_top()[1], 0],
            end=[unit_circle.get_right()[0], unit_circle.get_top()[1], 0],
            stroke_color=GREY,
            stroke_width=1.2
        )

        
        def get_cos_dotted_line():
            start_p = cos_dot.get_center()
            end_p = [cos_axes.c2p(2 * PI, 0)[0], start_p[1], 0]
            return DashedLine(start_p, end_p, color=BLUE, stroke_width=1.5, dash_length=0.05, stroke_opacity=0.7)

        cos_dotted_line = always_redraw(get_cos_dotted_line)

        
        def get_circle_dotted_line():
            start_p = circle_dot.get_center()
            end_p = [start_p[0], horizontal_tangent.get_y(), 0]
            return DashedLine(start_p, end_p, color=BLUE, stroke_width=1.5, dash_length=0.05, stroke_opacity=0.7)

        circle_dotted_line = always_redraw(get_circle_dotted_line)

        
        def get_corner_arc():
            start_point = cos_dotted_line.get_end()
            end_point = circle_dotted_line.get_end()
            return ArcBetweenPoints(
                start_point, end_point, 
                angle=-PI/2, 
                color=GREEN,  
                stroke_width=2
            )

        corner_arc = always_redraw(get_corner_arc)

        
        sin_projection_line = always_redraw(lambda: DashedLine(
            circle_dot.get_center(),
            [sin_dot.get_center()[0], circle_dot.get_center()[1], 0],
            color=RED, stroke_width=1.5, dash_length=0.05, stroke_opacity=0.7
        ))
        
        
        theta_symbol = MathTex(r"\theta", font_size=20, color=ORANGE).next_to(unit_circle.get_center(), DR, buff=0.15)
        
        
        angle_arc = always_redraw(lambda: Arc(
            start_angle=0,
            angle=theta_tracker.get_value() % (2*PI),
            radius=0.25,
            color=ORANGE,
            stroke_width=2
        ).move_arc_center_to(unit_circle.get_center()))
        
        
        self.add(cos_path, sin_path)
        
        
        self.add(title)
        
        
        self.play(
            AnimationGroup(
                DrawBorderThenFill(cos_axes), FadeIn(cos_x_labels), FadeIn(cos_label),
                DrawBorderThenFill(sin_axes), FadeIn(sin_x_labels), FadeIn(sin_label),
                DrawBorderThenFill(unit_circle), DrawBorderThenFill(circle_axes), 
                FadeIn(circle_x_labels), FadeIn(circle_y_labels),
                FadeIn(cos_dot), FadeIn(sin_dot), FadeIn(circle_dot),
                DrawBorderThenFill(radius_line), DrawBorderThenFill(cos_component), DrawBorderThenFill(sin_component),
                DrawBorderThenFill(horizontal_tangent), DrawBorderThenFill(cos_dotted_line),
                DrawBorderThenFill(circle_dotted_line), DrawBorderThenFill(corner_arc), DrawBorderThenFill(sin_projection_line),
                FadeIn(theta_symbol), DrawBorderThenFill(angle_arc),
                lag_ratio=0
            ),
            run_time=1.5,
            rate_func=smooth
        )
        
        
        self.add(theta_display)
        
        
        self.play(
            theta_tracker.animate.set_value(2*PI),
            run_time=12,
            rate_func=linear
        )
        
        self.wait(2)