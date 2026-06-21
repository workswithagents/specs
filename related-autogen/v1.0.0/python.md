from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o")

# Define agents
code_agent = AssistantAgent(
    name="code_agent",
    model_client=model_client,
    system_message="You write Python code. Output code blocks.",
)

reviewer_agent = AssistantAgent(
    name="reviewer_agent",
    model_client=model_client,
    system_message="You review code and suggest improvements.",
)

# Create a team with round-robin coordination
team = RoundRobinGroupChat(
    [code_agent, reviewer_agent],
    max_turns=6,
)

# Run the team
async def main():
    result = await Console(
        team.run_stream(task="Write a function to merge two sorted lists")
    )
    print(f"Final result: {result.messages[-1].content}")

# import asyncio; asyncio.run(main())
