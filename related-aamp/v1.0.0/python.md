from aamp import AAMPClient

client = AAMPClient(
    transport="smtp",
    address="agent-prod@example.com",
    mailbox="imaps://mail.example.com",
)

client.dispatch(
    to="builder-agent@example.com",
    task={
        "id": "task-001",
        "description": "Run integration tests for v2.1",
        "priority": "high",
    }
)
