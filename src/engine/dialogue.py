from typing import Any

from engine.conditions import Evaluator
from engine.result import Result


class DialogueManager:
    def __init__(self, world, state, dialogues: dict[str, Any]) -> None:
        self.world = world
        self.state = state
        self.dialogues = dialogues

        self.active: str | None = None
        self.curr: str | None = None

    def _visible_entities(self):
        location = self.world.current_location
        evaluator = Evaluator(self.state)

        for _id in location.entities:
            entity = self.world.get_entity(_id)

            if entity and evaluator.eval(entity.visible_when):
                yield entity

    def _list_characters(self) -> Result:
        characters = [
            entity.name
            for entity in self._visible_entities()
            if entity._id in self.dialogues
        ]

        if not characters:
            return Result(text="There is nobody here to talk to")

        return Result(text=f"You can talk to {', '.join(characters)}")

    def start(self, target: str | None) -> Result:
        if not target:
            return self._list_characters()
        entity = next(
            (
                entity
                for entity in self._visible_entities()
                if entity._id.lower() == target or entity.matches(target)
            ),
            None,
        )

        if entity is None:
            return Result(text=f"You cannot see anyone called {target}", success=False)

        dialogue = self.dialogues.get(entity._id)

        if not dialogue:
            return Result(text=f"{entity.name} has nothing to say")

        self.active = entity._id
        self.curr = dialogue.get("start")

        if not self.curr:
            self.end()
            return Result(text=f"{entity.name} has no starting node.", success=False)

        return self._show_node()

    def _get_current_definition(self):
        if self.active is None:
            raise ValueError("later")
        d = self.dialogues[self.active]
        return d["nodes"][self.curr]

    def _choices(self, node: dict) -> list[dict]:
        evaluator = Evaluator(self.state)
        c = []

        for choice in node.get("choices", []):
            cond = choice.get("cond")
            if evaluator.eval(cond):
                c.append(choice)

        return c

    def _apply_effects(self, definition: dict) -> list[str]:
        effects = {**definition.get("effects", {}), **definition}

        for name, val in effects.get("set_flags", {}).items():
            self.state.set_flag(name, val)

        for name, val in effects.get("set_variables", {}).items():
            self.state.set_var(name, val)

        for name, amt in effects.get("increment_variables", {}).items():
            self.state.inc_var(name, amt)

        emmited = effects.get("emit", [])

        if isinstance(emmited, str):
            emmited = [emmited]

        return emmited

    def _show_node(self) -> Result:
        node = self._get_current_definition()
        events = self._apply_effects(node)

        lines = [node.get("text", "")]
        choices = self._choices(node)

        for i, c in enumerate(choices, start=1):
            lines.append(f"{i}. {c['text']}")

        if not choices:
            lines.append("")
            lines.append("The conversation has ended.")
            self.end()

        return Result(
            text="\n".join(line for line in lines if line is not None),
            metadata={"events": events},
        )

    def choose(self, raw: str) -> Result:
        if raw.lower() in {"leave", "bye", "goodbye", "cancel", "exit"}:
            self.end()
            return Result(text="You ended the conversation")

        if not raw.isdigit():
            return Result(
                text="Choose a numbered dialogue option, or type 'leave'", success=False
            )

        node = self._get_current_definition()
        choices = self._choices(node)

        idx = int(raw) - 1

        if idx < 0 or idx >= len(choices):
            return Result(text="That is not a valid choice", success=False)

        choice = choices[idx]
        events = self._apply_effects(choice)

        lines = [f"> {choice['text']}"]

        response = choice.get("response")
        if response:
            lines.append(response)

        next_node = choice.get("next")

        if next_node is None:
            self.end()
            lines.append("")
            lines.append("The conversation has ended")

            return Result(text="\n".join(lines), metadata={"events": events})

        if self.active is None:
            raise ValueError("later")
        d = self.dialogues[self.active]

        if next_node not in d["nodes"]:
            self.end()
            return Result(
                text="Dialogue error: the next node does not exist.",
                success=False,
                metadata={"events": events},
            )
        self.curr = next_node
        res = self._show_node()

        lines.append("")
        lines.append(res.text)

        events.extend(res.metadata.get("events", []))

        return Result(text="\n".join(lines), metadata={"events": events})

    def end(self):
        self.active = None
        self.curr = None
