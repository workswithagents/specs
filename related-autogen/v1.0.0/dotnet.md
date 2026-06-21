using Microsoft.AutoGen.Agents;
using Microsoft.AutoGen.Teams;
using Microsoft.AutoGen.Models;

var modelClient = new OpenAIChatCompletionClient(model: "gpt-4o");

// Define agents
var codeAgent = new AssistantAgent(
    name: "code_agent",
    modelClient: modelClient,
    systemMessage: "You write C# code. Output code blocks."
);

var reviewerAgent = new AssistantAgent(
    name: "reviewer_agent",
    modelClient: modelClient,
    systemMessage: "You review code and suggest improvements."
);

// Create a team with round-robin coordination
var team = new RoundRobinGroupChat(
    new[] { codeAgent, reviewerAgent },
    maxTurns: 6
);

// Run the team
var result = await team.RunAsync(
    task: "Write a function to merge two sorted lists"
);

Console.WriteLine($"Final result: {result.Messages[^1].Content}");
