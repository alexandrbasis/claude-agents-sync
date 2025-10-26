# Simple Project Example

This example shows the minimal setup for a single project with one CLAUDE.md/AGENTS.md pair.

## Project Structure

```
your-project/
├── .claude/
│   ├── hooks/
│   │   ├── auto-sync-claude-agents.py
│   │   ├── claude-agents-sync.py
│   │   └── claude-agents-sync.sh
│   └── settings.local.json
├── CLAUDE.md
└── AGENTS.md
```

## Installation

1. Copy the `.claude/` directory to your project root:
   ```bash
   cp -r /path/to/claude-agents-sync/.claude /path/to/your-project/
   ```

2. Make scripts executable:
   ```bash
   chmod +x your-project/.claude/hooks/*.sh
   ```

3. Add hook configuration to your `.claude/settings.local.json`:
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

## How It Works

- Edit `CLAUDE.md` → `AGENTS.md` updates automatically
- Edit `AGENTS.md` → `CLAUDE.md` updates automatically
- Works in real-time as you edit files in Claude Code
- Silent background operation (check `.claude/hooks/hook-debug.log` for details)

## Use Case

Perfect for:
- Single codebase projects
- Teams using both Claude Code and Cursor
- Developers who want zero-maintenance sync
