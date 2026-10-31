from dataclasses import dataclass


@dataclass
class Command:
    action: str
    target: str | None = None
    raw: str = ""


class CommandParser:
    ACTION_ALIASES = {
        "look": "look",
        "l": "look",
        "examime": "examine" "inspect:" "examine",
        "x": "examine",
        "go": "go",
        "walk": "go",
        "move": "go",
        "invetory": "inventory",
        "inv": "inventory",
        "i": "inventory",
        "help": "help",
        "?": "help",
    }

    DIRECTIONS = {"north", "south", "east", "west", "up", "down"}

    ARTICLES = {"the", "a", "an"}

    def parse(self, text: str) -> Command:
        raw = text.strip()
        normalized = " ".join(raw.lower().split())

        if not normalized:
            return Command("empty", raw=raw)

        words = normalized.split()

        if words[0] in self.DIRECTIONS and len(words) == 1:
            return Command("go", target=words[0], raw=raw)

        if normalized.startswith("look at"):
            target = normalized[8:].strip()

            return Command(
                "examine",
                target=self._clean_target(target),
                raw=raw,
            )

        if normalized.startswith("look at"):
            return Command("look", raw=raw)

        action = self.ACTION_ALIASES.get(words[0])

        if action is None:
            return Command("unknown", target=normalized, raw=raw)

        remaining = words[1:]

        while remaining and remaining[0] in self.ARTICLES:
            remaining.pop(0)

        target = " ".join(remaining) or None

        if action == "look":
            if target:
                return Command("examine", target=target, raw=raw)

        if action == "go":
            if target and len(target.split()) == 1:
                return Command("go", target=target, raw=raw)

            return Command("unknown", target=normalized, raw=raw)

        if action == "examine" and not target:
            return Command("unknown", target=normalized, raw=raw)

        if action in {"inventory", "help"}:
            return Command(action, raw=raw)

        return Command(action, target=target, raw=raw)

    def _clean_target(self, target):
        words = target.split()

        while words and words[0] in self.ARTICLES:
            words.pop(0)

        return " ".join(words)
