from manim import *

class DiophantusIdentity(Scene):
    def construct(self):
        
        
        c_a = TEAL_D
        c_b = MAROON_D
        c_c = BLUE_D
        c_d = GOLD_D
        
        
        title = Tex(r"$\mathbb{D}$iophantus Identity", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.2)
        
        self.add(title)

        
        
        val_a = 0.8
        val_b = 1.2
        val_c = 0.9
        val_d = 1.5
        
        
        
        
        
        
        w1, w2 = 2.0, 3.5 
        h1, h2 = 1.5, 3.0 
        
        r_ac = Rectangle(width=w1, height=h1).set_fill(c_a, 0.5).set_stroke(WHITE, 1)
        r_bc = Rectangle(width=w2, height=h1).set_fill(c_d, 0.5).set_stroke(WHITE, 1)
        r_ad = Rectangle(width=w1, height=h2).set_fill(c_c, 0.5).set_stroke(WHITE, 1)
        r_bd = Rectangle(width=w2, height=h2).set_fill(c_b, 0.5).set_stroke(WHITE, 1)
        
        
        top_row = VGroup(r_ac, r_bc).arrange(RIGHT, buff=0)
        bot_row = VGroup(r_ad, r_bd).arrange(RIGHT, buff=0)
        initial_grid = VGroup(top_row, bot_row).arrange(DOWN, buff=0).scale(0.6).move_to(ORIGIN)
        
        
        l_ac = MathTex(r"a^2c^2").move_to(r_ac).scale(0.6)
        l_bc = MathTex(r"b^2c^2").move_to(r_bc).scale(0.6)
        l_ad = MathTex(r"a^2d^2").move_to(r_ad).scale(0.6)
        l_bd = MathTex(r"b^2d^2").move_to(r_bd).scale(0.6)
        labels_1 = VGroup(l_ac, l_bc, l_ad, l_bd)

        
        top_brace = Brace(top_row, UP, buff=0.05)
        top_label = MathTex(r"a^2+b^2").next_to(top_brace, UP, buff=0.00).scale(0.6)
        left_brace = Brace(VGroup(r_ac, r_ad), LEFT, buff=0.02)
        left_label = MathTex(r"c^2+d^2").scale(0.6).rotate(90 * DEGREES).next_to(left_brace, LEFT, buff=0.05)
        
        self.play(DrawBorderThenFill(initial_grid), Write(labels_1), run_time=1.5)
        self.play(GrowFromCenter(top_brace), Write(top_label),
                  GrowFromCenter(left_brace), Write(left_label))
        self.wait(0.5)

        
        
        s_ac = Square(side_length=val_a*val_c).set_fill(c_a, 0.5).set_stroke(WHITE, 1)
        s_bd = Square(side_length=val_b*val_d).set_fill(c_b, 0.5).set_stroke(WHITE, 1)
        s_ad = Square(side_length=val_a*val_d).set_fill(c_c, 0.5).set_stroke(WHITE, 1)
        s_bc = Square(side_length=val_b*val_c).set_fill(c_d, 0.5).set_stroke(WHITE, 1)
        
        
        
        
        
        
        center_point = LEFT * 1
        s_ad.move_to(center_point, aligned_edge=DR)
        s_bc.move_to(center_point, aligned_edge=UL)
        s_ac.move_to(center_point, aligned_edge=DL)
        s_bd.move_to(center_point, aligned_edge=UR)
        
        squares_group = VGroup(s_ac, s_bc, s_ad, s_bd)
        
        
        nl_ac = MathTex(r"(ac)^2").move_to(s_ac).scale(0.5)
        nl_bc = MathTex(r"(bc)^2").move_to(s_bc).scale(0.5)
        nl_ad = MathTex(r"(ad)^2").move_to(s_ad).scale(0.5)
        nl_bd = MathTex(r"(bd)^2").move_to(s_bd).scale(0.5)
        new_labels = VGroup(nl_ac, nl_bc, nl_ad, nl_bd)

        self.play(
            FadeOut(top_brace), FadeOut(top_label), FadeOut(left_brace), FadeOut(left_label),
            ReplacementTransform(initial_grid, squares_group),
            ReplacementTransform(labels_1, new_labels),
            run_time=1.5
        )
        self.wait(0.5)

        
        
        
        
        
        
        s_ac_target = s_ac.generate_target()
        s_bd_target = s_bd.generate_target()
        
        
        
        s_bd_target.move_to(ORIGIN, aligned_edge=ORIGIN)
        s_ac_target.next_to(s_bd_target, UP, buff=0, aligned_edge=LEFT)
        
        
        stack = VGroup(s_ac_target, s_bd_target)
        stack.move_to(RIGHT * 1.5 + ORIGIN)
        
        
        nl_ac.add_updater(lambda m: m.move_to(s_ac))
        nl_bd.add_updater(lambda m: m.move_to(s_bd))

        self.play(
            MoveToTarget(s_ac), MoveToTarget(s_bd),
            run_time=1.5
        )
        
        
        
        bd_corn = s_bd.get_corner(DL)
        ac_len = s_ac.width
        bd_len = s_bd.width
        
        
        
        rect_bottom = Rectangle(width=bd_len, height=ac_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_bottom.move_to(s_bd.get_corner(DL), aligned_edge=DL)
        
        
        rect_vertical = Rectangle(width=ac_len, height=bd_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_vertical.move_to(s_ac.get_corner(UL), aligned_edge=UL)
        
        
        diff_side = bd_len - ac_len
        sq_diff = Square(side_length=diff_side).set_fill(GRAY, 0.8).set_stroke(WHITE, 1)
        sq_diff.move_to(s_bd.get_corner(DR), aligned_edge=DR).shift(UP * ac_len)

        
        cut_line_horiz = DashedLine(s_bd.get_corner(DL) + UP*ac_len, s_bd.get_corner(DR) + UP*ac_len)
        cut_line_vert = DashedLine(s_bd.get_corner(UL) + RIGHT*ac_len, s_bd.get_corner(DL) + RIGHT*ac_len)
        
        
        
        bd_top_label = MathTex("bd", font_size=20).next_to(rect_vertical, LEFT, buff=0.1).shift(DOWN * 0.5)
        
        self.play(Create(cut_line_horiz), Create(cut_line_vert), Write(bd_top_label))
        self.wait(0.3)
        
        
        l_abcd1 = MathTex("abcd", font_size=28).move_to(rect_bottom)
        l_abcd2 = MathTex("abcd", font_size=28).move_to(rect_vertical).shift(DOWN*0.2)
        
        
        side_label_ac = MathTex("ac", font_size=20).next_to(rect_bottom, DOWN, buff=0.1)
        side_label_bd1 = MathTex("bd", font_size=20).next_to(rect_bottom, LEFT, buff=0.1)
        side_label_bd2 = MathTex("bd", font_size=20).next_to(rect_vertical, UP, buff=0.1)
        side_label_ac2 = MathTex("ac", font_size=20).next_to(rect_vertical, RIGHT, buff=0.1)
        
        l_diff = MathTex(r"(bd-ac)^2", font_size=20).move_to(sq_diff)
        
        self.remove(nl_ac, nl_bd) 
        self.play(
            FadeOut(s_ac), FadeOut(s_bd),
            FadeOut(bd_top_label),
            FadeIn(rect_bottom), FadeIn(rect_vertical),
            Write(l_abcd1), Write(l_abcd2),
            Write(side_label_ac), Write(side_label_bd1),
            Write(side_label_bd2), Write(side_label_ac2),
            FadeIn(sq_diff), Write(l_diff)
        )
        self.wait(0.3)
        
        
        self.play(FadeOut(cut_line_horiz), FadeOut(cut_line_vert), run_time=0.5)
        self.wait(0.2)

        
        
        
        
        ad_len = s_ad.width
        bc_len = s_bc.width
        
        
        
        
        rect_bottom_final = Rectangle(width=ad_len, height=bc_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        rect_vertical_final = Rectangle(width=bc_len, height=ad_len).set_fill(GREEN_D, 0.6).set_stroke(WHITE, 1)
        
        
        
        
        
        s_ad.generate_target().move_to(ORIGIN + LEFT*0.8 + UP*0.8, aligned_edge=DR)
        s_bc.generate_target().move_to(s_ad.target.get_corner(DR), aligned_edge=UL)
        
        rect_vertical_final.next_to(s_ad.target, RIGHT, buff=0, aligned_edge=UP)
        rect_bottom_final.next_to(s_ad.target, DOWN, buff=0, aligned_edge=LEFT)
        
        
        rect_vertical_final.align_to(s_bc.target, RIGHT)
        rect_bottom_final.align_to(s_bc.target, DOWN)
        
        
        sq_diff.generate_target().next_to(s_bc.target, RIGHT, buff=0.5)
        l_diff.add_updater(lambda m: m.move_to(sq_diff))

        
        self.play(
            FadeOut(side_label_ac), FadeOut(side_label_bd1),
            FadeOut(side_label_bd2), FadeOut(side_label_ac2),
            MoveToTarget(s_ad), MoveToTarget(s_bc),
            ReplacementTransform(rect_vertical, rect_vertical_final),
            ReplacementTransform(rect_bottom, rect_bottom_final),
            MoveToTarget(sq_diff),
            l_abcd1.animate.move_to(rect_bottom_final),
            l_abcd2.animate.move_to(rect_vertical_final),
            nl_ad.animate.move_to(s_ad.target),
            nl_bc.animate.move_to(s_bc.target),
            run_time=2
        )
        
        
        final_group = VGroup(s_ad, s_bc, rect_vertical_final, rect_bottom_final)
        
        
        
        top_ad_label = MathTex("ad", font_size=20).next_to(s_ad.target, UP, buff=0.1)
        top_bc_label = MathTex("bc", font_size=20).next_to(rect_vertical_final, UP, buff=0.1)
        
        
        right_bc_label = MathTex("bc", font_size=20).next_to(rect_vertical_final, RIGHT, buff=0.1)
        right_ad_label = MathTex("ad", font_size=20).next_to(s_bc.target, RIGHT, buff=0.1)
        
        
        bottom_bc_label = MathTex("bc", font_size=20).next_to(s_bc.target, DOWN, buff=0.1)
        bottom_ad_label = MathTex("ad", font_size=20).next_to(rect_bottom_final, DOWN, buff=0.1)
        
        
        left_ad_label = MathTex("ad", font_size=20).next_to(s_ad.target, LEFT, buff=0.1)
        left_bc_label = MathTex("bc", font_size=20).next_to(rect_bottom_final, LEFT, buff=0.1)
        
        side_labels = VGroup(top_ad_label, top_bc_label, right_bc_label, right_ad_label,
                             bottom_bc_label, bottom_ad_label, left_ad_label, left_bc_label)
        
        
        self.play(Write(side_labels))
        self.wait(0.3)
        
        
        brace = Brace(final_group, DOWN)
        final_text = MathTex(r"(ad+bc)^2").next_to(brace, DOWN).scale(0.8)
        
        self.play(GrowFromCenter(brace), Write(final_text))
        
        
        eq_line1 = MathTex(r"(a^2+b^2)(c^2+d^2)")
        eq_line2 = MathTex(r"= (ad+bc)^2 + (bd-ac)^2")
        eq = VGroup(eq_line1, eq_line2).arrange(DOWN, buff=0.2)
        eq.scale(0.7).to_edge(DOWN, buff=0.3)
        bg = BackgroundRectangle(eq, fill_color=BLACK, fill_opacity=0.8)
        
        self.play(FadeIn(bg), Write(eq))
        self.wait(2)