"""Full-screen animations: static, fades, rain, flashlight, heartbeat,
jump scares, the scrolling train, the split-flap board, the livestream and
the title screen. Every function owns the whole screen while it runs and
leaves it cleared (or holding its last frame) when it returns."""
import math
import random
import textwrap

from .term import T, fg, bg, RESET, BOLD, vlen
from . import art, lettering

NOISE = " ░░▒▒▓"
GRAY = list(range(232, 256))
REDS = [52, 88, 124, 160, 196]


# ------------------------------------------------------------------ helpers
def center(lines, dy=0):
    cols, rows = T.size()
    h = len(lines)
    w = max((len(l) for l in lines), default=0)
    r = max(1, (rows - h) // 2 + 1 + dy)
    c = max(1, (cols - w) // 2 + 1)
    return r, c


def blit(lines, r, c, color=""):
    cols, rows = T.size()
    buf = []
    for i, l in enumerate(lines):
        rr = r + i
        if 1 <= rr <= rows:
            buf.append("\x1b[%d;%dH%s%s" % (rr, max(1, c), color, l[: max(0, cols - c)]))
    buf.append(RESET)
    T.write("".join(buf))


def ctext(r, text, color=""):
    cols, _ = T.size()
    T.at(r, max(1, (cols - vlen(text)) // 2 + 1), color + text + RESET)


def skip_pressed():
    return T.poll() is not None


def hold(seconds, skippable=True):
    """Sleep, but let any key cut it short. Returns True if skipped."""
    end = T.now() + seconds
    while T.now() < end:
        if skippable and T.key(min(0.05, max(0.001, end - T.now()))) is not None:
            return True
        if not skippable:
            T.sleep(min(0.05, end - T.now()))
    return False


def fill_screen(color_bg):
    cols, rows = T.size()
    line = bg(color_bg) + " " * (cols - 1)
    T.write("".join("\x1b[%d;1H%s" % (r, line) for r in range(1, rows + 1)) + RESET)


# ------------------------------------------------------------------- static
def static(duration=0.5, fps=24, heavy=1.0):
    cols, rows = T.size()
    end = T.now() + duration
    while T.now() < end:
        buf = []
        for r in range(1, rows + 1):
            col = 0
            row = []
            while col < cols - 1:
                run = min(random.randint(3, 16), cols - 1 - col)
                row.append(fg(random.choice((234, 236, 238, 240, 243, 247))))
                if random.random() < heavy:
                    row.append("".join(random.choice(NOISE) for _ in range(run)))
                else:
                    row.append(" " * run)
                col += run
            buf.append("\x1b[%d;1H" % r + "".join(row))
        T.write("".join(buf) + RESET)
        T.sleep(1.0 / fps)
    T.clear()
    T.flush()


# -------------------------------------------------------------------- fades
def fade(lines, r=None, c=None, ramp=None, step=0.03, out=False):
    if r is None:
        r, c = center(lines)
    ramp = ramp or GRAY[::2]
    seq = list(reversed(ramp)) if out else ramp
    for lvl in seq:
        blit(lines, r, c, fg(lvl))
        T.sleep(step)
    if out:
        blit([" " * len(l) for l in lines], r, c)


def typeline(r, text, color, cps=30, c=None):
    cols, _ = T.size()
    if c is None:
        c = max(1, (cols - len(text)) // 2 + 1)
    T.at(r, c, color)
    for ch in text:
        T.write(ch)
        T.sleep(1.0 / cps if ch != " " else 0.5 / cps)
    T.write(RESET)


def chapter_card(numeral, kicker, title):
    static(0.35)
    T.clear()
    big = lettering.NUMERALS[numeral]
    cols, rows = T.size()
    h = len(big) + 5
    r0 = max(1, (rows - h) // 2)
    ctext(r0, kicker, fg(240))
    w = max(len(l) for l in big)
    c0 = max(1, (cols - w) // 2 + 1)
    fade(big, r0 + 2, c0, ramp=[52, 88, 88, 124, 124, 160], step=0.06)
    spaced = "   ".join(" ".join(word) for word in title.split(" "))
    typeline(r0 + 3 + len(big), spaced, fg(252), cps=26)
    T.flush_input()
    hold(1.8)
    fade(big, r0 + 2, c0, ramp=[52, 88, 124, 160], step=0.05, out=True)
    T.clear()
    T.sleep(0.25)


def title_card(lines, sub=None, hold_s=2.2):
    """A centred block of plain lines that fades in and out (endings, etc)."""
    T.clear()
    r, c = center(lines, -1)
    fade(lines, r, c, ramp=REDS, step=0.07)
    if sub:
        typeline(r + len(lines) + 2, sub, fg(250), cps=30)
    T.flush_input()
    hold(hold_s)
    T.clear()


# ------------------------------------------------------------ flicker/shake
def flicker(lines, duration=1.5, bright=252, dark=236):
    r, c = center(lines)
    end = T.now() + duration
    while T.now() < end:
        on = random.random() < 0.6
        blit(lines, r, c, fg(bright if on else dark))
        T.sleep(random.uniform(0.03, 0.18))
    blit(lines, r, c, fg(bright))
    T.flush()


def shake(lines, duration=0.8, amp=3, color=None):
    color = color or fg(196)
    r, c = center(lines)
    w = max(len(l) for l in lines)
    blank = [" " * (w + 2 * amp + 2)] * (len(lines) + 2)
    end = T.now() + duration
    while T.now() < end:
        blit(blank, r - 1, c - amp - 1)
        blit(lines, r + random.randint(-1, 1), c + random.randint(-amp, amp), color)
        T.sleep(0.04)
    blit(blank, r - 1, c - amp - 1)
    blit(lines, r, c, color)
    T.flush()


def vignette(color=124, pulses=2):
    """Red flash at the screen edges (non-destructive: text is left alone)."""
    cols, rows = T.size()
    for _ in range(pulses):
        buf = []
        for r in range(3, rows + 1):
            buf.append("\x1b[%d;1H%s██" % (r, fg(color)))
            buf.append("\x1b[%d;%dH██" % (r, cols - 2))
        T.write("".join(buf) + RESET)
        T.sleep(0.09)
        buf = []
        for r in range(3, rows + 1):
            buf.append("\x1b[%d;1H  \x1b[%d;%dH  " % (r, r, cols - 2))
        T.write("".join(buf))
        T.sleep(0.07)
    T.flush()


# ---------------------------------------------------------------- jumpscare
def jumpscare(face=None, text=None):
    face = face or art.FACE
    cols, rows = T.size()
    r, c = center(face, -1)
    T.ding()
    frames = 1 if T.reduce_flash else 7
    for i in range(frames):
        inv = (i % 2 == 0) and not T.reduce_flash
        fill_screen(124 if inv else 16)
        dr = 0 if T.reduce_flash else random.randint(-1, 1)
        dc = 0 if T.reduce_flash else random.randint(-4, 4)
        col = (bg(124) + fg(16)) if inv else (bg(16) + fg(196))
        blit(face, r + dr, c + dc, col)
        if text:
            ctext(r + len(face) + 1 + dr, text, col + BOLD)
        T.sleep(0.06 if not T.reduce_flash else 0.4)
    fill_screen(16)
    blit(face, r, c, fg(160))
    if text:
        ctext(r + len(face) + 1, text, fg(196) + BOLD)
    T.sleep(0.9)
    static(0.25)
    T.clear()
    T.sleep(0.5)
    T.flush_input()


# --------------------------------------------------------------- heartbeat
def _ecg(p):
    if 0.08 < p < 0.18:
        return 2 + 3 * math.sin((p - 0.08) / 0.10 * math.pi)
    if 0.28 <= p < 0.31:
        return 1
    if 0.31 <= p < 0.36:
        return 23
    if 0.36 <= p < 0.39:
        return 0
    if 0.52 < p < 0.70:
        return 2 + 5 * math.sin((p - 0.52) / 0.18 * math.pi)
    return 2


def heartbeat(duration=4.0, bpm_from=70, bpm_to=140, caption=None, fps=30):
    cols, rows = T.size()
    T.clear()
    W = min(70, cols - 6)
    c0 = max(1, (cols - W) // 2 + 1)
    r_heart = max(2, rows // 2 - 5)
    r_ecg = r_heart + 7
    if caption:
        typeline(max(1, r_heart - 3), caption, fg(250), cps=40)
    vals = [2.0] * W
    phase = 0.0
    t0 = T.now()
    last = t0
    beat_t = -1.0
    samples_per_sec = 70.0
    acc = 0.0
    blocks = " ▁▂▃▄▅▆▇█"
    hw = max(len(l) for l in art.HEART_BIG)
    while True:
        now = T.now()
        t = now - t0
        if t >= duration or skip_pressed():
            break
        dt = now - last
        last = now
        bpm = bpm_from + (bpm_to - bpm_from) * min(1.0, t / duration)
        acc += dt * samples_per_sec
        n = int(acc)
        acc -= n
        for _ in range(n):
            prev = phase
            phase += (bpm / 60.0) / samples_per_sec
            if phase >= 1.0:
                phase -= 1.0
            if prev < 0.33 <= phase:
                beat_t = t
            vals.append(_ecg(phase))
        vals = vals[-W:]
        big = (t - beat_t) < 0.16
        heart = art.HEART_BIG if big else art.HEART_SMALL
        buf = []
        for i in range(5):
            buf.append("\x1b[%d;%dH%s" % (r_heart + i, max(1, (cols - hw) // 2 + 1), " " * (hw + 2)))
        hc = max(1, (cols - max(len(l) for l in heart)) // 2 + 1)
        for i, l in enumerate(heart):
            buf.append("\x1b[%d;%dH%s%s" % (r_heart + i + (1 if not big else 0), hc, fg(196 if big else 124), l))
        for k, rr in enumerate((r_ecg, r_ecg + 1, r_ecg + 2)):
            lvl_base = (2 - k) * 8
            line = []
            for v in vals:
                lv = int(max(0, min(8, v - lvl_base)))
                line.append(blocks[lv])
            buf.append("\x1b[%d;%dH%s%s" % (rr, c0, fg(160), "".join(line)))
        buf.append("\x1b[%d;%dH%s%3d BPM" % (r_ecg + 4, c0 + W - 7, fg(240), bpm))
        T.write("".join(buf) + RESET)
        T.sleep(1.0 / fps)
    T.clear()
    T.flush()


# ------------------------------------------------------------------ whispers
def whispers(words, duration=2.5, center_text=None):
    cols, rows = T.size()
    T.clear()
    if center_text:
        ctext(rows // 2, center_text, fg(252))
    live = []
    end = T.now() + duration
    while T.now() < end:
        if skip_pressed():
            break
        now = T.now()
        if random.random() < 0.35:
            w = random.choice(words)
            r = random.randint(2, rows - 1)
            if center_text and abs(r - rows // 2) < 2:
                continue
            c = random.randint(2, max(2, cols - len(w) - 2))
            col = random.choice((52, 88, 89, 96, 238, 240))
            T.at(r, c, fg(col) + w + RESET)
            live.append((now + random.uniform(0.5, 1.4), r, c, len(w)))
        keep = []
        for item in live:
            if item[0] <= now:
                T.at(item[1], item[2], " " * item[3])
            else:
                keep.append(item)
        live = keep
        T.sleep(0.06)
    T.clear()
    T.flush()


# ---------------------------------------------------------------------- rain
def rain_scene(scene, duration=4.0, caption=None, fps=20):
    cols, rows = T.size()
    W = cols - 1
    sh = len(scene)
    sw = max(len(l) for l in scene)
    r0 = max(2, rows - sh - 1)
    c0 = max(0, (W - sw) // 2)
    grid = [[" "] * W for _ in range(rows)]
    for i, l in enumerate(scene):
        for j, ch in enumerate(l):
            rr, cc = r0 - 1 + i, c0 + j
            if 0 <= rr < rows and 0 <= cc < W:
                grid[rr][cc] = ch
    drops = [[random.randrange(W), random.uniform(-rows, rows), random.uniform(22, 38)]
             for _ in range(max(20, int(W * 0.55)))]
    T.clear()
    t0 = T.now()
    last = t0
    cap_done = False
    flash_left = 0
    while True:
        now = T.now()
        if now - t0 >= duration or skip_pressed():
            break
        dt = min(0.2, now - last)
        last = now
        if flash_left <= 0 and not T.reduce_flash and random.random() < 0.02:
            flash_left = 3
        art_col = fg(255) if flash_left > 0 else fg(239)
        flash_left -= 1
        rainmask = set()
        for d in drops:
            d[1] += d[2] * dt
            if d[1] >= rows:
                d[0] = random.randrange(W)
                d[1] = random.uniform(-6, 0)
            y = int(d[1])
            for yy in (y, y - 1):
                if 0 <= yy < rows and grid[yy][d[0]] == " ":
                    rainmask.add((yy, d[0]))
        buf = []
        for r in range(rows):
            row = grid[r]
            parts = []
            mode = None
            for cidx in range(W):
                is_rain = (r, cidx) in rainmask
                m = 1 if is_rain else 0
                if m != mode:
                    parts.append(fg(67) if m else art_col)
                    mode = m
                parts.append("╎" if is_rain else row[cidx])
            buf.append("\x1b[%d;1H%s" % (r + 1, "".join(parts)))
        T.write("".join(buf) + RESET)
        if caption and not cap_done and now - t0 > 0.6:
            cap_done = True
        if caption and cap_done:
            T.at(2, 3, fg(250) + caption + RESET)
        T.sleep(1.0 / fps)
    T.clear()
    T.flush()


# ---------------------------------------------------------------- flashlight
def flashlight(scene, duration=3.0, eyes=None, fps=24):
    cols, rows = T.size()
    sh = len(scene)
    sw = max(len(l) for l in scene)
    r0, c0 = center(scene)
    R = max(7.0, sw / 6.5)
    eyes = eyes or []
    T.clear()
    t0 = T.now()
    while True:
        t = T.now() - t0
        if t >= duration or skip_pressed():
            break
        p = t / duration
        bx = -R + p * (sw + 2 * R)
        by = sh / 2.0 + math.sin(p * math.pi * 3) * sh / 4.0
        buf = []
        for i, l in enumerate(scene):
            parts = []
            mode = None
            for j, ch in enumerate(l):
                d = math.hypot((j - bx) / 2.0, i - by)
                if (i, j) in eyes and d > R * 1.15:
                    m, out = 9, "●"
                elif ch == " ":
                    m, out = 0, " "
                elif d < R * 0.55:
                    m, out = 1, ch
                elif d < R:
                    m, out = 2, ch
                elif d < R + 1.6:
                    m, out = 3, ch
                else:
                    m, out = 0, " "
                if m != mode:
                    parts.append({0: "", 1: fg(230), 2: fg(186), 3: fg(239), 9: fg(160)}[m])
                    mode = m
                parts.append(out)
            buf.append("\x1b[%d;%dH%s" % (r0 + i, c0, "".join(parts)))
        T.write("".join(buf) + RESET)
        T.sleep(1.0 / fps)
    blit(scene, r0, c0, fg(238))
    for (i, j) in eyes:
        T.at(r0 + i, c0 + j, fg(124) + "●" + RESET)
    T.flush()
    T.sleep(0.6)
    for (i, j) in eyes:
        T.at(r0 + i, c0 + j, fg(238) + scene[i][j] + RESET)
    T.sleep(0.5)


def show_art(lines, color=250, caption=None, flick=True):
    T.clear()
    if flick:
        flicker(lines, 0.7, bright=color)
    r, c = center(lines, -1)
    blit(lines, r, c, fg(color))
    if caption:
        ctext(r + len(lines) + 2, caption, fg(245))
    T.flush()


# --------------------------------------------------------------------- train
def _train_grid(coaches):
    """Build a list of rows; each row is a list of (char, colour)."""
    parts = []
    eng = art.ENGINE
    parts.append([[(ch, _engine_col(ch)) for ch in row] for row in eng])
    for label in coaches:
        rows = []
        dark = label == ""
        for row in art.COACH:
            if "LBL" in row:
                row = row.replace("LBL", (label or "   ").center(3))
            line = []
            for ch in row:
                if ch == "#":
                    line.append(("▒" if dark else "█", 234 if dark else 214))
                elif ch in "S0123456789" and not dark:
                    line.append((ch, 231))
                elif ch in "(O)":
                    line.append((ch, 240))
                elif ch == "=":
                    line.append((ch, 244))
                else:
                    line.append((ch, 236 if dark else 31))
            rows.append(line)
        parts.append(rows)
    h = max(len(p) for p in parts)
    grid = [[] for _ in range(h)]
    for p in parts:
        w = max(len(r) for r in p)
        for i in range(h):
            row = p[i] if i < len(p) else []
            grid[i].extend(row + [(" ", 0)] * (w - len(row)))
    return grid


def _engine_col(ch):
    if ch in "@":
        return 229
    if ch in "(O)":
        return 240
    if ch in "0123456789:":
        return 214
    if ch == "=":
        return 244
    return 130


def train_pass(coaches, speed=30.0, caption=None):
    cols, rows = T.size()
    W = cols - 1
    grid = _train_grid(coaches)
    h = len(grid)
    tw = len(grid[0])
    r0 = max(4, (rows - h) // 2)
    T.clear()
    if caption:
        ctext(2, caption, fg(245))
    rail = fg(240) + ("═" * W)
    sleepers = fg(237) + ("┴──" * (W // 3 + 1))[:W]
    T.at(r0 + h, 1, rail)
    T.at(r0 + h + 1, 1, sleepers + RESET)
    total = W + tw
    t0 = T.now()
    while True:
        t = T.now() - t0
        x = int(W - t * speed)   # screen column of the train's first char
        if x < -tw:
            break
        buf = []
        for i in range(h):
            row = grid[i]
            parts = []
            mode = None
            for sc in range(W):
                k = sc - x
                if 0 <= k < tw:
                    ch, col = row[k]
                    if col == 214 and random.random() < 0.004:
                        col = 94
                else:
                    ch, col = " ", 0
                if col != mode:
                    parts.append(fg(col) if col else "")
                    mode = col
                parts.append(ch)
            buf.append("\x1b[%d;1H%s" % (r0 + i, "".join(parts)))
        T.write("".join(buf) + RESET)
        T.sleep(1.0 / 24)
    T.clear()
    T.flush()


# ----------------------------------------------------------------- split flap
FLAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:·"


def split_flap(lines, header="DEPARTURES", clock="03:17"):
    cols, rows = T.size()
    w = max(len(l) for l in lines) + 4
    w = max(w, 40)
    lines = [l.ljust(w - 4) for l in lines]
    r0 = max(2, (rows - len(lines) - 5) // 2)
    c0 = max(1, (cols - w - 2) // 2 + 1)
    frame = bg(233)
    T.clear()
    top = "╔" + "═" * w + "╗"
    T.at(r0, c0, fg(240) + top)
    hdr = "  " + header + clock.rjust(w - len(header) - 4) + "  "
    T.at(r0 + 1, c0, fg(240) + "║" + frame + fg(250) + hdr + RESET + fg(240) + "║")
    T.at(r0 + 2, c0, fg(240) + "╠" + "═" * w + "╣")
    for i in range(len(lines)):
        T.at(r0 + 3 + i, c0, fg(240) + "║" + frame + " " * w + RESET + fg(240) + "║")
    T.at(r0 + 3 + len(lines), c0, fg(240) + "╚" + "═" * w + "╝" + RESET)
    settle = {}
    for i, l in enumerate(lines):
        for j, ch in enumerate(l):
            settle[(i, j)] = 0.25 + i * 0.35 + j * 0.035 + random.uniform(0, 0.4)
    t0 = T.now()
    done = False
    while not done:
        t = T.now() - t0
        if skip_pressed():
            t = 999
        done = True
        buf = []
        for i, l in enumerate(lines):
            parts = [frame]
            for j, ch in enumerate(l):
                if ch == " " or t >= settle[(i, j)]:
                    hot = i == len(lines) - 1 and ch != " "
                    parts.append((fg(196) if hot else fg(214)) + ch)
                else:
                    done = False
                    parts.append(fg(130) + random.choice(FLAP))
            buf.append("\x1b[%d;%dH%s" % (r0 + 3 + i, c0 + 3, "".join(parts)))
        T.write("".join(buf) + RESET)
        T.sleep(0.045)
    T.flush()
    return r0 + 4 + len(lines)


# ---------------------------------------------------------------- livestream
STREAM = [
    (0.3, "c", "ghostbuster_99", "bro its literally 2am"),
    (1.0, "s", None, "ok guys. tunnel 9. sealed since '87. we're going in."),
    (1.6, "c", "ankita.r", "ishaan pls dont"),
    (2.6, "c", "xXvoidXx", "fake. 100% fake"),
    (3.4, "s", None, "...like 400 metres in. it's so cold. you can see my breath."),
    (4.2, "c", "mohit_k", "why is there a green light behind u"),
    (5.0, "v", None, 196),
    (5.4, "c", "r3dshift", "theres something on the wall"),
    (6.2, "s", None, "guys. there's a light. up ahead."),
    (6.8, "c", "ankita.r", "TURN BACK"),
    (7.6, "c", "anon_211", "count the coaches"),
    (8.4, "s", None, "there's a TRAIN in here. it's lit up. how is it lit up"),
    (9.0, "c", "ghostbuster_99", "LMAOOO what"),
    (9.6, "v", None, 205),
    (10.2, "s", None, "someone's walking toward me. he's got a... lantern?"),
    (10.8, "c", "mohit_k", "dude his face"),
    (11.4, "c", "ankita.r", "ISHAAN RUN"),
    (12.2, "s", None, "hello? sir? ...he wants my ticket. he's asking for my ticket."),
    (12.8, "c", "_____", "ticket please"),
    (13.4, "v", None, 213),
    (13.6, "c", "_____", "ticket please"),
    (14.0, "c", "_____", "ticket please"),
    (14.4, "s", None, "...two hundred and twelve..."),
]
USER_COLS = [117, 180, 150, 210, 109, 223]


def livestream(duration=16.5):
    cols, rows = T.size()
    VW, VH = 44, 12
    CW = 31
    W = VW + CW + 3
    c0 = max(1, (cols - W) // 2 + 1)
    r0 = max(1, (rows - (VH + 7)) // 2)
    T.clear()
    edge = fg(240)
    T.at(r0, c0, edge + "┌" + "─" * VW + "┬" + "─" * CW + "┐")
    T.at(r0 + 1, c0, edge + "│" + " " * VW + "│" + " " * CW + "│")
    T.at(r0 + 2, c0, edge + "├" + "─" * VW + "┼" + "─" * CW + "┤")
    for i in range(VH + 3):
        T.at(r0 + 3 + i, c0, edge + "│" + " " * VW + "│" + " " * CW + "│")
    T.at(r0 + 3 + VH, c0, edge + "├" + "─" * VW + "┤")
    T.at(r0 + 6 + VH, c0, edge + "└" + "─" * VW + "┴" + "─" * CW + "┘" + RESET)
    ucol = {}
    chat = []
    sub = ""
    viewers = 187
    t0 = T.now()
    idx = 0
    ended = False
    while True:
        t = T.now() - t0
        if skip_pressed():
            t = duration + 1
            idx = len(STREAM)
            viewers = 213
            sub = "...two hundred and twelve..."
        while idx < len(STREAM) and STREAM[idx][0] <= t:
            _, kind, who, what = STREAM[idx]
            if kind == "c":
                if who not in ucol:
                    ucol[who] = 238 if who.startswith("_") else random.choice(USER_COLS)
                chat.append((who, what))
            elif kind == "s":
                sub = what
            elif kind == "v":
                viewers = what
            idx += 1
        if t < 13.4 and random.random() < 0.3:
            viewers += random.choice((0, 1, 1, 2))
        buf = []
        live = (fg(196) + "●" if int(t * 2) % 2 == 0 else " ") + fg(252) + " LIVE"
        head = " %s  %sishaan.explores" % (live, fg(250))
        buf.append("\x1b[%d;%dH%s" % (r0 + 1, c0 + 1, head + " " * 4 + fg(240) + "◉ %d watching  " % viewers))
        buf.append("\x1b[%d;%dH%s" % (r0 + 1, c0 + VW + 2, fg(245) + " CHAT".ljust(CW)))
        # video
        glitchy = t > duration - 3.0
        lamp = max(0.0, (t - 5.0) / 8.0)
        for i in range(VH):
            row = []
            for j in range(VW):
                dx = abs(j - VW / 2.0) / (VW / 2.0)
                dy = abs(i - VH / 2.0) / (VH / 2.0)
                ring = max(dx, dy)
                if glitchy and random.random() < min(0.9, (t - (duration - 3.0)) / 2.0):
                    row.append(fg(random.choice((236, 240, 244))) + random.choice(NOISE))
                    continue
                d = math.hypot((j - VW / 2.0) / 2.0, i - VH / 2.0)
                if lamp > 0 and d < lamp * 3.2:
                    row.append(fg(214 if d < lamp * 1.6 else 94) + ("█" if d < lamp * 1.2 else "░"))
                elif abs(ring - 0.92) < 0.06 or abs(ring - 0.62) < 0.05 or abs(ring - 0.35) < 0.05:
                    row.append(fg(235 if ring < 0.5 else 237) + "·")
                else:
                    row.append(" ")
            buf.append("\x1b[%d;%dH%s" % (r0 + 3 + i, c0 + 1, "".join(row)))
        sub_lines = textwrap.wrap(sub, VW - 2)[:2] + ["", ""]
        for si in range(2):
            buf.append("\x1b[%d;%dH%s" % (r0 + 4 + VH + si, c0 + 1, fg(252) + (" " + sub_lines[si]).ljust(VW)))
        # chat
        lines = []
        for who, what in chat:
            txt = "%s: %s" % (who, what)
            pieces = textwrap.wrap(txt, CW - 2, subsequent_indent="  ")
            for n, pc in enumerate(pieces):
                lines.append((who if n == 0 else None, pc))
        lines = lines[-(VH + 3):]
        for k in range(VH + 3):
            if k < len(lines):
                who, pc = lines[k]
                if who:
                    name, rest = pc.split(":", 1) if ":" in pc else (pc, "")
                    s = fg(ucol.get(who, 250)) + name + fg(250) + ":" + rest
                    vis = len(pc)
                else:
                    s = fg(250) + pc
                    vis = len(pc)
                buf.append("\x1b[%d;%dH %s%s" % (r0 + 3 + k, c0 + VW + 2, s, " " * (CW - 1 - vis)))
            else:
                buf.append("\x1b[%d;%dH%s" % (r0 + 3 + k, c0 + VW + 2, " " * CW))
        T.write("".join(buf) + RESET)
        if t >= duration:
            ended = True
            break
        T.sleep(1.0 / 14)
    if ended:
        msg = "STREAM ENDED · 3:17 AM"
        rr = r0 + 3 + VH // 2
        T.at(rr, c0 + 1 + (VW - len(msg)) // 2, bg(16) + fg(196) + BOLD + msg + RESET)
        T.flush()
        T.flush_input()
        hold(2.0)
    T.clear()


# ---------------------------------------------------------------- phone ring
def phone_ring(name, when, seconds=3.0):
    T.clear()
    screen = ["", "INCOMING CALL", "", name, "", when, "", "", ""]
    t0 = T.now()
    i = 0
    while T.now() - t0 < seconds:
        if skip_pressed():
            break
        lines = art.phone(screen, ring=i)
        r, c = center(lines)
        c += random.choice((-1, 0, 1)) if i % 2 else 0
        blank = [" " * (len(lines[0]) + 4)] * len(lines)
        blit(blank, r, c - 2)
        blit(lines, r, c, fg(250))
        # light up the screen text
        for k, l in enumerate(lines):
            if "INCOMING" in l or name in l or when in l:
                pos = l.find(l.strip())
                T.at(r + k, c + pos, fg(80) + l.strip() + RESET)
        if i == 0:
            T.ding()
        T.sleep(0.12)
        i += 1
    T.clear()


# --------------------------------------------------------------------- paper
def paper(title, lines):
    """A torn notebook page, typed out in a handwriting colour."""
    cols, rows = T.size()
    w = min(58, cols - 6)
    body = []
    for para in lines:
        words = para.split(" ")
        cur = ""
        for wd in words:
            if len(cur) + len(wd) + 1 > w - 6:
                body.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        body.append(cur)
        body.append("")
    h = len(body) + 4
    r0 = max(1, (rows - h) // 2)
    c0 = max(1, (cols - w) // 2 + 1)
    T.clear()
    edge = fg(137)
    torn = "".join(random.choice("▔▔▔ ▔") for _ in range(w))
    T.at(r0, c0, edge + torn)
    for i in range(h - 2):
        T.at(r0 + 1 + i, c0, bg(236) + " " * w + RESET)
    T.at(r0 + h - 1, c0, edge + "".join(random.choice("▁▁▁ ▁") for _ in range(w)) + RESET)
    T.at(r0 + 1, c0 + 3, bg(236) + fg(244) + title + RESET)
    skip = False
    for i, l in enumerate(body):
        T.at(r0 + 3 + i, c0 + 3, bg(236) + fg(180))
        for ch in l:
            if not skip and skip_pressed():
                skip = True
            T.write(bg(236) + fg(223 if ch.isupper() else 180) + ch)
            if not skip:
                T.sleep(0.018)
        T.write(RESET)
    T.flush()
    T.flush_input()
    T.at(min(rows, r0 + h + 1), c0 + w - 2, fg(245) + "▼" + RESET)
    T.flush()
    T.key()
    T.clear()


# --------------------------------------------------------------- title screen
def _title_block():
    cols, rows = T.size()
    hollow = art._block("\n".join(lettering.TITLE_HOLLOW))
    line = art._block("\n".join(lettering.TITLE_LINE))
    if cols >= 88 and rows >= 26:
        side = [h + "   " + (line[i] if i < len(line) else "") for i, h in enumerate(hollow)]
        return ["T  H  E"] + [""] + side, True
    if rows >= 36 and cols >= 60:
        return ["T  H  E".center(51), ""] + hollow + [""] + [l.center(51) for l in line], True
    return list(lettering.TITLE_SMALL), False


def draw_title(drips, flick=False):
    cols, rows = T.size()
    block, big = _title_block()
    w = max(len(l) for l in block)
    c0 = max(1, (cols - w) // 2 + 1)
    r0 = 2
    color = fg(52) if flick else fg(124)
    buf = []
    for i, l in enumerate(block):
        if i == 0 and big:
            buf.append("\x1b[%d;%dH%s%s" % (r0 + i, c0, fg(245), l))
        else:
            buf.append("\x1b[%d;%dH%s%s" % (r0 + i, c0, color, l))
    for (x, length) in drips:
        for k in range(int(length)):
            rr = r0 + len(block) + k
            ch = "▼" if k == int(length) - 1 else "│"
            buf.append("\x1b[%d;%dH%s%s" % (rr, c0 + x, fg(88), ch))
    T.write("".join(buf) + RESET)
    return r0 + len(block), w, c0


def title_screen(menu, footer=""):
    """Animated title. `menu` is a list of (key, label). Returns the key pressed."""
    T.clear()
    cols, rows = T.size()
    block, big = _title_block()
    last = block[-1]
    cand = [i for i, ch in enumerate(last) if ch != " "] or [5, 10, 20]
    drips = []
    T.flush_input()
    frame = 0
    while True:
        frame += 1
        if random.random() < 0.08 and len(drips) < 10:
            drips.append([random.choice(cand), 0.0, random.uniform(0.6, 2.2), random.randint(1, 3)])
        for d in drips:
            d[1] = min(d[3], d[1] + d[2] * 0.06)
        flick = random.random() < 0.04
        bottom, w, c0 = draw_title([(d[0], d[1]) for d in drips], flick)
        menu_top = min(bottom + 4, max(1, rows - len(menu) - 2))
        mc = max(1, (cols - 34) // 2 + 1)
        for i, (k, label) in enumerate(menu):
            T.at(menu_top + i, mc, fg(240) + "[%s]  " % k + fg(250) + label + RESET + "      ")
        if footer and menu_top + len(menu) + 1 <= rows:
            ctext(menu_top + len(menu) + 1, footer, fg(238))
        T.flush()
        k = T.key(0.06)
        if k is not None:
            return k
        if frame % 300 == 0:
            T.clear()
            drips = []
