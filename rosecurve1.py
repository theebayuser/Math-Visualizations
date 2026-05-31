from manim import *
import numpy as np

class Rosace3Arm(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        SCALE = 0.85

        GRAPH_OFFSET = np.array([0, 0.3, 0])

        title = VGroup(
            MathTex(r"\mathbb{R}\mathrm{osace}", font_size=40),
            MathTex(r"\mathbb{C}\mathrm{urve}", font_size=40),
        ).arrange(RIGHT, buff=0.18)
        title.set_color_by_gradient("#29ABCA", "#9B59B6", "#FC6255")

        header = title.copy()
        header.to_edge(UP, buff=0.6)
        header_bg = BackgroundRectangle(header, color=BLACK, fill_opacity=0.7, buff=0.25)

        param_group = VGroup(
            MathTex(r"x(t) = \sin(7t) + \sin(13t) + \sin(7t)", font_size=32, color=PINK),
            MathTex(r"y(t) = \cos(7t) + \cos(13t) + \cos(7t)", font_size=32, color=TEAL),
        ).arrange(DOWN, buff=0.15)

        def get_theta_from_t(val):
            x = 2 * np.sin(7 * val) + np.sin(13 * val)
            y = 2 * np.cos(7 * val) + np.cos(13 * val)
            return (np.arctan2(y, x) * 180 / PI) % 360

        val_theta = DecimalNumber(get_theta_from_t(PI), num_decimal_places=1, font_size=32, color=WHITE)

        eq_theta = VGroup(
            MathTex(r"\theta = ", font_size=32, color=WHITE),
            val_theta,
        ).arrange(RIGHT, buff=0.1)

        polar_group = VGroup(
            MathTex(r"r(t) = \sqrt{5 + 4\cos(6t)}", font_size=32, color=PINK),
            eq_theta
        ).arrange(DOWN, buff=0.15)

        max_width = max(param_group.width, polar_group.width)
        max_height = max(param_group.height, polar_group.height)
        dummy_box = Rectangle(width=max_width, height=max_height).move_to(param_group)
        dummy_box.to_edge(DOWN, buff=0.35)

        param_group.move_to(dummy_box.get_center())
        polar_group.move_to(dummy_box.get_center())

        box_padding = 0.35
        param_box = RoundedRectangle(
            corner_radius=0.2,
            width=param_group.width + box_padding * 2,
            height=param_group.height + box_padding * 2,
            color=WHITE,
            stroke_width=1.8,
            fill_color="#0E1F39",
            fill_opacity=0.25,
        ).move_to(param_group)

        polar_box = RoundedRectangle(
            corner_radius=0.2,
            width=polar_group.width + box_padding * 2,
            height=polar_group.height + box_padding * 2,
            color=WHITE,
            stroke_width=1.8,
            fill_color="#0E1F39",
            fill_opacity=0.25,
        ).move_to(polar_group)

  
        t = ValueTracker(0)

        def get_j1():
            val = t.get_value()
            return np.array([np.sin(7 * val), np.cos(7 * val), 0]) * SCALE + GRAPH_OFFSET

        def get_j2():
            val = t.get_value()
            return get_j1() + np.array([np.sin(13 * val), np.cos(13 * val), 0]) * SCALE

        def get_j3():
            val = t.get_value()
            return get_j2() + np.array([np.sin(7 * val), np.cos(7 * val), 0]) * SCALE

        origin_dot = Dot(GRAPH_OFFSET, color=WHITE, radius=0.04)

        j1_dot = Dot(point=get_j1(), radius=0.03, color=BLUE)
        j2_dot = Dot(point=get_j2(), radius=0.03, color=PURPLE)
        j3_dot = Dot(point=get_j3(), radius=0.05, color=WHITE)

        line1 = Line(GRAPH_OFFSET, j1_dot.get_center(), color=DARK_GREY, stroke_width=3)
        line2 = Line(j1_dot.get_center(), j2_dot.get_center(), color=LIGHT_GREY, stroke_width=2.5)
        line3 = Line(j2_dot.get_center(), j3_dot.get_center(), color=WHITE, stroke_width=2)

        j1_dot.add_updater(lambda m: m.move_to(get_j1()))
        j2_dot.add_updater(lambda m: m.move_to(get_j2()))
        j3_dot.add_updater(lambda m: m.move_to(get_j3()))

        line1.add_updater(lambda m: m.become(Line(GRAPH_OFFSET, j1_dot.get_center(), color=DARK_GREY, stroke_width=3)))
        line2.add_updater(lambda m: m.become(Line(j1_dot.get_center(), j2_dot.get_center(), color=LIGHT_GREY, stroke_width=2.5)))
        line3.add_updater(lambda m: m.become(Line(j2_dot.get_center(), j3_dot.get_center(), color=WHITE, stroke_width=2)))

        path1 = VGroup()
        path2 = VGroup()
        main_path = VGroup()

        self.last_p1 = None
        self.last_p2 = None
        self.last_p3 = None

        def update_traces(m):
            p1, p2, p3 = j1_dot.get_center(), j2_dot.get_center(), j3_dot.get_center()
            val = t.get_value()

            if self.last_p1 is None or np.linalg.norm(p1 - self.last_p1) > 0.08:
                path1.add(Dot(p1, radius=0.009, color=BLUE, fill_opacity=0.38))
                self.last_p1 = p1

            if self.last_p2 is None or np.linalg.norm(p2 - self.last_p2) > 0.08:
                path2.add(Dot(p2, radius=0.013, color=PURPLE, fill_opacity=0.62))
                self.last_p2 = p2

            if self.last_p3 is None:
                self.last_p3 = p3
            elif np.linalg.norm(p3 - self.last_p3) > 0.02:
                r = np.sqrt(5 + 4 * np.cos(6 * val))
                ratio = (r - 1) / 2
                current_color = interpolate_color(TEAL, PINK, ratio)

                new_line = Line(self.last_p3, p3, color=current_color, stroke_width=2.5)
                main_path.add(new_line)
                self.last_p3 = p3
                j3_dot.set_color(current_color)

        main_path.add_updater(update_traces)

        self.add(header_bg, header)
        self.add(param_box, param_group)
        self.add(t, origin_dot, path1, path2, main_path, line1, line2, line3, j1_dot, j2_dot, j3_dot)

        self.play(t.animate.set_value(PI), run_time=10, rate_func=linear)

        self.play(
            FadeOut(param_box, param_group, shift=UP*0.2),
            FadeIn(polar_box, polar_group, shift=UP*0.2),
            t.animate.set_value(PI + 0.15 * PI),
            run_time=1.0,
            rate_func=linear
        )

        val_theta.add_updater(lambda m: m.set_value(get_theta_from_t(t.get_value())))

        self.play(t.animate.set_value(2 * PI + 0.25 * PI), run_time=9.5, rate_func=linear)