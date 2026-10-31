from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from engine import Entity, Room, World


@dataclass
class LoadedStory:

    metadata = dict[str, Any]
    world: World


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
