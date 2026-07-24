# IDEAS.md — animation backlog + growth playbook

A living backlog of future animations **and** how to make them land. Not a rulebook —
prune what's shipped, add what you dream up. Companion to `README.md` (what this repo is)
and `CLAUDE.md` (how to build in the house style).

Every idea below is written as **hook → visual → why it pops**, because the *hook* is
what stops the scroll, not the topic.

---

## 1. The viral playbook (what makes a math reel actually pop)

These reinforce the house style already in `CLAUDE.md` (vertical 9:16, safe-zone layout,
`\mathbb{}` gradient titles, minimal text):

- **Earn the first second.** The title + first motion must imply a payoff *immediately*.
  Cold-open on the moving thing; don't spend 2s drawing axes. (We already moved to
  "title already drawn in" for exactly this reason.)
- **Promise → tension → reveal.** State a question or a "this shouldn't be possible,"
  let it build, then deliver the visual "aha." One idea per reel.
- **Make it loop / be oddly satisfying.** Motion that resolves cleanly or loops seamlessly
  gets re-watched, and re-watch time is the algorithm's #1 signal.
- **End on a clean held frame** (a finished figure or a boxed result) — that's the
  thumbnail and the "save this" moment.
- **Minimal on-screen text; put the words in the caption.** Ask a question in the caption
  ("Guess which fills first?") to farm comments.
- **Keep it short.** 8–20s outperforms 40s for this format; we've been trending shorter
  (logic gates 9.5s, apex ellipse 16s) on purpose.

---

## 2. New animation ideas — grouped by engagement archetype

Deduped against the ~65 scenes already shipped. Archetype = the reason someone shares it.

### 🌀 Oddly-satisfying / mesmerizing loops
*(highest raw virality; "I could watch this forever")*
- **Spirograph / hypotrochoids** — one dot on a rolling gear draws impossibly ornate
  loops; sweep the radius ratio so the pattern morphs. Pure hypnosis.
- **Cycloid brachistochrone race** — three balls, three ramps (straight, steep,
  cycloid); the curved one wins from behind. "Wait for it" built in.
- **Rolling circle = π** — unroll a unit circle along a line; the diameter fits π times.
  The classic "why is π there" reveal.
- **Circle / sphere packing** — circles cascade in and settle into a perfect hexagonal
  pack; count the density → π/√12. Satisfying *settle* motion.
- **Lissajous curves** — two perpendicular sine waves trace figure-8s; sweep the
  frequency ratio and watch curves bloom.
- **Double pendulum** — two identical pendulums, one-pixel different start, diverge into
  chaos. Mesmerizing + a lesson about sensitivity.
- **Chladni plates** — sand jumps into symmetric patterns as frequency climbs.
- **Phyllotaxis** — sunflower seeds placed by the golden angle; nudge the angle 0.1° and
  the spirals shatter. (Pairs with the golden-ratio pieces already done.)

### 🤯 "Wait, WHAT?" counterintuitive
*(comment-bait; people argue in the replies = engagement)*
- **0.999… = 1** — visually zoom/pack the nines until the gap vanishes. Eternal comment war.
- **Gabriel's horn** — a trumpet with *finite volume* but *infinite surface area*. "You
  can fill it with paint but never paint it."
- **Hilbert's hotel** — a fully-booked infinite hotel still fits infinitely many new guests.
- **Monty Hall** — animate 100 doors so switching *obviously* wins; kills the intuition.
- **Simpson's paradox** — two trends that both go up but combine to go down.
- **Coastline paradox / fractal dimension** — measure Britain with shrinking rulers; the
  length → ∞. Zoom into a coastline that never smooths out.
- **Buffon's needle → π** — drop thousands of needles, tally crossings, watch the estimate
  converge to π. (Great loop + payoff.)
- **Banach–Tarski (hint, not full)** — one ball → two identical balls, teased visually.

### 📐 Proof-without-words *(our core strength — extend the streak)*
- **Sum of odd numbers = n²** — odd L-shaped gnomons snap into a growing square.
- **Nicomachus** — 1³+2³+…+n³ = (1+2+…+n)². Cubes rearrange into a square.
- **Viviani's theorem** — distances from any interior point to the sides of an equilateral
  triangle always sum to the height.
- **Napoleon's theorem** — build triangles on any triangle's sides; their centers form an
  equilateral triangle. Feels like magic.
- **Pick's theorem** — area from counting lattice dots (interior + ½ boundary − 1).
- **Ptolemy's theorem** — the cyclic-quadrilateral diagonal identity, shown with rotating chords.

