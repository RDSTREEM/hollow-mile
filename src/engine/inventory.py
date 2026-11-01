class Inventory:
    def __init__(self):
        self.entities: list[str] = []

    @property
    def items(self) -> list[str]:
        return self.entities

    @items.setter
    def items(self, entity_ids: list[str]) -> None:
        self.entities = entity_ids

    def add(self, _id: str) -> None:
        if _id not in self.entities:
            self.entities.append(_id)

    def remove(self, _id: str) -> None:
        if _id not in self.entities:
            raise ValueError(f"Entity is not in inventory: {_id}")

        self.entities.remove(_id)

    def contains(self, _id: str) -> bool:
        return _id in self.entities

    def is_empty(self) -> bool:
        return len(self.entities) == 0

    def clear(self) -> None:
        self.entities.clear()

    def __len__(self) -> int:
        return len(self.entities)
