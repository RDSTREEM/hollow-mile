from collections.abc import Callable

from engine.world import World
from engine.parser import Command
from engine.result import Result

Handler = Callable[[World, Command], Result]


class ActionRegistry:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def register(self, name: str, handler: Handler) -> None:
        self.handlers[name] = handler

    def execute(self, world: World, command: Command) -> Result:
        handler = self.handlers.get(command.action)

        if handler is None:
            return Result(
                text="The command was not understood.",
                success=False,
            )

        return handler(world, command)


def find_entity(world: World, query: str):

    room = world.curr_room

    if room is None:
        return None, False

    query = " ".join(query.lower().split())

    matches = []

    for _id in room.entities:
        entity = world.get_entity(_id)

        names = [entity.name, *entity.aliases]

        for name in names:
            normalized_name = " ".join(name.lower().split())

            if query == normalized_name or normalized_name in query:
                matches.append(entity)
                break

    if len(matches) == 1:
        return matches[0], False

    if len(matches) > 1:
        return None, True

    return None, False


def look(world: World, command: Command) -> Result:
    room = world.curr_room

    if room is None:
        return Result(text="You have no current location.", success=False)

    output = [room.name, "", room.desc]

    if room.entities:
        output.extend(
            ["", "You notice: "]
        )  # todo: should change this to be changable by the metadata yaml

        for _id in room.entities:
            entity = world.get_entity(_id)
            output.append(f" - {entity.name}")

    if room.exits:
        output.extend(["", "Available exits: "])

        for d in room.exits:
            output.append(f" - {d}")

    return Result(
        text="\n".join(output),
        suggestions=[f"Go {d}" for d in room.exits],
    )
