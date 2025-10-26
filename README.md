# claude-agents-sync

**Automatic synchronization for CLAUDE.md ↔ AGENTS.md files in Claude Code projects**

Keep your AI assistant instructions synchronized when using multiple AI coding tools (Claude Code, Cursor, etc.) in the same project.

---

## The Problem

Different AI coding tools read instructions from different files:
- **Claude Code** reads `CLAUDE.md`
- **Cursor** (and other tools) read `AGENTS.md`

When using multiple AI tools in the same project, you need both files to contain identical instructions. Manually keeping them in sync is tedious and error-prone.

## The Solution

`claude-agents-sync` is a Claude Code hook that automatically synchronizes `CLAUDE.md` and `AGENTS.md` files:

- ✅ **Bidirectional sync**: Edit either file, the other updates instantly
- ✅ **Auto-discovery**: Automatically finds all pairs in your project
- ✅ **Zero maintenance**: Set it once, forget about it
- ✅ **Safe**: Only updates when content actually differs
- ✅ **Monorepo ready**: Handles multiple pairs in subdirectories
- ✅ **Silent operation**: Works in background, logs available if needed

---

## Quick Start

### 1. Installation

```bash
# Clone or download this repository
git clone https://github.com/YOUR_USERNAME/claude-agents-sync.git

# Copy .claude directory to your project
cp -r claude-agents-sync/.claude /path/to/your-project/

# Make scripts executable
chmod +x /path/to/your-project/.claude/hooks/*.sh
```

### 2. Configuration

Add to your `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-sync-claude-agents.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 3. Done!

Now whenever you edit `CLAUDE.md` or `AGENTS.md` in Claude Code, the other file updates automatically.

---

## How It Works

```
┌─────────────────────────────────────────────────┐
│  You edit CLAUDE.md in Claude Code             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  PostToolUse hook detects Edit operation       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  auto-sync-claude-agents.py                    │
│  • Checks if edited file is CLAUDE.md/AGENTS.md│
│  • Triggers sync if needed                      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  claude-agents-sync.py                         │
│  • Auto-discovers all pairs in project          │
│  • Finds matching pair for edited file          │
│  • Compares content (ignores whitespace)        │
│  • Copies to counterpart if different           │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  AGENTS.md is updated with CLAUDE.md content   │
│  ✅ Both files now identical                    │
└─────────────────────────────────────────────────┘
```

**Time taken:** < 1 second
**User interaction:** ZERO

---

## Features

### Auto-Discovery

No need to configure file pairs manually. The hook automatically scans your project and finds all `CLAUDE.md` files, creating sync pairs with corresponding `AGENTS.md` files.

**Example project structure:**

```
your-project/
├── CLAUDE.md           # ↔ Auto-paired with AGENTS.md
├── AGENTS.md
├── backend/
│   ├── CLAUDE.md      # ↔ Auto-paired with backend/AGENTS.md
│   └── AGENTS.md
└── frontend/
    ├── CLAUDE.md      # ↔ Auto-paired with frontend/AGENTS.md
    └── AGENTS.md
```

All three pairs are automatically discovered and kept in sync!

### Bidirectional Sync

Edit either `CLAUDE.md` or `AGENTS.md` - the other file updates automatically:

- `CLAUDE.md` → `AGENTS.md` ✅
- `AGENTS.md` → `CLAUDE.md` ✅

### Smart Comparison

Only updates files when content actually differs:
- Normalizes whitespace before comparing
- Skips unnecessary writes
- Logs when files are already in sync

### Logging

All operations are logged to `.claude/hooks/hook-debug.log`:

```
[2025-10-26 12:57:24] INFO: File change detected: CLAUDE.md
[2025-10-26 12:57:24] INFO: Auto-discovering CLAUDE.md/AGENTS.md pairs...
[2025-10-26 12:57:24] INFO: Found 3 file pair(s) in project
[2025-10-26 12:57:24] INFO: Processing synchronization for Root files
[2025-10-26 12:57:24] INFO: Successfully synchronized Root (CLAUDE.md → AGENTS.md)
[2025-10-26 12:57:24] INFO: Synchronization completed successfully
```

---

## Use Cases

### Single Project

Perfect for individual projects with one `CLAUDE.md`/`AGENTS.md` pair:

```
project/
├── .claude/hooks/...
├── CLAUDE.md
└── AGENTS.md
```

**Benefits:**
- Zero configuration needed
- Works out of the box
- Silent background operation

See [`examples/simple-project/`](examples/simple-project/) for details.

---

### Monorepo / Microservices

Perfect for monorepos with multiple components:

```
monorepo/
├── .claude/hooks/...
├── CLAUDE.md              # Root instructions
├── AGENTS.md
├── api/
│   ├── CLAUDE.md         # API-specific instructions
│   └── AGENTS.md
├── web/
│   ├── CLAUDE.md         # Web-specific instructions
│   └── AGENTS.md
└── mobile/
    ├── CLAUDE.md         # Mobile-specific instructions
    └── AGENTS.md