### 🌍 Everyday / real-world *(the "math is everywhere" angle sells to non-math folks)*
- **Curves of constant width** — a Reuleaux triangle rolls a book smoothly; "why manhole
  covers are round (and don't have to be)."
- **Why honeycombs are hexagons** — bubbles/soap film relax into the least-perimeter tiling.
- **Catenary vs parabola** — hang a chain, overlay a parabola; they're *not* the same curve.
- **Involute gears** — why gear teeth are that specific curve so they mesh without slipping.
- **GPS = trilateration** — three shrinking circles pin your location.
- **How Fourier/JPEG compresses an image** — drop high frequencies and watch the photo
  survive. (Direct sequel to `fouriermessi.py`.)

### 🔢 Scale / big-number / CS *(crossover into tech audiences)*
- **Sorting-algorithm race** — bubble vs quick vs merge on the same bars, side by side
  (this is *the* `riemann.py`-style multi-panel comparison, applied to code).
- **Maze generation + solving** — grow a maze, then flood-fill/A* to solve it.
- **Dijkstra / A\* pathfinding** — the search frontier expanding is deeply satisfying.
- **Collatz orbits** — every number's hailstone path crashing to 1.
- **Graham's number** — a sense-of-scale reel that keeps zooming out and never arrives.

### 🎡 Fourier follow-ups *(reuse the `fouriermessi.py` engine — cheap wins)*
- **Epicycles draw a signature / a logo / a country's outline** — same code, new path.
- **Square-wave build-up** — add harmonics one by one; the wobble sharpens into a square.
- **Sine unrolled from a circle** — the canonical "where sine comes from" loop.

---

## 3. Convert the classics (the easy wins)

**Recreating a proven animation beats inventing one:** the concept already went viral once,
and you have a *reference to match against* — exactly how `apexellipse.py` and
`twelvedots.py` were built this session. Faster to make, lower risk, and many already have
a home on Wikipedia (instant credibility + evergreen traffic).

> Note: the apex-ellipse & twelve-dots reference clips are watermarked
> **`1ucasvb.tumblr.com`** — Lucas V. Barbosa, whose animations are on dozens of Wikipedia
> math pages under Creative Commons. His catalog is a ready-made, battle-tested backlog.

| Classic animation | Status | Why it's a good convert |
|---|---|---|
| Sine/cosine from the unit circle | ~partly (`unitcircle2`, `sine1`) | Canonical; polish to reel + loop |
| Ellipse two-foci string trace | new | Iconic, dead simple, satisfying |
| Fourier square-wave build-up | new | Reuses `fouriermessi` math |
| Reuleaux triangle rolling | new | "Oddly satisfying" + real-world hook |
| Matrix transforms the plane (shear/rotate/scale) | new | Grid-warp is very shareable |
| Eigenvectors (the arrows that don't turn) | new | The 3Blue1Brown crowd loves it |
| Convolution "flip and slide" | new | Hard to picture → high value |
| Mandelbrot / Julia zoom | new | Infinite-detail eye candy |
| SVD = rotate → scale → rotate | new | Makes an abstract idea physical |
| Stereographic projection / Riemann sphere | new | Beautiful + mind-bending |

---

## 4. Distribution — one render, four platforms

The render is the hard part; posting it four places is nearly free. Each new piece should
fan out:

- **Instagram Reels (primary — audience).** Post consistently (2–4×/week beats one big
  drop). Hook in the first second, ask a question in the caption to farm comments, build
  **series** ("Proofs without words #7") so people follow for the next one. Starter
  hashtags: `#manim #maths #mathvisualization #oddlysatisfying #proofwithoutwords
  #mathart #3blue1brown`. Ride trending audio when it fits.
- **Wikipedia / Wikimedia Commons (evergreen + credibility).** This is the sleeper
  channel. Export the recreation as a CC-BY-SA GIF/webm and add it to the relevant math
  article — 1ucasvb's animations have sat on Wikipedia for a decade racking up passive
  views and lending real legitimacy. Manim → `--format=gif` or webm; upload under a free
  license; link the article. Huge for backlinks and "this creator is legit."
- **Reddit (discovery — can spike hard).** r/math, r/mathpics, r/manim,
  r/educationalgifs, r/oddlysatisfying, r/theydidthemath. Post as OC, explain the math in
  the top comment, engage replies, and **don't** spam-drop the IG link — let people find it.
- **YouTube Shorts + TikTok (free reach).** The exact same vertical MP4, cross-posted. Zero
  extra work.

**The flywheel:** Reddit + Wikipedia build credibility and evergreen traffic; IG + TikTok
build the following; every recreation feeds all four from a single render. Convert a
classic → post it everywhere → it earns a permanent Wikipedia home *and* a reel.

---

## 5. Next up (highest engagement × easiest to build)

Biased toward classic conversions and reuse of engines we already have:

- [ ] **Ellipse two-foci string trace** — simple, iconic, satisfying.
- [ ] **Sorting-algorithm race** — the `riemann.py` multi-panel pattern applied to code.
- [ ] **Square-wave from harmonics** — reuses `fouriermessi.py` math.
- [ ] **Reuleaux triangle rolling** — oddly-satisfying + real-world hook.
- [ ] **0.999… = 1** — guaranteed comment section.
- [ ] **Matrix transforms the plane** — grid-warp, very shareable.
- [ ] **Cycloid brachistochrone race** — "wait for it" built in.

---

## Keeping this file current

Living document, like `CLAUDE.md`. When a reel ships, check it off / delete it and note it
in `README.md`. When an idea sparks (or a reel goes unexpectedly viral and you want more of
that archetype), add it here so the backlog compounds.
