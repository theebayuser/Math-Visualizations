from manim import *
import numpy as np

class SineOfSumProof(Scene):
    def construct(self):
        
        self.camera.background_color = "#000000"
        
        
        MAX_WIDTH = 4.5
        
        
        C_CIRCLE = WHITE
        C_RADIUS = WHITE
        C_TRIANGLE = WHITE
        C_ALTITUDE = GREY_B
        C_X = TEAL_A
        C_Y = MAROON_A
        C_Z = PURPLE_A
        
        
        C_VAR_A = RED_D      
        C_VAR_B = BLUE_D     
        C_SIDE_C = GOLD_D    
        
        
        R = 1.8 
        DIAGRAM_POS = UP * 1.4 
        
        
        EQ_MAIN_POS = DOWN * 1.0           
        EQ_LOWER_POS = DOWN * 2.4          
        EQ_BOTTOM_POS = DOWN * 3.3         
        EQ_TOP_POS = UP * 0.1
        
        
        val_x = 60
        val_y = 45
        val_z = 180 - (val_x + val_y) 
        
        rad_x = val_x * DEGREES
        rad_y = val_y * DEGREES
        
        
        theta_C = (270 + val_z) * DEGREES
        theta_B = (270 - val_z) * DEGREES
        theta_A = theta_C + 2 * rad_x 
        
        pt_O = DIAGRAM_POS
        pt_A = pt_O + R * np.array([np.cos(theta_A), np.sin(theta_A), 0])
        pt_B = pt_O + R * np.array([np.cos(theta_B), np.sin(theta_B), 0])
        pt_C = pt_O + R * np.array([np.cos(theta_C), np.sin(theta_C), 0])
        pt_D = np.array([pt_A[0], pt_B[1], 0]) 
        pt_M = (pt_B + pt_C) / 2                
        
        def fit(mobj):
            if mobj.width > MAX_WIDTH:
                mobj.scale(MAX_WIDTH / mobj.width)
            return mobj

        
        title = Tex(r"$\mathbb{S}$ine $\mathbb{S}$um $\mathbb{I}$dentities", font_size=44)
        title.set_color_by_gradient(BLUE, RED)
        title.to_edge(UP, buff=0.1)
        self.add(title)
        
        center_dot = Dot(pt_O, color=C_CIRCLE, radius=0.05)
        
        
        radius_lbl = MathTex("r = 1/2", font_size=24, color=C_RADIUS).next_to(pt_O, UP, buff=0.15)
        
        
        radius_draw = Line(pt_O, pt_B, color=C_RADIUS)
        
        self.play(Create(center_dot), Create(radius_draw), Write(radius_lbl))
        
        
        circle = Circle(radius=R, color=C_CIRCLE, stroke_opacity=0.8).move_to(pt_O)
        
        circle.rotate(theta_B, about_point=pt_O)
        
        
        self.play(
            Rotate(radius_draw, angle=2*PI, about_point=pt_O, run_time=1.5), 
            Create(circle),
            run_time=1.5
        )
        

        line_BC = Line(pt_B, pt_C, color=C_SIDE_C)
        line_AB = Line(pt_A, pt_B, color=C_VAR_B)
        line_AC = Line(pt_A, pt_C, color=C_VAR_A)
        
        lbl_c = MathTex("c", color=C_SIDE_C, font_size=28).next_to(line_BC, DOWN, buff=0.1)
        lbl_b = MathTex("b", color=C_VAR_B, font_size=28).next_to(line_AB.get_center(), LEFT, buff=0.1)
        lbl_a = MathTex("a", color=C_VAR_A, font_size=28).next_to(line_AC.get_center(), RIGHT, buff=0.1)
        
        
        arc_x = Angle(Line(pt_B, pt_C), Line(pt_B, pt_A), radius=0.5, color=C_X)
        txt_x = MathTex("x", color=C_X, font_size=24).next_to(arc_x, UP+RIGHT, buff=0.05)
        arc_y = Angle(Line(pt_C, pt_A), Line(pt_C, pt_B), radius=0.5, color=C_Y)
        txt_y = MathTex("y", color=C_Y, font_size=24).next_to(arc_y, UP+LEFT, buff=0.05)
        arc_z = Angle(Line(pt_A, pt_B), Line(pt_A, pt_C), radius=0.5, color=C_Z)
        txt_z = MathTex("z", color=C_Z, font_size=24).next_to(arc_z, DOWN, buff=0.1)
        
        
        self.play(Create(line_BC), Create(line_AB), Create(line_AC))
        self.play(
            Write(lbl_c), Write(lbl_b), Write(lbl_a),
            Create(arc_x), Write(txt_x), Create(arc_y), Write(txt_y), Create(arc_z), Write(txt_z)
        )
        
        alt_A = DashedLine(pt_A, pt_D, color=C_ALTITUDE)
        perp_A = RightAngle(line_BC, alt_A, length=0.1, quadrant=(-1,-1))
        alt_O = DashedLine(pt_O, pt_M, color=C_ALTITUDE)
        perp_O = RightAngle(line_BC, alt_O, length=0.1, quadrant=(-1,-1))
        
        rad_C = Line(pt_O, pt_C, color=C_RADIUS, stroke_opacity=0.4)
        rad_B = Line(pt_O, pt_B, color=C_RADIUS, stroke_opacity=0.4)
        
        
        self.play(
            Create(alt_A), FadeIn(perp_A),
            Create(alt_O), FadeIn(perp_O)
        )
        self.play(Create(rad_B))
        
        
        arc_2z = Angle(rad_B, rad_C, radius=0.3, color=C_Z)
        lbl_2z = MathTex("2z", color=C_Z, font_size=24).next_to(arc_2z, UP, buff=0.05)
        
        self.play(Create(rad_C), Create(arc_2z), Write(lbl_2z))
        
        arc_small_z = Angle(alt_O, rad_C, radius=0.3, color=C_Z)
        lbl_small_z = MathTex("z", color=C_Z, font_size=24).next_to(arc_small_z, RIGHT+DOWN, buff=0.05)
        
        eq_z_1 = MathTex(r"\sin z", r"=", r"\frac{c/2}{r}", font_size=32).move_to(EQ_MAIN_POS)
        
        self.play(
            Transform(arc_2z, arc_small_z), 
            ReplacementTransform(lbl_2z, lbl_small_z),
            Write(eq_z_1)
        )
        
        
        eq_z_2 = MathTex(r"\sin z", r"=", r"\frac{c/2}{1/2}", font_size=32).move_to(EQ_MAIN_POS)
        self.play(
            Indicate(eq_z_1[2][4], color=C_RADIUS), 
            Indicate(radius_lbl, color=C_RADIUS),
            ReplacementTransform(eq_z_1, eq_z_2)
        )
        
        eq_z_3 = MathTex(r"\sin z", r"=", r"c", font_size=32).move_to(EQ_MAIN_POS)
        eq_z_3[2].set_color(C_SIDE_C)
        self.play(ReplacementTransform(eq_z_2, eq_z_3))
        
        
        line_BD = Line(pt_B, pt_D, color=C_VAR_B, stroke_width=4)
        brace_left = Brace(line_BD, DOWN, buff=0.05)
        txt_left = MathTex(r"b \cos x", color=C_VAR_B, font_size=24).next_to(brace_left, DOWN, buff=0.05)
        
        line_DC = Line(pt_D, pt_C, color=C_VAR_A, stroke_width=4)
        brace_right = Brace(line_DC, DOWN, buff=0.05)
        txt_right = MathTex(r"a \cos y", color=C_VAR_A, font_size=24).next_to(brace_right, DOWN, buff=0.05)
        
        
        self.play(
            eq_z_3.animate.scale(0.8).move_to(EQ_TOP_POS),
            Create(line_BD), GrowFromCenter(brace_left), Write(txt_left),
            Create(line_DC), GrowFromCenter(brace_right), Write(txt_right)
        )
        
        eq_main = MathTex(r"c", r"=", r"b", r"\cos x", r"+", r"a", r"\cos y", font_size=32)
        eq_main[0].set_color(C_SIDE_C)
        eq_main[2].set_color(C_VAR_B)
        eq_main[5].set_color(C_VAR_A)
        fit(eq_main).move_to(EQ_MAIN_POS)
        
        self.play(Write(eq_main))
        self.play(FadeOut(brace_left), FadeOut(txt_left), FadeOut(brace_right), FadeOut(txt_right))
        
        
        eq_sine_1 = MathTex(r"{a \over \sin x}", r"=", r"{b \over \sin y}", r"=", r"2r", font_size=32).move_to(EQ_LOWER_POS)
        
        
        sine_box = RoundedRectangle(
            corner_radius=0.15,
            width=eq_sine_1.width + 0.7,
            height=eq_sine_1.height + 0.8,
            color=BLUE,
            fill_opacity=0.15,
            stroke_width=2
        ).move_to(eq_sine_1)
        sine_label = Text("Extended Law of Sines", font_size=20, color=BLUE).next_to(sine_box, UP, buff=0.05)
        
        
        self.play(Write(fit(eq_sine_1)), Create(sine_box), Write(sine_label))
        self.wait(0.5)
        
        
        eq_sine_2 = MathTex(r"{a \over \sin x}", r"=", r"{b \over \sin y}", r"=", r"2(1/2)", font_size=32).move_to(EQ_LOWER_POS)
        self.play(
            Indicate(eq_sine_1[4][1], color=C_RADIUS), 
            Indicate(radius_lbl, color=C_RADIUS),
            ReplacementTransform(eq_sine_1, fit(eq_sine_2))
        )
        
        
        eq_sine_3 = MathTex(r"{a \over \sin x}", r"=", r"{b \over \sin y}", r"=", r"1", font_size=32).move_to(EQ_LOWER_POS)
        self.play(ReplacementTransform(eq_sine_2, fit(eq_sine_3)))
        
        eq_sine_final = MathTex(r"a = \sin x", r", \;", r"b = \sin y", font_size=32).move_to(EQ_LOWER_POS)
        eq_sine_final[0].set_color(C_VAR_A)
        eq_sine_final[2].set_color(C_VAR_B)
        self.play(
            ReplacementTransform(eq_sine_3, fit(eq_sine_final)),
            FadeOut(sine_box),
            FadeOut(sine_label)
        )
        
        
        eq_target = MathTex(r"c", r"=", r"\sin y", r"\cos x", r"+", r"\sin x", r"\cos y", font_size=32).move_to(EQ_MAIN_POS)
        eq_target[0].set_color(C_SIDE_C)
        eq_target[2].set_color(C_VAR_B)
        eq_target[5].set_color(C_VAR_A)
        
        self.play(
            ReplacementTransform(eq_main, fit(eq_target)),
            FadeOut(eq_sine_final)
        )
        
        
        eq_angle = MathTex(r"z = 180^\circ - (x+y)", font_size=32, color=C_Z).move_to(EQ_LOWER_POS)
        
        self.play(
            Write(eq_angle),
            Indicate(txt_x, color=C_X),
            Indicate(txt_y, color=C_Y),
            Indicate(txt_z, color=C_Z)
        )
        
        
        eq_sin_intermediate = MathTex(r"\sin z", r"=", r"\sin(180^\circ - (x+y))", r"=", r"\sin(x+y)", font_size=32).move_to(EQ_LOWER_POS)
        eq_sin_intermediate[0].set_color(C_Z)
        eq_sin_intermediate[4].set_color(C_SIDE_C)
        self.play(ReplacementTransform(eq_angle, fit(eq_sin_intermediate)))
        self.wait(0.5)
        
        
        eq_sin_simp = MathTex(r"\sin z", r"=", r"\sin(x+y)", font_size=32).move_to(EQ_LOWER_POS)
        eq_sin_simp[0].set_color(C_Z)
        eq_sin_simp[2].set_color(C_SIDE_C)
        self.play(ReplacementTransform(eq_sin_intermediate, fit(eq_sin_simp)))
        
        eq_c_sub = MathTex(r"c", r"=", r"\sin(x+y)", font_size=32).move_to(EQ_LOWER_POS)
        eq_c_sub[0].set_color(C_SIDE_C)
        eq_c_sub[2].set_color(C_SIDE_C)
        
        self.play(Indicate(eq_z_3), ReplacementTransform(eq_sin_simp, fit(eq_c_sub)))
        self.wait(1)
        
        
        final_eq = MathTex(
            r"\sin(x+y)", r"=", r"\sin y \cos x", r"+", r"\sin x \cos y",
            font_size=32
        ).move_to(EQ_MAIN_POS)
        
        final_eq[0].set_color(C_SIDE_C)
        final_eq[2][0:4].set_color(C_VAR_B)
        final_eq[4][0:4].set_color(C_VAR_A)
        fit(final_eq)

        
        self.play(
            ReplacementTransform(eq_c_sub, final_eq[0:1]), 
            ReplacementTransform(eq_target, final_eq[1:]),  
            FadeOut(eq_z_3),
            run_time=2
        )
        
        
        final_box = RoundedRectangle(
            corner_radius=0.2,
            width=final_eq.width + 0.4,
            height=final_eq.height + 0.5,
            color=GOLD,
            fill_opacity=0.2,
            stroke_width=3
        ).move_to(final_eq)
        
        self.play(Create(final_box))
        self.wait(4)