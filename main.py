from engine.loader import Loader
from engine import Engine
from engine.actions import look
from pathlib import Path


def main():
    p = Path(__file__).parent / "stories" / "hollow_mile"
    story = Loader(p).load()
    engine = Engine(story)

    metadata = story.metadata

    print("=" * 60)
    print(f"                    {metadata["title"]}")
    print(f"                {metadata.get("subtitle", "")}")
    print("=" * 60)

    print("\nType 'help' to see avialalbe commands.")
    print("Type 'quit' to leave the station.\n")

    result = engine.start()

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

        result = engine.execute(user)

        print(f"\n{result.text}")

        if result.suggestions:
            print("\nSuggested actions:")
            for sug in result.suggestions:
                print(f" - {sug}")


if __name__ == "__main__":
    main()
