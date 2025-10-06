# 📊 MCP Progress Notifications Mastery Guide

## What is Progress Tracking in MCP?

Progress Notifications are MCP's mechanism for providing real-time status updates during long-running operations. Using a token-based linking system, they transform opaque processes into transparent, user-friendly experiences with live feedback about completion status.

**Think of it like this:** Ordering a package online. Bad service: "Order placed" then silence for days. Great service: "Order confirmed" → "Packed" → "Shipped" → "Out for delivery" → "Delivered." You're informed at every step. MCP Progress does this for any long operation.

---

## 🤔 The Problem Progress Notifications Solve

### Scenario: AI Agent Processing Large Dataset

**User request:** "Download and process this 5GB dataset"

#### Without Progress Notifications:
- ❌ Agent starts... (user sees nothing)
- ❌ 30 seconds pass... (user worried)
- ❌ 1 minute passes... (user thinks it crashed)
- ❌ 2 minutes pass... (user cancels and retries)
- ❌ Operation was actually working fine!

#### With Progress Notifications:
- ✅ [████░░░░░░░░░░░░░░░░] 20% - Downloading dataset... (1GB/5GB)
- ✅ [████████░░░░░░░░░░░░] 40% - Downloading dataset... (2GB/5GB)
- ✅ [████████████░░░░░░░░] 60% - Downloading dataset... (3GB/5GB)
- ✅ [████████████████░░░░] 80% - Processing data... (4000/5000 records)
- ✅ [████████████████████] 100% - Complete!

**The Magic:** Users stay informed, confident, and patient because they see continuous progress instead of mysterious silence.

---

## 🎯 Core Concept: Token-Based Progress Linking

### Three-Step Process:

**1️⃣ Request**
- Client sends `progressToken` in request
- "I want updates for THIS job"

**2️⃣ Notifications**
- Server sends progress updates with same token
- "Here's the status of THAT job"

**3️⃣ Completion**
- Final result returned, progress stops
- "Job is done!"

---

## 🔄 MCP Progress Protocol Flow

### Step 1: Client Requests Operation with Progress Token

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "download_file",
    "arguments": {
      "filename": "dataset.zip",
      "size_mb": 100
    },
    "_meta": {
      "progressToken": "download_123"
    }
  }
}
```

**Key Points:**
- `progressToken` goes in the special `_meta` field
- Token can be string or integer
- Token MUST be unique across all active requests
- Client chooses the token value

### Step 2: Server Sends Progress Notifications

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "download_123",
    "progress": 25,
    "total": 100,
    "message": "Downloading dataset.zip... 25MB/100MB"
  }
}
```

**Key Fields:**
- `progressToken`: Links to the original request
- `progress`: Current progress value (MUST increase)
- `total`: Optional total value (can be omitted if unknown)
- `message`: Optional human-readable status

### Step 3: Server Continues Sending Updates

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "download_123",
    "progress": 50,
    "total": 100,
    "message": "Downloading dataset.zip... 50MB/100MB"
  }
}
```

### Step 4: Server Returns Final Result

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Download complete: dataset.zip (100MB)"
      }
    ]
  }
}
```

**Important:** Progress notifications MUST stop after the operation completes.

---

## 📊 Complete Message Flow Diagram

```
1. 👤 Client wants to download file with progress tracking
        ↓
2. 📤 Client sends tools/call with progressToken="dl_001"
        ↓
3. 🔄 Server starts download operation
        ↓
4. 📊 Server sends: notifications/progress (20/100) "Downloading..."
        ↓
5. 📊 Server sends: notifications/progress (40/100) "Downloading..."
        ↓
6. 📊 Server sends: notifications/progress (60/100) "Downloading..."
        ↓
7. 📊 Server sends: notifications/progress (80/100) "Downloading..."
        ↓
8. 📊 Server sends: notifications/progress (100/100) "Complete!"
        ↓
9. ✅ Server sends: Result response (operation finished)
        ↓
10. 🛑 Progress notifications stop
```

**Key Insight:** The `progressToken` acts like a tracking number - it lets the client match incoming progress updates to the specific operation they belong to.

---

## 💡 Token Management Strategies

### Token Generation Patterns

#### 1. Sequential Integers (Simple)

```python
progress_counter = 0

def get_progress_token():
    global progress_counter
    progress_counter += 1
    return progress_counter

# Usage: progressToken = 1, 2, 3, 4...
```

#### 2. Request ID Matching (Clean)

```python
# Use the same value as request ID
request_id = 42
progress_token = request_id  # progressToken = 42
```

