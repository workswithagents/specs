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
