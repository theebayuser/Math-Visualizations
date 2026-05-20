"""
Galton Board — Continuous stream, larger marbles, live counters, styled legend.
Run:
    manim -pql galton_board.py GaltonBoard
    manim -pqh galton_board.py GaltonBoard
"""

from manim import *
import random
import numpy as np
from math import comb

random.seed(42)
np.random.seed(42)


C_BG       = "#000000"
C_PEG      = "#4a9eff"
C_CURVE    = "#ff6b6b"
BALL_HEX_A = (255, 107, 107)
BALL_HEX_B = (255, 217,  61)

def lerp_hex(a, b, t):
    return "#{:02x}{:02x}{:02x}".format(
        *(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    )


USABLE_W   = 14.222 / 3
LEFT_EDGE  = -USABLE_W / 2
RIGHT_EDGE =  USABLE_W / 2

PEG_ROWS    = 10
PEG_SPACING = 0.245
PEG_RADIUS  = 0.028


BOARD_TOP   = 3.10
BOARD_BOT   = BOARD_TOP - (PEG_ROWS - 1) * PEG_SPACING   

NUM_BINS    = PEG_ROWS + 1    
BIN_W       = USABLE_W / NUM_BINS
BIN_BOTTOM  = -2.50
BIN_CEIL    = BOARD_BOT - 0.28    


BALL_RADIUS = 0.016
BALL_GAP    = 0.002
NUM_BALLS   = 350
COUNT_FS    = 16 

TITLE_Y = 3.75


def peg_pos(row, col):
    x = col * PEG_SPACING - row * PEG_SPACING / 2.0
    y = BOARD_TOP - row * PEG_SPACING
    return np.array([x, y, 0.0], dtype=float)

def bin_cx(idx):
    return float(LEFT_EDGE + BIN_W * (idx + 0.5))

def ball_land_y(stack):
    y = BIN_BOTTOM + BALL_RADIUS + stack * (BALL_RADIUS * 2.0 + BALL_GAP)
    return float(min(y, BIN_CEIL - BALL_RADIUS))

def make_path_pts(bin_idx, stack):
    turns = [1]*bin_idx + [-1]*(PEG_ROWS - bin_idx)
    random.shuffle(turns)
    
    pts = [np.array([0.0, BOARD_TOP + 0.35, 0.0])]
    x = 0.0
    for row, t in enumerate(turns):
        y = BOARD_TOP - row * PEG_SPACING + PEG_SPACING * 0.24
        pts.append(np.array([float(x), float(y), 0.0]))
        x += t * PEG_SPACING / 2.0
    bx = bin_cx(bin_idx)
    pts.append(np.array([bx, float(BOARD_BOT - 0.14), 0.0]))
    pts.append(np.array([bx, ball_land_y(stack), 0.0]))
    return pts

def make_vmob(pts):
    p = VMobject()
    p.set_points_smoothly(pts)
    return p

def make_marble(pos, color_hex):
    base = Dot(point=pos, radius=BALL_RADIUS, color=color_hex)
    hl_pos = pos + np.array([-BALL_RADIUS*0.28, BALL_RADIUS*0.30, 0.0])
    hl = Dot(point=hl_pos, radius=BALL_RADIUS * 0.30, color=WHITE)
    
    
    base.set_fill(opacity=0).set_stroke(opacity=0)
    hl.set_fill(opacity=0).set_stroke(opacity=0)
    return VGroup(base, hl)


class GaltonBoard(Scene):

    def construct(self):
        self.camera.background_color = C_BG

        
        bb_b  = MathTex(r"\mathbb{B}", font_size=56)
        t1    = Tex("inomial",         font_size=52)
        bb_d  = MathTex(r"\mathbb{D}", font_size=56)
        t2    = Tex("istribution",     font_size=52)
        
        
        word1 = VGroup(bb_b, t1).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        word2 = VGroup(bb_d, t2).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        
        title = VGroup(word1, word2).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        title.set_color_by_gradient("#C9E498", "#78C0E0", "#B28DFF")
        title.move_to(np.array([0.0, TITLE_Y, 0.0]))
        self.play(FadeIn(title, shift=DOWN*0.08), run_time=0.45)

        
        pegs = VGroup(*[
            Dot(point=peg_pos(r, c), radius=PEG_RADIUS, color=C_PEG)
            for r in range(PEG_ROWS) for c in range(r + 1)
        ])
        pegs.set_opacity(0.78)
        self.play(FadeIn(pegs, lag_ratio=0.008, run_time=0.35))

        
        walls = VGroup(*[
            Line(
                start=np.array([LEFT_EDGE + i*BIN_W, BIN_BOTTOM,     0.0]),
                end  =np.array([LEFT_EDGE + i*BIN_W, BOARD_BOT-0.16, 0.0]),
                stroke_width=0.7, stroke_opacity=0.30, color=C_PEG,
            )
            for i in range(NUM_BINS + 1)
        ])
        self.play(FadeIn(walls, run_time=0.20))

        
        bin_counts = [0] * NUM_BINS
        count_labels = VGroup(*[
            Integer(0, font_size=COUNT_FS, color=WHITE)
            .move_to(np.array([bin_cx(b), BIN_BOTTOM - 0.25, 0.0]))
            for b in range(NUM_BINS)
        ])
        self.add(count_labels)

        
        bin_indices = np.random.binomial(PEG_ROWS, 0.5, NUM_BALLS).tolist()
        
        drop_times = []
        current_time = 0.0
        for j in range(NUM_BALLS):
            drop_times.append(current_time)
            
            prog = j / NUM_BALLS
            dt_step = 0.20 * (1 - prog)**3 + 0.008
            current_time += dt_step
            
        
        time_tracker = ValueTracker(0.0)
        self.add(time_tracker)
        
        all_marbles = VGroup()
        landed_status = [False] * NUM_BALLS
        FALL_DURATION = 3.6  

        
        def get_update_func(marble_mob, start_t, path_vmob):
            def update_marble(m, dt):
                ct = time_tracker.get_value()
                if ct < start_t:
                    return
                
                
                if not hasattr(m, "is_revealed"):
                    m[0].set_fill(opacity=0.95).set_stroke(opacity=0.95)
                    m[1].set_fill(opacity=0.42).set_stroke(opacity=0.42)
                    m.is_revealed = True
                
                alpha = (ct - start_t) / FALL_DURATION
                alpha = min(alpha, 1.0)
                    
                m.move_to(path_vmob.point_from_proportion(alpha))
            return update_marble

        
        temp_bin_counts = [0] * NUM_BINS
        for j in range(NUM_BALLS):
            bidx = int(bin_indices[j])
            pts  = make_path_pts(bidx, temp_bin_counts[bidx])
            temp_bin_counts[bidx] += 1
            
            t_color = j / max(NUM_BALLS - 1, 1)
            color   = lerp_hex(BALL_HEX_A, BALL_HEX_B, t_color)
            marble  = make_marble(pts[0].copy(), color)
            
            
            marble.add_updater(get_update_func(marble, drop_times[j], make_vmob(pts)))
            all_marbles.add(marble)
            self.add(marble)

        
        def update_labels(m, dt):
            ct = time_tracker.get_value()
            changed = False
            for j in range(NUM_BALLS):
                if not landed_status[j] and ct >= (drop_times[j] + FALL_DURATION):
                    landed_status[j] = True
                    bidx = int(bin_indices[j])
                    bin_counts[bidx] += 1
                    changed = True
                    
            if changed:
                for b in range(NUM_BINS):
                    count_labels[b].set_value(bin_counts[b])

        count_labels.add_updater(update_labels)

        
        total_anim_time = drop_times[-1] + FALL_DURATION + 0.5
        self.play(time_tracker.animate.set_value(total_anim_time), run_time=total_anim_time, rate_func=linear)
        
        
        for m in all_marbles:
            m.clear_updaters()
        count_labels.clear_updaters()

        self.wait(0.50)

        
        max_prob  = max(comb(PEG_ROWS, k) / 2**PEG_ROWS for k in range(NUM_BINS))
        max_bar_h = BIN_CEIL - BIN_BOTTOM
        curve_pts = [np.array([LEFT_EDGE, BIN_BOTTOM, 0.0])]
        for k in range(NUM_BINS):
            prob = comb(PEG_ROWS, k) / 2**PEG_ROWS
            by   = float(BIN_BOTTOM + (prob / max_prob) * max_bar_h)
            curve_pts.append(np.array([bin_cx(k), by, 0.0]))
        curve_pts.append(np.array([RIGHT_EDGE, BIN_BOTTOM, 0.0]))

        bell = VMobject()
        bell.set_points_smoothly(curve_pts)
        bell.set_stroke(color=C_CURVE, width=3.5)
        bell.set_fill(opacity=0)
        self.play(Create(bell), run_time=0.80)

        self.wait(0.30)

        
        self.play(FadeOut(pegs), run_time=0.60)
        
        graph_group  = VGroup(walls, count_labels, all_marbles, bell)
        
        
        self.play(graph_group.animate.shift(UP * 2.3), run_time=1.2)
        self.wait(0.2)

        
        formula = MathTex(
            r"P(X{=}k)=\binom{n}{k}p^{k}(1-p)^{n-k}",
            font_size=36, color=WHITE,
        )
        formula.move_to(DOWN * 1.5)
        
        box_formula = SurroundingRectangle(
            formula, corner_radius=0.15, color="#5DA9E9", stroke_width=2.5,
            fill_color="#121B24", fill_opacity=1.0, buff=0.25
        )
        formula_group = VGroup(box_formula, formula)

        
        legend = VGroup(
            MathTex(r"n", font_size=24, color=YELLOW),
            Text("= trials   ",        font_size=20, color=GRAY_A),
            MathTex(r"k", font_size=24, color=YELLOW),
            Text("= successes   ",     font_size=20, color=GRAY_A),
            MathTex(r"p", font_size=24, color=YELLOW),
            Text("= prob per trial",   font_size=20, color=GRAY_A),
        ).arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
        legend.move_to(DOWN * 2.8)
        
        box_legend = SurroundingRectangle(
            legend, corner_radius=0.15, color="#5DA9E9", stroke_width=2.5,
            fill_color="#121B24", fill_opacity=1.0, buff=0.25
        )
        legend_group = VGroup(box_legend, legend)

        
        self.play(Create(box_formula), Write(formula), run_time=1.2)
        self.wait(0.15)
        self.play(FadeIn(legend_group, shift=UP*0.1), run_time=0.80)

        self.wait(2.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.80)