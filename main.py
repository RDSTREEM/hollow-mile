from engine.loader import Loader
from pathlib import Path


def main():
    p = Path(__file__).parent / "stories" / "hollow_mile"
    loader = Loader(p)
    story = loader.load()
    world = story.world
    metadata = story.metadata

    print("=" * 50)
    print(f"                    {metadata["title"]}")
    print(f"                {metadata.get("subtitle", "")}")
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
