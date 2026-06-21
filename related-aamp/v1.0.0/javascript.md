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
    description: 'Run integration tests for v2.1',
    priority: 'high',
    deadline: '2026-06-22T00:00:00Z',
  },
});

// Cancel a task
await client.cancel({ taskId: 'task-001' });

// Request human help
await client.helpNeeded({
  taskId: 'task-001',
  reason: 'Unexpected test failure in auth module',
  escalation: ['human-ops@example.com'],
});
