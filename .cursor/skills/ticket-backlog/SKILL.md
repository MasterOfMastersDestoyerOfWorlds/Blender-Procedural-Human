---
name: ticket-backlog
description: Query the ticket backlog for this repo and recommend the best ticket to work on next. Use when the user asks what to work on, mentions tickets, backlog, priorities, or asks to pick a task.
---

# Ticket Backlog

## Step 1: Fetch the backlog

Run from the workspace root:

```bash
python ixdar-tickets/generate_board.py backlog Blender-Procedural-Human
```

This prints all actionable tickets (IN_PROGRESS and TODO) with priorities,
dependency chains, and truncated descriptions.

## Step 2: Recommend the best ticket

Apply these rules in order to pick the best next ticket:

1. **Finish in-progress work first.** Any IN_PROGRESS ticket takes priority
   over starting new work.
2. **Respect blockers.** A ticket with `blocked-by` dependencies that are
   not DONE cannot be started. Skip it.
3. **Prefer unblocked tickets that unblock others.** A ticket that `blocks`
   other tickets has higher leverage.
4. **Lower priority number = higher importance.** P1 before P2 before P3.

## Step 3: Report to the user

Present a short summary:

```
Recommended: BLEN-XX — Title
Priority: PX | Blocked by: (none) | Unblocks: BLEN-YY, BLEN-ZZ
Reason: [one sentence why this is the best pick]
```

If multiple tickets are equally viable, list the top 2-3 and let the user
choose.

## Step 4: Read the ticket

Once a ticket is chosen, read the full ticket JSON to get the definition of
done, testing plan, and TODO list:

```bash
cat ixdar-tickets/content/<EPIC>/<ID>.json
```

Then follow the ticket-lifecycle rule for status updates as work proceeds.
