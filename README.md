# HOLLOW MILE

A reusable, data-driven interactive-fiction engine.

## CLI

```powershell
hollow-mile init my_game
hollow-mile validate my_game
hollow-mile run my_game
```

Stories use `story.yaml` with a `start_location` ID, indexed YAML files under
`locations/` and `entities/`, and dialogue definitions under `dialogue/`.

Location files use a top-level `locations:` mapping. Entity files use an
`entities:` mapping; each entity's `location` field references a location ID.
Dialogue definitions reference characters by their entity IDs.
