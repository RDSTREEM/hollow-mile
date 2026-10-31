from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from engine import Entity, Room, World


@dataclass
class Story:
    metadata: dict[str, Any]
    world: World


"""
The format imma use for the engine is as follows.
Each game will have a folder where the data is stored.
It will have a story.yaml with the main story, settings and stuff
It will have a rooms.yaml with  the rooms and the connections
And finally an items.yaml with the items and where they r found
"""


class Loader:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _read_yaml(self, filename: str) -> dict:

        p = self.path / filename

        if not p.exists():
            raise FileNotFoundError(f"Story file not found: {p}")

        try:
            with p.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {filename}: {e}")

        if not isinstance(data, dict):
            raise ValueError(f"{filename} must contain a YAML mapping")

        return data

    def load(self) -> Story:
        metadata = self._read_yaml("story.yaml")
        room_data = self._read_yaml("rooms.yaml")
        item_data = self._read_yaml("items.yaml")

        world = World()

        self._load_rooms(room_data, world)
        self._load_entities(item_data, world)
        self._connect(room_data, world)

        start_room = metadata.get("start_room")

        if not isinstance(start_room, str) or not start_room:
            raise ValueError("story.yaml must have a starting room value")

        world.set_curr(start_room)

        return Story(metadata=metadata, world=world)

    def _load_rooms(self, room_data: dict, world: World):
        rooms = room_data.get("rooms")

        if not isinstance(rooms, dict) or not rooms:
            raise ValueError("rooms.yaml must contain a non-empty 'rooms' mapping")

        for _id, definition in rooms.items():
            if not isinstance(definition, dict):
                raise ValueError(f"Invalid definition for room: {_id}")

            name = definition.get(name)
            desc = definition.get("description", "")

            # ? Parsing hell like before muhahahahahahahahaha

            if not isinstance(name, str) or not name:
                raise ValueError(f"Room {_id} must have a name")

            if not isinstance(desc, str):
                raise ValueError(f"Descriptions must be text, {_id}")

            world.add_room(
                Room(
                    _id=_id,
                    name=name,
                    desc=desc.strip(),
                ),
            )

    def _load_entities(self, item_data: dict, world: World):
        items = item_data.get("items", {})

        if not isinstance(items, dict):
            raise ValueError("There has to be an items mapping in items.yaml")

        for _id, definition in items.items():
            if not isinstance(definition, dict):
                raise ValueError(f"Invalid entity definition: {_id}")

            name = definition.get("name")
            desc = definition.get("description", "")
            aliases = definition.get("aliases", [])
            t = definition.get("entity_type", "item")
            portable = definition.get("portable", False)
            location = definition.get("location")

            if not isinstance(name, str) or not name:
                raise ValueError(f"Name for {_id} must be text")

            if not isinstance(desc, str) or not name:
                raise ValueError(f"Description for {_id} must be text")

            if not isinstance(aliases, list) or not all(
                isinstance(alias, str) for alias in aliases
            ):
                raise ValueError(f"Aliases for {_id} must be strings")

            if not isinstance(t, str) or not t:
                raise ValueError(f"Entity type for {_id} must be text")

            if not isinstance(portable, bool):
                raise ValueError(f"Portable for {_id} must be bool")

            if not isinstance(location, str) or not location:
                raise ValueError(f"Location for {_id} must be text")

            entity = Entity(
                _id,
                name=name,
                desc=desc,
                _type=t,
                aliases=aliases,
                portable=portable,
            )

            world.add_entity(entity)
            world.place_entity(_id, location)

    def _connect(self, room_data: dict, world: World):
        rooms = room_data["rooms"]

        for _id, definition in rooms.items():
            exits = definition.get("exits", {})

            if not isinstance(exits, dict):
                raise ValueError(f"Exits for {_id} must be a mapping")

            for d, dest in exits.items():
                if not isinstance(d, str) or not d:
                    raise ValueError(f"Invalid direction for exit {d} room")

                if not isinstance(dest, str):
                    raise ValueError(
                        f"Invalid destination for exit {d}" f"in room {_id}"
                    )

                try:
                    world.connect(_id, d, dest)
                except KeyError as e:
                    raise ValueError(f"Invalid exit from {_id} to {dest}: {e}") from e
