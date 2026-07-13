from manim import *
import numpy as np

class ThreeBodyProblem(Scene):
    def construct(self):
        # 1. Intriguing Hook (Kept vertically central for 9:16 cropping)
        hook = Tex("Is the universe predictable?", font_size=36, color=WHITE)
        hook_bg = BackgroundRectangle(hook, color=BLACK, fill_opacity=0.6, buff=0.2)
        hook_group = VGroup(hook_bg, hook).shift(UP * 2.5)

        # 2. Title with \mathbb and gradient
        title = Tex(r"The $\mathbb{T}$hree $\mathbb{B}$ody $\mathbb{P}$roblem", font_size=40)
        title.set_color_by_gradient(BLUE, MAROON, RED)
        title_bg = BackgroundRectangle(title, color=BLACK, fill_opacity=0.6, buff=0.2)
        title_group = VGroup(title_bg, title).shift(UP * 2.5)

        # Intro Sequence
        self.play(FadeIn(hook_group, shift=UP), run_time=1.5)
        self.wait(1.5)
        self.play(Transform(hook_group, title_group), run_time=1.5)
        self.wait(0.5)

        # 3. Setup Physics Bodies
        b1 = Dot(radius=0.08, color=BLUE)
        b2 = Dot(radius=0.08, color=RED)
        b3 = Dot(radius=0.08, color=YELLOW)

        # Initial Positions (Tight bounds to fit the middle vertical third)
        b1.pos = np.array([1.2, 0.5, 0.0])
        b2.pos = np.array([-1.2, 0.5, 0.0])
        b3.pos = np.array([0.0, -1.0, 0.0])

        # Initial Velocities (Sum equals 0 to prevent drifting off-screen)
        b1.v = np.array([-0.2, 0.6, 0.0])
        b2.v = np.array([-0.2, -0.6, 0.0])
        b3.v = np.array([0.4, 0.0, 0.0])

        for b in (b1, b2, b3):
            b.move_to(b.pos)

        # Glow Effects
        glow1 = Dot(radius=0.3, color=BLUE, fill_opacity=0.2)
        glow2 = Dot(radius=0.3, color=RED, fill_opacity=0.2)
        glow3 = Dot(radius=0.3, color=YELLOW, fill_opacity=0.2)
        
        glow1.add_updater(lambda m: m.move_to(b1.get_center()))
        glow2.add_updater(lambda m: m.move_to(b2.get_center()))
        glow3.add_updater(lambda m: m.move_to(b3.get_center()))

        # Orbital Traces
        trace1 = TracedPath(b1.get_center, stroke_color=BLUE, stroke_opacity=0.8, stroke_width=2.5)
        trace2 = TracedPath(b2.get_center, stroke_color=RED, stroke_opacity=0.8, stroke_width=2.5)
        trace3 = TracedPath(b3.get_center, stroke_color=YELLOW, stroke_opacity=0.8, stroke_width=2.5)

        self.add(trace1, trace2, trace3, glow1, glow2, glow3, b1, b2, b3)

        # 4. Custom Sub-stepped Physics Engine
        def physics_updater(mob, dt):
            # Clamp max dt to prevent simulation explosions on first frame drop
            if dt > 0.05: 
                dt = 0.016 
            
            substeps = 10
            sub_dt = dt / substeps
            G = 2.5
            epsilon = 0.15  # Softening to prevent slingshots to infinity

            for _ in range(substeps):
                p1, p2, p3 = b1.pos, b2.pos, b3.pos
                
                # Vectors between bodies
                d12 = p2 - p1
                d13 = p3 - p1
                d23 = p3 - p2

                r12 = np.linalg.norm(d12)
                r13 = np.linalg.norm(d13)
                r23 = np.linalg.norm(d23)

                # Newton's Law of Universal Gravitation
                a1 = G * (d12 / (r12**2 + epsilon**2)**1.5 + d13 / (r13**2 + epsilon**2)**1.5)
                a2 = G * (-d12 / (r12**2 + epsilon**2)**1.5 + d23 / (r23**2 + epsilon**2)**1.5)
                a3 = G * (-d13 / (r13**2 + epsilon**2)**1.5 - d23 / (r23**2 + epsilon**2)**1.5)

                # Update Velocities
                b1.v += a1 * sub_dt
                b2.v += a2 * sub_dt
                b3.v += a3 * sub_dt

                # Update Positions
                b1.pos += b1.v * sub_dt
                b2.pos += b2.v * sub_dt
                b3.pos += b3.v * sub_dt

            b1.move_to(b1.pos)
            b2.move_to(b2.pos)
            b3.move_to(b3.pos)

        # Run Simulation
        physics_engine = Mobject()
        physics_engine.add_updater(physics_updater)
        self.add(physics_engine)

        # Total wait time brings duration to ~24 seconds
        self.wait(18)

        # 5. Safe Teardown
        for m in list(self.mobjects):
            m.clear_updaters()
            
        self.play(
            *[FadeOut(m) for m in list(self.mobjects)],
            run_time=1.5
        )