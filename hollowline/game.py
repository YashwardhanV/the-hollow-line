"""Game loop: title screen, menus, chapters, death, endings."""
import getpass
import random

from .term import T, fg, bg, RESET, BOLD
from .ui import UI, QuitToTitle
from .state import State, Save, Death, Ending
from . import fx, art, lettering, story

TIME_FACTOR = {"story": 1.6, "normal": 1.0, "nightmare": 0.75}
MIND_MULT = {"story": 0.6, "normal": 1.0, "nightmare": 1.3}
NOT_NAMES = {"root", "user", "admin", "administrator", "pc", "owner", "guest", "default",
             "ubuntu", "runner", "claude", "home", "test", "student", "windows", "desktop"}


class Game:
    def __init__(self, save=None):
        self.save = save or Save()
        self.settings = self.save.settings
        self.s = State()
        self.ui = UI(self)
        self.chapter_label = ""
        self._checkpoint = None
        self.apply_settings()

    def apply_settings(self):
        T.bell = self.settings.get("sound") == "on"
        T.reduce_flash = self.settings.get("flash") != "on"

    # ===================================================== story API
    def page(self, hud=True):
        self.ui.page(hud)

    def say(self, text, **kw):
        self.ui.say(text, **kw)

    def pause(self, s):
        self.ui.pause(s)

    def wait(self):
        self.ui.wait()

    def choose(self, options, timeout=None, default=None):
        if timeout:
            timeout *= TIME_FACTOR.get(self.settings.get("difficulty"), 1.0)
        return self.ui.choose(options, timeout, default)

    def ask(self, prompt, **kw):
        return self.ui.ask(prompt, **kw)

    def time_factor(self):
        f = TIME_FACTOR.get(self.settings.get("difficulty"), 1.0)
        if self.s.sanity < 30:
            f *= 0.85
        if self.dark():
            f *= 0.9
        return f

    def dark(self):
        return self.has_flag("dark")

    def flag(self, name):
        if name not in self.s.flags:
            self.s.flags.append(name)

    def has_flag(self, name):
        return name in self.s.flags

    def has(self, item):
        return item in self.s.items

    def give(self, item, label, silent=False):
        if item not in self.s.items:
            self.s.items.append(item)
        if not silent:
            self.ui.notify("OBTAINED", label)

    def mind(self, delta, reason=None, quiet=False):
        if delta < 0:
            delta = min(-1, int(round(delta * MIND_MULT.get(self.settings.get("difficulty"), 1.0))))
        self.s.sanity = max(0, min(100, self.s.sanity + delta))
        if not quiet:
            self.ui.draw_hud()
            self.ui.tag("%+d mind" % delta, 140 if delta < 0 else 120)
        if self.s.sanity <= 0:
            raise Death(reason or "Your mind went into the dark and did not come back. Somewhere, it is still counting.")

    def hurt(self, n=1, reason=None):
        self.s.health = max(0, self.s.health - n)
        fx.vignette(160, 2)
        self.ui.draw_hud()
        self.ui.tag("-%d ♥" % n, 196)
        if self.s.health <= 0:
            raise Death(reason or "Your heart stopped. Your seat didn't.")

    def heal(self, n=1):
        before = self.s.health
        self.s.health = min(self.s.max_health, self.s.health + n)
        if self.s.health > before:
            self.ui.draw_hud()
            self.ui.tag("+%d ♥" % (self.s.health - before), 203)

    def drain(self, n):
        s = self.s
        if s.battery <= 0 and not s.spares:
            return
        s.battery = max(0, s.battery - n)
        if s.battery == 0:
            if s.spares > 0:
                s.spares -= 1
                s.battery = 100
                self.ui.draw_hud()
                self.say("{y}Your torch browns out and dies. Fumbling in the dark, you thumb in one of the old batteries from the ticket office. Light again.{/}")
            else:
                self.flag("dark")
                self.ui.draw_hud()
                self.say("{r}Your torch flickers, browns out, and dies. The dark comes in close, like it was waiting for you.{/}")
                self.mind(-10)
        self.ui.draw_hud()

    def find_page(self, n):
        if n not in self.s.pages:
            self.s.pages.append(n)
        title, lines = story.PAGES[n]
        fx.paper(title, lines)
        self.page()
        self.ui.notify("FOUND", "LAMPMAN'S NOTEBOOK  %d / 3" % len(self.s.pages), color=223)

    def chapter_card(self, i):
        numeral, kicker, title = story.CHAPTERS[i]
        self.chapter_label = ("PROLOGUE" if i == 0 else "CH.%s" % numeral) + " · " + title
        fx.chapter_card(numeral, kicker, title)

    def os_user(self):
        try:
            name = getpass.getuser() or ""
        except Exception:
            return None
        name = name.strip()
        if not name.isalpha() or not (3 <= len(name) <= 14):
            return None
        if name.lower() in NOT_NAMES or name.lower() == self.s.name.lower():
            return None
        return name.upper()

    # ===================================================== flow
    def run(self):
        self.size_check()
        if not self.settings.get("warned"):
            self.warning()
        while True:
            cp = self.save.checkpoint()
            found = len(self.save.endings)
            items = [("new", "New game")]
            if cp:
                items.append(("cont", "Continue   " + fg(240) + story.CHAPTERS[cp.chapter][2].title()))
            items += [("settings", "Settings"),
                      ("endings", "Endings   " + fg(240) + "%d / %d" % (found, len(story.ENDINGS))),
                      ("quit", "Quit")]
            menu = [(str(i + 1), label) for i, (_, label) in enumerate(items)]
            k = fx.title_screen(menu, footer="best played in the dark, full screen, alone")
            if k in ("q", "Q", "ESC"):
                return
            if not (len(k) == 1 and k.isdigit() and 1 <= int(k) <= len(items)):
                continue
            act = items[int(k) - 1][0]
            if act == "new":
                self.new_game()
            elif act == "cont":
                self.play(cp)
            elif act == "settings":
                self.settings_menu()
            elif act == "endings":
                self.endings_menu()
            else:
                return

    def new_game(self):
        self.s = State()
        self.chapter_label = ""
        self.page(hud=False)
        cols, rows = T.size()
        self.ui.row = max(3, rows // 2 - 6)
        self.say("{d}KALVARI GHAT RAILWAY  ·  PASSENGER MANIFEST  ·  14.08.87{/}", instant=True)
        self.pause(0.6)
        name = self.ask("Write your name in the manifest.", maxlen=12, default="")
        name = " ".join(w.capitalize() for w in name.split())
        if not name:
            name = "Traveller"
        self.s.name = name
        self.say("{d}Thank you, {/}{w}%s{/}{d}. Your seat has been reserved.{/}" % name)
        self.pause(1.4)
        self.play(self.s)

    def play(self, state):
        self.s = state
        while True:
            start = self.s.chapter
            try:
                for i in range(start, len(story.CHAPTER_FUNCS)):
                    self.s.chapter = i
                    if i >= 2 and ("rest%d" % i) not in self.s.flags:
                        # a breath between chapters
                        self.s.flags.append("rest%d" % i)
                        self.s.sanity = min(100, self.s.sanity + 6)
                    self.save.set_checkpoint(self.s)
                    self._checkpoint = self.s.to_dict()
                    story.CHAPTER_FUNCS[i](self)
                return
            except Death as d:
                if self.death_screen(d.reason) == 0:
                    self.s = State.from_dict(self._checkpoint)
                    # waking up again leaves you a little stronger than the checkpoint
                    self.s.health = max(self.s.health, 2)
                    self.s.sanity = max(self.s.sanity, 45)
                    continue
                return
            except Ending as e:
                self.save.set_checkpoint(None)
                first = e.key not in self.save.endings
                self.save.add_ending(e.key)
                self.ending_screen(e.key, first)
                return
            except QuitToTitle:
                return

    # ===================================================== screens
    def death_screen(self, reason):
        fx.static(0.7)
        T.clear()
        cols, rows = T.size()
        lines = lettering.PASSENGER_213
        w = max(len(l) for l in lines)
        c0 = max(1, (cols - w) // 2 + 1)
        r0 = max(2, rows // 2 - 7)
        end = T.now() + 1.2
        while T.now() < end:
            fx.blit([" " * (w + 8)] * (len(lines) + 2), r0 - 1, max(1, c0 - 4))
            fx.blit(lines, r0 + random.randint(-1, 1), c0 + random.randint(-3, 3), fg(random.choice((124, 160, 196))))
            T.sleep(0.05)
        fx.blit([" " * (w + 8)] * (len(lines) + 2), r0 - 1, max(1, c0 - 4))
        fx.blit(lines, r0, c0, fg(160))
        self.ui.hud = False
        self.ui.row = r0 + len(lines) + 2
        self.say(reason.replace("@NAME", self.s.name), style="d")
        self.say("{d}The 11:47 has a new passenger.{/}")
        return self.ui.choose(["Wake up.  " + "{D}(retry from the start of this chapter){/}", "Return to the title."])

    def ending_screen(self, key, first):
        idx = [e[0] for e in story.ENDINGS].index(key)
        name, tag = story.ENDINGS[idx][1], story.ENDINGS[idx][2]
        fx.static(0.4)
        sub = "ENDING  %d / %d" % (idx + 1, len(story.ENDINGS))
        if tag:
            sub += "  ·  " + tag.upper()
        fx.title_card(lettering.ENDING_TITLES[key], sub=sub, hold_s=3.0)
        self.page(hud=False)
        cols, rows = T.size()
        self.ui.row = max(3, rows // 2 - 5)
        fx.blit(lettering.THE_END, self.ui.row, max(1, (cols - max(len(l) for l in lettering.THE_END)) // 2 + 1), fg(124))
        self.ui.row += len(lettering.THE_END) + 2
        found = len(self.save.endings)
        self.say("{w}THE HOLLOW LINE{/}   {d}·   a terminal horror{/}", instant=True)
        self.say("You found {w}%s{/}%s  Endings discovered: {w}%d / %d{/}." % (
            name, " for the first time." if first else ".", found, len(story.ENDINGS)))
        if found < len(story.ENDINGS):
            self.say("{d}The 11:47 runs every night. Some of its passengers got off at different stations.{/}")
        else:
            self.say("{y}You've seen every ending. The line is quiet now. Thank you for riding.{/}")
        self.wait()

    def endings_menu(self):
        self.page(hud=False)
        self.say("{w}ENDINGS{/}")
        any_found = bool(self.save.endings)
        for key, name, tag, hint in story.ENDINGS:
            if key in self.save.endings:
                extra = ("  {d}(" + tag + "){/}") if tag else ""
                self.say("{y}◆{/}  {w}" + name + "{/}" + extra, gap=0)
            else:
                h = ("   {D}" + hint + "{/}") if any_found else ""
                self.say("{D}◇  ? ? ?{/}" + h, gap=0)
        self.ui.row += 1
        if not any_found:
            self.say("{d}Hints appear here once you've reached your first ending.{/}")
        self.wait()

    def settings_menu(self):
        order = [
            ("speed", "Text speed", ["slow", "normal", "fast", "instant"]),
            ("difficulty", "Difficulty", ["story", "normal", "nightmare"]),
            ("flash", "Flashing", ["on", "reduced"]),
            ("sound", "Sound (terminal bell)", ["on", "off"]),
        ]
        while True:
            self.page(hud=False)
            self.say("{w}SETTINGS{/}   {d}press a number to change it, 5 to go back{/}")
            for i, (k, label, vals) in enumerate(order):
                self.say("{d}[%d]{/}  %-22s {y}%s{/}" % (i + 1, label, self.settings[k].upper()), gap=0, instant=True)
            self.say("{d}[5]{/}  Back", instant=True)
            self.say("{D}Story mode gives more time on quick-time events and softens sanity loss.  "
                     "Reduced flashing tones down jump-scare strobes.{/}", instant=True)
            T.flush_input()
            k = T.key()
            if k in ("1", "2", "3", "4"):
                key, _, vals = order[int(k) - 1]
                cur = self.settings[key]
                self.settings[key] = vals[(vals.index(cur) + 1) % len(vals)] if cur in vals else vals[0]
                self.apply_settings()
                self.save.write()
            elif k in ("5", "ESC", "q", "Q", "\n"):
                return

    def warning(self):
        self.page(hud=False)
        cols, rows = T.size()
        self.ui.row = max(3, rows // 2 - 6)
        self.say("{r}THE HOLLOW LINE{/}", instant=True)
        self.say("A horror story for your terminal. It has jump scares, flashing lights, and a few moments where a timer is running and you won't be warned in advance.")
        self.say("{d}If flashing is a problem for you, turn it down in Settings. Press keys to answer. Press any key to skip text. ESC pauses.{/}")
        self.say("{d}Lights off. Headphones on if your terminal beeps. Full screen.{/}")
        self.settings["warned"] = True
        self.save.write()
        self.wait()

    def size_check(self):
        if not T.interactive:
            return
        T.flush_input()
        while True:
            cols, rows = T.size()
            if cols >= 80 and rows >= 24:
                return
            T.clear()
            fx.ctext(max(1, rows // 2 - 1), "Make this window bigger.", fg(231) + BOLD)
            fx.ctext(max(1, rows // 2 + 1), "Now %d x %d.  Needs at least 80 x 24 (100 x 30 is better)." % (cols, rows), fg(245))
            fx.ctext(max(1, rows // 2 + 3), "Press any key to play anyway.", fg(240))
            T.flush()
            if T.key(0.4) is not None:
                return
