As a part of continuous improvement of the environment we would like to think about the blender-cli and how it could be better. Think about the following and propose changes to the cli:

## Commands & Capabilities
- What blender-cli commands do you wish you had?
- What multi-step workflows do you repeat that should be a single command?
- Are there server-side handlers that have no CLI command (or vice versa)?

## Verbosity & Output
- What blender-cli commands are too verbose?
- What output fields are never useful and should be removed or hidden behind --verbose?
- Should any commands have a --brief mode that shows just pass/fail + key numbers?

## Observability
- What information do you wish the blender-cli could show you?
- What errors do you see frequently that could have better diagnostics?
- Can we surface addon.log errors/warnings through CLI commands instead of reading the file?

## Validation & Safety
- What information do you wish the blender-cli could automatically validate?
- What checks should run automatically before/after common operations (export, promote, reload)?
- Are there common failure modes that could be detected earlier?

## Context & Persistence
- What context is lost between conversations that should be persisted?
- Should the CLI track operation history (last export, last promote, last validate)?
- Would a .blender-cli-state file help avoid re-specifying common arguments?
