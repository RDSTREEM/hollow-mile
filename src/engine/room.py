from dataclasses import dataclass, field


@dataclass
class Room:
    _id: str
    name: str
    desc: str

    exits: dict[str, str] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)

    def add_exit(self, d: str, dest: str) -> None:
        self.exits[d.lower()] = dest

    def add_entity(self, _id: str) -> None:
        if _id not in self.entities:
            self.entities.append(_id)

    def remove_exit(self, d: str) -> None:
        self.exits.pop(d.lower(), None)

    def remove_entity(self, _id: str) -> None:
        if _id in self.entities:
            self.entities.remove(_id)

    def has_exit(self, d) -> None:
        return d.lower()
