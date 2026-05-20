from manim import *
import numpy as np

class EulerLineAnimation(Scene):
    def construct(self):
        
        self.camera.background_color = "#0a0a0a"
        
        
        title = Text("The Euler Line", font_size=36, gradient=(BLUE, PURPLE))
        title.to_edge(UP, buff=1.2)
        
        
        A = np.array([-1.3, -0.4, 0])
        B = np.array([1.5, -0.6, 0])
        C = np.array([0.1, 1.0, 0])
        
        triangle = Polygon(A, B, C, color=WHITE, stroke_width=3)
        
        
        label_A = Text("A", font_size=20, color=WHITE).next_to(A, DOWN+LEFT, buff=0.15)
        label_B = Text("B", font_size=20, color=WHITE).next_to(B, DOWN+RIGHT, buff=0.15)
        label_C = Text("C", font_size=20, color=WHITE).next_to(C, UP, buff=0.15)
        
        
        circumcenter = self.get_circumcenter(A, B, C)
        centroid = (A + B + C) / 3
        orthocenter = self.get_orthocenter(A, B, C)
        
        
        circumcenter_dot = Dot(circumcenter, color=BLUE, radius=0.06)
        centroid_dot = Dot(centroid, color=GREEN, radius=0.06)
        orthocenter_dot = Dot(orthocenter, color=RED, radius=0.06)
        
        
        circumcenter_label_full = Text("Circumcenter", font_size=14, color=BLUE)
        centroid_label_full = Text("Centroid", font_size=14, color=GREEN)
        orthocenter_label_full = Text("Orthocenter", font_size=14, color=RED)
        
        circumcenter_label = Text("O", font_size=16, color=BLUE)
        centroid_label = Text("N", font_size=16, color=GREEN)
        orthocenter_label = Text("P", font_size=16, color=RED)
        
        
        circumcenter_label_full.next_to(circumcenter_dot, UP+LEFT, buff=0.2)
        centroid_label_full.next_to(centroid_dot, DOWN+LEFT, buff=0.2)
        orthocenter_label_full.next_to(orthocenter_dot, UP+RIGHT, buff=0.2)
        
        circumcenter_label.next_to(circumcenter_dot, UP+LEFT, buff=0.2)
        centroid_label.next_to(centroid_dot, DOWN+LEFT, buff=0.2)
        orthocenter_label.next_to(orthocenter_dot, UP+RIGHT, buff=0.2)
        
        
        circumradius = min(np.linalg.norm(A - circumcenter), 2.5)
        circumcircle = Circle(radius=circumradius, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        circumcircle.move_to(circumcenter)
        
        
        perp_bisector_AB = self.get_perpendicular_bisector_extended(A, B, C)
        perp_bisector_BC = self.get_perpendicular_bisector_extended(B, C, A)
        perp_bisector_AC = self.get_perpendicular_bisector_extended(A, C, B)
        
        
        mid_BC = (B + C) / 2
        mid_AC = (A + C) / 2
        mid_AB = (A + B) / 2
        
        median_A = Line(A, mid_BC, color=GREEN, stroke_width=2, stroke_opacity=0.6)
        median_B = Line(B, mid_AC, color=GREEN, stroke_width=2, stroke_opacity=0.6)
        median_C = Line(C, mid_AB, color=GREEN, stroke_width=2, stroke_opacity=0.6)
        
        
        median_marks_BC = self.get_median_tick_marks(B, mid_BC, C)
        median_marks_AC = self.get_median_tick_marks(A, mid_AC, C)
        median_marks_AB = self.get_median_tick_marks(A, mid_AB, B)
        
        
        altitude_A = self.get_altitude(A, B, C)
        altitude_B = self.get_altitude(B, A, C)
        altitude_C = self.get_altitude(C, A, B)
        
        
        euler_direction = orthocenter - circumcenter
        euler_length = np.linalg.norm(euler_direction)
        if euler_length > 0:
            euler_direction = euler_direction / euler_length
        
        euler_line = Line(
            circumcenter - 1.2 * euler_direction,
            orthocenter + 1.2 * euler_direction,
            color=YELLOW,
            stroke_width=4
        )
        
        
        self.play(Write(title))
        self.wait(0.3)
        
        
        self.play(Create(triangle))
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(0.3)
        
        
        self.play(Create(perp_bisector_AB), Create(perp_bisector_BC), Create(perp_bisector_AC))
        self.wait(0.3)
        
        
        
        right_angle_AB = self.get_right_angle_marker_inside_triangle((A + B) / 2, A, B, C)
        right_angle_BC = self.get_right_angle_marker_inside_triangle((B + C) / 2, B, C, A)
        right_angle_AC = self.get_right_angle_marker_inside_triangle((A + C) / 2, A, C, B)
        
        equal_marks_AB = self.get_equal_length_marks(A, (A + B) / 2, (A + B) / 2, B)
        equal_marks_BC = self.get_equal_length_marks(B, (B + C) / 2, (B + C) / 2, C)
        equal_marks_AC = self.get_equal_length_marks(A, (A + C) / 2, (A + C) / 2, C)
        
        self.play(Create(right_angle_AB), Create(right_angle_BC), Create(right_angle_AC))
        self.play(Create(equal_marks_AB), Create(equal_marks_BC), Create(equal_marks_AC))
        self.play(FadeIn(circumcenter_dot))
        self.play(Write(circumcenter_label_full))
        self.wait(0.3)
        
        
        self.play(Create(circumcircle))
        self.wait(0.3)
        
        
        
        self.play(FadeOut(right_angle_AB), FadeOut(right_angle_BC), FadeOut(right_angle_AC),
                  FadeOut(equal_marks_AB), FadeOut(equal_marks_BC), FadeOut(equal_marks_AC))
        
        self.play(Create(median_A), Create(median_B), Create(median_C))
        self.play(Create(median_marks_BC), Create(median_marks_AC), Create(median_marks_AB))
        self.play(FadeIn(centroid_dot))
        self.play(Write(centroid_label_full))
        self.wait(0.3)
        
        
        self.play(FadeOut(median_marks_BC), FadeOut(median_marks_AC), FadeOut(median_marks_AB))
        
        
        self.play(Create(altitude_A), Create(altitude_B), Create(altitude_C))
        
        
        altitude_foot_A = self.get_foot_of_perpendicular(A, B, C)
        altitude_foot_B = self.get_foot_of_perpendicular(B, A, C)
        altitude_foot_C = self.get_foot_of_perpendicular(C, A, B)
        
        right_angle_alt_A = self.get_right_angle_marker_altitude_inside(altitude_foot_A, A, B, C)
        right_angle_alt_B = self.get_right_angle_marker_altitude_inside(altitude_foot_B, B, A, C)
        right_angle_alt_C = self.get_right_angle_marker_altitude_inside(altitude_foot_C, C, A, B)
        
        self.play(Create(right_angle_alt_A), Create(right_angle_alt_B), Create(right_angle_alt_C))
        self.play(FadeIn(orthocenter_dot))
        self.play(Write(orthocenter_label_full))
        self.wait(0.3)
        
        
        
        self.play(FadeOut(right_angle_alt_A), FadeOut(right_angle_alt_B), FadeOut(right_angle_alt_C))
        
        
        self.play(
            Transform(circumcenter_label_full, circumcenter_label),
            Transform(centroid_label_full, centroid_label),
            Transform(orthocenter_label_full, orthocenter_label)
        )
        
        self.play(Create(euler_line))
        self.wait(0.3)
        
        
        self.play(
            Flash(circumcenter_dot, color=BLUE, flash_radius=0.2),
            Flash(centroid_dot, color=GREEN, flash_radius=0.2),
            Flash(orthocenter_dot, color=RED, flash_radius=0.2)
        )
        self.wait(0.3)
        
        
        triangle_configs = [
            (np.array([-1.0, -0.5, 0]), np.array([1.3, -0.3, 0]), np.array([-0.2, 1.2, 0])),
            (np.array([-1.4, -0.2, 0]), np.array([1.1, -0.7, 0]), np.array([0.6, 0.9, 0])),
            (np.array([-0.8, -0.8, 0]), np.array([1.0, -0.1, 0]), np.array([0.3, 1.4, 0])),
            (np.array([-1.6, 0.0, 0]), np.array([0.8, -0.9, 0]), np.array([0.0, 0.8, 0])),
            (np.array([-1.1, -0.6, 0]), np.array([1.2, -0.2, 0]), np.array([-0.1, 1.1, 0]))
        ]
        
        for new_A, new_B, new_C in triangle_configs:
            
            new_circumcenter = self.get_circumcenter(new_A, new_B, new_C)
            new_centroid = (new_A + new_B + new_C) / 3
            new_orthocenter = self.get_orthocenter(new_A, new_B, new_C)
            
            
            new_triangle = Polygon(new_A, new_B, new_C, color=WHITE, stroke_width=3)
            new_circumradius = min(np.linalg.norm(new_A - new_circumcenter), 2.5)
            new_circumcircle = Circle(radius=new_circumradius, color=BLUE, stroke_width=2, stroke_opacity=0.5)
            new_circumcircle.move_to(new_circumcenter)
            
            new_perp_bisector_AB = self.get_perpendicular_bisector_extended(new_A, new_B, new_C)
            new_perp_bisector_BC = self.get_perpendicular_bisector_extended(new_B, new_C, new_A)
            new_perp_bisector_AC = self.get_perpendicular_bisector_extended(new_A, new_C, new_B)
            
            new_mid_BC = (new_B + new_C) / 2
            new_mid_AC = (new_A + new_C) / 2
            new_mid_AB = (new_A + new_B) / 2
            
            new_median_A = Line(new_A, new_mid_BC, color=GREEN, stroke_width=2, stroke_opacity=0.6)
            new_median_B = Line(new_B, new_mid_AC, color=GREEN, stroke_width=2, stroke_opacity=0.6)
            new_median_C = Line(new_C, new_mid_AB, color=GREEN, stroke_width=2, stroke_opacity=0.6)
            
            new_altitude_A = self.get_altitude(new_A, new_B, new_C)
            new_altitude_B = self.get_altitude(new_B, new_A, new_C)
            new_altitude_C = self.get_altitude(new_C, new_A, new_B)
            
            new_euler_direction = new_orthocenter - new_circumcenter
            new_euler_length = np.linalg.norm(new_euler_direction)
            if new_euler_length > 0:
                new_euler_direction = new_euler_direction / new_euler_length
            
            new_euler_line = Line(
                new_circumcenter - 1.2 * new_euler_direction,
                new_orthocenter + 1.2 * new_euler_direction,
                color=YELLOW,
                stroke_width=4
            )
            
            
            new_label_A = Text("A", font_size=20, color=WHITE).next_to(new_A, DOWN+LEFT, buff=0.15)
            new_label_B = Text("B", font_size=20, color=WHITE).next_to(new_B, DOWN+RIGHT, buff=0.15)
            new_label_C = Text("C", font_size=20, color=WHITE).next_to(new_C, UP, buff=0.15)
            
            new_circumcenter_label = Text("O", font_size=16, color=BLUE)
            new_centroid_label = Text("N", font_size=16, color=GREEN)
            new_orthocenter_label = Text("P", font_size=16, color=RED)
            
            new_circumcenter_label.next_to(new_circumcenter, UP+LEFT, buff=0.2)
            new_centroid_label.next_to(new_centroid, DOWN+LEFT, buff=0.2)
            new_orthocenter_label.next_to(new_orthocenter, UP+RIGHT, buff=0.2)
            
            
            self.play(
                Transform(triangle, new_triangle),
                Transform(circumcircle, new_circumcircle),
                Transform(perp_bisector_AB, new_perp_bisector_AB),
                Transform(perp_bisector_BC, new_perp_bisector_BC),
                Transform(perp_bisector_AC, new_perp_bisector_AC),
                Transform(median_A, new_median_A),
                Transform(median_B, new_median_B),
                Transform(median_C, new_median_C),
                Transform(altitude_A, new_altitude_A),
                Transform(altitude_B, new_altitude_B),
                Transform(altitude_C, new_altitude_C),
                Transform(euler_line, new_euler_line),
                circumcenter_dot.animate.move_to(new_circumcenter),
                centroid_dot.animate.move_to(new_centroid),
                orthocenter_dot.animate.move_to(new_orthocenter),
                Transform(label_A, new_label_A),
                Transform(label_B, new_label_B),
                Transform(label_C, new_label_C),
                Transform(circumcenter_label_full, new_circumcenter_label),
                Transform(centroid_label_full, new_centroid_label),
                Transform(orthocenter_label_full, new_orthocenter_label),
                run_time=0.8
            )
            self.wait(0.15)
        
        self.wait(0.8)
    
    def get_circumcenter(self, A, B, C):
        """Calculate circumcenter of triangle ABC"""
        
        A2D = A[:2]
        B2D = B[:2]
        C2D = C[:2]
        
        
        mid_AB = (A2D + B2D) / 2
        mid_BC = (B2D + C2D) / 2
        
        
        dir_AB = B2D - A2D
        dir_BC = C2D - B2D
        
        
        perp_AB = np.array([-dir_AB[1], dir_AB[0]])
        perp_BC = np.array([-dir_BC[1], dir_BC[0]])
        
        
        matrix = np.column_stack([perp_AB, -perp_BC])
        rhs = mid_BC - mid_AB
        
        if np.abs(np.linalg.det(matrix)) < 1e-10:
            return (A + B + C) / 3
        
        params = np.linalg.solve(matrix, rhs)
        circumcenter_2d = mid_AB + params[0] * perp_AB
        
        return np.array([circumcenter_2d[0], circumcenter_2d[1], 0])
    
    def get_orthocenter(self, A, B, C):
        """Calculate orthocenter of triangle ABC"""
        
        A2D = A[:2]
        B2D = B[:2]
        C2D = C[:2]
        
        
        BC = C2D - B2D
        BC_perp = np.array([-BC[1], BC[0]])
        
        
        AC = C2D - A2D
        AC_perp = np.array([-AC[1], AC[0]])
        
        
        matrix = np.column_stack([BC_perp, -AC_perp])
        rhs = B2D - A2D
        
        if np.abs(np.linalg.det(matrix)) < 1e-10:
            return (A + B + C) / 3
        
        params = np.linalg.solve(matrix, rhs)
        orthocenter_2d = A2D + params[0] * BC_perp
        
        return np.array([orthocenter_2d[0], orthocenter_2d[1], 0])
    
    def get_altitude(self, vertex, point1, point2):
        """Get altitude from vertex to line defined by point1 and point2"""
        
        v1 = point1 - point2
        v2 = vertex - point2
        
        
        proj_length = np.dot(v2, v1) / np.dot(v1, v1)
        foot = point2 + proj_length * v1
        
        return Line(vertex, foot, color=RED, stroke_width=2, stroke_opacity=0.6)
    
    def get_perpendicular_bisector_extended(self, point1, point2, opposite_vertex):
        """Get perpendicular bisector that stops at the opposite side of the triangle"""
        midpoint = (point1 + point2) / 2
        
        
        side_dir = point2 - point1
        
        perp_dir = np.array([-side_dir[1], side_dir[0], 0])
        perp_dir = perp_dir / np.linalg.norm(perp_dir)
        
        
        
        
        
        
        vertices = [point1, point2, opposite_vertex]
        other_vertices = [v for v in vertices if not np.allclose(v, point1) and not np.allclose(v, point2)]
        
        if len(other_vertices) == 1:
            
            
            
            
            
            intersection1 = self.line_intersection(midpoint, midpoint + perp_dir, point1, opposite_vertex)
            
            intersection2 = self.line_intersection(midpoint, midpoint + perp_dir, point2, opposite_vertex)
            
            
            if intersection1 is not None and self.point_on_segment(intersection1, point1, opposite_vertex):
                end_point = intersection1
            elif intersection2 is not None and self.point_on_segment(intersection2, point2, opposite_vertex):
                end_point = intersection2
            else:
                
                end_point = midpoint + 1.5 * perp_dir
        else:
            
            end_point = midpoint + 1.5 * perp_dir
        
        return Line(midpoint, end_point, color=BLUE, stroke_width=2, stroke_opacity=0.6)
    
    def line_intersection(self, p1, p2, p3, p4):
        """Find intersection of two lines defined by points (p1,p2) and (p3,p4)"""
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        x3, y3 = p3[0], p3[1]
        x4, y4 = p4[0], p4[1]
        
        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if abs(denom) < 1e-10:
            return None  
        
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
        
        x = x1 + t*(x2-x1)
        y = y1 + t*(y2-y1)
        
        return np.array([x, y, 0])
    
    def point_on_segment(self, point, seg_start, seg_end):
        """Check if a point lies on a line segment"""
        
        vec1 = point - seg_start
        vec2 = seg_end - seg_start
        
        if np.linalg.norm(vec2) < 1e-10:
            return False
        
        
        t = np.dot(vec1, vec2) / np.dot(vec2, vec2)
        
        
        return 0 <= t <= 1
    
    def get_median_tick_marks(self, point1, midpoint, point2):
        """Create tick marks on both halves of a side to show equal length"""
        
        v1 = midpoint - point1
        if np.linalg.norm(v1) > 0:
            v1 = v1 / np.linalg.norm(v1)
        
        
        perp = np.array([-v1[1], v1[0], 0]) * 0.08
        
        
        mark1_center = (point1 + midpoint) / 2
        mark1 = Line(mark1_center - perp, mark1_center + perp, color=GREEN, stroke_width=2)
        
        
        mark2_center = (midpoint + point2) / 2
        mark2 = Line(mark2_center - perp, mark2_center + perp, color=GREEN, stroke_width=2)
        
        return VGroup(mark1, mark2)
    
    def get_right_angle_marker_inside_triangle(self, point, line_point1, line_point2, opposite_vertex, size=0.12):
        """Create a right angle marker positioned inside the triangle"""
        
        centroid = (line_point1 + line_point2 + opposite_vertex) / 3
        
        
        line_dir = line_point2 - line_point1
        if np.linalg.norm(line_dir) > 0:
            line_dir = line_dir / np.linalg.norm(line_dir) * size
        
        
        perp_dir = np.array([-line_dir[1], line_dir[0], 0])
        
        
        to_centroid = centroid - point
        if np.dot(perp_dir, to_centroid) < 0:
            perp_dir = -perp_dir
        
        perp_dir = perp_dir / np.linalg.norm(perp_dir) * size
        
        
        corner1 = point + line_dir * 0.7
        corner2 = point + line_dir * 0.7 + perp_dir * 0.7
        corner3 = point + perp_dir * 0.7
        
        return VGroup(
            Line(point, corner1, color=WHITE, stroke_width=1.5),
            Line(corner1, corner2, color=WHITE, stroke_width=1.5),
            Line(corner2, corner3, color=WHITE, stroke_width=1.5)
        )
    
    def get_equal_length_marks(self, point1, mid_point, mid_point2, point2):
        """Create equal length marks on line segments"""
        
        v1 = mid_point - point1
        if np.linalg.norm(v1) > 0:
            v1 = v1 / np.linalg.norm(v1)
        
        
        perp = np.array([-v1[1], v1[0], 0]) * 0.08
        
        
        mark1_center = (point1 + mid_point) / 2
        mark1 = Line(mark1_center - perp, mark1_center + perp, color=WHITE, stroke_width=2)
        
        
        mark2_center = (mid_point2 + point2) / 2
        mark2 = Line(mark2_center - perp, mark2_center + perp, color=WHITE, stroke_width=2)
        
        return VGroup(mark1, mark2)
    
    def get_foot_of_perpendicular(self, vertex, point1, point2):
        """Get foot of perpendicular from vertex to line defined by point1 and point2"""
        v1 = point1 - point2
        v2 = vertex - point2
        
        
        proj_length = np.dot(v2, v1) / np.dot(v1, v1)
        foot = point2 + proj_length * v1
        
        return foot
    
    def get_right_angle_marker_altitude_inside(self, point, vertex, line_point1, line_point2, size=0.10):
        """Create a right angle marker for altitudes positioned inside triangle"""
        
        centroid = (line_point1 + line_point2 + vertex) / 3
        
        
        line_dir = line_point2 - line_point1
        if np.linalg.norm(line_dir) > 0:
            line_dir = line_dir / np.linalg.norm(line_dir) * size
        
        
        vertex_dir = vertex - point
        if np.linalg.norm(vertex_dir) > 0:
            vertex_dir = vertex_dir / np.linalg.norm(vertex_dir) * size
        
        
        to_centroid = centroid - point
        if np.dot(vertex_dir, to_centroid) < 0:
            vertex_dir = -vertex_dir
        
        
        corner1 = point + line_dir * 0.8
        corner2 = point + line_dir * 0.8 + vertex_dir * 0.8
        corner3 = point + vertex_dir * 0.8
        
        return VGroup(
            Line(point, corner1, color=WHITE, stroke_width=1.5),
            Line(corner1, corner2, color=WHITE, stroke_width=1.5),
            Line(corner2, corner3, color=WHITE, stroke_width=1.5)
        )


