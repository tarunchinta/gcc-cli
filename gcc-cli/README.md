# GCC — Git Context Controller

Git-style version control for AI agent context. Think of it as **"git for AI reasoning state."**

GCC lets you commit, branch, and diff your AI agent's context and reasoning snapshots — 100% locally, no network required.

## Install

```bash
pip install gcc-cli
```

Or install from source:

```bash
git clone <repo-url>
cd gcc-cli
pip install -e .
```

## Quickstart

```bash
# Initialize a workspace
gcc init

# Edit your context file
# (or let your agent write to .GCC/branches/main/commit.md)

# Commit a snapshot
gcc commit -m "found root cause in auth middleware"

# View history
gcc log

# Check current state
gcc status

# Create and switch branches
gcc branch experiment
gcc checkout experiment

# Compare two commits
gcc diff abc12345 def67890
```

## Commands

| Command | Description |
|---|---|
| `gcc init` | Initialize `.GCC/` workspace in the current directory |
| `gcc commit -m "msg"` | Snapshot current context state |
| `gcc log` | Show commit history |
| `gcc status` | Show current branch, HEAD, and dirty state |
| `gcc branch <name>` | Create a new branch from current |
| `gcc checkout <name>` | Switch to an existing branch |
| `gcc diff <h1> <h2>` | Unified text diff between two commits |
| `gcc version` | Show GCC version |

## Python SDK

Use GCC programmatically from any Python agent:

```python
from gcc.sdk import GCCClient

client = GCCClient(".")

# Commit context
hash = client.commit("analyzed auth flow", "# Auth Analysis\nThe middleware...")

# Retrieve context
context = client.get_context()       # latest
context = client.get_context(hash)   # specific commit

# Get history
for entry in client.get_log():
    print(entry["hash"], entry["message"])
```

## LangGraph Adapter

```python
from gcc.adapters.langgraph import GCCCheckpointer

checkpointer = GCCCheckpointer(".")

# Save a checkpoint
config = {"configurable": {"thread_id": "agent-1"}}
checkpointer.put(config, {"messages": [...], "step": 5})

# Restore latest
state = checkpointer.get(config)
```

## Workspace Structure

```
.GCC/
  config                    # workspace name, current branch
  HEAD                      # current commit hash
  main.md                   # global project roadmap
  branches/
    main/
      commit.md             # current context for this branch
      log.md                # execution trace
      metadata.yaml         # model, tokens, task info
  commits/
    <hash>.json             # commit metadata
  snapshots/
    <hash>/
      context.md            # full context at that commit
      metadata.yaml         # timestamp, message, parent, branch
```

## Compatibility

The `.GCC/` folder format is fully compatible with the [Git Context Controller](https://github.com/faugustdev/git-context-controller) research implementation. Projects already using the Claude Code GCC skill work immediately with this CLI.

## Requirements

- Python 3.9+
- No network connection needed — everything is local
