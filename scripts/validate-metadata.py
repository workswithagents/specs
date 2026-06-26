#!/usr/bin/env python3
"""Validate community script metadata.yaml files."""
import sys
from pathlib import Path

REQUIRED = ["agent_id", "title", "description", "tags"]
OPTIONAL = ["spec_versions", "tested_on", "tested_by", "ci_skip", "script_of_week_candidate"]
VALID_TAG_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789-_")

errors = []

for f in Path("reference/community").rglob("metadata.yaml"):
    try:
        import yaml
        meta = yaml.safe_load(f.read_text())
        if not isinstance(meta, dict):
            errors.append(f"{f}: not a valid YAML dict")
            continue
        for field in REQUIRED:
            if field not in meta:
                errors.append(f"{f}: missing required field '{field}'")
            elif not isinstance(meta[field], str) and field != "tags":
                errors.append(f"{f}: '{field}' must be a string")
        if "tags" in meta:
            if not isinstance(meta["tags"], list):
                errors.append(f"{f}: 'tags' must be a list")
            else:
                for tag in meta["tags"]:
                    if not all(c in VALID_TAG_CHARS for c in tag):
                        errors.append(f"{f}: tag '{tag}' contains invalid characters")
    except yaml.YAMLError as e:
        errors.append(f"{f}: YAML parse error: {e}")
    except Exception as e:
        errors.append(f"{f}: error: {e}")

if errors:
    for e in errors:
        print(e, file=sys.stderr)
    sys.exit(1)

print(f"All metadata valid ({len(list(Path('reference/community').rglob('metadata.yaml')))} files checked)")
