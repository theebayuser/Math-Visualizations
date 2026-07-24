import os
import numpy as np
from manim import *
from PIL import Image
from scipy.ndimage import gaussian_filter, sobel

# ----------------------------------------------------------------------
#  Drawing the 2026 Champions with 2026 circles.
#  A chain of 2026 rotating vectors (Fourier / DFT terms) whose tip traces
#  a single-stroke line-art of the map of Spain -- 2026 World Cup winners.
#  The silhouette is turned into one continuous closed path (marching-
#  squares iso-contours stitched together), Fourier-transformed, and the
#  biggest 2026 frequency terms become the epicycles.
#  (Sibling of fouriermessi.py; extraction is tuned for a clean silhouette
#  rather than a busy photo -- see _extract_loops.)
# ----------------------------------------------------------------------

# Vertical 9:16 (Instagram Reels)
config.frame_height = 14.22
config.frame_width = 8.0
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 30

IMG_PATH = os.path.join(os.path.dirname(__file__), "spain.png")
N_SAMPLES = 6000       # points along the stitched path
N_CIRCLES = 2026       # rotating terms (title-mandated)
N_VISIBLE = 220        # how many circles are actually drawn (rest are sub-pixel)

C_PEN = "#FFC93C"      # gold traced line (España yellow)
C_CIRCLE_A = RED       # gradient ends for the epicycle circles (Spain flag)
C_CIRCLE_B = GOLD

TITLE_Y = 4.7
FIG_Y = -0.4           # centre of the drawing
TARGET_H = 9.0         # max drawing height in manim units
TARGET_W = 6.9         # max drawing width  in manim units (Spain is wider than tall)


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


