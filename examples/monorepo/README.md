# Monorepo Example

This example shows how to use claude-agents-sync in a monorepo with multiple CLAUDE.md/AGENTS.md pairs.

## Project Structure

```
monorepo/
├── .claude/
│   ├── hooks/
│   │   ├── auto-sync-claude-agents.py
│   │   ├── claude-agents-sync.py
│   │   └── claude-agents-sync.sh
│   └── settings.local.json
├── CLAUDE.md                 # Root-level instructions
├── AGENTS.md
├── backend/
│   ├── CLAUDE.md            # Backend-specific instructions
│   └── AGENTS.md
├── frontend/
│   ├── CLAUDE.md            # Frontend-specific instructions
│   └── AGENTS.md
└── mobile/
    ├── CLAUDE.md            # Mobile-specific instructions
    └── AGENTS.md
```

## Installation

Same as simple project - the auto-discovery feature will automatically find all pairs!

1. Copy the `.claude/` directory to your monorepo root:
   ```bash
   cp -r /path/to/claude-agents-sync/.claude /path/to/your-monorepo/
   ```

2. Make scripts executable:
   ```bash
   chmod +x your-monorepo/.claude/hooks/*.sh
   ```

3. Add hook configuration to your `.claude/settings.local.json`

## How Auto-Discovery Works

The hook automatically scans your entire project and finds all `CLAUDE.md` files, then:
1. Looks for corresponding `AGENTS.md` in the same directory
2. Creates sync pairs for each location
3. Logs discovered pairs on first run

Example output:
```
[2025-10-26 12:00:00] INFO: Auto-discovering CLAUDE.md/AGENTS.md pairs...
[2025-10-26 12:00:00] INFO: Found 4 file pair(s) in project
[2025-10-26 12:00:00] INFO: Processing synchronization for Root files
[2025-10-26 12:00:00] INFO: Processing synchronization for backend files
[2025-10-26 12:00:00] INFO: Processing synchronization for frontend files
[2025-10-26 12:00:00] INFO: Processing synchronization for mobile files
```

## Benefits for Monorepos

- **Automatic**: No need to configure each pair manually
- **Scalable**: Add new subdirectories with CLAUDE.md/AGENTS.md anytime
- **Flexible**: Each component can have its own AI instructions
- **Consistent**: All pairs stay in sync automatically

## Use Case

Perfect for:
- Monorepo architectures
- Microservices projects
- Projects with multiple teams/components
- Large codebases with different contexts
