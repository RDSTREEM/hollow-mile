from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    _id: str
    name: str
    desc: str

    _type: str = "item"

    aliases: list[str] = field(default_factory=list)

    portable: bool = False

    interactions: dict[str, Any] = field(default_factory=dict)

    def matches(self, query: str) -> bool:

        query = " ".join(query.lower().split())
        names = [self.name, *self.aliases]

        return any(query == " ".join(name.lower().split()) for name in names)
