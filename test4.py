from manim import *

class RotationMatrices(ThreeDScene):
    def construct(self):
        # Set dark background
        self.camera.background_color = BLACK
        
        # Title
        title = MathTex(r"3\mathbb{D} \text{ } \mathbb{R}\text{otation} \text{ } \mathbb{M}\text{atrices}", font_size=50)
        title.to_edge(UP, buff=0.05)  
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)
        
        # Create three sections - matrices positions (spaced out more)
        y_positions = [2.5, 0.0, -2.5]  # Increased spacing between matrices
        
        # Function to create a Rubik's cube with shading
        def create_rubiks_cube(position, color_scheme):
            rubiks = VGroup()
            cube_size = 0.16  
            spacing = 0.17
            
            # Define colors for each face
            if color_scheme == "x":
                colors = [RED, ORANGE, YELLOW, WHITE, BLUE, GREEN]
            elif color_scheme == "y":
                colors = [GREEN, TEAL, BLUE, BLUE_A, GREEN_A, YELLOW]
            else:  # z
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
        
        # --- MATRICES & LABELS (Repositioned to be adjacent to cubes) ---
        # Helper to create matrix with background box
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

        # X-axis rotation
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
        
        # Y-axis rotation
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
        
        # Z-axis rotation
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
        
        # --- CUBE SETUP ---
        axis_config_shared = {"color": WHITE, "stroke_width": 2, "tip_length": 0.1, "tip_width": 0.1}
        axis_length = 1.8  # Reduced from 2.5 to prevent overlap
        col_x = 1.8  # Moved left from 2.5 to 1.8
        col_y = 0
        z_positions = [3, 0.5, -2]  # Adjusted to match y_positions for alignment

        # X-rotation cube
        pos_x = [col_x, col_y, z_positions[0]]
        rubiks_x = create_rubiks_cube(pos_x, "x")
        axes_x = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1], 
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_x)
        
        # Y-rotation cube
        pos_y = [col_x, col_y, z_positions[1]]
        rubiks_y = create_rubiks_cube(pos_y, "y")
        axes_y = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1],
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_y)
        
        # Z-rotation cube
        pos_z = [col_x, col_y, z_positions[2]]
        rubiks_z = create_rubiks_cube(pos_z, "z")
        axes_z = ThreeDAxes(
            x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1],
            x_length=axis_length, y_length=axis_length, z_length=axis_length, 
            axis_config=axis_config_shared
        ).move_to(pos_z)

        # Helper to create right-hand rule visualization arrows
        def create_arrow(axis_vector, position, color=YELLOW):
            # Create a basic arc in the XY plane (counter-clockwise, which is standard positive)
            # Radius slightly larger than the cube (cube side is ~0.48 total with spacing, diagonals larger)
            # cube_size=0.16, spacing=0.17. 3 blocks -> ~0.5 total width. Diagonal ~0.8.
            # Radius 0.9 seems safe.
            arrow = Arc(
                radius=0.8,
                start_angle=0,
                angle=1.5*PI,
                color=color,
                stroke_width=5
            ).add_tip()
            
            # Align the normal of the arc (Layout is in XY, normal is OUT/Z) with the target axis
            if np.array_equal(axis_vector, RIGHT): # Align Z to X
                arrow.rotate(PI/2, axis=UP)
            elif np.array_equal(axis_vector, UP): # Align Z to Y
                 arrow.rotate(-PI/2, axis=RIGHT)
            # If Z (OUT), no rotation needed as it's already in XY plane
            
            arrow.move_to(position)
            return arrow

        # Create Arrows (Matching Matrix Colors)
        arrow_x = create_arrow(RIGHT, pos_x, color=RED)
        arrow_y = create_arrow(UP, pos_y, color=GREEN)
        arrow_z = create_arrow(OUT, pos_z, color=BLUE)

        # Helper to create a trace on the corner closest to viewer
        def create_trace(cube_group, color):
            # The corner closest to viewer from the camera angle (phi=60°, theta=-45°)
            # is the front-bottom-right corner at position (2, 0, 2) in the 3x3x3 grid
            # Loop order: i (x), j (y), k (z) each 0-2
            # Index = i*9 + j*3 + k, so (2, 0, 2) = 2*9 + 0*3 + 2 = 20
            closest_corner = cube_group[20]  # Front-bottom-right corner
            trace = TracedPath(
                closest_corner.get_center, 
                stroke_color=color, 
                stroke_width=6,  # Reduced from 8 to 6
                stroke_opacity=0.9,  # Added opacity for visibility
                dissipating_time=6.5  # Increased to show full circle trace
            )
            return trace

        # Set 3D camera
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        # Don't add arrows to scene yet - they'll be created during rotation
        self.add(axes_x, rubiks_x, axes_y, rubiks_y, axes_z, rubiks_z)
        
        # Animate labels appearing (without arrows initially)
        self.play(
            Write(x_label), Write(y_label), Write(z_label),
            Write(x_matrix_group), Write(y_matrix_group), Write(z_matrix_group),
            run_time=2
        )

        self.wait(0.5)
        
        # --- ANIMATION PART 1: Complete one full rotation (No Trace) ---
        # Start rotation, then show arrows after 1 second
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

        # --- ANIMATION PART 2: Add Traces ---
        trace_x = create_trace(rubiks_x, RED)     # Match x-axis matrix color
        trace_y = create_trace(rubiks_y, GREEN)   # Match y-axis matrix color
        trace_z = create_trace(rubiks_z, BLUE)    # Match z-axis matrix color
        
        self.add(trace_x, trace_y, trace_z)

        # --- ANIMATION PART 3: One complete rotation with trace (full circle) ---
        self.play(
            Rotate(rubiks_x, angle=2*PI, axis=RIGHT, about_point=rubiks_x.get_center()),
            Rotate(rubiks_y, angle=2*PI, axis=UP, about_point=rubiks_y.get_center()),
            Rotate(rubiks_z, angle=2*PI, axis=OUT, about_point=rubiks_z.get_center()),
            run_time=6,
            rate_func=linear
        )
        
        self.wait(1)