```

**Benefits:**
- All pairs automatically discovered
- Each component can have its own instructions
- Scales to any number of subdirectories

See [`examples/monorepo/`](examples/monorepo/) for details.

---

## Requirements

- **Claude Code**: Latest version with hooks support
- **Python 3**: Pre-installed on macOS/Linux, required for Windows

No additional dependencies needed!

---

## Comparison with Other Solutions

### vs. Manual Copying

| Manual Copying | claude-agents-sync |
|----------------|-------------------|
| ❌ Easy to forget | ✅ Automatic |
| ❌ Copy/paste errors | ✅ Guaranteed identical |
| ❌ Wastes time | ✅ Instant sync |

### vs. source-agents

[source-agents](https://github.com/iannuttall/source-agents) is an excellent alternative with a different philosophy:

| Feature | source-agents | claude-agents-sync |
|---------|--------------|-------------------|
| **Approach** | Sourcing pattern (`CLAUDE.md` → `@AGENTS.md`) | Content duplication |
| **Interaction** | Interactive TUI | Silent automatic |
| **Scope** | Multi-project governance | Single-project automation |
| **When to run** | Periodic (manual) | Real-time (automatic) |
| **Best for** | Managing 5+ projects | Daily work on one project |

**Both are great!** Choose based on your workflow:
- **Managing multiple projects?** → Use source-agents
- **Working on one project daily?** → Use claude-agents-sync

Read our [detailed comparison](https://docs.example.com/comparison) for more.

---

## Troubleshooting

### Hook not triggering?

Check your `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",  // ← Correct matcher
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-sync-claude-agents.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Scripts not executable?

```bash
chmod +x .claude/hooks/*.sh
```

### Want to see what's happening?

Check the log file:

```bash
tail -f .claude/hooks/hook-debug.log
```

### Sync not working for subdirectories?

Make sure:
1. Files are named exactly `CLAUDE.md` and `AGENTS.md` (case-sensitive)
2. They're in the same directory
3. You're editing them in Claude Code (not external editor)

---

## Architecture

### File Structure

```
.claude/
├── hooks/
│   ├── auto-sync-claude-agents.py  # PostToolUse hook entry point
│   ├── claude-agents-sync.py       # Core sync logic with auto-discovery
│   └── claude-agents-sync.sh       # Bash wrapper
└── settings.local.json              # Hook configuration
```

### Workflow

1. **Trigger**: Claude Code fires `PostToolUse` hook after `Edit` or `Write` operation
2. **Detection**: `auto-sync-claude-agents.py` receives JSON via stdin, checks if `CLAUDE.md` or `AGENTS.md` was edited
3. **Orchestration**: Calls `claude-agents-sync.sh` wrapper with file path
4. **Discovery**: `claude-agents-sync.py` scans project for all pairs
5. **Matching**: Finds pair containing the edited file
6. **Sync**: Compares content, updates counterpart if different
7. **Log**: Records result in `hook-debug.log`

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Credits

Inspired by the [source-agents](https://github.com/iannuttall/source-agents) project by [@iannuttall](https://github.com/iannuttall).

Built for teams using multiple AI coding assistants in harmony.

---

## Questions?

- 🐛 **Found a bug?** [Open an issue](https://github.com/YOUR_USERNAME/claude-agents-sync/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/YOUR_USERNAME/claude-agents-sync/discussions)
- 📖 **Need help?** Check the [examples](examples/) directory

---

**Happy coding with multiple AI assistants!** 🤖✨
