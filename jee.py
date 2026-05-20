from manim import *
import numpy as np

class FourierJEE(Scene):
    def construct(self):
        # --- Config & Setup ---
        self.camera.background_color = "#101010"
        
        # --- 1. Static Elements ---
        
        # Title: "Good Luck" with Mathbb font (Gradient Blue to Red)
        title = Tex(r"$\mathbb{G}$ood $\mathbb{L}$uck", font_size=60)
        title.to_edge(UP, buff=0.9)
        title.set_color_by_gradient(BLUE, RED)
        
        # Bottom Text: "Share with a topper!" in a rounded translucent box
        bottom_text = Tex("Share with a topper!", color=PURPLE).scale(0.8)
        
        # Create the rounded box
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
        
        # Group text and box, position at bottom
        bottom_group = VGroup(bottom_box, bottom_text)
        bottom_group.to_edge(DOWN, buff=1.2)
        
        # Add static elements immediately
        self.add(title, bottom_group)

        # --- 2. Data Generation (Smooth JEE) ---
        # "JEE" centered at ORIGIN -> Moved UP (slightly down from 1.5)
        # Reduced Scale: font_size 200 -> 160
        dummy_jee = Text("JEE", font_size=160, weight=BOLD)
        dummy_jee.move_to(UP * 1.0)
        
        # Logic to sample points smoothly including gaps between letters
        points = []
        subpaths = dummy_jee.get_family()
        valid_paths = [m for m in subpaths if hasattr(m, "points") and len(m.points) > 0]
        
        # Increased Precision: 1500 -> 3000 -> 5000
        total_samples = 5000 
        raw_complex_points = []
        
        for i, path in enumerate(valid_paths):
            # Sample points along this letter
            num_points_in_letter = int(total_samples / len(valid_paths))
            for k in range(num_points_in_letter):
                alpha = k / num_points_in_letter
                pt = path.point_from_proportion(alpha)
                raw_complex_points.append(complex(pt[0], pt[1]))
            
            # Bridge gaps between letters (J -> E -> E) to prevent loops
            if i < len(valid_paths) - 1:
                start_pt = path.points[-1]
                end_pt = valid_paths[i+1].points[0]
                start_c = complex(start_pt[0], start_pt[1])
                end_c = complex(end_pt[0], end_pt[1])
                
                # Add transition points (invisible bridge)
                for j in range(50):
                    t = j / 50
                    interp = start_c * (1 - t) + end_c * t
                    raw_complex_points.append(interp)

        points = raw_complex_points
        
        # --- 3. Fourier Math ---
        N = len(points)
        # Increased Vectors: 100 -> 300 -> 500
        NUM_VECTORS = 500 
        
        coeffs = []
        for n in range(-NUM_VECTORS, NUM_VECTORS + 1):
            c_n = sum(points[k] * np.exp(-1j * 2 * np.pi * n * k / N) for k in range(N)) / N
            coeffs.append({"freq": n, "coeff": c_n})
            
        coeffs.sort(key=lambda x: abs(x["coeff"]), reverse=True)

        # --- 4. Animation Objects ---
        time_tracker = ValueTracker(0)
        
        # Start center
        center_c = coeffs[0]["coeff"] 
        center_point = [center_c.real, center_c.imag, 0]

        drawing_point = VectorizedPoint(center_point)
        
        # Path color: Teal/Cyan
        path = TracedPath(drawing_point.get_center, stroke_width=4, stroke_opacity=1, dissipating_time=None)
        path.set_color(TEAL) 
        
        # Text Stack below JEE
        # 1. Mains 2026
        mains_text = Tex(r"$\mathbb{M}$ains 2026", font_size=60)
        mains_text.set_color_by_gradient(BLUE, RED)
        mains_text.next_to(dummy_jee, DOWN, buff=0.3)
        
        # 2. Future IITians
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
                
                # Visuals
                if radius > 0.03: 
                    circle = Circle(radius=radius, color=WHITE, stroke_opacity=0.5, stroke_width=1)
                    circle.move_to([current_pos.real, current_pos.imag, 0])
                    circles.add(circle)
                
                # Vectors
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

        # --- 5. Execution ---
        # Animate faster (8 seconds)
        self.play(
            time_tracker.animate.set_value(0.99), 
            run_time=8, 
            rate_func=linear
        )
        
        # --- 6. Final Message ---
        # Fade out the machine (circles/vectors) but keep the drawn path
        self.play(FadeOut(epicycles_updater), run_time=1)
        
        # Prepare final message in box
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
        
        # Transform bottom text to final message
        self.play(
            Transform(bottom_group, final_group),
            run_time=1.5
        )
        
        self.wait(2)