import { A2AClient } from "@a2aproject/sdk";

const client = new A2AClient("http://agent-b.example.com");

const task = await client.sendTask({
  message: {
    role: "user",
    parts: [{ text: "Analyze this dataset" }],
  },
});

// Stream updates
for await (const event of client.subscribeToTask(task.id)) {
  console.log("Update:", event);
}
