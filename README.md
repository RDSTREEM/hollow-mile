# HOLLOW MILE

**A reusable, data-driven interactive-fiction engine built with Python.**

HOLLOW MILE is a modular engine for creating text adventures and narrative-driven games. It separates game logic from story content, allowing developers to build different worlds and experiences using structured YAML files rather than hardcoding individual games.

Inspired by classic interactive fiction and narrative RPGs, HOLLOW MILE provides systems for world navigation, entity interactions, inventory management, dialogue, puzzles, and conditional game events.

Built with Python, Textual, and PyYAML.

## Features

- **Data-driven worlds:** Define locations, entities, and game content through YAML.
- **World navigation:** Connect locations through directional exits.
- **Entity system:** Define objects, characters, aliases, and portability.
- **Inventory:** Pick up, carry, and drop items.
- **Interactions:** Use inventory items on objects and characters.
- **Dialogue:** Create conversations using branching dialogue nodes.
- **Puzzles:** Define answer-based interactions.
- **Game state:** Support flags, variables, conditions, and state changes.
- **Configurable UI:** Customize the terminal interface through YAML configuration.
- **Project management:** Initialize, validate, and run story projects through the CLI.

## Installation

There are two ways to get HOLLOW MILE.

### Option 1: Download from GitHub Releases

If you just want to use HOLLOW MILE without installing Python or its dependencies, download a prebuilt release.

Visit the repository's **Releases** page and download the appropriate package.

Available packages:

| Download | Contents |
|---|---|
| HOLLOW MILE CLI | Standalone engine executable |
| HOLLOW MILE Showcase | Engine executable bundled with the showcase game |

Extract the downloaded archive and run the executable through your terminal.

For example:

```powershell
.\hollow-mile.exe init my_game
.\hollow-mile.exe validate my_game
.\hollow-mile.exe run my_game
```

The showcase package includes an example game that can be run immediately.

### Option 2: Build from Source

For development or modifying the engine, you can install HOLLOW MILE directly from its source code.

**Requirements:**
- Python 3.12 or newer
- Git
- pip

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/hollow-mile.git
cd hollow-mile
```

Install the project:

```bash
pip install -e .
```

This installs HOLLOW MILE in editable mode along with its dependencies.

You can now use the CLI:

```bash
hollow-mile init my_game
hollow-mile validate my_game
hollow-mile run my_game
```

## Quick Start

Create a new story project:

```bash
hollow-mile init my_game
```

This generates a basic project structure containing story metadata, configuration, locations, entities, and dialogue directories.

Validate your project:

```bash
hollow-mile validate my_game
```

Run your game:

```bash
hollow-mile run my_game
```

## Showcase Game

HOLLOW MILE includes a small showcase game demonstrating how a playable project can be created using the engine.

It serves as an example of how locations, entities, interactions, and other game content can be defined independently of the engine itself.

The showcase is intentionally small and is primarily intended to demonstrate the engine's capabilities and project structure.

## Project Structure

A typical HOLLOW MILE game project looks like this:

```text
my_game/
├── story.yaml
├── config.yaml
│
├── locations/
│   ├── index.yaml
│   └── ...
│
├── entities/
│   ├── index.yaml
│   └── ...
│
└── dialogue/
    ├── index.yaml
    └── ...
```

Game content is separated into indexed YAML files, making projects easier to organize and expand.

## Commands

| Command | Description |
|---|---|
| `hollow-mile init <path>` | Creates a new project |
| `hollow-mile validate <path>` | Validates a project |
| `hollow-mile run <path>` | Runs a project |

## Technology

- **Python 3.12+** — Core engine.
- **Textual** — Terminal user interface.
- **PyYAML** — YAML parsing and data loading.
- **setuptools** — Python packaging.

## Project Status

HOLLOW MILE is currently under active development. Features, internal systems, and project formats may change between releases.

## License

See [LICENSE](LICENSE) for licensing information.

---

**HOLLOW MILE — Build a world. Give it rules. Let it tell a story.**