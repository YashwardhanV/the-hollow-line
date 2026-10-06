"""Real-time challenges: quick-time keys, mashing, breath control, the lantern
walk, holding still, the headlight and the lever frame."""
import math
import random

from .term import T, fg, bg, RESET, BOLD
from . import fx, art

QTE_KEYS = "ASDFJKLEWRUIO"


def _frame(title, hint=None):
    T.clear()
    cols, rows = T.size()
    if title:
        fx.ctext(3, title, fg(196) + BOLD)
    if hint:
        fx.ctext(rows - 1, hint, fg(242))
    return cols, rows


def _bar(frac, w, good=46):
    n = max(0, min(w, int(round(frac * w))))
    col = good if frac > 0.6 else (214 if frac > 0.3 else 196)
    return fg(col) + "█" * n + fg(236) + "░" * (w - n) + RESET


def _keybox(key, color):
    return [color + "┏━━━━━━━┓", color + "┃       ┃", color + "┃   " + BOLD + key + RESET + color + "   ┃",
            color + "┃       ┃", color + "┗━━━━━━━┛" + RESET]


def _draw_box(r, c, key, color):
    for i, l in enumerate(_keybox(key, color)):
        T.at(r + i, c, l)


def _shaky_title(r, text, amp, color):
    cols, _ = T.size()
    T.at(r, 1, "\x1b[2K")
    off = random.randint(-amp, amp) if amp else 0
    T.at(r, max(1, (cols - len(text)) // 2 + 1 + off), color + text + RESET)


# ------------------------------------------------------------------ QTE
def _one_key(g, key, seconds, r, c, bar_r, bar_c, title=None):
    start = T.now()
    _draw_box(r, c, key, fg(252))
    while True:
        left = seconds - (T.now() - start)
        if left <= 0:
            _draw_box(r, c, key, fg(196))
            T.flush()
            return False
        T.at(bar_r, bar_c, _bar(left / seconds, 40) + fg(245) + " %4.1fs" % left + RESET)
        if title:
            _shaky_title(3, title, 2 if left < seconds * 0.4 else 1, fg(196) + BOLD)
        T.flush()
        k = T.key(0.03)
        if k is None:
            continue
        if k.upper() == key:
            _draw_box(r, c, key, fg(46))
            T.flush()
            return True
        start -= seconds * 0.3
        _draw_box(r, c, key, fg(160))
        T.flush()
        T.sleep(0.05)
        _draw_box(r, c, key, fg(252))


def qte(g, key, seconds, title="", hint="Press the key. Fast."):
    if not T.interactive:
        return True
    seconds *= g.time_factor()
    key = key.upper()
    cols, rows = _frame(title, hint)
    cy = rows // 2 - 2
    T.flush_input()
    ok = _one_key(g, key, seconds, cy, (cols - 9) // 2 + 1, cy + 7, (cols - 46) // 2 + 1, title)
    fx.ctext(cy + 9, "✓" if ok else "✗", fg(46) if ok else fg(196))
    T.sleep(0.45)
    return ok


def sequence(g, n, seconds, title="", hint="Hit each key as it appears."):
    """n keys in a row. Returns the number of misses."""
    if not T.interactive:
        return 0
    seconds *= g.time_factor()
    cols, rows = _frame(title, hint)
    cy = rows // 2 - 2
    keys = []
    for _ in range(n):
        k = random.choice(QTE_KEYS)
        while keys and k == keys[-1]:
            k = random.choice(QTE_KEYS)
        keys.append(k)
    misses = 0
    T.flush_input()
    for i, k in enumerate(keys):
        dots = "".join((fg(46) + "● " if j < i else (fg(231) + "◉ " if j == i else fg(238) + "○ ")) for j in range(n))
        fx.ctext(cy - 3, dots.rstrip(), "")
        ok = _one_key(g, k, seconds, cy, (cols - 9) // 2 + 1, cy + 7, (cols - 46) // 2 + 1, title)
        if not ok:
            misses += 1
            fx.vignette(124, 1)
        T.sleep(0.12)
        T.flush_input()
    return misses


# ----------------------------------------------------------------- mash
def mash(g, seconds, title="", need=18, hint="Alternate  A  and  D  as fast as you can."):
    if not T.interactive:
        return True
    seconds *= g.time_factor()
    cols, rows = _frame(title, hint)
    cy = rows // 2 - 3
    lc = (cols - 26) // 2 + 1
    expect = "A"
    prog = 0.0
    start = T.now()
    last = start
    T.flush_input()
    while True:
        now = T.now()
        left = seconds - (now - start)
        prog = max(0.0, prog - 1.1 * (now - last))
        last = now
        if prog >= need:
            ok = True
            break
        if left <= 0:
            ok = False
            break
        _draw_box(cy, lc, "A", fg(231) if expect == "A" else fg(238))
        _draw_box(cy, lc + 17, "D", fg(231) if expect == "D" else fg(238))
        T.at(cy + 6, (cols - 46) // 2 + 1, fg(245) + "STRENGTH " + _bar(prog / need, 36, good=196))
        T.at(cy + 8, (cols - 46) // 2 + 1, fg(245) + "TIME     " + _bar(left / seconds, 36) + fg(245) + " %4.1fs" % left + RESET)
        _shaky_title(3, title, int(1 + 3 * prog / need), fg(196) + BOLD)
        T.flush()
        k = T.key(0.025)
        if k and k.upper() == expect:
            prog += 1
            expect = "D" if expect == "A" else "A"
    fx.ctext(cy + 11, "FREE" if ok else "TOO SLOW", (fg(46) if ok else fg(196)) + BOLD)
    T.flush()
    T.sleep(0.6)
    return ok


# --------------------------------------------------------------- breathe
def breathe(g, needed=3, attempts=6):
    """Press when the marker is inside the green zone. Returns hits."""
    if not T.interactive:
        return needed
    tf = g.time_factor()
    cols, rows = _frame("STEADY YOUR BREATHING", "Press any key when the marker is inside the green zone.")
    W = min(48, cols - 10)
    c0 = (cols - W) // 2 + 1
    cy = rows // 2
    hits = 0
    zone_w = 10
    speed = 30.0 / tf
    for a in range(attempts):
        if hits >= needed:
            break
        zw = max(4, zone_w - 2 * hits)
        z0 = random.randint(2, W - zw - 2)
        pos = random.choice((0.0, float(W - 1)))
        direction = 1 if pos == 0 else -1
        dots = "".join((fg(46) + "● " if j < hits else fg(238) + "○ ") for j in range(needed))
        fx.ctext(cy - 5, "BREATH  " + dots, fg(245))
        fx.ctext(cy - 3, random.choice(["in...", "hold...", "slowly...", "in... out..."]), fg(242))
        T.flush_input()
        t_start = T.now()
        last = t_start
        pressed = False
        while T.now() - t_start < 4.5:
            now = T.now()
            pos += direction * speed * (now - last)
            last = now
            if pos <= 0:
                pos, direction = 0.0, 1
            if pos >= W - 1:
                pos, direction = float(W - 1), -1
            cells = []
            for i in range(W):
                inz = z0 <= i < z0 + zw
                if i == int(pos):
                    cells.append(fg(231) + "█")
                else:
                    cells.append((fg(28) + "▓") if inz else (fg(237) + "░"))
            T.at(cy, c0, "".join(cells) + RESET)
            T.flush()
            if T.key(0.02) is not None:
                pressed = True
                break
        inside = pressed and z0 <= int(pos) < z0 + zw
        if inside:
            hits += 1
            fx.ctext(cy + 2, "   steady   ", fg(46) + BOLD)
        else:
            fx.ctext(cy + 2, "  BREATHE!  ", fg(196) + BOLD)
            g.mind(-2, quiet=True)
        T.sleep(0.5)
        fx.ctext(cy + 2, "            ", "")
    return hits


# ---------------------------------------------------------- lantern walk
def lantern_walk(g, steps=12, max_caught=3):
    """Move only in the dark between lantern swings. Returns times caught."""
    if not T.interactive:
        return 0
    tf = g.time_factor()
    cols, rows = _frame("", "Any key = one step.  Move in the DARK.  Freeze when the LANTERN is LIT.")
    W = min(58, cols - 12)
    c0 = (cols - W) // 2 + 1
    r0 = rows // 2 - 4
    pos = 0
    caught = 0
    phase = "dark"
    phase_end = T.now() + random.uniform(1.4, 2.2) * tf
    last_step = 0.0
    T.flush_input()

    def draw(lit, warn, flash=False):
        x = 1 + int(pos / float(steps) * (W - 8))
        aisle = []
        for i in range(W):
            if i == x:
                aisle.append(fg(231) + BOLD + "@" + RESET)
            elif i == W - 4:
                aisle.append(fg(214) + "*")
            elif i == W - 3:
                aisle.append(fg(252) + BOLD + "T" + RESET)
            elif lit and x < i < W - 4:
                aisle.append(fg(136) + "░")
            else:
                aisle.append(fg(238) + "·")
        seat = []
        for i in range(W):
            if i % 3 == 1 and i < W - 5:
                seat.append((fg(196) + "●") if lit else (fg(240) + "o"))
            else:
                seat.append(fg(236) + "▄")
        edge = fg(214) if lit else fg(238)
        T.at(r0, c0 - 1, edge + "╔" + "═" * W + "╗")
        T.at(r0 + 1, c0 - 1, edge + "║" + "".join(seat) + edge + "║")
        T.at(r0 + 2, c0 - 1, edge + "║" + "".join(aisle) + edge + "║")
        T.at(r0 + 3, c0 - 1, edge + "║" + "".join(seat) + edge + "║")
        T.at(r0 + 4, c0 - 1, edge + "╚" + "═" * W + "╝" + RESET)
        if flash:
            msg, col = "  IT SEES YOU  ", bg(124) + fg(231) + BOLD
        elif lit:
            msg, col = "  THE LANTERN IS ON YOU.  DON'T MOVE.  ", bg(94) + fg(231) + BOLD
        elif warn:
            msg, col = "      ...it's turning...      ", fg(214)
        else:
            msg, col = "         dark.  move.         ", fg(240)
        T.at(r0 + 7, 1, "\x1b[2K")
        fx.ctext(r0 + 7, msg, col)
        fx.ctext(r0 - 3, '“Tickets.  Tickets, please.”', fg(250))
        fx.ctext(r0 + 9, "STEPS %2d / %d" % (pos, steps), fg(242))
        T.flush()

    while pos < steps and caught < max_caught:
        now = T.now()
        if now >= phase_end:
            if phase == "dark":
                phase = "warn"
                phase_end = now + random.uniform(0.5, 0.75) * max(0.8, tf)
            elif phase == "warn":
                phase = "lit"
                phase_end = now + random.uniform(1.2, 2.4)
            else:
                phase = "dark"
                phase_end = now + random.uniform(1.0, 2.2) * tf
        warn_flick = phase == "warn" and int(now * 10) % 2 == 0
        draw(phase == "lit", phase == "warn" and warn_flick)
        k = T.key(0.03)
        if k is None:
            continue
        if phase == "lit":
            caught += 1
            for _ in range(3):
                draw(True, False, flash=True)
                fx.vignette(160, 1)
            pos = max(0, pos - 3)
            T.sleep(0.6)
            T.flush_input()
            phase = "dark"
            phase_end = T.now() + random.uniform(1.4, 2.2) * tf
            continue
        if now - last_step >= 0.14:
            pos += 1
            last_step = now
    draw(False, False)
    T.sleep(0.4)
    return caught


# --------------------------------------------------------- hold still
def stillness(g, seconds, voice, prompt="[  PRESS  Y  TO ANSWER  ]"):
    """The screen begs you to press a key. Returns True if you didn't."""
    if not T.interactive:
        return True
    cols, rows = T.size()
    T.clear()
    cy = rows // 2 - 3
    T.flush_input()
    start = T.now()
    shown = 0
    gap = seconds / float(len(voice) + 1)
    while True:
        t = T.now() - start
        if t >= seconds:
            break
        while shown < len(voice) and t >= gap * shown + 0.3:
            r = cy - 4 + shown * 2
            fx.ctext(r, voice[shown].replace("@NAME", g.s.name), fg(231))
            shown += 1
        on = int(t * 3) % 2 == 0
        fx.ctext(cy + 6, prompt, (bg(124) + fg(231) + BOLD) if on else fg(124))
        frac = 1.0 - t / seconds
        T.at(cy + 8, (cols - 40) // 2 + 1, _bar(frac, 40, good=196))
        T.flush()
        if T.key(0.04) is not None:
            return False
    T.at(cy + 6, 1, "\x1b[2K")
    T.at(cy + 8, 1, "\x1b[2K")
    for txt in ("[  PR  SS  Y  T   AN  WER  ]", "[  ? ? ?  ]", "", ):
        T.at(cy + 6, 1, "\x1b[2K")
        if txt:
            fx.ctext(cy + 6, txt, fg(238))
        T.sleep(0.25)
    return True


# ------------------------------------------------------------ headlight
def headlight(g, seconds=7.0):
    """The train charges at you. Returns True if you didn't flinch."""
    if not T.interactive:
        return True
    cols, rows = T.size()
    T.clear()
    cx = cols / 2.0
    cy = rows / 2.0
    maxr = math.hypot(cols / 4.0, rows / 2.0) * 1.15
    start = T.now()
    T.flush_input()
    held = True
    while True:
        t = T.now() - start
        if t >= seconds:
            break
        p = t / seconds
        R = 0.6 + (p ** 2.2) * maxr
        shake = int(p * 3)
        ox = random.randint(-shake, shake)
        oy = random.randint(-1, 1) if p > 0.5 else 0
        buf = []
        for r in range(1, rows + 1):
            parts = []
            mode = None
            for c in range(1, cols):
                d = math.hypot((c - cx - ox) / 2.0, r - cy - oy)
                if d < R * 0.35:
                    m, ch = 231, "█"
                elif d < R * 0.6:
                    m, ch = 229, "▓"
                elif d < R * 0.85:
                    m, ch = 222, "▒"
                elif d < R * 1.15:
                    m, ch = 136, "░"
                elif d < R * 1.5 and random.random() < 0.08:
                    m, ch = 94, "·"
                else:
                    m, ch = 0, " "
                if m != mode:
                    parts.append(fg(m) if m else "")
                    mode = m
                parts.append(ch)
            buf.append("\x1b[%d;1H%s" % (r, "".join(parts)))
        T.write("".join(buf) + RESET)
        lamp_r = int(rows - 3)
        fx.ctext(lamp_r, "  your red lamp, held high  ", bg(52) + fg(196) + BOLD)
        if p > 0.35 and int(t * 4) % 2 == 0:
            fx.ctext(3, "  [ ANY KEY ]  JUMP ASIDE  ", bg(16) + fg(231) + BOLD)
        T.flush()
        if T.key(0.03) is not None:
            held = False
            break
    if held:
        if not T.reduce_flash:
            fx.fill_screen(231)
            T.sleep(0.12)
        fx.fill_screen(16)
        T.sleep(1.2)
    T.clear()
    T.flush_input()
    return held


# --------------------------------------------------------------- levers
def levers(g, target, hint_line=None, on_wrong=None):
    """Lever frame puzzle. `target` is a list like ['R','N','N','R']."""
    state = ["N", "N", "N", "N"]
    tries = 0
    if not T.interactive:
        return 1
    colours = [160, 245, 245, 160]
    msg = ""
    while True:
        cols, rows = T.size()
        T.clear()
        fx.ctext(2, "LEVER FRAME  ·  TUNNEL 9", fg(245) + BOLD)
        fx.ctext(4, "[1]-[4] throw a lever     [ENTER] test the route", fg(242))
        r0 = 7
        c0 = (cols - 4 * 9) // 2 + 1
        for i in range(4):
            spr = art.LEVER_N if state[i] == "N" else art.LEVER_R
            for k, l in enumerate(spr):
                col = colours[i] if "●" in l else 244
                T.at(r0 + k, c0 + i * 9 + 2, fg(col) + l + RESET)
            T.at(r0 + 6, c0 + i * 9 + 3, fg(231) + str(i + 1) + RESET)
            T.at(r0 + 7, c0 + i * 9 + 2, fg(242) + ("NORM" if state[i] == "N" else "REV ") + RESET)
        T.at(r0 + 5, c0, fg(240) + "═" * (4 * 9) + RESET)
        fx.ctext(r0 + 10, "Tunnel 9 signal:  " + fg(160) + "●  RED", fg(245))
        if hint_line:
            fx.ctext(r0 + 13, hint_line, fg(180))
        if msg:
            fx.ctext(r0 + 15, msg, fg(160))
        T.flush()
        T.flush_input()
        k = T.key()
        if k in ("1", "2", "3", "4"):
            i = int(k) - 1
            state[i] = "R" if state[i] == "N" else "N"
            msg = ""
            continue
        if k == "\n":
            tries += 1
            if state == target:
                fx.ctext(r0 + 10, "Tunnel 9 signal:  " + fg(46) + BOLD + "●  GREEN" + RESET, fg(245))
                T.flush()
                T.sleep(1.4)
                T.clear()
                return tries
            msg = "CLANK.  The frame locks.  Nothing moves."
            fx.vignette(88, 1)
            if on_wrong:
                extra = on_wrong(tries)
                if extra:
                    hint_line = extra
