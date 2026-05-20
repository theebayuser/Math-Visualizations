from manim import *

class RotationMatrices(ThreeDScene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        title = MathTex(r"3\mathbb{D} \text{ } \mathbb{R}\text{otation} \text{ } \mathbb{M}\text{atrices}", font_size=50)
        title.to_edge(UP, buff=0.05)  
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)
        
        
        y_positions = [2.5, 0.0, -2.5]  
        
        
        def create_rubiks_cube(position, color_scheme):
            rubiks = VGroup()
            cube_size = 0.16  
            spacing = 0.17
            
            
            if color_scheme == "x":
                colors = [RED, ORANGE, YELLOW, WHITE, BLUE, GREEN]
            elif color_scheme == "y":
                colors = [GREEN, TEAL, BLUE, BLUE_A, GREEN_A, YELLOW]
            else:  
                colors = [BLUE, PURPLE, PINK, MAROON, BLUE_D, PURPLE_D]
            
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        small_cube = Cube(
                            side_length=cube_size, 
                            fill_opacity=0.95, 
                            stroke_width=2, 
                            stroke_color=BLACK,
                            sheen_factor=0.3,
                            sheen_direction=UP+RIGHT
                        )
                        color_index = (i + j + k) % len(colors)
                        small_cube.set_color(colors[color_index])
                        small_cube.set_sheen(-0.4, direction=UP+RIGHT)
                        small_cube.move_to([
                            (i - 1) * spacing,
                            (j - 1) * spacing,
                            (k - 1) * spacing
                        ])
                        rubiks.add(small_cube)
            
            rubiks.move_to(position)
            return rubiks
        
        
        
        def create_matrix_box(matrix, color):
            bg = RoundedRectangle(
                width=matrix.width + 0.4,
                height=matrix.height,
                corner_radius=0.1,
                fill_color=GREY_E,
                fill_opacity=0.8,
                stroke_color=color,
                stroke_width=2
            )
            group = VGroup(bg, matrix)
            return group

        
        x_label = Text("Rotation about x-axis", font_size=20, color=RED).move_to([-1.5, y_positions[0] + 0.8, 0])
        x_matrix = MathTex(
            r"R_x = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{pmatrix}", 
            font_size=22, color=RED
        ).move_to([-1.5, y_positions[0] - 0.05, 0])
        x_bg = RoundedRectangle(
            width=x_matrix.width + 0.4,
            height=x_matrix.height + 0.3,
            corner_radius=0.1,
            fill_color=GREY_E,
            fill_opacity=0.8,
            stroke_color=RED,
            stroke_width=2
        ).move_to(x_matrix.get_center())
        x_matrix_group = VGroup(x_bg, x_matrix)
        
        
        y_label = Text("Rotation about y-axis", font_size=20, color=GREEN).move_to([-1.5, y_positions[1] + 0.8, 0])
        y_matrix = MathTex(
            r"R_y = \begin{pmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{pmatrix}", 
            font_size=22, color=GREEN
        ).move_to([-1.5, y_positions[1] - 0.05, 0])
        y_bg = RoundedRectangle(
            width=y_matrix.width + 0.4,
            height=y_matrix.height + 0.3,
            corner_radius=0.1,
            fill_color=GREY_E,
            fill_opacity=0.8,
            stroke_color=GREEN,
            stroke_width=2
        ).move_to(y_matrix.get_center())
        y_matrix_group = VGroup(y_bg, y_matrix)
        
        
        z_label = Text("Rotation about z-axis", font_size=20, color=BLUE).move_to([-1.5, y_positions[2] + 0.8, 0])
        z_matrix = MathTex(
            r"R_z = \begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}", 
            font_size=22, color=BLUE
        ).move_to([-1.5, y_positions[2] - 0.05, 0])
        z_bg = RoundedRectangle(
            width=z_matrix.width + 0.4,
            height=z_matrix.height + 0.3,
            corner_radius=0.1,
            fill_color=GREY_E,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        ).move_to(z_matrix.get_center())
        z_matrix_group = VGroup(z_bg, z_matrix)
        
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label, x_matrix_group, y_matrix_group, z_matrix_group)
        
        
        axis_config_shared = {"color": WHITE, "stroke_width": 2, "tip_length": 0.1, "tip_width": 0.1}
        axis_length = 1.8  
        col_x = 1.8  
        col_y = 0
        z_positions = [3, 0.5, -2]  

        
        pos_x = [col_x, col_y, z_positions[0]]
        rubiks_x = create_rubiks_cube(pos_x, "x")
        axes_x = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1], 
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_x)
        
        
        pos_y = [col_x, col_y, z_positions[1]]
        rubiks_y = create_rubiks_cube(pos_y, "y")
        axes_y = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1],
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_y)
        
        
        pos_z = [col_x, col_y, z_positions[2]]
        rubiks_z = create_rubiks_cube(pos_z, "z")
        axes_z = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1],
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_z)

        
        def create_arrow(axis_vector, position, color=YELLOW):
            
            
            
            
            arrow = Arc(
                radius=0.8,
                start_angle=0,
                angle=1.5*PI,
                color=color,
                stroke_width=5
            ).add_tip()
            
            
            if np.array_equal(axis_vector, RIGHT): 
                arrow.rotate(PI/2, axis=UP)
            elif np.array_equal(axis_vector, UP): 
                 arrow.rotate(-PI/2, axis=RIGHT)
            
            
            arrow.move_to(position)
            return arrow

        
        arrow_x = create_arrow(RIGHT, pos_x, color=RED)
        arrow_y = create_arrow(UP, pos_y, color=GREEN)
        arrow_z = create_arrow(OUT, pos_z, color=BLUE)

        
        def create_trace(cube_group, color):
            
            
            
            
            closest_corner = cube_group[20]  
            trace = TracedPath(
                closest_corner.get_center, 
                stroke_color=color, 
                stroke_width=6,  
                stroke_opacity=0.9,  
                dissipating_time=6.5  
            )
            return trace

        
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        self.add(axes_x, rubiks_x, axes_y, rubiks_y, axes_z, rubiks_z)
        
        
        self.play(
            Write(x_label), Write(y_label), Write(z_label),
            Write(x_matrix_group), Write(y_matrix_group), Write(z_matrix_group),
            run_time=2
        )

        self.wait(0.5)
        
        
        
        self.play(
            Rotate(rubiks_x, angle=2*PI, axis=RIGHT, about_point=rubiks_x.get_center(), run_time=6, rate_func=linear),
            Rotate(rubiks_y, angle=2*PI, axis=UP, about_point=rubiks_y.get_center(), run_time=6, rate_func=linear),
            Rotate(rubiks_z, angle=2*PI, axis=OUT, about_point=rubiks_z.get_center(), run_time=6, rate_func=linear),
            Succession(
                Wait(1),
                AnimationGroup(
                    Create(arrow_x),
                    Create(arrow_y),
                    Create(arrow_z),
                    run_time=0.5
                )
            )
        )
        
        self.wait(0.5)

        
        trace_x = create_trace(rubiks_x, RED)     
        trace_y = create_trace(rubiks_y, GREEN)   
        trace_z = create_trace(rubiks_z, BLUE)    
        
        self.add(trace_x, trace_y, trace_z)

        
        self.play(
            Rotate(rubiks_x, angle=2*PI, axis=RIGHT, about_point=rubiks_x.get_center()),
            Rotate(rubiks_y, angle=2*PI, axis=UP, about_point=rubiks_y.get_center()),
            Rotate(rubiks_z, angle=2*PI, axis=OUT, about_point=rubiks_z.get_center()),
            run_time=6,
            rate_func=linear
        )
        
        self.wait(1)