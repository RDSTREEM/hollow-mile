from dataclasses import dataclass, field


@dataclass
class Entity:
    _id: str
    name: str
    desc: str

    _type: str = "item"

    aliases: list[str] = field(default_factory=list)

    portable: bool = False
