from manim import *
import numpy as np
import random

class GoldenRatioSpiralCinema(Scene):
    def construct(self):
        
        self.camera.background_color = BLACK
        
        
        
        particles = VGroup()
        for i in range(30):
            particle = Dot(radius=0.02, color=GOLD)
            particle.move_to([
                random.uniform(-7, 7),
                random.uniform(-4, 4),
                0
            ])
            particle.set_opacity(random.uniform(0.3, 0.8))
            particles.add(particle)
        
        
        self.play(
            *[FadeIn(p, shift=UP*0.5) for p in particles],
            run_time=3
        )
        
        
        self.play(
            *[p.animate.move_to(ORIGIN + 0.1*np.array([
                np.cos(i*0.5), np.sin(i*0.5), 0
            ])) for i, p in enumerate(particles)],
            run_time=2
        )
        
        
        self.play(
            *[FadeOut(p, shift=5*np.array([
                np.cos(i*0.3), np.sin(i*0.3), 0
            ])) for i, p in enumerate(particles)],
            run_time=1.5
        )
        
        
        
        fib_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        fib_texts = []
        
        for i, num in enumerate(fib_numbers):
            
            size = 24 + i * 4
            color_intensity = interpolate_color(WHITE, GOLD, i / len(fib_numbers))
            
            fib_text = Text(str(num), font_size=size, color=color_intensity)
            fib_text.move_to([
                -5 + i * 1.0,
                2 + 0.3 * np.sin(i * 0.5),
                0
            ])
            
            
            fib_text.scale(0.1)
            self.add(fib_text)
            self.play(
                fib_text.animate.scale(10).set_opacity(1),
                run_time=0.4 + i * 0.1
            )
            
            
            if i > 5:  
                self.play(
                    fib_text.animate.set_color(YELLOW).scale(1.2),
                    run_time=0.2
                )
                self.play(
                    fib_text.animate.set_color(color_intensity).scale(1/1.2),
                    run_time=0.2
                )
            
            fib_texts.append(fib_text)
            self.wait(0.1)
        
        
        self.wait(1)
        
        
        
        self.play(
            *[FadeOut(text, shift=DOWN*2) for text in fib_texts],
            run_time=2
        )
        
        
        phi_formula = MathTex(
            r"\phi = \frac{1 + \sqrt{5}}{2}",
            font_size=80,
            color=GOLD
        )
        phi_formula.move_to(UP * 2)
        
        
        phi_formula.set_stroke(YELLOW, width=3, opacity=0.8)
        self.play(
            DrawBorderThenFill(phi_formula),
            run_time=3
        )
        
        
        for _ in range(3):
            self.play(
                phi_formula.animate.set_stroke(opacity=1, width=5),
                run_time=0.4
            )
            self.play(
                phi_formula.animate.set_stroke(opacity=0.8, width=3),
                run_time=0.4
            )
        
        
        phi_value = MathTex(
            r"\phi \approx 1.618033988...",
            font_size=60,
            color=GOLD
        )
        phi_value.next_to(phi_formula, DOWN, buff=1)
        
        self.play(
            Write(phi_value),
            run_time=2
        )
        self.wait(1)
        
        
        
        self.play(
            phi_formula.animate.scale(0.5).to_corner(UL),
            FadeOut(phi_value),
            run_time=1.5
        )
        
        
        unit_square = Square(side_length=2, color=BLUE, fill_opacity=0.2)
        unit_square.move_to(LEFT * 2)
        
        self.play(
            DrawBorderThenFill(unit_square),
            run_time=1.5
        )
        
        
        square_label = Text("1", font_size=36, color=BLUE)
        square_label.move_to(unit_square.get_center())
        self.play(Write(square_label), run_time=0.8)
        
        
        golden_width = 2 * 1.618  
        golden_rect = Rectangle(
            width=golden_width, 
            height=2, 
            color=GOLD, 
            fill_opacity=0.2
        )
        golden_rect.next_to(unit_square, RIGHT, buff=0)
        
        self.play(
            DrawBorderThenFill(golden_rect),
            run_time=2
        )
        
        
        phi_label = MathTex(r"\phi", font_size=48, color=GOLD)
        phi_label.move_to(golden_rect.get_center())
        self.play(Write(phi_label), run_time=1)
        
        self.wait(1)
        
        
        
        self.play(
            *[FadeOut(mob) for mob in [unit_square, golden_rect, square_label, phi_label]],
            run_time=1
        )
        
        
        squares = []
        square_sizes = [0.2, 0.2, 0.4, 0.6, 1.0, 1.6, 2.6]  
        colors = [RED, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        current_pos = ORIGIN
        
        for i, (size, color) in enumerate(zip(square_sizes, colors)):
            square = Square(side_length=size, color=color, fill_opacity=0.3)
            
            
            if i == 0:
                square.move_to(current_pos)
            elif i == 1:
                square.next_to(squares[0], RIGHT, buff=0)
            elif i == 2:
                square.next_to(squares[1], UP, buff=0, aligned_edge=RIGHT)
            elif i == 3:
                square.next_to(squares[2], LEFT, buff=0, aligned_edge=UP)
            elif i == 4:
                square.next_to(squares[3], DOWN, buff=0, aligned_edge=LEFT)
            elif i == 5:
                square.next_to(squares[4], RIGHT, buff=0, aligned_edge=DOWN)
            elif i == 6:
                square.next_to(squares[5], UP, buff=0, aligned_edge=RIGHT)
            
            
            square.scale(0.1)
            self.add(square)
            self.play(
                square.animate.scale(10),
                run_time=0.8
            )
            
            
            fib_label = Text(str(fib_numbers[i]), font_size=int(size*20+10), color=WHITE)
            fib_label.move_to(square.get_center())
            self.play(FadeIn(fib_label), run_time=0.4)
            
            squares.append(square)
            self.wait(0.3)
        
        self.wait(1)
        
        
        
        spiral_points = []
        
        
        for i in range(50):
            angle = i * 0.3
            radius = 0.1 * (1.618 ** (angle / 5))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            spiral_points.append([x, y, 0])
        
        
        spiral_curve = VMobject()
        spiral_curve.set_points_smoothly(spiral_points)
        spiral_curve.set_color(GOLD)
        spiral_curve.set_stroke(width=4)
        
        
        spiral_glow = spiral_curve.copy()
        spiral_glow.set_stroke(YELLOW, width=8, opacity=0.5)
        
        
        self.play(
            Create(spiral_glow),
            Create(spiral_curve),
            run_time=4
        )
        
        
        
        formulas = [
            r"\phi^2 = \phi + 1",
            r"\frac{1}{\phi} = \phi - 1", 
            r"\phi = 1 + \frac{1}{1 + \frac{1}{1 + \frac{1}{1 + \ddots}}}",
            r"F_n = \frac{\phi^n - (-\phi)^{-n}}{\sqrt{5}}"
        ]
        
        
        positions = [UP*2.5 + RIGHT*3, DOWN*2.5 + RIGHT*3, UP*2.5 + LEFT*4, DOWN*2.5 + LEFT*4]
        
        formula_mobs = []
        for formula, pos in zip(formulas, positions):
            formula_mob = MathTex(formula, font_size=32, color=WHITE)
            formula_mob.move_to(pos)
            formula_mob.set_stroke(GOLD, width=1, opacity=0.8)
            formula_mobs.append(formula_mob)
        
        
        for i, formula_mob in enumerate(formula_mobs):
            self.play(
                DrawBorderThenFill(formula_mob),
                run_time=1.5
            )
            self.wait(0.5)
        
        self.wait(2)
        
        
        
        nature_text = Text("Found everywhere in nature...", font_size=36, color=GREEN)
        nature_text.to_edge(UP)
        
        self.play(
            *[FadeOut(f, shift=UP) for f in formula_mobs],
            Write(nature_text),
            run_time=2
        )
        
        
        small_spirals = VGroup()
        for i in range(8):
            small_spiral = spiral_curve.copy()
            small_spiral.scale(0.3)
            small_spiral.move_to([
                random.uniform(-6, 6),
                random.uniform(-3, 2),
                0
            ])
            small_spiral.rotate(random.uniform(0, 2*PI))
            small_spiral.set_color(random.choice([GREEN, BLUE, YELLOW, ORANGE]))
            small_spirals.add(small_spiral)
        
        self.play(
            LaggedStart(
                *[Create(s) for s in small_spirals],
                lag_ratio=0.2
            ),
            run_time=3
        )
        
        self.wait(1)
        
        
        
        self.play(
            *[FadeOut(mob) for mob in small_spirals],
            FadeOut(nature_text),
            run_time=1.5
        )
        
        
        giant_phi = MathTex(r"\phi", font_size=200, color=GOLD)
        giant_phi.set_stroke(YELLOW, width=5, opacity=0.8)
        
        self.play(
            Transform(spiral_curve, giant_phi),
            FadeOut(spiral_glow),
            run_time=3
        )
        
        
        self.play(
            Rotate(spiral_curve, 2*PI),
            spiral_curve.animate.set_stroke(width=8, opacity=1),
            run_time=4
        )
        
        
        for _ in range(5):
            self.play(
                spiral_curve.animate.scale(1.1).set_color(YELLOW),
                run_time=0.3
            )
            self.play(
                spiral_curve.animate.scale(1/1.1).set_color(GOLD),
                run_time=0.3
            )
        
        self.wait(2)
        
        
        final_particles = VGroup()
        for i in range(40):
            particle = Dot(radius=0.03, color=GOLD)
            particle.move_to(ORIGIN)
            final_particles.add(particle)
        
        self.add(final_particles)
        self.play(
            *[p.animate.move_to(8*np.array([
                np.cos(i*0.157), np.sin(i*0.157), 0
            ])).fade(1) for i, p in enumerate(final_particles)],
            FadeOut(spiral_curve),
            run_time=3
        )
        
        self.wait(1)

class MathematicalConstantsJourney(Scene):
    def construct(self):
        """Alternative cinematic animation exploring mathematical constants"""
        self.camera.background_color = BLACK
        
        
        title = Text("The Language of the Universe", font_size=48, color=WHITE)
        title.set_stroke(BLUE, width=2, opacity=0.7)
        
        self.play(
            Write(title),
            run_time=3
        )
        self.wait(1)
        
        self.play(
            title.animate.scale(0.5).to_corner(UL),
            run_time=1.5
        )
        
        
        pi_symbol = MathTex(r"\pi", font_size=120, color=BLUE)
        
        
        pi_copies = VGroup()
        for i in range(8):
            pi_copy = pi_symbol.copy()
            angle = i * PI / 4
            pi_copy.move_to(6 * np.array([np.cos(angle), np.sin(angle), 0]))
            pi_copy.set_opacity(0.3)
            pi_copies.add(pi_copy)
        
        self.add(pi_copies)
        self.play(
            *[pc.animate.move_to(ORIGIN).set_opacity(1) for pc in pi_copies],
            run_time=2
        )
        
        
        self.play(
            Transform(pi_copies, pi_symbol),
            run_time=1.5
        )
        
        
        pi_digits = Text("3.14159265358979323846...", font_size=32, color=BLUE)
        pi_digits.next_to(pi_copies, DOWN, buff=1)
        
        
        for i in range(len("3.14159265358979323846...")):
            partial = Text("3.14159265358979323846..."[:i+1], font_size=32, color=BLUE)
            partial.move_to(pi_digits.get_center())
            if i == 0:
                self.play(Write(partial), run_time=0.2)
            else:
                self.play(Transform(pi_digits, partial), run_time=0.1)
            if i == 0:
                pi_digits = partial
        
        self.wait(1)
        
        
        self.play(
            pi_copies.animate.shift(LEFT * 4).scale(0.7),
            pi_digits.animate.shift(LEFT * 4).scale(0.7),
            run_time=1.5
        )
        
        
        e_symbol = MathTex(r"e", font_size=120, color=GREEN)
        e_symbol.move_to(RIGHT * 1)
        
        
        e_temp = e_symbol.copy()
        e_temp.scale(0.1).move_to(ORIGIN)
        self.add(e_temp)
        
        self.play(
            Rotate(e_temp, 4*PI),
            e_temp.animate.scale(10).move_to(RIGHT * 1).set_color(GREEN),
            run_time=2.5
        )
        
        e_formula = MathTex(r"e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n", 
                           font_size=28, color=GREEN)
        e_formula.next_to(e_temp, DOWN, buff=1)
        
        self.play(Write(e_formula), run_time=2)
        self.wait(1)
        
        
        self.play(
            Group(pi_copies, pi_digits, e_temp, e_formula).animate.scale(0.6).to_edge(LEFT),
            run_time=1.5
        )
        
        phi_symbol = MathTex(r"\phi", font_size=120, color=GOLD)
        phi_symbol.move_to(RIGHT * 2)
        
        
        particles = VGroup()
        for i in range(20):
            particle = Dot(radius=0.05, color=GOLD)
            particle.move_to([
                random.uniform(-3, 7),
                random.uniform(-3, 3),
                0
            ])
            particles.add(particle)
        
        self.add(particles)
        self.play(
            *[p.animate.move_to(phi_symbol.get_center()) for p in particles],
            run_time=2
        )
        
        self.play(
            Transform(particles, phi_symbol),
            run_time=1
        )
        
        
        self.play(
            *[FadeOut(mob) for mob in [pi_copies, pi_digits, e_temp, e_formula]],
            particles.animate.move_to(ORIGIN).scale(0.8),
            run_time=2
        )
        
        
        beauty_text = Text("The most beautiful equation in mathematics", 
                          font_size=32, color=WHITE)
        beauty_text.to_edge(UP, buff=1)
        
        self.play(Write(beauty_text), run_time=2)
        
        
        euler_parts = [
            MathTex(r"e", font_size=80, color=GREEN),
            MathTex(r"^{i\pi}", font_size=60, color=BLUE), 
            MathTex(r"+ 1", font_size=80, color=WHITE),
            MathTex(r"= 0", font_size=80, color=RED)
        ]
        
        
        euler_parts[0].move_to(LEFT * 2)
        euler_parts[1].next_to(euler_parts[0], RIGHT, buff=0.1, aligned_edge=UP)
        euler_parts[2].next_to(euler_parts[1], RIGHT, buff=0.3)
        euler_parts[3].next_to(euler_parts[2], RIGHT, buff=0.3)
        
        
        for i, part in enumerate(euler_parts):
            if i == 0:
                
                self.play(
                    Transform(particles, part),
                    run_time=1.5
                )
            else:
                
                part.scale(0.1)
                self.add(part)
                self.play(
                    part.animate.scale(10),
                    run_time=1
                )
            self.wait(0.5)
        
        
        complete_equation = VGroup(particles, *euler_parts[1:])
        for _ in range(3):
            self.play(
                complete_equation.animate.set_stroke(YELLOW, width=3, opacity=1),
                run_time=0.5
            )
            self.play(
                complete_equation.animate.set_stroke(opacity=0),
                run_time=0.5
            )
        
        self.wait(2)
        
        
        
        self.play(
            *[FadeOut(mob) for mob in [beauty_text, particles] + euler_parts[1:]],
            run_time=2
        )
        
        
        cosmic_symbols = VGroup()
        symbols = [r"\pi", r"e", r"\phi", r"\infty", r"\sum", r"\int", r"\partial", r"\nabla"]
        
        for i in range(30):
            symbol = MathTex(random.choice(symbols), font_size=random.randint(20, 60))
            symbol.move_to([
                random.uniform(-7, 7),
                random.uniform(-4, 4),
                0
            ])
            symbol.set_color(random.choice([BLUE, GREEN, GOLD, WHITE, PURPLE]))
            symbol.set_opacity(random.uniform(0.2, 0.6))
            cosmic_symbols.add(symbol)
        
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=UP*0.5) for s in cosmic_symbols],
                lag_ratio=0.1
            ),
            run_time=4
        )
        
        
        self.play(
            *[Rotate(s, 2*PI, about_point=ORIGIN) for s in cosmic_symbols],
            run_time=8
        )
        
        
        final_text = Text("Mathematics: The Universe's Hidden Language", 
                         font_size=40, color=GOLD)
        final_text.set_stroke(WHITE, width=2, opacity=0.7)
        
        self.play(
            Write(final_text),
            *[FadeOut(s) for s in cosmic_symbols],
            run_time=3
        )
        
        self.wait(2)
        
        self.play(FadeOut(final_text), run_time=3)



