from dataclasses import dataclass, field


@dataclass
class Entity:
    id: str
    name: str
    description: str

    entity_type: str = "item"

    aliases: list[str] = field(default_factory=list)

    portable: bool = False
