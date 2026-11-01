import json
from pathlib import Path
from typing import Any
from engine import Engine


class SaveManager:
    FORMAT_VERSION = 1

    @staticmethod
    def save(engine: Engine, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "format_version": SaveManager.FORMAT_VERSION,
            "story_id": engine.story.metadata.get("id"),
            "current_room": engine.world.curr,
            "inventory": engine.inv.items,
            "room_entities": {
                _id: room.entities for _id, room in engine.world.rooms.items()
            },
            "flags": engine.state.flags,
            "variables": engine.state.vars,
        }

        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=4), encoding="utf-8")
        tmp.replace(path)

    @staticmethod
    def load(engine: Engine, path: str | Path) -> None:
        path = Path(path)

        data = json.loads(path.read_text(encoding="utf-8"))

        SaveManager._validate(engine, data)

        engine.world.curr = data["current_room"]

        for _id, entity in data["room_entities"].items():
            engine.world.rooms[_id].entities = entity.copy()

        engine.inv.items = data["inventory"].copy()
        engine.state.flags = data["flags"].copy()
        engine.state.vars = data["variables"].copy()

    @staticmethod
    def _validate(engine: Engine, data: Any) -> None:
        if not isinstance(data, dict):
            raise ValueError("Invalid save file format.")

        if data.get("format_version") != SaveManager.FORMAT_VERSION:
            raise ValueError("Unsupported save file version.")

        expected = engine.story.metadata.get("id")

        if data.get("story_id") != expected:
            raise ValueError("This save belongs to a different story")

        _id = data.get("current_room")

        if _id not in engine.world.rooms:
            raise ValueError("Save file contains an unknown room")

        inv = data.get("inventory")
        room_entities = data.get("room_entities")
        flags = data.get("flags")
        variables = data.get("variables")

        if not isinstance(inv, list):
            raise ValueError("Invalid inventory in save file")

        if not isinstance(room_entities, dict):
            raise ValueError("Invalid room data in save file")

        if set(room_entities) != set(engine.world.rooms):
            raise ValueError("Save file has an incompatible room layout")

        if not isinstance(flags, dict):
            raise ValueError("Invalid flags in save file")

        if not isinstance(variables, dict):
            raise ValueError("Invalid variables in save file")

        if not all(isinstance(value, bool) for value in flags.values()):
            raise ValueError("Save file contains invalid flag values")

        var_types = (str, int, float, bool)

        if not all(isinstance(value, var_types) for value in variables.values()):
            raise ValueError("Save file contains invalid variable values")

        all_ids = []

        for ids in room_entities.values():
            if not isinstance(ids, list):
                raise ValueError("Invalid entity list in save file")

            all_ids.extend(ids)

        all_ids.extend(inv)

        if not all(
            isinstance(_id, str) and _id in engine.world.entities for _id in all_ids
        ):
            raise ValueError("Save file contains an unknown entity.")

        if len(all_ids) != len(set(all_ids)):
            raise ValueError("An entity appears in multiple locations.")

        for _id in inv:
            if not engine.world.get_entity(_id).portable:
                raise ValueError(f"Non portable entity in inventory: {_id}")
