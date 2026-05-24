from manim import *
import numpy as np

class UlamSpiralPattern(ThreeDScene):
    def construct(self):
        # 1. Setup the Title
        title = Tex(
            r"$\mathbb{D}$o $\mathbb{P}$rimes have a $\mathbb{P}$attern?",
            font_size=40
        )
        title.set_color_by_gradient(BLUE, RED)

        title_box = BackgroundRectangle(
            title, color=BLACK, fill_opacity=0.75, buff=0.25
        )
        title_group = VGroup(title_box, title).to_edge(UP, buff=0.25)
        self.add_fixed_in_frame_mobjects(title_group)

        # 2. Configuration Parameters
        SCALE = 1.0 / 1.5
        TOTAL_NODES = 3025          # 55^2 perfect square
        NODE_RADIUS = 0.4 * SCALE
        STEP_SIZE = 1.0 * SCALE
        FONT_SIZE = int(22 * SCALE)

        PRIME_COLORS = [BLUE, TEAL, GREEN, YELLOW, RED, PURPLE]

        # 3. Helper Functions
        def is_prime(n):
            if n < 2: return False
            if n in (2, 3): return True
            if n % 2 == 0 or n % 3 == 0: return False
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return False
                i += 6
            return True

        def generate_ulam_coordinates(max_n, step):
            coords = {}
            cx, cy = 0.0, 0.0
            cdx, cdy = step, 0.0
            step_limit = 1
            steps_taken = 0
            turns = 0
            for idx in range(1, max_n + 1):
                coords[idx] = np.array([cx, cy, 0.0])
                cx += cdx
                cy += cdy
                steps_taken += 1
                if steps_taken == step_limit:
                    steps_taken = 0
                    cdx, cdy = -cdy, cdx
                    turns += 1
                    if turns % 2 == 0:
                        step_limit += 1
            return coords

        # 4. Assign each node to its ring
        def ring_of(n):
            if n == 1:
                return 0
            k = int(np.ceil((np.sqrt(n) - 1) / 2))
            return k

        # 5. Generate Coordinates
        node_coords = generate_ulam_coordinates(TOTAL_NODES, STEP_SIZE)

        # 6. Build Visuals
        nodes = VGroup()
        prime_counter = 0
        for i in range(1, TOTAL_NODES + 1):
            pos = node_coords[i]
            if is_prime(i):
                color = PRIME_COLORS[prime_counter % len(PRIME_COLORS)]
                prime_counter += 1
                circle = Circle(radius=NODE_RADIUS, fill_color=color,
                                fill_opacity=1, stroke_width=0)
                text = Text(str(i), font_size=FONT_SIZE, color=BLACK)
            else:
                circle = Circle(radius=NODE_RADIUS, fill_color=BLACK,
                                fill_opacity=1, stroke_color=WHITE,
                                stroke_width=2 * SCALE)
                text = Text(str(i), font_size=FONT_SIZE, color=WHITE)
            circle.move_to(pos)
            text.move_to(pos)
            nodes.add(VGroup(circle, text))

        # 7. every ring

        max_ring = ring_of(TOTAL_NODES)          
        TIME_PER_RING = 1.2                       
        DRAW_TIME = (max_ring + 1) * TIME_PER_RING

        node_start_times = {}   
        ring_node_lists = {}
        for i in range(2, TOTAL_NODES + 1):
            k = ring_of(i)
            ring_node_lists.setdefault(k, []).append(i)

        for k, members in ring_node_lists.items():
            ring_start = k * TIME_PER_RING
            count = len(members)
            for j, node_idx in enumerate(members):

                node_start_times[node_idx] = ring_start + j * TIME_PER_RING / count

        # 8. Animation Sequence
        self.play(FadeIn(title_group, shift=DOWN), run_time=1.5)
        self.play(FadeIn(nodes[0]), run_time=0.5)

        spiral_width = (np.sqrt(TOTAL_NODES) + 2) * STEP_SIZE
        target_camera_width = spiral_width * 3
        target_zoom = config.frame_width / target_camera_width


        fade_ins = []
        for i, node in enumerate(nodes[1:], start=2):   # nodes[0] already shown
            t0 = node_start_times[i]
            shift_dir = (node_coords[min(i+1, TOTAL_NODES)] - node_coords[i]) * 0.5
            fade_ins.append(
                Succession(
                    Wait(t0),
                    FadeIn(node, shift=shift_dir, run_time=0.25),
                )
            )

        draw_all = AnimationGroup(*fade_ins)


        def zoom_rate(t):
            return 1.0 - (1.0 - t) ** 2.5

        self.move_camera(
            zoom=target_zoom,
            added_anims=[draw_all],
            run_time=DRAW_TIME,
            rate_func=zoom_rate
        )

        self.wait(3)