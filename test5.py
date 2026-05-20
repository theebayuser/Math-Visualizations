from manim import *
import numpy as np

class PeanoCurve(Scene):
    def construct(self):
        
        title_tex = Tex(r"The $\mathbb{P}$eano $\mathbb{C}$urve", font_size=40)
        title_tex.set_color_by_gradient(BLUE, RED)
        title_box = BackgroundRectangle(title_tex, color=BLACK, fill_opacity=0.75, buff=0.25)
        title = VGroup(title_box, title_tex).move_to(UP * 3.4) 

        
        def make_table(n_val, length_val, segments_val, use_math=False):
            col_w = [1.8, 2.6] 
            
            row_h = 0.55 if use_math else 0.45 
            rows = [
                ("n =", str(n_val)),
                ("Length", str(length_val)),
                ("Segments", str(segments_val)),
            ]
            cells = VGroup()
            for r, (label, value) in enumerate(rows):
                y = -r * row_h
                lbl = Text(label, font_size=22, color=GREY_A).move_to([-col_w[0]/2, y, 0])
                
                
                if use_math:
                    val = MathTex(value, font_size=28, color=WHITE).move_to([col_w[1]/2, y, 0])
                else:
                    val = Text(value, font_size=22, color=WHITE).move_to([col_w[1]/2, y, 0])
                    
                sep = Line(
                    [-col_w[0] - 0.1, y - row_h / 2, 0],
                    [col_w[1] + 0.1, y - row_h / 2, 0],
                    stroke_width=0.8, color=GREY_D
                )
                cells.add(lbl, val, sep)

            total_h = len(rows) * row_h
            
            
            border = RoundedRectangle(
                corner_radius=0.2,
                width=col_w[0] + col_w[1] + 0.4,
                height=total_h + 0.2,
                stroke_color=BLUE_D, stroke_width=1.2,
                fill_color=BLACK, fill_opacity=0.72
            ).move_to([(col_w[1] - col_w[0])/2, -(total_h / 2) + row_h / 2, 0])
            
            vdiv = Line([0, 0.1, 0], [0, -total_h + 0.1, 0], stroke_width=0.8, color=GREY_D)
            return VGroup(border, vdiv, cells)

        curve_size = 4.2 
        center_offset = UP * 0.4 

        
        def get_peano_points(order, size=curve_size):
            def generate_peano(n):
                if n == 0:
                    return np.array([[0, 0]])
                
                pts_prev = generate_peano(n - 1)
                size_prev = 3**(n - 1)
                
                pts = []
                for i in range(9):
                    grid_x = i // 3
                    grid_y = i % 3 if grid_x % 2 == 0 else 2 - (i % 3)
                    
                    block_pts = pts_prev.copy()
                    
                    if grid_x % 2 == 1:
                        block_pts[:, 1] = (size_prev - 1) - block_pts[:, 1]
                    if grid_y % 2 == 1:
                        block_pts[:, 0] = (size_prev - 1) - block_pts[:, 0]
                        
                    block_pts[:, 0] += grid_x * size_prev
                    block_pts[:, 1] += grid_y * size_prev
                    
                    pts.extend(block_pts)
                return np.array(pts)

            raw_pts = generate_peano(order).astype(float)
            raw_pts = raw_pts / (3**order - 1) * size

            pts_3d = np.zeros((len(raw_pts), 3))
            pts_3d[:, :2] = raw_pts
            
            center = (pts_3d.min(axis=0) + pts_3d.max(axis=0)) / 2
            return pts_3d - center + center_offset

        
        def create_chunked_curve(pts, stroke_width, color=TEAL):
            max_verts = 15000 
            
            if len(pts) <= max_verts:
                curve = VMobject().set_points_as_corners(pts)
                curve.set_stroke(width=stroke_width, color=color)
                return curve
                
            curve_group = VGroup()
            for i in range(0, len(pts) - 1, max_verts):
                chunk_pts = pts[i : min(i + max_verts + 1, len(pts))]
                chunk_curve = VMobject().set_points_as_corners(chunk_pts)
                chunk_curve.set_stroke(width=stroke_width, color=color)
                curve_group.add(chunk_curve)
                
            return curve_group

        
        curve_color = TEAL
        stroke_widths = [8, 6, 4, 2.5, 1.25, 0.5] 
        
        
        dynamic_speeds = [2.0, 1.7, 1.4, 1.1, 1.8]
        dynamic_waits = [0.8, 0.7, 0.6, 0.5, 1.0]

        def get_math_length(n):
            return (3**n + 1) / 2.0

        
        pts0 = np.array([[0, -curve_size/2, 0], [0, curve_size/2, 0]]) + center_offset
        curve = create_chunked_curve(pts0, stroke_widths[0], curve_color)

        tbl = make_table("0", f"{get_math_length(0):.1f}", "1")
        tbl.move_to(DOWN * 2.6) 

        self.add(title, tbl)
        
        
        self.play(Create(curve), run_time=1.5)
        self.wait(0.6)

        
        for i in range(1, 6):
            new_pts = get_peano_points(i)
            new_curve = create_chunked_curve(new_pts, stroke_widths[i], curve_color)

            new_tbl = make_table(str(i), f"{get_math_length(i):.1f}", f"{9**i:,}")
            new_tbl.move_to(DOWN * 2.6)

            current_speed = dynamic_speeds[i - 1]
            
            self.play(
                Transform(curve, new_curve),
                FadeOut(tbl),
                FadeIn(new_tbl),
                run_time=current_speed
            )
            tbl = new_tbl
            self.wait(dynamic_waits[i - 1])

        
        haus_text = Text("Hausdorff Dimension: 2", font_size=24, color=WHITE)
        haus_border = RoundedRectangle(
            corner_radius=0.15,
            width=haus_text.width + 0.6,
            height=haus_text.height + 0.3,
            stroke_color=YELLOW, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.75
        )
        haus_group = VGroup(haus_border, haus_text)
        
        haus_group.move_to(UP * 2.65) 

        self.play(FadeIn(haus_group, shift=DOWN * 0.2), run_time=1.2)
        self.wait(1.0)

        
        
        final_tbl = make_table("n", r"\frac{3^n + 1}{2}", "9^n", use_math=True)
        final_tbl.move_to(DOWN * 2.6)

        self.play(
            FadeOut(tbl),
            FadeIn(final_tbl),
            run_time=1.5
        )
        
        self.wait(4.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=2.0)