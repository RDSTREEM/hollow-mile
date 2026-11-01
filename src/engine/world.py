from engine.entity import Entity
from engine.location import Location


class World:
    def __init__(self) -> None:
        self.locations: dict[str, Location] = {}
        self.entities: dict[str, Entity] = {}

        self.current_location_id: str | None = None

    @property
    def current_location(self) -> Location:
        if self.current_location_id is None:
            raise RuntimeError("Current location does not exist")
        return self.get_location(self.current_location_id)

    @property
    def rooms(self) -> dict[str, Location]:
        return self.locations

    @rooms.setter
    def rooms(self, locations: dict[str, Location]) -> None:
        self.locations = locations

    @property
    def curr(self) -> str | None:
        return self.current_location_id

    @curr.setter
    def curr(self, location_id: str | None) -> None:
        self.current_location_id = location_id

    @property
    def curr_room(self) -> Location:
        return self.current_location

    def add_location(self, location: Location) -> None:
        if location._id in self.locations:
            return
        self.locations[location._id] = location

    def add_entity(self, entity: Entity) -> None:
        if entity._id in self.entities:
            return
        self.entities[entity._id] = entity

    def get_location(self, location_id: str) -> Location:
        try:
            return self.locations[location_id]
        except KeyError:
            raise ValueError(f"Unknown location id: {location_id}") from None

    def get_entity(self, entity_id: str) -> Entity:
        try:
            return self.entities[entity_id]
        except KeyError:
            raise ValueError(f"Unknown entity id: {entity_id}") from None

    def set_current_location(self, location_id: str) -> None:
        self.get_location(location_id)
        self.current_location_id = location_id

    def place_entity(self, entity_id: str, location_id: str) -> None:
        entity = self.get_entity(entity_id)
        location = self.get_location(location_id)

        if not entity.portable and entity.entity_type == "item":
            pass

        for prev in self.locations.values():
            prev.remove_entity(entity_id)

        location.add_entity(entity_id)

    def move(self, direction: str) -> Location:
        if self.current_location_id is None:
            raise RuntimeError("Player has no current location")

        direction = direction.strip().lower()

        dest_id = self.current_location.exits.get(direction)

        if dest_id is None:
            raise ValueError(f"There is no exit in that direction: {direction}")

        dest = self.get_location(dest_id)

        self.current_location_id = dest._id

        return dest

    def connect(
        self, location_id: str, direction: str, destination_id: str, bidir: bool = False
    ) -> None:
        location = self.get_location(location_id)
        self.get_location(destination_id)

        location.add_exit(direction, destination_id)

        if bidir:
            op = {
                "north": "south",
                "south": "north",
                "east": "west",
                "west": "east",
                "up": "down",
                "down": "up",
            }

            _op = op.get(direction)

            if _op is None:
                raise ValueError(f"Cant determin the opposite of {direction}")

            self.get_location(destination_id).add_exit(_op, location_id)

    def get_room(self, location_id: str) -> Location:
        return self.get_location(location_id)

    def add_room(self, location: Location) -> None:
        self.add_location(location)

    def set_curr(self, location_id: str) -> None:
        self.set_current_location(location_id)
