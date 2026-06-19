from manim import *
import numpy as np
import random
import math

# Force a vertical aspect ratio for shorts/TikTok
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 10.8
config.frame_height = 19.2

random.seed(42)
np.random.seed(42)

# --- COLORS & STYLE ---
C_BG       = "#050505"
C_WALL     = "#4a9eff"
C_CURVE    = "#ff6b6b"

# RGB Tuples for smooth color interpolation
COLOR_SLOW_RGB  = (33, 150, 243)  # Blue
COLOR_FAST_RGB  = (255, 235, 59)  # Yellow
COLOR_START_RGB = (240, 240, 240) # Bright Gray/White initially

def lerp_rgb(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

# --- DIMENSIONS ---
LEFT_WALL  = -4.5
RIGHT_WALL = 4.5
DIVIDER_X  = -1.5

# Moved the Box Apparatus UP
BOT_WALL   = -0.5
TOP_WALL   = 5.5  

BIN_TOP    = 4.0  
GAP_BOT    = 5.0  # Opening squeezed between 5.0 and 5.5

NUM_BINS   = 15
BIN_W      = (RIGHT_WALL - DIVIDER_X) / NUM_BINS

BALL_RADIUS = 0.045
NUM_BALLS   = 400
COUNT_FS    = 24 

TITLE_Y    = 8.0
FORMULA_Y  = -5.0 

# --- TIMING ---
T_REST = 0.5
T_BOIL = 1.0


class BallParams:
    """Stores the precalculated trajectory parameters for a single bead"""
    def __init__(self):
        self.t_exit = 0.0
        self.t_shoot = 0.0
        self.t_drop = 0.0
        self.t_done = 0.0
        
        self.P_rest = np.zeros(3)
        self.P_shoot = np.zeros(3)
        self.P_control = np.zeros(3)
        self.P_bin_top = np.zeros(3)
        self.P_stack = np.zeros(3)
        
        self.cx = 0.0
        self.cy = 0.0
        self.rx = 0.0
        self.ry = 0.0
        self.wx = 0.0
        self.wy = 0.0
        self.px = 0.0
        self.py = 0.0
        
        self.target_rgb = (255, 255, 255)

def get_marble_pos(t, p):
    """Analytic pseudo-physics pathing"""
    if t < T_REST:
        # 0. Motionless at the bottom
        return p.P_rest
        
    elif t < p.t_exit:
        # 1. Agitated Chaos (Phase-Modulated Lissajous for erratic, snappy bouncing)
        angle_x = p.wx * t + p.px + 1.5 * np.sin(p.wx * 0.618 * t)
        angle_y = p.wy * t + p.py + 1.5 * np.sin(p.wy * 0.732 * t)
        
        target_x = p.cx + p.rx * np.sin(angle_x)
        target_y = p.cy + p.ry * np.sin(angle_y)
        
        if t < T_BOIL:
            # Tween from resting pile to bouncing chaos
            alpha = smoothstep(T_REST, T_BOIL, t)
            return np.array([
                p.P_rest[0] * (1 - alpha) + target_x * alpha,
                p.P_rest[1] * (1 - alpha) + target_y * alpha,
                0.0
            ])
        else:
            return np.array([target_x, target_y, 0.0])
        
    elif t < p.t_shoot:
        # 2. Funneling Naturally: Shrink the bouncing bounds toward the exit hole over time
        alpha = (t - p.t_exit) / (p.t_shoot - p.t_exit)
        ease_alpha = alpha ** 2 # Ease-in to funneling slowly
        
        cur_cx = p.cx * (1 - ease_alpha) + p.P_shoot[0] * ease_alpha
        cur_cy = p.cy * (1 - ease_alpha) + p.P_shoot[1] * ease_alpha
        cur_rx = p.rx * (1 - ease_alpha)
        cur_ry = p.ry * (1 - ease_alpha)
        
        angle_x = p.wx * t + p.px + 1.5 * np.sin(p.wx * 0.618 * t)
        angle_y = p.wy * t + p.py + 1.5 * np.sin(p.wy * 0.732 * t)
        
        x = cur_cx + cur_rx * np.sin(angle_x)
        y = cur_cy + cur_ry * np.sin(angle_y)
        return np.array([x, y, 0.0])
        
    elif t < p.t_drop:
        # 3. Parabolic Trajectory into bins
        alpha = (t - p.t_shoot) / (p.t_drop - p.t_shoot)
        P0, P1, P2 = p.P_shoot, p.P_control, p.P_bin_top
        
        x = (1-alpha)**2 * P0[0] + 2*(1-alpha)*alpha * P1[0] + alpha**2 * P2[0]
        y = (1-alpha)**2 * P0[1] + 2*(1-alpha)*alpha * P1[1] + alpha**2 * P2[1]
        return np.array([x, y, 0.0])
        
    elif t < p.t_done:
        # 4. Straight Drop into Bin
        alpha = (t - p.t_drop) / (p.t_done - p.t_drop)
        y = p.P_bin_top[1] + (p.P_stack[1] - p.P_bin_top[1]) * alpha
        return np.array([p.P_bin_top[0], y, 0.0])
        
    else:
        # 5. Stacked at Rest
        return p.P_stack

class BoltzmannDistribution(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        # ---------------------------
        # TITLE
        # ---------------------------
        bb_m  = MathTex(r"\mathbb{M}", font_size=96)
        t1    = Tex("axwell-",         font_size=86)
        bb_b  = MathTex(r"\mathbb{B}", font_size=96)
        t2    = Tex("oltzmann",        font_size=86)
        
        word1 = VGroup(bb_m, t1, bb_b, t2).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        subtitle = Tex("Speed Distribution Simulation", font_size=54, color=GRAY_A)
        
        title = VGroup(word1, subtitle).arrange(DOWN, buff=0.25)
        title.set_color_by_gradient("#ff6b6b", "#ffd93d", "#4a9eff")
        title.move_to(np.array([0.0, TITLE_Y, 0.0]))

        # ---------------------------
        # APPARATUS DRAWING
        # ---------------------------
        box_lines = VGroup(
            Line([LEFT_WALL, BOT_WALL, 0], [LEFT_WALL, TOP_WALL, 0]),
            Line([RIGHT_WALL, BOT_WALL, 0], [RIGHT_WALL, TOP_WALL, 0]),
            Line([LEFT_WALL, BOT_WALL, 0], [RIGHT_WALL, BOT_WALL, 0]),
            Line([LEFT_WALL, TOP_WALL, 0], [RIGHT_WALL, TOP_WALL, 0]),
            Line([DIVIDER_X, BOT_WALL, 0], [DIVIDER_X, GAP_BOT, 0]),
        )
        box_lines.set_stroke(color=C_WALL, width=4, opacity=0.8)
        
        bin_lines = VGroup(*[
            Line([DIVIDER_X + i*BIN_W, BOT_WALL, 0], [DIVIDER_X + i*BIN_W, BIN_TOP, 0])
            for i in range(1, NUM_BINS)
        ])
        bin_lines.set_stroke(color=C_WALL, width=2, opacity=0.4)

        # ---------------------------
        # STATISTICS & BELL CURVE
        # ---------------------------
        sigma = 3.0
        def mb_pdf(x):
            return x**2 * np.exp(-x**2 / (2 * sigma**2))
            
        peak_x = sigma * np.sqrt(2)
        max_p = mb_pdf(peak_x)
        
        bin_assignments = []
        while len(bin_assignments) < NUM_BALLS:
            x_val = random.uniform(0, NUM_BINS)
            y_val = random.uniform(0, max_p)
            if y_val < mb_pdf(x_val):
                b_idx = int(x_val)
                if 0 <= b_idx < NUM_BINS:
                    bin_assignments.append(b_idx)

        max_bar_h = BIN_TOP - BOT_WALL
        curve_pts = [np.array([DIVIDER_X, BOT_WALL, 0])]
        
        for k in range(NUM_BINS):
            prob = mb_pdf(k) / max_p
            bx = DIVIDER_X + (k + 0.5) * BIN_W
            by = float(BOT_WALL + prob * (max_bar_h * 0.95))
            curve_pts.append(np.array([bx, by, 0]))
            
        curve_pts.append(np.array([RIGHT_WALL, BOT_WALL, 0]))

        bell = VMobject()
        bell.set_points_smoothly(curve_pts)
        bell.set_stroke(color=C_CURVE, width=4)
        bell.set_fill(color=C_CURVE, opacity=0.1)

        # ---------------------------
        # FORMULA & MORE INFO
        # ---------------------------
        formula = MathTex(
            r"P(v) \propto v^{2} e^{-\frac{mv^{2}}{2kT}}",
            font_size=72, color=WHITE
        )
        formula.move_to(np.array([0, FORMULA_Y, 0]))
        
        box_formula = SurroundingRectangle(
            formula, corner_radius=0.2, color="#4a9eff", stroke_width=3,
            fill_color="#121B24", fill_opacity=1.0, buff=0.4
        )
        formula_group = VGroup(box_formula, formula)
        
        legend = VGroup(
            Tex("$v$ = Particle Speed", font_size=42, color=WHITE),
            Tex("$m$ = Particle Mass", font_size=42, color=WHITE),
            Tex("$T$ = Temperature", font_size=42, color=WHITE),
            Tex("$k$ = Boltzmann Constant", font_size=42, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend.next_to(formula_group, DOWN, buff=0.5)

        self.add(title, box_lines, bin_lines, bell, formula_group, legend)

        # ---------------------------
        # MID-ANIMATION SPEED SCALE
        # ---------------------------
        bar_segments = VGroup(*[
            Rectangle(width=BIN_W, height=0.15).set_stroke(width=0).set_fill(
                color=rgb_to_hex(lerp_rgb(COLOR_SLOW_RGB, COLOR_FAST_RGB, i / (NUM_BINS-1))), opacity=0.9
            ) for i in range(NUM_BINS)
        ]).arrange(RIGHT, buff=0)
        bar_segments.move_to([ (DIVIDER_X + RIGHT_WALL)/2, BOT_WALL - 1.4, 0 ])
        
        slow_label = Tex("Slow", font_size=32, color=rgb_to_hex(COLOR_SLOW_RGB)).next_to(bar_segments, DOWN, aligned_edge=LEFT)
        fast_label = Tex("Fast", font_size=32, color=rgb_to_hex(COLOR_FAST_RGB)).next_to(bar_segments, DOWN, aligned_edge=RIGHT)
        speed_label = Tex("Speed ($v$)", font_size=36, color=WHITE).next_to(bar_segments, UP, buff=0.15)
        
        speed_scale = VGroup(bar_segments, slow_label, fast_label, speed_label)

        # ---------------------------
        # BALL PATH PARAMS
        # ---------------------------
        all_params = []
        stack_counts = [0] * NUM_BINS
        
        min_x = LEFT_WALL + BALL_RADIUS + 0.1
        max_x = DIVIDER_X - BALL_RADIUS - 0.1
        min_y = BOT_WALL + BALL_RADIUS + 0.1
        max_y = TOP_WALL - BALL_RADIUS - 0.1
            
        for i in range(NUM_BALLS):
            p = BallParams()
            b_idx = bin_assignments[i]
            
            p.t_exit  = T_BOIL + 0.5 + i * (12.0 / NUM_BALLS) + random.uniform(-0.1, 0.1)
            # Extent duration so it funnels naturally over 1 second instead of zipping out
            p.t_shoot = p.t_exit + 1.0 
            p.t_drop  = p.t_shoot + 0.7 + (b_idx * 0.04) + random.uniform(-0.05, 0.05)
            
            p.P_rest = np.array([
                random.uniform(min_x, max_x),
                BOT_WALL + BALL_RADIUS + random.uniform(0.0, 0.6),
                0.0
            ])
            
            p.P_shoot = np.array([DIVIDER_X, random.uniform(GAP_BOT + 0.05, TOP_WALL - 0.05), 0])
            bin_cx    = DIVIDER_X + (b_idx + 0.5) * BIN_W
            p.P_bin_top = np.array([bin_cx, BIN_TOP, 0])
            
            stack_y   = BOT_WALL + BALL_RADIUS + stack_counts[b_idx] * (2 * BALL_RADIUS + 0.005)
            p.P_stack = np.array([bin_cx, stack_y, 0])
            stack_counts[b_idx] += 1
            
            p.t_done = p.t_drop + (BIN_TOP - stack_y) / 5.0
            
            p.P_control = np.array([
                (p.P_shoot[0] + p.P_bin_top[0]) / 2,
                min(p.P_shoot[1] + random.uniform(0.1, 0.3), TOP_WALL - 0.05), 
                0
            ])
            
            p.cy = (max_y + min_y) / 2
            p.ry = (max_y - min_y) / 2
            p.cx = (max_x + min_x) / 2
            p.rx = (max_x - min_x) / 2
            
            p.wx = random.uniform(8, 14) * random.choice([-1, 1])
            p.wy = random.uniform(8, 14) * random.choice([-1, 1])
            p.px = random.uniform(0, 2*np.pi)
            p.py = random.uniform(0, 2*np.pi)
            
            # Target color mapping based on speed (Bin index)
            b_alpha = b_idx / max(NUM_BINS - 1, 1)
            p.target_rgb = lerp_rgb(COLOR_SLOW_RGB, COLOR_FAST_RGB, b_alpha)
            
            all_params.append(p)

        # ---------------------------
        # VISUALS & ANIMATION
        # ---------------------------
        time_tracker = ValueTracker(0.0)
        self.add(time_tracker)
        
        total_time = max(p.t_done for p in all_params) + 0.5
        T_MID = total_time / 2.0

        count_labels = VGroup(*[
            Integer(0, font_size=COUNT_FS, color=WHITE).move_to([DIVIDER_X + (b+0.5)*BIN_W, BOT_WALL - 0.35, 0])
            for b in range(NUM_BINS)
        ])
        self.add(count_labels)

        def make_marble(color_hex):
            base = Dot(radius=BALL_RADIUS, color=color_hex).set_opacity(0.9)
            hl_pos = np.array([-BALL_RADIUS*0.3, BALL_RADIUS*0.3, 0])
            hl = Dot(point=hl_pos, radius=BALL_RADIUS * 0.3, color=WHITE).set_opacity(0.4)
            return VGroup(base, hl)

        all_marbles = VGroup()
        
        def get_updater(marble, p):
            def update(m, dt):
                ct = time_tracker.get_value()
                m.move_to(get_marble_pos(ct, p))
                
                # Dynamic Color Transition mid-simulation
                if ct < T_MID:
                    color = rgb_to_hex(COLOR_START_RGB)
                elif ct < T_MID + 1.0:
                    alpha = smoothstep(T_MID, T_MID + 1.0, ct)
                    color = rgb_to_hex(lerp_rgb(COLOR_START_RGB, p.target_rgb, alpha))
                else:
                    color = rgb_to_hex(p.target_rgb)
                    
                m[0].set_color(color)
            return update

        for i in range(NUM_BALLS):
            marble = make_marble(rgb_to_hex(COLOR_START_RGB))
            marble.move_to(get_marble_pos(0, all_params[i]))
            marble.add_updater(get_updater(marble, all_params[i]))
            all_marbles.add(marble)
            
        self.add(all_marbles)

        # Label Updater
        def update_labels(m, dt):
            ct = time_tracker.get_value()
            counts = [0] * NUM_BINS
            for i, p in enumerate(all_params):
                if ct >= p.t_done:
                    counts[bin_assignments[i]] += 1
            for b in range(NUM_BINS):
                count_labels[b].set_value(counts[b])
        count_labels.add_updater(update_labels)

        # --- PLAY SEQUENCE ---
        
        # 1. Play first half of the simulation
        self.play(time_tracker.animate.set_value(T_MID), run_time=T_MID, rate_func=linear)
        
        # 2. Fade in Speed Scale while time slowly progresses
        self.play(
            FadeIn(speed_scale, shift=UP*0.3),
            time_tracker.animate.set_value(T_MID + 1.0),
            run_time=1.0,
            rate_func=linear
        )
        
        # 3. Play remaining simulation
        remaining_time = total_time - (T_MID + 1.0)
        self.play(time_tracker.animate.set_value(total_time), run_time=remaining_time, rate_func=linear)

        for m in all_marbles: m.clear_updaters()
        count_labels.clear_updaters()
        self.wait(3.0)