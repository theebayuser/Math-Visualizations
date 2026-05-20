from manim import *
import numpy as np

class SumExteriorAngles(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = WHITE
        
        # Define grid centers
        centers = [
            UP * 3 + LEFT * 5.5,  # Top-left
            UP * 3 + RIGHT * 5.5,  # Top-right
            DOWN * 3 + LEFT * 5.5, # Bottom-left
            DOWN * 3 + RIGHT * 5.5 # Bottom-right
        ]
        
        # Polygon properties
        sides = [3, 4, 5, 6]
        colors = [LIGHT_BROWN, LIGHT_BLUE, PINK, LIGHT_GREEN]  # Changed BEIGE to LIGHT_BROWN
        radius = 1.5
        
        # Create polygons and store all elements
        all_polygons = []
        all_lines = []
        all_arcs = []
        all_angle_labels = []
        all_arc_groups = []
        
        for i, (n, center, color) in enumerate(zip(sides, centers, colors)):
            # Create regular polygon
            polygon = RegularPolygon(n, radius=radius, color=BLACK, fill_color=color, fill_opacity=0.7)
            polygon.move_to(center)
            polygon.rotate(PI/2)  # Rotate to have a flat base
            
            # Create extended lines
            lines = self.create_extended_lines(polygon)
            
            # Create exterior angles
            arcs, arc_group = self.create_exterior_angles(polygon, n)
            
            # Store elements
            all_polygons.append(polygon)
            all_lines.append(lines)
            all_arcs.append(arcs)
            all_arc_groups.append(arc_group)
        
        # Initial state (00:00)
        self.play(*[Create(poly) for poly in all_polygons], 
                  *[Create(line) for lines in all_lines for line in lines],
                  *[Create(arc) for arcs in all_arcs for arc in arcs],
                  run_time=1)
        self.wait(0.5)
        
        # Contraction animation (00:01-00:04)
        shrink_anims = []
        for polygon, lines, arcs, center in zip(all_polygons, all_lines, all_arcs, centers):
            shrink_anims.append(polygon.animate.scale(0.01).move_to(center))
            for line in lines:
                shrink_anims.append(line.animate.scale(0.01).move_to(center))
            for arc in arcs:
                shrink_anims.append(arc.animate.scale(0.01).move_to(center))
        
        self.play(*shrink_anims, run_time=3)
        self.wait(0.5)  # Mid-contraction (00:03)
        
        # Remove polygons, leaving only arcs (00:04)
        self.remove(*all_polygons, *[line for lines in all_lines for line in lines])
        self.wait(0.5)
        
        # Transform arcs into circles (00:05)
        circle_anims = []
        circles = []
        for i, (arcs, center) in enumerate(zip(all_arcs, centers)):
            circle = Circle(radius=0.7, color=BLACK, stroke_width=10)
            circle.move_to(center)
            circles.append(circle)
            
            # Create angle segments for the circle
            segment_group = self.create_angle_segments(circle, sides[i], arcs)
            circle_anims.append(Transform(arcs, segment_group))
        
        self.play(*circle_anims, run_time=1.5)
        self.wait(1.5)  # Hold the circles (00:06-00:07)
        
        # Expansion animation (reverse) (00:08-00:12)
        self.play(
            *[circle_anim.reverse() for circle_anim in circle_anims],
            *[anim.reverse() for anim in shrink_anims],
            run_time=4
        )
        
        # Final hold (00:12)
        self.wait(1)

    def create_extended_lines(self, polygon):
        lines = VGroup()
        vertices = polygon.get_vertices()
        n = len(vertices)
        
        for i in range(n):
            # Get current and next vertex
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]
            
            # Calculate direction vector
            direction = v2 - v1
            direction = direction / np.linalg.norm(direction)
            
            # Extend line beyond vertices
            start = v1 - direction * 1.5
            end = v2 + direction * 1.5
            
            line = Line(start, end, color=GREY, stroke_width=2)
            lines.add(line)
        
        return lines

    def create_exterior_angles(self, polygon, n_sides):
        vertices = polygon.get_vertices()
        arcs = VGroup()
        arc_group = VGroup()
        exterior_angle = 360 / n_sides
        arc_colors = [BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE]
        
        for i in range(n_sides):
            # Get three consecutive vertices
            v0 = vertices[(i - 1) % n_sides]
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n_sides]
            
            # Calculate vectors
            vec1 = v0 - v1
            vec2 = v2 - v1
            
            # Calculate angles
            angle1 = np.arctan2(vec1[1], vec1[0])
            angle2 = np.arctan2(vec2[1], vec2[0])
            angle_diff = angle2 - angle1
            
            # Adjust angle difference to be between 0 and 2π
            if angle_diff < 0:
                angle_diff += 2 * PI
                
            # Calculate exterior angle (π - interior angle)
            ext_angle = PI - (angle_diff if angle_diff < PI else 2 * PI - angle_diff)
            start_angle = angle1 - ext_angle
            
            # Create arc
            arc = Arc(
                radius=0.4,
                start_angle=start_angle,
                angle=ext_angle,
                arc_center=v1,
                color=arc_colors[i],
                stroke_width=8
            )
            arcs.add(arc)
            arc_group.add(arc.copy())
        
        return arcs, arc_group

    def create_angle_segments(self, circle, n_sides, original_arcs):
        segment_group = VGroup()
        arc_colors = [BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE]
        angle_per_segment = 2 * PI / n_sides
        center = circle.get_center()
        
        for i in range(n_sides):
            start_angle = i * angle_per_segment
            arc = Arc(
                radius=circle.radius,
                start_angle=start_angle,
                angle=angle_per_segment,
                arc_center=center,
                color=arc_colors[i],
                stroke_width=12
            )
            segment_group.add(arc)
        
        return segment_group