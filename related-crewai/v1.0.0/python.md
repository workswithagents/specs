from crewai import Agent, Task, Crew, Process

# Define agents with roles
code_agent = Agent(
    role="Senior Python Developer",
    goal="Write clean, tested, production-ready Python code",
    backstory="You are a developer with 15 years of experience.",
    allow_code_execution=True,
)

review_agent = Agent(
    role="Code Reviewer",
    goal="Review code for bugs, security issues, and style violations",
    backstory="You catch issues others miss.",
)

architect_agent = Agent(
    role="Software Architect",
    goal="Design system architecture and delegate implementation",
    backstory="You design scalable systems.",
    allow_delegation=True,
)

# Define tasks
design_task = Task(
    description="Design a REST API for a task management system",
    expected_output="Architecture diagram and API specification",
    agent=architect_agent,
)

code_task = Task(
    description="Implement the REST API per the architecture design",
    expected_output="Working FastAPI application with tests",
    agent=code_agent,
)

review_task = Task(
    description="Review the implemented API code",
    expected_output="Review report with findings",
    agent=review_agent,
)

# Assemble the crew in hierarchical mode
crew = Crew(
    agents=[architect_agent, code_agent, review_agent],
    tasks=[design_task, code_task, review_task],
    process=Process.hierarchical,
    verbose=True,
)

result = crew.kickoff()
print(result)
