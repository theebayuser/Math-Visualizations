from manim import *
import numpy as np

class RiemannToIntegral(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        TITLE_COLOR = "#FF1744"          
        CURVE_COLOR = "#FFFFFF"          
        AXES_COLOR = "#FFFFFF"           
        RIEMANN_COLOR = "#00A8FF"        
        FORMULA_COLOR = "#00E5FF"        
        INTERVAL_COLOR = "#00D2D3"       
        VISUAL_COLOR_1 = "#FF6B35"       
        VISUAL_COLOR_2 = "#F7931E"       
        AREA_COLOR = "#9B59B6"           
        DEFINITION_COLOR = "#E74C3C"     
        
        
        title = MathTex(
            "\\mathbb{L}\\text{imit } \\mathbb{D}\\text{efinition of } \\mathbb{I}\\text{ntegral}",
            font_size=38,  
            color=TITLE_COLOR
        ).shift(UP * 2.8)  
        
        
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 2.5, 0.5],
            x_length=4.5,    
            y_length=2.8,    
            axis_config={
                "color": AXES_COLOR,  
                "stroke_width": 3,    
                "include_numbers": False,
                "tip_length": 0.15,   
                "font_size": 18
            }
        ).shift(UP * 0.2)  
        
        
        def func(x):
            return 0.2 * x**2 + 0.3
        
        
        curve = axes.plot(func, x_range=[0.5, 3.5], color=CURVE_COLOR, stroke_width=4)
        
        
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=1.0)
        self.play(Create(curve), run_time=1.0)
        
        
        a, b = 1, 3
        area_under_curve = axes.get_area(
            curve, 
            x_range=(a, b), 
            color=RIEMANN_COLOR, 
            opacity=0.25
        )
        
        
        a_label = MathTex("a", font_size=24, color=INTERVAL_COLOR).next_to(axes.c2p(a, 0), DOWN, buff=0.2)
        b_label = MathTex("b", font_size=24, color=INTERVAL_COLOR).next_to(axes.c2p(b, 0), DOWN, buff=0.2)
        
        self.play(
            FadeIn(area_under_curve),
            Write(a_label), Write(b_label),
            run_time=1.0
        )
        self.wait(0.5)
        
        
        n = 4
        dx = (b - a) / n
        
        
        rectangles = VGroup()
        
        assert axes.x_length is not None
        assert axes.y_length is not None
        for i in range(n):
            x_i = a + i * dx
            height = func(x_i)
            
            rect = Rectangle(
                width=dx * axes.x_length / (axes.x_range[1] - axes.x_range[0]),
                height=height * axes.y_length / (axes.y_range[1] - axes.y_range[0]),
                fill_color=RIEMANN_COLOR,
                fill_opacity=0.6,
                stroke_color=RIEMANN_COLOR,
                stroke_width=2
            ).move_to(axes.c2p(x_i + dx/2, height/2))
            rectangles.add(rect)
        
        
        riemann_formula = MathTex(
            "\\sum_{i=1}^{4} f(x_i) \\Delta x",
            font_size=36,
            color=FORMULA_COLOR
        ).shift(DOWN * 2.2)  
        
        
        rect_count = MathTex(
            f"{n} \\text{{ rectangles}}",
            font_size=28,
            color=FORMULA_COLOR
        ).shift(UP * 2.2)  
        
        
        self.play(
            *[DrawBorderThenFill(rect) for rect in rectangles],
            run_time=1.0
        )
        
        
        self.play(
            Write(riemann_formula),
            Write(rect_count),
            run_time=1.0
        )
        
        
        
        n_box = SurroundingRectangle(
            MathTex("4", font_size=36).move_to(riemann_formula.get_center()).shift(LEFT * 0.72 + UP * 0.48),
            color=FORMULA_COLOR, 
            stroke_width=2, 
            buff=0.05
        )
        
        
        line_to_formula = Line(
            rect_count.get_bottom(),
            n_box.get_top(),
            color=FORMULA_COLOR,
            stroke_width=3
        )
        
        self.play(
            Create(n_box),
            Create(line_to_formula),
            run_time=1.0
        )
        
        
        self.play(
            FadeOut(n_box),
            FadeOut(line_to_formula),
            FadeOut(rect_count),
            run_time=0.5
        )
        
        
        
        x_start = a + 2 * dx  
        delta_x_line = Line(
            axes.c2p(x_start, 0),
            axes.c2p(x_start + dx, 0),
            color=VISUAL_COLOR_1,
            stroke_width=4
        ).shift(DOWN*0.1)
        delta_x_label = MathTex("\\Delta x", font_size=24, color=VISUAL_COLOR_1).next_to(delta_x_line, DOWN, buff=0.1)
        
        
        x_i_point = Dot(axes.c2p(x_start, 0), color=VISUAL_COLOR_2, radius=0.05)
        f_xi_point = Dot(axes.c2p(x_start, func(x_start)), color=VISUAL_COLOR_2, radius=0.05)
        f_xi_line = DashedLine(
            axes.c2p(x_start, 0),
            axes.c2p(x_start, func(x_start)),
            color=VISUAL_COLOR_2,
            stroke_width=3
        )
        f_xi_label = MathTex("f(x_i)", font_size=24, color=VISUAL_COLOR_2).next_to(f_xi_line, LEFT, buff=0.1)
        
        
        delta_x_formula = MathTex(
            "\\Delta x = \\frac{b-a}{n}",
            font_size=28,
            color=VISUAL_COLOR_1
        ).next_to(axes, UP, buff=0.3).shift(LEFT * 1.5)
        
        f_xi_formula = MathTex(
            "x_i = a + i\\Delta x",
            font_size=28,
            color=VISUAL_COLOR_2
        ).next_to(delta_x_formula, RIGHT, buff=0.5)
        
        
        self.play(
            Create(delta_x_line),
            Write(delta_x_label),
            Write(delta_x_formula),
            run_time=1.0
        )
        
        
        self.play(
            Create(x_i_point),
            Create(f_xi_point),
            Create(f_xi_line),
            Write(f_xi_label),
            Write(f_xi_formula),
            run_time=1.0
        )
        
        
        
        f_xi_box = SurroundingRectangle(
            MathTex("f(x_i)", font_size=36).move_to(riemann_formula.get_center()).shift(LEFT * 0.05),
            color=VISUAL_COLOR_2, 
            stroke_width=2, 
            buff=0.03
        )
        
        
        delta_x_box = SurroundingRectangle(
            MathTex("\\Delta x", font_size=36).move_to(riemann_formula.get_center()).shift(RIGHT * 0.7),
            color=VISUAL_COLOR_1, 
            stroke_width=2, 
            buff=0.03
        )
        
        line_to_fxi = Line(
            f_xi_label.get_bottom(),
            f_xi_box.get_top(),
            color=VISUAL_COLOR_2,
            stroke_width=3
        )
        
        line_to_dx = Line(
            delta_x_label.get_bottom(),
            delta_x_box.get_top(),
            color=VISUAL_COLOR_1,
            stroke_width=3
        )
        
        self.play(
            Create(f_xi_box),
            Create(line_to_fxi),
            Create(delta_x_box),
            Create(line_to_dx),
            run_time=1.0
        )
        
        self.wait(0.5)
        
        
        visual_aids = VGroup(
            delta_x_line, delta_x_label, x_i_point, f_xi_point, 
            f_xi_line, f_xi_label, line_to_fxi, line_to_dx,
            f_xi_box, delta_x_box, delta_x_formula, f_xi_formula
        )
        
        self.play(FadeOut(visual_aids), run_time=1.0)
        
        
        
        all_stages = [8, 16, 32, 64, 128, 256, 512, 1024, "\\infty"]
        
        
        base_runtime = 1.2
        decay_factor = 0.75  
        
        for i, stage_n in enumerate(all_stages):
            
            runtime = base_runtime * (decay_factor ** i)
            
            
            new_rectangles = VGroup()
            
            if stage_n == "\\infty":
                
                actual_n = n
                new_dx = (b - a) / actual_n
                opacity = 0.6
                stroke_width = 2
            else:
                actual_n = stage_n
                new_dx = (b - a) / actual_n
                
                opacity = 0.6
                stroke_width = 2
            
            for j in range(actual_n):
                x_i = a + j * new_dx
                height = func(x_i)
                
                rect = Rectangle(
                    width=new_dx * axes.x_length / (axes.x_range[1] - axes.x_range[0]),
                    height=height * axes.y_length / (axes.y_range[1] - axes.y_range[0]),
                    fill_color=RIEMANN_COLOR,
                    fill_opacity=opacity,
                    stroke_color=RIEMANN_COLOR,
                    stroke_width=stroke_width
                ).move_to(axes.c2p(x_i + new_dx/2, height/2))
                new_rectangles.add(rect)
            
            
            new_formula = MathTex(
                f"\\sum_{{i=1}}^{{{stage_n}}} f(x_i) \\Delta x",
                font_size=36,
                color=FORMULA_COLOR
            ).shift(DOWN * 2.2)  
            
            
            if stage_n == "\\infty":
                
                self.play(
                    Transform(riemann_formula, new_formula),
                    run_time=runtime
                )
            else:
                
                self.play(
                    Transform(rectangles, new_rectangles),
                    Transform(riemann_formula, new_formula),
                    run_time=runtime
                )
            
            
            wait_time = max(0.05, 0.3 * (decay_factor ** i))
            self.wait(wait_time)
        
        
        
        self.wait(1.0)
        
        
        limit_formula = MathTex(
            "\\lim_{n \\to \\infty} \\sum_{i=1}^{n} f(x_i) \\Delta x",
            font_size=36,
            color=FORMULA_COLOR
        ).shift(DOWN * 2.2)  
        
        
        self.play(
            Transform(riemann_formula, limit_formula),
            run_time=1.0
        )
        
        
        self.wait(0.5)
        
        
        self.play(
            FadeOut(rectangles),
            run_time=1.0
        )
        
        
        
        final_area = axes.get_area(
            curve,
            x_range=(a, b),
            color=AREA_COLOR,
            opacity=0.8
        )
        
        
        integral_expression = MathTex(
            "= \\int_{a}^{b} f(x) \\, dx", 
            font_size=36, 
            color=AREA_COLOR
        ).next_to(limit_formula, DOWN, buff=0.3)  
        
        
        self.play(
            FadeIn(final_area),
            run_time=1.0
        )
        
        self.play(
            Write(integral_expression),
            run_time=1.0
        )
        
        
        
        final_definition = MathTex(
            "\\lim_{n \\to \\infty} \\sum_{i=1}^{n} f(x_i) \\Delta x = \\int_{a}^{b} f(x) \\, dx",
            font_size=32,
            color=DEFINITION_COLOR
        ).move_to(UP * 0.3)  
        
        
        definition_box = SurroundingRectangle(
            final_definition,
            color=DEFINITION_COLOR,
            stroke_width=3,
            buff=0.3
        )
        
        
        graph_objects = VGroup(
            axes, curve, final_area, area_under_curve,
            a_label, b_label, title
        )
        
        
        self.play(
            FadeOut(graph_objects),
            run_time=1.0
        )
        
        
        
        temp_full = MathTex(
            "\\lim_{n \\to \\infty} \\sum_{i=1}^{n} f(x_i) \\Delta x = \\int_{a}^{b} f(x) \\, dx",
            font_size=32
        ).move_to(UP * 0.3)
        
        temp_left = MathTex(
            "\\lim_{n \\to \\infty} \\sum_{i=1}^{n} f(x_i) \\Delta x",
            font_size=32
        ).move_to(UP * 0.3)
        
        temp_right = MathTex(
            "\\int_{a}^{b} f(x) \\, dx",
            font_size=32
        ).move_to(UP * 0.3)
        
        
        full_width = temp_full.get_width()
        left_width = temp_left.get_width()
        right_width = temp_right.get_width()
        
        
        left_target = UP * 0.3 + LEFT * (full_width/2 - left_width/2)
        
        
        
        equals_offset = 0.8  
        right_target = UP * 0.34 + RIGHT * (full_width/2 - right_width/2) * 0.88
        
        
        left_target_formula = MathTex(
            "\\lim_{n \\to \\infty} \\sum_{i=1}^{n} f(x_i) \\Delta x",
            font_size=32,
            color=FORMULA_COLOR
        ).move_to(left_target)
        
        right_target_formula = MathTex(
            "= \\int_{a}^{b} f(x) \\, dx",
            font_size=32,
            color=AREA_COLOR
        ).move_to(right_target)
        
        
        self.play(
            Transform(riemann_formula, left_target_formula),
            Transform(integral_expression, right_target_formula),
            run_time=1.0
        )
        
        
        self.play(
            FadeIn(final_definition),
            FadeOut(VGroup(riemann_formula, integral_expression)),
            run_time=1.0
        )
        
        
        self.play(
            Create(definition_box), 
            run_time=1.0
        )
        
        
        self.wait(2.0)
        
        
        self.play(
            FadeOut(VGroup(final_definition, definition_box)),
            run_time=1.0
        )
        
        self.wait(0.5)