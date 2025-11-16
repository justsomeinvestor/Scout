# Claude-to-Claude Coordination API

**Seamless inter-Claude communication via REST API**

This coordination API enables Windows Claude and Server Claude to exchange tasks, share results, and coordinate work through a unified REST interface built into the main Express API.

---

## Quick Start

### Message Types

The coordination API supports two message types:

- **💬 chat** - Direct communication between Claude instances
  - Used for status updates, questions, acknowledgments
  - No execution required, just read and acknowledge

- **📋 task** - Work requests requiring execution
  - Used for scraping, analysis, data processing
  - Requires: claim → execute → complete workflow

### For Windows Claude (Sending Tasks)

```typescript
import { sendTask, getPendingTasks } from './coordinationClient';

// Send a TASK (requires execution)
const task = await sendTask(
  'Scrape latest RSS feeds for market data',
  'Need articles from financial sources published in last 24h',
  'server_backend',
  'windows_frontend',
  'task'  // Message type
);
console.log(`Sent task: ${task.id}`);

// Send a CHAT message (just communication)
const chat = await sendTask(
  'Workflow complete, dashboard updated',
  'All data processed successfully',
  'server_backend',
  'windows_frontend',
  'chat'  // Message type
);

// Check if Server Claude completed it
const response = await getPendingTasks('server_backend');
// ... monitor for completion
```

### For Server Claude (Processing Tasks)

```typescript
import { getPendingTasks, completeTask, claimTask } from './coordinationClient';

// Get pending tasks
const tasks = await getPendingTasks('server_backend');

for (const task of tasks) {
  // Claim the task to prevent others from processing it
  await claimTask(task.id);

  try {
    // Execute the task
    const result = await executeTask(task.task);

    // Report completion
    await completeTask(task.id, result);
  } catch (error) {
    // Report failure
    await completeTask(task.id, error.message, 'failed');
  }
}
```

---

## Architecture Overview

### Database-Backed Storage
- Coordination messages stored in `coordination_messages` SQLite table
- Persists across restarts
- Enables historical tracking and audit logs
- Part of existing `data/etf_data.db`

### Message Lifecycle

```
[Windows Claude]
      ↓
  sendTask()
      ↓
  POST /api/coord/message
      ↓
  [Database: pending]
      ↓
[Server Claude]
  getPendingTasks()
      ↓
  claimTask()  (status → in_progress)
      ↓
  [Execute task...]
      ↓
  completeTask()  (status → complete/failed)
      ↓
  [Windows Claude]
  checks for completed task
      ↓
  getMessage() or deleteMessage()
```

---

## Configuration

### Environment Variables

```bash
# .env or system environment

# Target API URL (defaults to localhost:3000)
COORDINATION_API_URL=http://localhost:3000/api/coord

# This Claude instance's identifier
CLAUDE_ID=windows_frontend  # or 'server_backend'
```

### At Runtime

Set before importing coordination modules:

```typescript
process.env.COORDINATION_API_URL = 'http://192.168.10.56:3000/api/coord';
process.env.CLAUDE_ID = 'server_backend';
```

---

## API Reference

### Core Endpoints

All endpoints use base URL: `http://localhost:3000/api/coord`

#### 1. Send a Task
```
POST /api/coord/message

Request:
{
  "from_claude": "windows_frontend",
  "to_claude": "server_backend",
  "task": "Run YouTube scraper for latest videos",
  "context": "Looking for market analysis from top 5 channels",
  "type": "task"  // or "chat"
}

Response (201 Created):
{
  "success": true,
  "data": {
    "id": "a1b2c3d4e5f6...",
    "from_claude": "windows_frontend",
    "to_claude": "server_backend",
    "task": "Run YouTube scraper for latest videos",
    "context": "Looking for market analysis from top 5 channels",
    "type": "task",
    "status": "pending",
    "created_at": "2025-11-15T10:30:00Z",
    "updated_at": "2025-11-15T10:30:00Z"
  }
}
```

#### 2. Get Pending Messages
```
GET /api/coord/messages?to_claude=server_backend&status=pending

Query Parameters:
  - to_claude: Filter by recipient (optional)
  - status: Filter by status: pending|in_progress|complete|failed (optional)
  - limit: Results per page (default: 100)
  - offset: Pagination offset (default: 0)

Response:
{
  "success": true,
  "count": 3,
  "data": [
    { ... message objects ... }
  ]
}
```

#### 3. Get Specific Message
```
GET /api/coord/message/:id

Response (200 if found, 404 if not):
{
  "success": true,
  "data": { ... message object ... }
}
```

#### 4. Update Message Status
```
PUT /api/coord/message/:id

Request:
{
  "status": "in_progress",  // or "complete", "failed"
  "result": "Scraped 150 articles from 6 feeds",  // optional
  "error": "Connection timeout"  // optional
}

Response:
{
  "success": true,
  "data": { ... updated message object ... }
}
```

