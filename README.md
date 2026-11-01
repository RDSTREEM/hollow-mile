# HOLLOW MILE

**A reusable, data-driven interactive-fiction engine built with Python.**

HOLLOW MILE is a framework for creating text-based adventures and narrative-driven games. It separates the game engine from story content, allowing you to build multiple games using YAML files without rewriting the underlying engine.

## Showcase

Here's HOLLOW MILE running the showcase game (also called Hollow Mile):

![HOLLOW MILE showcase game running in the terminal](docs/showcase.png)

*The showcase demonstrates the engine's terminal interface and an example game running on it.*

## Features

- YAML-defined stories, locations, entities, and dialogue
- Location navigation and conditional exits
- Entity inspection, interaction, and inventory management
- Branching dialogue with conditional choices
- Puzzles and item-based interactions
- Game state using flags and variables
- Configurable terminal interface
- CLI tools for creating, validating, and running projects

## Installation

### Download a release

Download the latest release from the [GitHub Releases page](../../releases).

If a release includes a standalone executable, extract it and run `hollow-mile.exe` from a terminal.

If you download the showcase bundle, keep the showcase folder alongside the executable.

### Run from source

Clone the repository:

```bash
git clone <repository-url>
cd hollow-mile
```

Install the project:

```bash
python -m pip install -e .
```

## Quick start

Create a new game project:

```bash
hollow-mile init my-game
```

Validate it:

```bash
hollow-mile validate my-game
```

Run it:

```bash
hollow-mile run my-game
```

## Showcase game

The showcase project demonstrates how HOLLOW MILE can run a separate game using the same engine.

```bash
hollow-mile validate showcase
hollow-mile run showcase
```

You can use it as a starting point when creating your own game.

## Project structure

```text
my-game/
├── story.yaml
├── config.yaml
├── locations/
│   ├── index.yaml
│   └── ...
├── entities/
│   ├── index.yaml
│   └── ...
└── dialogue/
    ├── index.yaml
    └── ...
```

See [YAML Reference](docs/YAML_REFERENCE.md) for details about the content format.

## Building from source

On Windows, run:

```bat
build.bat
```

The executable will be generated at:

```text
dist/hollow-mile.exe
```

## Requirements

- Python 3.12+
- Textual
- PyYAML

## Project status

HOLLOW MILE is under active development. Features and file formats may change between releases.

## License

See the `LICENSE` file for licensing information.