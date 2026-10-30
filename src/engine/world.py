from engine.entity import Entity
from engine.room import Room


class World:
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self.entities: dict[str, Entity] = {}

        self.curr: str | None = None

    @property
    def curr_room(self):
        if self.curr is None:
            return None
        return self.get_room(self.curr)

    def add_room(self, room: Room) -> None:
        if room._id not in self.rooms:
            return
        self.rooms[room._id] = room

    def add_entity(self, entity: Entity) -> None:
        if entity._id not in self.rooms:
            return
        self.entities[entity._id] = entity

    def get_room(self, room_id: str) -> Room:
        try:
            return self.rooms[room_id]
        except:
            raise ValueError(f"Unknown room id: {room_id}")

    def get_entity(self, entity_id: str) -> Entity:
        try:
            return self.entities[entity_id]
        except:
            raise ValueError(f"Unknown room id: {entity_id}")

    def set_curr(self, room_id: str) -> None:
        if self.get_room(room_id) is None:
            return
        self.curr = room_id

    def place_entity(self, entity_id: str, room_id: str) -> None:
        entity = self.get_entity(entity_id)
        room = self.get_room(room_id)

        if not entity.portable and entity._type == "item":
            pass

        for prev in self.rooms.values():
            prev.remove_entity(entity_id)

        room.add_entity(entity_id)

    def move(self, d: str) -> Room:
        if self.curr_room is None:
            raise RuntimeError("Player has no current location")

        d = d.strip().lower()

        dest_id = self.curr_room.exits.get(d)

        if dest_id is None:
            raise ValueError(f"There is no exit in that direction: {d}")

        dest = self.get_room(dest_id)

        self.curr = dest._id

        return dest
