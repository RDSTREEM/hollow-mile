from collections.abc import Callable

from engine.world import World
from engine.parser import Command
from engine.result import Result
from engine.inventory import Inventory
from engine.state import GameState
from engine.conditions import Evaluator

Handler = Callable[[World, Inventory, GameState, Command], Result]


class ActionRegistry:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def register(self, name: str, handler: Handler) -> None:
        self.handlers[name] = handler

    def execute(
        self, world: World, inv: Inventory, state: GameState, command: Command
    ) -> Result:
        handler = self.handlers.get(command.action)

        if handler is None:
            return Result(
                text="The command was not understood.",
                success=False,
            )

        return handler(world, inv, state, command)


def find_entity(world: World, query: str):

    room = world.curr_room

    if room is None:
        return None, False

    query = " ".join(query.lower().split())

    matches = []

    for _id in room.entities:
        entity = world.get_entity(_id)

        names = [entity.name, *entity.aliases]

        if any(" ".join(name.lower().split()) in query for name in names):
            matches.append(entity)

    if len(matches) == 1:
        return matches[0], False

    return None, len(matches) > 1


def find_inv_entity(world: World, inv: Inventory, query: str):
    query = " ".join(query.lower().split())
    matches = []

    for _id in inv.items:
        entity = world.get_entity(_id)

        if entity.matches(query):
            matches.append(entity)

    if len(matches) == 1:
        return matches[0], False

    return None, len(matches) > 1


def look(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
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


def go(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
    if not command.target:
        return Result(text="Go where?", success=False)

    try:
        dest = world.move(command.target)
    except (ValueError, KeyError) as e:
        return Result(text=str(e), success=False)

    return Result(
        text=(f"You travel {command.target}.\n\n{dest.name}\n\n{dest.desc}"),
        suggestions=[f"Go {d}" for d in dest.exits],
        metadata={"location": dest._id},
    )


def examine(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
    if not command.target:
        return Result(text="What would you like to examine?", success=False)

    entity, ambigous = find_entity(world, command.target)

    if not entity and not ambigous:
        entity, ambigous = find_inv_entity(world, inv, command.target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if entity is None:
        return Result(text=f"You dont see {command.target} here", success=False)

    desc = entity.desc
    variants = entity.interactions.get("descriptions", {})
    evaluator = Evaluator(state)

    for variant in variants:
        condition = variant.get("condition")

        if evaluator.eval(condition):
            desc = variant.get("text", desc)
            break

    return Result(text=f"{entity.name}\n\n{desc}")


def take(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
    if not command.target:
        return Result(text="What would you like to take?", success=False)

    entity, ambigous = find_entity(world, command.target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if entity is None:
        return Result(text=f"You dont see {command.target} here", success=False)

    if not entity.portable:
        return Result(text=f"You can't take the {entity.name}")

    room = world.curr_room

    room.remove_entity(entity._id)
    inv.add(entity._id)

    return Result(text=f"You picked up the {entity.name}")


def drop(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
    if not command.target:
        return Result(text="What would you like to drop?", success=False)

    entity, ambigous = find_inv_entity(world, inv, command.target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if entity is None:
        return Result(text=f"You are not carying {command.target}", success=False)

    inv.remove(entity._id)
    world.curr_room.add_entity(entity._id)

    return Result(
        text=f"You dropped the {entity.name}", metadata={"inventory_changed": True}
    )


def use(world: World, inv: Inventory, state: GameState, command: Command) -> Result:
    if not command.target or not command.secondary_target:
        return Result(text="Usage: use <item> on <targets>", success=False)

    item, ambigous = find_inv_entity(world, inv, command.target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if item is None:
        return Result(text=f"You aren't carrying {command.target}", success=False)

    target, ambigous = find_entity(world, command.secondary_target)

    if ambigous:
        return Result(
            text="That description matches multiple objects. Be more specific.",
            success=False,
        )

    if target is None:
        return Result(text=f"You don't see '{command.secondary_target}' here.")

    interactions = target.interactions.get("use", {})

    response = interactions.get(item._id)

    if response is None:
        return Result(
            text=f"Using the {item.name} on the {target.name} has no effect.",
            success=False,
        )

    if isinstance(response, str):
        response = {"text": response}
    if not isinstance(response, dict):
        return Result(text="This interaction has an invalid defintion.", success=False)

    evaluator = Evaluator(state)
    cond = response.get("condition")

    if not evaluator.eval(cond):
        return Result(
            text=response.get("failure_text", "Nothing happens."), success=False
        )

    text = response.get("text", "Nothing happens.")

    for name, val in response.get("set_flags", {}).items():
        state.set_flag(name, val)

    return Result(
        text=text.strip(),
        metadata={"interaction": "use", "item": item._id, "target": target._id},
    )


def inventory(
    world: World, inv: Inventory, state: GameState, command: Command
) -> Result:
    if inv.is_empty():
        return Result(text="Your inventory is empty.")

    output = ["You are carying: "]

    for _id in inv.items:
        entity = world.get_entity(_id)
        output.append(f" - {entity.name}")

    return Result(text="\n".join(output))


def help_action(
    world: World, inv: Inventory, state: GameState, command: Command
) -> Result:
    return Result(
        text=(
            "AVIALABLE COMMANDS\n\n"
            "look                              Describe your surroundings\n"
            "go <direction>                    Move through an exit\n"
            "north/south                       Quick movment\n"
            "examine <object>                  Examine something\n"
            "look at <object>                  Examine something\n"
            "take <object>                     Pick up an object"
            "drop <object>                     Drop an object\n"
            "use <item> on <target>            Use an item on something\n"
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
    reg.register("drop", drop)
    reg.register("use", use)
    reg.register("take", take)

    return reg
