# Math Animations

This repository contains the Python source code for my mathematical animations, created using the [Manim](https://www.manim.community/) community edition engine. You can see the final rendered videos on my Instagram page https://www.instagram.com/math.visualizations/

Each `.py` file at the repo root is one self-contained animation — pick a topic, open the file, and run it (see below).

## Topics Covered
Here are some of the concepts I've visualized in this repository (not exhaustive — browse the repo root for the full list):
* **Calculus:** Derivatives, limits, the squeeze theorem, the Fundamental Theorem of Calculus, integration by parts, Taylor series, Riemann sums.
* **Algebra & Number Theory:** Fibonacci sequences, Diophantine equations, Euler's formula, the AM-GM inequality, prime spirals.
* **Geometry & Linear Algebra:** Conic sections, circles, inverse Pythagorean theorem, rotation matrices, Cramer's rule, Bezier curves.
* **Probability & Physics:** Bayes' theorem, the Boltzmann distribution, Lorentz transformations, the three-body problem.
* **For fun:** A Rubik's cube speedsolve, the Peano curve, and more.

The `finished/` folder holds a handful of scripts kept separate from the root — treat it as an archive/reference subset rather than assuming everything else at the root is unfinished.

## How to Run Locally
To run these scripts on your own machine, you will need to install Manim and its core dependencies (like LaTeX and FFmpeg).

Once installed, you can render a low-quality preview of any script by running:
```
manim -pql filename.py SceneName
```

To render the final high-quality version for social media, run:
```
manim -pqh filename.py SceneName
```

`SceneName` is the Manim `Scene`/`ThreeDScene` class defined in that file (e.g. `ConicSections` in `conics.py`).

## Contributing / working in this repo with an AI agent
See [`CLAUDE.md`](CLAUDE.md) for the house style (title formatting, color conventions, video format choices) and workflow notes for coding agents working in this repo. It's a living document — if you're an agent and you learn something worth remembering, add it there.
