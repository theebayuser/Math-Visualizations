from manim import *
import numpy as np


SIN_COLOR = BLUE_D
COS_COLOR = TEAL_D
SUM_COLOR = GOLD_D
BACKGROUND_COLOR = BLACK
AXES_COLOR = WHITE

class PythagoreanTrigIdentity(MovingCameraScene):
    def construct(self):
        
        self.camera.background_color = BACKGROUND_COLOR
        x_tracker = ValueTracker(0)
        
        
        title = Text("The Pythagorean Identity", font_size=34).set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.2)
        
        
        axes = Axes(
            x_range=[0, 4.5 * PI, PI],  
            y_range=[-1.4, 1.4, 0.5],   
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
        
        
        axes.x_axis.tip.scale(0.6)
        axes.y_axis.tip.scale(0.6)
        
        axes.shift(UP * 0.1)  

        
        x_labels = VGroup()
        for i in range(1, 5):
            val = i * PI
            label_text = f"{i}\\pi" if i > 1 else "\\pi"
            label = MathTex(label_text, font_size=18).next_to(axes.c2p(val, 0), DOWN, buff=0.1)
            x_labels.add(label)
        
        
        y_labels = VGroup()
        for val in [-1, 0.5, 1.0]:
            if val != 0:
                label = MathTex(f"{val}" if val != 0.5 else "0.5", font_size=18).next_to(axes.c2p(0, val), LEFT, buff=0.1)
                y_labels.add(label)
        
        self.play(GrowFromCenter(title))
        self.play(Create(axes), Write(x_labels), Write(y_labels), run_time=2)

        
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
        
        
        sin_label_initial = MathTex("\\sin(x)", color=SIN_COLOR, font_size=35)
        cos_label_initial = MathTex("\\cos(x)", color=COS_COLOR, font_size=35)
        
        
        label_y_position = title.get_bottom()[1] - 1.5  
        axes_center_x = axes.get_center()[0]  
        
        sin_label_initial.move_to([axes_center_x - 1.0, label_y_position, 0])
        cos_label_initial.move_to([axes_center_x + 1.0, label_y_position, 0])
        
        
        self.play(
            Create(sin_graph),
            Create(cos_graph),
            Write(sin_label_initial),
            Write(cos_label_initial),
            run_time=2
        )
        
        self.wait(0.5)

        
        
        
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
        
        
        sin_label_sq = MathTex("\\sin^2(x)", color=SIN_COLOR, font_size=35)
        cos_label_sq = MathTex("\\cos^2(x)", color=COS_COLOR, font_size=35)
        
        sin_label_sq.move_to([axes_center_x - 1.0, label_y_position, 0])
        cos_label_sq.move_to([axes_center_x + 1.0, label_y_position, 0])
        
        
        self.play(
            Transform(sin_graph, sin_sq_graph),
            Transform(cos_graph, cos_sq_graph),
            Transform(sin_label_initial, sin_label_sq),
            Transform(cos_label_initial, cos_label_sq),
            run_time=2
        )
        
        self.wait(0.5)

        
        identity_eq = MathTex(
            "\\sin^2(\\theta) + \\cos^2(\\theta) = 1",
            font_size=40
        )
        identity_eq.shift(DOWN * 1.4)  
        
        identity_eq[0][0:6].set_color(SIN_COLOR)  
        identity_eq[0][7:13].set_color(COS_COLOR)  
        identity_eq[0][14].set_color(SUM_COLOR)   

        self.play(Write(identity_eq), run_time=1.5)

        
        
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

        
        plus_live = MathTex("+", font_size=30)
        equals_live = MathTex("=", font_size=30)
        
        
        live_equation = VGroup(sin_val, plus_live, cos_val, equals_live, sum_val)
        live_equation.arrange(RIGHT, buff=0.3)
        live_equation.shift(DOWN * 2.4)  
        
        
        sin_val.add_updater(lambda m: m.set_value(np.sin(x_tracker.get_value())**2))
        cos_val.add_updater(lambda m: m.set_value(np.cos(x_tracker.get_value())**2))
        sum_val.add_updater(lambda m: m.set_value(np.sin(x_tracker.get_value())**2 + np.cos(x_tracker.get_value())**2))
        
        self.add(live_equation)

        
        circle_center = np.array([axes_center_x, label_y_position, 0])  
        
        
        unit_circle = Circle(radius=0.8, color=WHITE, stroke_width=2)
        unit_circle.move_to(circle_center)
        
        
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
        
        
        radius_line = always_redraw(lambda: Line(
            start=circle_center,
            end=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), np.sin(x_tracker.get_value()), 0]),
            color=WHITE,
            stroke_width=2
        ))
        
        
        circle_dot = always_redraw(lambda: Dot(
            point=circle_center + 0.8 * np.array([np.cos(x_tracker.get_value()), np.sin(x_tracker.get_value()), 0]),
            color=WHITE,
            radius=0.04
        ))
        
        
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
        
        
        right_angle_symbol = always_redraw(lambda: self.create_perfect_right_angle_symbol(
            circle_center,
            x_tracker.get_value(),
            size=0.08
        ))
        
        
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
        
        
        angle_arc = always_redraw(lambda: Arc(
            start_angle=0,
            angle=x_tracker.get_value() % (2*PI),
            radius=0.3,
            color=RED,
            stroke_width=2,
            arc_center=circle_center
        ))

        
        dot_sin = always_redraw(lambda: Dot(
            point=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            color=SIN_COLOR,
            radius=0.05  
        ))
        
        dot_cos = always_redraw(lambda: Dot(
            point=axes.c2p(x_tracker.get_value(), np.cos(x_tracker.get_value())**2),
            color=COS_COLOR,
            radius=0.05  
        ))
        
        bar_sin = always_redraw(lambda: Line(
            start=axes.c2p(x_tracker.get_value(), 0),
            end=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            stroke_width=4,  
            color=SIN_COLOR,
            stroke_opacity=0.7
        ))
        
        bar_cos = always_redraw(lambda: Line(
            start=axes.c2p(x_tracker.get_value(), np.sin(x_tracker.get_value())**2),
            end=axes.c2p(x_tracker.get_value(), 1),
            stroke_width=4,  
            color=COS_COLOR,
            stroke_opacity=0.7
        ))
        
        
        vertical_line = always_redraw(lambda: DashedLine(
            start=axes.c2p(x_tracker.get_value(), -0.1),
            end=axes.c2p(x_tracker.get_value(), 1.1),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.5
        ))
        
        
        sin_dot_label = always_redraw(lambda: MathTex(
            "\\sin^2", 
            color=SIN_COLOR, 
            font_size=18  
        ).next_to(dot_sin.get_center(), UR, buff=0.08))
        
        cos_dot_label = always_redraw(lambda: MathTex(
            "\\cos^2", 
            color=COS_COLOR, 
            font_size=18  
        ).next_to(dot_cos.get_center(), DR, buff=0.08))

        
        
        
        self.add(vertical_line, dot_sin, dot_cos, bar_sin, bar_cos, sin_dot_label, cos_dot_label)
        
        
        self.play(
            FadeOut(sin_label_initial),
            FadeOut(cos_label_initial),
            FadeIn(unit_circle),
            FadeIn(circle_x_axis),
            FadeIn(circle_y_axis),
            run_time=1.5
        )
        
        
        self.add(radius_line, circle_dot, cos_line, sin_line, right_angle_symbol, cos_circle_label, sin_circle_label, angle_arc)
        
        
        self.play(
            x_tracker.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear
        )
        
        
        
        
        self.wait(1)
        
        
        self.play(
            Indicate(sum_val, color=GOLD, scale_factor=1.2),
            Indicate(identity_eq[0][14], color=GOLD, scale_factor=1.2),
            run_time=2
        )
        
        
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
        
        
        cos_val = np.cos(theta)
        sin_val = np.sin(theta)
        
        
        if abs(cos_val) < 0.01 or abs(sin_val) < 0.01:
            return Rectangle(width=0, height=0, fill_opacity=0, stroke_opacity=0)
        
        
        origin = circle_center  
        x_vertex = circle_center + 0.8 * np.array([cos_val, 0, 0])  
        y_vertex = circle_center + 0.8 * np.array([cos_val, sin_val, 0])  
        
        
        
        cos_direction = np.array([np.sign(cos_val), 0, 0])
        
        
        sin_direction = np.array([0, np.sign(sin_val), 0])
        
        
        
        corner_offset = size * 0.5  
        
        
        
        square_center = x_vertex + corner_offset * (cos_direction + sin_direction)
        
        
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