from manim import *

class IntegrationByPartsProof(Scene):
    def construct(self):
        # --- 1. CONFIGURATION ---
        # Explicit Pure Black Background
        self.camera.background_color = BLACK
        
        # Color Palette
        c_curve = WHITE
        c_vdu = TEAL_C     # Green-ish (Area under curve)
        c_udv = MAROON_B   # Red-ish (Area left of curve)
        c_total = BLUE     # qs (The Big Rectangle)
        c_void = PURPLE    # pr (The Small Rectangle)
        c_axes = GRAY_B
        c_text = GRAY_A

        # Title - Moved higher up (buff reduced to 0.35)
        title = Tex(r"$\mathbb{I}$ntegration by $\mathbb{P}$arts", font_size=40)
        title.set_color_by_gradient(TEAL, RED)
        title.to_edge(UP, buff=0.35)

        # --- 2. COORDINATE SYSTEM ---
        ax = Axes(
            x_range=[0, 5], y_range=[0, 5],
            x_length=4.5, y_length=4.5,
            axis_config={"include_numbers": False, "tip_shape": StealthTip, "color": c_axes}
        )
        
        # Labels
        lab_u = ax.get_x_axis_label("u", edge=RIGHT, direction=DOWN + RIGHT, buff=0).scale(0.8)
        lab_v = ax.get_y_axis_label("v", edge=UP, direction=UP + LEFT, buff=0).scale(0.8)

        # Curve Function: v = 0.2*u^2 + 1
        func = lambda u: 0.2 * u**2 + 1.0
        val_p, val_q = 1.5, 3.8
        val_r, val_s = func(val_p), func(val_q)

        # Precise Coordinates
        pt_origin = ax.c2p(0, 0)
        pt_p = ax.c2p(val_p, 0)
        pt_q = ax.c2p(val_q, 0)
        pt_r = ax.c2p(0, val_r)
        pt_s = ax.c2p(0, val_s)
        pt_corner_qs = ax.c2p(val_q, val_s) # Top right of big rect
        pt_corner_pr = ax.c2p(val_p, val_r) # Top right of small rect

        # --- 3. VISUAL OBJECTS ---
        curve = ax.plot(func, x_range=[val_p, val_q], color=c_curve, stroke_width=3)
        
        # Labels for p, q, r, s
        lbl_p = MathTex("p=f(a)", font_size=18, color=c_text).next_to(pt_p, DOWN, buff=0.15)
        lbl_q = MathTex("q=f(b)", font_size=18, color=c_text).next_to(pt_q, DOWN, buff=0.15)
        lbl_r = MathTex("r=g(a)", font_size=18, color=c_text).next_to(pt_r, LEFT, buff=0.15)
        lbl_s = MathTex("s=g(b)", font_size=18, color=c_text).next_to(pt_s, LEFT, buff=0.15)

        # Parametric Label
        lbl_curve = MathTex(
            r"\begin{cases} u=f(x) \\ v=g(x) \end{cases}", 
            font_size=20, color=c_curve
        ).next_to(curve.get_end(), UP, buff=0.1).shift(LEFT*0.5)

        # --- 4. GEOMETRIC SHAPES ---
        # Integrals
        area_vdu = ax.get_area(curve, x_range=[val_p, val_q], color=c_vdu, opacity=0.8)
        pts_udv = [pt_r, pt_s] + list(reversed(curve.get_points()))
        area_udv = Polygon(*pts_udv, color=c_udv, fill_opacity=0.8, stroke_width=0)

        # Small Rectangle (pr) - INITIALLY BLACK (HOLE)
        # Matches background color exactly
        rect_pr_poly = Polygon(
            pt_origin, pt_p, pt_corner_pr, pt_r,
            stroke_color=GRAY, stroke_width=1, fill_color=BLACK, fill_opacity=1.0
        )

        # Big Rectangle (qs) - Invisible initially
        rect_qs_poly = Polygon(
            pt_origin, pt_q, pt_corner_qs, pt_s,
            stroke_width=0, fill_color=c_total, fill_opacity=0.3
        )

        # --- 5. FORMULA OBJECTS ---
        # Eq 1 Parts
        t_intu = MathTex(r"\int_{r}^{s} u \, dv", color=c_udv).scale(0.7)
        t_plus = MathTex(r"+").scale(0.7)
        t_intv = MathTex(r"\int_{p}^{q} v \, du", color=c_vdu).scale(0.7)
        t_eq   = MathTex(r"=").scale(0.7)
        t_qs   = MathTex(r"qs", color=c_total).scale(0.7)
        t_sub  = MathTex(r"-").scale(0.7)
        t_pr   = MathTex(r"pr", color=c_void).scale(0.7)
        
        eq1_group = VGroup(t_intu, t_plus, t_intv, t_eq, t_qs, t_sub, t_pr).arrange(RIGHT, buff=0.15)

        # Equations 2, 3, 4
        eq2 = MathTex(r"\int_{r}^{s} u \, dv", r"=", r"(qs - pr)", r"-", r"\int_{p}^{q} v \, du").scale(0.7)
        eq2[0].set_color(c_udv); eq2[2].set_color(WHITE); eq2[4].set_color(c_vdu)

        eq3 = MathTex(r"\int_{r}^{s} u \, dv", r"=", r"uv \Big|_{(p,r)}^{(q,s)}", r"-", r"\int_{p}^{q} v \, du").scale(0.7)
        eq3[0].set_color(c_udv); eq3[2].set_color(c_total); eq3[4].set_color(c_vdu)

        eq4 = MathTex(r"\int u \, dv", r"=", r"uv", r"-", r"\int v \, du").scale(0.9)
        eq4[0].set_color(c_udv); eq4[2].set_color(c_total); eq4[4].set_color(c_vdu)

        # --- 6. LAYOUT ---
        # Add rect_qs_poly to group but set opacity 0 so it's hidden but positioned
        rect_qs_poly.set_opacity(0)

        # Group all graph elements to center them
        graph_group = VGroup(
            ax, curve, lab_u, lab_v, 
            lbl_p, lbl_q, lbl_r, lbl_s, 
            area_vdu, area_udv, rect_pr_poly, rect_qs_poly,
            lbl_curve # Add label to group to scale with it
        )
        graph_group.scale(0.85).move_to(ORIGIN).shift(UP*0.6)
        
        # Position formulas relative to the centered graph
        eq1_group.next_to(graph_group, DOWN, buff=0.4)
        for e in [eq2, eq3, eq4]: e.move_to(eq1_group)

        # --- 7. ANIMATION SEQUENCE ---
        
        # A. Setup (0s - 2.5s)
        self.play(Write(title), run_time=1)
        self.play(
            Create(ax), 
            FadeIn(lab_u), FadeIn(lab_v),
            FadeIn(lbl_p), FadeIn(lbl_q), FadeIn(lbl_r), FadeIn(lbl_s),
            run_time=1.5
        )
        
        # B. Curve & Label (2.5s - 4.5s)
        self.play(Create(curve), run_time=1.0)
        self.play(Write(lbl_curve), run_time=1.0)
        self.wait(0.5)

        # C. Geometric Areas (4.5s - 7.5s)
        self.play(
            FadeIn(area_udv), 
            FadeIn(area_vdu), 
            FadeIn(rect_pr_poly), # Appears as black cutout
            run_time=1.5
        )
        self.wait(1.0)

        # D. Equation 1 Building (7.5s - 13.5s)
        # Left Side: Integrals
        self.play(
            TransformFromCopy(area_udv, t_intu),
            Write(t_plus),
            TransformFromCopy(area_vdu, t_intv),
            Write(t_eq),
            run_time=1.5
        )
        
        # Right Side: qs (Blue Big Rectangle)
        self.play(rect_qs_poly.animate.set_opacity(0.3).set_color(c_total), run_time=0.5)
        self.play(Indicate(rect_qs_poly, color=c_total), run_time=0.5)
        self.play(
            TransformFromCopy(rect_qs_poly, t_qs),
            rect_qs_poly.animate.set_opacity(0), # Hide helper
            run_time=1.0
        )
        
        # Right Side: pr (Small Rect turning Purple momentarily)
        self.play(Write(t_sub), run_time=0.2)
        # Flash purple to show what is being subtracted
        self.play(rect_pr_poly.animate.set_fill(c_void, opacity=0.8), run_time=0.5)
        self.play(Indicate(rect_pr_poly, color=c_void), run_time=0.5)
        self.play(
            TransformFromCopy(rect_pr_poly, t_pr),
            rect_pr_poly.animate.set_fill(BLACK, opacity=1.0), # Return to void
            run_time=1.0
        )
        self.wait(1.0)

        # E. Transformations (13.5s - 25s)
        # Rearrange
        self.play(TransformMatchingTex(eq1_group, eq2), run_time=1.5)
        self.wait(0.5)
        
        # Limits
        self.play(TransformMatchingTex(eq2, eq3), run_time=1.5)
        self.wait(0.5)
        
        # Final Formula
        self.play(TransformMatchingTex(eq3, eq4), run_time=1.5)
        self.play(Indicate(eq4, color=WHITE), run_time=1.0)
        
        self.wait(2)