from engine import World, Room, Entity


def demo() -> World:
    world = World()

    platform = Room(
        _id="platform",
        name="Platform",
        desc=(
            "A deserted railway platform streches into darkness."
            "The lights flicker overhead."
        ),
    )

    hall = Room(
        _id="ticket_hall",
        name="Ticket Hall",
        desc=(
            "A narrow ticket hall. Dust covers the counters."
            "and an old clock hangs above the entrance"
        ),
    )

    office = Room(
        _id="maintenance_office",
        name="Maintenance Office",
        desc=("A cramped office filled with forgotten railway equipment"),
    )

    world.add_room(platform)
    world.add_room(hall)
    world.add_room(office)
    for room in world.rooms:
        print(room)

    world.connect("platform", "north", "ticket_hall", True)

    world.connect("ticket_hall", "east", "maintenance_office", True)

    key = Entity(
        _id="brass_key",
        name="Brass key",
        desc="A small brass key. Its handle bears the number 03.",
        aliases=["key", "old key"],
        portable=True,
    )

    board = Entity(
        _id="noticeboard",
        name="Noticeboard",
        desc="A faded timetable is pined beneath a layer of dust.",
        _type="object",
        aliases=["board", "timetable"],
    )

    world.add_entity(key)
    world.add_entity(board)

    world.place_entity("brass_key", "platform")
    world.place_entity("noticeboard", "ticket_hall")

    world.set_curr("platform")

    return world


def main():
    world = demo()

    print("=" * 50)
    print("                    HOLLOW MILE")
    print("=" * 50)

    print(f"\n Location: {world.curr_room.name}")
    print(world.curr_room.desc)

    print("\n Avialable exits: ")

    for d in world.curr_room.exits:
        print(f" - {d}")

    print("\n Moving north...")

    dest = world.move("north")

    print(f"\n Location: {dest.name}")
    print(dest.desc)

    print("\n Entities in this room: ")
    for entity in dest.entities:
        e = world.get_entity(entity)
        print(f"- {e.name}")


if __name__ == "__main__":
    main()
