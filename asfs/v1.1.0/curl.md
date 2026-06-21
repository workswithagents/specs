# ASFS — cURL Examples

cURL command examples for ASFS — Agent Skill Format Standard (v1.0.0).

## 1. List All Skills

```bash
curl https://workswithagents.dev/v1/skills \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
[
  {
    "name": "spfx-local-dev",
    "version": "1.0.0",
    "description": "Local SharePoint Framework development workflow",
    "tags": ["spfx", "sharepoint", "typescript"],
    "triggers": ["build:spfx", "spfx error"],
    "os": ["linux", "macos", "windows"]
  }
]
```

## 2. List Skills by Tag

```bash
curl "https://workswithagents.dev/v1/skills?tag=python" \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
[
  {"name": "python-debugging", "version": "1.0.0", "description": "Debug Python tracebacks"},
  {"name": "python-testing", "version": "1.1.0", "description": "Write and run Python tests"}
]
```

## 3. Download a Skill (ASFS Format)

```bash
curl https://workswithagents.dev/v1/skills/python-debugging \
  -H "Accept: text/markdown" \
  -o python-debugging.asfs.md
```

## 4. Search Skills

```bash
curl "https://workswithagents.dev/v1/skills/search?q=debugging" \
  -H "Accept: application/json"
```

## 5. Validate a Skill

```bash
curl -X POST https://workswithagents.dev/v1/skills/validate \
  -H "Content-Type: text/markdown" \
  --data-binary @my-skill.asfs.md
```

**Expected response (200 OK):**
```json
{
  "valid": true,
  "name": "my-skill",
  "version": "1.0.0",
  "errors": [],
  "warnings": []
}
```

**Invalid skill response:**
```json
{
  "valid": false,
  "errors": [
    "Missing required fields: ['triggers']",
    "Missing section: ## Pitfalls"
  ]
}
```

## 6. Convert Hermes Skill to ASFS

```bash
curl -X POST https://workswithagents.dev/v1/skills/convert \
  -H "Content-Type: text/markdown" \
  --data-binary @~/.hermes/skills/my-skill/SKILL.md \
  -o my-skill.asfs.md
```

**Expected response (200 OK):**
```markdown
---
name: my-skill
version: 1.0.0
description: My skill description
tags: [python]
triggers: ["trigger phrase"]
os: [linux, macos]
---
# My Skill
...
```

## 7. Publish a Skill

```bash
curl -X POST https://workswithagents.dev/v1/skills/publish \
  -H "Content-Type: text/markdown" \
  --data-binary @my-skill.asfs.md
```

**Expected response (201 Created):**
```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "published_at": "2026-06-20T12:00:00Z",
  "url": "https://workswithagents.dev/v1/skills/my-skill"
}
```

## Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/skills` | GET | List all skills (optional `?tag=`) |
| `/v1/skills/search?q=` | GET | Search skills |
| `/v1/skills/{name}` | GET | Download skill as ASFS markdown |
| `/v1/skills/validate` | POST | Validate an ASFS skill |
| `/v1/skills/convert` | POST | Convert Hermes → ASFS |
| `/v1/skills/publish` | POST | Publish a new skill |