#### 3. UUID Strings (Robust)

```python
import uuid

def get_progress_token():
    return str(uuid.uuid4())

# Usage: progressToken = "550e8400-e29b-41d4-a716-446655440000"
```

#### 4. Prefixed Descriptive (Readable)

```python
operation_counter = 0

def get_progress_token(operation_name: str):
    global operation_counter
    operation_counter += 1
    return f"{operation_name}_{operation_counter}"

# Usage: progressToken = "download_1", "process_2", etc.
```

### Token Tracking Pattern

```python
class ProgressTracker:
    def __init__(self):
        self.active_tokens = {}
    
    def register(self, token: str, description: str):
        """Register a new progress token"""
        if token in self.active_tokens:
            raise ValueError(f"Token {token} already in use")
        
        self.active_tokens[token] = {
            "description": description,
            "start_time": time.time(),
            "last_progress": 0
        }
    
    def update(self, token: str, progress: float):
        """Update progress for a token"""
        if token not in self.active_tokens:
            raise ValueError(f"Unknown token {token}")
        
        self.active_tokens[token]["last_progress"] = progress
    
    def complete(self, token: str):
        """Mark operation as complete and remove token"""
        if token in self.active_tokens:
            del self.active_tokens[token]
```

---

## 💻 Server Implementation Patterns

### Pattern 1: Basic Progress Reporting (Beginner)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

server = Server("progress-demo")

@server.call_tool()
async def download_file(filename: str, size_mb: int, ctx) -> str:
    """Download file with progress reporting"""
    
    # Simulate download in chunks
    total_chunks = size_mb
    
    for chunk in range(total_chunks + 1):
        # Report progress using context
        await ctx.report_progress(
            progress=chunk,
            total=total_chunks,
            message=f"Downloading {filename}... {chunk}MB/{size_mb}MB"
        )
        
        # Simulate work
        await asyncio.sleep(0.1)
    
    return f"Downloaded {filename} ({size_mb}MB)"
```

### Pattern 2: Progress with Unknown Total (Intermediate)

```python
@server.call_tool()
async def process_stream(stream_url: str, ctx) -> str:
    """Process streaming data with unknown total size"""
    
    processed_items = 0
    
    async for item in stream_data(stream_url):
        processed_items += 1
        
        # Report progress without total (total is None/omitted)
        await ctx.report_progress(
            progress=processed_items,
            message=f"Processed {processed_items} items..."
        )
        
        await process_item(item)
        
        # Update every 100 items to avoid flooding
        if processed_items % 100 == 0:
            await ctx.report_progress(
                progress=processed_items,
                message=f"Processed {processed_items} items..."
            )
    
    return f"Processed {processed_items} total items"
```

### Pattern 3: Multi-Stage Progress (Advanced)

```python
@server.call_tool()
async def complex_pipeline(data: dict, ctx) -> str:
    """Multi-stage operation with detailed progress"""
    
    stages = [
        ("validation", 20),
        ("transformation", 40),
        ("processing", 70),
        ("storage", 100)
    ]
    
    for stage_name, stage_progress in stages:
        await ctx.report_progress(
            progress=stage_progress,
            total=100,
            message=f"Stage: {stage_name}..."
        )
        
        # Perform stage work
        if stage_name == "validation":
            await validate_data(data, ctx, stage_progress)
        elif stage_name == "transformation":
            await transform_data(data, ctx, stage_progress)
        elif stage_name == "processing":
            await process_data(data, ctx, stage_progress)
        elif stage_name == "storage":
            await store_data(data, ctx, stage_progress)
    
    return "Pipeline completed successfully"

async def validate_data(data: dict, ctx, base_progress: int):
    """Validation with sub-progress"""
    items = len(data.get("records", []))
    
    for i in range(items):
        # Calculate sub-progress within stage
        sub_progress = base_progress - 20 + (i / items * 20)
        
        await ctx.report_progress(
            progress=sub_progress,
            total=100,
            message=f"Validating record {i+1}/{items}"
        )
        
        await asyncio.sleep(0.01)
```

### Pattern 4: Rate-Limited Progress (Expert)

```python
import time
from typing import Optional

