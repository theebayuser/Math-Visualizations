from manim import *

class GoldenRatioUnfold(ThreeDScene):
    def construct(self):
        
        title = Tex(r"$\mathbb{T}$he $\mathbb{G}$olden $\mathbb{R}$atio", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=1.0) 

        
        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34]
        scale_factor = 0.10 
        
        palette = [RED_E, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, MAROON, GOLD]

        
        squares = VGroup()
        s0 = Square(
            side_length=fibs[0], 
            color=WHITE, stroke_width=1.5, fill_opacity=0.6, fill_color=palette[0]
        )
        squares.add(s0)

        directions = [RIGHT, UP, LEFT, DOWN]
        alignments = [DOWN, RIGHT, UP, LEFT]

        for i in range(1, len(fibs)):
            direction = directions[(i-1) % 4]
            alignment = alignments[(i-1) % 4]
            sq = Square(
                side_length=fibs[i], 
                color=WHITE, stroke_width=1.5, fill_opacity=0.6, fill_color=palette[i]
            )
            sq.next_to(squares, direction, buff=0, aligned_edge=alignment)
            squares.add(sq)

        squares.move_to(ORIGIN).shift(DOWN * 1.0)
        squares.scale(scale_factor)

        
        arc_corners = [(UL, DR), (DL, UR), (DR, UL), (UR, DL)]
        original_arcs = VGroup()
        
        for i, sq in enumerate(squares):
            start_corner, end_corner = arc_corners[i % 4]
            arc = ArcBetweenPoints(sq.get_corner(start_corner), sq.get_corner(end_corner), angle=PI/2, color=WHITE, stroke_width=3)
            original_arcs.add(arc)

        arcs = original_arcs.copy()

        
        self.add(arcs)
        self.wait(0.5)
        self.play(FadeIn(squares, lag_ratio=0.1), run_time=2.0)
        self.wait(0.5)
        
        original_centers = [sq.get_center() for sq in squares] 

        
        unfolded_squares = VGroup(*[
            Square(side_length=sq.width, color=WHITE, stroke_width=1.5, fill_opacity=0.6, fill_color=sq.get_fill_color()) 
            for sq in squares
        ])
        
        for i in range(1, len(unfolded_squares)):
            shift_vec = unfolded_squares[i-1].get_corner(UR) - unfolded_squares[i].get_corner(DL)
            unfolded_squares[i].shift(shift_vec)

        unfolded_squares.move_to(ORIGIN).shift(DOWN * 1.0)
        
        
        flat_diagonal_lines = VGroup()
        total_width = sum([sq.width for sq in unfolded_squares])
        start_2d = unfolded_squares[0].get_corner(DL)
        end_2d = unfolded_squares[-1].get_corner(UR)
        vec_2d = end_2d - start_2d

        curr_t = 0
        for sq in unfolded_squares:
            t_next = curr_t + (sq.width / total_width)
            p1 = start_2d + curr_t * vec_2d
            p2 = start_2d + t_next * vec_2d
            flat_diagonal_lines.add(Line(p1, p2, color=WHITE, stroke_width=3))
            curr_t = t_next

        self.move_camera(zoom=0.35, run_time=1.5)

        self.play(
            ReplacementTransform(squares, unfolded_squares),
            ReplacementTransform(arcs, flat_diagonal_lines),
            run_time=0.8 
        )
        self.wait(0.5) 

        
        cubes = VGroup()
        cube_lines = VGroup()

        
        w_first = unfolded_squares[0].width
        w_last = unfolded_squares[-1].width
        start_3d = unfolded_squares[0].get_center() + np.array([-w_first/2, -w_first/2, -w_first/2])
        end_3d = unfolded_squares[-1].get_center() + np.array([w_last/2, w_last/2, w_last/2])
        vec_3d = end_3d - start_3d

        curr_t = 0
        for sq in unfolded_squares:
            
            c = Cube(side_length=sq.width, fill_opacity=0.7, fill_color=sq.get_fill_color(), stroke_color=WHITE, stroke_width=1.5)
            c.move_to(sq.get_center())
            c.save_state()
            c.stretch(0.001, dim=2)
            cubes.add(c)

            
            t_next = curr_t + (sq.width / total_width)
            p1 = start_3d + curr_t * vec_3d
            p2 = start_3d + t_next * vec_3d
            cl = Line(p1, p2, color=WHITE, stroke_width=3)
            cl.save_state()
            cl.stretch(0.001, dim=2)
            cube_lines.add(cl)
            curr_t = t_next

        
        self.remove(unfolded_squares, flat_diagonal_lines)
        self.add(cubes, cube_lines)

        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=0.35, run_time=1.5)
        
        self.play(
            *[c.animate.restore() for c in cubes],
            *[cl.animate.restore() for cl in cube_lines],
            run_time=2
        )
        self.wait(0.5)

        
        final_spiral = original_arcs.copy() 
        
        self.play(
            *[c.animate.move_to(center) for c, center in zip(cubes, original_centers)],
            ReplacementTransform(cube_lines, final_spiral),
            run_time=2.0
        )
        
        self.move_camera(zoom=1.0, run_time=1.5)
        self.wait(0.5)

        
        numbers = VGroup()
        for i, cube in enumerate(cubes):
            num = MathTex(str(fibs[i]), color=WHITE)
            num.scale_to_fit_width(min(num.width, cube.width * 0.4))
            
            z_offset = cube.depth / 2 + 0.02
            num.move_to(original_centers[i] + OUT * z_offset)
            numbers.add(num)

        self.play(Write(numbers), run_time=1.5)
        self.wait(0.5)

        
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0, run_time=1.5)

        self.play(
            *[c.animate.stretch(0.001, dim=2) for c in cubes],
            *[num.animate.move_to(original_centers[i] + OUT * 0.01) for i, num in enumerate(numbers)],
            run_time=1.5
        )

        flat_squares = VGroup(*[
            Square(
                side_length=c.width, 
                color=WHITE, stroke_width=1.5, fill_opacity=0.6, fill_color=c.get_fill_color()
            ).move_to(c.get_center()) 
            for c in cubes
        ])

        self.remove(cubes)
        self.add(flat_squares)
        
        self.wait(1)