# AGENTS.md — gurvindersingh-web

This repo is part of the machine-wide memory system.

> **The Obsidian vault is the canonical source of truth.** This file and the
> graphify graph are *not* canonical. If they disagree with the vault, the vault
> wins and the mismatch must be flagged.

| What | Where |
|---|---|
| Vault | `~/Brain` |
| Project note | `~/Brain/01-projects/gurvindersingh-web.md` |
| Hot context | `~/Brain/00-hot/hot.md` |
| Handovers | `~/Brain/04-handovers/` (filter by project) |
| Decisions | `~/Brain/03-decisions/` |
| Graph (discovery only) | `graphify-out/` in this repo, linked at `~/Brain/06-graphs/gurvindersingh-web/` |

## SESSION START

1. Read `~/Brain/00-hot/hot.md`.
2. Read `~/Brain/01-projects/gurvindersingh-web.md` and the **2 most recent** handover notes for
   this project in `~/Brain/04-handovers/` (newest first, matching `project: gurvindersingh-web`).
3. If `graphify-out/graph.json` exists, **query the graph before grepping raw files**:

   ```bash
   graphify query "<question>"      # scoped BFS over graph.json
   graphify path "A" "B"            # shortest path between two nodes
   graphify explain "Symbol"        # plain-language node explanation
   graphify god-nodes --top 10      # architectural hubs
   ```

   The graph is a **map, not the territory** — confirm anything surprising in the
   source file.

## DURING WORK

- Log any architectural decision to `~/Brain/03-decisions/` **immediately**
  (context, choice, reason, date).
- **Never** store secrets, tokens, API keys, passwords or `.env` contents in the
  vault. Reference *where* a secret lives, never its value.
- Keep `~/Brain/01-projects/gurvindersingh-web.md` accurate — update **Status** when the
  project state changes, add a **Gotcha** the moment one bites.

## SESSION END (or when the user says "handover")

1. Write `~/Brain/04-handovers/YYYY-MM-DD-gurvindersingh-web.md` containing: **what was done,
   what changed, what's broken, next steps, and the exact commands to resume**.
2. Update the **Status** section of `~/Brain/01-projects/gurvindersingh-web.md`.
3. Rewrite `~/Brain/00-hot/hot.md` to reflect the current state — **under 500 words**.

## CONFLICT RULE

If graph output and vault notes disagree, **the vault notes win**. Flag the mismatch
explicitly instead of silently preferring one.

## Housekeeping

- `graphify-out/` is git-ignored: it is a generated artefact, rebuilt by
  `graphify hook install` (post-commit/post-checkout/post-merge/post-rewrite) and
  by `brain-update`.
- Set `GRAPHIFY_SKIP_HOOK=1` to skip the automatic rebuild for one commit.
- Rebuild everything: `brain-update`.
