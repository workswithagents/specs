# ASFS — TypeScript Example

Complete TypeScript implementation of ASFS — Agent Skill Format Standard (v1.0.0).

```typescript
/**
 * ASFS v1.0.0 — TypeScript Reference Implementation
 *
 * Implements: ASFS validation, Hermes → ASFS conversion, skill API client.
 */

// ── Types ────────────────────────────────────────────────────────

interface ASFSValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

interface ASFSSkill {
  name: string;
  version: string;
  description: string;
  tags: string[];
  triggers: string[];
  os: string[];
  deps?: string[];
}

// ── Validator ────────────────────────────────────────────────────

class ASFSValidator {
  private static REQUIRED_FIELDS = new Set([
    "name", "version", "description", "tags", "triggers", "os",
  ]);
  private static VALID_SECTIONS = new Set([
    "When to Use", "Steps", "Pitfalls", "Verification",
  ]);

  static validate(content: string): ASFSValidationResult {
    const errors: string[] = [];

    // Parse frontmatter
    const fmMatch = content.match(/^---\n(.*?)\n---/s);
    if (!fmMatch) {
      return { valid: false, errors: ["Missing YAML frontmatter"], warnings: [] };
    }

    const fmText = fmMatch[1];
    const foundFields = new Set<string>();

    for (const line of fmText.split("\n")) {
      const colonIdx = line.indexOf(":");
      if (colonIdx > 0) {
        foundFields.add(line.slice(0, colonIdx).trim());
      }
    }

    const missing = [...ASFSValidator.REQUIRED_FIELDS].filter(f => !foundFields.has(f));
    if (missing.length) {
      errors.push(`Missing required fields: ${missing.join(", ")}`);
    }

    // Check sections
    for (const section of ASFSValidator.VALID_SECTIONS) {
      if (!content.includes(`## ${section}`)) {
        errors.push(`Missing section: ## ${section}`);
      }
    }

    // Validate semver
    const versionLine = fmText.split("\n").find(l => l.trim().startsWith("version:"));
    if (versionLine) {
      const version = versionLine.split(":")[1].trim();
      if (!/^\d+\.\d+\.\d+$/.test(version)) {
        errors.push(`Invalid version '${version}'. Must be semver (x.y.z)`);
      }
    }

    // Validate name
    const nameLine = fmText.split("\n").find(l => l.trim().startsWith("name:"));
    if (nameLine) {
      const name = nameLine.split(":")[1].trim();
      if (name.length > 64) errors.push(`Name exceeds 64 characters`);
      if (!/^[a-z0-9-]+$/.test(name)) errors.push(`Name must be lowercase-hyphens`);
    }

    return { valid: errors.length === 0, errors, warnings: [] };
  }
}

// ── Converter ────────────────────────────────────────────────────

class HermesToASFSConverter {
  private static HERMES_ONLY = new Set([
    "hermes", "metadata", "related_skills", "category", "prerequisites", "author",
  ]);

  static convert(skillMd: string): string {
    const lines = skillMd.split("\n");
    const output: string[] = [];
    let inFm = false;
    let fmStarted = false;

    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed === "---" && !fmStarted) {
        fmStarted = true;
        inFm = true;
        output.push(line);
        continue;
      }
      if (inFm && trimmed === "---") {
        inFm = false;
        output.push(line);
        continue;
      }
      if (inFm && line.includes(":")) {
        const key = trimmed.split(":")[0].trim();
        if (HermesToASFSConverter.HERMES_ONLY.has(key)) continue;
      }
      output.push(line);
    }
    return output.join("\n");
  }
}

// ── Client ───────────────────────────────────────────────────────

class ASFSClient {
  constructor(private apiBase: string = "https://workswithagents.dev") {}

  private async get<T>(path: string, params?: Record<string, string>): Promise<T> {
    let url = `${this.apiBase}${path}`;
    if (params) {
      const qs = new URLSearchParams(params).toString();
      url += `?${qs}`;
    }
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    if (!res.ok) throw new Error(`ASFS error (${res.status})`);
    return res.json() as Promise<T>;
  }

  async listSkills(tag?: string): Promise<ASFSSkill[]> {
    return this.get("/v1/skills", tag ? { tag } : undefined);
  }

  async getSkill(skillName: string): Promise<string> {
    const res = await fetch(`${this.apiBase}/v1/skills/${skillName}`);
    return res.text();
  }

  async search(query: string): Promise<ASFSSkill[]> {
    return this.get("/v1/skills/search", { q: query });
  }
}

// ── Demo ─────────────────────────────────────────────────────────

async function main() {
  console.log("=== ASFS v1.0.0 Demo ===\n");

  // 1. Validate
  const sampleSkill = `---
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

1. Read the traceback
2. Identify error type/location
3. Apply fix
4. Re-run

## Pitfalls

- Don't suppress exceptions without handling

## Verification

Run \`python3 script.py\` and confirm no errors.
`;

  console.log("1. Validating ASFS skill:");
  const result = ASFSValidator.validate(sampleSkill);
  console.log(`   Valid: ${result.valid}`);
  for (const e of result.errors) console.log(`   ✗ ${e}`);
  if (result.valid) console.log("   ✓ All checks passed");

  // 2. Convert
  console.log("\n2. Hermes → ASFS conversion:");
  const hermesSkill = `---
name: my-skill
version: 1.0.0
description: Sample
tags: [example]
triggers: ["test"]
os: [linux]
hermes: "extra"
author: "Vilius"
related_skills: ["other"]
---

# Content
`;
  const converted = HermesToASFSConverter.convert(hermesSkill);
  console.log("   Hermes-only fields stripped");
  console.log(`   Result: ${converted.split("---")[1].length} chars`);

  // 3. Client
  console.log("\n3. Listing skills...");
  const client = new ASFSClient();
  try {
    const skills = await client.listSkills("python");
    console.log(`   Found ${skills.length} skill(s)`);
    for (const s of skills.slice(0, 3)) {
      console.log(`   - ${s.name}: ${s.description.slice(0, 60)}`);
    }
  } catch (e) {
    console.log(`   API call (offline): ${(e as Error).message}`);
  }

  console.log("\n=== Demo Complete ===");
}

main().catch(console.error);
```
