from manim import *

class GroupTheoryOrder(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.08)

        def create_cubie(x, y, z):
            cubie = VGroup()
            size = 0.95
            
            base = Cube(
                side_length=size, 
                fill_color="#1A1A1A",
                fill_opacity=1, 
                stroke_width=1, 
                stroke_color=BLACK
            )
            base.set_shade_in_3d(True)
            cubie.add(base)
            
            s_size = size * 0.85
            d = size / 2 + 0.01
            
            def make_sticker(color, pos, rot_axis, angle):
                sticker = Square(side_length=s_size, fill_color=color, fill_opacity=1, stroke_width=0)
                sticker.set_shade_in_3d(True)
                if rot_axis is not None:
                    sticker.rotate(angle, axis=rot_axis)
                sticker.move_to(pos)
                return sticker

            if x == 1:   cubie.add(make_sticker(PURE_RED, RIGHT*d, UP, PI/2))  # Right
            if x == -1:  cubie.add(make_sticker(ORANGE, LEFT*d, UP, -PI/2))    # Left
            if y == 1:   cubie.add(make_sticker(WHITE, UP*d, RIGHT, -PI/2))    # Up
            if y == -1:  cubie.add(make_sticker(YELLOW, DOWN*d, RIGHT, PI/2))  # Down
            if z == 1:   cubie.add(make_sticker(GREEN, OUT*d, None, 0))        # Front
            if z == -1:  cubie.add(make_sticker(BLUE, IN*d, UP, PI))           # Back
                
            cubie.move_to(RIGHT * x + UP * y + OUT * z)
            return cubie

        cubies = VGroup()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    cubies.add(create_cubie(x, y, z))
                    
        def make_fixed_text(mobj, y_pos):
            bg = SurroundingRectangle(
                mobj,
                color="#78B9D2",      
                stroke_width=2.5,
                fill_color="#0D1117", 
                fill_opacity=0.95,
                corner_radius=0.15,
                buff=0.25             
            )
            grp = VGroup(bg, mobj).move_to(UP * y_pos)
            self.add_fixed_in_frame_mobjects(grp)
            return grp

        def execute_alg(alg_string, rt=0.15):
            clean_string = alg_string.replace('(', '').replace(')', '')
            moves = clean_string.split()
            
            for move in moves:
                if not move: continue
                
                base = move[0]
                if base in ['R', 'r', 'x']: axis, base_angle = RIGHT, -PI/2
                elif base == 'L':           axis, base_angle = RIGHT, PI/2
                elif base == 'U':           axis, base_angle = UP, -PI/2
                elif base == 'D':           axis, base_angle = UP, PI/2
                elif base == 'F':           axis, base_angle = OUT, -PI/2
                elif base == 'B':           axis, base_angle = OUT, PI/2
                else: continue
                
                if len(move) > 1:
                    if move[1] == "'":   angle = -base_angle
                    elif move[1] == "2": angle = base_angle * 2
                    else:                angle = base_angle
                else:
                    angle = base_angle
                    
                layer_cubes = []
                for c in cubies:
                    pos = c.get_center()
                    if base == 'R':   cond = pos[0] > 0.5
                    elif base == 'L': cond = pos[0] < -0.5
                    elif base == 'U': cond = pos[1] > 0.5
                    elif base == 'D': cond = pos[1] < -0.5
                    elif base == 'F': cond = pos[2] > 0.5
                    elif base == 'B': cond = pos[2] < -0.5
                    elif base == 'r': cond = pos[0] > -0.5
                    elif base == 'x': cond = True         
                    else: cond = False
                    
                    if cond: layer_cubes.append(c)
                    
                if layer_cubes:
                    layer = VGroup(*layer_cubes)
                    self.play(Rotate(layer, angle=angle, axis=axis, about_point=ORIGIN), run_time=rt)

        def highlight_progress(condition_func, do_flash=False):
            targets, non_targets = [], []
            for c in cubies:
                if condition_func(c.get_center()):
                    targets.append(c)
                else:
                    non_targets.append(c)
            
            if not non_targets: return
            
            dim_anims = [sub.animate.set_fill(opacity=0.15) for c in non_targets for sub in c] + \
                        [sub.animate.set_stroke(opacity=0.15) for c in non_targets for sub in c]
            self.play(*dim_anims, run_time=0.4)
            
            if do_flash and targets:
                target_group = VGroup(*targets)
                center_pt = target_group.get_center()
                self.play(target_group.animate.scale(1.08, about_point=center_pt), run_time=0.25)
                self.play(target_group.animate.scale(1/1.08, about_point=center_pt), run_time=0.25)
                self.wait(0.3)
            else:
                self.wait(0.3)
            
            restore_anims = [sub.animate.set_fill(opacity=1) for c in non_targets for sub in c] + \
                            [sub.animate.set_stroke(opacity=1) for c in non_targets for sub in c]
            self.play(*restore_anims, run_time=0.4)


        title = Tex(r"$\mathbb{W}$orld $\mathbb{R}$ecord $\mathbb{S}$olve", font_size=50)
        title.set_color_by_gradient(RED, BLUE)
        title.move_to(UP * 3.3)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), FadeIn(cubies), run_time=1.2)

        ui_y_pos = -3.1
        
        scramble_text = Tex(
            r"Scramble: L B R2 B' R2 U2 F D R2 \\ U R2 F2 D2 R U B L2", 
            font_size=24, color=PURE_RED
        )
        ui_grp = make_fixed_text(scramble_text, ui_y_pos)
        self.play(FadeIn(ui_grp), run_time=0.5)
        
        execute_alg("L B R2 B' R2 U2 F D R2 U R2 F2 D2 R U B L2", rt=0.08) 
        self.wait(0.3)

        steps = [
            (r"$\mathbb{I}$nspection", "x'", lambda pos: False, False), 
            (r"$\mathbb{X}$-Cross", "r' U F U' r U' r' U2 r' U r", lambda pos: pos[1] < 0.5 and (pos[0] < 0.5 or pos[2] < 0.5), True),
            (r"$\mathbf{4}$th Pair", "R U2 R2 U' R U R U2 R'", lambda pos: pos[1] < 0.5, True), # using mathbf to avoid number rendering issues in mathbb
            (r"$\mathbb{Z}\mathbb{B}\mathbb{L}\mathbb{L}$", "U' F' r U R' U' r' F R", lambda pos: pos[1] > 0.5, False)
        ]

        for step_name, alg, highlight_cond, do_flash in steps:
            self.play(FadeOut(ui_grp), run_time=0.2)
            step_text = Tex(f"{step_name}: {alg}", font_size=28)
            ui_grp = make_fixed_text(step_text, ui_y_pos)
            self.play(FadeIn(ui_grp), run_time=0.3)
            
            self.wait(0.3)
            execute_alg(alg, rt=0.4)
            
            if step_name != r"$\mathbb{I}$nspection":
                highlight_progress(highlight_cond, do_flash=do_flash)

        self.play(FadeOut(ui_grp), run_time=0.2)
        
        finale_text = Tex(r"$\mathbb{T}$otal $\mathbb{T}$ime: 2.76s", font_size=32, color=GREEN_C)
        ui_grp = make_fixed_text(finale_text, ui_y_pos)
        self.play(FadeIn(ui_grp), run_time=0.5)
        
        self.stop_ambient_camera_rotation()
        self.wait(2)