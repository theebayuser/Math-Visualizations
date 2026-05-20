from manim import *
import numpy as np

class LawOfCosinesDerivation(Scene):
    def construct(self):
        
        color_a   = BLUE_C
        color_b   = GREEN_C
        color_c   = RED_C
        color_emp = YELLOW_D
        color_hyp = ORANGE
        color_adj = TEAL_C

        tex_colors = {
            "a": color_a,
            "b": color_b,
            "c": color_c,
            r"\theta": color_emp,
        }

        
        title = MathTex(
            r"\mathbb{L}\text{aw of }\mathbb{C}\text{osines}",
            font_size=36, color=WHITE
        )
        title.to_edge(UP, buff=0.18)

        
        a_val   = 1.85
        b_val   = 1.45
        theta_v = 48 * DEGREES

        shift = UP * 0.55 + LEFT * 0.1

        O_pt   = np.array([0.0, 0.0, 0.0]) + shift
        A_pt   = O_pt + np.array([a_val, 0.0, 0.0])
        dir_AB = np.array([-np.cos(theta_v),  np.sin(theta_v), 0.0])
        B_pt   = A_pt + b_val * dir_AB
        c_val  = float(np.linalg.norm(B_pt - O_pt))

        
        circle     = Circle(radius=a_val, color=WHITE, stroke_opacity=0.40).move_to(O_pt)
        center_dot = Dot(O_pt, color=WHITE, radius=0.05)

        
        line_a = Line(O_pt, A_pt, color=color_a, stroke_width=2.5)
        line_b = Line(A_pt, B_pt, color=color_b, stroke_width=2.5)
        line_c = Line(O_pt, B_pt, color=color_c, stroke_width=2.5)

        label_a = MathTex("a", color=color_a, font_size=28).next_to(line_a, DOWN, buff=0.12)
        label_b = MathTex("b", color=color_b, font_size=28).next_to(line_b, RIGHT, buff=0.12)
        label_c = MathTex("c", color=color_c, font_size=28).move_to(
            (O_pt + B_pt) / 2 + LEFT * 0.28 + UP * 0.05
        )

        
        ray_AB_line = Line(A_pt, B_pt)
        ray_AO_line = Line(A_pt, O_pt)
        angle_arc   = Angle(ray_AB_line, ray_AO_line, radius=0.36, color=color_emp)
        lbl_theta   = MathTex(r"\theta", color=color_emp, font_size=26).move_to(
            Angle(ray_AB_line, ray_AO_line, radius=0.60).point_from_proportion(0.5)
        )

        
        self.play(
            Write(title),
            Create(circle),
            FadeIn(center_dot),
            Create(line_a), Create(line_b), Create(line_c),
            run_time=1.4
        )
        self.play(
            Write(label_a), Write(label_b), Write(label_c),
            Create(angle_arc), Write(lbl_theta),
        )
        self.wait(0.1)

        
        dir_OB  = (B_pt - O_pt) / c_val
        P_near  = O_pt + a_val * dir_OB
        P_far   = O_pt - a_val * dir_OB
        perp_OB = np.array([-dir_OB[1], dir_OB[0], 0.0])

        dash1 = DashedLine(B_pt, P_near, color=GREY_B, dash_length=0.10, stroke_width=1.8)
        dash2 = DashedLine(O_pt, P_far,  color=GREY_B, dash_length=0.10, stroke_width=1.8)

        lbl_a_minus_c = MathTex("a-c", font_size=23, color=WHITE).move_to(
            (B_pt + P_near) / 2 + perp_OB * 0.32
        )
        lbl_a_minus_c.set_color_by_tex_to_color_map(tex_colors)

        lbl_a_far = MathTex("a", font_size=23, color=color_a).move_to(
            (O_pt + P_far) / 2 + perp_OB * 0.32
        )

        
        BmO  = B_pt - O_pt
        qa   = float(np.dot(dir_AB, dir_AB))
        qb   = float(2 * np.dot(BmO, dir_AB))
        qc   = float(np.dot(BmO, BmO) - a_val**2)
        disc = qb**2 - 4*qa*qc
        t1   = (-qb + np.sqrt(max(disc, 0.0))) / (2*qa)
        t2   = (-qb - np.sqrt(max(disc, 0.0))) / (2*qa)
        t_Q  = t1 if t1 > 1e-6 else t2
        Q_pt = B_pt + t_Q * dir_AB

        perp_AB = np.array([-dir_AB[1], dir_AB[0], 0.0])
        dash3   = DashedLine(B_pt, Q_pt, color=GREY_B, dash_length=0.10, stroke_width=1.8)

        self.play(Create(dash1), Create(dash2), Create(dash3))
        self.play(Write(lbl_a_minus_c), Write(lbl_a_far))
        self.wait(0.1)

        
        A_opp = O_pt - np.array([a_val, 0.0, 0.0])

        dash_diam = DashedLine(A_pt, A_opp, color=BLUE_A,
                               dash_length=0.09, stroke_width=1.8)
        lbl_2a = MathTex("2a", font_size=22, color=color_a).next_to(
            dash_diam, DOWN, buff=0.12
        )
        line_AoppQ = Line(A_opp, Q_pt, color=color_hyp, stroke_width=2.2)

        self.play(Create(dash_diam), Create(line_AoppQ))
        self.play(Write(lbl_2a))
        self.wait(0.01)

        
        dir_QA    = (A_pt  - Q_pt) / np.linalg.norm(A_pt  - Q_pt)
        dir_QAopp = (A_opp - Q_pt) / np.linalg.norm(A_opp - Q_pt)
        sq        = 0.10
        sq_p1     = Q_pt + sq * dir_QA
        sq_p2     = Q_pt + sq * dir_QAopp
        sq_corner = Q_pt + sq * dir_QA + sq * dir_QAopp
        right_mark = Polygon(
            sq_p1, sq_corner, sq_p2, Q_pt,
            color=WHITE, stroke_width=1.3, fill_opacity=0
        )
        self.play(Create(right_mark))
        self.wait(0.3)

        
        line_AQ = Line(A_pt, Q_pt, color=color_adj, stroke_width=2.2)
        self.play(Create(line_AQ))

        
        cos_eq0 = MathTex(
            r"\cos", r"\theta", r"=",
            r"\frac{\text{adj}}{\text{hyp}}",
            font_size=28
        )
        cos_eq0[1].set_color(color_emp)
        cos_eq0.to_edge(DOWN, buff=1.55)

        hyp_highlight = line_AoppQ.copy().set_stroke(color=color_hyp, width=5, opacity=0.85)
        adj_highlight = line_AQ.copy().set_stroke(color=color_adj, width=5, opacity=0.85)

        self.play(
            Create(hyp_highlight),
            Create(adj_highlight),
            Write(cos_eq0),
            run_time=0.8
        )
        self.wait(0.2)

        
        cos_eq1 = MathTex(
            r"\text{hyp}", r"\cdot", r"\cos", r"\theta", r"=", r"\text{adj}",
            font_size=28
        )
        cos_eq1[0].set_color(color_hyp)
        cos_eq1[3].set_color(color_emp)
        cos_eq1[5].set_color(color_adj)
        cos_eq1.move_to(cos_eq0)

        self.play(TransformMatchingTex(cos_eq0, cos_eq1))
        self.wait(0.2)

        
        cos_eq2 = MathTex(
            r"2", r"a", r"\cdot", r"\cos", r"\theta", r"=", r"\text{adj}",
            font_size=28
        )
        cos_eq2[0].set_color(color_a)
        cos_eq2[1].set_color(color_a)
        cos_eq2[4].set_color(color_emp)
        cos_eq2[6].set_color(color_adj)
        cos_eq2.move_to(cos_eq1)

        self.play(
            TransformMatchingTex(cos_eq1, cos_eq2),
            FadeOut(hyp_highlight),
            FadeOut(adj_highlight),
        )
        self.wait(0.6)

        
        aq_label_pos = (A_pt + Q_pt) / 2 + perp_AB * (-0.38)

        
        lbl_AQ = MathTex(r"2a\cos\theta", font_size=21)
        lbl_AQ.set_color(color_adj)
        lbl_AQ.move_to(aq_label_pos)

        eq2_lhs_copy = VGroup(*[cos_eq2[i].copy() for i in range(5)])

        self.play(
            FadeOut(cos_eq2),
            Transform(eq2_lhs_copy, lbl_AQ),
            run_time=0.8
        )
        self.remove(eq2_lhs_copy)
        self.add(lbl_AQ)
        self.wait(0.4)

        
        lbl_BQ = MathTex(r"2a\cos\theta - b", font_size=22).move_to(
            (B_pt + Q_pt) / 2 + perp_AB * 0.38
        )
        lbl_BQ.set_color(color_adj)
        self.play(Write(lbl_BQ))
        self.wait(0.6)

        
        eq1 = MathTex(
            "(", "a", "+", "c", ")(", "a", "-", "c", ")",
            "=",
            "b", "(", "2", "a", r"\cos", r"\theta", "-", "b", ")",
            font_size=28
        )
        eq1.set_color_by_tex_to_color_map(tex_colors)
        
        eq1.to_edge(DOWN, buff=1.55)

        
        pop_label = Tex("Power of a Point", font_size=20, color=color_emp)
        pop_label.next_to(eq1, DOWN, buff=0.20)

        
        combined = VGroup(eq1, pop_label)
        pop_box = BackgroundRectangle(
            combined, color="#1a1a2e", fill_opacity=0.82,
            buff=0.22, corner_radius=0.14
        )
        pop_box.set_stroke(color=WHITE, width=1.2, opacity=0.7)

        
        self.play(
            FadeIn(pop_box),
            Write(eq1),
            Write(pop_label),
            line_c.animate.set_stroke(color=YELLOW_A, width=5),
            dash1.animate.set_stroke(color=YELLOW_A, width=3),
            dash2.animate.set_stroke(color=YELLOW_A, width=3),
            line_b.animate.set_stroke(color=YELLOW_A, width=5),
            dash3.animate.set_stroke(color=YELLOW_A, width=3),
            run_time=1.2
        )
        self.wait(0.6)

        
        self.play(
            line_c.animate.set_stroke(color=color_c, width=2.5),
            dash1.animate.set_stroke(color=GREY_B, width=1.8),
            dash2.animate.set_stroke(color=GREY_B, width=1.8),
            line_b.animate.set_stroke(color=color_b, width=2.5),
            dash3.animate.set_stroke(color=GREY_B, width=1.8),
            run_time=0.5
        )
        self.wait(0.5)

        
        eq2 = MathTex(
            "a", "^2", "-", "c", "^2",
            "=",
            "2", "a", "b", r"\cos", r"\theta", "-", "b", "^2",
            font_size=28
        )
        eq2.set_color_by_tex_to_color_map(tex_colors)
        eq2.move_to(eq1)

        self.play(
            TransformMatchingTex(eq1, eq2),
            FadeOut(pop_box),
            FadeOut(pop_label),
        )
        self.wait(1.0)

        
        eq3 = MathTex(
            "c", "^2",
            "=",
            "a", "^2", "+", "b", "^2",
            "-", "2", "a", "b", r"\cos", r"\theta",
            font_size=33
        )
        eq3.set_color_by_tex_to_color_map(tex_colors)
        eq3.move_to(eq2)

        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(2.0)