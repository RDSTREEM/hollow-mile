class Inventory:
    def __init__(self):
        self.items: list[str] = []

    def add(self, _id: str) -> None:
        if _id not in self.items:
            self.items.append(_id)

    def remove(self, _id: str) -> None:
        if _id not in self.items:
            raise ValueError(f"Entity is not in inventory: {_id}")

        self.items.remove(_id)

    def contains(self, _id: str) -> bool:
        return _id in self.items

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def clear(self) -> None:
        self.items.clear()

    def __len__(self) -> int:
        return len(self.items)
