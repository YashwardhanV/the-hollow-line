# THE HOLLOW LINE

*A horror story for your terminal.*

A standalone, choice-driven Python horror game with seven chapters, six endings,
timed decisions, animated terminal scenes, and chapter checkpoints. Built entirely
with the Python standard library for Windows, macOS, and Linux.

At 3:17 AM your little brother calls you from a railway tunnel that was sealed in 1987. Nobody speaks. Something counts. The last number is in your voice.

You drive up to Kalvari Ghat to bring him home.

---

## Run it

Needs **Python 3.7+**. Nothing to install, no packages.

| System | How |
|---|---|
| Windows | Double-click `run_windows.bat`, or in a terminal: `python play.py` |
| macOS / Linux | `./run_mac_linux.sh`, or `python3 play.py` |

Download and extract the repository ZIP from GitHub's **Code** menu, then open a
terminal in the extracted folder and run the command for your system. You can
also launch it as a module with `python -m hollowline`.

Make the window **full screen** (at least 80×24, 100×30 or bigger is best). Turn the lights off.

Use a real terminal: Windows Terminal, PowerShell, macOS Terminal / iTerm2, any Linux terminal. IDLE and some IDE "run" panes can't read single keypresses, so the game won't work properly there.

## Controls

- **Number keys** pick a choice. Some choices have a timer. If it runs out, you hesitate, and hesitating is a choice too.
- **Any key** skips the typewriter text and turns the page (`▼`).
- **ESC** at a choice opens the quit prompt. Progress is saved at the start of every chapter.
- Quick-time events tell you what to press. Not every prompt on screen is telling you the truth.

## What's inside

- 7 chapters, roughly 25 to 35 minutes for one run
- 6 endings (one true ending), tracked between runs, with hints after your first
- Choices that matter later: what you take, what you answer, what you count
- Real-time scenes: quick-time keys, breath control, a lantern you have to move between, and moments where the right move is not pressing anything at all
- Hearts, sanity and torch battery. Low sanity starts to corrupt the text you're reading
- Animations: rain and lightning, a sweeping torch beam, a live-stream replay, a heartbeat monitor, a split-flap departure board, a scrolling train, a headlight bearing down on you, and a few things that jump

## Settings

From the title screen: text speed, difficulty (Story / Normal / Nightmare), reduced flashing, and the terminal bell used on jump scares.

Command-line flags:

```
python play.py --speed fast          slow | normal | fast | instant
python play.py --difficulty story    story | normal | nightmare
python play.py --no-flash            tone down strobe effects
python play.py --mute                no terminal bell
python play.py --reset               wipe saved progress and endings
```

Save file: `~/.hollow_line_save.json` (your user folder on Windows).

## Troubleshooting

- **Boxes or question marks instead of shapes:** your terminal font is missing block characters. Use Windows Terminal, or a font like Cascadia Mono, Consolas, Menlo or DejaVu Sans Mono.
- **No colours / strange codes on old Windows:** use Windows 10 or newer and Windows Terminal.
- **`python` not found on Windows:** install Python from python.org and tick "Add Python to PATH", or run `py play.py`.
- **Permission denied on macOS / Linux:** run `sh run_mac_linux.sh`, or enable the launcher with `chmod +x run_mac_linux.sh`.

## Development

No dependency installation is needed. Check syntax and both entry points with:

```sh
python -m compileall -q hollowline play.py
python play.py --help
python -m hollowline --help
```

GitHub Actions runs these checks and imports the game modules on Windows,
macOS, and Linux. Interactive gameplay should be tested in a real terminal.

Content: jump scares, flashing light effects, mild body horror, death.
