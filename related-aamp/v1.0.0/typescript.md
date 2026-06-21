import { AAMPClient } from '@larksuite/aamp';

const client = new AAMPClient({
  transport: 'smtp',
  address: 'agent-prod@example.com',
  mailbox: 'imaps://mail.example.com',
});

// Dispatch a task to another agent
await client.dispatch({
  to: 'builder-agent@example.com',
  task: {
    id: 'task-001',
    description: 'Run integration tests',
    priority: 'high',
  },
});

// Poll for results
const result = await client.poll('task-001');
console.log(result.status, result.output);
