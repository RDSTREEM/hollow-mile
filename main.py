from engine.loader import Loader
from engine import CommandParser, Command, create_registry, Inventory
from engine.actions import look
from pathlib import Path


def main():
    p = Path(__file__).parent / "stories" / "hollow_mile"
    loader = Loader(p)
    story = loader.load()
    world = story.world
    metadata = story.metadata

    inv = Inventory()

    parser = CommandParser()
    actions = create_registry()

    print("=" * 60)
    print(f"                    {metadata["title"]}")
    print(f"                {metadata.get("subtitle", "")}")
    print("=" * 60)

    print("\nType 'help' to see avialalbe commands.")
    print("Type 'quit' to leave the station.\n")

    result = look(world, inv, Command(action="look"))

    print(result.text)

    while True:
        try:
            user = input("\n>").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n Leaving the station")
            break

        if user.lower() in {"quit", "exit"}:
            print("\nYour train remains silent.")
            print("HOLLOW MILE - SESSION ENDED")
            break

        command = parser.parse(user)

        if command.action == "empty":
            continue

        res = actions.execute(world, inv, command)

        print(f"\n{res.text}")

        if res.suggestions:
            print("\nSuggested actions:")
            for sug in res.suggestions:
                print(f" - {sug}")


if __name__ == "__main__":
    main()
