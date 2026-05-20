from manim import *
import numpy as np

class TrigFunctionsAnimation(Scene):
    def construct(self):
        
        self.camera.background_color = "#000000"
        
        
        title = MathTex(r"\mathbb{T}\text{rigonometric } \mathbb{F}\text{unctions}", font_size=52)
        title.set_color_by_gradient(BLUE, RED)  
        title.move_to(ORIGIN)  
        
        
        title_final_pos = title.copy()
        title_final_pos.scale(1)  
        title_final_pos.to_edge(UP, buff=0.1)  
        
        
        circle = Circle(radius=2, color=WHITE, stroke_width=2.5, stroke_opacity=0.9)
        circle.move_to([0, -0.7, 0])  
        
        
        axes_lines = VGroup(
            Line(LEFT * 3.5, RIGHT * 3.5, color=GRAY, stroke_width=1.5).move_to([0, -0.7, 0]),
            Line(DOWN * 3.5, UP * 3.5, color=GRAY, stroke_width=1.5).move_to([0, -0.7, 0])
        )
        
        
        X_MIN, X_MAX = -3.5, 3.5
        Y_MIN, Y_MAX = -4.2, 2.8  
        
        
        unit_marks = VGroup()
        unit_labels = VGroup()
        for i in [-2, 2]:
            unit_marks.add(Line([i, -0.8, 0], [i, -0.6, 0], color=LIGHT_GRAY, stroke_width=1.5))
            unit_marks.add(Line([-0.1, i - 0.7, 0], [0.1, i - 0.7, 0], color=LIGHT_GRAY, stroke_width=1.5))
            
            label_val = "1" if i > 0 else "-1"
            
            x_pos = i - 0.1 if i > 0 else i - 0.1  
            unit_labels.add(MathTex(label_val, font_size=16, color=WHITE).move_to([x_pos, -1.0, 0]))
            
            y_offset = -0.85 if i > 0 else -0.8  
            unit_labels.add(MathTex(label_val, font_size=16, color=WHITE).move_to([-0.3, i + y_offset, 0]))
        
        
        line_thickness = 4
        colors = {
            'point': "#00E066",      
            'sin': "#E6007A",        
            'cos': "#0099E6",        
            'radius': "#E6C200",     
            'tan': "#7A1FCC",        
            'sec': "#E63A00",        
            'cot': "#1FB34D",        
            'csc': "#E6529A"         
        }
        
        
        demo_angle = PI/4  
        
        
        cos_val = np.cos(demo_angle)
        sin_val = np.sin(demo_angle)
        
        
        circle_x = 2 * cos_val
        circle_y = 2 * sin_val - 0.7  
        circle_point = [circle_x, circle_y, 0]
        
        
        self.play(Write(title, run_time=1.5), rate_func=smooth)
        self.wait(0.5)  
        self.play(
            Transform(title, title_final_pos, run_time=1),
            rate_func=smooth
        )
        self.play(
            Create(axes_lines, run_time=1),
            Create(unit_marks, run_time=1),
            Write(unit_labels, run_time=1),
            rate_func=smooth
        )
        self.play(Create(circle, run_time=1.5), rate_func=smooth)
        self.wait(0.5)
        
        
        point = Dot(circle_point, radius=0.08, color=colors['point'])
        
        self.play(Create(point, run_time=0.5), rate_func=smooth)
        self.wait(0.3)
        
        
        
        sin_line = Line([circle_x, -0.7, 0], circle_point, stroke_width=line_thickness, color=colors['sin'])
        
        cos_line = Line([0, -0.7, 0], [circle_x, -0.7, 0], stroke_width=line_thickness, color=colors['cos'])
        
        
        self.play(
            Create(sin_line, run_time=1),
            Create(cos_line, run_time=1),
            rate_func=smooth
        )
        self.wait(0.3)
        
        
        size = 0.2
        main_right_angle = VGroup(
            Line([circle_x - size, -0.7, 0], [circle_x - size, size - 0.7, 0], color=WHITE, stroke_width=1.5),
            Line([circle_x - size, size - 0.7, 0], [circle_x, size - 0.7, 0], color=WHITE, stroke_width=1.5)
        )
        
        self.play(Create(main_right_angle, run_time=0.5), rate_func=smooth)
        self.wait(0.3)
        
        
        angle_tracker = ValueTracker(demo_angle)
        
        
        angle_counter_label = MathTex(r"\theta = ", font_size=24, color=WHITE)
        
        
        angle_counter = DecimalNumber(
            demo_angle * 180 / PI,  
            num_decimal_places=1,
            color=WHITE,
            font_size=24
        )
        degree_symbol = MathTex(r"^\circ", font_size=24, color=WHITE)
        
        
        angle_counter_group = VGroup(angle_counter_label, angle_counter, degree_symbol)
        angle_counter_group.arrange(RIGHT, buff=0.05)
        angle_counter_group.move_to([2.1, 1.5, 0])  
        
        
        def update_angle_counter(m):
            raw_angle = angle_tracker.get_value()
            normalized_angle = (raw_angle * 180 / PI) % 360  
            m.set_value(normalized_angle)
        angle_counter.add_updater(update_angle_counter)
        
        
        radius = Line([0, -0.7, 0], circle_point, stroke_width=line_thickness, color=colors['radius'])
        
        angle_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=demo_angle,
            stroke_width=3,
            color=WHITE,
            arc_center=[0, -0.7, 0]
        )
        
        
        angle_label = MathTex(r"\theta", font_size=20, color=WHITE).move_to([0.25, -0.55, 0])
        
        self.play(
            Create(radius, run_time=0.8),
            Create(angle_arc, run_time=0.8),
            Write(angle_label, run_time=0.8),
            Write(angle_counter_group, run_time=0.8),  
            rate_func=smooth
        )
        self.wait(0.3)
        
        
        sin_label = MathTex(r"\sin \theta", font_size=18, color=colors['sin']).move_to([circle_x + 0.3, circle_y/2 - 0.35, 0])
        cos_label = MathTex(r"\cos \theta", font_size=18, color=colors['cos']).move_to([circle_x/2, -1.0, 0])
        
        self.play(
            Write(sin_label, run_time=0.8),
            Write(cos_label, run_time=0.8),
            rate_func=smooth
        )
        self.wait(0.5)
        
        
        
        tan_x_intersection = 2 / cos_val
        tan_intersection = [tan_x_intersection, -0.7, 0]  
        
        tan_line = Line(circle_point, tan_intersection, stroke_width=line_thickness, color=colors['tan'])
        
        
        sec_y_offset = -0.9  
        sec_line = Line([0, sec_y_offset, 0], [tan_x_intersection, sec_y_offset, 0], stroke_width=line_thickness, color=colors['sec'])
        
        
        sec_vertical_left = DashedLine([0, -0.7, 0], [0, sec_y_offset, 0], stroke_width=line_thickness, color=colors['sec'], dash_length=0.05)
        sec_vertical_right = DashedLine([tan_x_intersection, -0.7, 0], [tan_x_intersection, sec_y_offset, 0], stroke_width=line_thickness, color=colors['sec'], dash_length=0.05)
        
        
        tan_label = MathTex(r"\tan \theta", font_size=18, color=colors['tan']).move_to([(circle_x + tan_x_intersection)/2 + 0.3, (circle_y - 0.7)/2, 0])
        sec_label = MathTex(r"\sec \theta", font_size=18, color=colors['sec']).move_to([tan_x_intersection/2, sec_y_offset - 0.15, 0])
        
        self.play(
            Create(tan_line, run_time=1),
            rate_func=smooth
        )
        self.play(
            Create(sec_line, run_time=1),
            Create(sec_vertical_left, run_time=0.8),
            Create(sec_vertical_right, run_time=0.8),
            Write(tan_label, run_time=0.8),
            Write(sec_label, run_time=0.8),
            rate_func=smooth
        )
        self.wait(0.5)
        
        
        cot_intersection_y = 2 / sin_val - 0.7  
        cot_intersection = [0, cot_intersection_y, 0]
        
        cot_line = Line(circle_point, cot_intersection, stroke_width=line_thickness, color=colors['cot'])
        csc_line = Line([0, -0.7, 0], cot_intersection, stroke_width=line_thickness, color=colors['csc'])
        
        
        cot_direction = np.array(cot_intersection) - np.array(circle_point)
        if np.linalg.norm(cot_direction) > 0:
            cot_direction = cot_direction / np.linalg.norm(cot_direction) * size
        radius_direction = np.array(circle_point) - np.array([0, -0.7, 0])
        if np.linalg.norm(radius_direction) > 0:
            radius_direction = radius_direction / np.linalg.norm(radius_direction) * size
        
        cot_right_angle = VGroup(
            Line(
                np.array(circle_point) - radius_direction,
                np.array(circle_point) - radius_direction + cot_direction,
                color=WHITE, stroke_width=1.5
            ),
            Line(
                np.array(circle_point) - radius_direction + cot_direction,
                np.array(circle_point) + cot_direction,
                color=WHITE, stroke_width=1.5
            )
        )
        
        
        cot_label = MathTex(r"\cot \theta", font_size=18, color=colors['cot']).move_to([(circle_x)/2 - 0.3, (circle_y + cot_intersection_y)/2, 0])
        csc_label = MathTex(r"\csc \theta", font_size=18, color=colors['csc']).move_to([-0.4, (cot_intersection_y - 0.7)/2, 0])
        
        self.play(
            Create(cot_line, run_time=1),
            Create(cot_right_angle, run_time=0.8),
            rate_func=smooth
        )
        self.play(
            Create(csc_line, run_time=1),
            Write(cot_label, run_time=0.8),
            Write(csc_label, run_time=0.8),
            rate_func=smooth
        )
        self.wait(1)
        
        
        def clip_line(start_point, end_point, x_min, x_max, y_min, y_max):
            """Clip line to stay within bounds and return visible portion"""
            x1, y1 = start_point[0], start_point[1]
            x2, y2 = end_point[0], end_point[1]
            
            
            if (x_min <= x1 <= x_max and y_min <= y1 <= y_max and 
                x_min <= x2 <= x_max and y_min <= y2 <= y_max):
                return start_point, end_point
            
            
            dx = x2 - x1
            dy = y2 - y1
            
            
            t_values = []
            
            if abs(dx) > 1e-10:  
                
                t = (x_min - x1) / dx
                if 0 <= t <= 1:
                    y = y1 + t * dy
                    if y_min <= y <= y_max:
                        t_values.append(t)
                
                
                t = (x_max - x1) / dx
                if 0 <= t <= 1:
                    y = y1 + t * dy
                    if y_min <= y <= y_max:
                        t_values.append(t)
            
            if abs(dy) > 1e-10:  
                
                t = (y_min - y1) / dy
                if 0 <= t <= 1:
                    x = x1 + t * dx
                    if x_min <= x <= x_max:
                        t_values.append(t)
                
                
                t = (y_max - y1) / dy
                if 0 <= t <= 1:
                    x = x1 + t * dx
                    if x_min <= x <= x_max:
                        t_values.append(t)
            
            
            t_values = sorted(set(t_values))
            
            
            start_inside = (x_min <= x1 <= x_max and y_min <= y1 <= y_max)
            end_inside = (x_min <= x2 <= x_max and y_min <= y2 <= y_max)
            
            if start_inside and end_inside:
                return start_point, end_point
            elif start_inside and t_values:
                t = t_values[0]
                clipped_end = [x1 + t * dx, y1 + t * dy, 0]
                return start_point, clipped_end
            elif end_inside and t_values:
                t = t_values[-1]
                clipped_start = [x1 + t * dx, y1 + t * dy, 0]
                return clipped_start, end_point
            elif len(t_values) >= 2:
                t1, t2 = t_values[0], t_values[-1]
                clipped_start = [x1 + t1 * dx, y1 + t1 * dy, 0]
                clipped_end = [x1 + t2 * dx, y1 + t2 * dy, 0]
                return clipped_start, clipped_end
            else:
                
                return None, None
        
        def get_dynamic_radius():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            new_point = [2 * c, 2 * s - 0.7, 0]
            return Line([0, -0.7, 0], new_point, stroke_width=line_thickness, color=colors['radius'])
        
        def get_dynamic_point():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            point_pos = [2 * c, 2 * s - 0.7, 0]
            return Dot(point_pos, radius=0.08, color=colors['point'])
        
        def get_dynamic_sin():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            return Line([2 * c, -0.7, 0], [2 * c, 2 * s - 0.7, 0], stroke_width=line_thickness, color=colors['sin'])
        
        def get_dynamic_cos():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            return Line([0, -0.7, 0], [2 * c, -0.7, 0], stroke_width=line_thickness, color=colors['cos'])
        
        def get_dynamic_angle_arc():
            angle = angle_tracker.get_value()
            normalized_angle = angle % (2 * PI)  
            return Arc(
                radius=0.5,
                start_angle=0,
                angle=normalized_angle,
                stroke_width=3,
                color=WHITE,
                arc_center=[0, -0.7, 0]
            )
        
        def get_dynamic_angle_label():
            return MathTex(r"\theta", font_size=20, color=WHITE).move_to([0.25, -0.55, 0])
        
        def get_dynamic_right_angle():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            size = 0.2
            
            x_offset = -size if c > 0 else size
            y_offset = size if s > 0 else -size
            return VGroup(
                Line([2 * c + x_offset, -0.7, 0], [2 * c + x_offset, y_offset - 0.7, 0], color=WHITE, stroke_width=1.5),
                Line([2 * c + x_offset, y_offset - 0.7, 0], [2 * c, y_offset - 0.7, 0], color=WHITE, stroke_width=1.5)
            )
        
        def get_dynamic_sin_label():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            
            mid_x = 2 * c
            mid_y = (-0.7 + (2 * s - 0.7)) / 2
            offset = 0.3 if c > 0 else -0.3
            return MathTex(r"\sin \theta", font_size=18, color=colors['sin']).move_to([mid_x + offset, mid_y, 0])
        
        def get_dynamic_cos_label():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            
            mid_x = c
            mid_y = -0.7
            offset = -0.3 if s > 0 else 0.3
            return MathTex(r"\cos \theta", font_size=18, color=colors['cos']).move_to([mid_x, mid_y + offset, 0])
        
        def get_dynamic_tan():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(c) > 0.01:  
                tan_x = 2 / c
                circle_point = [2 * c, 2 * s - 0.7, 0]
                tan_point = [tan_x, -0.7, 0]
                
                
                start, end = clip_line(circle_point, tan_point, X_MIN, X_MAX, Y_MIN, Y_MAX)
                if start is not None and end is not None:
                    return Line(start, end, stroke_width=line_thickness, color=colors['tan'])
            
            return Line(ORIGIN, ORIGIN, stroke_width=0, color=colors['tan'])
        
        def get_dynamic_sec():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(c) > 0.01:
                tan_x = 2 / c
                
                if s >= 0:  
                    sec_y_offset = -0.9  
                else:  
                    sec_y_offset = -0.5   
                
                start_point = [0, sec_y_offset, 0]
                end_point = [tan_x, sec_y_offset, 0]
                
                
                start, end = clip_line(start_point, end_point, X_MIN, X_MAX, Y_MIN, Y_MAX)
                if start is not None and end is not None:
                    return Line(start, end, stroke_width=line_thickness, color=colors['sec'])
            return Line(ORIGIN, ORIGIN, stroke_width=0, color=colors['sec'])
        
        def get_dynamic_sec_verticals():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(c) > 0.01:
                tan_x = 2 / c
                
                if X_MIN <= tan_x <= X_MAX:
                    
                    if s >= 0:  
                        sec_y_offset = -0.9  
                    else:  
                        sec_y_offset = -0.5   
                    
                    return VGroup(
                        DashedLine([0, -0.7, 0], [0, sec_y_offset, 0], stroke_width=line_thickness, color=colors['sec'], dash_length=0.05),
                        DashedLine([tan_x, -0.7, 0], [tan_x, sec_y_offset, 0], stroke_width=line_thickness, color=colors['sec'], dash_length=0.05)
                    )
            return VGroup()
        
        def get_dynamic_tan_label():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(c) > 0.01:
                tan_x = 2 / c
                if abs(tan_x) < 10:  
                    
                    circle_point = [2 * c, 2 * s - 0.7, 0]
                    tan_point = [tan_x, -0.7, 0]
                    mid_x = (circle_point[0] + tan_point[0]) / 2
                    mid_y = (circle_point[1] + tan_point[1]) / 2
                    
                    
                    if X_MIN <= mid_x <= X_MAX and Y_MIN <= mid_y <= Y_MAX:
                        
                        offset_x = 0.3 if c > 0 else -0.3
                        return MathTex(r"\tan \theta", font_size=18, color=colors['tan']).move_to([mid_x + offset_x, mid_y, 0])
            
            
            return MathTex(r"\tan \theta", font_size=18, color=colors['tan'], fill_opacity=0).move_to(ORIGIN)
        
        def get_dynamic_sec_label():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(c) > 0.01:
                tan_x = 2 / c
                if abs(tan_x) < 10:  
                    
                    if s >= 0:  
                        sec_y_offset = -0.9  
                    else:  
                        sec_y_offset = -0.5   
                    
                    mid_x = tan_x / 2
                    
                    
                    if X_MIN <= mid_x <= X_MAX and Y_MIN <= sec_y_offset <= Y_MAX:
                        label_y_offset = sec_y_offset - 0.15 if s >= 0 else sec_y_offset + 0.15
                        return MathTex(r"\sec \theta", font_size=18, color=colors['sec']).move_to([mid_x, label_y_offset, 0])
            
            
            return MathTex(r"\sec \theta", font_size=18, color=colors['sec'], fill_opacity=0).move_to(ORIGIN)
        
        def get_dynamic_cot():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(s) > 0.01:
                cot_y = 2 / s - 0.7
                circle_point = [2 * c, 2 * s - 0.7, 0]
                cot_point = [0, cot_y, 0]
                
                
                start, end = clip_line(circle_point, cot_point, X_MIN, X_MAX, Y_MIN, Y_MAX)
                if start is not None and end is not None:
                    return Line(start, end, stroke_width=line_thickness, color=colors['cot'])
            return Line(ORIGIN, ORIGIN, stroke_width=0, color=colors['cot'])
        
        def get_dynamic_csc():
            angle = angle_tracker.get_value()
            s = np.sin(angle)
            if abs(s) > 0.01:
                cot_y = 2 / s - 0.7
                start_point = [0, -0.7, 0]
                end_point = [0, cot_y, 0]
                
                
                start, end = clip_line(start_point, end_point, X_MIN, X_MAX, Y_MIN, Y_MAX)
                if start is not None and end is not None:
                    return Line(start, end, stroke_width=line_thickness, color=colors['csc'])
            return Line(ORIGIN, ORIGIN, stroke_width=0, color=colors['csc'])
        
        def get_dynamic_cot_right_angle():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(s) > 0.01:
                cot_y = 2 / s - 0.7
                
                if Y_MIN <= cot_y <= Y_MAX:
                    size = 0.2
                    circle_point = [2 * c, 2 * s - 0.7, 0]
                    cot_intersection = [0, cot_y, 0]
                    
                    cot_direction = np.array(cot_intersection) - np.array(circle_point)
                    if np.linalg.norm(cot_direction) > 0:
                        cot_direction = cot_direction / np.linalg.norm(cot_direction) * size
                    radius_direction = np.array(circle_point) - np.array([0, -0.7, 0])
                    if np.linalg.norm(radius_direction) > 0:
                        radius_direction = radius_direction / np.linalg.norm(radius_direction) * size
                    
                    return VGroup(
                        Line(
                            np.array(circle_point) - radius_direction,
                            np.array(circle_point) - radius_direction + cot_direction,
                            color=WHITE, stroke_width=1.5
                        ),
                        Line(
                            np.array(circle_point) - radius_direction + cot_direction,
                            np.array(circle_point) + cot_direction,
                            color=WHITE, stroke_width=1.5
                        )
                    )
            return VGroup()
        
        def get_dynamic_cot_label():
            angle = angle_tracker.get_value()
            c = np.cos(angle)
            s = np.sin(angle)
            if abs(s) > 0.01:
                cot_y = 2 / s - 0.7
                if Y_MIN + 0.5 <= cot_y <= Y_MAX - 0.5:  
                    
                    circle_point = [2 * c, 2 * s - 0.7, 0]
                    cot_point = [0, cot_y, 0]
                    mid_x = (circle_point[0] + cot_point[0]) / 2
                    mid_y = (circle_point[1] + cot_point[1]) / 2
                    
                    
                    if X_MIN <= mid_x <= X_MAX and Y_MIN <= mid_y <= Y_MAX:
                        
                        offset_x = -0.3 if c > 0 else 0.3
                        return MathTex(r"\cot \theta", font_size=18, color=colors['cot']).move_to([mid_x + offset_x, mid_y, 0])
            
            
            return MathTex(r"\cot \theta", font_size=18, color=colors['cot'], fill_opacity=0).move_to(ORIGIN)
        
        def get_dynamic_csc_label():
            angle = angle_tracker.get_value()
            s = np.sin(angle)
            if abs(s) > 0.01:
                cot_y = 2 / s - 0.7
                if Y_MIN + 0.5 <= cot_y <= Y_MAX - 0.5:  
                    
                    mid_y = (-0.7 + cot_y) / 2
                    
                    
                    if Y_MIN <= mid_y <= Y_MAX:
                        return MathTex(r"\csc \theta", font_size=18, color=colors['csc']).move_to([-0.4, mid_y, 0])
            
            
            return MathTex(r"\csc \theta", font_size=18, color=colors['csc'], fill_opacity=0).move_to(ORIGIN)
        
        
        dynamic_radius = always_redraw(get_dynamic_radius)
        dynamic_point = always_redraw(get_dynamic_point)
        dynamic_sin = always_redraw(get_dynamic_sin)
        dynamic_cos = always_redraw(get_dynamic_cos)
        dynamic_angle_arc = always_redraw(get_dynamic_angle_arc)
        dynamic_angle_label = always_redraw(get_dynamic_angle_label)
        dynamic_right_angle = always_redraw(get_dynamic_right_angle)
        dynamic_sin_label = always_redraw(get_dynamic_sin_label)
        dynamic_cos_label = always_redraw(get_dynamic_cos_label)
        dynamic_tan = always_redraw(get_dynamic_tan)
        dynamic_sec = always_redraw(get_dynamic_sec)
        dynamic_sec_verticals = always_redraw(get_dynamic_sec_verticals)
        dynamic_tan_label = always_redraw(get_dynamic_tan_label)
        dynamic_sec_label = always_redraw(get_dynamic_sec_label)
        dynamic_cot = always_redraw(get_dynamic_cot)
        dynamic_csc = always_redraw(get_dynamic_csc)
        dynamic_cot_right_angle = always_redraw(get_dynamic_cot_right_angle)
        dynamic_cot_label = always_redraw(get_dynamic_cot_label)
        dynamic_csc_label = always_redraw(get_dynamic_csc_label)
        
        
        static_elements = [radius, point, sin_line, cos_line, angle_arc, angle_label, 
                          main_right_angle, sin_label, cos_label, 
                          tan_line, sec_line, sec_vertical_left, sec_vertical_right, 
                          tan_label, sec_label, 
                          cot_line, csc_line, cot_right_angle, cot_label, csc_label]
        
        
        self.remove(*static_elements)
        self.add(dynamic_radius, dynamic_point, dynamic_sin, dynamic_cos, 
                dynamic_angle_arc, dynamic_angle_label, dynamic_right_angle,
                dynamic_sin_label, dynamic_cos_label, dynamic_tan, dynamic_sec, 
                dynamic_sec_verticals, dynamic_tan_label, 
                dynamic_sec_label, dynamic_cot, dynamic_csc, dynamic_cot_right_angle,
                dynamic_cot_label, dynamic_csc_label)
        
        
        self.wait(0.3)  
        
        
        
        total_rotation = 2 * PI
        rotation_time = 12
        
        self.play(
            angle_tracker.animate.set_value(demo_angle + total_rotation),
            rate_func=linear,  
            run_time=rotation_time
        )
        
        self.wait(1)
        
        
        all_elements = [
            title, axes_lines, unit_marks, unit_labels, circle,
            dynamic_radius, dynamic_point, dynamic_sin, dynamic_cos,
            dynamic_angle_arc, dynamic_angle_label, dynamic_right_angle,
            dynamic_sin_label, dynamic_cos_label, dynamic_tan, dynamic_sec,
            dynamic_sec_verticals, dynamic_tan_label, dynamic_sec_label,
            dynamic_cot, dynamic_csc, dynamic_cot_right_angle,
            dynamic_cot_label, dynamic_csc_label, angle_counter_group
        ]
        
        self.play(
            *[FadeOut(element) for element in all_elements],
            run_time=2
        )
        
        self.wait(1)