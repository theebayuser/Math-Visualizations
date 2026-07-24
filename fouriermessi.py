import os
import numpy as np
from manim import *
from PIL import Image
from scipy.ndimage import gaussian_filter, sobel

# ----------------------------------------------------------------------
#  Drawing Messi with 2026 circles.
#  A chain of 2026 rotating vectors (Fourier / DFT terms) whose tip traces
#  a single-stroke line-art of the Messi portrait.  The image is turned
#  into one continuous closed path (marching-squares iso-contours stitched
#  together), Fourier-transformed, and the biggest 2026 frequency terms
#  become the epicycles.
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080

IMG_PATH = os.path.join(os.path.dirname(__file__), "messi.jpg")
N_SAMPLES = 6000       # points along the stitched path
N_CIRCLES = 2026       # rotating terms (title-mandated)
N_VISIBLE = 220        # how many circles are actually drawn (rest are sub-pixel)

C_PEN = "#FFC93C"      # gold traced line
C_CIRCLE_A = BLUE      # gradient ends for the epicycle circles
C_CIRCLE_B = RED

TITLE_Y = 4.75
FIG_Y = -0.55          # vertical centre of the drawing
TARGET_H = 7.3         # drawing height in manim units


# =============================================================== extraction
def _iso_contours(field, level):
    """Marching squares: closed/open polylines at `level` of a scalar field.
    Coordinates are (x=col, y=row)."""
    H, W = field.shape
    segs = []

    def interp(p1, p2, v1, v2):
        t = 0.5 if v1 == v2 else (level - v1) / (v2 - v1)
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))

    f = field
    table = {
        1: [(3, 0)], 2: [(0, 1)], 3: [(3, 1)], 4: [(1, 2)],
        5: [(3, 2), (0, 1)], 6: [(0, 2)], 7: [(3, 2)], 8: [(2, 3)],
        9: [(2, 0)], 10: [(0, 3), (1, 2)], 11: [(1, 2)], 12: [(1, 3)],
        13: [(1, 0)], 14: [(0, 3)],
    }
    for r in range(H - 1):
        for c in range(W - 1):
            tl, tr = f[r, c], f[r, c + 1]
            br, bl = f[r + 1, c + 1], f[r + 1, c]
            idx = (int(tl > level) | (int(tr > level) << 1)
                   | (int(br > level) << 2) | (int(bl > level) << 3))
            if idx in (0, 15):
                continue
            edges = [
                interp((c, r), (c + 1, r), tl, tr),          # 0 top
                interp((c + 1, r), (c + 1, r + 1), tr, br),  # 1 right
                interp((c, r + 1), (c + 1, r + 1), bl, br),  # 2 bottom
                interp((c, r), (c, r + 1), tl, bl),          # 3 left
            ]
            for a, b in table.get(idx, []):
                segs.append((edges[a], edges[b]))
    return _chain_segments(segs)


def _chain_segments(segs):
    from collections import defaultdict
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    pointmap, edges = {}, defaultdict(set)
    for a, b in segs:
        ka, kb = key(a), key(b)
        pointmap[ka], pointmap[kb] = a, b
        edges[ka].add(kb)
        edges[kb].add(ka)
    seen = set()
    polylines = []
    for a, b in segs:
        ka, kb = key(a), key(b)
        if tuple(sorted([ka, kb])) in seen:
            continue
        line, cur = [pointmap[ka]], ka
        while True:
            nxts = [w for w in edges[cur] if tuple(sorted([cur, w])) not in seen]
            if not nxts:
                break
            w = nxts[0]
            seen.add(tuple(sorted([cur, w])))
            line.append(pointmap[w])
            cur = w
        polylines.append(np.array(line, dtype=float))
    return polylines


def _plen(p):
    if len(p) < 2:
        return 0.0
    d = np.diff(p, axis=0)
    return float(np.sum(np.hypot(d[:, 0], d[:, 1])))


def _extract_loops():
    im = Image.open(IMG_PATH).convert("L")
    w = 250
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    g = np.asarray(im, dtype=float)
    sm = gaussian_filter(g, sigma=1.6)
    edge = np.hypot(sobel(sm, axis=1), sobel(sm, axis=0))
    edge = gaussian_filter(edge / edge.max() * 255.0, sigma=1.0)

    loops = []
    for lvl in (55, 90):
        loops += _iso_contours(edge, lvl)
    for lvl in (70, 120, 175):
        loops += _iso_contours(sm, lvl)
    return [p for p in loops if _plen(p) > 12 and len(p) > 6]


def _stitch(loops):
    loops = sorted(loops, key=lambda p: -len(p))
    used = [False] * len(loops)
    used[0] = True
    path = [loops[0]]
    end = loops[0][-1]
    for _ in range(len(loops) - 1):
        best, bd, rev = -1, 1e18, False
        for i, lp in enumerate(loops):
            if used[i]:
                continue
            d0 = np.hypot(*(lp[0] - end))
            d1 = np.hypot(*(lp[-1] - end))
            if d0 < bd:
                best, bd, rev = i, d0, False
            if d1 < bd:
                best, bd, rev = i, d1, True
        seg = loops[best][::-1] if rev else loops[best]
        path.append(seg)
        used[best] = True
        end = seg[-1]
    return np.concatenate(path, axis=0)


