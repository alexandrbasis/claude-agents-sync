# Project Structure

```
claude-agents-sync/
│
├── README.md                       # Main documentation
├── STRUCTURE.md                    # This file
├── .gitignore                      # Git ignore rules
│
├── .claude/
│   ├── hooks/
│   │   ├── auto-sync-claude-agents.py    # PostToolUse hook entry point
│   │   ├── claude-agents-sync.py         # Core sync logic (auto-discovery)
│   │   └── claude-agents-sync.sh         # Bash wrapper script
│   │
│   └── settings.local.json         # Example hook configuration
│
└── examples/
    ├── simple-project/
    │   └── README.md              # Single pair setup guide
    │
    └── monorepo/
        └── README.md              # Multiple pairs setup guide
```

## File Descriptions

### Core Files

- **`.claude/hooks/auto-sync-claude-agents.py`**
  - Entry point for PostToolUse hook
  - Receives JSON from Claude Code via stdin
  - Detects Edit/Write operations on CLAUDE.md/AGENTS.md
  - Triggers sync process

- **`.claude/hooks/claude-agents-sync.py`**
  - Core synchronization logic
  - Auto-discovers all CLAUDE.md/AGENTS.md pairs in project
  - Compares content (ignores whitespace)
  - Bidirectional sync: updates counterpart file

- **`.claude/hooks/claude-agents-sync.sh`**
  - Bash wrapper for Python script
  - Handles file path arguments
  - Sets up environment variables

- **`.claude/settings.local.json`**
  - Example configuration for Claude Code
  - Shows how to register PostToolUse hook

### Documentation

- **`README.md`**
  - Comprehensive project documentation
  - Installation guide
  - Usage examples
  - Comparison with alternatives
  - Troubleshooting

- **`examples/simple-project/README.md`**
  - Setup guide for single CLAUDE.md/AGENTS.md pair
  - Perfect for individual projects

- **`examples/monorepo/README.md`**
  - Setup guide for multiple pairs
  - Perfect for monorepos and microservices

## Installation Workflow

1. **Clone/Download** this repository
2. **Copy** `.claude/` directory to your project
3. **Make executable**: `chmod +x .claude/hooks/*.sh`
4. **Configure** hook in your `.claude/settings.local.json`
5. **Done!** Sync happens automatically

## Technical Flow

```
User edits CLAUDE.md in Claude Code
         ↓
Claude Code fires PostToolUse hook
         ↓
auto-sync-claude-agents.py (reads JSON via stdin)
         ↓
Detects file is CLAUDE.md or AGENTS.md
         ↓
Calls claude-agents-sync.sh with file path
         ↓
claude-agents-sync.py:
  1. Auto-discovers all pairs in project
  2. Finds pair containing edited file
  3. Compares content (normalized)
  4. Updates counterpart if different
         ↓
AGENTS.md is synchronized
         ↓
Logs result to hook-debug.log
```

## Key Features

- ✅ **Zero Configuration**: Auto-discovers pairs
- ✅ **Bidirectional**: Edit either file
- ✅ **Safe**: Only updates when needed
- ✅ **Fast**: < 1 second
- ✅ **Silent**: Background operation
- ✅ **Scalable**: Handles multiple pairs

## No Dependencies

Only requires:
- Python 3 (pre-installed on macOS/Linux)
- Claude Code with hooks support

No pip packages, no virtual environments, no complexity!
