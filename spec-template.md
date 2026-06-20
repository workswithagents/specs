---
id: your-spec-id
title: Your Spec Name
version: 0.1.0
status: Draft
authors: [Your Name]
date: YYYY-MM-DD
---

# Your Spec Name

## Status

**Draft** — this specification is under active development and may change substantially. Implementations SHOULD NOT rely on Draft specs in production.

## Abstract

One paragraph describing what this specification defines. What protocol, format, or framework does it establish? What problem domain does it address? Which layer(s) of the Agent OSI Model does it cover?

## Motivation

Why does this specification exist? What problem does it solve that existing specifications do not? Include:
- The specific gap or pain point
- Why existing specs are insufficient
- What use cases this enables
- Who benefits (agent developers, platform operators, end users)

## Specification

The detailed, normative specification content. Use [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) conventions for all requirements:

- **MUST** / **MUST NOT** — absolute requirements or prohibitions
- **SHOULD** / **SHOULD NOT** — strong recommendations
- **MAY** — optional features

### Example Section Structure

```
## 1. Overview
## 2. Terminology
## 3. Protocol
### 3.1. Initialization
### 3.2. Message Format
### 3.3. Error Handling
## 4. Implementation Guidance
## 5. Examples
```

### Required: Versioned Examples

Every new spec version MUST include matching implementation examples in a versioned directory alongside the spec file:

```
{spec-name}/
  v{version}/
    python.md    — complete Python implementation
    typescript.md — complete TypeScript implementation
    curl.md       — curl command examples
```

The spec file MUST include an `## Examples` section linking to these files. See existing specs for the format.

## Examples Stub

```markdown
---

## Examples

Implementation examples for this version:

| Language | File |
|----------|------|
| Python | [{spec-name}/v{version}/python.md]({spec-name}/v{version}/python.md) |
| TypeScript | [{spec-name}/v{version}/typescript.md]({spec-name}/v{version}/typescript.md) |
| cURL | [{spec-name}/v{version}/curl.md]({spec-name}/v{version}/curl.md) |
```

## Security Considerations

What are the security implications of this specification?

- Attack surface introduced
- Threat model considerations
- Required security properties (confidentiality, integrity, availability, non-repudiation)
- Mitigations and recommendations
- Privacy considerations

## References

- [Agent OSI Model](../agent-osi-model.md) — layered architecture framework
- [IACP](../iacp.md) — Inter-Agent Communication Protocol
- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- Other relevant specifications, RFCs, and standards
