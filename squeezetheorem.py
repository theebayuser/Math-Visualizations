from manim import *
import numpy as np

class SqueezeTheoremProof(Scene):
    def construct(self):
        
        self.camera.frame_width = 14
        self.camera.frame_height = 8
        
        
        limit_expr = MathTex(r"\lim_{x \to 0} \frac{\sin x}{x} = 1", font_size=40)
        limit_expr.set_color_by_gradient(BLUE, RED)
        proof_text = Text("Proof of", font_size=32, color=WHITE)
        squeeze_text = Text("Using the Squeeze Theorem", font_size=32, color=WHITE)
        
        
        limit_expr.move_to(ORIGIN)
        proof_text.move_to(UP * 0.8)
        squeeze_text.move_to(DOWN * 0.8)
        
        
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
        
        
        self.play(
            FadeOut(proof_text),
            FadeOut(squeeze_text),
            limit_expr.animate.move_to(UP * 3.2),
            run_time=1
        )
        self.wait(0.5)
        
        
        unit_length = 1.2  
        
        
        axes = Axes(
            x_range=[-1.5, 1.5, 1.0],
            y_range=[-1.5, 1.5, 1.0],
            x_length=3.0 * unit_length,  
            y_length=3.0 * unit_length,  
            axis_config={
                "color": GRAY, 
                "stroke_width": 2,
                "tip_width": 0.15,
                "tip_height": 0.15
            },
            tips=True
        ).shift(DOWN * 1.5)  
        
        
        x_pos_label = MathTex("1", font_size=18, color=WHITE)
        x_pos_label.next_to(axes.c2p(1, 0), DOWN, buff=0.1)
        x_neg_label = MathTex("-1", font_size=18, color=WHITE)
        x_neg_label.next_to(axes.c2p(-1, 0), DOWN, buff=0.1)
        
        y_pos_label = MathTex("1", font_size=18, color=WHITE)
        y_pos_label.next_to(axes.c2p(0, 1), LEFT, buff=0.1)
        y_neg_label = MathTex("-1", font_size=18, color=WHITE)
        y_neg_label.next_to(axes.c2p(0, -1), LEFT, buff=0.1)
        
        
        circle = Circle(radius=unit_length, color=WHITE, stroke_width=3)
        circle.move_to(axes.c2p(0, 0))
        
        
        theta_value = ValueTracker(PI/3)
        
        
        def get_angle():
            return theta_value.get_value()
        
        def get_circle_point():
            theta = get_angle()
            return axes.c2p(np.cos(theta), np.sin(theta))
        
        def get_unit_point():
            return axes.c2p(1, 0)
        
        def get_origin():
            return axes.c2p(0, 0)
        
        
        radius_line = always_redraw(lambda: Line(
            get_origin(), get_circle_point(), 
            color=GREEN, stroke_width=3  
        ))
        
        
        unit_radius = always_redraw(lambda: Line(
            get_origin(), get_unit_point(),
            color=GREEN, stroke_width=3  
        ))
        
        
        chord_line = always_redraw(lambda: Line(
            get_unit_point(), get_circle_point(),
            color=GREEN, stroke_width=3  
        ))
        
        
        tangent_line = always_redraw(lambda: Line(
            get_unit_point(), axes.c2p(1, np.tan(get_angle())),
            color=BLUE, stroke_width=3  
        ))
        
        
        hypotenuse_line = always_redraw(lambda: Line(
            get_origin(), axes.c2p(1, np.tan(get_angle())),
            color=BLUE, stroke_width=3
        ))
        
        
        green_triangle = always_redraw(lambda: Polygon(
            get_origin(), get_unit_point(), get_circle_point(),
            fill_color=GREEN, fill_opacity=0, stroke_width=0
        ))
        
        
        def create_sector():
            theta = get_angle()
            if theta < 0.01:  
                return VMobject()
            points = [get_origin()]
            
            for t in np.linspace(0, theta, max(10, int(20*theta))):
                points.append(axes.c2p(np.cos(t), np.sin(t)))
            points.append(get_origin())
            return Polygon(*points, fill_color=PINK, fill_opacity=0, stroke_width=0)
        
        sector = always_redraw(create_sector)
        
        
        blue_triangle = always_redraw(lambda: Polygon(
            get_origin(), get_unit_point(), axes.c2p(1, np.tan(get_angle())),
            fill_color=BLUE, fill_opacity=0, stroke_width=0
        ))
        
        
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
        
        
        self.play(
            FadeIn(green_triangle),
            FadeIn(sector), 
            FadeIn(blue_triangle),
            run_time=1
        )
        
        
        
        
        area_triangle1_full = MathTex(r"\text{Area}_{\text{triangle1}} = \frac{1}{2} \cdot 1 \cdot \sin x", font_size=24, color=GREEN)
        area_sector_full = MathTex(r"\text{Area}_{\text{sector}} = \frac{1}{2} \cdot 1^2 \cdot x", font_size=24, color=PINK)
        area_triangle2_full = MathTex(r"\text{Area}_{\text{triangle2}} = \frac{1}{2} \cdot 1 \cdot \tan x", font_size=24, color=BLUE)
        
        
        area_triangle1_full.move_to(UP * 2.2)
        area_sector_full.move_to(UP * 1.6)
        area_triangle2_full.move_to(UP * 1.0)
        
        
        area_triangle1_expr = MathTex(r"\frac{1}{2} \cdot 1 \cdot \sin x", font_size=24, color=GREEN)
        area_sector_expr = MathTex(r"\frac{1}{2} \cdot 1^2 \cdot x", font_size=24, color=PINK)
        area_triangle2_expr = MathTex(r"\frac{1}{2} \cdot 1 \cdot \tan x", font_size=24, color=BLUE)
        
        
        self.play(
            green_triangle.animate.set_fill_opacity(0.4),
            Write(area_triangle1_full),
            run_time=1
        )
        
        
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
        
        
        self.play(
            FadeOut(altitude_line),
            FadeOut(altitude_label), 
            FadeOut(base_label),
            run_time=0.5
        )
        
        
        self.play(
            sector.animate.set_fill_opacity(0.4),
            Write(area_sector_full),
            run_time=1
        )
        
        
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
        
        
        self.play(
            FadeOut(angle_label),
            FadeOut(radius_label),
            run_time=0.5
        )
        
        
        self.play(
            blue_triangle.animate.set_fill_opacity(0.4),
            Write(area_triangle2_full),
            run_time=1
        )
        
        
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
        
        
        self.play(
            FadeOut(tanx_label),
            FadeOut(base_1_label),
            run_time=0.5
        )
        
        
        
        
        
        eq1_complete = MathTex(
            r"\frac{1}{2} \cdot 1 \cdot \sin x", r"\leq", r"\frac{1}{2} \cdot 1^2 \cdot x", r"\leq", r"\frac{1}{2} \cdot 1 \cdot \tan x",
            font_size=26
        )
        eq1_complete.move_to(UP * 2.4)
        eq1_complete[0].set_color(GREEN)  
        eq1_complete[2].set_color(PINK)   
        eq1_complete[4].set_color(BLUE)   
        
        
        area_triangle1_expr.move_to(area_triangle1_full[-1].get_center())  
        area_sector_expr.move_to(area_sector_full[-1].get_center())
        area_triangle2_expr.move_to(area_triangle2_full[-1].get_center())
        
        
        self.play(
            
            Transform(area_triangle1_full, area_triangle1_expr),
            Transform(area_sector_full, area_sector_expr), 
            Transform(area_triangle2_full, area_triangle2_expr),
            run_time=1
        )
        
        
        self.play(
            Transform(area_triangle1_full, eq1_complete[0]),
            Transform(area_sector_full, eq1_complete[2]),
            Transform(area_triangle2_full, eq1_complete[4]),
            Write(eq1_complete[1]),  
            Write(eq1_complete[3]),  
            run_time=1.5
        )
        self.wait(1)
        
        
        
        eq2 = MathTex(r"\frac{\sin x}{2}", r"\leq", r"\frac{x}{2}", r"\leq", r"\frac{\tan x}{2}", font_size=24)
        eq2.move_to(UP * 1.9)
        eq2[0].set_color(GREEN)
        eq2[2].set_color(PINK)
        eq2[4].set_color(BLUE)
        
        self.play(Write(eq2), run_time=1)
        self.wait(1)
        
        
        eq3 = MathTex(r"\sin x", r"\leq", r"x", r"\leq", r"\tan x", font_size=26)
        eq3.move_to(UP * 1.9)  
        eq3[0].set_color(GREEN)
        eq3[2].set_color(PINK)
        eq3[4].set_color(BLUE)
        
        self.play(Transform(eq2, eq3), run_time=1)
        self.wait(1)
        
        
        eq4 = MathTex(r"\frac{\sin x}{\sin x}", r"\leq", r"\frac{x}{\sin x}", r"\leq", r"\frac{\tan x}{\sin x}", font_size=24)
        eq4.move_to(UP * 1.4)
        eq4[0].set_color(GREEN)
        eq4[2].set_color(PINK)
        eq4[4].set_color(BLUE)
        
        self.play(Write(eq4), run_time=1)
        self.wait(1)
        
        
        eq5 = MathTex(r"1", r"\leq", r"\frac{x}{\sin x}", r"\leq", r"\frac{1}{\cos x}", font_size=26)
        eq5.move_to(UP * 1.4)  
        eq5[0].set_color(GREEN)
        eq5[2].set_color(PINK)
        eq5[4].set_color(BLUE)
        
        self.play(Transform(eq4, eq5), run_time=1)
        self.wait(1)
        
        
        eq6 = MathTex(r"\cos x", r"\leq", r"\frac{\sin x}{x}", r"\leq", r"1", font_size=26)
        eq6.move_to(UP * 0.7)  
        eq6[0].set_color(BLUE)   
        eq6[2].set_color(PINK)   
        eq6[4].set_color(GREEN)  
        
        self.play(Write(eq6), run_time=1)
        self.wait(1)
        
        
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
        
        
        eq7 = MathTex(
            r"\lim_{x \to 0} \cos x \leq \lim_{x \to 0} \frac{\sin x}{x} \leq \lim_{x \to 0} 1",
            font_size=26
        )
        eq7.move_to(UP * 2)  
        eq7.set_color(YELLOW)
        
        self.play(Transform(eq6, eq7), run_time=1)
        self.wait(0.5)
        
        
        eq8 = MathTex(r"1 \leq \lim_{x \to 0} \frac{\sin x}{x} \leq 1", font_size=28)
        eq8.move_to(UP * 1.2)  
        eq8.set_color(GOLD)
        
        self.play(Write(eq8), run_time=1)
        self.wait(0.5)
        
        
        graph_axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[0, 1.2, 0.2],
            x_length=4,  
            y_length=2,  
            axis_config={"color": GRAY, "stroke_width": 1},
            tips=False
        ).shift(DOWN * 0.5)  
        
        
        def cos_func(x):
            if abs(x) < 0.001:  
                return 1
            return np.cos(x)
            
        def sinc_func(x):
            if abs(x) < 0.001:  
                return 1
            return np.sin(x) / x
            
        def one_func(x):
            return 1
        
        
        cos_graph = graph_axes.plot(cos_func, x_range=[-1.5, 1.5], color=BLUE, stroke_width=3)
        sinc_graph = graph_axes.plot(sinc_func, x_range=[-1.5, 1.5], color=PINK, stroke_width=3)
        one_graph = graph_axes.plot(one_func, x_range=[-1.5, 1.5], color=GREEN, stroke_width=3)
        
        
        cos_label = MathTex(r"\cos x", font_size=16, color=BLUE).next_to(graph_axes.c2p(-1.2, 0.5), UP)
        sinc_label = MathTex(r"\frac{\sin x}{x}", font_size=16, color=PINK).next_to(graph_axes.c2p(0, 1), UP + RIGHT, buff=0.1)
        one_label = MathTex(r"1", font_size=16, color=GREEN).next_to(graph_axes.c2p(1.2, 1), UP)
        
        
        vertical_line = DashedLine(
            graph_axes.c2p(0, 0), graph_axes.c2p(0, 1.1),
            color=WHITE, stroke_width=2
        )
        
        
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
        
        
        graph_elements = VGroup(graph_axes, cos_graph, sinc_graph, one_graph, cos_label, sinc_label, one_label, vertical_line)
        
        self.play(
            FadeOut(eq6),  
            FadeOut(graph_elements),  
            run_time=1
        )
        
        
        final_limit = MathTex(r"\lim_{x \to 0} \frac{\sin x}{x} = 1", font_size=48)
        final_limit.set_color_by_gradient(BLUE, RED)
        final_limit.move_to(ORIGIN)
        
        self.play(
            Transform(eq8, final_limit),
            run_time=2
        )
        
        self.wait(1)