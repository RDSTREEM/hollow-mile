from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from engine import Entity, Room, World


@dataclass
class Story:
    metadata: dict[str, Any]
    world: World
    config: dict[str, Any]


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

    def _read_yaml(self, filename: str | Path) -> dict:

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

    def _load_config(self) -> dict:
        config = self.path / "config.yaml"

        defaults = {
            "ui": {
                "title": "HOLLOW MILE",
                "subtitle": "A Station That Should Not Exist",
                "theme": {
                    "background": "#000000",
                    "surface": "#080808",
                    "text": "#b5b5b5",
                    "muted": "#777777",
                    "accent": "#d5a85f",
                    "secondary": "#9ca88e",
                    "error": "#d58b76",
                    "border": "#333333",
                },
                "layout": {
                    "sidebar": True,
                    "sidebar_width": 32,
                    "header": True,
                    "footer": False,
                },
                "command": {
                    "placeholder": "What do you do?",
                },
            }
        }

        if not config.exists():
            return defaults

        c = self._read_yaml(config)
        ui = c.get("ui", {})

        if not isinstance(ui, dict):
            raise ValueError("config.yaml: ui must be a mapping")

        result = defaults.copy()
        result["ui"] = {**defaults["ui"], **ui}

        for section in ("theme", "layout", "command"):
            section_data = result["ui"].get(section, {})

            if not isinstance(section_data, dict):
                raise ValueError(f"{section} should be a mapping")

            result["ui"][section] = {**defaults["ui"][section], **section_data}

        return result

    def _load_indexed_files(self, folder_name: str, section_name: str) -> dict:
        folder = self.path / folder_name
        index_path = folder / "index.yaml"

        index = self._read_yaml(index_path)

        files = index.get("files")

        if not isinstance(files, list) or not files:
            raise ValueError(f"{index_path} must contain a non-empty files list")

        combined = {}

        for filename in files:
            if not isinstance(filename, str) or not filename:
                raise ValueError(f"Every entry in {index_path} must be a filename")

            file_path = (
                folder / filename
            ).resolve()  # great recall from yt archiver :)

            if not file_path.is_relative_to(folder.resolve()):
                raise ValueError(f"Invalid file path in {index_path}: {filename}")

            data = self._read_yaml(file_path)

            section = data.get(section_name)

            if not isinstance(section, dict):
                raise ValueError(f"{file_path} must contain a {section_name} mapping")

            for _id, definition in section.items():
                if _id in combined:
                    raise ValueError("Duplicate")

                combined[_id] = definition

        return {section_name: combined}

    def _load_section(self, folder_name: str, legacy: str, section_name: str) -> dict:
        # backward compatible is prob not the correct term butttt it is like that with the prev non modular way of holding items
        index_path = self.path / folder_name / "index.yaml"

        if index_path.exists():
            return self._load_indexed_files(folder_name, section_name)

        return self._read_yaml(self.path / legacy)

    def load(self) -> Story:
        metadata = self._read_yaml("story.yaml")
        config = self._load_config()

        room_data = self._load_section("rooms", "room.yaml", "rooms")
        item_data = self._load_section("items", "items.yaml", "items")

        world = World()

        self._load_rooms(room_data, world)
        self._load_entities(item_data, world)
        self._connect(room_data, world)

        start_room = metadata.get("start_room")

        if not isinstance(start_room, str) or not start_room:
            raise ValueError("story.yaml must have a starting room value")

        world.set_curr(start_room)

        return Story(metadata=metadata, world=world, config=config)

    def _load_rooms(self, room_data: dict, world: World):
        rooms = room_data.get("rooms")

        if not isinstance(rooms, dict) or not rooms:
            raise ValueError("Room data must contain a non-empty 'rooms' mapping")

        for _id, definition in rooms.items():
            if not isinstance(definition, dict):
                raise ValueError(f"Invalid definition for room: {_id}")

            name = definition.get("name")
            desc = definition.get("description", "")
            exit_conditions = definition.get("exit_conditions", {})

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
                    exit_conditions=exit_conditions,
                ),
            )

    def _load_entities(self, item_data: dict, world: World):
        items = item_data.get("items", {})

        if not isinstance(items, dict):
            raise ValueError("There has to be an items mapping in item data")

        for _id, definition in items.items():
            if not isinstance(definition, dict):
                raise ValueError(f"Invalid entity definition: {_id}")

            name = definition.get("name")
            desc = definition.get("description", "")
            aliases = definition.get("aliases", [])
            t = definition.get("entity_type", "item")
            portable = definition.get("portable", False)
            location = definition.get("location")
            interactions = definition.get("interactions", {})
            visible_when = definition.get("visible_when")

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

            if not isinstance(interactions, dict):
                raise ValueError(f"Interactions for {_id} must be a mapping")

            if not isinstance(visible_when, dict) and not visible_when is None:
                raise ValueError(f"Visibility rules for {_id} must be a mapping")

            entity = Entity(
                _id,
                name=name,
                desc=desc,
                _type=t,
                aliases=aliases,
                portable=portable,
                interactions=interactions,
                visible_when=visible_when,
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
