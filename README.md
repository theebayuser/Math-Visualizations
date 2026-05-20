# Math Animations 

This repository contains the Python source code for my mathematical animations, created using the [Manim](https://www.manim.community/) community edition engine. You can see the final rendered videos on my Instagram page https://www.instagram.com/math.visualizations/

## Topics Covered
Here are some of the concepts I've visualized in this repository:
* **Calculus:** Derivatives, Limits, and the Fundamental Theorem of Calculus.
* **Algebra & Number Theory:** Fibonacci sequences, Diophantine equations, and Euler's formula.
* **Geometry:** Conic sections, circles, and inverse Pythagorean theorems.

##  How to Run Locally
To run these scripts on your own machine, you will need to install Manim and its core dependencies (like LaTeX and FFmpeg). 

Once installed, you can render a low-quality preview of any script by running:
`manim -pql filename.py SceneName`

To render the final 1080p 60fps version for social media, run:
`manim -pqh filename.py SceneName`