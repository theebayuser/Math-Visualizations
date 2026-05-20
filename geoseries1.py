from manim import *
import numpy as np

class GeometricSeriesSquares(Scene):
    def construct(self):
        
        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PURPLE, PINK]
        
        
        series_part = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots")
        series_part.set_color_by_gradient(BLUE, RED)
        series_part.scale(1.2)
        series_part.move_to(ORIGIN)  
        
        
        why_text = Text("Why does", font="serif")
        why_text.scale(0.8)
        why_text.set_color(WHITE)
        why_text.next_to(series_part, UP, buff=0.6)  
        
        equal_text = Text("equal 1?", font="serif")
        equal_text.scale(0.8)
        equal_text.set_color(WHITE)
        equal_text.next_to(series_part, DOWN, buff=0.6)  
        
        
        full_expression = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots = 1")
        full_expression.set_color_by_gradient(BLUE, RED)
        full_expression.scale(1.2)
        full_expression.to_edge(UP, buff=0.2)
        
        
        dynamic_equation = MathTex("")
        dynamic_equation.move_to([0, 3.2, 0])  
        dynamic_equation.set_color_by_gradient(BLUE, RED)  
        dynamic_equation.scale(0.7)  
        
        
        unit_square = Square(side_length=4)
        unit_square.set_fill(opacity=0)
        unit_square.set_stroke(WHITE, width=2, opacity=0.5)
        unit_square.move_to([0, -0.5, 0])
        
        
        frame_size = 20
        clipping_frame = Rectangle(width=frame_size, height=frame_size)
        clipping_frame.set_fill(BLACK, opacity=1)
        clipping_frame.set_stroke(opacity=0)
        clipping_frame.move_to([0, -0.5, 0])
        
        hole = Square(side_length=4)
        hole.set_fill(BLACK, opacity=1)
        hole.set_stroke(opacity=0)
        hole.move_to([0, -0.5, 0])
        
        clipping_mask = Difference(clipping_frame, hole)
        clipping_mask.set_fill(BLACK, opacity=1)
        clipping_mask.set_stroke(opacity=0)
        
        
        squares = VGroup()
        labels = VGroup()
        
        
        terms = []
        running_sum = 0
        stop_adding_terms = False  
        
        
        size = 4
        base_y = -0.5
        
        
        square_data = [
            
            {"width": size/2, "height": size, "pos": [-size/4, base_y, 0], "denom": 2, "scale": 1.0},
            {"width": size/2, "height": size/2, "pos": [size/4, base_y + size/4, 0], "denom": 4, "scale": 0.7},
            {"width": size/4, "height": size/2, "pos": [size/8, base_y - size/4, 0], "denom": 8, "scale": 0.5},
            {"width": size/4, "height": size/4, "pos": [3*size/8, base_y - size/8, 0], "denom": 16, "scale": 0.4},
            {"width": size/8, "height": size/4, "pos": [5*size/16, base_y - 3*size/8, 0], "denom": 32, "scale": 0.3},
            {"width": size/8, "height": size/8, "pos": [7*size/16, base_y - 5*size/16, 0], "denom": 64, "scale": 0.25},
        ]
        
        
        question_group = VGroup(why_text, series_part, equal_text)
        self.play(Write(question_group), run_time=1.5, rate_func=smooth)  
        self.wait(1.0)  
        
        
        self.play(FadeOut(question_group), run_time=0.8, rate_func=smooth)  
        self.wait(0.3)  
        
        self.play(Create(unit_square), run_time=1.2, rate_func=smooth)  
        self.wait(0.15)  
        
        
        def update_equation(new_denom):
            nonlocal terms, running_sum, stop_adding_terms
            running_sum += 1/new_denom
            
            
            if new_denom <= 16 and not stop_adding_terms:
                terms.append(f"\\frac{{1}}{{{new_denom}}}")
                if new_denom == 16:
                    stop_adding_terms = True
            
            
            if len(terms) == 0:
                equation_text = ""
            elif len(terms) == 1:
                equation_text = terms[0]
            else:
                equation_text = " + ".join(terms)
            
            
            if stop_adding_terms or len(terms) > 4:
                if len(terms) > 0:
                    equation_text += " + \\cdots"
            
            
            if equation_text:
                equation_text += f" = {running_sum:.6f}".rstrip('0').rstrip('.')
            
            new_equation = MathTex(equation_text)
            new_equation.move_to([0, 3.2, 0])  
            new_equation.set_color_by_gradient(BLUE, RED)  
            new_equation.scale(0.7)  
            
            return new_equation
        
        
        for i, data in enumerate(square_data):
            
            square = Rectangle(width=data["width"], height=data["height"])
            square.set_fill(colors[i % len(colors)], opacity=0.8)
            square.set_stroke(WHITE, width=1)
            square.move_to(data["pos"])
            
            
            label = MathTex(f"\\frac{{1}}{{{data['denom']}}}")
            label.move_to(square.get_center())
            label.set_color(WHITE)
            label.scale(data["scale"])
            
            squares.add(square)
            labels.add(label)
            
            
            square_copy = square.copy()
            square_copy.scale(0)
            square_copy.move_to(square.get_center())
            
            
            new_equation = update_equation(data["denom"])
            
            
            animations = [
                ReplacementTransform(square_copy, square, rate_func=smooth),
                FadeIn(label, rate_func=smooth)
            ]
            
            if i == 0:
                animations.append(Write(new_equation))
                dynamic_equation = new_equation
            else:
                animations.append(Transform(dynamic_equation, new_equation))
            
            self.play(*animations, run_time=1.2 if i < 2 else 1.0)  
            self.wait(0.15 if i < 2 else 0.05)  
        
        
        self.wait(0.15)  
        
        
        self.add_foreground_mobject(clipping_mask)
        self.add_foreground_mobject(dynamic_equation)
        
        
        unit_square_bottom_right = [size/2, base_y - size/2, 0]
        zoom_factor = 4
        fixed_point = np.array(unit_square_bottom_right)
        
        zoom_group = VGroup(unit_square, squares, labels)
        
        self.play(
            zoom_group.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=1,  
            rate_func=smooth
        )
        self.wait(0.15)  
        
        
        smaller_squares = VGroup()
        smaller_labels = VGroup()
        
        base_size = size/2
        remaining_area_center_x = size/2 - base_size/2
        remaining_area_center_y = base_y - size/2 + base_size/2
        
        additional_square_data = [
            {"width": base_size/2, "height": base_size, "pos": [remaining_area_center_x - base_size/4, remaining_area_center_y, 0], "denom": 128, "scale": 1.0},
            {"width": base_size/2, "height": base_size/2, "pos": [remaining_area_center_x + base_size/4, remaining_area_center_y + base_size/4, 0], "denom": 256, "scale": 0.7},
            {"width": base_size/4, "height": base_size/2, "pos": [remaining_area_center_x + base_size/8, remaining_area_center_y - base_size/4, 0], "denom": 512, "scale": 0.5},
            {"width": base_size/4, "height": base_size/4, "pos": [remaining_area_center_x + 3*base_size/8, remaining_area_center_y - base_size/8, 0], "denom": 1024, "scale": 0.4},
        ]
        
        
        for i, data in enumerate(additional_square_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            
            left = pos_x - width/2
            right = pos_x + width/2
            top = pos_y + height/2
            bottom = pos_y - height/2
            
            unit_left = -size/2
            unit_right = size/2
            unit_top = base_y + size/2
            unit_bottom = base_y - size/2
            
            if (left >= unit_left and right <= unit_right and 
                top <= unit_top and bottom >= unit_bottom):
                
                square = Rectangle(width=width, height=height)
                square.set_fill(colors[(i + 6) % len(colors)], opacity=0.8)
                square.set_stroke(WHITE, width=1)
                square.move_to([pos_x, pos_y, 0])
                
                label = MathTex(f"\\frac{{1}}{{{data['denom']}}}")
                label.move_to(square.get_center())
                label.set_color(WHITE)
                label.scale(data["scale"])
                
                smaller_squares.add(square)
                smaller_labels.add(label)
                
                
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.6  
                )
                self.wait(0.05)  
        
        self.wait(0.1)  
        
        
        zoom_group_2 = VGroup(unit_square, squares, labels, smaller_squares, smaller_labels)
        
        self.play(
            zoom_group_2.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=0.8,  
            rate_func=smooth
        )
        self.wait(0.1)  
        
        
        even_smaller_squares = VGroup()
        even_smaller_labels = VGroup()
        
        base_size_2 = size/2
        remaining_area_center_x_2 = size/2 - base_size_2/2
        remaining_area_center_y_2 = base_y - size/2 + base_size_2/2
        
        third_iteration_data = [
            {"width": base_size_2/2, "height": base_size_2, "pos": [remaining_area_center_x_2 - base_size_2/4, remaining_area_center_y_2, 0], "denom": 2048, "scale": 1.0},
            {"width": base_size_2/2, "height": base_size_2/2, "pos": [remaining_area_center_x_2 + base_size_2/4, remaining_area_center_y_2 + base_size_2/4, 0], "denom": 4096, "scale": 0.7},
            {"width": base_size_2/4, "height": base_size_2/2, "pos": [remaining_area_center_x_2 + base_size_2/8, remaining_area_center_y_2 - base_size_2/4, 0], "denom": 8192, "scale": 0.5},
            {"width": base_size_2/4, "height": base_size_2/4, "pos": [remaining_area_center_x_2 + 3*base_size_2/8, remaining_area_center_y_2 - base_size_2/8, 0], "denom": 16384, "scale": 0.4},
        ]
        
        
        for i, data in enumerate(third_iteration_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            
            left = pos_x - width/2
            right = pos_x + width/2
            top = pos_y + height/2
            bottom = pos_y - height/2
            
            unit_left = -size/2
            unit_right = size/2
            unit_top = base_y + size/2
            unit_bottom = base_y - size/2
            
            if (left >= unit_left and right <= unit_right and 
                top <= unit_top and bottom >= unit_bottom):
                
                square = Rectangle(width=width, height=height)
                square.set_fill(colors[(i + 2) % len(colors)], opacity=0.8)
                square.set_stroke(WHITE, width=1)
                square.move_to([pos_x, pos_y, 0])
                
                label = MathTex(f"\\frac{{1}}{{{data['denom']}}}")
                label.move_to(square.get_center())
                label.set_color(WHITE)
                label.scale(data["scale"])
                
                even_smaller_squares.add(square)
                even_smaller_labels.add(label)
                
                
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.3  
                )
                self.wait(0.02)  
        
        
        self.wait(0.05)  
        
        
        zoom_group_3 = VGroup(unit_square, squares, labels, smaller_squares, smaller_labels, even_smaller_squares, even_smaller_labels)
        
        self.play(
            zoom_group_3.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=0.6,  
            rate_func=smooth
        )
        self.wait(0.05)  
        
        
        tiniest_squares = VGroup()
        tiniest_labels = VGroup()
        
        base_size_3 = size/2
        remaining_area_center_x_3 = size/2 - base_size_3/2
        remaining_area_center_y_3 = base_y - size/2 + base_size_3/2
        
        fourth_iteration_data = [
            {"width": base_size_3/2, "height": base_size_3, "pos": [remaining_area_center_x_3 - base_size_3/4, remaining_area_center_y_3, 0], "denom": 32768, "scale": 1.0},
            {"width": base_size_3/2, "height": base_size_3/2, "pos": [remaining_area_center_x_3 + base_size_3/4, remaining_area_center_y_3 + base_size_3/4, 0], "denom": 65536, "scale": 0.7},
            {"width": base_size_3/4, "height": base_size_3/2, "pos": [remaining_area_center_x_3 + base_size_3/8, remaining_area_center_y_3 - base_size_3/4, 0], "denom": 131072, "scale": 0.5},
            {"width": base_size_3/4, "height": base_size_3/4, "pos": [remaining_area_center_x_3 + 3*base_size_3/8, remaining_area_center_y_3 - base_size_3/8, 0], "denom": 262144, "scale": 0.4},
        ]
        
        
        for i, data in enumerate(fourth_iteration_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            
            left = pos_x - width/2
            right = pos_x + width/2
            top = pos_y + height/2
            bottom = pos_y - height/2
            
            unit_left = -size/2
            unit_right = size/2
            unit_top = base_y + size/2
            unit_bottom = base_y - size/2
            
            if (left >= unit_left and right <= unit_right and 
                top <= unit_top and bottom >= unit_bottom):
                
                square = Rectangle(width=width, height=height)
                square.set_fill(colors[(i + 4) % len(colors)], opacity=0.8)
                square.set_stroke(WHITE, width=1)
                square.move_to([pos_x, pos_y, 0])
                
                label = MathTex(f"\\frac{{1}}{{{data['denom']}}}")
                label.move_to(square.get_center())
                label.set_color(WHITE)
                label.scale(data["scale"])
                
                tiniest_squares.add(square)
                tiniest_labels.add(label)
                
                
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.3  
                )
                self.wait(0.01)  
        
        
        self.wait(1)  
        
        
        self.play(
            zoom_group_3.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            tiniest_squares.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            tiniest_labels.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            run_time=2,
            rate_func=lambda t: smooth(t) * (1 - 0.3 * (1 - smooth(t)))  
        )
        
        
        self.remove_foreground_mobject(clipping_mask)
        
        
        all_squares = VGroup(squares, smaller_squares, even_smaller_squares, tiniest_squares)
        self.play(
            all_squares.animate.set_fill(BLUE, opacity=0.8),
            unit_square.animate.set_stroke(GREEN, width=3, opacity=1),
            run_time=0.8,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        
        all_labels = VGroup(labels, smaller_labels, even_smaller_labels, tiniest_labels)
        
        self.play(
            FadeOut(all_labels),
            run_time=0.6,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        
        self.play(
            dynamic_equation.animate.set_color(WHITE).scale(1.1),
            run_time=0.6
        )
        
        self.wait(0.2)
        
        
        self.play(
            FadeOut(all_squares, unit_square),
            run_time=1,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        
        final_equation = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots = 1")
        final_equation.set_color_by_gradient(BLUE, RED)
        final_equation.scale(0.9)  
        final_equation.move_to([0, -0.5, 0])  
        
        self.play(
            Transform(dynamic_equation, final_equation),
            run_time=1.5,  
            rate_func=smooth
        )
        
        self.wait(1)  
        
        
        self.play(
            FadeOut(dynamic_equation),
            run_time=1,  
            rate_func=there_and_back_with_pause  
        )
        self.wait(0.3)  