from manim import *

class BezierCurves(Scene):
    def construct(self):
        S = 0.75 
        dy = -0.2 

        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            x_length=5.5, 
            y_length=7,
            background_line_style={
                "stroke_opacity": 0.25, 
                "stroke_color": "#00FFCC"
            },
            faded_line_ratio=1
        ).shift(DOWN * 0.5)

        title = MathTex(r"\mathbb{B}\text{ezier}\ \mathbb{C}\text{urves}", font_size=45)
        title.set_color_by_gradient("#FF007F", "#FFD700").to_edge(UP, buff=0.2)
        
        subtitle = MathTex(r"\text{Ever wonder how computers draw curves?}", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.2)

        def get_bezier_point(pts, t_val):
            current = list(pts)
            while len(current) > 1:
                current = [interpolate(current[i], current[i+1], t_val) for i in range(len(current)-1)]
            return current[0]

        def create_bezier_system(ctrl_points, t_tracker, path_color=RED, path_width=8, glow_opac=0.25):
            def get_frame():
                group = VGroup()
                current_pts = ctrl_points
                colors = [WHITE, "#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF4500", "#FF007F"]
                
                for i in range(len(current_pts)-1):
                    group.add(Line(current_pts[i], current_pts[i+1], color=LIGHT_GREY, stroke_width=4.0, stroke_opacity=1.0))
                    group.add(Dot(current_pts[i], color=WHITE, radius=0.06))
                group.add(Dot(current_pts[-1], color=WHITE, radius=0.06))

                lvl = 1
                val = t_tracker.get_value()

                while len(current_pts) > 1:
                    next_pts = [interpolate(current_pts[i], current_pts[i+1], val) for i in range(len(current_pts)-1)]
                    for i in range(len(next_pts)-1):
                        group.add(Line(next_pts[i], next_pts[i+1], color=colors[lvl % len(colors)], stroke_width=2.5, stroke_opacity=0.75))
                    for p in next_pts:
                        if len(next_pts) == 1:
                            group.add(Dot(p, color=path_color, radius=0.12)) 
                        else:
                            group.add(Dot(p, color=colors[lvl % len(colors)], radius=0.05))
                    current_pts = next_pts
                    lvl += 1
                return group

            dynamic_mobs = always_redraw(get_frame)
            
            tracer_dot = Dot(radius=0).add_updater(
                lambda m: m.move_to(get_bezier_point(ctrl_points, t_tracker.get_value()))
            )
            
            path = TracedPath(tracer_dot.get_center, stroke_color=path_color, stroke_width=path_width)
            glow = TracedPath(tracer_dot.get_center, stroke_color=path_color, stroke_width=path_width*2.5, stroke_opacity=glow_opac)

            return VGroup(dynamic_mobs, tracer_dot, path, glow)

        def create_ui_box(text, y_pos, is_math=False, box_width=4.2, box_height=0.55):
            box = RoundedRectangle(
                corner_radius=0.2, width=box_width, height=box_height, 
                color=BLUE, stroke_width=2.5, fill_opacity=0.85, fill_color=BLACK
            )
            if is_math:
                content = MathTex(text, font_size=18, color="#FFFF00")
            else:
                content = MathTex(rf"\text{{{text}}}", font_size=18, color=WHITE)
            return VGroup(box, content).move_to(UP * (y_pos + dy))

        pts_quad = [np.array([-1.8*S, 1.0*S+dy, 0]), np.array([0, 2.5*S+dy, 0]), np.array([1.8*S, 1.0*S+dy, 0])]
        pts_cubic = [np.array([-2.0*S, -2.6*S+dy, 0]), np.array([-1.0*S, -1.0*S+dy, 0]), np.array([1.0*S, -2.6*S+dy, 0]), np.array([2.0*S, -1.0*S+dy, 0])]

        t_tracker1 = ValueTracker(0)
        sys_quad = create_bezier_system(pts_quad, t_tracker1, path_color="#FF3366")
        sys_cubic = create_bezier_system(pts_cubic, t_tracker1, path_color="#00FFCC")

        lbl_quad = create_ui_box("Quadratic", y_pos=2.6, box_width=2.5)
        eq_quad = create_ui_box(r"P(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2", y_pos=0.4, is_math=True, box_width=4.0)
        
        lbl_cubic = create_ui_box("Cubic", y_pos=-0.3, box_width=2.5)
        eq_cubic = create_ui_box(r"P(t) = (1-t)^3 P_0 + 3(1-t)^2t P_1 + 3(1-t)t^2 P_2 + t^3 P_3", y_pos=-2.6, is_math=True, box_width=4.8)

        self.add(grid, title, sys_quad, sys_cubic, lbl_quad, eq_quad, lbl_cubic, eq_cubic)

        self.play(
            Write(subtitle, run_time=0.8),
            t_tracker1.animate(run_time=3.0, rate_func=linear).set_value(1)
        )
        self.wait(0.2)
        self.play(FadeOut(lbl_quad, eq_quad, sys_quad, lbl_cubic, eq_cubic, sys_cubic, shift=DOWN*0.2, run_time=0.2))

        pts_deg5 = [
            np.array([-2.2*S, -1.5*S+dy, 0]), np.array([-1.4*S, 2.4*S+dy, 0]), np.array([-0.5*S, -2.4*S+dy, 0]),
            np.array([0.5*S, 2.4*S+dy, 0]), np.array([1.4*S, -2.4*S+dy, 0]), np.array([2.2*S, -0.5*S+dy, 0])
        ]
        
        t_tracker2 = ValueTracker(0)
        sys_deg5 = create_bezier_system(pts_deg5, t_tracker2, path_color="#B026FF")
        
        lbl_deg5 = create_ui_box("Degree 5", y_pos=2.6, box_width=2.5)
        eq_deg5 = create_ui_box(r"P(t) = \sum_{i=0}^{5} \binom{5}{i} (1-t)^{5-i} t^i P_i", y_pos=-2.6, is_math=True, box_width=4.0, box_height=0.8)

        self.play(FadeIn(lbl_deg5, eq_deg5, sys_deg5, shift=UP*0.2, run_time=0.2))
        self.play(t_tracker2.animate(run_time=3.0, rate_func=linear).set_value(1))
        self.wait(0.2)
        
        self.play(FadeOut(lbl_deg5, eq_deg5, sys_deg5, shift=DOWN*0.2, run_time=0.2))

        S2 = 0.55 
        pts_knot = [
            np.array([0, dy, 0]), 
            np.array([-4*S2, 3.5*S2+dy, 0]), np.array([-4*S2, -3.5*S2+dy, 0]), 
            np.array([0, dy, 0]), 
            np.array([4*S2, 3.5*S2+dy, 0]), np.array([4*S2, -3.5*S2+dy, 0]), 
            np.array([0, dy, 0])
        ]
        
        t_tracker3 = ValueTracker(0)
        sys_knot = create_bezier_system(pts_knot, t_tracker3, path_color="#FFD700")
        lbl_knot = create_ui_box("Degree 6: Infinity Knot", y_pos=2.6, box_width=3.5)
        
        self.play(FadeIn(lbl_knot, sys_knot, shift=UP*0.2, run_time=0.2))
        self.play(t_tracker3.animate(run_time=3.5, rate_func=linear).set_value(1))
        self.wait(0.2)

        self.play(FadeOut(lbl_knot, sys_knot, shift=DOWN*0.2, run_time=0.2))

        bg_circle = Circle(radius=2.0, color="#1ED760", fill_opacity=1.0).shift(UP * dy)
        lbl_spotify = create_ui_box("Spotify Logo", y_pos=2.6, box_width=3.5)

        base_top = [np.array([-1.45, 0.45, 0]), np.array([0, 1.15, 0]), np.array([1.45, 0.45, 0])]
        base_mid = [np.array([-1.15, -0.4, 0]), np.array([0, 0.15, 0]), np.array([1.15, -0.4, 0])]
        base_bot = [np.array([-0.8, -1.15, 0]), np.array([0, -0.8, 0]), np.array([0.8, -1.15, 0])]

        angle = -6 * DEGREES
        def orient_pts(pts):
            return [rotate_vector(p, angle) + np.array([0, dy, 0]) for p in pts]

        pts_spot_top = orient_pts(base_top)
        pts_spot_mid = orient_pts(base_mid)
        pts_spot_bot = orient_pts(base_bot)

        t_tracker4 = ValueTracker(0)
        
        sys_top = create_bezier_system(pts_spot_top, t_tracker4, path_color=BLACK, path_width=28, glow_opac=0)
        sys_mid = create_bezier_system(pts_spot_mid, t_tracker4, path_color=BLACK, path_width=21, glow_opac=0)
        sys_bot = create_bezier_system(pts_spot_bot, t_tracker4, path_color=BLACK, path_width=15, glow_opac=0)

        self.play(FadeIn(bg_circle, lbl_spotify, shift=UP*0.2, run_time=0.3))
        self.add(sys_top, sys_mid, sys_bot)
        
        self.play(t_tracker4.animate(run_time=3.5, rate_func=linear).set_value(1))
        
        self.play(FadeOut(sys_top[0], sys_mid[0], sys_bot[0], run_time=0.5))
        self.wait(1.5)