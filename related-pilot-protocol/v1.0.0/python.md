import asyncio
from pilot_protocol import Node, Config

async def main():
    # Create a new agent node on the P2P overlay
    node = await Node.create(Config(
        listen_addr=":0",       # random UDP port
        virtual_addr="alice.agent",
    ))

    # Discover and communicate with another agent
    peer = await node.discover("bob.agent")
    if peer:
        response = await node.send(peer, {
            "type": "task_request",
            "payload": {"description": "Compute hash"},
        })
        print(f"Response from bob: {response}")

    await node.close()

asyncio.run(main())
