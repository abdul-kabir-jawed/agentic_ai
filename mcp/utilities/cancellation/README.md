# 📋 MCP Progress Tracking Mastery Guide

## What is MCP Progress Tracking?

Progress tracking is MCP's mechanism for monitoring and controlling long-running operations through standardized notification messages. It enables servers to report incremental updates during task execution and allows clients to cancel operations that are no longer needed, creating responsive and user-controlled AI experiences.

**Think of it like this:** A download manager showing "45% complete, 2 minutes remaining" with a cancel button—users see what's happening, how long it will take, and can stop it anytime. MCP brings this same transparency and control to AI agent operations.

---

## 🤔 The Problem Progress Tracking Solves

### Scenario: AI Agent Processing Large Dataset

**User request:** "Process this 10GB CSV file"

#### Without Progress Tracking:
- ❌ Operation starts... (user sees nothing)
- ❌ 5 minutes pass... (still nothing)
- ❌ User gets impatient, closes browser
- ❌ Server keeps processing for 30 more minutes
- ❌ Wasted computation, frustrated user
- ❌ No way to know: Is it stuck? How much longer?

#### With Progress & Cancellation:
- ✅ Processing started: 0/1,000,000 rows
- ✅ Progress: 25% complete (250,000 rows)
- ✅ Progress: 50% complete (500,000 rows)
- ✅ User decides data isn't needed → clicks Cancel
- ✅ Server receives cancellation notification
- ✅ Server stops at row 520,000, cleans up resources
- ✅ Response: "Operation cancelled by user"
- ✅ Everyone's happy: User got control, server didn't waste time

**The Magic:** Progress tracking transforms opaque operations into transparent, controllable processes where users feel informed and in control.

---

## 🎯 Core Concept: Cooperative Cancellation

### Three Key Components:

1. **📊 Progress Updates** - Real-time visibility, know what's happening
2. **🛑 Cancellation Request** - User-initiated control, stop when needed
3. **🧹 Graceful Cleanup** - Resource management, clean exit always

---

## 🔄 MCP Cancellation Protocol Flow

### Step 1: Client Starts Long-Running Operation

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "method": "tools/call",
  "params": {
    "name": "process_large_file",
    "arguments": {
      "filename": "data.csv"
    }
  }
}
```

**Meaning:** Client issues request with unique ID (123)

### Step 2: Server Begins Processing

```python
# Server side - tool starts executing
async def process_large_file(filename: str, ctx):
    total_rows = 1_000_000
    
    for i in range(total_rows):
        # Check if cancelled at each iteration
        if ctx.is_cancelled:
            await cleanup_resources()
            raise asyncio.CancelledError("Processing cancelled by user")
        
        # Process one row
        await process_row(i)
        
        # Report progress every 10%
        if i % 100_000 == 0:
            await ctx.report_progress(i, total_rows)
```

**Key Pattern:** Regular cancellation checks during processing

### Step 3: Client Sends Cancellation Notification

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": "123",
    "reason": "User requested cancellation"
  }
}
```

**Effect:** Server's `ctx.is_cancelled` becomes True for request 123

### Step 4: Server Stops Gracefully

```python
# Inside the loop, cancellation detected
if ctx.is_cancelled:
    # Clean up any resources
    await close_file_handles()
    await release_database_connections()
    
    # Raise to signal cancellation
    raise asyncio.CancelledError("Processing cancelled")
```

**Result:** Server exits cleanly, no response sent (notification = fire-and-forget)

---

## 📊 Complete Cancellation Flow Diagram

```
1. 🚀 Client sends request (ID: 123)
        ↓
2. 🔄 Server starts processing
        ↓
3. 📊 Server reports: "Progress: 10%"
        ↓
4. 📊 Server reports: "Progress: 25%"
        ↓
5. 🛑 User clicks "Cancel"
        ↓
6. 📤 Client sends: notifications/cancelled (requestId: 123)
        ↓
7. ⏸️ Server checks ctx.is_cancelled → True
        ↓
8. 🧹 Server cleans up resources
        ↓
9. 🚫 Server raises CancelledError
        ↓
10. ✅ Server does NOT send response (notification = no reply)
        ↓
11. 😊 Client UI shows: "Operation cancelled"
```

