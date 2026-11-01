from engine.loader import Loader
from engine import Engine
from pathlib import Path
from engine.ui import UI


def main():
    p = Path(__file__).parent / "stories" / "hollow_mile"
    story = Loader(p).load()
    engine = Engine(story)

    app = UI(engine)
    app.run()


if __name__ == "__main__":
    main()
