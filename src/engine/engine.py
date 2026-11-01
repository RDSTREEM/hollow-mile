from engine.loader import Story
from engine.parser import CommandParser, Command
from engine.inventory import Inventory
from engine.state import GameState
from engine.actions import create_registry, look
from engine.result import Result


class Engine:
    def __init__(self, story: Story):
        self.story = story
        self.world = story.world

        self.inv = Inventory()
        self.state = GameState()

        self.parser = CommandParser()
        self.actions = create_registry()

    def start(self) -> Result:
        return look(self.world, self.inv, self.state, Command(action="look"))

    def execute(self, raw: str) -> Result:
        cmd = self.parser.parse(raw)

        if cmd.action == "empty":
            return Result(text="")

        return self.actions.execute(self.world, self.inv, self.state, cmd)