**Key Insight:** Cancellation is cooperative—the server chooses when to check and stop. The client requests, but doesn't force termination.

---

## 🏗️ Critical Behavior Requirements

### MUST Requirements

| Requirement | Why It Matters | Example |
|------------|----------------|---------|
| Only cancel in-progress requests | Can't cancel what's already done | Check request exists before canceling |
| Never cancel initialize request | Would break the connection | Skip cancellation for initialization |
| Handle race conditions gracefully | Network delays cause timing issues | Ignore cancellation if request completed |
| Stop processing when cancelled | Free up resources immediately | Exit loops, close files, release memory |
| Don't send response after cancel | Notifications are fire-and-forget | No reply to cancellation notification |

### SHOULD Recommendations

- Stop processing promptly (< 1 second ideally)
- Free associated resources (memory, connections, file handles)
- Log cancellation reasons for debugging
- Indicate cancellation in UI so users know it worked

### MAY Allowances

- Ignore unknown request IDs (might be typo or timing)
- Ignore if already completed (race condition is normal)
- Ignore if operation can't be cancelled (atomic operations)

---

## 💡 Perfect Example: Large File Processing

### The Scenario

A data analysis tool processes CSV files with millions of rows. Users need to see progress and cancel if they realize they uploaded the wrong file.

**Challenge:** Processing takes 10+ minutes. Without cancellation, users are trapped.

**Solution:** Cooperative cancellation with regular check points and clean resource management.

### Server Implementation

```python
@mcp.tool()
async def process_csv_file(filepath: str, ctx) -> dict:
    """Process large CSV with cancellation support"""
    
    # Open resources
    file = await open_file(filepath)
    db_conn = await get_database_connection()
    
    try:
        total_rows = await count_rows(file)
        processed = 0
        
        await ctx.info(f"Starting processing: {total_rows} rows")
        
        async for row in file:
            # CRITICAL: Check cancellation at start of each iteration
            if ctx.is_cancelled:
                await ctx.info("Cancellation detected, stopping...")
                raise asyncio.CancelledError("User cancelled operation")
            
            # Process the row
            await process_row(row, db_conn)
            processed += 1
            
            # Report progress every 10,000 rows
            if processed % 10_000 == 0:
                percent = (processed / total_rows) * 100
                await ctx.info(f"Progress: {percent:.1f}% ({processed}/{total_rows})")
        
        return {"status": "completed", "rows": processed}
        
    except asyncio.CancelledError:
        # Clean up resources
        await ctx.info(f"Cleanup: Processed {processed} rows before cancel")
        raise  # Re-raise to signal cancellation
        
    finally:
        # Always clean up, cancelled or not
        await file.close()
        await db_conn.close()
        await ctx.info("Resources released")
```

### Client Implementation

```python
# Start the operation
result_task = asyncio.create_task(
    session.call_tool("process_csv_file", {"filepath": "data.csv"})
)

# Get the request ID (this is implementation-specific)
request_id = session._last_request_id

# User clicks cancel after 30 seconds
await asyncio.sleep(30)

# Send cancellation notification
await session.send_notification(
    "notifications/cancelled",
    {
        "requestId": request_id,
        "reason": "User uploaded wrong file"
    }
)

# Don't wait for result_task - it won't complete normally
# Just update UI to show cancellation
ui.show_message("Operation cancelled successfully")
```

### Server Logs

```
[INFO] Starting processing: 1000000 rows
[INFO] Progress: 10.0% (100000/1000000)
[INFO] Progress: 20.0% (200000/1000000)
[INFO] Cancellation detected, stopping...
[INFO] Cleanup: Processed 237450 rows before cancel
[INFO] Resources released
```

**Result:** File closed, database connection returned to pool, user can start new operation immediately.

---

## 💻 Server Implementation Patterns

### Pattern 1: Basic Cancellation Check (Beginner)

```python
from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("cancellable-server")

@mcp.tool()
async def process_items(items: list, ctx) -> dict:
    """Process items with basic cancellation"""
    
    results = []
    
    for i, item in enumerate(items):
        # Check at start of each iteration
        if ctx.is_cancelled:
            return {
                "status": "cancelled",
                "processed": i,
                "total": len(items)
            }
        
        # Do work
        result = await process_item(item)
        results.append(result)
        
        # Optional: Report progress
        if i % 100 == 0:
            await ctx.info(f"Processed {i}/{len(items)} items")
    
    return {
        "status": "completed",
        "processed": len(items),
        "results": results
    }
```

