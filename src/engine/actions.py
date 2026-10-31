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


def go(world: World, command: Command) -> Result:
    if not command.target:
        return Result(text="Go where?", success=False)

    try:
        dest = world.move(command.target)
    except (ValueError, KeyError) as e:
        return Result(text=str(e), success=False)

    return Result(
        text=f"You travel {command.target}. \n\n{dest.name}\n{dest.desc}",
        suggestions=[f"Go {d}" for d in dest.exits],
        metadata={"location": dest._id},
    )


def examine(world: World, command: Command) -> Result:
    if not command.target:
        return Result(text="What would you like to examine?", success=False)

    entity, ambigous = find_entity(world, command.target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if entity is None:
        return Result(text=f"You dont see {command.target} here", success=False)

    return Result(text=f"{entity.name}\n\n{entity.desc}")


def inventory(world: World, command: Command) -> Result:
    return Result(
        text="Your inventory is empty."
    )  # for now, i would impolement taking and droping later


def help_action(world: World, command: Command) -> Result:
    return Result(
        text=(
            "AVIALABLE COMMANDS\n\n"
            "look                              Describe your surroundings\n"
            "go <direction>                    Move through an exit\n"
            "north/south                       Quick movment\n"
            "examine <object>                  Examine something\n"
            "look at <object>                  Examine something\n"
            "inventory                         Check your inventory\n"
            "help                              Displays this help\n"
        )
    )


def create_registry() -> ActionRegistry:
    reg = ActionRegistry()

    reg.register("look", look)
    reg.register("go", go)
    reg.register("examine", examine)
    reg.register("inventory", inventory)
    reg.register("help", help_action)

    return reg