#### 5. Delete Message
```
DELETE /api/coord/message/:id

Response:
{
  "success": true,
  "message": "Message deleted: a1b2c3d4e5f6..."
}
```

#### 6. Get Statistics
```
GET /api/coord/stats

Response:
{
  "success": true,
  "data": {
    "total": 145,
    "pending": 3,
    "in_progress": 1,
    "complete": 140,
    "failed": 1
  }
}
```

#### 7. Heartbeat (Keep-Alive)
```
POST /api/coord/heartbeat

Request:
{
  "claude_id": "server_backend"
}

Response:
{
  "success": true,
  "timestamp": "2025-11-15T10:35:20Z",
  "claude_id": "server_backend"
}
```

---

## Client Library Reference

### coordinationClient.ts

#### Functions

##### `sendTask(task, context?, to?, from?)`
Send a task to another Claude instance
- **Parameters:**
  - `task` (string): Task description
  - `context` (string, optional): Additional context
  - `to` (string, default: 'server_backend'): Target Claude
  - `from` (string, default: CLAUDE_ID env var): Sender
- **Returns:** Promise<CoordinationMessage>
- **Example:**
```typescript
const msg = await sendTask('Scrape ETF data', 'SPY and QQQ');
console.log(msg.id); // Task ID for tracking
```

##### `getPendingTasks(forClaude?)`
Get pending tasks for a Claude instance
- **Parameters:**
  - `forClaude` (string, default: CLAUDE_ID): Target Claude
- **Returns:** Promise<CoordinationMessage[]>
- **Example:**
```typescript
const tasks = await getPendingTasks('server_backend');
for (const task of tasks) {
  console.log(`Task: ${task.task}`);
}
```

##### `getAllMessages(status?)`
Get all messages, optionally filtered by status
- **Parameters:**
  - `status` (string, optional): 'pending'|'in_progress'|'complete'|'failed'
- **Returns:** Promise<CoordinationMessage[]>
- **Example:**
```typescript
const completed = await getAllMessages('complete');
console.log(`Completed tasks: ${completed.length}`);
```

##### `getMessage(messageId)`
Get a specific message by ID
- **Parameters:**
  - `messageId` (string): Message ID
- **Returns:** Promise<CoordinationMessage>
- **Example:**
```typescript
const msg = await getMessage('a1b2c3d4e5f6');
console.log(msg.status); // Check if it's complete yet
```

##### `claimTask(messageId)`
Mark a task as in_progress
- **Parameters:**
  - `messageId` (string): Message ID
- **Returns:** Promise<CoordinationMessage>
- **Example:**
```typescript
await claimTask(task.id);
// Now execute the task...
```

##### `completeTask(messageId, result, status?)`
Mark task as complete or failed with result
- **Parameters:**
  - `messageId` (string): Message ID
  - `result` (string): Result/output of the task
  - `status` (default: 'complete'): 'complete' or 'failed'
- **Returns:** Promise<CoordinationMessage>
- **Example:**
```typescript
// Success
await completeTask(task.id, 'Scraped 250 ETF records');

// Failure
await completeTask(task.id, 'API rate limited', 'failed');
```

##### `deleteMessage(messageId)`
Delete a message (typically after processing)
- **Parameters:**
  - `messageId` (string): Message ID
- **Returns:** Promise<boolean>
- **Example:**
```typescript
const deleted = await deleteMessage(task.id);
```

##### `startHeartbeat(claudeId?, interval?)`
Start periodic heartbeat to signal this Claude is alive
- **Parameters:**
  - `claudeId` (default: CLAUDE_ID): Instance identifier
  - `interval` (default: 30000): Milliseconds between heartbeats
- **Returns:** void
- **Example:**
```typescript
startHeartbeat('server_backend', 30000);
// Runs every 30 seconds until stopHeartbeat() is called
```

##### `stopHeartbeat()`
Stop the periodic heartbeat
- **Returns:** void

##### `testCoordinationAPI()`
Test if coordination API is reachable
- **Returns:** Promise<boolean>
- **Example:**
```typescript
const isAvailable = await testCoordinationAPI();
if (!isAvailable) {
  throw new Error('Coordination API not responding');
}
```

---

## Workflow Examples

### Example 1: Windows → Server Task Dispatch

**Windows Claude:**
```typescript
import { sendTask, getMessage } from './coordinationClient';

async function dispatchWork() {
  // Send task
  const task = await sendTask(
    'Scrape RSS feeds',
    'Get latest financial news articles'
  );

  console.log(`Sent task ${task.id}`);

  // Poll for completion (in real code, use better polling)
  let completed = false;
  for (let i = 0; i < 60; i++) {
    const msg = await getMessage(task.id);

    if (msg.status === 'complete') {
      console.log(`Task completed: ${msg.result}`);
      completed = true;
      break;
    } else if (msg.status === 'failed') {
      console.error(`Task failed: ${msg.error}`);
      break;
    }

    await new Promise(r => setTimeout(r, 5000)); // Wait 5s
  }
}
```

