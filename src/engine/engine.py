from pathlib import Path

from engine.loader import Story
from engine.parser import CommandParser, Command
from engine.inventory import Inventory
from engine.state import GameState
from engine.actions import create_registry, look
from engine.result import Result
from engine.events import Bus
from engine.save_manager import SaveManager
from engine.dialogue import DialogueManager


class Engine:
    def __init__(self, story: Story):
        self.story = story
        self.world = story.world

        self.inv = Inventory()
        self.state = GameState()

        self.parser = CommandParser()

        self.dialogue = DialogueManager(self.world, self.state, self.story.dialogues)

        self.actions = create_registry(self.dialogue)

        self.events = Bus()

        self.path = Path("saves/slot1.json")

    def start(self) -> Result:
        return look(self.world, self.inv, self.state, Command(action="look"))

    def save(self) -> Result:
        try:
            SaveManager.save(self, self.path)
        except (OSError, TypeError, ValueError) as e:
            return Result(text=f"Could not save the game: {e}", success=False)

        return Result(text=f"Game saved successfully")

    def load(self) -> Result:
        try:
            SaveManager.load(self, self.path)
        except (OSError, TypeError, ValueError, KeyError) as e:
            return Result(text=f"Could not load the game: {e}", success=False)

        return Result(
            text=f"Game loaded successfully", metadata={"location": self.world.curr}
        )

    def execute(self, raw: str) -> Result:
        cmd = self.parser.parse(raw)

        if cmd.action == "empty":
            return Result(text="")

        if cmd.action == "save":
            return self.save()

        if cmd.action == "load":
            return self.load()

        if self.dialogue.active:
            res = self.dialogue.choose(raw)
            self._emit_events(res)
            return res

        res = self.actions.execute(self.world, self.inv, self.state, cmd)

        self._emit_events(res)

        return res

    def _emit_events(self, res: Result):
        for event in res.metadata.get("events", []):
            self.events.emit(
                event,
                {
                    "location": self.world.curr,
                    "metadata": res.metadata,
                },
            )
