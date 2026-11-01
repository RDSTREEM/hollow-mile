import argparse
import sys
from pathlib import Path

from engine.loader import Loader
from engine.ui import UI
from engine import Engine


def create_project(path: Path) -> None:
    if path.exists():
        raise FileExistsError("Destination alr exists")

    story = """\
id: my_game
title: My Story
subtitle: An Interactive Fiction Adventure
author: Author
version: "1.0"
start_room: starting_room  
            """

    config = """\
ui:
    title: "MY STORY"
    subtitle: "An Interactive Fiction Adventure"

    theme:
        background: "#000000"
        surface: "#080808"
        text: "#b5b5b5"
        muted: "#777777"
        accent: "#d5a85f"
        secondary: "#9ca88e"
        error: "#d58b76"
        border: "#333333"

    layout:
        sidebar: true
        sidebar_width: 32
        header: true
        footer: false

    command:
        placeholder: "What do you do?"
            """

    room_index = """\
files:
    - starting_area.yaml
            """

    starting_room = """\
rooms:
    starting_room:
        name: "A Quiet Room"
        description: >
            You are standing in a quiet room.
            An exit leads east.
        exits:
            east: hallway
    
    hallway:
        name: "Hallway"
        description: >
            A narrow hallway stretches before you.
            You can return west.
        exits:
            west: starting_room
            """

    item_index = """\
files:
    - objects.yaml
            """

    objects = """\
items:
    old_note:
        name: "Old Note"
        description: "A small note with faded writing"
        aliases:
            - note
        entity_type: item
        portable: true
        location: starting_room
            """

    files = {
        "story.yaml": story,
        "config.yaml": config,
        "rooms/index.yaml": room_index,
        "rooms/starting_area.yaml": starting_room,
        "items/index.yaml": item_index,
        "items/objects.yaml": objects,
    }

    path.mkdir(parents=True)

    for f, content in files.items():
        p = path / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    print(f"Created project: {path}")
    print()
    print("Next steps:")
    print(f"\thollow-mile run {path}")
    print(f"\thollow-mile validae {path}")


def run_game(path: Path) -> None:
    story = Loader(path).load()
    engine = Engine(story)

    app = UI(engine)
    app.run()


def validate_game(path: Path) -> bool:
    print(f"Validating projectL {path}")
    print()

    try:
        story = Loader(path).load()

        room_count = len(story.world.rooms)
        entity_count = len(story.world.entities)

        print("[OK] Story files loaded")
        print("[OK] Starting room exists")
        print(f"[OK] Loaded {room_count} rooms")
        print(f"[OK] Loaded {entity_count} entities")
        print("[OK] Room connections and entity placements loaded")
        print("[OK] Configuration loaded")

        print()

        print("Project validation successful")

        return True

    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"[ERROR] {e}")
        print()
        print("Project validation failed")

        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hollow-mile", description="A data driven interactive fiction engine."
    )

    subparsers = parser.add_subparsers(dest="cmd", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new story project")
    init_parser.add_argument(
        "path", type=Path, help="Destination folder for then new project"
    )

    run_parser = subparsers.add_parser("run", help="Run an interactive fiction project")
    run_parser.add_argument("path", type=Path, help="Path to the story project")

    validate_parser = subparsers.add_parser("validate", help="Validate a story project")
    validate_parser.add_argument("path", type=Path, help="Path to the story project")

    return parser


def main() -> None:
    parser = build_parser()

    args = parser.parse_args()

    try:
        if args.cmd == "init":
            create_project(args.path)
        elif args.cmd == "run":
            run_game(args.path)
        elif args.cmd == "validate":
            s = validate_game(args.path)

            if not s:
                sys.exit(0)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