**Server Claude:**
```typescript
import { getPendingTasks, claimTask, completeTask } from './coordinationClient';

async function processWork() {
  process.env.CLAUDE_ID = 'server_backend';

  while (true) {
    const tasks = await getPendingTasks('server_backend');

    for (const task of tasks) {
      try {
        await claimTask(task.id);

        // Execute task
        let result;
        if (task.task.includes('RSS')) {
          result = await scrapeRSSFeeds(task.context);
        } else if (task.task.includes('ETF')) {
          result = await scrapeETFData(task.context);
        }

        await completeTask(task.id, result);
      } catch (error) {
        await completeTask(
          task.id,
          error.message,
          'failed'
        );
      }
    }

    // Check every 10 seconds
    await new Promise(r => setTimeout(r, 10000));
  }
}
```

### Example 2: Heartbeat Monitoring

```typescript
import { startHeartbeat, stopHeartbeat } from './coordinationClient';

// Start server
const server = app.listen(3000, () => {
  // Signal that this Claude is running
  startHeartbeat('server_backend', 30000);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down...');
  stopHeartbeat();
  server.close();
});
```

### Example 3: Batch Task Processing

```typescript
import { getPendingTasks, completeTask, claimTask } from './coordinationClient';

async function processBatch() {
  const tasks = await getPendingTasks('server_backend');

  console.log(`Processing ${tasks.length} pending tasks`);

  let completed = 0;
  let failed = 0;

  for (const task of tasks) {
    try {
      await claimTask(task.id);

      // Execute with timeout
      const result = await Promise.race([
        executeTask(task),
        timeout(5 * 60 * 1000) // 5 minute timeout
      ]);

      await completeTask(task.id, result);
      completed++;
    } catch (error) {
      await completeTask(task.id, error.message, 'failed');
      failed++;
    }
  }

  console.log(`Completed: ${completed}, Failed: ${failed}`);
}
```

---

## Error Handling

### Common Errors

**API Not Running**
```
Error: Coordination API server not running
→ Solution: Ensure `npm run api` is running and API_URL is correct
```

**Message Not Found**
```
Error: Message not found
→ May occur if message was deleted
→ Check that message ID is correct
```

**Invalid Status**
```
Error: Invalid status. Must be one of: pending, in_progress, complete, failed
→ Use one of the valid status values
```

### Retry Logic

```typescript
async function sendTaskWithRetry(
  task: string,
  maxRetries: number = 3
): Promise<CoordinationMessage> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await sendTask(task);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1))); // Exponential backoff
    }
  }
  throw new Error('Failed to send task after retries');
}
```

---

## Performance Considerations

### Rate Limiting
- No built-in rate limiting on coordination endpoints
- Consider implementing in production
- ~10-50 tasks per second per instance is reasonable

### Database Size
- Each message: ~500-1000 bytes depending on content
- 1000 messages: ~1MB
- Old messages can be deleted with DELETE endpoint
- Consider archival if message volume gets large

### Polling vs WebSocket
- Current implementation uses REST polling
- For real-time coordination, consider WebSocket upgrade
- Polling interval: 5-10 seconds is reasonable balance

---

## Deployment

### Running Both Claudes

**Terminal 1 - Start API Server:**
```bash
npm run api
```

**Terminal 2 - Windows Claude (this instance):**
- Set `CLAUDE_ID=windows_frontend`
- Can call coordination endpoints directly

**Terminal 3 - Server Claude (remote instance):**
- Set `CLAUDE_ID=server_backend`
- Set `COORDINATION_API_URL=http://192.168.10.56:3000/api/coord`
- Monitor and process tasks

### Docker/Container Support

```dockerfile
ENV COORDINATION_API_URL=http://api-server:3000/api/coord
ENV CLAUDE_ID=server_backend
```

---

## Troubleshooting

### "Connection Refused"
- API server not running
- Wrong hostname/port in COORDINATION_API_URL
- Check firewall if using different machines

### Heartbeats Not Being Acknowledged
- Normal - heartbeat is one-way
- If API isn't responding to heartbeat, API server is down

### Tasks Stuck in "in_progress"
- Claude crashed without updating status
- Manual cleanup: `DELETE /api/coord/message/:id`
- Or update manually: `PUT /api/coord/message/:id` with `status=failed`

### Message Persistence
- Messages stored in SQLite database
- Survives API restarts
- Query database directly if API is down:
```bash
sqlite3 data/etf_data.db "SELECT * FROM coordination_messages LIMIT 10;"
```

---

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Message retention policies
- [ ] Automatic task timeout/retry
- [ ] Priority queues for tasks
- [ ] Distributed tracing across Claudes
- [ ] Heartbeat storage and monitoring dashboard
- [ ] Task templates/macros
- [ ] Rate limiting per Claude instance

---

## See Also

- [API Reference Documentation](../API_REFERENCE.md)
- [System Architecture](../SESSION_HANDOFF-11-12.md)
- Source Code: `src/coordinationClient.ts`, `src/databaseCoordination.ts`, `src/api.ts`
