"""
Fundamental Theorem of Calculus – Manim CE animation
=====================================================
Render full video:
    manim -pqh ftc_animation.py FundamentalTheoremOfCalculus
"""

from manim import *
import math as _math




C_CURVE  = "#F48FB1"   
C_AREA   = "#4DB6AC"   
C_EDGE   = "#FFB74D"   
C_TICK   = "#CE93D8"   
C_FTC1   = "#80DEEA"   
C_MVT    = "#A5D6A7"   
C_FINAL  = "#EF9A9A"   
C_STRIKE = "#FF5252"   
C_WHITE  = "#FFFFFF"
C_GRAY   = "#607D8B"
BG       = "#000000"




TITLE_Y   =  3.30
DIV_Y     =  2.85
AX_DEF_Y  =  2.48
GRAPH_Y   =  0.90
A_VAL     = -1.50
X_VAL     =  1.10
CURVE_START = -2.0
CURVE_END   =  3.2




EQ_Y = [1.26, 0.04, -1.18, -2.40, -3.60]







def f(x):
    return -0.18 * x**3 + 0.4 * x**2 + 1.6





def make_axes():
    ax = Axes(
        x_range=[-3.2, 3.2, 1],
        y_range=[-0.3, 3.2, 1],
        x_length=5.2,
        y_length=2.0,
        axis_config={
            "color": C_GRAY,
            "stroke_width": 1.4,
            "include_tip": True,
            "tip_length": 0.6,
            "tip_width": 0.25,
        },
    )
    ax.move_to(UP * GRAPH_Y)
    return ax


def make_curve(ax):
    return ax.plot(f, x_range=[CURVE_START, CURVE_END],
                   color=C_CURVE, stroke_width=2.8)


def make_title():
    
    line1_words = ["Fundamental", "Theorem"]
    line1_pieces = []
    for word in line1_words:
        bb   = MathTex(rf"\mathbb{{{word[0]}}}", font_size=38, color=C_WHITE)
        tail = Text(word[1:], font_size=36, color=C_WHITE)
        line1_pieces.append(VGroup(bb, tail).arrange(RIGHT, buff=0.03))
    line1 = VGroup(*line1_pieces).arrange(RIGHT, buff=0.22)

    
    of_text  = Text("of", font_size=36, color=C_WHITE)
    cal_bb   = MathTex(r"\mathbb{C}", font_size=38, color=C_WHITE)
    cal_tail = Text("alculus", font_size=36, color=C_WHITE)
    cal_word = VGroup(cal_bb, cal_tail).arrange(RIGHT, buff=0.03)
    line2 = VGroup(of_text, cal_word).arrange(RIGHT, buff=0.22)

    title = VGroup(line1, line2).arrange(DOWN, buff=0.18, aligned_edge=ORIGIN)
    title.move_to(UP * TITLE_Y)
    return title


def thin_divider():
    ln = Line(LEFT * 3.5, RIGHT * 3.5, stroke_width=0.7, color=C_GRAY)
    ln.set_opacity(0.35)
    ln.move_to(UP * DIV_Y)
    return ln


def labeled_box(content, label_str, box_color, label_size=17):
    bg = SurroundingRectangle(
        content, color=box_color, stroke_width=1.3,
        buff=0.22, corner_radius=0.10
    )
    bg.set_fill(box_color, opacity=0.13)
    lbl = Text(label_str, font_size=label_size, color=box_color, weight=BOLD)
    lbl.next_to(bg, UP, buff=0.07).align_to(bg, LEFT)
    return bg, lbl


def strikethrough(mob, color=C_STRIKE, width=3.2):
    return Line(mob.get_corner(DL), mob.get_corner(UR),
                color=color, stroke_width=width)





