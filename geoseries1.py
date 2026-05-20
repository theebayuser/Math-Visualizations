from manim import *
import numpy as np

class GeometricSeriesSquares(Scene):
    def construct(self):
        # Cool color scheme
        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PURPLE, PINK]
        
        # Initial question setup - series without equals
        series_part = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots")
        series_part.set_color_by_gradient(BLUE, RED)
        series_part.scale(1.2)
        series_part.move_to(ORIGIN)  # Start in center
        
        # Question text above and below - moved further apart
        why_text = Text("Why does", font="serif")
        why_text.scale(0.8)
        why_text.set_color(WHITE)
        why_text.next_to(series_part, UP, buff=0.6)  # Increased from 0.3 to 0.6
        
        equal_text = Text("equal 1?", font="serif")
        equal_text.scale(0.8)
        equal_text.set_color(WHITE)
        equal_text.next_to(series_part, DOWN, buff=0.6)  # Increased from 0.3 to 0.6
        
        # Full expression for later use
        full_expression = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots = 1")
        full_expression.set_color_by_gradient(BLUE, RED)
        full_expression.scale(1.2)
        full_expression.to_edge(UP, buff=0.2)
        
        # Dynamic equation that will build up with running sum - moved higher and made smaller
        dynamic_equation = MathTex("")
        dynamic_equation.move_to([0, 3.2, 0])  # Moved up from 2.5 to 3.2
        dynamic_equation.set_color_by_gradient(BLUE, RED)  # Same gradient as old title
        dynamic_equation.scale(0.7)  # Made smaller - reduced from 0.8 to 0.7
        
        # Create the main unit square
        unit_square = Square(side_length=4)
        unit_square.set_fill(opacity=0)
        unit_square.set_stroke(WHITE, width=2, opacity=0.5)
        unit_square.move_to([0, -0.5, 0])
        
        # Create clipping frame
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
        
        # Create squares for the geometric series
        squares = VGroup()
        labels = VGroup()
        
        # Keep track of terms and running sum
        terms = []
        running_sum = 0
        stop_adding_terms = False  # Flag to stop adding new terms after 1/1024
        
        # Main square dimensions
        size = 4
        base_y = -0.5
        
        # Define all square data
        square_data = [
            # First few squares
            {"width": size/2, "height": size, "pos": [-size/4, base_y, 0], "denom": 2, "scale": 1.0},
            {"width": size/2, "height": size/2, "pos": [size/4, base_y + size/4, 0], "denom": 4, "scale": 0.7},
            {"width": size/4, "height": size/2, "pos": [size/8, base_y - size/4, 0], "denom": 8, "scale": 0.5},
            {"width": size/4, "height": size/4, "pos": [3*size/8, base_y - size/8, 0], "denom": 16, "scale": 0.4},
            {"width": size/8, "height": size/4, "pos": [5*size/16, base_y - 3*size/8, 0], "denom": 32, "scale": 0.3},
            {"width": size/8, "height": size/8, "pos": [7*size/16, base_y - 5*size/16, 0], "denom": 64, "scale": 0.25},
        ]
        
        # Animation sequence - start with question
        question_group = VGroup(why_text, series_part, equal_text)
        self.play(Write(question_group), run_time=1.5, rate_func=smooth)  # Reduced from 2.0
        self.wait(1.0)  # Reduced from 1.5
        
        # Fade out the question faster
        self.play(FadeOut(question_group), run_time=0.8, rate_func=smooth)  # Reduced from 1.0
        self.wait(0.3)  # Reduced from 0.5
        
        self.play(Create(unit_square), run_time=1.2, rate_func=smooth)  # Reduced from 1.5
        self.wait(0.15)  # Reduced from 0.3
        
        # Function to update dynamic equation with running sum
        def update_equation(new_denom):
            nonlocal terms, running_sum, stop_adding_terms
            running_sum += 1/new_denom
            
            # Only add new terms until we reach 1/16
            if new_denom <= 16 and not stop_adding_terms:
                terms.append(f"\\frac{{1}}{{{new_denom}}}")
                if new_denom == 16:
                    stop_adding_terms = True
            
            # Build equation string
            if len(terms) == 0:
                equation_text = ""
            elif len(terms) == 1:
                equation_text = terms[0]
            else:
                equation_text = " + ".join(terms)
            
            # Add dots if we've stopped adding terms or have many terms
            if stop_adding_terms or len(terms) > 4:
                if len(terms) > 0:
                    equation_text += " + \\cdots"
            
            # Add equals and decimal value (remove trailing zeros)
            if equation_text:
                equation_text += f" = {running_sum:.6f}".rstrip('0').rstrip('.')
            
            new_equation = MathTex(equation_text)
            new_equation.move_to([0, 3.2, 0])  # Updated position
            new_equation.set_color_by_gradient(BLUE, RED)  # Same gradient as old title
            new_equation.scale(0.7)  # Made smaller - reduced from 0.8 to 0.7
            
            return new_equation
        
        # Animate squares one by one with equation updates - faster timing
        for i, data in enumerate(square_data):
            # Create square
            square = Rectangle(width=data["width"], height=data["height"])
            square.set_fill(colors[i % len(colors)], opacity=0.8)
            square.set_stroke(WHITE, width=1)
            square.move_to(data["pos"])
            
            # Create label
            label = MathTex(f"\\frac{{1}}{{{data['denom']}}}")
            label.move_to(square.get_center())
            label.set_color(WHITE)
            label.scale(data["scale"])
            
            squares.add(square)
            labels.add(label)
            
            # Show square growing from nothing
            square_copy = square.copy()
            square_copy.scale(0)
            square_copy.move_to(square.get_center())
            
            # Update equation
            new_equation = update_equation(data["denom"])
            
            # Animate square, label, and equation together with smoother timing
            animations = [
                ReplacementTransform(square_copy, square, rate_func=smooth),
                FadeIn(label, rate_func=smooth)
            ]
            
            if i == 0:
                animations.append(Write(new_equation))
                dynamic_equation = new_equation
            else:
                animations.append(Transform(dynamic_equation, new_equation))
            
            self.play(*animations, run_time=1.2 if i < 2 else 1.0)  # Slightly reduced
            self.wait(0.15 if i < 2 else 0.05)  # Reduced wait times
        
        # After creating the first set of squares
        self.wait(0.15)  # Further reduced
        
        # Add the clipping mask but keep equation as foreground element
        self.add_foreground_mobject(clipping_mask)
        self.add_foreground_mobject(dynamic_equation)
        
        # Zoom in - smoother and faster
        unit_square_bottom_right = [size/2, base_y - size/2, 0]
        zoom_factor = 4
        fixed_point = np.array(unit_square_bottom_right)
        
        zoom_group = VGroup(unit_square, squares, labels)
        
        self.play(
            zoom_group.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=1,  # Reduced from 1.5
            rate_func=smooth
        )
        self.wait(0.15)  # Reduced from 0.3
        
        # Second iteration of squares
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
        
        # Create and animate additional squares with equation updates - faster
        for i, data in enumerate(additional_square_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            # Boundary checking
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
                
                # Animate with equation update
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.6  # Reduced from 0.8
                )
                self.wait(0.05)  # Reduced from 0.1
        
        self.wait(0.1)  # Reduced from 0.2
        
        # Second zoom iteration
        zoom_group_2 = VGroup(unit_square, squares, labels, smaller_squares, smaller_labels)
        
        self.play(
            zoom_group_2.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=0.8,  # Reduced from 1.2
            rate_func=smooth
        )
        self.wait(0.1)  # Reduced from 0.2
        
        # Third iteration of squares
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
        
        # Create and animate third iteration squares with equation updates - even faster
        for i, data in enumerate(third_iteration_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            # Boundary checking
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
                
                # Animate with equation update
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.3  # Reduced from 0.6
                )
                self.wait(0.02)  # Reduced from 0.05
        
        # Show final sum approaching 1
        self.wait(0.05)  # Much reduced
        
        # Fourth zoom iteration - zoom in again on the remaining area
        zoom_group_3 = VGroup(unit_square, squares, labels, smaller_squares, smaller_labels, even_smaller_squares, even_smaller_labels)
        
        self.play(
            zoom_group_3.animate.scale(zoom_factor, about_point=fixed_point),
            run_time=0.6,  # Reduced from 1.0
            rate_func=smooth
        )
        self.wait(0.05)  # Reduced from 0.1
        
        # Fourth iteration of squares
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
        
        # Create and animate fourth iteration squares with equation updates - fastest
        for i, data in enumerate(fourth_iteration_data):
            pos_x, pos_y = data["pos"][0], data["pos"][1]
            width, height = data["width"], data["height"]
            
            # Boundary checking
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
                
                # Animate with equation update
                square_copy = square.copy()
                square_copy.scale(0)
                square_copy.move_to(square.get_center())
                
                new_equation = update_equation(data["denom"])
                
                self.play(
                    ReplacementTransform(square_copy, square, rate_func=smooth),
                    FadeIn(label, rate_func=smooth),
                    Transform(dynamic_equation, new_equation),
                    run_time=0.3  # Reduced from 0.4
                )
                self.wait(0.01)  # Minimal wait
        
        # Pause before zooming out
        self.wait(1)  # Reduced from 2.0
        
        # Zoom back out with soft ending speed ramp
        self.play(
            zoom_group_3.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            tiniest_squares.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            tiniest_labels.animate.scale(1/(zoom_factor*zoom_factor*zoom_factor), about_point=fixed_point),
            run_time=2,
            rate_func=lambda t: smooth(t) * (1 - 0.3 * (1 - smooth(t)))  # Soft ending ramp
        )
        
        # Remove the clipping mask
        self.remove_foreground_mobject(clipping_mask)
        
        # Final emphasis - change all squares to same color (no flashing)
        all_squares = VGroup(squares, smaller_squares, even_smaller_squares, tiniest_squares)
        self.play(
            all_squares.animate.set_fill(BLUE, opacity=0.8),
            unit_square.animate.set_stroke(GREEN, width=3, opacity=1),
            run_time=0.8,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Simple clean fade out of labels
        all_labels = VGroup(labels, smaller_labels, even_smaller_labels, tiniest_labels)
        
        self.play(
            FadeOut(all_labels),
            run_time=0.6,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Smooth transition from finite sum to infinite series
        self.play(
            dynamic_equation.animate.set_color(WHITE).scale(1.1),
            run_time=0.6
        )
        
        self.wait(0.2)
        
        # Fade out squares smoothly
        self.play(
            FadeOut(all_squares, unit_square),
            run_time=1,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Move equation down to center and transform to final summation - made smaller
        final_equation = MathTex(r"\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16} + \cdots = 1")
        final_equation.set_color_by_gradient(BLUE, RED)
        final_equation.scale(0.9)  # Reduced from 1.0 to make it smaller
        final_equation.move_to([0, -0.5, 0])  # Move down a bit from center
        
        self.play(
            Transform(dynamic_equation, final_equation),
            run_time=1.5,  # Reduced from 2.0
            rate_func=smooth
        )
        
        self.wait(1)  # Reduced from 2.0
        
        # Final fade out with smoother transition
        self.play(
            FadeOut(dynamic_equation),
            run_time=1,  # Increased from 0.8 for smoother fade
            rate_func=there_and_back_with_pause  # Smoother rate function
        )
        self.wait(0.3)  # Slightly increased wait