def _otsu(gray):
    """Otsu threshold (numpy only -- no cv2/skimage)."""
    hist, _ = np.histogram(gray, bins=256, range=(0, 255))
    total = gray.size
    sumall = np.dot(np.arange(256), hist)
    sumB = wB = 0.0
    best_t, best_var = 127, -1.0
    for t in range(256):
        wB += hist[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sumB += t * hist[t]
        mB = sumB / wB
        mF = (sumall - sumB) / wF
        var = wB * wF * (mB - mF) ** 2
        if var > best_var:
            best_var, best_t = var, t
    return best_t


# crop (as fractions of the source w/h) keeping mainland + Balearic Islands,
# dropping the Canary Islands (bottom-left) and the "Vemaps" watermark (bottom-right)
CROP = (0.40, 0.00, 0.93, 0.60)   # (left, top, right, bottom)
KEEP_BALEARICS = False             # False -> mainland only (cleanest single loop)


def _extract_loops():
    """Silhouette-friendly: threshold to a clean shape mask, then contour it.
    Works whether the source is a filled country shape or an outline drawing."""
    # composite onto white first, so palette/transparent PNGs threshold cleanly
    src = Image.open(IMG_PATH).convert("RGBA")
    bg = Image.new("RGBA", src.size, (255, 255, 255, 255))
    im = Image.alpha_composite(bg, src).convert("L")
    W0, H0 = im.size
    l, t, r, b = CROP
    im = im.crop((int(l * W0), int(t * H0), int(r * W0), int(b * H0)))
    w = 320
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    g = np.asarray(im, dtype=float)
    sm = gaussian_filter(g, sigma=1.2)

    thr = _otsu(sm)
    # mask = 1 where the shape is; pick whichever polarity is the minority
    # (the country), so it works for dark-on-light and light-on-dark sources
    mask = (sm < thr).astype(float)
    if mask.mean() > 0.5:
        mask = 1.0 - mask
    mask = gaussian_filter(mask, sigma=1.0)

    loops = _iso_contours(mask, 0.5)
    loops = [p for p in loops if _plen(p) > 15 and len(p) > 8]
    if not loops:   # fallback: edge magnitude if the threshold gave nothing
        edge = np.hypot(sobel(sm, axis=1), sobel(sm, axis=0))
        edge = gaussian_filter(edge / edge.max() * 255.0, sigma=1.0)
        loops = [p for p in _iso_contours(edge, 60) if _plen(p) > 15 and len(p) > 8]
    if not KEEP_BALEARICS:
        # mainland only -> one perfectly clean closed loop, no island travel lines
        loops = [max(loops, key=_plen)]
    return loops


def _roll_closed(loop, target):
    """Reindex a closed loop to start at its vertex nearest `target`, and append
    that start again at the end so it's traversed as a full closed circuit that
    returns to where it was entered -- keeps island hops to short there-and-back
    stubs instead of long slashes across the map."""
    i = int(np.argmin(np.hypot(loop[:, 0] - target[0], loop[:, 1] - target[1])))
    rolled = np.concatenate([loop[i:], loop[:i], loop[i:i + 1]], axis=0)
    return rolled


def _stitch(loops):
    loops = sorted(loops, key=lambda p: -_plen(p))
    # start the mainland circuit near the other pieces, so it ends close to them
    rest_centroid = (np.concatenate(loops[1:], axis=0).mean(axis=0)
                     if len(loops) > 1 else loops[0].mean(axis=0))
    path = [_roll_closed(loops[0], rest_centroid)]
    end = path[0][-1]
    remaining = list(loops[1:])
    while remaining:
        # nearest loop by closest vertex to the current pen position
        best_i, best_d = 0, 1e18
        for i, lp in enumerate(remaining):
            d = np.min(np.hypot(lp[:, 0] - end[0], lp[:, 1] - end[1]))
            if d < best_d:
                best_i, best_d = i, d
        seg = _roll_closed(remaining.pop(best_i), end)
        path.append(seg)
        end = seg[-1]
    return np.concatenate(path, axis=0)


def _resample(path, n):
    d = np.diff(path, axis=0)
    s = np.concatenate([[0], np.cumsum(np.hypot(d[:, 0], d[:, 1]))])
    targ = np.linspace(0, s[-1], n, endpoint=False)
    return np.stack([np.interp(targ, s, path[:, 0]),
                     np.interp(targ, s, path[:, 1])], axis=1)


def build_epicycles():
    """Return (C, F, base_xy, S): complex amplitudes, integer freqs (sorted by
    |C| desc, DC removed), path-centre in image px, and px->manim scale (fit to
    both TARGET_W and TARGET_H)."""
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
    S = min(TARGET_W / (xmax - xmin), TARGET_H / (ymax - ymin))
    return C, F, base_xy, S


def _to_manim(img_pts, base_xy, S):
    """Map image-space complex points -> manim [x, y, 0] rows (y flipped)."""
    x = (img_pts.real - base_xy[0]) * S
    y = -(img_pts.imag - base_xy[1]) * S + FIG_Y
    return np.stack([x, y, np.zeros_like(x)], axis=1)


class FourierSpain(Scene):
    def construct(self):
        title = Tex(r"$\mathbb{D}$rawing the $2026$ $\mathbb{C}$hampions\\"
                    r"with $2026$ $\mathbb{C}$ircles", font_size=44)
        title.set_color_by_gradient(RED, GOLD, RED)
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
            Circle(radius=max(r, 1e-3), stroke_color=grad[i], stroke_width=2.6,
                   stroke_opacity=0.95, fill_opacity=0)
            for i, r in enumerate(radii)
        ])
        arms = VMobject(stroke_color=WHITE, stroke_width=2.2, stroke_opacity=0.85)
        tip = Dot(radius=0.075, color=C_PEN)

        def update_chain(_):
            m = _to_manim(partial_sums(t_tracker.get_value()), base_xy, S)
            for i, circ in enumerate(circles):
                circ.move_to(m[i])
            arms.set_points_as_corners(m[:N_VISIBLE + 1])
            tip.move_to(m[-1])

        # the gold drawing, revealed up to the current time (full detail)
        drawn = always_redraw(lambda: VMobject(
            stroke_color=C_PEN, stroke_width=3.4).set_points_as_corners(
                full_pts[:max(2, int(t_tracker.get_value() * (M - 1)) + 1)]))

        update_chain(None)
        chain = VGroup(arms, circles)
        chain.add_updater(update_chain)
        self.add(drawn, chain, tip)

        # ---- the Spanish flag (red / gualda-yellow / red bands) clipped to the
        # full Spain silhouette, for a mid-way flash tease ----
        FLAG_RED, FLAG_YEL = "#AA151B", "#F1BF00"
        sil_pts = full_pts[::8]
        sil = Polygon(*sil_pts, stroke_width=0)
        xs, ys = sil_pts[:, 0], sil_pts[:, 1]
        xmin, xmax, ymin, ymax = xs.min(), xs.max(), ys.min(), ys.max()
        h, cx = ymax - ymin, (xmin + xmax) / 2

        def band(y0, y1, color):
            r = Rectangle(width=(xmax - xmin) + 0.4, height=(y1 - y0) + 0.02)
            r.move_to([cx, (y0 + y1) / 2, 0])
            return Intersection(sil, r, color=color, fill_color=color,
                                fill_opacity=1, stroke_width=0)

        flag = VGroup(
            band(ymin, ymin + 0.25 * h, FLAG_RED),
            band(ymin + 0.25 * h, ymin + 0.75 * h, FLAG_YEL),
            band(ymin + 0.75 * h, ymax, FLAG_RED),
        ).set_z_index(-1)

        # draw continuously (never pausing) at a constant rate; at the halfway
        # mark the flag fills in and STAYS behind the outline to the end.
        # segment run_times keep t moving at one steady 0.125 units/s so the
        # three back-to-back plays read as a single uninterrupted trace.
        self.play(t_tracker.animate.set_value(0.5), run_time=4.0, rate_func=linear)
        self.play(t_tracker.animate.set_value(0.6875), FadeIn(flag),
                  run_time=1.5, rate_func=linear)
        self.play(t_tracker.animate.set_value(1.0), run_time=2.5, rate_func=linear)
        chain.clear_updaters()

        # fade the machinery, leave the flag-filled Spain with its gold outline
        self.play(FadeOut(chain), FadeOut(tip), run_time=0.6)
        self.wait(1.2)


if __name__ == "__main__":
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "preview": True}):
        FourierSpain().render()
