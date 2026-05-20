from manim import *

class ElegantRadianAnimation(Scene):
    def construct(self):
        # Configure background
        self.camera.background_color = BLACK
        
        # Add title that stays throughout the video - using a cool color, smaller and lower
        title = MathTex("\\mathbb{D}\\text{erivation of a }\\mathbb{R}\\text{adian}", 
                       color=TEAL_C, font_size=28)
        title.to_edge(UP, buff=0.6)
        title.set_glow_opacity(0.6)
        
        # THE SETUP (0-4s) - Start with just the radius - much smaller
        self.play(
            Write(title, run_time=2),
            rate_func=smooth
        )
        
        # Create the initial radius line (glowing orange) - much smaller
        radius_line = Line(ORIGIN, RIGHT * 1.0, color=ORANGE, stroke_width=4)
        radius_line.set_glow_opacity(0.8)
        
        # Radius label - "1 radius" - smaller font
        radius_label = MathTex("1~\\text{radius}", color=ORANGE, font_size=20)
        radius_label.next_to(radius_line, DOWN, buff=0.2)
        radius_label.set_glow_opacity(0.8)
        
        self.play(
            DrawBorderThenFill(radius_line, run_time=1.5),
            FadeIn(radius_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # Trace out the circle using the radius - much smaller radius
        circle = Circle(radius=1.0, color=GREY_B, stroke_width=2, stroke_opacity=0.5)
        
        # Create a rotating radius to trace the circle
        rotating_radius = radius_line.copy()
        
        # Animate the radius rotating to trace the circle
        self.play(
            Create(circle, run_time=2),
            Rotate(rotating_radius, angle=2*PI, about_point=ORIGIN, run_time=2),
            rate_func=smooth
        )
        
        # Remove the rotating radius and keep the original
        self.remove(rotating_radius)
        
        # Create coordinate axes - MUCH smaller and more constrained
        axes = Axes(
            x_range=[-0.6, 0.6, 0.5],
            y_range=[-0.6, 0.6, 0.5],
            x_length=4,
            y_length=4,
            axis_config={
                "color": GREY_B, 
                "stroke_width": 1, 
                "stroke_opacity": 0.4,
                "tip_length": 0.02,
                "tip_width": 0.04
            }
        )
        
        self.play(
            FadeIn(axes, run_time=1),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # THE "WRAP" - Simple wrapping animation (4-8s)
        # Step 1: Move the line to be tangent with the circle
        tangent_line = Line(RIGHT * 1.0, RIGHT * 1.0 + UP * 1.0, color=ORANGE, stroke_width=4)
        tangent_line.set_glow_opacity(0.8)
        
        # Animate moving the line to the tangent position
        self.play(
            Transform(radius_line, tangent_line, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # Step 2: In one smooth animation, wrap it around the circle
        # Create the target arc (1 radian) - smaller
        target_arc = Arc(
            radius=1.0,
            start_angle=0,
            angle=1,
            color=BLUE_C,
            stroke_width=5
        )
        target_arc.set_glow_opacity(0.8)
        
        # Single smooth wrapping animation
        self.play(
            Transform(radius_line, target_arc, run_time=2.5),
            rate_func=smooth
        )
        
        # Store reference to the blue arc for proper cleanup
        blue_arc = radius_line
        
        self.wait(0.5)
        
        # THE COUNT-UP (8-16s)
        # Create a fixed position for angle measurements - moved up and closer to center
        angle_label_position = LEFT * 1.3 + DOWN * 0.8
        
        # Define the first angle and label it "1 rad" - smaller
        first_sector = Sector(
            angle=1,
            radius=1.0,
            color=BLUE_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        # Add angle mark for first radian - smaller
        angle_mark_1 = Arc(
            radius=0.3,
            start_angle=0,
            angle=1,
            color=BLUE_C,
            stroke_width=2
        )
        angle_mark_1.set_glow_opacity(0.8)
        
        # Create "1 radian" label that morphs from "1 radius" - smaller font
        one_radian_label = MathTex("1~\\text{radian}", color=BLUE_C, font_size=20)
        one_radian_label.move_to(angle_label_position)
        one_radian_label.set_glow_opacity(0.8)
        
        # Move the existing radius label to the fixed position and change its color
        self.play(
            radius_label.animate.move_to(angle_label_position).set_color(BLUE_C),
            FadeIn(first_sector, run_time=1),
            Create(angle_mark_1, run_time=1),
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Now morph "1 radius" to "1 radian"
        self.play(
            Transform(radius_label, one_radian_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # Second arc and angle (Green) - smaller
        second_arc = Arc(
            radius=1.0,
            start_angle=1,
            angle=1,
            color=GREEN_C,
            stroke_width=5
        )
        second_arc.set_glow_opacity(0.8)
        
        second_sector = Sector(
            angle=1,
            radius=1.0,
            start_angle=1,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        # Add angle mark for second radian - smaller
        angle_mark_2 = Arc(
            radius=0.3,
            start_angle=1,
            angle=1,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_2.set_glow_opacity(0.8)
        
        # Update label to "2 radians" - same position, smaller font
        count_label_2 = MathTex("2~\\text{radians}", color=GREEN_C, font_size=20)
        count_label_2.move_to(angle_label_position)
        count_label_2.set_glow_opacity(0.8)
        
        self.play(
            Create(second_arc, run_time=1.5),
            FadeIn(second_sector, run_time=1.5),
            Create(angle_mark_2, run_time=1.5),
            Transform(radius_label, count_label_2, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # Third arc and angle (keeping Green theme) - smaller
        third_arc = Arc(
            radius=1.0,
            start_angle=2,
            angle=1,
            color=GREEN_C,
            stroke_width=5
        )
        third_arc.set_glow_opacity(0.8)
        
        third_sector = Sector(
            angle=1,
            radius=1.0,
            start_angle=2,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        # Add angle mark for third radian - smaller
        angle_mark_3 = Arc(
            radius=0.3,
            start_angle=2,
            angle=1,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_3.set_glow_opacity(0.8)
        
        # Update label to "3 radians" - same position, smaller font
        count_label_3 = MathTex("3~\\text{radians}", color=GREEN_C, font_size=20)
        count_label_3.move_to(angle_label_position)
        count_label_3.set_glow_opacity(0.8)
        
        self.play(
            Create(third_arc, run_time=1.5),
            FadeIn(third_sector, run_time=1.5),
            Create(angle_mark_3, run_time=1.5),
            Transform(radius_label, count_label_3, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # THE "PI" REVEAL (16-20s)
        # Animate the tiny final piece to complete the semicircle - smaller
        final_gap_arc = Arc(
            radius=1.0,
            start_angle=3,
            angle=PI - 3,  # Small remaining gap to π
            color=GREEN_C,
            stroke_width=5
        )
        final_gap_arc.set_glow_opacity(0.8)
        
        final_gap_sector = Sector(
            angle=PI - 3,
            radius=1.0,
            start_angle=3,
            color=GREEN_C,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        # Add angle mark for the final gap - smaller
        angle_mark_final = Arc(
            radius=0.3,
            start_angle=3,
            angle=PI - 3,
            color=GREEN_C,
            stroke_width=2
        )
        angle_mark_final.set_glow_opacity(0.8)
        
        # Pi label - same position, smaller font
        pi_label = MathTex("\\pi~\\text{radians}", color=GREEN_C, font_size=20)
        pi_label.move_to(angle_label_position)
        pi_label.set_glow_opacity(0.8)
        
        self.play(
            Create(final_gap_arc, run_time=1.5),
            FadeIn(final_gap_sector, run_time=1.5),
            Create(angle_mark_final, run_time=1.5),
            Transform(radius_label, pi_label, run_time=1.5),
            rate_func=smooth
        )
        
        self.wait(1)
        
        # THE CONCLUSION (20-24s)
        # Create the second half of the circle - smaller
        second_half_arc = Arc(
            radius=1.0,
            start_angle=PI,
            angle=PI,
            color=GREEN_C,
            stroke_width=5
        )
        second_half_arc.set_glow_opacity(0.8)
        
        second_half_sector = Sector(
            angle=PI,
            radius=1.0,
            start_angle=PI,
            color=GREEN_C,
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Second half angle mark - smaller
        second_half_angle_mark = Arc(
            radius=0.3,
            start_angle=PI,
            angle=PI,
            color=GREEN_C,
            stroke_width=2
        )
        second_half_angle_mark.set_glow_opacity(0.8)
        
        # 2π label - same position, smaller font
        two_pi_label = MathTex("2\\pi~\\text{radians}", color=GREEN_C, font_size=20)
        two_pi_label.move_to(angle_label_position)
        two_pi_label.set_glow_opacity(0.8)
        
        # Animate the duplication and rotation
        self.play(
            Create(second_half_arc, run_time=1.5),
            FadeIn(second_half_sector, run_time=1.5),
            Create(second_half_angle_mark, run_time=1.5),
            Transform(radius_label, two_pi_label, run_time=1.5),
            rate_func=smooth
        )
        
        # Hold on the final clean image
        self.wait(3)
        
        # Fade to black - fade everything properly including the blue arc
        self.play(
            FadeOut(VGroup(
                axes, circle, blue_arc, second_arc, third_arc, final_gap_arc, 
                first_sector, second_sector, third_sector, final_gap_sector,
                second_half_arc, second_half_sector, angle_mark_1, angle_mark_2, 
                angle_mark_3, angle_mark_final, second_half_angle_mark, 
                radius_label, title
            ), run_time=2),
            rate_func=smooth
        )
        
        self.wait(1)