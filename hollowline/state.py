"""Game state, settings, checkpoints and discovered endings (saved as JSON)."""
import copy
import json
import os

SAVE_PATH = os.path.join(os.path.expanduser("~"), ".hollow_line_save.json")

DEFAULT_SETTINGS = {
    "speed": "normal",       # slow / normal / fast / instant
    "difficulty": "normal",  # story / normal / nightmare
    "flash": "on",           # on / reduced
    "sound": "on",           # terminal bell on jump scares
    "warned": False,
}


class State:
    def __init__(self, name="Traveller"):
        self.name = name
        self.health = 3
        self.max_health = 3
        self.sanity = 100
        self.battery = 100
        self.spares = 0
        self.items = []
        self.flags = []
        self.pages = []
        self.chapter = 0

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, d):
        s = cls()
        for k, v in d.items():
            if hasattr(s, k):
                setattr(s, k, copy.deepcopy(v))
        return s


class Save:
    def __init__(self, path=SAVE_PATH):
        self.path = path
        self.data = {"settings": dict(DEFAULT_SETTINGS), "endings": [], "checkpoint": None}
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                d = json.load(fh)
            self.data["settings"].update(d.get("settings", {}))
            self.data["endings"] = list(d.get("endings", []))
            self.data["checkpoint"] = d.get("checkpoint")
        except (OSError, ValueError):
            pass

    def write(self):
        try:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(self.data, fh, indent=1)
        except OSError:
            pass

    @property
    def settings(self):
        return self.data["settings"]

    @property
    def endings(self):
        return self.data["endings"]

    def add_ending(self, key):
        if key not in self.data["endings"]:
            self.data["endings"].append(key)
        self.write()

    def set_checkpoint(self, state):
        self.data["checkpoint"] = state.to_dict() if state else None
        self.write()

    def checkpoint(self):
        cp = self.data.get("checkpoint")
        return State.from_dict(cp) if cp else None


class Death(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason


class Ending(Exception):
    def __init__(self, key):
        Exception.__init__(self, key)
        self.key = key
