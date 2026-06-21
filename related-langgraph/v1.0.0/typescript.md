import { StateGraph, Annotation } from "@langchain/langgraph";

// Define state
const AgentState = {
  messages: Annotation<{ role: string; content: string }[]>({
    reducer: (a, b) => a.concat(b),
  }),
  nextAgent: Annotation<string>(),
};

// Define nodes
const analyzer = async (state: typeof AgentState) => {
  const response = await callLLM("Analyze the request", state.messages);
  return { messages: [response], nextAgent: "planner" };
};

const planner = async (state: typeof AgentState) => {
  const response = await callLLM("Create a plan", state.messages);
  return { messages: [response], nextAgent: "__end__" };
};

// Build graph
const graph = new StateGraph(AgentState)
  .addNode("analyzer", analyzer)
  .addNode("planner", planner)
  .addEdge("analyzer", "planner")
  .addConditionalEdges("__start__", (s) => "analyzer")
  .compile();

// Run
const result = await graph.invoke({
  messages: [{ role: "user", content: "Build a REST API" }],
});
