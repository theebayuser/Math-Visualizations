from manim import *

class GroupTheoryOrder(ThreeDScene):
    def construct(self):
        # Set an aesthetically pleasing isometric-style camera angle
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1) # Slow rotation for a dynamic feel

        # Helper function to create a cubie with proper Rubik's Cube stickers
        def create_cubie(x, y, z):
            cubie = VGroup()
            size = 0.95
            
            # The core mechanism of the cubie (dark plastic)
            base = Cube(
                side_length=size, 
                fill_color=GREY_E, 
                fill_opacity=1, 
                stroke_width=2, 
                stroke_color=BLACK
            )
            cubie.add(base)
            
            # The colored stickers
            s_size = size * 0.85
            d = size / 2 + 0.01 # Offset slightly to prevent Z-fighting
            
            # Standard Western Color Scheme
            if x == 1:   # Right
                cubie.add(Square(side_length=s_size, fill_color=RED, fill_opacity=1, stroke_width=0).move_to(RIGHT*d).rotate(PI/2, UP))
            if x == -1:  # Left
                cubie.add(Square(side_length=s_size, fill_color=ORANGE, fill_opacity=1, stroke_width=0).move_to(LEFT*d).rotate(PI/2, UP))
            if y == 1:   # Up
                cubie.add(Square(side_length=s_size, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(UP*d).rotate(PI/2, RIGHT))
            if y == -1:  # Down
                cubie.add(Square(side_length=s_size, fill_color=YELLOW, fill_opacity=1, stroke_width=0).move_to(DOWN*d).rotate(PI/2, RIGHT))
            if z == 1:   # Front
                cubie.add(Square(side_length=s_size, fill_color=GREEN, fill_opacity=1, stroke_width=0).move_to(OUT*d))
            if z == -1:  # Back
                cubie.add(Square(side_length=s_size, fill_color=BLUE, fill_opacity=1, stroke_width=0).move_to(IN*d))
                
            # Place the finalized cubie in spatial alignment
            cubie.move_to(RIGHT * x + UP * y + OUT * z)
            return cubie

        # Generate the full 3x3x3 Cube
        cubies = VGroup()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    cubies.add(create_cubie(x, y, z))
                    
        # Helper function to render text with translucent backgrounds in fixed 3D space
        def make_fixed_text(mobj, y_pos):
            bg = BackgroundRectangle(mobj, color=BLACK, fill_opacity=0.75, buff=0.15)
            grp = VGroup(bg, mobj).move_to(UP * y_pos)
            self.add_fixed_in_frame_mobjects(grp)
            return grp

        # Helper function to dynamically rotate a layer
        def do_move(axis_idx, val, angle, axis_vec, rt=0.25):
            # Locate cubies by their current center, avoiding floating point drift via < 0.5 threshold
            cubes_in_layer = [c for c in cubies if abs(c.get_center()[axis_idx] - val) < 0.5]
            if cubes_in_layer:
                layer = VGroup(*cubes_in_layer)
                self.play(Rotate(layer, angle=angle, axis=axis_vec, about_point=ORIGIN), run_time=rt)

        # --- ANIMATION SEQUENCE ---

        # 0. Title & Hook
        title = Tex(r"$\mathbb{G}$roup $\mathbb{T}$heory: Order", font_size=40)
        title.set_color_by_gradient(BLUE, RED)
        title_grp = make_fixed_text(title, 3.3)
        
        hook = Text("Start: Solved State", font_size=24, color=GREEN)
        hook_grp = make_fixed_text(hook, 2.5)

        self.play(FadeIn(title_grp), FadeIn(hook_grp), FadeIn(cubies), run_time=1.5)
        self.wait(0.5)

        # 1. Introduce the Algorithm
        math_seq = Tex(r"Algorithm: $(R \, U \, R' \, U')$", font_size=32)
        math_seq_grp = make_fixed_text(math_seq, -2.5)
        self.play(FadeOut(hook_grp), FadeIn(math_seq_grp), run_time=0.5)

        # Initial UI Counter
        counter_text = Text("Cycles: 0/6", font_size=24)
        counter_grp = make_fixed_text(counter_text, 2.5)
        self.play(FadeIn(counter_grp), run_time=0.5)

        # 2. Execute the sequence 6 times
        for i in range(1, 7):
            do_move(0, 1, -PI/2, RIGHT) # R
            do_move(1, 1, -PI/2, UP)    # U
            do_move(0, 1, PI/2, RIGHT)  # R'
            do_move(1, 1, PI/2, UP)     # U'
            
            # Cleanly update the UI counter without leaving render artifacts
            self.remove(*counter_grp)
            new_counter = Text(f"Cycles: {i}/6", font_size=24)
            counter_grp = make_fixed_text(new_counter, 2.5)
            self.wait(0.1)

        # 3. Finale (The Return to Identity)
        self.play(FadeOut(math_seq_grp), run_time=0.5)
        
        finale_math = Tex(r"$(R \, U \, R' \, U')^6 = I$", font_size=36, color=YELLOW)
        finale_math_grp = make_fixed_text(finale_math, -2.0)
        
        solved_text = Text("End: Solved State", font_size=24, color=GREEN)
        solved_grp = make_fixed_text(solved_text, -3.0)

        self.play(FadeIn(finale_math_grp), FadeIn(solved_grp), run_time=1)

        self.wait(2.5)
        self.stop_ambient_camera_rotation()