### Pattern 2: Resource Cleanup (Intermediate)

```python
@mcp.tool()
async def query_database(query: str, ctx) -> dict:
    """Database query with proper cleanup"""
    
    conn = None
    cursor = None
    
    try:
        # Acquire resources
        conn = await db_pool.acquire()
        cursor = await conn.cursor()
        
        # Execute query
        await cursor.execute(query)
        
        # Fetch results with cancellation checks
        results = []
        row_count = 0
        
        while True:
            # Check cancellation before each fetch
            if ctx.is_cancelled:
                await ctx.info(f"Query cancelled after {row_count} rows")
                raise asyncio.CancelledError("Query cancelled by user")
            
            # Fetch batch
            batch = await cursor.fetchmany(1000)
            if not batch:
                break
            
            results.extend(batch)
            row_count += len(batch)
            
            # Report progress
            if row_count % 10_000 == 0:
                await ctx.info(f"Fetched {row_count} rows")
        
        return {
            "status": "completed",
            "rows": results,
            "count": row_count
        }
        
    except asyncio.CancelledError:
        # Log cancellation
        await ctx.warning("Database query cancelled")
        raise  # Re-raise to propagate
        
    finally:
        # Always clean up resources
        if cursor:
            await cursor.close()
        if conn:
            await db_pool.release(conn)
        await ctx.debug("Database resources released")
```

### Pattern 3: Nested Operations (Advanced)

```python
@mcp.tool()
async def batch_process(file_list: list, ctx) -> dict:
    """Process multiple files with cancellation"""
    
    results = {
        "completed": [],
        "failed": [],
        "cancelled_at": None
    }
    
    for i, filepath in enumerate(file_list):
        # Check cancellation at file level
        if ctx.is_cancelled:
            results["cancelled_at"] = i
            await ctx.info(f"Batch cancelled at file {i}/{len(file_list)}")
            return results
        
        await ctx.info(f"Processing file {i+1}/{len(file_list)}: {filepath}")
        
        try:
            # Call another cancellable operation
            file_result = await process_single_file(filepath, ctx)
            results["completed"].append({
                "file": filepath,
                "result": file_result
            })
            
        except asyncio.CancelledError:
            # Propagate cancellation from nested operation
            results["cancelled_at"] = i
            await ctx.info("Nested operation cancelled")
            raise
            
        except Exception as e:
            results["failed"].append({
                "file": filepath,
                "error": str(e)
            })
    
    return results

async def process_single_file(filepath: str, ctx) -> dict:
    """Helper that also respects cancellation"""
    
    file = await open_async(filepath)
    
    try:
        lines = []
        line_count = 0
        
        async for line in file:
            # Check cancellation in nested operation
            if ctx.is_cancelled:
                raise asyncio.CancelledError("File processing cancelled")
            
            processed_line = await process_line(line)
            lines.append(processed_line)
            line_count += 1
            
            # Progress for individual file
            if line_count % 1000 == 0:
                await ctx.debug(f"  {filepath}: {line_count} lines")
        
        return {"lines": line_count, "data": lines}
        
    finally:
        await file.close()
```

### Pattern 4: Timeout + Cancellation (Expert)

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def cancellable_timeout(ctx, seconds: float):
    """Combine timeout and cancellation checking"""
    
    async def check_cancelled():
        """Periodically check for cancellation"""
        while True:
            if ctx.is_cancelled:
                raise asyncio.CancelledError("Operation cancelled by user")
            await asyncio.sleep(0.1)  # Check every 100ms
    
    # Run operation with both timeout and cancellation checking
    cancel_checker = asyncio.create_task(check_cancelled())
    
    try:
        yield
    except asyncio.TimeoutError:
        await ctx.error("Operation timed out")
        raise
    finally:
        cancel_checker.cancel()
        try:
            await cancel_checker
        except asyncio.CancelledError:
            pass

