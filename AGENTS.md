# AGENTS.md

Guidance for Codex (or any agent) working in this repository. This file
is a **living document** — see "Keeping this file current" at the bottom.

## What this repo is

Source code for Daniel's math-animation videos, built with
[Manim Community Edition](https://www.manim.community/) and posted to
Instagram [@math.visualizations](https://www.instagram.com/math.visualizations/).
Each `.py` file at the repo root is one self-contained animation (flat
structure, no shared package/library code between them — some duplication
across files is normal and fine).

## Environment

- Python 3.13 (`.python-version`), dependencies declared via `pyproject.toml` / `uv`.
- **The `manim` CLI is a Homebrew install** (`/opt/homebrew/bin/manim`), wrapping
  its own bundled interpreter (`/opt/homebrew/Cellar/manim/<version>/libexec/bin/python`)
  — it is **not** the repo's `.venv`. Don't assume `python3 -m manim` or the
  project venv's `python` has manim importable. For standalone debug/math
  scripts (e.g. sanity-checking geometry before wiring it into a Scene), use
  `/opt/homebrew/bin/python3` or the manim-bundled interpreter directly.
- Rendered output goes to `media/` — gitignored, never commit it.

## Rendering

```
manim -pql file.py SceneName   # fast low-quality preview (iterate with this)
manim -pqh file.py SceneName   # final high-quality render for posting
```

Most scripts have **no** `if __name__ == "__main__":` block — the CLI above
is the standard way to run them. A few newer/iterative scripts (e.g.
`conics.py`) add a bottom block using `tempconfig({"quality": "low_quality",
"preview": True})` + `.render()` so the file is one-shot executable (handy
when a user asks for a "single block executable in VS Code" script). Add one
if asked for that; it's not required repo-wide otherwise.

## Video format conventions

Two formats are used depending on what's requested — check recent files or
ask if unclear:

1. **Vertical 9:16 (Instagram Reels), full-bleed.** Set at the top of the file:
   ```python
   config.pixel_width = 1080
   config.pixel_height = 1920
   config.frame_width = 10.8      # or similar; keep frame_height/width ratio 9:16
   config.frame_height = 19.2
   ```
   See `boltzmann.py`, `cramer's rule.py`, `taylorseries2.py`.

2. **Default 16:9, content confined to the middle third.** No config override;
   instead keep all visual content within the central vertical strip of the
   default landscape frame so it can be manually cropped to vertical later.
   See `conics.py`. Use this when the user explicitly asks for "middle third"
   framing or doesn't want a hard-coded portrait config.

## The house style (title, color, text)

Nearly every script follows this branding pattern for the title — it's a
strong, consistent convention, not a one-off:

```python
title = Tex(r"$\mathbb{T}$aylor $\mathbb{S}$eries", font_size=40)
title.set_color_by_gradient(BLUE, RED)   # or BLUE, PURPLE, RED, etc.
title.to_edge(UP, buff=0.35)  # or similar small buffer
```

- First letter of each major title word wrapped in `\mathbb{...}`. Use
  `\mathbf{}` instead for a leading digit (`\mathbb{}` on numerals renders
  oddly — see `rubix.py`'s `4th Pair` step for the workaround).
- Title font size **40** unless told otherwise.
- `set_color_by_gradient(...)` on the title is common; pick colors that also
  inform the rest of the palette (e.g. if the title gradient is blue→red,
  color-code stages/curves/labels along that same gradient rather than
  picking clashing colors — ties the whole animation together).
- Minimal on-screen text. When text needs to sit over busy visual content,
  put it in a small `RoundedRectangle` with `fill_opacity` ~0.45–0.55 and
  `fill_color=BLACK` behind it, rather than relying on text alone for
  contrast.
- Prefer standard Manim color constants (`BLUE`, `RED`, `PURPLE`, `TEAL`,
  `GREY_C`, ...) over raw hex. Raw hex is fine *only* when defined as named
  constants at the top of the file for a deliberate custom palette (see
  `boltzmann.py`'s `C_BG`, `C_WALL`).
- Scene class names are PascalCase and match the topic
  (`ConicSections`, `CramersRule`, `BoltzmannDistribution`, ...).

## Common Manim pitfalls hit in this repo (avoid repeating)

- **`mobject.set_opacity(x)` sets fill *and* stroke opacity uniformly.**
  Using it to fade in/out a hollow/outline shape will make it solid-fill;
  using it on a mobject with a deliberately translucent fill (e.g. a label
  box at `fill_opacity=0.55`) will snap that back to fully opaque. Fixes:
  - For hollow shapes, animate `.set_stroke(opacity=...)` instead.
  - For composite objects with an intentional partial opacity, prefer the
    `FadeIn`/`FadeOut` animation classes over `.animate.set_opacity(...)` —
    they interpolate toward the mobject's own authored opacity rather than
    forcing it to 1.0.
- **`always_redraw` + `add_fixed_in_frame_mobjects` (ThreeDScene overlays):**
  if the generator function's returned mobject has a *changing number of
  child submobjects* between frames, the fixed-in-frame flag can silently
  break on the newly-added child, and it starts rendering in 3D world space
  instead of screen space (looks like a stray shape drifting with the
  camera). Fix: always return a **constant number of child mobjects** from
  the generator (pad with degenerate/zero-length placeholders if a branch
  has fewer real segments than usual).
- **Clip before `sqrt`.** Any time a cross-section/curve is computed from a
  formula like `sqrt(R)`, clip `R` with `np.clip(R, 0, None)` first —
  floating point noise can make a mathematically-zero R slightly negative.
- **Camera/attribute errors in `ThreeDScene`:** always use
  `self.add_fixed_in_frame_mobjects(...)` for 2D overlay UI (titles, labels,
  HUD elements) rather than adding them as regular mobjects, or they'll
  rotate/move with the camera.
- **Finite geometry vs. idealized math:** when animating something like a
  cone that's visually finite (bounded height `H`), don't let a curve's
  parametric range run unclipped — an ellipse tilting toward a parabola, or
  a hyperbola branch translating, needs to be clipped against the actual
  drawn geometry's bounds, or it'll grow/fly off unrealistically instead of
  visibly truncating the way it would on the real (finite-looking) object.
- **`Indicate` (and similar temporary-effect anims) restore the mobject's
  *original* state on finish.** So `self.play(m.animate.set_color(X),
  Indicate(m))` in a *single* play snaps the color right back — `Indicate`
  captured the pre-color at construction and restores it at the end,
  clobbering the `set_color`. Run the permanent change and the `Indicate` as
  two separate `self.play(...)` calls (change first, then indicate).
- **Mixed 2D→3D reveal in one `ThreeDScene`:** start at
  `set_camera_orientation(phi=0, theta=-90*DEGREES)` so the xy-plane renders
  face-on like a normal 2D scene (good for 1D/2D build-up), then
  `move_camera(phi≈68°, theta≈-45°)` to "lift" into 3D and reveal depth.
  `Prism(dimensions=[dx,dy,dz])` gives arbitrary rectangular boxes (needed for
  non-cubic sub-volumes); call `.set_shade_in_3d(True)` on them. A "4D"
  figure can be faked with two offset/scaled wire-cubes joined by
  `DashedLine` connectors (see `binomial.py`).

## Workflow this user likes

- **Prototype math standalone first.** Before wiring a formula into Manim
  mobjects, sanity-check it with a quick throwaway Python snippet (via
  Bash) — much faster to catch sign errors, div-by-zero, wrong roots, etc.
  than debugging inside a render.
- **Iterate visually, not just by reading code.** Render at `-ql`, then
  extract specific frames with `ffmpeg -vf "select=eq(n\,N)"` and view them
  with the Read tool, rather than describing changes without checking them.
  Sampling several frames across the timeline (a tiled contact-sheet via
  `ffmpeg ... tile=NxM`) is a fast way to sanity-check a whole animation at
  once.
- **When something looks visually wrong, find the root cause, not a patch.**
  E.g. a stray shape floating off-screen was traced back to the
  `always_redraw` child-count bug above, not just hidden or worked around.
- **Follow-up requests refine the existing file in place** — keep prior
  structure/logic intact and layer changes in surgically rather than
  rewriting from scratch, unless a rewrite is genuinely the cleanest way to
  express a new requirement.
- **Care about polish**: even spacing/buffers (don't let content touch the
  frame edges), no overlapping elements, cohesive color schemes tied to the
  title's gradient, numerically precise geometry (real derived intersection
  formulas, not hand-approximated shapes) even for purely illustrative
  content.
- **Keep it minimal-text, visual-first, and "cropped-frame safe"** when a
  request emphasizes portrait/social cropping — see the "middle third"
  convention above.

## Keeping this file current

This file (and `README.md`) should evolve as the project does. When you
learn something in a session that would help a *future* agent — a new
preference, a correction the user gave you, a convention you noticed while
reading other scripts, a gotcha you had to debug — add it here before you
finish, in the most relevant section above (or a new one if it doesn't fit).
Keep entries concrete and short; prefer editing/tightening an existing
bullet over piling on near-duplicates. If something here turns out to be
wrong or stale, fix it rather than leaving it to mislead the next session.