class FundamentalTheoremOfCalculus(Scene):

    def setup(self):
        self.camera.background_color = BG

    def construct(self):

        
        title = make_title()
        div   = thin_divider()
        ax    = make_axes()
        curve = make_curve(ax)

        label_fx = MathTex(r"y = f(x)", color=C_CURVE, font_size=22)
        label_fx.move_to(ax.c2p(-2.3, 2.85))

        
        self.play(
            AnimationGroup(
                FadeIn(title, shift=UP * 0.12),
                Create(div),
                lag_ratio=0.3
            ),
            AnimationGroup(
                Create(ax),
                Create(curve),
                lag_ratio=0.2
            ),
            run_time=1.2
        )
        self.play(FadeIn(label_fx), run_time=0.4)

        
        tick_a = Line(ax.c2p(A_VAL, -0.08), ax.c2p(A_VAL, 0.08),
                      color=C_TICK, stroke_width=2.2)
        label_a = MathTex(r"a", color=C_TICK, font_size=22)
        label_a.next_to(ax.c2p(A_VAL, 0), DOWN, buff=0.17)

        self.play(Create(tick_a), FadeIn(label_a))
        self.wait(0.2)

        
        tick_x = Line(ax.c2p(X_VAL, -0.08), ax.c2p(X_VAL, 0.08),
                      color=C_TICK, stroke_width=2.2)
        label_x = MathTex(r"x", color=C_TICK, font_size=22)
        label_x.next_to(ax.c2p(X_VAL, 0), DOWN, buff=0.17)

        self.play(Create(tick_x), FadeIn(label_x))

        
        vert_a_line = Line(ax.c2p(A_VAL, 0), ax.c2p(A_VAL, f(A_VAL)),
                           color=C_EDGE, stroke_width=2.0)
        self.play(Create(vert_a_line))

        
        eq_Ax = MathTex(r"A(x) = \int_a^x f(t)\,dt",
                        color=C_WHITE, font_size=23)
        eq_Ax.move_to(UP * AX_DEF_Y)

        
        N_STEPS  = 60
        fill_dur = 1.3
        dt       = fill_dur / N_STEPS

        area        = ax.get_area(curve, x_range=[A_VAL, A_VAL + 1e-4],
                                  color=C_AREA, opacity=0.45)
        vert_x_line = Line(ax.c2p(A_VAL, 0), ax.c2p(A_VAL, f(A_VAL)),
                           color=C_EDGE, stroke_width=2.0)
        self.add(area, vert_x_line)

        
        self.play(FadeIn(eq_Ax, shift=DOWN * 0.07), run_time=0.45)

        xs = [A_VAL + (X_VAL - A_VAL) * i / N_STEPS for i in range(1, N_STEPS + 1)]
        for x in xs:
            new_area = ax.get_area(curve, x_range=[A_VAL, x],
                                   color=C_AREA, opacity=0.45)
            new_vert = Line(ax.c2p(x, 0), ax.c2p(x, f(x)),
                            color=C_EDGE, stroke_width=2.0)
            self.remove(area, vert_x_line)
            area        = new_area
            vert_x_line = new_vert
            self.add(area, vert_x_line)
            self.wait(dt)

        self.wait(0.4)

        
        self.play(FadeOut(VGroup(label_fx, vert_a_line, vert_x_line)), run_time=0.5)

        ftc1_eq = MathTex(
            r"\frac{d}{dx}\int_a^x f(t)\,dt = f(x)",
            color=C_WHITE, font_size=23
        )
        ftc1_eq.move_to(DOWN * 1.00)

        ftc1_bg, ftc1_lbl = labeled_box(ftc1_eq, "FTC 1", C_FTC1)

        self.play(FadeIn(ftc1_eq))
        self.play(Create(ftc1_bg), FadeIn(ftc1_lbl))
        self.wait(0.4)

        
        mvt_eq = MathTex(
            r"\text{if }G'(x)=f(x),\ \text{then }G(x)=A(x)+C",
            color=C_WHITE, font_size=23
        )
        mvt_eq.move_to(DOWN * 2.15)

        mvt_bg, mvt_lbl = labeled_box(mvt_eq, "Mean Value Theorem", C_MVT)

        self.play(FadeIn(mvt_eq))
        self.play(Create(mvt_bg), FadeIn(mvt_lbl))
        self.wait(0.4)

        
        self.play(
            FadeOut(VGroup(tick_a, label_a, tick_x, label_x,
                           ax, curve, area)),
            run_time=0.6
        )

        
        
        ftc1_group = VGroup(ftc1_eq, ftc1_bg, ftc1_lbl)
        mvt_group  = VGroup(mvt_eq,  mvt_bg,  mvt_lbl)

        ftc1_shift = UP * EQ_Y[0] - ftc1_eq.get_center()
        mvt_shift  = UP * EQ_Y[1] - mvt_eq.get_center()

        self.play(
            ftc1_group.animate.shift(ftc1_shift),
            mvt_group.animate.shift(mvt_shift),
            run_time=0.65
        )

        
        line1 = MathTex(
            r"G(b) - G(a)",   
            r"=",              
            r"\bigl[A(b)",     
            r"+",              
            r"C\bigr]",       
            r"-",              
            r"\bigl[A(a)",     
            r"+",              
            r"C\bigr]",       
            font_size=25, color=C_WHITE
        )
        line1.move_to(UP * EQ_Y[2])

        self.play(FadeIn(line1), run_time=0.7)
        self.wait(0.4)

        st_c1 = strikethrough(line1[4])
        st_c2 = strikethrough(line1[8])
        self.play(Create(st_c1), Create(st_c2), run_time=0.65)
        self.wait(0.35)

        
        line2 = MathTex(
            r"G(b) - G(a)",   
            r"=",              
            r"A(b)",           
            r"-",              
            r"A(a)",           
            font_size=25, color=C_WHITE
        )
        line2.move_to(line1.get_center())

        self.play(
            ReplacementTransform(
                VGroup(line1[0], line1[1], line1[2], line1[3],
                       line1[4], line1[5], line1[6], line1[7], line1[8],
                       st_c1, st_c2),
                line2
            ),
            run_time=0.85
        )
        self.wait(0.4)

        
        line3 = MathTex(
            r"G(b) - G(a)",           
            r"=",                      
            r"\int_a^b\! f(t)\,dt",   
            r"-",                      
            r"\int_a^a\! f(t)\,dt",   
            font_size=25, color=C_WHITE
        )
        line3.move_to(line2.get_center())

        self.play(eq_Ax.animate.set_color(C_AREA).scale(1.08), run_time=0.30)
        self.play(
            ReplacementTransform(line2, line3),
            eq_Ax.animate.set_color(C_WHITE).scale(1 / 1.08),
            run_time=0.90
        )
        self.wait(0.45)

        
        line3b = MathTex(
            r"G(b) - G(a)",           
            r"=",                      
            r"\int_a^b\! f(t)\,dt",   
            r"-",                      
            r"0",                      
            font_size=25, color=C_WHITE
        )
        line3b.move_to(line3.get_center())
        line3b[3].set_color(C_STRIKE)
        line3b[4].set_color(C_STRIKE)

        self.play(
            ReplacementTransform(
                VGroup(line3[0], line3[1], line3[2], line3[3], line3[4]),
                line3b
            ),
            run_time=0.7
        )
        self.wait(0.4)

        self.play(
            FadeOut(VGroup(line3b[3], line3b[4])),
            run_time=0.6
        )
        self.wait(0.35)

        
        
        
        
        
        

        final_eq = MathTex(
            r"\int_a^b f(t)\,dt",   
            r"=",                    
            r"G(b) - G(a)",         
            font_size=25, color=C_WHITE
        )
        final_eq.move_to(UP * EQ_Y[2])   

        
        self.play(
            ReplacementTransform(line3b[2], final_eq[0]),
            ReplacementTransform(line3b[1], final_eq[1]),
            ReplacementTransform(line3b[0], final_eq[2]),
            run_time=0.9
        )
        self.wait(0.3)

        
        final_box = SurroundingRectangle(
            final_eq, color=C_FINAL,
            stroke_width=2.0, buff=0.20, corner_radius=0.10
        )
        final_box.set_fill(C_FINAL, opacity=0.09)

        ftc2_lbl = Text(
            "Fundamental Theorem of Calculus – Part 2",
            font_size=16, color=C_FINAL
        )
        ftc2_lbl.next_to(final_box, DOWN, buff=0.18)

        self.play(Create(final_box))
        self.play(FadeIn(ftc2_lbl))
        self.wait(2.5)