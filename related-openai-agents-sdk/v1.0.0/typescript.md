// Conceptual TypeScript equivalent — SDK is Python-native
// OpenAI Agents SDK pattern: Agent + Runner + Handoffs

interface Agent {
  name: string;
  instructions: string;
  model: string;
  tools: Function[];
  handoffs: Agent[];
}

class Runner {
  static async run(agent: Agent, input: string): Promise<string> {
    let currentAgent = agent;
    let result = "";

    while (true) {
      // Call the LLM with current agent's instructions
      const response = await callLLM(currentAgent, input);
      
      // Handle handoffs
      if (response.handoffTo) {
        currentAgent = agent.handoffs.find(h => h.name === response.handoffTo)
          ?? currentAgent;
        continue;
      }

      result = response.output;
      break;
    }

    return result;
  }
}

// Usage
const codeAgent: Agent = {
  name: "CodeAgent",
  instructions: "You write and review code.",
  model: "gpt-4o",
  tools: [],
  handoffs: [],
};

const output = await Runner.run(codeAgent, "Write a sorting function");
