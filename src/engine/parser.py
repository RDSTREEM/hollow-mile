from dataclasses import dataclass


@dataclass
class Command:
    action: str
    target: str | None = None
    secondary_target: str | None = None
    raw: str = ""


class CommandParser:
    ACTION_ALIASES = {
        "look": "look",
        "l": "look",
        "examine": "examine",
        "inspect": "examine",
        "x": "examine",
        "go": "go",
        "walk": "go",
        "move": "go",
        "inventory": "inventory",
        "inv": "inventory",
        "i": "inventory",
        "take": "take",
        "pick": "take",
        "grab": "take",
        "get": "take",
        "drop": "drop",
        "use": "use",
        "talk": "talk",
        "speak": "talk",
        "answer": "answer",
        "solve": "solve",
        "save": "save",
        "load": "load",
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

        action = self.ACTION_ALIASES.get(words[0])

        if action is None:
            return Command("unknown", target=normalized, raw=raw)

        remaining = words[1:]

        if action == "use":
            if "on" not in remaining:
                return Command("unknown", target=normalized, raw=raw)

            s = remaining.index("on")

            item = self._clean_target(" ".join(remaining[:s]))

            target = self._clean_target(" ".join(remaining[s + 1 :]))

            if not item or not target:
                return Command("unknown", target=normalized, raw=raw)

            return Command("use", target=item, secondary_target=target, raw=raw)

        target = self._clean_target(" ".join(remaining))

        # if action == "look":
        # if target:
        # return Command("examine", target=target, raw=raw)

        if action in {"inventory", "help", "look"}:
            return Command(action, target=target or None, raw=raw)

        if action in {"take", "drop", "examine", "answer"}:
            if action == "take" and target.startswith("up "):
                target = self._clean_target(target[3:])

            if target:
                return Command(action, target=target, raw=raw)

        if action == "go":
            if target and len(target.split()) == 1:
                return Command("go", target=target, raw=raw)

            return Command("unknown", target=normalized, raw=raw)

        if action == "answer":
            return Command("answer", target=target, raw=raw)

        if action == "talk" and target.startswith("to "):
            target = self._clean_target(target[3:])

        return Command(action, target=target, raw=raw)

    def _clean_target(self, target):
        words = target.split()

        while words and words[0] in self.ARTICLES:
            words.pop(0)

        return " ".join(words)
