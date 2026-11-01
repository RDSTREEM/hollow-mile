# YAML Reference

HOLLOW MILE uses YAML files to define game content separately from the engine.

A game project contains a story definition, UI configuration, and indexed collections of locations, entities, and dialogue.

## Project layout

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

## Indexed content files

Locations, entities, and dialogue are loaded through an `index.yaml` file in their respective directories.

The index contains a `files` list identifying the YAML files to load.

Example:

```yaml
files:
  - starting_area.yaml
  - underground.yaml
```

Each indexed file contains a top-level mapping for its content type.

For example, a locations file uses:

```yaml
locations:
  ...
```

An entities file uses:

```yaml
entities:
  ...
```

A dialogue file uses:

```yaml
dialogues:
  ...
```

Content IDs are used to identify individual definitions. Duplicate IDs across indexed files are rejected.

## Locations

Locations define places the player can visit.

A location can contain:

- `name`: Display name.
- `description`: Description shown when examining or entering the location.
- `exit_conditions`: Conditions associated with leaving the location.
- Exits: Connections to other locations, including any conditions required to use them.

Example outline:

```yaml
locations:
  starting_area:
    name: Starting Area
    description: A quiet place at the edge of the world.
```

Check the generated project files for the exact exit mapping structure used by your version.

## Entities

Entities represent objects and characters in the game world.

Supported fields include:

| Field | Purpose |
|---|---|
| `name` | Display name |
| `description` | Default description |
| `aliases` | Alternative names recognized by the parser |
| `entity_type` | Entity category; defaults to `item` |
| `portable` | Whether the entity can be picked up |
| `location` | Entity's starting location |
| `interactions` | Definitions for supported interactions |
| `visible_when` | Condition controlling visibility |

Example:

```yaml
entities:
  old_key:
    name: Old Key
    description: A small, worn key.
    aliases:
      - rusty key
    entity_type: item
    portable: true
    location: starting_area
```

### Interactions

Entities can define interaction behavior through the `interactions` mapping.

The engine supports item-use interactions and answer-based puzzle interactions.

An item-use interaction is associated with the ID of an inventory item. An answer interaction can define accepted answers and success or failure behavior.

Interaction responses can include text, conditions, state changes, and emitted events. Supported state effects include:

- `set_flags`
- `set_variables`
- `increment_variables`
- `emit`

See the engine's action implementation for the exact response structure.

## Dialogue

Dialogue definitions are associated with character entity IDs.

A dialogue contains a starting node and a mapping of nodes.

Each node can contain text and a list of choices.

Example outline:

```yaml
dialogues:
  village_guard:
    start: greeting
    nodes:
      greeting:
        text: The guard looks in your direction.
        choices:
          - text: Ask about the road.
            next: road_information
          - text: Leave.
```

A choice can include:

- `text`: Text displayed for the choice.
- `response`: Optional response text.
- `next`: ID of the next dialogue node.
- `cond`: Condition controlling whether the choice is available.
- State effects such as flags, variables, and emitted events.

A node can also apply effects when it is entered.

## Conditions

Conditions determine whether an action, exit, entity, description variant, or dialogue choice is available.

The condition evaluator supports logical operators and game-state checks.

### Flags

Flags are boolean values. A flag condition is true when the flag matches the expected value.

```yaml
flag: gate_unlocked
equals: true
```

If `equals` is omitted, it defaults to `true`.

### Variables

Variables can contain numeric or string values.

```yaml
variable: trust
value: 3
operator: ">="
```

Supported operators:

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

If `operator` is omitted, it defaults to `==`.

### Logical operators

Use `all` to require every nested condition to pass:

```yaml
all:
  - flag: gate_unlocked
  - variable: trust
    value: 3
    operator: ">="
```

Use `any` to require at least one nested condition to pass:

```yaml
any:
  - flag: found_key
  - flag: gate_unlocked
```

Use `not` to invert a condition:

```yaml
not:
  flag: guard_alerted
```

A missing condition (`null`) is treated as true.

## Game state

The engine maintains game state using flags and variables.

- Flags store boolean state.
- Variables store numeric or string values.
- Variables can be assigned or incremented when an interaction or dialogue effect is applied.

Example effect structure:

```yaml
set_flags:
  gate_unlocked: true

set_variables:
  trust: 3

increment_variables:
  clues_found: 1
```

## UI configuration

The project's `config.yaml` controls terminal interface settings.

The supported configuration sections include:

- `title`
- `subtitle`
- `theme`
- `layout`
- `command`

Defaults are applied when optional configuration values are not supplied.

Refer to the generated `config.yaml` for the exact nested structure and accepted values in your engine version.

## Validation

Use the CLI validator to check a project:

```bash
hollow-mile validate my-game
```

Validation checks the loaded content and reports basic project information, including counts of locations, entities, and dialogue definitions.

For the most reliable examples, start with a project generated by:

```bash
hollow-mile init my-game
```

Then modify its YAML files while keeping the generated structure intact.