"""The narration page: HUD, typewriter text, choices, timed choices, text input."""
import random

from .term import T, STYLES, RESET, BOLD, fg, parse, wrap, render, vlen

GLITCH = "#%&@$?!░▒▓/\\"
SPEEDS = {"slow": 26, "normal": 46, "fast": 110, "instant": 0}


class QuitToTitle(Exception):
    pass


class UI:
    TOP = 4

    def __init__(self, game):
        self.g = game
        self.row = self.TOP
        self.hud = True
        self._tag_x = None

    # --------------------------------------------------------------- layout
    @property
    def width(self):
        cols, _ = T.size()
        return max(30, min(72, cols - 8))

    @property
    def left(self):
        cols, _ = T.size()
        return max(1, (cols - self.width) // 2 + 1)

    @property
    def bottom(self):
        _, rows = T.size()
        return rows - 1

    def page(self, hud=True):
        T.clear()
        self.hud = hud
        if hud:
            self.draw_hud()
            self.row = self.TOP
        else:
            self.row = 3
        self._tag_x = None
        T.flush()

    def ensure(self, n):
        if self.row + n - 1 > self.bottom - 1:
            self.more()
            self.page(self.hud)

    # ------------------------------------------------------------------ HUD
    def draw_hud(self):
        if not self.hud:
            return
        s = self.g.s
        cols, _ = T.size()
        hearts = ""
        for i in range(s.max_health):
            hearts += (STYLES["R"] + "♥" if i < s.health else RESET + fg(238) + "♡") + " "
        n = 10
        filled = max(0, min(n, int(round(s.sanity / 100.0 * n))))
        sc = 141 if s.sanity > 60 else (133 if s.sanity > 30 else 161)
        label = "MIND"
        if s.sanity < 30 and random.random() < 0.6:
            label = random.choice(["M!ND", "MI#D", "M▒ND", "NIMD", "HELP"])
        bat = s.battery
        bc = 187 if bat > 50 else (214 if bat > 20 else 160)
        bf = max(0, min(6, int(round(bat / 100.0 * 6))))
        torch = fg(bc) + "█" * bf + fg(236) + "░" * (6 - bf)
        if s.spares:
            torch += fg(242) + " +%d" % s.spares
        parts = [
            " " + hearts,
            fg(244) + label + " " + fg(sc) + "█" * filled + fg(236) + "░" * (n - filled),
            fg(244) + "TORCH " + torch,
        ]
        if s.pages:
            parts.append(fg(244) + "PAGES " + fg(180) + "%d/3" % len(s.pages))
        line = (RESET + "  ").join(parts) + RESET
        right = fg(240) + self.g.chapter_label + " " + RESET
        if vlen(line) + vlen(right) + 2 <= cols - 1:
            line += " " * (cols - 1 - vlen(line) - vlen(right)) + right
        T.write("\x1b[1;1H\x1b[2K" + line)
        T.write("\x1b[2;1H\x1b[2K" + fg(236) + "─" * (cols - 1) + RESET)
        T.flush()

    def tag(self, text, color):
        """Small right-aligned stat change marker on the blank line above."""
        r = self.row - 1
        if r < self.TOP:
            return
        right = self.left + self.width if self._tag_x is None else self._tag_x
        c = right - len(text)
        T.at(r, c, fg(color) + text + RESET)
        self._tag_x = c - 2
        T.flush()

    # ----------------------------------------------------------------- text
    def say(self, text, style="t", speed=1.0, gap=1, instant=False):
        text = text.replace("@NAME", self.g.s.name)
        lines = wrap(parse(text, style), self.width)
        cps = SPEEDS.get(self.g.settings.get("speed"), 46) * speed
        skip = instant or cps <= 0
        self._tag_x = None
        for ln in lines:
            self.ensure(1)
            T.at(self.row, self.left)
            if skip:
                T.write(render(ln))
            else:
                skip = self._type(ln, cps)
            self.row += 1
        self.row += gap
        T.flush()

    def _type(self, ln, cps):
        delay = 1.0 / cps
        san = self.g.s.sanity
        p_glitch = max(0.0, (45 - san) / 650.0)
        cur = None
        for i, (ch, st) in enumerate(ln):
            if T.poll() is not None:
                T.write(render(ln[i:]))
                return True
            if st != cur:
                T.write(RESET + STYLES[st])
                cur = st
            if p_glitch and ch != " " and random.random() < p_glitch:
                T.write(STYLES["R"] + random.choice(GLITCH))
                T.sleep(0.06)
                T.write("\b" + RESET + STYLES[st] + ch)
            else:
                T.write(ch)
            d = delay
            if ch in ".!?":
                d *= 6
            elif ch in ",;:":
                d *= 3
            T.sleep(d)
        T.write(RESET)
        return False

    def pause(self, s):
        fast = self.g.settings.get("speed") in ("fast", "instant")
        T.sleep(s * (0.5 if fast else 1.0))

    # ----------------------------------------------------------------- waits
    def _blink(self, r, c, glyph="▼"):
        T.flush_input()
        on = True
        while True:
            T.at(r, c, (fg(245) + glyph if on else " ") + RESET)
            T.flush()
            k = T.key(0.5)
            if k is None:
                on = not on
                continue
            if k in ("ESC", "q", "Q"):
                self.pause_menu()
                continue
            break
        T.at(r, c, " ")
        T.flush()

    def more(self):
        self._blink(self.bottom, self.left + self.width - 1)

    def wait(self):
        r = max(self.TOP, min(self.row - 1, self.bottom))
        self._blink(r, self.left + self.width - 1)

    def pause_menu(self):
        r = self.bottom + 1
        cols, _ = T.size()
        msg = "  Quit to title? (progress is kept from the chapter start)"
        msg = msg[: max(0, cols - 22)]
        T.at(r, 1, "\x1b[2K" + fg(245) + msg + "  " + fg(231) + "[Y]" + fg(245) + " yes  "
             + fg(231) + "[N]" + fg(245) + " no" + RESET)
        T.flush()
        T.flush_input()
        while True:
            k = T.key()
            if k in ("y", "Y"):
                raise QuitToTitle()
            if k in ("n", "N", "ESC", "q", "Q", "\n"):
                break
        T.at(r, 1, "\x1b[2K")
        T.flush()

    # --------------------------------------------------------------- choices
    def choose(self, options, timeout=None, default=None):
        opts = [o.replace("@NAME", self.g.s.name) for o in options]
        wrapped = [wrap(parse(o, "o"), self.width - 7) for o in opts]
        body = sum(len(w) for w in wrapped)
        need = body + (3 if timeout else 1)
        self.ensure(need)
        top = self.row
        spots = []
        r = top
        for wl in wrapped:
            spots.append((r, wl))
            r += len(wl)
        end_row = r

        def draw(i, state):
            r0, wl = spots[i]
            for j, ln in enumerate(wl):
                if j == 0:
                    if state == "chosen":
                        pre = fg(196) + " › " + fg(231) + "[%d] " % (i + 1)
                    elif state == "faded":
                        pre = fg(236) + "   [%d] " % (i + 1)
                    else:
                        pre = fg(242) + "   [%d] " % (i + 1)
                else:
                    pre = "       "
                over = {"chosen": "w", "faded": "D"}.get(state)
                T.at(r0 + j, self.left, pre + RESET + render(ln, over))

        for i in range(len(opts)):
            draw(i, "normal")
            T.sleep(0.05)
        T.flush()
        T.flush_input()
        bar_row = end_row + 1
        start = T.now()
        result = None
        while True:
            if timeout:
                left = timeout - (T.now() - start)
                if left <= 0:
                    result = default
                    break
                self._timer(bar_row, left / timeout, left)
                k = T.key(0.05)
            else:
                k = T.key()
            if k is None:
                continue
            if len(k) == 1 and k.isdigit() and 1 <= int(k) <= len(opts):
                result = int(k) - 1
                break
            if not timeout and k in ("q", "Q", "ESC"):
                self.pause_menu()
        for i in range(len(opts)):
            draw(i, "chosen" if i == result else "faded")
        if timeout:
            T.at(bar_row, 1, "\x1b[2K")
        T.flush()
        T.sleep(0.35)
        self.row = end_row + 1
        return result

    def _timer(self, r, frac, left):
        w = min(36, self.width - 12)
        n = max(0, int(round(frac * w)))
        col = 46 if frac > 0.6 else (214 if frac > 0.3 else 196)
        bar = fg(col) + "█" * n + fg(236) + "░" * (w - n)
        T.at(r, self.left + 3, bar + " " + fg(245) + "%4.1fs" % max(0.0, left) + RESET)
        T.flush()

    # ------------------------------------------------------------ text input
    def ask(self, prompt, maxlen=12, digits=False, default=""):
        self.say(prompt, gap=0)
        self.ensure(3)
        r = self.row + 1
        c = self.left + 3
        buf = ""
        T.flush_input()
        on = True
        while True:
            field = (fg(231) + BOLD + buf + RESET + (fg(196) + "▌" if on else " ")
                     + fg(238) + "_" * (maxlen - len(buf)) + RESET)
            T.at(r, c, "\x1b[K" + fg(242) + "› " + field)
            T.flush()
            k = T.key(0.5)
            if k is None:
                on = not on
                continue
            on = True
            if k == "\n":
                if buf.strip() or default:
                    break
            elif k == "BACKSPACE":
                buf = buf[:-1]
            elif len(k) == 1 and len(buf) < maxlen:
                if digits:
                    if k.isdigit():
                        buf += k
                elif k.isalpha() or (k in " -'" and buf):
                    buf += k
        T.at(r, c, "\x1b[K" + fg(242) + "› " + fg(231) + BOLD + buf + RESET)
        self.row = r + 2
        return buf.strip() or default

    # ---------------------------------------------------------- notification
    def notify(self, label, text, color=180):
        inner = "  %s   %s  " % (label, text)
        w = len(inner)
        self.ensure(4)
        r = self.row
        c = self.left + 2
        for lvl in (231, 230, 223, color):
            T.at(r, c, fg(lvl) + "┌" + "─" * w + "┐")
            T.at(r + 1, c, fg(lvl) + "│" + BOLD + inner + RESET + fg(lvl) + "│")
            T.at(r + 2, c, fg(lvl) + "└" + "─" * w + "┘" + RESET)
            T.sleep(0.07)
        T.flush()
        self.row += 4
