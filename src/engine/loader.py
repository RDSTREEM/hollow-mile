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

    def _load_rooms(self, room_data, world):
        pass

    def _load_entities(self, item_data, world):
        pass

    def _connect(self, room_data, world):
        pass
