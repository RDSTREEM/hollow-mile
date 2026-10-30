from dataclasses import dataclass, field


@dataclass
class Room:
    _id: str
    name: str
    desc: str

    exits: dict[str, str] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)
