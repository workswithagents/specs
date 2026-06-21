# Open Knowledge Format (OKF)

**Version:** 0.1
**Status:** Published
**Layer:** L1 — Execution / Knowledge Context
**Steward:** Google Cloud
**License:** MIT (Apache 2.0)
**Repository:** https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf
**Specification:** https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

## Relationship to WWA

OKF is complementary to WWA specs. OKF defines a format for structured knowledge bundles using markdown files with YAML frontmatter, while WWA defines protocol semantics for agent communication and coordination. OKF content could carry WWA spec definitions — a skill manifest or compliance rule encoded in OKF format could be ingested by WWA-compliant agents. OKF operates at the knowledge representation layer (L1), which WWA builds upon.

## Architecture

OKF represents knowledge as a directory hierarchy of markdown files, each with YAML frontmatter metadata. Concepts form a tree, with cross-linking between related concepts. The format is designed to be both human-readable and machine-parseable. A reference agent can enrich OKF bundles using BigQuery, and an HTML visualizer renders the concept hierarchy for exploration. The format is intentionally simple — no custom binary formats or databases required.

## Features

- Markdown files with YAML frontmatter for structured metadata
- Concept directory hierarchy for knowledge organization
- Cross-linking between related concepts
- BigQuery enrichment agent for automated knowledge expansion
- HTML visualizer for interactive concept exploration
- Human-readable and machine-parseable
- 4.6k ★ on GitHub (June 2026)

## Governance

Created and maintained by Google Cloud under MIT license with Apache 2.0 compatibility. The specification is published as part of the GoogleCloudPlatform/knowledge-catalog repository. Development is open-source with community contributions accepted through standard GitHub pull requests.

## Examples

### Python (Reference Agent)
```python
from okf import KnowledgeBundle, Concept

bundle = KnowledgeBundle.load("./my-knowledge-bundle")

# Query concepts
concept = bundle.get_concept("agent/identity")
print(f"Title: {concept.title}")
print(f"Description: {concept.description}")
print(f"Related: {concept.related_concepts}")

# Enrich with BigQuery
enriched = bundle.enrich_with_bigquery(
    query="SELECT context FROM knowledge_base WHERE concept = @name",
    params={"name": concept.id}
)
```

### Shell (Bundle Structure)
```bash
# OKF bundle directory structure
my-knowledge-bundle/
├── okf.yaml                    # Bundle metadata
├── concepts/
│   ├── agent/
│   │   ├── identity.md         # Concept definition
│   │   └── capabilities.md
│   └── protocol/
│       ├── handoff.md
│       └── attestation.md
└── cross-references.yaml       # Explicit cross-links
```