class RateLimitedProgress:
    """Prevent progress notification flooding"""
    
    def __init__(self, ctx, min_interval: float = 0.1):
        self.ctx = ctx
        self.min_interval = min_interval
        self.last_report = 0
        self.last_progress = 0
    
    async def report(
        self,
        progress: float,
        total: Optional[float] = None,
        message: Optional[str] = None,
        force: bool = False
    ):
        """Report progress with rate limiting"""
        now = time.time()
        
        # Always report if progress increased and enough time passed
        should_report = (
            force or
            (progress > self.last_progress and 
             now - self.last_report >= self.min_interval)
        )
        
        if should_report:
            await self.ctx.report_progress(
                progress=progress,
                total=total,
                message=message
            )
            self.last_report = now
            self.last_progress = progress

@server.call_tool()
async def batch_process(items: list, ctx) -> str:
    """Process items with rate-limited progress"""
    
    progress_reporter = RateLimitedProgress(ctx, min_interval=0.5)
    total = len(items)
    
    for i, item in enumerate(items):
        await process_item(item)
        
        # Report progress (will be rate-limited internally)
        await progress_reporter.report(
            progress=i + 1,
            total=total,
            message=f"Processing {i+1}/{total}"
        )
    
    # Force final progress report
    await progress_reporter.report(
        progress=total,
        total=total,
        message="Complete!",
        force=True
    )
    
    return f"Processed {total} items"
```

---

## 🎯 Protocol Requirements & Best Practices

### ✅ MUST Requirements (Protocol)

**Progress Tokens:**
- MUST be string or integer
- MUST be unique across active requests
- MUST only reference active operations

**Progress Values:**
- `progress` MUST increase with each notification
- `progress` and `total` MAY be floating point
- Progress notifications MUST stop after completion

**Server Behavior:**
- MAY choose not to send progress
- MAY send at any frequency
- MAY omit total if unknown

**Message Format:**
- `message` SHOULD provide human-readable info
- Use `notifications/progress` method
- Include `progressToken` in params

### ✅ DO (Best Practices)

**Token Management:**
- Use descriptive token names
- Track active tokens
- Clean up completed tokens
- Validate tokens before use

**Progress Reporting:**
- Report at reasonable intervals
- Include meaningful messages
- Use consistent units
- Report final 100% explicitly

**Performance:**
- Implement rate limiting
- Buffer notifications if needed
- Don't block operations for progress
- Use async reporting

**User Experience:**
- Provide clear status messages
- Show ETAs when possible
- Use visual indicators
- Handle unknown totals gracefully

### ❌ MUST NOT (Protocol Violations)

**Token Violations:**
- Don't reuse tokens while operations are active
- Don't send progress for unknown tokens
- Don't continue progress after completion

**Progress Violations:**
- Don't decrease progress values
- Don't send inconsistent totals
- Don't send progress without token

### ❌ DON'T (Anti-Patterns)

**Flooding:**
- Don't send progress for every tiny step
- Don't report more than once per 100ms
- Don't send unchanged progress values

**Poor UX:**
- Don't use cryptic messages
- Don't ignore total when known
- Don't forget final progress update
- Don't leave users guessing

**Performance:**
- Don't block operations for progress
- Don't do expensive work in progress reporting
- Don't create memory leaks with token tracking

---

## 🎯 Quick Reference

### Server Checklist
- ✅ Include `progressToken` in request `_meta` field
- ✅ Send progress notifications with same token
- ✅ Ensure progress values always increase
- ✅ Include meaningful status messages
- ✅ Report final 100% before returning result
- ✅ Stop progress notifications after completion
- ✅ Implement rate limiting for high-frequency updates
- ✅ Handle operation cancellation gracefully

### Client Checklist
- ✅ Generate unique progress tokens for each request
- ✅ Register progress callback handler
- ✅ Display progress visually (bar, percentage, ETA)
- ✅ Handle progress without known total
- ✅ Track active operations by token
- ✅ Clean up completed progress tokens
- ✅ Handle missing or delayed updates
- ✅ Support concurrent operations

---

## 🧠 Mental Model

**Think of Progress as GPS Navigation**

**Without Progress:**
"You have 200 miles to go" → silence → "You have arrived"

**With Progress:**
"Starting route" → "25 miles complete" → "Halfway there" → "5 minutes away" → "Arrived!"

**Progress Token = Trip ID:**
Links all updates to your specific journey, not someone else's

**Result:**
Users feel informed, confident, and patient during long operations

---

## 🎯 Master It in One Sentence

MCP Progress Notifications enable real-time status updates for long-running operations by having clients include a unique `progressToken` in request metadata and servers send `notifications/progress` messages with monotonically increasing progress values, optional totals, and human-readable messages, all linked by the same token until operation completion.

---

*You now master MCP Progress Notifications from basic concepts to advanced implementation patterns. Build transparent, user-friendly MCP servers that keep users informed during long operations!*
