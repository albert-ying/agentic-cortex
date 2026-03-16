---
description: "Vault sync router — orchestrates source adapters and vault updater. Use: /sync [source] [--dry-run]"
---

# Vault Sync

Orchestrates the vault sync pipeline: dispatches source adapters, collects manifests,
invokes the vault-updater.

## Usage

- `/sync` or `/sync all` — run calendar + email + screenpipe adapters in parallel, then updater
- `/sync calendar` — run only calendar adapter, then updater
- `/sync email` — run only email adapter, then updater
- `/sync screenpipe` — run only screenpipe adapter, then updater
- `/sync <source> --dry-run` — generate manifest, print summary, don't apply

## Session-Start Mode

When invoked by the command center at session start:

1. **Prune old manifests**: Delete `*-manifest-*.json` files older than 7 days from `.cache/sync-state/`
2. **Rebuild vault index**: Run `python3 notes/.scripts/build_vault_index.py`
3. **Wait for vault index**: Block until `.cache/sync-state/vault-index.json` exists and is fresh (built_at within last 60s)
4. **Dispatch adapters in parallel** using the Agent tool:
   - Calendar sync agent (foreground — fast, ~5s)
   - Email sync agent (foreground — moderate, ~15s)
   - Screenpipe sync agent (background — slow, ~60s)
5. **Invoke vault-updater** as each manifest arrives:
   - After calendar manifest -> vault-updater
   - After email manifest -> vault-updater
   - After screenpipe manifest -> vault-updater (background notification)
6. **Surface delta briefing** after each updater run

## Single-Source Mode

When invoked as `/sync <source>`:

1. Rebuild vault index (if older than 1 hour)
2. Run the specified adapter
3. If not `--dry-run`: invoke vault-updater with the manifest
4. If `--dry-run`: print manifest summary (N changes, affected notes, confidence levels)

## Adapter Dispatch

Each adapter is a separate skill invoked as a subagent:

| Source | Skill | Trigger |
|--------|-------|---------|
| Calendar | `sync/calendar-sync` | Session start (foreground) |
| Email | `sync/email-sync` | Session start (foreground) |
| Screenpipe | `sync/screenpipe-sync` | Session start (background) |

## Vault Updater Dispatch

After each adapter produces a manifest:
1. Invoke `sync/vault-updater` skill as a subagent
2. Pass the manifest file path(s)
3. Collect the delta report
4. Surface to user: "Sync delta: Updated N notes from <source>. [details]"

## Error Handling

- If an adapter fails: log the error, skip that source, continue with others
- Surface failures in the delta briefing: "Email sync failed: [error]. Using cached state."
- If vault-updater fails: log error, preserve manifest for retry on next session

## Manifest Pruning

At session start, before dispatching adapters:
```bash
find .cache/sync-state/ -name "*-manifest-*.json" -mtime +7 -delete
```
