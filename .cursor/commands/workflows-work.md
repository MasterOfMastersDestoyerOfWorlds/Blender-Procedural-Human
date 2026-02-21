# workflows-work

Execute an approved plan in small validated increments.

## Before You Start

If you did not run `/workflows-plan` first, search `.cursor/docs/ai-learnings/`
for related learnings (grep by tags, modules, or keywords). Prior decisions and
anti-patterns should inform how you implement.

## Execution Rules

- Work one plan step at a time.
- Validate after each step (compile/tests/manual check).
- Keep progress updates short and explicit.
- Stop and report if an unexpected state change appears.

## Completion Checklist

- Planned steps implemented
- Validations run and passing
- No unrelated files changed
