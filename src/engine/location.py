from dataclasses import dataclass, field


@dataclass
class Location:
    _id: str
    name: str
    desc: str

    exits: dict[str, str] = field(default_factory=dict)
    entities: list[str] = field(default_factory=list)

    exit_conditions: dict[str, dict] = field(default_factory=dict)

    def add_exit(self, direction: str, destination: str) -> None:
        self.exits[direction.lower()] = destination

    def add_entity(self, entity_id: str) -> None:
        if entity_id not in self.entities:
            self.entities.append(entity_id)

    def remove_exit(self, direction: str) -> None:
        self.exits.pop(direction.lower(), None)

    def remove_entity(self, entity_id: str) -> None:
        if entity_id in self.entities:
            self.entities.remove(entity_id)

    def has_exit(self, direction: str) -> str:
        return direction.lower()
