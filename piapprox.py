"""
Archimedes π — Manim Animation
Run:  manim -pql archimedes_pi.py ArchimedesPi
HQ:   manim -pqh archimedes_pi.py ArchimedesPi
"""

from manim import *
import numpy as np


def ra_mark(corner, p1, p2, size=0.11, col=GREY):
    u = (p1 - corner) / np.linalg.norm(p1 - corner)
    v = (p2 - corner) / np.linalg.norm(p2 - corner)
    return Polygon(
        corner + size * u,
        corner + size * (u + v),
        corner + size * v,
        corner,
        stroke_width=1.2, stroke_color=col, fill_opacity=0
    ).set_stroke(color=col)


def pyth_box_under(eq_mob, col=BLUE_C):
    """Translucent neon-blue box behind equation, thin white stroke, label underneath."""
    bg = SurroundingRectangle(
        eq_mob, buff=0.22,
        stroke_width=0.8, stroke_color=WHITE,
        fill_color=interpolate_color(BLACK, col, 0.30),
        fill_opacity=0.78, corner_radius=0.10
    )
    lbl = Text("Pythagorean Theorem", font_size=13, color=col)
    lbl.next_to(bg, DOWN, buff=0.06)
    return bg, lbl


class ArchimedesPi(MovingCameraScene):
    def construct(self):
        C_CIRC   = TEAL
        C_POLY   = YELLOW
        C_BISECT = ORANGE
        C_EQ     = WHITE
        C_ACC    = PINK
        C_BLUE   = BLUE_C
        C_RED    = RED_C
        C_GREY   = GREY_B
        C_SUB    = GREEN_C

        cam = self.camera.frame  

        
        
        
        
        
        title_parts = [
            (r"\mathbb{A}\text{rchimedes' }", interpolate_color(RED_C, BLUE_C, 0.0)),
            (r"\pi",                           interpolate_color(RED_C, BLUE_C, 0.4)),
            (r"\text{ }\mathbb{A}\text{pproximation}", interpolate_color(RED_C, BLUE_C, 1.0)),
        ]
        title_mobs = [MathTex(tex, font_size=28, color=col) for tex, col in title_parts]
        title_group = VGroup(*title_mobs).arrange(RIGHT, buff=0.08)
        title_group.to_edge(UP, buff=0.14)
        self.add(title_group)

        
        TW        = title_group.width          
        TITLE_L   = title_group.get_left()[0]  
        TITLE_R   = title_group.get_right()[0] 
        TITLE_CX  = (TITLE_L + TITLE_R) / 2   
        TITLE_BOT = title_group.get_bottom()[1]

        
        bar_w  = TW
        bar_h  = 0.13
        bar_y  = -3.88
        n_stops = 40
        bar_segs = VGroup()
        for i in range(n_stops):
            frac  = i / (n_stops - 1)
            col_s = interpolate_color(C_BLUE, C_RED, frac)
            x_pos = TITLE_L + (i + 0.5) * bar_w / n_stops
            seg   = Rectangle(
                width=bar_w / n_stops, height=bar_h,
                fill_color=col_s, fill_opacity=0.0, stroke_width=0
            ).move_to([x_pos, bar_y, 0])
            bar_segs.add(seg)

        prog_dot = Dot(radius=0.065, color=WHITE).move_to([TITLE_L, bar_y, 0])
        self.add(bar_segs, prog_dot)

        def set_progress(frac, run_time=0.28):
            anims = []
            for i, seg in enumerate(bar_segs):
                seg_frac = i / (n_stops - 1)
                anims.append(seg.animate.set_fill(opacity=0.88 if seg_frac <= frac else 0.0))
            target_x = TITLE_L + frac * bar_w
            anims.append(prog_dot.animate.move_to([target_x, bar_y, 0]))
            return AnimationGroup(*anims, run_time=run_time)

        
        
        
        R      = 1.52
        FIG_CY = TITLE_BOT - R - 0.55   
        cO     = np.array([0.0, FIG_CY, 0])

        EQ_TOP = FIG_CY - R - 0.55      
        EQ_X   = 0.0
        EQ_GAP = 1.02                   

        def eq_pos(row):
            return np.array([EQ_X, EQ_TOP - row * EQ_GAP, 0])

        
        angle_C = PI / 2
        angle_E = PI / 2 - PI / 4
        angle_D = (angle_C + angle_E) / 2
        C = cO + R * np.array([np.cos(angle_C), np.sin(angle_C), 0])
        E = cO + R * np.array([np.cos(angle_E), np.sin(angle_E), 0])
        D = cO + R * np.array([np.cos(angle_D), np.sin(angle_D), 0])
        B = (C + E) / 2

        circ  = Circle(radius=R, color=C_CIRC, stroke_width=2.5).move_to(cO)
        dot_A = Dot(cO, radius=0.055, color=WHITE)
        lbl_A = MathTex("A", font_size=21).next_to(dot_A, LEFT, buff=0.09)

        seg_AC = Line(cO, C, color=WHITE,  stroke_width=1.6)
        seg_AE = Line(cO, E, color=WHITE,  stroke_width=1.6)
        seg_CE = Line(C,  E, color=C_POLY, stroke_width=2.8)
        dot_C  = Dot(C, radius=0.055, color=C_POLY)
        dot_E  = Dot(E, radius=0.055, color=C_POLY)
        lbl_C  = MathTex("C", font_size=20, color=C_POLY).next_to(dot_C, UL, buff=0.06)
        lbl_E  = MathTex("E", font_size=20, color=C_POLY).next_to(dot_E, RIGHT, buff=0.07)

        
        CE_mid  = (C + E) / 2
        CE_perp = np.array([-(E - C)[1], (E - C)[0], 0])
        CE_perp /= np.linalg.norm(CE_perp)
        if np.dot(CE_perp, CE_mid - cO) < 0:
            CE_perp = -CE_perp
        dn_lbl = MathTex(r"d_n", font_size=20, color=C_POLY).move_to(CE_mid + CE_perp * 0.30)

        seg_AD  = Line(cO, D, color=C_BISECT, stroke_width=1.6)
        seg_CD  = Line(C,  D, color=C_BISECT, stroke_width=2.8)
        seg_BD  = Line(B,  D, color=C_GREY,   stroke_width=1.6)
        seg_AB  = Line(cO, B, color=C_GREY,   stroke_width=1.6)
        dot_D   = Dot(D, radius=0.055, color=C_BISECT)
        dot_B   = Dot(B, radius=0.055, color=C_GREY)
        lbl_D   = MathTex("D", font_size=20, color=C_BISECT).next_to(dot_D, UR, buff=0.06)
        lbl_B   = MathTex("B", font_size=20, color=C_GREY).next_to(dot_B, DR, buff=0.06)

        
        CD_mid  = (C + D) / 2
        CD_perp = np.array([-(D - C)[1], (D - C)[0], 0])
        CD_perp /= np.linalg.norm(CD_perp)
        if np.dot(CD_perp, CD_mid - B) < 0:
            CD_perp = -CD_perp
        d2n_lbl = MathTex(r"d_{2n}", font_size=20, color=C_BISECT).move_to(CD_mid + CD_perp * 0.32)

        ra_B = ra_mark(B, cO, D, size=0.12, col=C_GREY)

        def hl(seg, col=C_ACC, width=5):
            return seg.copy().set_color(col).set_stroke(width=width)

        def inscribed_poly(n, radius, centre, **kw):
            angs  = [PI / 2 + 2 * PI * k / n for k in range(n)]
            verts = [centre + radius * np.array([np.cos(a), np.sin(a), 0]) for a in angs]
            return Polygon(*verts, **kw)

        
        live_eqs   = []
        slot_count = [0]

        def place_eq(mob):
            mob.move_to(eq_pos(slot_count[0]))
            live_eqs.append(mob)
            slot_count[0] += 1

        def retire_eq(mob):
            idx = live_eqs.index(mob)
            live_eqs.remove(mob)
            slot_count[0] -= 1
            anims = [FadeOut(mob)]
            for j, m in enumerate(live_eqs[idx:]):
                anims.append(m.animate.move_to(eq_pos(idx + j)))
            return anims

        
        
        
        self.play(set_progress(0.0, run_time=0.01))

        oct8  = inscribed_poly(8,  R, cO, color=C_POLY,   stroke_width=1.8,
                               fill_opacity=0.07, fill_color=C_POLY)
        oct16 = inscribed_poly(16, R, cO, color=C_BISECT, stroke_width=1.8,
                               fill_opacity=0.0)

        dn_def  = MathTex(r"d_n = \text{side of } N\text{-gon}",  font_size=23, color=C_POLY)
        d2n_def = MathTex(r"d_{2n} = \text{side of } 2N\text{-gon}", font_size=23, color=C_BISECT)
        defs    = VGroup(dn_def, d2n_def).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        defs.move_to(eq_pos(0.55))

        self.play(Create(circ), FadeIn(dot_A, lbl_A), run_time=0.40)
        
        oct8_verts  = [cO + R * np.array([np.cos(PI/2 + 2*PI*k/8),
                                            np.sin(PI/2 + 2*PI*k/8), 0]) for k in range(8)]
        oct16_verts = [cO + R * np.array([np.cos(PI/2 + 2*PI*k/16),
                                            np.sin(PI/2 + 2*PI*k/16), 0]) for k in range(16)]
        oct8_edges  = [Line(oct8_verts[k], oct8_verts[(k+1) % 8],
                            color=C_POLY, stroke_width=1.8) for k in range(8)]
        oct16_edges = [Line(oct16_verts[k], oct16_verts[(k+1) % 16],
                            color=C_BISECT, stroke_width=1.8) for k in range(16)]

        
        self.play(Write(dn_def), Write(d2n_def),
                  *[Create(e) for e in oct8_edges],
                  *[Create(e) for e in oct16_edges],
                  run_time=1.2)
        self.remove(*oct8_edges, *oct16_edges)
        self.add(oct8, oct16)
        self.wait(0.30)

        
        self.play(
            Create(seg_AC), Create(seg_AE), Create(seg_CE),
            FadeIn(dot_C, dot_E, lbl_C, lbl_E), run_time=0.40
        )
        self.play(FadeIn(dn_lbl), run_time=0.20)
        self.play(Create(seg_AD), FadeIn(dot_D, lbl_D), run_time=0.30)
        self.play(Create(seg_CD), FadeIn(d2n_lbl), run_time=0.30)

        
        self.play(FadeOut(oct8, oct16, defs), run_time=0.30)

        self.play(Create(seg_AB), Create(seg_BD), FadeIn(dot_B, lbl_B), run_time=0.30)
        self.play(Create(ra_B), run_time=0.20)
        self.wait(0.30)

        self.play(set_progress(0.08))

        
        
        
        
        hl1_CE = hl(seg_CE, col=C_ACC, width=6)
        eq1 = MathTex(r"BC = \frac{d_n}{2}", font_size=31, color=C_EQ)
        place_eq(eq1)

        
        self.play(FadeIn(hl1_CE),
                  dn_lbl.animate.set_color(C_ACC).scale(1.15),
                  run_time=0.25)
        self.wait(0.15)
        self.play(Write(eq1), run_time=0.45)
        self.wait(0.5)
        self.play(FadeOut(hl1_CE),
                  dn_lbl.animate.set_color(C_POLY).scale(1/1.15),
                  run_time=0.20)
        self.play(set_progress(0.18))

        
        
        
        
        
        hl2_AC = hl(seg_AC, col=GREEN_B, width=5)   
        hl2_AB = hl(seg_AB, col=C_SUB,   width=5)   
        hl2_BC = hl(seg_CE, col=C_POLY,  width=5)   
        ra_hl  = ra_B.copy().set_stroke(color=C_ACC, width=2.5)

        eq2 = MathTex(r"AB^2 + BC^2 = 1", font_size=31, color=C_EQ)
        place_eq(eq2)
        eq2.set_color_by_tex("AB", C_SUB)
        eq2.set_color_by_tex("BC", C_POLY)
        bg2, lbl2 = pyth_box_under(eq2)

        self.play(FadeIn(hl2_AB, hl2_BC, hl2_AC, ra_hl), run_time=0.22)
        self.wait(0.15)
        self.add(bg2)
        self.play(Write(eq2), FadeIn(lbl2), run_time=0.45)
        self.wait(0.65)
        self.play(FadeOut(bg2, lbl2, hl2_AB, hl2_BC, hl2_AC, ra_hl), run_time=0.28)
        self.play(set_progress(0.28))

        
        
        
        
        hl3_AB = hl(seg_AB, col=C_SUB, width=5)
        self.play(FadeIn(hl3_AB), run_time=0.15)
        eq2_mid = MathTex(r"AB = \sqrt{1 - BC^2}", font_size=31, color=C_EQ)
        eq2_mid.move_to(eq2.get_center())
        eq2_mid.set_color_by_tex("AB", C_SUB)
        eq2_mid.set_color_by_tex("BC", C_POLY)
        self.play(TransformMatchingShapes(eq2, eq2_mid), run_time=0.48)
        live_eqs[live_eqs.index(eq2)] = eq2_mid
        self.wait(0.35)

        eq1_ghost = eq1.copy().set_color(C_POLY).scale(0.80)
        eq1_ghost.next_to(eq2_mid, DOWN, buff=0.14)
        self.play(FadeIn(eq1_ghost, shift=UP * 0.07), run_time=0.22)
        self.wait(0.35)

        eq3 = MathTex(r"AB = \sqrt{1 - \frac{d_n^2}{4}}", font_size=31, color=C_EQ)
        eq3.move_to(eq2_mid.get_center())
        eq3.set_color_by_tex("AB",  C_SUB)
        eq3.set_color_by_tex("d_n", C_POLY)
        self.play(TransformMatchingShapes(eq2_mid, eq3), FadeOut(eq1_ghost), run_time=0.48)
        live_eqs[live_eqs.index(eq2_mid)] = eq3
        self.play(FadeOut(hl3_AB), run_time=0.18)
        self.wait(0.55)

        ret1 = retire_eq(eq1)
        self.play(*ret1, run_time=0.35)
        self.wait(0.25)
        self.play(set_progress(0.38))

        
        
        
        
        
        hl4_AD = hl(seg_AD, col=GREEN_B,  width=4)  
        hl4_AB = hl(seg_AB, col=C_SUB,    width=5)  
        hl4_BD = hl(seg_BD, col=C_BISECT, width=5)  

        eq4 = MathTex(r"BD = 1 - \sqrt{1 - \frac{d_n^2}{4}}", font_size=29, color=C_EQ)
        place_eq(eq4)
        eq4.set_color_by_tex("BD",  C_BISECT)
        eq4.set_color_by_tex("d_n", C_POLY)

        eq3_ghost = eq3.copy().set_color(C_SUB).scale(0.78)
        eq3_ghost.next_to(eq4, DOWN, buff=0.14)

        self.play(FadeIn(hl4_AD, hl4_AB, hl4_BD), run_time=0.20)
        self.wait(0.15)
        self.play(Write(eq4), run_time=0.42)
        self.play(FadeIn(eq3_ghost, shift=UP * 0.07), run_time=0.20)
        self.wait(0.50)
        self.play(FadeOut(eq3_ghost, hl4_AD, hl4_AB, hl4_BD), run_time=0.22)

        ret3 = retire_eq(eq3)
        self.play(*ret3, run_time=0.32)
        self.wait(0.25)
        self.play(set_progress(0.48))

        
        
        
        
        
        hl5_CD = hl(seg_CD, col=C_ACC,    width=6)   
        hl5_BC = hl(seg_CE, col=C_POLY,   width=5)   
        hl5_BD = hl(seg_BD, col=C_BISECT, width=5)   
        ra_C   = ra_mark(B, C, D, size=0.12, col=C_ACC)  

        eq5 = MathTex(r"d_{2n}^2 = BC^2 + BD^2", font_size=31, color=C_EQ)
        place_eq(eq5)
        eq5.set_color_by_tex("d_{2n}", C_BISECT)
        eq5.set_color_by_tex("BC",     C_POLY)
        eq5.set_color_by_tex("BD",     C_BISECT)
        bg5, lbl5 = pyth_box_under(eq5)

        self.play(FadeIn(hl5_CD, hl5_BC, hl5_BD, ra_C),
                  d2n_lbl.animate.set_color(C_ACC).scale(1.15),
                  run_time=0.22)
        self.wait(0.15)
        self.add(bg5)
        self.play(Write(eq5), FadeIn(lbl5), run_time=0.42)
        self.wait(0.65)
        self.play(FadeOut(bg5, lbl5, hl5_CD, hl5_BC, hl5_BD, ra_C),
                  d2n_lbl.animate.set_color(C_BISECT).scale(1/1.15),
                  run_time=0.25)

        ret4 = retire_eq(eq4)
        self.play(*ret4, run_time=0.32)
        self.wait(0.25)
        self.play(set_progress(0.58))

        
        
        
        
        hl6_CD  = hl(seg_CD, col=C_ACC,    width=6)
        hl6_BC  = hl(seg_CE, col=C_POLY,   width=4)
        hl6_BD  = hl(seg_BD, col=C_BISECT, width=4)
        self.play(FadeIn(hl6_CD, hl6_BC, hl6_BD), run_time=0.20)
        eq6 = MathTex(
            r"d_{2n}^2 = \frac{d_n^2}{4} + \left(1-\sqrt{1-\frac{d_n^2}{4}}\right)^{2}",
            font_size=22, color=C_EQ
        )
        place_eq(eq6)
        eq6.set_color_by_tex("d_{2n}", C_BISECT)
        eq6.set_color_by_tex("d_n",    C_POLY)
        self.play(Write(eq6), run_time=0.42)
        self.wait(0.55)

        eq_final = MathTex(
            r"d_{2n} = \sqrt{2 - 2\sqrt{1 - \frac{d_n^2}{4}}}",
            font_size=31, color=YELLOW
        )
        
        eq_final.move_to(eq6.get_center())
        eq_final.set_color_by_tex("d_{2n}", C_BISECT)
        eq_final.set_color_by_tex("d_n",    C_POLY)

        self.play(TransformMatchingShapes(eq6, eq_final), run_time=0.55)
        live_eqs[live_eqs.index(eq6)] = eq_final
        self.play(FadeOut(hl6_CD, hl6_BC, hl6_BD), run_time=0.20)

        ret5 = retire_eq(eq5)
        self.play(*ret5, run_time=0.30)

        
        self.play(eq_final.animate.shift(DOWN * 0.55), run_time=0.35)

        box_final = SurroundingRectangle(
            eq_final, buff=0.20, color=YELLOW,
            corner_radius=0.11, stroke_width=1.8
        )
        self.play(Create(box_final), run_time=0.28)
        self.play(Wiggle(eq_final, scale_value=1.07, n_wiggles=2), run_time=0.50)
        self.wait(0.55)
        self.play(set_progress(0.65))

        
        
        
        eq_in_circle = MathTex(
            r"d_{2n} = \sqrt{2 - 2\sqrt{1 - \dfrac{d_n^2}{4}}}",
            font_size=15, color=YELLOW
        ).move_to(cO)   

        proof_geo = VGroup(
            dot_A, lbl_A, dot_C, dot_E, dot_D, dot_B,
            lbl_C, lbl_E, lbl_D, lbl_B,
            seg_AC, seg_AE, seg_AD, seg_CE, seg_CD, seg_BD, seg_AB,
            ra_B, dn_lbl, d2n_lbl
        )
        self.play(
            FadeOut(proof_geo),
            FadeOut(eq_final), FadeOut(box_final),
            FadeIn(eq_in_circle),
            run_time=0.45
        )
        self.wait(0.65)

        
        rec_compact = MathTex(
            r"d_{2n} = \sqrt{2 - 2\sqrt{1-\frac{d_n^2}{4}}}",
            font_size=17, color=YELLOW
        ).to_corner(UR, buff=0.28).shift(DOWN * 0.55)
        self.play(FadeIn(rec_compact), run_time=0.28)
        self.wait(0.28)
        self.play(set_progress(0.72))

        
        
        
        R_it = R
        cIt  = cO   

        
        TBL_TOP  = EQ_TOP + 0.14
        
        COL_FRAC = [0.08, 0.30, 0.62, 0.88]   
        COL_X    = [TITLE_L + f * TW for f in COL_FRAC]

        hdr_texts = [
            r"n", 
            r"d_n", 
            r"\frac{n \cdot d(n)}{2}",  
            r"\text{error}"             
        ]
        hdr_cols  = [WHITE, C_POLY, C_ACC, C_GREY]
        
        
        hdr_mobs  = VGroup(*[
            MathTex(t, font_size=14, color=c)
            for t, c in zip(hdr_texts, hdr_cols)
        ])
        for h, x in zip(hdr_mobs, COL_X):
            h.move_to(np.array([x, TBL_TOP, 0]))

        hdr_line = Line(
            np.array([TITLE_L,  TBL_TOP - 0.19, 0]),
            np.array([TITLE_R,  TBL_TOP - 0.19, 0]),
            stroke_width=0.7, color=GREY_B
        )
        self.play(FadeIn(hdr_mobs), Create(hdr_line), run_time=0.26)

        ROW_Y_START = TBL_TOP - 0.43
        ROW_GAP     = 0.31

        def next_d2(d2):
            return 2 - 2 * np.sqrt(max(0.0, 1 - d2 / 4))

        iter_data = []
        d2, n = 1.0, 6
        for _ in range(8):
            d         = np.sqrt(max(0.0, d2))
            pi_approx = n * d / 2
            err       = abs(pi_approx - np.pi)
            iter_data.append((n, d, pi_approx, err))
            d2 = next_d2(d2)
            n *= 2

        prev_poly = None
        all_rows  = []

        def iter_run(idx):
            if idx < 5:
                return 0.42
            return max(0.13, 0.42 - (idx - 4) * 0.10)

        for idx, (n_s, d_s, pi_s, err_s) in enumerate(iter_data):
            frac = idx / (len(iter_data) - 1)
            col  = interpolate_color(YELLOW, TEAL, frac)
            spd  = iter_run(idx)
            sw   = max(0.20, 1.5 - idx * 0.17)

            
            angs  = [PI / 2 + 2 * PI * k / n_s for k in range(n_s)]
            verts = [cIt + R_it * np.array([np.cos(a), np.sin(a), 0]) for a in angs]
            poly  = Polygon(*verts, color=col, stroke_width=sw, fill_opacity=0.0)

            if idx == 0:
                
                edges = [Line(verts[k], verts[(k+1) % n_s], color=col, stroke_width=sw)
                         for k in range(n_s)]
                for e in edges:
                    self.play(Create(e), run_time=spd / n_s)
                self.remove(*edges)
                self.add(poly)
                prev_poly = poly
            else:
                self.play(Transform(prev_poly, poly), run_time=spd)

            
            row_y    = ROW_Y_START - idx * ROW_GAP
            row_vals = [f"{n_s}", f"{d_s:.5f}", f"{pi_s:.6f}", f"{err_s:.6f}"]
            row_col_ = [col, C_POLY, C_ACC, C_GREY]
            row_mobs = VGroup(*[
                Text(v, font_size=13, color=c)
                for v, c in zip(row_vals, row_col_)
            ])
            for rm, x in zip(row_mobs, COL_X):
                rm.move_to(np.array([x, row_y, 0]))
            all_rows.append(row_mobs)
            self.play(FadeIn(row_mobs, shift=UP * 0.04), run_time=max(0.18, spd * 0.6))
            self.add(row_mobs)

            prog_frac = 0.72 + 0.28 * (idx + 1) / len(iter_data)
            self.play(set_progress(prog_frac, run_time=0.10))
            self.wait(0.05)

        self.play(set_progress(1.0))
        self.wait(0.90)

        
        
        
        fade_group = VGroup(
            rec_compact, hdr_mobs, hdr_line,
            bar_segs, prog_dot,
            *all_rows
        )
        self.play(FadeOut(fade_group), run_time=0.55)

        CIRC_BOT = cIt[1] - R_it

        pi_day   = MathTex(r"\text{Happy } \pi \text{ Day!}",
                            font_size=52, color=C_ACC)
        pi_limit = MathTex(
            r"\pi \;\approx\; \frac{n \cdot d_n}{2} \;\longrightarrow\; 3.14159265\ldots",
            font_size=26, color=YELLOW
        )
        splash = VGroup(pi_day, pi_limit).arrange(DOWN, buff=0.44)
        splash.move_to(np.array([0.0, CIRC_BOT - 1.30, 0]))

        self.play(FadeIn(pi_day,   scale=1.18), run_time=0.50)
        self.play(FadeIn(pi_limit, shift=UP * 0.12), run_time=0.42)
        self.wait(4.0)