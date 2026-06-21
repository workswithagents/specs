from agents import Agent, Runner, handoff

# Define specialized agents
code_agent = Agent(
    name="Code Agent",
    instructions="You write and review code.",
    model="gpt-4o",
    tools=[terminal_tool, file_tool],
)

review_agent = Agent(
    name="Review Agent",
    instructions="You review code for quality and security.",
    model="gpt-4o",
)

# Orchestrator agent with handoff targets
orchestrator = Agent(
    name="Orchestrator",
    instructions="You coordinate coding tasks.",
    handoffs=[
        handoff(code_agent, on_handoff="Sending to code agent..."),
        handoff(review_agent, on_handoff="Sending for review..."),
    ],
)

# Run the orchestrator
result = await Runner.run(
    orchestrator,
    input="Write a function to sort a list and get it reviewed.",
)
print(result.final_output)