@mcp.tool()
async def api_call_with_timeout(endpoint: str, ctx) -> dict:
    """API call with timeout and cancellation"""
    
    try:
        async with cancellable_timeout(ctx, seconds=30.0):
            await ctx.info(f"Calling API: {endpoint}")
            
            # Make API call
            response = await asyncio.wait_for(
                http_client.get(endpoint),
                timeout=30.0
            )
            
            await ctx.info("API call completed")
            return response.json()
            
    except asyncio.CancelledError:
        await ctx.warning("API call cancelled by user")
        raise
        
    except asyncio.TimeoutError:
        await ctx.error("API call timed out after 30 seconds")
        raise
```

---

## 💻 Client Implementation Patterns

### Pattern 1: Basic Cancellation

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def main():
    """Basic cancellation example"""
    
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            await session.initialize()
            
            # Start long-running operation
            print("Starting long operation...")
            result_task = asyncio.create_task(
                session.call_tool("process_large_file", {
                    "filename": "huge_data.csv"
                })
            )
            
            # Get the request ID (implementation-specific)
            request_id = "123"
            
            # Wait a bit, then cancel
            await asyncio.sleep(5)
            
            print("Sending cancellation...")
            await session.send_notification(
                "notifications/cancelled",
                {
                    "requestId": request_id,
                    "reason": "User requested cancellation"
                }
            )
            
            print("Cancellation sent")

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 2: User-Controlled Cancellation

```python
import asyncio
from typing import Optional

class CancellableOperation:
    """Wrapper for cancellable MCP operations"""
    
    def __init__(self, session, tool_name: str, arguments: dict):
        self.session = session
        self.tool_name = tool_name
        self.arguments = arguments
        self.request_id: Optional[str] = None
        self.task: Optional[asyncio.Task] = None
        self.cancelled = False
    
    async def start(self):
        """Start the operation"""
        self.task = asyncio.create_task(
            self.session.call_tool(self.tool_name, self.arguments)
        )
        
        self.request_id = self.session._last_request_id
        print(f"Operation started with ID: {self.request_id}")
    
    async def cancel(self, reason: str = "User cancelled"):
        """Cancel the operation"""
        if self.cancelled:
            print("Already cancelled")
            return
        
        if not self.request_id:
            print("Operation not started yet")
            return
        
        print(f"Cancelling operation {self.request_id}...")
        
        await self.session.send_notification(
            "notifications/cancelled",
            {
                "requestId": self.request_id,
                "reason": reason
            }
        )
        
        self.cancelled = True
        print("Cancellation sent")
    
    async def wait(self, timeout: Optional[float] = None):
        """Wait for operation to complete or be cancelled"""
        if not self.task:
            raise ValueError("Operation not started")
        
        try:
            if timeout:
                return await asyncio.wait_for(self.task, timeout)
            else:
                return await self.task
        except asyncio.TimeoutError:
            print("Operation timed out")
            await self.cancel("Operation timeout")
            raise
```

### Pattern 3: Multiple Concurrent Operations

```python
class OperationManager:
    """Manage multiple cancellable operations"""
    
    def __init__(self, session):
        self.session = session
        self.operations: dict[str, CancellableOperation] = {}
    
    async def start_operation(self, op_id: str, tool_name: str, 
                             arguments: dict) -> str:
        """Start a new operation"""
        
        op = CancellableOperation(self.session, tool_name, arguments)
        await op.start()
        
        self.operations[op_id] = op
        return op.request_id
    
    async def cancel_operation(self, op_id: str, reason: str):
        """Cancel specific operation"""
        
        op = self.operations.get(op_id)
        if not op:
            print(f"Unknown operation: {op_id}")
            return
        
        await op.cancel(reason)
    
    async def cancel_all(self, reason: str = "Cancelling all operations"):
        """Cancel all in-progress operations"""
        
        print(f"Cancelling {len(self.operations)} operations...")
        
        tasks = [
            op.cancel(reason)
            for op in self.operations.values()
            if not op.cancelled
        ]
        
        await asyncio.gather(*tasks)
        print("All operations cancelled")
    
    def get_status(self) -> dict:
        """Get status of all operations"""
        
        return {
            op_id: {
                "cancelled": op.cancelled,
                "done": op.task.done() if op.task else False
            }
            for op_id, op in self.operations.items()
        }
```

---

## 🏁 Race Condition Handling

### Understanding the Race

Due to network latency, several timing scenarios can occur:

**Scenario 1: Normal Cancellation**
```
Client sends request → Server starts processing → 
Client sends cancel → Server checks ctx.is_cancelled → 
Server stops → Done
```

**Scenario 2: Cancel Arrives After Completion**
```
Client sends request → Server processes → 
Server completes → Server sends response → 
Client sends cancel (arrives late) → 
Server ignores (request already done)
```

**Scenario 3: Response and Cancel Cross in Transit**
```
Client sends request → Server processes → 
Server sends response → Client sends cancel → 
Both messages in transit → 
Client ignores response, Server ignores cancel
```

### Server Handling

```python
@mcp.tool()
async def operation(data: dict, ctx) -> dict:
    """Handle race conditions gracefully"""
    
    try:
        # Normal processing
        for i in range(100):
            if ctx.is_cancelled:
                raise asyncio.CancelledError()
            
            await process_item(i)
        
        return {"status": "completed"}
        
    except asyncio.CancelledError:
        await ctx.info("Cancellation detected")
        raise
```

### Client Handling

```python
async def robust_cancellation(session, request_id: str):
    """Handle cancellation race conditions"""
    
    # Send cancellation
    await session.send_notification(
        "notifications/cancelled",
        {"requestId": request_id, "reason": "User cancelled"}
    )
    
    # Update UI immediately
    ui.show_message("Operation cancelled")
    
    # Don't wait for confirmation - notifications don't get replies
```

### Key Principles

- **Server:** Check `ctx.is_cancelled` frequently, but accept that the operation might complete between checks
- **Client:** Send cancellation notification and move on—don't expect confirmation
- **Both:** Log unexpected states for debugging but handle gracefully
- **Framework:** MCP implementations should track request state and ignore stale notifications

---

## 🛡️ Best Practices & Anti-Patterns

### ✅ DO (Server)

**Cancellation Checks:**
- Check `ctx.is_cancelled` at start of each loop iteration
- Check before expensive operations
- Check after awaiting slow I/O
- Check every few seconds in long computations

**Resource Management:**
- Always clean up in finally blocks
- Close files, connections, sockets
- Release locks and semaphores
- Free memory allocations

**Error Handling:**
- Re-raise `CancelledError` after cleanup
- Log cancellation for debugging
- Don't treat cancellation as an error (it's not)

**Good Code Example:**

```python
# Good: Frequent checks
async def process_data(data: list, ctx):
    file = await open_file()
    try:
        for item in data:
            if ctx.is_cancelled:  # Check early
                raise asyncio.CancelledError()
            
            result = await expensive_operation(item)
            
            if ctx.is_cancelled:  # Check after slow op
                raise asyncio.CancelledError()
            
            await save_result(result)
    finally:
        await file.close()  # Always clean up

# Good: Resource cleanup
async def database_query(sql: str, ctx):
    conn = await pool.acquire()
    try:
        cursor = await conn.cursor()
        try:
            for row in cursor:
                if ctx.is_cancelled:
                    raise asyncio.CancelledError()
                process(row)
        finally:
            await cursor.close()
    finally:
        await pool.release(conn)
```

### ❌ DON'T (Server)

**Cancellation Mistakes:**
- Don't check `ctx.is_cancelled` only once
- Don't ignore cancellation checks
- Don't check too infrequently (every 100k iterations)
- Don't continue after detecting cancellation

**Resource Leaks:**
- Don't forget to clean up resources
- Don't leave files open
- Don't leave connections in pool
- Don't leak memory on cancellation

**Error Handling:**
- Don't swallow `CancelledError`
- Don't convert `CancelledError` to success
- Don't send response after cancellation

**Bad Code Example:**

```python
# Bad: No cancellation checks
async def process_data(data: list, ctx):
    for item in data:  # Could run for hours
        await expensive_operation(item)
    return "done"  # User can't cancel!

# Bad: Check only at start
async def long_operation(ctx):
    if ctx.is_cancelled:
        return
    # Process for 10 minutes with no checks
    await very_long_computation()

