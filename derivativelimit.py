from manim import *

class DerivativeAsLimit(Scene):
    def construct(self):
        
        self.camera.background_color = "#0a0a0a"  
        
        
        CURVE_COLOR = "#4a9eff"      
        TANGENT_COLOR = "#ff6b35"    
        SECANT_COLOR = "#00ff88"     
        POINT_COLOR = "#ffffff"      
        TEXT_COLOR = "#e8e8e8"       
        ACCENT_COLOR = "#ffd700"     
        
        
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=6,
            axis_config={
                "color": "#333333",
                "stroke_width": 2,
                "include_numbers": False,
                "include_tip": True
            }
        )
        
        
        def func(x):
            return x**2 * 0.5 + 0.5
        
        
        c = 2.0
        
        
        curve = axes.plot(
            func,
            x_range=[-0.5, 3.5],
            color=CURVE_COLOR,
            stroke_width=4
        )
        
        
        func_label = MathTex("f(x)", color=TEXT_COLOR, font_size=36)
        func_label.next_to(curve, UP + RIGHT, buff=0.5)
        
        
        point_c = axes.coords_to_point(c, func(c))
        main_point = Dot(point_c, color=POINT_COLOR, radius=0.08)
        try:
            main_point.set_glow_factor(2)
        except AttributeError:
            
            main_point.set_stroke(POINT_COLOR, width=2)
        
        
        x_coord_label = MathTex("c", color=TEXT_COLOR, font_size=24)
        y_coord_label = MathTex("f(c)", color=TEXT_COLOR, font_size=24)
        
        
        x_coord_label.next_to(axes.coords_to_point(c, 0), DOWN, buff=0.2)
        y_coord_label.next_to(axes.coords_to_point(0, func(c)), LEFT, buff=0.2)
        
        
        derivative_slope = c  
        tangent_line = axes.plot(
            lambda x: func(c) + derivative_slope * (x - c),
            x_range=[c - 1.5, c + 1.5],
            color=TANGENT_COLOR,
            stroke_width=3
        )
        
        
        self.wait(0.5)
        
        
        self.play(Create(axes), run_time=2)
        
        
        self.play(Create(curve), run_time=2.5)
        
        
        self.play(FadeIn(func_label), run_time=1)
        
        
        self.wait(1)
        
        
        self.wait(0.5)
        
        
        self.play(
            GrowFromCenter(main_point),
            run_time=1
        )
        
        
        self.play(
            FadeIn(x_coord_label),
            FadeIn(y_coord_label),
            run_time=1
        )
        
        
        self.play(Create(tangent_line), run_time=2)
        
        
        self.wait(0.5)
        
        
        
        
        h_initial = 1.2
        point_h_pos = axes.coords_to_point(c + h_initial, func(c + h_initial))
        second_point = Dot(point_h_pos, color=POINT_COLOR, radius=0.08)
        try:
            second_point.set_glow_factor(2)
        except AttributeError:
            
            second_point.set_stroke(POINT_COLOR, width=2)
        
        self.play(GrowFromCenter(second_point), run_time=1)
        
        
        secant_line = Line(
            point_c,
            point_h_pos,
            color=SECANT_COLOR,
            stroke_width=3
        )
        
        self.play(Create(secant_line), run_time=1)
        
        
        
        rise_line = DashedLine(
            point_h_pos,
            axes.coords_to_point(c + h_initial, func(c)),
            color=TEXT_COLOR,
            stroke_width=2
        )
        
        
        run_line = DashedLine(
            axes.coords_to_point(c + h_initial, func(c)),
            point_c,
            color=TEXT_COLOR,
            stroke_width=2
        )
        
        self.play(
            Create(rise_line),
            Create(run_line),
            run_time=1.5
        )
        
        
        slope_formula = MathTex(
            r"\frac{\Delta y}{\Delta x}",
            color=TEXT_COLOR,
            font_size=32
        )
        slope_formula.to_edge(UP + LEFT, buff=1)
        
        self.play(Write(slope_formula), run_time=1)
        
        self.wait(0.5)
        
        
        
        
        h_tracker = ValueTracker(h_initial)
        
        
        def update_second_point(mob):
            h_val = h_tracker.get_value()
            new_pos = axes.coords_to_point(c + h_val, func(c + h_val))
            mob.move_to(new_pos)
        
        def update_secant_line(mob):
            h_val = h_tracker.get_value()
            new_end = axes.coords_to_point(c + h_val, func(c + h_val))
            mob.put_start_and_end_on(point_c, new_end)
        
        def update_rise_line(mob):
            h_val = h_tracker.get_value()
            top_point = axes.coords_to_point(c + h_val, func(c + h_val))
            bottom_point = axes.coords_to_point(c + h_val, func(c))
            mob.put_start_and_end_on(top_point, bottom_point)
        
        def update_run_line(mob):
            h_val = h_tracker.get_value()
            right_point = axes.coords_to_point(c + h_val, func(c))
            mob.put_start_and_end_on(right_point, point_c)
        
        
        second_point.add_updater(update_second_point)
        secant_line.add_updater(update_secant_line)
        rise_line.add_updater(update_rise_line)
        run_line.add_updater(update_run_line)
        
        
        self.play(
            h_tracker.animate.set_value(0.01),
            run_time=6,
            rate_func=smooth
        )
        
        
        second_point.clear_updaters()
        secant_line.clear_updaters()
        rise_line.clear_updaters()
        run_line.clear_updaters()
        
        
        
        
        flash_color = ACCENT_COLOR
        
        
        self.play(
            secant_line.animate.set_color(TANGENT_COLOR),
            run_time=0.5
        )
        
        
        try:
            self.play(
                Flash(main_point, color=flash_color, flash_radius=0.3),
                run_time=0.5
            )
        except (AttributeError, TypeError):
            
            self.play(
                main_point.animate.set_color(flash_color),
                run_time=0.25
            )
            self.play(
                main_point.animate.set_color(POINT_COLOR),
                run_time=0.25
            )
        
        
        limit_definition = MathTex(
            r"f'(c) = \lim_{h \to 0} \frac{f(c+h) - f(c)}{h}",
            color=TEXT_COLOR,
            font_size=40
        )
        limit_definition.to_edge(DOWN, buff=1)
        
        
        limit_part = MathTex(
            r"\lim_{h \to 0}",
            color=ACCENT_COLOR,
            font_size=40
        )
        limit_part.move_to(limit_definition.get_part_by_tex(r"\lim_{h \to 0}"))
        
        self.play(Write(limit_definition), run_time=1.5)
        
        
        try:
            self.play(
                ReplacementTransform(limit_definition.get_part_by_tex(r"\lim_{h \to 0}"), limit_part),
                run_time=0.5
            )
        except AttributeError:
            
            self.play(
                limit_definition.animate.set_color(ACCENT_COLOR),
                run_time=0.5
            )
            self.play(
                limit_definition.animate.set_color(TEXT_COLOR),
                run_time=0.5
            )
        
        
        self.wait(1)
        
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )