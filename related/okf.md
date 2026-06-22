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

### Problem

Agents need structured, machine-readable context to operate effectively — product documentation, API specs, organizational policies — but there's no standard format for packaging this knowledge. Developers dump markdown files into a folder with no metadata, no cross-linking, and no schema, forcing each agent to parse context differently. Knowledge bundles are ad-hoc, non-portable, and impossible to enrich programmatically.

### Solution

OKF defines a directory-based format where each concept is a markdown file with YAML frontmatter metadata, organized in a concept hierarchy with explicit cross-links between related concepts. It's both human-readable and machine-parseable — agents can navigate the concept tree, follow cross-references, and extract structured metadata without custom parsing. A BigQuery enrichment agent can automatically expand bundles with additional context, and an HTML visualizer makes the knowledge graph explorable by humans.

### When to use

- Packaging structured knowledge (docs, policies, API references) for agent consumption
- Building knowledge bases where concepts have hierarchical relationships and cross-references
- Programmatic knowledge enrichment workflows (e.g., augmenting docs with BigQuery data)
- Sharing knowledge bundles between agents in a standard, portable format

### When NOT to use

- Packaging executable skills or tools — use ASFS for skills or MCP for runtime tool invocation
- Simple, flat documentation without cross-references — plain markdown or llms.txt is sufficient
- Real-time knowledge retrieval — OKF is a file-based format; use a vector database for semantic search
- Website discovery of agent endpoints — use llms.txt or robots.txt for discovery; OKF is for content, not discovery

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA ASFS | Packaging executable skills with manifests and versioning | ASFS is for skills (code + metadata); OKF is for static knowledge (concepts + cross-links) |
| MCP Resources | Runtime access to tool-accessible data sources | MCP resources are live data; OKF is a file-based knowledge packaging format |
| llms.txt | Website-level agent discovery and content hints | llms.txt is for discovery and summarization; OKF is for full concept hierarchies with cross-links |

### What you lose without THIS spec

- No standard format for structured, cross-linked agent knowledge bundles
- Every agent project defines its own knowledge packaging format, preventing portability
- No built-in concept hierarchy or cross-referencing — knowledge is flat and hard to navigate programmatically
- No standard enrichment pipeline (BigQuery agent) for automatically expanding knowledge bundles

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
