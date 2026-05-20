from manim import *
import numpy as np

class RiemannApproximations(Scene):
    
    # --- Helper Functions ---
    def calculate_riemann_value(self, func, x_min, x_max, n, sample_type):
        """Calculate the numerical value of a Riemann sum."""
        dx = (x_max - x_min) / n
        total = 0
        
        if sample_type == "left":
            for i in range(n):
                x = x_min + i * dx
                total += func(x) * dx
        elif sample_type == "right":
            for i in range(n):
                x = x_min + (i + 1) * dx
                total += func(x) * dx
        elif sample_type == "center":
            for i in range(n):
                x = x_min + (i + 0.5) * dx
                total += func(x) * dx
        elif sample_type == "trapezoid":
            for i in range(n):
                x_left = x_min + i * dx
                x_right = x_min + (i + 1) * dx
                total += (func(x_left) + func(x_right)) / 2 * dx
        
        return total
    
    def get_riemann_equation(self, sample_type, n, value, x_min, x_max):
        """Generate the full Riemann sum equation for each type."""
        dx = (x_max - x_min) / n
        
        if sample_type == "left":
            eq = MathTex(
                r"\sum_{i=0}^{" + str(n-1) + r"} f(x_i) \Delta x \approx " + f"{value:.2f}",
                font_size=16
            )
        elif sample_type == "right":
            eq = MathTex(
                r"\sum_{i=1}^{" + str(n) + r"} f(x_i) \Delta x \approx " + f"{value:.2f}",
                font_size=16
            )
        elif sample_type == "center":
            eq = MathTex(
                r"\sum_{i=0}^{" + str(n-1) + r"} f(x_i + \frac{\Delta x}{2}) \Delta x \approx " + f"{value:.2f}",
                font_size=16
            )
        else:  # trapezoid
            eq = MathTex(
                r"\sum_{i=0}^{" + str(n-1) + r"} \frac{f(x_i) + f(x_{i+1})}{2} \Delta x \approx " + f"{value:.2f}",
                font_size=14
            )
        
        return eq
    
    def get_riemann_sum(self, axes, graph, x_min, x_max, n, sample_type, color):
        """
        Creates a VGroup for a Riemann sum.
        sample_type can be 'left', 'right', 'center', or 'trapezoid'.
        """
        dx = (x_max - x_min) / n
        sum_group = VGroup()
        
        if sample_type == "trapezoid":
            # Manually create VGroup of trapezoids
            x_coords = np.arange(x_min, x_max, dx)
            if x_coords[-1] < x_max - (dx * 0.01):
                 x_coords = np.append(x_coords, x_max - dx)

            for x_start in x_coords:
                x_end = min(x_start + dx, x_max)
                
                y_start = graph.underlying_function(x_start)
                y_end = graph.underlying_function(x_end)
                
                p1 = axes.c2p(x_start, 0)
                p2 = axes.c2p(x_start, y_start)
                p3 = axes.c2p(x_end, y_end)
                p4 = axes.c2p(x_end, 0)
                
                trapezoid = Polygon(
                    p1, p2, p3, p4,
                    stroke_width=1,
                    stroke_color=WHITE,
                    fill_opacity=0.7,
                    color=color
                )
                sum_group.add(trapezoid)
        else:
            sum_group = axes.get_riemann_rectangles(
                graph,
                x_range=[x_min, x_max],
                dx=dx,
                input_sample_type=sample_type,
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=0.7,
                color=color
            )
            
        return sum_group

    def construct(self):
        # --- Config ---
        self.camera.background_color = BLACK
        
        # Define colors for each type
        LEFT_COLOR = BLUE_C
        RIGHT_COLOR = GREEN_C
        MID_COLOR = YELLOW_C
        TRAP_COLOR = MAROON_C
        CURVE_COLOR = WHITE
        
        # Define the math
        x_min, x_max = 0, 4
        
        # New function with larger variation - exponential with sin
        def func(x):
            return 2 + 3 * np.sin(2 * x) + 0.5 * x

        # --- Title ---
        title = Tex(r"$\mathbb{R}$iemann $\mathbb{A}$pproximations", font_size=44)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.3)

        # --- Create 2x2 Grid with smaller axes ---
        ax_config = {
            "x_range": [0, 5, 1],
            "y_range": [0, 7, 2],
            "x_length": 2.2,
            "y_length": 1.4,
            "axis_config": {"include_tip": False, "color": GRAY_A, "font_size": 20}
        }
        
        ax_l = Axes(**ax_config)
        ax_r = Axes(**ax_config)
        ax_m = Axes(**ax_config)
        ax_t = Axes(**ax_config)

        # Arrange in tighter grid with bottom row moved down
        grid = VGroup(
            VGroup(ax_l, ax_r).arrange(RIGHT, buff=0.5),
            VGroup(ax_m, ax_t).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, buff=2.0).scale(0.8)
        grid.move_to(ORIGIN).shift(UP*0.5)

        # Create graphs
        graph_l = ax_l.plot(func, x_range=[x_min, x_max], color=CURVE_COLOR)
        graph_r = ax_r.plot(func, x_range=[x_min, x_max], color=CURVE_COLOR)
        graph_m = ax_m.plot(func, x_range=[x_min, x_max], color=CURVE_COLOR)
        graph_t = ax_t.plot(func, x_range=[x_min, x_max], color=CURVE_COLOR)
        
        all_axes = VGroup(ax_l, ax_r, ax_m, ax_t)
        all_graphs = VGroup(graph_l, graph_r, graph_m, graph_t)

        # Add labels - align them all at the same height
        label_l = Tex("Left Riemann", font_size=28)
        label_r = Tex("Right Riemann", font_size=28)
        label_m = Tex("Midpoint Riemann", font_size=28)
        label_t = Tex("Trapezoid Rule", font_size=28)
        
        # Position labels at the same height
        label_l.next_to(ax_l, UP, buff=0.2)
        label_r.next_to(ax_r, UP, buff=0.2)
        label_m.next_to(ax_m, UP, buff=0.2)
        label_t.next_to(ax_t, UP, buff=0.2)
        
        # Align all labels to the same y-coordinate
        target_y = label_r.get_y()
        label_l.set_y(target_y)
        label_m.set_y(label_t.get_y())
        
        all_labels = VGroup(label_l, label_r, label_m, label_t)
        
        # Create initial equation labels
        eq_l = MathTex(r"\sum f(x_i) \Delta x", font_size=16).next_to(ax_l, DOWN, buff=0.2)
        eq_r = MathTex(r"\sum f(x_i) \Delta x", font_size=16).next_to(ax_r, DOWN, buff=0.2)
        eq_m = MathTex(r"\sum f(x_i) \Delta x", font_size=16).next_to(ax_m, DOWN, buff=0.2)
        eq_t = MathTex(r"\sum f(x_i) \Delta x", font_size=16).next_to(ax_t, DOWN, buff=0.2)
        all_equations = VGroup(eq_l, eq_r, eq_m, eq_t)
        
        # Calculate the actual integral value
        from scipy import integrate
        actual_value, _ = integrate.quad(func, x_min, x_max)
        
        # Create integral expression below the bottom row of graphs
        integral_eq = MathTex(
            r"\int_{0}^{4} \left(2 + 3\sin(2x) + 0.5x\right) dx = " + f"{actual_value:.4f}",
            font_size=24
        )
        # Position it below the center of the bottom two graphs
        bottom_center = VGroup(ax_m, ax_t).get_center()
        integral_eq.next_to(VGroup(ax_m, ax_t), DOWN, buff=0.85)
        integral_eq.set_x(bottom_center[0])
        
        # --- Animation Sequence ---
        # Add everything at the start
        self.add(
            title,
            *all_axes,
            *all_graphs,
            *all_labels,
            *all_equations,
            integral_eq
        )
        
        # --- n = 4 ---
        n_4 = 4
        sums_n4 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_4, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_4, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_4, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_4, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(*[Create(s) for s in sums_n4], run_time=1.5)
        
        # Update equations for n=4
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_4, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_4, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_4, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_4, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_4, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_4, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_4, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_4, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.7
        )
        self.wait(1.0)
        
        # --- n = 8 ---
        n_8 = 8
        sums_n8 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_8, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_8, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_8, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_8, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(ReplacementTransform(sums_n4, sums_n8), run_time=1.0)
        
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_8, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_8, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_8, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_8, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_8, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_8, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_8, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_8, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.3
        )
        self.wait(0.1)
        
        # --- n = 16 ---
        n_16 = 16
        sums_n16 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_16, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_16, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_16, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_16, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(ReplacementTransform(sums_n8, sums_n16), run_time=1.0)
        
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_16, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_16, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_16, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_16, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_16, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_16, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_16, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_16, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.3
        )
        self.wait(0.1)

        # --- n = 32 ---
        n_32 = 32
        sums_n32 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_32, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_32, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_32, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_32, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(ReplacementTransform(sums_n16, sums_n32), run_time=0.8)
        
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_32, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_32, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_32, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_32, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_32, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_32, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_32, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_32, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.25
        )
        self.wait(0.1)
        
        # --- n = 64 ---
        n_64 = 64
        sums_n64 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_64, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_64, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_64, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_64, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(ReplacementTransform(sums_n32, sums_n64), run_time=0.6)
        
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_64, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_64, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_64, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_64, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_64, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_64, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_64, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_64, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.2
        )
        self.wait(0.1)
        
        # --- n = 128 ---
        n_128 = 128
        sums_n128 = VGroup(
            self.get_riemann_sum(ax_l, graph_l, x_min, x_max, n_128, 'left', LEFT_COLOR),
            self.get_riemann_sum(ax_r, graph_r, x_min, x_max, n_128, 'right', RIGHT_COLOR),
            self.get_riemann_sum(ax_m, graph_m, x_min, x_max, n_128, 'center', MID_COLOR),
            self.get_riemann_sum(ax_t, graph_t, x_min, x_max, n_128, 'trapezoid', TRAP_COLOR)
        )
        
        self.play(ReplacementTransform(sums_n64, sums_n128), run_time=0.4)
        
        val_l = self.calculate_riemann_value(func, x_min, x_max, n_128, 'left')
        val_r = self.calculate_riemann_value(func, x_min, x_max, n_128, 'right')
        val_m = self.calculate_riemann_value(func, x_min, x_max, n_128, 'center')
        val_t = self.calculate_riemann_value(func, x_min, x_max, n_128, 'trapezoid')
        
        new_eq_l = self.get_riemann_equation('left', n_128, val_l, x_min, x_max).next_to(ax_l, DOWN, buff=0.2)
        new_eq_r = self.get_riemann_equation('right', n_128, val_r, x_min, x_max).next_to(ax_r, DOWN, buff=0.2)
        new_eq_m = self.get_riemann_equation('center', n_128, val_m, x_min, x_max).next_to(ax_m, DOWN, buff=0.2)
        new_eq_t = self.get_riemann_equation('trapezoid', n_128, val_t, x_min, x_max).next_to(ax_t, DOWN, buff=0.2)
        
        self.play(
            Transform(eq_l, new_eq_l),
            Transform(eq_r, new_eq_r),
            Transform(eq_m, new_eq_m),
            Transform(eq_t, new_eq_t),
            run_time=0.1
        )
        self.wait(0.1)

        # --- n = Infinity (Smooth Area) ---
        areas = VGroup(
            ax_l.get_area(graph_l, x_range=[x_min, x_max], color=LEFT_COLOR, opacity=0.7),
            ax_r.get_area(graph_r, x_range=[x_min, x_max], color=RIGHT_COLOR, opacity=0.7),
            ax_m.get_area(graph_m, x_range=[x_min, x_max], color=MID_COLOR, opacity=0.7),
            ax_t.get_area(graph_t, x_range=[x_min, x_max], color=TRAP_COLOR, opacity=0.7)
        )
        
        self.play(
            FadeOut(sums_n128),
            FadeIn(areas),
            run_time=0.8
        )
        
        self.wait(1)
        
        self.play(FadeOut(*self.mobjects), run_time=1)