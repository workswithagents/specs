import { KnowledgeBundle } from "@google-cloud/okf";

const bundle = await KnowledgeBundle.load("./my-knowledge-bundle");

// Query concepts
const concept = bundle.getConcept("agent/identity");
console.log(`Title: ${concept.title}`);
console.log(`Description: ${concept.description}`);
console.log(`Related: ${concept.relatedConcepts}`);

// Enumerate bundle structure
for (const c of bundle.concepts()) {
  console.log(`${c.id}: ${c.title}`);
}

// Search across concepts
const results = bundle.search("verification protocol");
for (const r of results) {
  console.log(r.conceptId, r.relevance);
}