def _resample(path, n):
    d = np.diff(path, axis=0)
    s = np.concatenate([[0], np.cumsum(np.hypot(d[:, 0], d[:, 1]))])
    targ = np.linspace(0, s[-1], n, endpoint=False)
    return np.stack([np.interp(targ, s, path[:, 0]),
                     np.interp(targ, s, path[:, 1])], axis=1)


def build_epicycles():
    """Return (C, F, base_xy, S) : complex amplitudes, integer freqs (sorted by
    |C| desc, DC removed), the path-centre in image px, and the px->manim
    scale.  Only the biggest N_CIRCLES terms are kept."""
    path = _resample(_stitch(_extract_loops()), N_SAMPLES)
    z = path[:, 0] + 1j * path[:, 1]
    N = len(z)
    coeff = np.fft.fft(z) / N
    freq = np.fft.fftfreq(N, d=1.0 / N).astype(int)

    nz = freq != 0                       # DC becomes the fixed figure centre
    coeff, freq = coeff[nz], freq[nz]
    order = np.argsort(-np.abs(coeff))[:N_CIRCLES]
    C, F = coeff[order], freq[order]

    xmin, ymin = path.min(axis=0)
    xmax, ymax = path.max(axis=0)
    base_xy = np.array([(xmin + xmax) / 2, (ymin + ymax) / 2])
    S = TARGET_H / (ymax - ymin)
    return C, F, base_xy, S


def _to_manim(img_pts, base_xy, S):
    """Map image-space complex points -> manim [x, y, 0] rows (y flipped)."""
    x = (img_pts.real - base_xy[0]) * S
    y = -(img_pts.imag - base_xy[1]) * S + FIG_Y
    return np.stack([x, y, np.zeros_like(x)], axis=1)


class FourierMessi(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{D}$rawing $\mathbb{M}$essi\\with $2026$ $\mathbb{C}$ircles",
                    font_size=46)
        title.set_color_by_gradient(BLUE, RED)
        title.move_to(UP * TITLE_Y)
        self.add(title)

        C, F, base_xy, S = build_epicycles()
        base_c = base_xy[0] + 1j * base_xy[1]

        def partial_sums(t):
            """Image-space running tip positions [base, +term0, +term1, ...]."""
            v = C * np.exp(2j * np.pi * F * t)
            pts = np.empty(len(C) + 1, dtype=complex)
            pts[0] = base_c
            pts[1:] = base_c + np.cumsum(v)
            return pts

        # high-res reconstruction of the whole curve (the pen's true path, at far
        # more points than the frame rate -- so the drawn line keeps its detail
        # instead of being a low-poly TracedPath sampled once per frame)
        M = 5000
        ts = np.linspace(0.0, 1.0, M)
        tip_img = base_c + (C[None, :] * np.exp(2j * np.pi * np.outer(ts, F))).sum(axis=1)
        full_pts = _to_manim(tip_img, base_xy, S)

        t_tracker = ValueTracker(0.0)
        radii = np.abs(C[:N_VISIBLE]) * S
        grad = color_gradient([C_CIRCLE_A, C_CIRCLE_B], N_VISIBLE)

        circles = VGroup(*[
            Circle(radius=max(r, 1e-3), stroke_color=grad[i], stroke_width=1.4,
                   stroke_opacity=0.55, fill_opacity=0)
            for i, r in enumerate(radii)
        ])
        arms = VMobject(stroke_color=GREY_B, stroke_width=1.2, stroke_opacity=0.5)
        tip = Dot(radius=0.05, color=C_PEN)

        def update_chain(_):
            m = _to_manim(partial_sums(t_tracker.get_value()), base_xy, S)
            for i, circ in enumerate(circles):
                circ.move_to(m[i])
            arms.set_points_as_corners(m[:N_VISIBLE + 1])
            tip.move_to(m[-1])

        # the gold drawing, revealed up to the current time (full detail)
        drawn = always_redraw(lambda: VMobject(
            stroke_color=C_PEN, stroke_width=2.6).set_points_as_corners(
                full_pts[:max(2, int(t_tracker.get_value() * (M - 1)) + 1)]))

        update_chain(None)
        chain = VGroup(arms, circles)
        chain.add_updater(update_chain)
        self.add(drawn, chain, tip)

        # draw!  t : 0 -> 1 winds every epicycle exactly F[k] times.
        self.play(t_tracker.animate.set_value(1.0), run_time=17, rate_func=linear)
        chain.clear_updaters()

        # leave the finished gold drawing on its own
        self.play(FadeOut(chain), FadeOut(tip), run_time=1.2)
        self.wait(1.6)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        FourierMessi().render()
