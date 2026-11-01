import json
from pathlib import Path
from typing import Any


class SaveManager:
    FORMAT_VERSION = 2

    @staticmethod
    def save(engine, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "format_version": SaveManager.FORMAT_VERSION,
            "story_id": engine.story.metadata.get("id"),
            "current_location": engine.world.current_location_id,
            "inventory_entities": engine.inv.entities,
            "location_entities": {
                _id: location.entities
                for _id, location in engine.world.locations.items()
            },
            "flags": engine.state.flags,
            "variables": engine.state.vars,
        }

        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=4), encoding="utf-8")
        tmp.replace(path)

    @staticmethod
    def load(engine, path: str | Path) -> None:
        path = Path(path)

        data = json.loads(path.read_text(encoding="utf-8"))

        current_location, inventory_entities, location_entities = SaveManager._validate(
            engine, data
        )

        engine.world.current_location_id = current_location

        for _id, entities in location_entities.items():
            engine.world.locations[_id].entities = entities.copy()

        engine.inv.entities = inventory_entities.copy()
        engine.state.flags = data["flags"].copy()
        engine.state.vars = data["variables"].copy()

    @staticmethod
    def _validate(engine, data: Any) -> tuple[str, list[str], dict[str, list[str]]]:
        if not isinstance(data, dict):
            raise ValueError("Invalid save file format.")

        version = data.get("format_version")
        if version not in {1, SaveManager.FORMAT_VERSION}:
            raise ValueError("Unsupported save file version.")

        expected = engine.story.metadata.get("id")

        if data.get("story_id") != expected:
            raise ValueError("This save belongs to a different story")

        current_location = data.get("current_location", data.get("current_room"))

        if (
            not isinstance(current_location, str)
            or current_location not in engine.world.locations
        ):
            raise ValueError("Save file contains an unknown location")

        inventory_entities = data.get("inventory_entities", data.get("inventory"))
        location_entities = data.get("location_entities", data.get("room_entities"))
        flags = data.get("flags")
        variables = data.get("variables")

        if not isinstance(inventory_entities, list):
            raise ValueError("Invalid inventory in save file")

        if not isinstance(location_entities, dict):
            raise ValueError("Invalid location data in save file")

        if set(location_entities) != set(engine.world.locations):
            raise ValueError("Save file has an incompatible location layout")

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

        for ids in location_entities.values():
            if not isinstance(ids, list):
                raise ValueError("Invalid entity list in save file")

            all_ids.extend(ids)

        all_ids.extend(inventory_entities)

        if not all(
            isinstance(_id, str) and _id in engine.world.entities for _id in all_ids
        ):
            raise ValueError("Save file contains an unknown entity.")

        if len(all_ids) != len(set(all_ids)):
            raise ValueError("An entity appears in multiple locations.")

        for _id in inventory_entities:
            if not engine.world.get_entity(_id).portable:
                raise ValueError(f"Non portable entity in inventory: {_id}")

        return current_location, inventory_entities, location_entities
