"""Low-level terminal layer for THE HOLLOW LINE.

Standard library only. Handles 256-colour ANSI output, cursor control and raw
single-key input with timeouts (Windows: msvcrt, macOS/Linux: termios+select).
Every sleep and clock read goes through T.sleep / T.now, so the whole game can
be fast-forwarded by swapping the clock (used by the test bot).
"""
import os
import re
import sys
import time
import shutil
from collections import deque

IS_WIN = os.name == "nt"
if IS_WIN:  # pragma: no cover
    import msvcrt
else:
    import select
    import termios
    import tty

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def fg(n):
    return "\x1b[38;5;%dm" % n


def bg(n):
    return "\x1b[48;5;%dm" % n


def vlen(s):
    """Visible length of a string (ANSI codes stripped)."""
    return len(ANSI_RE.sub("", s))


# Text styles used by the {x} markup in story text.
STYLES = {
    "t": fg(250),          # narration
    "o": fg(253),          # choice text
    "w": BOLD + fg(231),   # speech / emphasis
    "d": fg(243),          # dim
    "D": fg(238),          # very dim
    "r": fg(160),          # red
    "R": BOLD + fg(196),   # blood red
    "y": fg(214),          # lantern amber
    "Y": BOLD + fg(220),
    "g": fg(71),           # signal green
    "G": BOLD + fg(46),
    "c": fg(80),           # screens, phones
    "p": fg(140),          # the uncanny
    "b": fg(67),
}

TAG_RE = re.compile(r"\{([a-zA-Z/])\}")


def parse(text, base="t"):
    """Turn '{r}red{/} text' into a list of (char, style_key)."""
    out = []
    cur = base
    pos = 0
    for m in TAG_RE.finditer(text):
        for ch in text[pos:m.start()]:
            out.append((ch, cur))
        k = m.group(1)
        if k == "/":
            cur = base
        elif k in STYLES:
            cur = k
        pos = m.end()
    for ch in text[pos:]:
        out.append((ch, cur))
    return out


def wrap(chars, width):
    """Word-wrap a list of (char, style) into lines no wider than width."""
    lines = []
    line = []
    word = []

    def push():
        nonlocal line
        if not word:
            return
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = []
        if line:
            line.append((" ", word[0][1]))
        line.extend(word)

    for ch, st in chars:
        if ch == "\n":
            push()
            word = []
            lines.append(line)
            line = []
        elif ch == " ":
            push()
            word = []
        else:
            word.append((ch, st))
    push()
    if line or not lines:
        lines.append(line)
    return lines


def render(chars, override=None):
    """Render (char, style) pairs into an ANSI string."""
    out = []
    cur = None
    for ch, st in chars:
        st = override or st
        if st != cur:
            out.append(RESET + STYLES[st])
            cur = st
        out.append(ch)
    out.append(RESET)
    return "".join(out)


class Clock:
    def now(self):
        return time.monotonic()

    def sleep(self, s):
        if s > 0:
            time.sleep(s)


class Terminal:
    def __init__(self):
        self.interactive = sys.stdin.isatty() and sys.stdout.isatty()
        self.clock = Clock()
        self.queue = deque()
        self.fd = None
        self._old = None
        self.active = False
        self.bell = True
        self.reduce_flash = False

    # ------------------------------------------------------------ output
    def write(self, s):
        sys.stdout.write(s)

    def flush(self):
        try:
            sys.stdout.flush()
        except Exception:
            pass

    def size(self):
        s = shutil.get_terminal_size((100, 30))
        return max(40, s.columns), max(16, s.lines)

    def clear(self):
        self.write(RESET + "\x1b[2J\x1b[H")

    def at(self, r, c, s=""):
        self.write("\x1b[%d;%dH%s" % (max(1, r), max(1, c), s))

    def ding(self):
        if self.bell:
            self.write("\a")

    def now(self):
        return self.clock.now()

    def sleep(self, s):
        self.flush()
        self.clock.sleep(s)

    # ------------------------------------------------------- lifecycle
    def start(self):
        if IS_WIN:  # pragma: no cover
            try:
                import ctypes
                k = ctypes.windll.kernel32
                h = k.GetStdHandle(-11)
                mode = ctypes.c_uint32()
                if k.GetConsoleMode(h, ctypes.byref(mode)):
                    k.SetConsoleMode(h, mode.value | 0x0004)
            except Exception:
                pass
            os.system("")
        try:
            enc = (sys.stdout.encoding or "").lower().replace("-", "")
            if enc != "utf8" and hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        if not IS_WIN and self.interactive:
            self.fd = sys.stdin.fileno()
            self._old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        self.write("\x1b[?1049h\x1b[?25l")
        self.clear()
        self.flush()
        self.active = True

    def stop(self):
        if not self.active:
            return
        self.active = False
        self.write(RESET + "\x1b[?25h\x1b[2J\x1b[H\x1b[?1049l")
        self.flush()
        if self._old is not None:
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self._old)
            except Exception:
                pass

    # ----------------------------------------------------------- input
    @staticmethod
    def _norm(ch):
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch in ("\r", "\n"):
            return "\n"
        if ch in ("\x7f", "\x08"):
            return "BACKSPACE"
        if ch == "\x1b":
            return "ESC"
        return ch

    def _fill(self, timeout):
        """Wait up to `timeout` seconds (None = forever) and queue any keys."""
        if not self.interactive:
            if timeout is not None:
                self.clock.sleep(timeout)
                return
            line = sys.stdin.readline()
            if line == "":
                raise KeyboardInterrupt
            for ch in line.rstrip("\r\n"):
                self.queue.append(ch)
            self.queue.append("\n")
            return
        if IS_WIN:  # pragma: no cover
            end = None if timeout is None else time.monotonic() + timeout
            while True:
                got = False
                while msvcrt.kbhit():
                    got = True
                    ch = msvcrt.getwch()
                    if ch in ("\x00", "\xe0"):
                        code = msvcrt.getwch()
                        k = {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}.get(code)
                        if k:
                            self.queue.append(k)
                        continue
                    self.queue.append(self._norm(ch))
                if got:
                    return
                if end is not None and time.monotonic() >= end:
                    return
                time.sleep(0.008)
        r, _, _ = select.select([self.fd], [], [], timeout)
        if not r:
            return
        data = os.read(self.fd, 256).decode("utf-8", "ignore")
        i = 0
        while i < len(data):
            ch = data[i]
            if ch == "\x1b" and i + 2 < len(data) and data[i + 1] in "[O":
                code = data[i + 2]
                k = {"A": "UP", "B": "DOWN", "C": "RIGHT", "D": "LEFT"}.get(code)
                self.queue.append(k or "ESC")
                i += 3
                continue
            self.queue.append(self._norm(ch))
            i += 1

    def poll(self):
        """Non-blocking: the next key, or None."""
        if not self.queue:
            self._fill(0)
        return self.queue.popleft() if self.queue else None

    def key(self, timeout=None):
        """Wait for a key. Returns None if `timeout` seconds pass first."""
        if self.queue:
            return self.queue.popleft()
        if timeout is None:
            while not self.queue:
                self._fill(None)
            return self.queue.popleft()
        end = self.now() + timeout
        while True:
            left = end - self.now()
            if left <= 0:
                return None
            self._fill(left)
            if self.queue:
                return self.queue.popleft()

    def flush_input(self):
        self.queue.clear()
        if not self.interactive:
            return
        if IS_WIN:  # pragma: no cover
            while msvcrt.kbhit():
                msvcrt.getwch()
        else:
            try:
                termios.tcflush(self.fd, termios.TCIFLUSH)
            except Exception:
                pass


T = Terminal()
