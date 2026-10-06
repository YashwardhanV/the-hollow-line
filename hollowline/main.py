"""Entry point: python play.py  (or python -m hollowline)."""
import argparse
import os
import sys
import traceback


def main():
    if sys.version_info < (3, 7):
        print("THE HOLLOW LINE needs Python 3.7 or newer.")
        sys.exit(1)
    ap = argparse.ArgumentParser(description="THE HOLLOW LINE - a horror story for your terminal.")
    ap.add_argument("--speed", choices=["slow", "normal", "fast", "instant"], help="text speed")
    ap.add_argument("--difficulty", choices=["story", "normal", "nightmare"])
    ap.add_argument("--no-flash", action="store_true", help="tone down flashing effects")
    ap.add_argument("--mute", action="store_true", help="no terminal bell")
    ap.add_argument("--reset", action="store_true", help="delete saved progress and endings")
    args = ap.parse_args()

    from .state import SAVE_PATH, Save
    if args.reset:
        try:
            os.remove(SAVE_PATH)
            print("Save deleted.")
        except OSError:
            print("No save to delete.")
        return

    from .term import T
    from .game import Game

    save = Save()
    if args.speed:
        save.settings["speed"] = args.speed
    if args.difficulty:
        save.settings["difficulty"] = args.difficulty
    if args.no_flash:
        save.settings["flash"] = "reduced"
    if args.mute:
        save.settings["sound"] = "off"

    crashed = None
    T.start()
    try:
        Game(save).run()
    except KeyboardInterrupt:
        pass
    except Exception:
        crashed = traceback.format_exc()
    finally:
        T.stop()
    if crashed:
        print(crashed)
        print("THE HOLLOW LINE crashed. Your progress from the start of the chapter is saved.")
    else:
        print("\n  The line goes quiet.  Thanks for riding THE HOLLOW LINE.\n")


if __name__ == "__main__":
    main()
