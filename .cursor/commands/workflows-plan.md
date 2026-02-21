# workflows-plan

Create a scoped implementation plan before coding.

## Before You Plan

Search `.cursor/docs/ai-learnings/` for related learnings — grep by tags, title,
or module names relevant to the task. Surface any prior decisions, anti-patterns,
or counter-intuitive findings that could shape the plan.

```
rg -l "<keyword>" .cursor/docs/ai-learnings/
```

## Inputs

- Goal and success criteria
- Constraints (runtime, performance, compatibility, deadlines)
- Relevant files/systems
- **Prior learnings** found in the step above

## Output Format

1. Problem statement
2. Constraints and assumptions (include relevant prior learnings)
3. Step-by-step implementation plan (3-7 steps)
4. Validation plan
5. Risks and rollback

Keep the plan actionable and file-specific.
