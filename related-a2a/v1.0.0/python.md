from a2a.client import A2AClient
from a2a.types import TaskSendParams, Message, Part, Task

async def main():
    client = A2AClient("http://agent-b.example.com")

    # Send task to another agent
    task: Task = await client.send_task(
        TaskSendParams(
            message=Message(
                role="user",
                parts=[Part.from_text("Analyze this dataset")],
            )
        )
    )

    # Poll for status
    status = await client.get_task(task.id)
    print(f"Status: {status.state}")

    # Subscribe to streaming updates
    async for event in client.subscribe(task.id):
        print(f"Update: {event}")
