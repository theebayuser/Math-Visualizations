from manim import *
import numpy as np

class FourierJEE(Scene):
    def construct(self):
        
        self.camera.background_color = "#101010"
        
        
        
        
        title = Tex(r"$\mathbb{G}$ood $\mathbb{L}$uck", font_size=60)
        title.to_edge(UP, buff=0.9)
        title.set_color_by_gradient(BLUE, RED)
        
        
        bottom_text = Tex("Share with a topper!", color=PURPLE).scale(0.8)
        
        
        bottom_box = SurroundingRectangle(
            bottom_text, 
            corner_radius=0.2, 
            color=WHITE,
            fill_color="#222222", 
            fill_opacity=0.6,
            stroke_width=1,
            stroke_opacity=0.5,
            buff=0.2
        )
        
        
        bottom_group = VGroup(bottom_box, bottom_text)
        bottom_group.to_edge(DOWN, buff=1.2)
        
        
        self.add(title, bottom_group)

        
        
        
        dummy_jee = Text("JEE", font_size=160, weight=BOLD)
        dummy_jee.move_to(UP * 1.0)
        
        
        points = []
        subpaths = dummy_jee.get_family()
        valid_paths = [m for m in subpaths if hasattr(m, "points") and len(m.points) > 0]
        
        
        total_samples = 5000 
        raw_complex_points = []
        
        for i, path in enumerate(valid_paths):
            
            num_points_in_letter = int(total_samples / len(valid_paths))
            for k in range(num_points_in_letter):
                alpha = k / num_points_in_letter
                pt = path.point_from_proportion(alpha)
                raw_complex_points.append(complex(pt[0], pt[1]))
            
            
            if i < len(valid_paths) - 1:
                start_pt = path.points[-1]
                end_pt = valid_paths[i+1].points[0]
                start_c = complex(start_pt[0], start_pt[1])
                end_c = complex(end_pt[0], end_pt[1])
                
                
                for j in range(50):
                    t = j / 50
                    interp = start_c * (1 - t) + end_c * t
                    raw_complex_points.append(interp)

        points = raw_complex_points
        
        
        N = len(points)
        
        NUM_VECTORS = 500 
        
        coeffs = []
        for n in range(-NUM_VECTORS, NUM_VECTORS + 1):
            c_n = sum(points[k] * np.exp(-1j * 2 * np.pi * n * k / N) for k in range(N)) / N
            coeffs.append({"freq": n, "coeff": c_n})
            
        coeffs.sort(key=lambda x: abs(x["coeff"]), reverse=True)

        
        time_tracker = ValueTracker(0)
        
        
        center_c = coeffs[0]["coeff"] 
        center_point = [center_c.real, center_c.imag, 0]

        drawing_point = VectorizedPoint(center_point)
        
        
        path = TracedPath(drawing_point.get_center, stroke_width=4, stroke_opacity=1, dissipating_time=None)
        path.set_color(TEAL) 
        
        
        
        mains_text = Tex(r"$\mathbb{M}$ains 2026", font_size=60)
        mains_text.set_color_by_gradient(BLUE, RED)
        mains_text.next_to(dummy_jee, DOWN, buff=0.3)
        
        
        aspirants_text = Tex(r"$\mathbb{F}$uture $\mathbb{IIT}$ians", font_size=60)
        aspirants_text.set_color_by_gradient(BLUE, RED)
        aspirants_text.next_to(mains_text, DOWN, buff=0.45)
        
        self.add(mains_text, aspirants_text)

        def get_epicycles():
            t = time_tracker.get_value()
            vectors = VGroup()
            circles = VGroup()
            
            current_pos = complex(center_point[0], center_point[1])
            
            for item in coeffs:
                freq = item["freq"]
                c = item["coeff"]
                
                if freq == 0: continue
                
                radius = abs(c)
                phase = np.angle(c)
                angle = 2 * np.pi * freq * t + phase
                
                new_pos = current_pos + complex(radius * np.cos(angle), radius * np.sin(angle))
                
                
                if radius > 0.03: 
                    circle = Circle(radius=radius, color=WHITE, stroke_opacity=0.5, stroke_width=1)
                    circle.move_to([current_pos.real, current_pos.imag, 0])
                    circles.add(circle)
                
                
                vec_color = interpolate_color(BLUE_E, WHITE, len(vectors)/len(coeffs))
                line = Line(
                    start=[current_pos.real, current_pos.imag, 0], 
                    end=[new_pos.real, new_pos.imag, 0],
                    stroke_color=vec_color,
                    stroke_width=1.5
                )
                vectors.add(line)
                
                current_pos = new_pos
            
            drawing_point.move_to([current_pos.real, current_pos.imag, 0])
            return VGroup(circles, vectors)

        epicycles_updater = always_redraw(get_epicycles)
        
        self.add(path, epicycles_updater, drawing_point)

        
        
        self.play(
            time_tracker.animate.set_value(0.99), 
            run_time=8, 
            rate_func=linear
        )
        
        
        
        self.play(FadeOut(epicycles_updater), run_time=1)
        
        
        final_msg = Tex(r"Wishing you all a \\ successful exam!", color=PURPLE)
        final_box = SurroundingRectangle(
            final_msg,
            corner_radius=0.2,
            color=WHITE,
            fill_color="#222222",
            fill_opacity=0.6,
            stroke_width=1,
            stroke_opacity=0.5,
            buff=0.2
        )
        final_group = VGroup(final_box, final_msg)
        final_group.move_to(bottom_group.get_center())
        
        
        self.play(
            Transform(bottom_group, final_group),
            run_time=1.5
        )
        
        self.wait(2)