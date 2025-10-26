#!/usr/bin/env python3
"""
Claude/Agents Files Synchronization Hook

This hook ensures that CLAUDE.md and AGENTS.md files stay synchronized across the entire project.
When changes are detected in either file, the corresponding counterpart is updated automatically.

Features:
- Auto-discovery: Automatically finds all CLAUDE.md/AGENTS.md pairs in the project
- Bidirectional sync: Edit either file, the other updates automatically
- Smart comparison: Only updates when content actually differs (ignores whitespace)
- Safe: Never overwrites if files are already in sync
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def log_message(message: str, level: str = "INFO") -> None:
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")
    sys.stdout.flush()

def calculate_file_hash(file_path: Path) -> Optional[str]:
    """Calculate MD5 hash of file content"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def find_all_sync_pairs(project_root: Path) -> List[Dict[str, any]]:
    """
    Auto-discover all CLAUDE.md/AGENTS.md pairs in the project.

    Returns a list of pairs with their paths and descriptive names.
    """
    pairs = []

    # Find all CLAUDE.md files in the project
    claude_files = list(project_root.rglob("CLAUDE.md"))

    for claude_file in claude_files:
        # Determine the corresponding AGENTS.md path
        agents_file = claude_file.parent / "AGENTS.md"

        # Calculate relative path for descriptive name
        try:
            relative_dir = claude_file.parent.relative_to(project_root)
            if str(relative_dir) == ".":
                name = "Root"
            else:
                name = str(relative_dir).replace("/", " > ")
        except ValueError:
            name = str(claude_file.parent)

        pairs.append({
            "source": claude_file,
            "target": agents_file,
            "name": name
        })

    # Also check for standalone AGENTS.md files (without corresponding CLAUDE.md)
    agents_files = list(project_root.rglob("AGENTS.md"))

    for agents_file in agents_files:
        claude_file = agents_file.parent / "CLAUDE.md"

        # Only add if CLAUDE.md doesn't exist (not already in pairs)
        if not claude_file.exists():
            try:
                relative_dir = agents_file.parent.relative_to(project_root)
                if str(relative_dir) == ".":
                    name = "Root"
                else:
                    name = str(relative_dir).replace("/", " > ")
            except ValueError:
                name = str(agents_file.parent)

            pairs.append({
                "source": agents_file,
                "target": claude_file,
                "name": name
            })

    return pairs

def should_sync_file(file_path: Path) -> bool:
    """Check if a file should trigger synchronization"""
    filename = file_path.name.upper()
    return filename in ["CLAUDE.MD", "AGENTS.MD"]

def find_pair_for_file(changed_file: Path, file_pairs: List[Dict]) -> Optional[Dict]:
    """Find the corresponding pair for a changed file"""
    changed_path = changed_file.resolve()

    for pair in file_pairs:
        source_path = Path(pair["source"]).resolve()
        target_path = Path(pair["target"]).resolve()

        if changed_path == source_path or changed_path == target_path:
            return pair

    return None

def normalize_content(text: str) -> str:
    """Normalize content for comparison (ignore whitespace differences)"""
    return '\n'.join(line.strip() for line in text.split('\n') if line.strip())

def synchronize_files(pair: Dict, changed_file: Path) -> bool:
    """Synchronize a pair of files"""
    source_path = Path(pair["source"])
    target_path = Path(pair["target"])
    changed_path = changed_file.resolve()

    log_message(f"Processing synchronization for {pair['name']} files")

    # Determine which file was changed and which needs to be updated
    if changed_path == source_path.resolve():
        source = source_path
        target = target_path
        direction = f"{source.name} → {target.name}"
    else:
        source = target_path
        target = source_path
        direction = f"{source.name} → {target.name}"

    # Verify source file exists
    if not source.exists():
        log_message(f"Source file {source} does not exist!", "ERROR")
        return False

    # Read source content
    try:
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        log_message(f"Error reading {source}: {e}", "ERROR")
        return False

    # If target exists, check if it actually needs updating
    if target.exists():
        try:
            with open(target, 'r', encoding='utf-8') as f:
                target_content = f.read()

            if normalize_content(content) == normalize_content(target_content):
                log_message(f"Files are already in sync ({direction})")
                return True
        except Exception as e:
            log_message(f"Error reading {target}: {e}", "ERROR")

    # Update target file
    try:
        # Ensure target directory exists
        target.parent.mkdir(parents=True, exist_ok=True)

        # Write the synchronized content
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)

        log_message(f"Successfully synchronized {pair['name']} ({direction})")
        log_message(f"Updated: {target}")

        return True

    except Exception as e:
        log_message(f"Error updating {target}: {e}", "ERROR")
        return False

def main() -> None:
    """Main hook function"""
    # Get the repository root directory
    repo_root = Path(__file__).parent.parent.parent

    # Get the changed file from environment variable or command line argument
    changed_file = os.environ.get('FILE_PATH', '')
    if len(sys.argv) > 1:
        changed_file = sys.argv[1]

    if not changed_file:
        log_message("No file path provided", "ERROR")
        sys.exit(1)

    # Convert to absolute path
    changed_file = Path(changed_file).resolve()

    log_message(f"File change detected: {changed_file}")

    # Check if this file should trigger synchronization
    if not should_sync_file(changed_file):
        log_message("File does not require synchronization")
        sys.exit(0)

    # Auto-discover all file pairs in the project
    log_message("Auto-discovering CLAUDE.md/AGENTS.md pairs...")
    file_pairs = find_all_sync_pairs(repo_root)

    if not file_pairs:
        log_message("No CLAUDE.md/AGENTS.md pairs found in project", "WARNING")
        sys.exit(0)

    log_message(f"Found {len(file_pairs)} file pair(s) in project")

    # Find the pair that contains the changed file
    pair = find_pair_for_file(changed_file, file_pairs)

    if not pair:
        log_message("No matching file pair found for changed file", "ERROR")
        sys.exit(1)

    # Perform synchronization
    success = synchronize_files(pair, changed_file)

    if success:
        log_message("Synchronization completed successfully")
        sys.exit(0)
    else:
        log_message("Synchronization failed", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