# Bad: Resource leak
async def query_db(sql: str, ctx):
    conn = await pool.acquire()
    if ctx.is_cancelled:
        return  # Leaked connection!
    result = await conn.execute(sql)
    await pool.release(conn)

# Bad: Swallowing cancellation
async def process(ctx):
    try:
        for i in range(1000000):
            if ctx.is_cancelled:
                raise asyncio.CancelledError()
            await work()
    except asyncio.CancelledError:
        return "completed"  # Wrong! Should re-raise
```

### ✅ DO (Client)

**Request Tracking:**
- Track request IDs for all long operations
- Store mapping of operation → request ID
- Use unique identifiers for each operation

**Cancellation Sending:**
- Send cancellation as soon as user decides
- Include helpful reason string
- Don't wait for confirmation

**UI/UX:**
- Show "Cancelling..." immediately
- Don't wait for server
- Don't make users wait to see cancellation effect

**Good Code Example:**

```python
# Good: Track request IDs
class OperationTracker:
    def __init__(self):
        self.operations = {}
    
    async def start(self, session, tool, args):
        task = asyncio.create_task(
            session.call_tool(tool, args)
        )
        req_id = session._last_request_id
        self.operations[req_id] = task
        return req_id
    
    async def cancel(self, session, req_id):
        await session.send_notification(
            "notifications/cancelled",
            {"requestId": req_id, "reason": "User cancelled"}
        )
        # Update UI immediately
        ui.show_cancelled()
```

### ❌ DON'T (Client)

**Bad Code Example:**

```python
# Bad: No request tracking
async def start_operation():
    await session.call_tool("long_op", {})
    # Lost the request ID!

# Bad: Hardcoded ID
async def cancel_something():
    await session.send_notification(
        "notifications/cancelled",
        {"requestId": "123"}  # What if it's not 123?
    )

# Bad: Waiting for confirmation
async def cancel_and_wait(request_id):
    await session.send_notification(
        "notifications/cancelled",
        {"requestId": request_id}
    )
    # DON'T DO THIS - notifications have no response
    await wait_for_cancellation_confirmation()

# Bad: Cancelling initialize
await session.send_notification(
    "notifications/cancelled",
    {"requestId": initialize_request_id}  # FORBIDDEN!
)

# Bad: UI confusion
async def cancel_op(op_id):
    await send_cancel(op_id)
    # UI still shows "Processing..."
    # User thinks cancel didn't work
```

---

## 🎓 Real-World Use Cases

### Use Case 1: Large Dataset Analysis

**Challenge:** User uploads 10GB CSV for analysis, realizes it's the wrong file after 2 minutes.

```python
@mcp.tool()
async def analyze_dataset(filepath: str, ctx) -> dict:
    """Analyze large dataset with cancellation"""
    
    stats = {
        "total_rows": 0,
        "processed_rows": 0,
        "errors": 0
    }
    
    async with open_csv_file(filepath) as csv_file:
        try:
            # Count total rows first
            stats["total_rows"] = await count_rows(csv_file)
            await ctx.info(f"Starting analysis of {stats['total_rows']} rows")
            
            # Process each row
            async for row_num, row in enumerate(csv_file):
                # Cancellation check every row
                if ctx.is_cancelled:
                    await ctx.info(
                        f"Analysis cancelled at row {row_num}/{stats['total_rows']}"
                    )
                    raise asyncio.CancelledError()
                
                try:
                    await analyze_row(row)
                    stats["processed_rows"] += 1
                except Exception as e:
                    stats["errors"] += 1
                    await ctx.warning(f"Row {row_num} error: {e}")
                
                # Progress every 10,000 rows
                if row_num % 10_000 == 0:
                    percent = (row_num / stats["total_rows"]) * 100
                    await ctx.info(f"Progress: {percent:.1f}%")
            
            await ctx.info("Analysis completed successfully")
            return stats
            
        except asyncio.CancelledError:
            await ctx.info(f"Final stats before cancellation: {stats}")
            raise
```

**User Experience:**
- Uploads file → sees "Starting analysis of 5,000,000 rows"
- Realizes mistake at "Progress: 5.2%"
- Clicks Cancel → immediately sees "Cancelled"
- Can start new analysis without waiting
