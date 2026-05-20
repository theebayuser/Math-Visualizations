from manim import *


class EulersFormulaReels(ThreeDScene):
    def construct(self):

        # ═══════════════════════════════════════════════════════════════════
        # 1.  STATIC SETUP — everything already on screen at frame 0
        # ═══════════════════════════════════════════════════════════════════
        title = MathTex(r"\mathbb{E}\text{uler's } \mathbb{F}\text{ormula}").scale(0.9)
        title.set_color_by_gradient(GREEN, BLUE, PURPLE)
        title.to_edge(UP, buff=0.5)

        formula = MathTex(
            r"(", r"e^{ix}", r"=", r"\cos x", r"+", r"i \cdot \sin x", r")"
        ).scale(0.7)
        formula.next_to(title, DOWN, buff=0.2)
        formula.set_color_by_tex("e^{ix}",          GREEN)
        formula.set_color_by_tex(r"\cos x",         BLUE)
        formula.set_color_by_tex(r"i \cdot \sin x", RED)

        axes = ThreeDAxes(
            x_range=[0, 15, 2],
            y_range=[-1.5, 1.5, 1],
            z_range=[-1.5, 1.5, 1],
            x_length=4.5,
            y_length=2.5,
            z_length=2.5,
        )
        axes.move_to(DOWN * 0.5)

        re_label = MathTex("Re").scale(0.7).next_to(axes.y_axis.get_end(), RIGHT, buff=0.1)
        im_label = MathTex("Im").scale(0.7).next_to(axes.z_axis.get_end(), UP,    buff=0.1)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        self.add_fixed_in_frame_mobjects(title, formula)
        self.add(title, formula, axes, re_label, im_label)

        # Slow ambient rotation from frame 0.
        # rate is in rad/s; 0.04 ≈ 2.3°/s — leisurely but clearly moving.
        self.begin_ambient_camera_rotation(rate=0.04)

        # ═══════════════════════════════════════════════════════════════════
        # 2.  cos & sin CURVES — drawn simultaneously
        # ═══════════════════════════════════════════════════════════════════
        cos_curve = axes.plot_parametric_curve(
            lambda t: np.array([t, np.cos(t), 0]),
            t_range=[0, 14], color=BLUE,
        )
        sin_curve = axes.plot_parametric_curve(
            lambda t: np.array([t, 0, np.sin(t)]),
            t_range=[0, 14], color=RED,
        )

        cos_label = MathTex(r"\cos(x)", color=BLUE).scale(0.6)
        cos_label.move_to(axes.c2p(14, np.cos(14), 0))
        cos_label.shift(UP * 0.35)

        sin_label = MathTex(r"\sin(x)", color=RED).scale(0.6)
        sin_label.move_to(axes.c2p(14, 0, np.sin(14)))
        sin_label.shift(UP * 0.35)

        self.play(Create(cos_curve), Create(sin_curve), run_time=1.2)
        self.play(FadeIn(cos_label), FadeIn(sin_label), run_time=0.5)

        # ═══════════════════════════════════════════════════════════════════
        # 3.  UNIT CIRCLE + snap geometry + ALL pulses simultaneously
        # ═══════════════════════════════════════════════════════════════════
        unit_circle = axes.plot_parametric_curve(
            lambda theta: np.array([0, np.cos(theta), np.sin(theta)]),
            t_range=[0, 2 * PI],
            color=WHITE, stroke_opacity=0.5,
        )

        t_snap      = PI / 4
        snap_pt     = axes.c2p(0, np.cos(t_snap), np.sin(t_snap))
        snap_origin = axes.c2p(0, 0, 0)
        snap_cos_pt = axes.c2p(0, np.cos(t_snap), 0)
        snap_sin_pt = axes.c2p(0, 0, np.sin(t_snap))

        snap_radius   = Line(snap_origin, snap_pt, color=GREEN, stroke_width=4)
        snap_dot      = Dot3D(snap_pt, color=GREEN, radius=0.08)
        snap_cos_drop = DashedLine(snap_pt, snap_cos_pt, color=BLUE, stroke_width=3)
        snap_sin_drop = DashedLine(snap_pt, snap_sin_pt, color=RED,  stroke_width=3)
        snap_cos_end  = Dot3D(snap_cos_pt, color=BLUE, radius=0.07)
        snap_sin_end  = Dot3D(snap_sin_pt, color=RED,  radius=0.07)

        self.play(
            Create(unit_circle),
            Create(snap_radius),
            Create(snap_dot),
            Create(snap_cos_drop),
            Create(snap_sin_drop),
            FadeIn(snap_cos_end),
            FadeIn(snap_sin_end),
            Indicate(formula.get_part_by_tex(r"\cos x"),         color=BLUE,  scale_factor=1.6),
            Indicate(formula.get_part_by_tex(r"i \cdot \sin x"), color=RED,   scale_factor=1.6),
            Indicate(formula.get_part_by_tex("e^{ix}"),          color=GREEN, scale_factor=1.6),
            Indicate(cos_label, color=BLUE,  scale_factor=1.4),
            Indicate(sin_label, color=RED,   scale_factor=1.4),
            ShowPassingFlash(cos_curve.copy().set_stroke(color=BLUE,  width=8), time_width=0.4),
            ShowPassingFlash(sin_curve.copy().set_stroke(color=RED,   width=8), time_width=0.4),
            ShowPassingFlash(unit_circle.copy().set_color(GREEN).set_stroke(width=7), time_width=0.6),
            run_time=1.5,
        )

        self.play(
            FadeOut(snap_dot), FadeOut(snap_radius),
            FadeOut(snap_cos_drop), FadeOut(snap_cos_end),
            FadeOut(snap_sin_drop), FadeOut(snap_sin_end),
            run_time=0.3,
        )

        # ═══════════════════════════════════════════════════════════════════
        # 4.  DYNAMIC TRACE ELEMENTS
        # ═══════════════════════════════════════════════════════════════════
        t_tracker = ValueTracker(0.01)

        helix = always_redraw(lambda: axes.plot_parametric_curve(
            lambda t: np.array([t, np.cos(t), np.sin(t)]),
            t_range=[0, t_tracker.get_value()],
            color=GREEN,
        ))
        dot_3d = always_redraw(lambda: Dot3D(
            axes.c2p(t_tracker.get_value(),
                     np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            color=GREEN, radius=0.08,
        ))
        radius_vector = always_redraw(lambda: Line(
            axes.c2p(0, 0, 0),
            axes.c2p(0, np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            color=GREEN, stroke_width=4,
        ))
        dot_2d = always_redraw(lambda: Dot3D(
            axes.c2p(0, np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            color=GREEN, radius=0.08,
        ))
        extrusion_line = always_redraw(lambda: DashedLine(
            axes.c2p(0, np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            axes.c2p(t_tracker.get_value(),
                     np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            color=WHITE, stroke_opacity=0.5,
        ))
        line_cos = always_redraw(lambda: DashedLine(
            axes.c2p(t_tracker.get_value(),
                     np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            axes.c2p(t_tracker.get_value(), np.cos(t_tracker.get_value()), 0),
            color=BLUE,
        ))
        line_sin = always_redraw(lambda: DashedLine(
            axes.c2p(t_tracker.get_value(),
                     np.cos(t_tracker.get_value()),
                     np.sin(t_tracker.get_value())),
            axes.c2p(t_tracker.get_value(), 0, np.sin(t_tracker.get_value())),
            color=RED,
        ))

        label_static  = MathTex(r"e^{i \cdot}", color=GREEN).scale(0.8)
        label_dynamic = DecimalNumber(0, num_decimal_places=2, color=GREEN).scale(0.8)
        label_group   = VGroup(label_static, label_dynamic).arrange(RIGHT, buff=0.05)

        def update_label(mob):
            label_dynamic.set_value(t_tracker.get_value())
            mob.arrange(RIGHT, buff=0.05)
            mob.move_to(axes.c2p(t_tracker.get_value(),
                                 np.cos(t_tracker.get_value()),
                                 np.sin(t_tracker.get_value())))
            mob.shift(UP * 0.5 + RIGHT * 0.3)

        label_group.add_updater(update_label)

        self.add(helix, dot_3d, radius_vector, dot_2d,
                 extrusion_line, line_cos, line_sin, label_group)

        # ═══════════════════════════════════════════════════════════════════
        # 5.  SWEEP 1 — trace to x=π  +  camera to flat 2-D circle view
        # ═══════════════════════════════════════════════════════════════════
        # Stop ambient drift so explicit camera animation has full control.
        self.stop_ambient_camera_rotation()
        self.play(
            t_tracker.animate(rate_func=linear).set_value(PI),
            self.camera.theta_tracker.animate(rate_func=smooth).set_value(120 * DEGREES),
            self.camera.phi_tracker.animate(rate_func=smooth).set_value(75 * DEGREES),
            run_time=5,
        )

        # ═══════════════════════════════════════════════════════════════════
        # 6.  EULER'S IDENTITY DERIVATION
        #     Camera pauses briefly at the flat view, then ambient rotation
        #     resumes partway through the derivation steps.
        # ═══════════════════════════════════════════════════════════════════

        EQ_POS = DOWN * 2.1

        # ── Step A:  e^{iπ} = cos π + i·sin π ───────────────────────────
        step_a = MathTex(
            r"e^{i\pi}", r"=", r"\cos\pi", r"+", r"i\cdot\sin\pi",
            font_size=34,
        )
        step_a.set_color_by_tex(r"e^{i\pi}",      GREEN)
        step_a.set_color_by_tex(r"\cos\pi",        BLUE)
        step_a.set_color_by_tex(r"i\cdot\sin\pi", RED)
        step_a.move_to(EQ_POS)

        formula_copy = formula.copy()
        self.add_fixed_in_frame_mobjects(formula_copy)
        self.add_fixed_in_frame_mobjects(step_a)
        self.remove(step_a)
        self.play(
            TransformFromCopy(formula_copy, step_a),
            run_time=1,
        )
        self.remove(formula_copy)
        self.wait(0.2)

        # Camera has been still since sweep-1 ended — resume slow rotation
        # now, mid-derivation, so it's clearly moving before step D lands.
        self.begin_ambient_camera_rotation(rate=0.04)

        # ── Step B:  e^{iπ} = −1 + i·0 ──────────────────────────────────
        step_b = MathTex(
            r"e^{i\pi}", r"=", r"-1", r"+", r"i\cdot 0",
            font_size=34,
        )
        step_b.set_color_by_tex(r"e^{i\pi}", GREEN)
        step_b.set_color_by_tex(r"-1",       BLUE)
        step_b.set_color_by_tex(r"i\cdot 0", RED)
        step_b.move_to(EQ_POS)

        self.add_fixed_in_frame_mobjects(step_b)
        self.remove(step_b)
        self.play(ReplacementTransform(step_a, step_b), run_time=0.6)
        self.wait(0.2)

        # ── Step C:  e^{iπ} = −1 ─────────────────────────────────────────
        step_c = MathTex(
            r"e^{i\pi}", r"=", r"-1",
            font_size=34,
        )
        step_c.set_color_by_tex(r"e^{i\pi}", GREEN)
        step_c.move_to(EQ_POS)

        self.add_fixed_in_frame_mobjects(step_c)
        self.remove(step_c)
        self.play(ReplacementTransform(step_b, step_c), run_time=0.6)
        self.wait(0.25)

        # ── Step D:  e^{iπ} + 1 = 0  (white, inside teal box) ───────────
        step_d = MathTex(
            r"e^{i\pi}", r"+", r"1", r"=", r"0",
            font_size=38,
        )
        step_d.set_color(WHITE)
        step_d.move_to(EQ_POS)

        self.add_fixed_in_frame_mobjects(step_d)
        self.remove(step_d)
        self.play(ReplacementTransform(step_c, step_d), run_time=0.75)
        self.wait(0.5)

        # ── Box + "Euler's Identity" label  (matches screenshot style) ───
        # Dark teal fill, rounded corners, cyan/teal border, white italic label.
        TEAL_DARK   = ManimColor("#0d2b35")
        TEAL_BORDER = ManimColor("#3bbfcf")

        box_bg = RoundedRectangle(
            corner_radius=0.18,
            width=3.8, height=1.1,
            fill_color=TEAL_DARK, fill_opacity=0.92,
            stroke_color=TEAL_BORDER, stroke_width=3,
        )
        id_label = Text(
            "Euler's Identity",
            font="Georgia",
            font_size=16,
            color=WHITE,
            slant=ITALIC,
        )

        box_bg.move_to(EQ_POS + DOWN * 0.2)
        step_d.move_to(box_bg.get_center() + UP * 0.15)
        id_label.next_to(box_bg, DOWN, buff=0.1)

        box_bg.z_index   = -1
        step_d.z_index   =  1
        id_label.z_index =  1

        self.add_fixed_in_frame_mobjects(box_bg, id_label)
        self.play(
            FadeIn(box_bg),
            FadeIn(id_label),
            run_time=0.4,
        )
        self.wait(0.4)
        identity_group = VGroup(box_bg, id_label, step_d)
        self.play(
            FadeOut(identity_group, run_time=1),
            run_time=0.5,
        )

        # ═══════════════════════════════════════════════════════════════════
        # 7.  SWEEP 2 — finish helix to t=14, pull back to isometric.
        #     Ambient rotation is already running. Fade out identity early.
        # ═══════════════════════════════════════════════════════════════════
        

        self.play(
            t_tracker.animate(rate_func=linear).set_value(14),
            self.camera.theta_tracker.animate(rate_func=smooth).set_value(300 * DEGREES),
            self.camera.phi_tracker.animate(rate_func=smooth).set_value(65 * DEGREES),
            run_time=7,
        )

        self.wait(2)