# ASFS — Python Example

Complete Python implementation of ASFS — Agent Skill Format Standard (v1.0.0). Stdlib only.

```python
"""
ASFS v1.0.0 — Agent Skill Format Standard Reference Implementation

Implements:
  - ASFS skill validation
  - Hermes → ASFS converter
  - ASFS skill loading and parsing
  - Skill discovery via API
Stdlib only. No dependencies required.
"""
import json
import re
import urllib.request
import urllib.error
from typing import Optional


class ASFSValidator:
    """Validate an ASFS skill file."""

    REQUIRED_FIELDS = {"name", "version", "description",
                       "tags", "triggers", "os"}
    VALID_SECTIONS = {"When to Use", "Steps", "Pitfalls", "Verification"}

    @staticmethod
    def validate(content: str) -> dict:
        """Validate an ASFS skill and return errors if any."""
        errors = []

        # Parse frontmatter
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            return {"valid": False, "errors": ["Missing YAML frontmatter"]}

        fm_text = fm_match.group(1)

        # Check required fields
        found_fields = set()
        for line in fm_text.split("\n"):
            if ":" in line:
                key = line.split(":")[0].strip()
                found_fields.add(key)

        missing = ASFSValidator.REQUIRED_FIELDS - found_fields
        if missing:
            errors.append(f"Missing required fields: {sorted(missing)}")

        # Check required sections
        body = content[fm_match.end():]
        for section in ASFSValidator.VALID_SECTIONS:
            if f"## {section}" not in content:
                errors.append(f"Missing section: ## {section}")

        # Validate version format (semver)
        version_line = [l for l in fm_text.split("\n")
                        if l.strip().startswith("version:")]
        if version_line:
            version = version_line[0].split(":", 1)[1].strip()
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                errors.append(f"Invalid version '{version}'. Must be semver (x.y.z)")

        # Validate name format
        name_line = [l for l in fm_text.split("\n")
                     if l.strip().startswith("name:")]
        if name_line:
            name = name_line[0].split(":", 1)[1].strip()
            if len(name) > 64:
                errors.append(f"Name '{name}' exceeds 64 characters")
            if not re.match(r'^[a-z0-9-]+$', name):
                errors.append(f"Name '{name}' must be lowercase, hyphens, alphanumeric")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": []
        }


class HermesToASFSConverter:
    """Convert Hermes SKILL.md to ASFS format."""

    HERMES_ONLY_KEYS = {"hermes", "metadata", "related_skills",
                        "category", "prerequisites", "author"}

    @staticmethod
    def convert(skill_md: str) -> str:
        """Strip Hermes-specific frontmatter, keep ASFS-compatible fields."""
        lines = skill_md.split("\n")
        output = []
        in_fm = False
        fm_started = False

        for line in lines:
            stripped = line.strip()
            if stripped == "---" and not fm_started:
                fm_started = True
                in_fm = True
                output.append(line)
                continue
            if in_fm and stripped == "---":
                in_fm = False
                output.append(line)
                continue
            if in_fm and ":" in line:
                key = stripped.split(":")[0].strip()
                if key in HermesToASFSConverter.HERMES_ONLY_KEYS:
                    continue
            output.append(line)

        return "\n".join(output)


class ASFSClient:
    """ASFS skill API client."""

    def __init__(self, api_base: str = "https://workswithagents.dev"):
        self.api_base = api_base.rstrip("/")

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self.api_base}{path}"
        if params:
            qs = "&".join(f"{k}={urllib.request.quote(str(v))}"
                          for k, v in params.items() if v)
            url += f"?{qs}"
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())

    def list_skills(self, tag: Optional[str] = None) -> list[dict]:
        """List all available ASFS skills, optionally filtered by tag."""
        params = {"tag": tag} if tag else None
        return self._get("/v1/skills", params)

    def get_skill(self, skill_name: str) -> str:
        """Download a skill in ASFS format."""
        url = f"{self.api_base}/v1/skills/{skill_name}"
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode()

    def search(self, query: str) -> list[dict]:
        """Search skills by name or description."""
        return self._get("/v1/skills/search", {"q": query})


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== ASFS v1.0.0 Demo ===\n")

    # 1. Validate an ASFS skill
    sample_skill = """---
name: python-debugging
version: 1.0.0
description: Debug Python tracebacks and common errors
tags: [python, debugging, cli]
triggers:
  - "debug python"
  - "traceback"
os: [linux, macos, windows]
deps: [python3]
---

# Python Debugging

## When to Use

When you encounter a Python traceback or need to debug a script.

## Steps

1. Read the traceback carefully
2. Identify the error type and location
3. Apply the fix
4. Re-run to verify

## Pitfalls

- Don't suppress exceptions without handling them
- Check Python version compatibility

## Verification

Run `python3 script.py` and confirm no errors.
"""

    print("1. Validating a sample ASFS skill:")
    result = ASFSValidator.validate(sample_skill)
    print(f"   Valid: {result['valid']}")
    if result['errors']:
        for e in result['errors']:
            print(f"   ✗ {e}")
    else:
        print("   ✓ All checks passed")

    # 2. Convert Hermes skill to ASFS
    hermes_skill = """---
name: my-skill
version: 1.0.0
description: A sample skill
tags: [example]
triggers: ["test"]
os: [linux, macos]
hermes: "extra-field"
author: "Vilius"
related_skills: ["other-skill"]
---

# My Skill

Content here.
"""
    print("\n2. Converting Hermes skill to ASFS:")
    converted = HermesToASFSConverter.convert(hermes_skill)
    print(f"   Hermes-only fields stripped: 'hermes', 'author', 'related_skills'")
    print(f"   Resulting frontmatter length: {len(converted.split('---')[1])} chars")

    # 3. Client: list skills
    print("\n3. Listing available skills...")
    client = ASFSClient()
    try:
        skills = client.list_skills(tag="python")
        print(f"   Found {len(skills)} skill(s)")
        for s in skills[:3]:
            print(f"   - {s.get('name', 'unknown')}: {s.get('description', '')[:60]}")
    except Exception as e:
        print(f"   API call (offline): {e}")

    # 4. Search skills
    print("\n4. Searching skills...")
    try:
        results = client.search("debugging")
        print(f"   Found {len(results)} result(s)")
    except Exception as e:
        print(f"   API call (offline): {e}")

    print("\n=== Demo Complete ===")
```
