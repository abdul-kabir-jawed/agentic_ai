# 📋 MCP Logging Mastery Guide

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is MCP Logging?

**Logging** is MCP's standardized mechanism for servers to send structured diagnostic messages to clients, enabling real-time monitoring, debugging, and operational transparency. Based on RFC 5424 syslog severity levels, it provides 8 levels of message granularity with optional logger names and arbitrary JSON-serializable context data.

> **Think of it like this:** Your server narrating its activities like a pilot's radio communication—"Taking off," "Cruising at 30,000 feet," "Warning: turbulence ahead," "Emergency: engine failure." Each message has a severity level so listeners know what needs attention.

</div>

---

## 🤔 The Problem Logging Solves

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Scenario: AI Agent Processing Database Queries

**User request:** *"Fetch weather data for 100 cities"*

**Without Logging:**
```
❌ Agent starts processing... (user sees nothing)
❌ Database connection fails... (silent error)
❌ Retrying connection... (user unaware)
❌ Processing takes 30 seconds (user confused)
❌ Agent crashes (no diagnostic info)
❌ User sees: "Request failed" with no context
```

**With Structured Logging:**
```
✅ [INFO] Starting weather data fetch for 100 cities
✅ [DEBUG] Connecting to database at db.weather.com:5432
✅ [WARNING] Connection attempt 1 failed, retrying...
✅ [INFO] Connection established successfully
✅ [DEBUG] Fetched data for city 1/100: New York
✅ [DEBUG] Fetched data for city 50/100: Tokyo
✅ [ERROR] Rate limit exceeded for API endpoint
✅ [INFO] Completed: 95/100 cities (5 failed)
```

**The Magic:** Logging transforms mysterious black-box operations into transparent, debuggable processes with clear visibility into what's happening, when, and why.

</div>

---

## 🎯 Core Concept: Structured Severity Levels

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🔍 Debug/Info
Operational visibility

*Normal activity tracking*

</div>

<div style="background: linear-gradient(135deg, #ffa500 0%, #ff6347 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### ⚠️ Notice/Warning
Attention required

*Potential issues detected*

</div>

<div style="background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🚨 Error/Critical/Alert/Emergency
Immediate action

*Failures and crises*

</div>

</div>

---

## 🏗️ The 8 Logging Levels (RFC 5424)

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

| Level | Severity | When to Use | Example Scenario | Sample Message |
|-------|----------|-------------|------------------|----------------|
| **🐛 debug** | Lowest | Detailed tracing | Function entry/exit | "Entering validateUser() with id=123" |
| **ℹ️ info** | Low | General updates | Progress tracking | "Processing batch 3/10 (30% complete)" |
| **📢 notice** | Medium-Low | Significant events | Config changes | "Database connection pool size changed: 10→20" |
| **⚠️ warning** | Medium | Potential issues | Deprecated features | "Using deprecated API endpoint /v1/users" |
| **❌ error** | Medium-High | Operation failures | Request errors | "Failed to fetch user data: 404 Not Found" |
| **🔴 critical** | High | System component failure | Service unavailable | "Authentication service offline" |
| **🚨 alert** | Very High | Immediate action needed | Data corruption | "Database integrity check failed" |
| **💥 emergency** | Highest | System unusable | Complete failure | "All database replicas down, system halted" |

</div>

---

## 🔄 MCP Logging Protocol Flow

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Step 1: Server Capability Declaration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "capabilities": {
      "logging": {}
    }
  }
}
```

**Meaning:** Server tells client "I can send you log messages"

### Step 2: Client Sets Minimum Log Level

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "logging/setLevel",
  "params": {
    "level": "info"
  }
}
```

**Effect:** Client will only receive `info` level and above (info, notice, warning, error, critical, alert, emergency). Debug messages are filtered out.

### Step 3: Server Sends Log Notifications

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "level": "error",
    "logger": "database",
    "data": {
      "error": "Connection failed",
      "details": {
        "host": "localhost",
        "port": 5432,
        "retry_count": 3
      }
    }
  }
}
```

**Key Fields:**
- `level`: Severity (one of 8 levels)
- `logger`: Optional component identifier
- `data`: Arbitrary JSON context

### Step 4: Client Processes and Displays

```python
def handle_log_message(params):
    level = params["level"]
    logger = params.get("logger", "server")
    data = params.get("data", {})
    
    print(f"[{level.upper()}] [{logger}] {data.get('error', '')}")
    if "details" in data:
        print(f"  Details: {data['details']}")
```

**Output:**
```
[ERROR] [database] Connection failed
  Details: {'host': 'localhost', 'port': 5432, 'retry_count': 3}
```

</div>

---

## 📊 Complete Message Flow Diagram

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #667eea;">

```
1. 🔌 Client connects to Server
        ↓
2. 🤝 Server declares logging capability
        ↓
3. 🎛️ Client sets log level to "info"
        ↓
4. ✅ Server acknowledges level change
        ↓
5. 🔄 Server begins operations
        ↓
6. 📤 Server sends: [DEBUG] "Function entry" → FILTERED (below info)
        ↓
7. 📤 Server sends: [INFO] "Processing started" → ✅ DELIVERED
        ↓
8. 📤 Server sends: [WARNING] "Slow query" → ✅ DELIVERED
        ↓
9. 📤 Server sends: [ERROR] "Failed operation" → ✅ DELIVERED
        ↓
10. 🎛️ Client changes level to "error"
        ↓
11. 📤 Server sends: [INFO] "Completed task" → FILTERED (below error)
        ↓
12. 📤 Server sends: [ERROR] "Timeout" → ✅ DELIVERED
```

**Key Insight:** Log level filtering happens server-side based on client preferences. Lower-severity messages never reach the client if below the configured threshold.

</div>

---

## 💡 Perfect Example: Weather Data Server

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 15px; margin: 20px 0;">

### The Scenario

A weather data aggregation server processes requests from multiple cities, making API calls and caching results.

**Challenge:** Users need visibility into what's happening during slow operations.

**Solution:** Structured logging with contextual data at appropriate severity levels.

### Operation Timeline with Logging

**User Request:** "Get weather for New York, London, Tokyo"

```python
# Server logs throughout operation:

await ctx.info("Weather request received", extra={
    "cities": ["New York", "London", "Tokyo"],
    "user_id": "user_123"
})

await ctx.debug("Checking cache for New York", extra={
    "cache_key": "weather_nyc"
})

await ctx.info("Cache hit for New York", extra={
    "city": "New York",
    "data_age_seconds": 120
})

await ctx.debug("Making API call for London", extra={
    "endpoint": "api.weather.com/v2/current",
    "city": "London"
})

await ctx.warning("API rate limit approaching", extra={
    "current_usage": 950,
    "limit": 1000,
    "reset_in_seconds": 300
})

await ctx.error("API call failed for Tokyo", extra={
    "city": "Tokyo",
    "error": "Timeout after 5 seconds",
    "retry_attempt": 1
})

await ctx.info("Retrying Tokyo with backup API", extra={
    "backup_endpoint": "backup.weather.org/data"
})

await ctx.info("Weather request completed", extra={
    "cities_succeeded": ["New York", "London", "Tokyo"],
    "cities_failed": [],
    "total_time_ms": 3200
})
```

**Client receives** (if log level = "info"):
```
[INFO] Weather request received
  Cities: New York, London, Tokyo
  
[INFO] Cache hit for New York
  Data age: 2 minutes
  
[WARNING] API rate limit approaching
  Usage: 950/1000 (resets in 5 min)
  
[ERROR] API call failed for Tokyo
  Timeout after 5 seconds (attempt 1)
  
[INFO] Retrying Tokyo with backup API

[INFO] Weather request completed
  Success: 3/3 cities in 3.2 seconds
```

**Result:** User sees exactly what's happening, understands delays, knows when to expect results.

</div>

---

## 💻 Server Implementation Patterns

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern 1: Basic Logging with Context (Beginner)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("weather-server")

@server.call_tool()
async def fetch_weather(city: str, ctx) -> str:
    """Fetch weather with logging"""
    
    # Info: Operation started
    await ctx.info(f"Fetching weather for {city}", extra={
        "city": city,
        "timestamp": datetime.now().isoformat()
    })
    
    try:
        # Debug: Checking cache
        await ctx.debug("Checking cache", extra={
            "cache_key": f"weather_{city}"
        })
        
        # Simulate API call
        weather_data = await weather_api.get(city)
        
        # Info: Success
        await ctx.info(f"Weather retrieved successfully", extra={
            "city": city,
            "temperature": weather_data["temp"],
            "conditions": weather_data["conditions"]
        })
        
        return f"{city}: {weather_data['temp']}°F, {weather_data['conditions']}"
        
    except ApiRateLimitError as e:
        # Warning: Rate limit
        await ctx.warning("API rate limit hit", extra={
            "city": city,
            "retry_after": e.retry_after
        })
        raise
        
    except ApiTimeoutError as e:
        # Error: Timeout
        await ctx.error("API timeout", extra={
            "city": city,
            "timeout_seconds": e.timeout
        })
        raise
        
    except Exception as e:
        # Critical: Unexpected error
        await ctx.critical("Unexpected error in fetch_weather", extra={
            "city": city,
            "error_type": type(e).__name__,
            "error_message": str(e)
        })
        raise
```

### Pattern 2: Named Loggers (Intermediate)

```python
@server.call_tool()
async def process_data(data: dict, ctx) -> dict:
    """Process data with component-specific logging"""
    
    # Use logger names to categorize
    await ctx.info("Starting data processing", extra={
        "record_count": len(data)
    }, logger="processor")
    
    # Validation phase
    await ctx.debug("Validating input", extra={
        "schema_version": "2.0"
    }, logger="validator")
    
    if not validate(data):
        await ctx.error("Validation failed", extra={
            "errors": get_validation_errors(data)
        }, logger="validator")
        raise ValueError("Invalid data")
    
    # Transformation phase
    await ctx.debug("Applying transformations", extra={
        "transformations": ["normalize", "enrich"]
    }, logger="transformer")
    
    result = transform(data)
    
    # Storage phase
    await ctx.info("Saving to database", extra={
        "record_count": len(result)
    }, logger="storage")
    
    try:
        await db.save(result)
        await ctx.info("Data saved successfully", extra={
            "duration_ms": 250
        }, logger="storage")
    except DatabaseError as e:
        await ctx.critical("Database write failed", extra={
            "error": str(e),
            "rollback": True
        }, logger="storage")
        raise
    
    return result
```

### Pattern 3: Performance Tracking (Advanced)

```python
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def log_performance(ctx, operation: str, logger: str = "perf"):
    """Context manager for performance logging"""
    
    start = time.time()
    await ctx.debug(f"{operation} started", logger=logger)
    
    try:
        yield
        duration = time.time() - start
        
        # Choose level based on duration
        if duration > 5.0:
            await ctx.warning(f"{operation} slow", extra={
                "duration_seconds": round(duration, 2),
                "threshold": 5.0
            }, logger=logger)
        else:
            await ctx.info(f"{operation} completed", extra={
                "duration_seconds": round(duration, 2)
            }, logger=logger)
            
    except Exception as e:
        duration = time.time() - start
        await ctx.error(f"{operation} failed", extra={
            "duration_seconds": round(duration, 2),
            "error": str(e)
        }, logger=logger)
        raise

@server.call_tool()
async def batch_process(items: list, ctx) -> dict:
    """Process items with performance logging"""
    
    async with log_performance(ctx, "batch_process", "processor"):
        results = []
        
        for i, item in enumerate(items):
            async with log_performance(ctx, f"process_item_{i}", "processor"):
                result = await process_item(item)
                results.append(result)
        
        return {"processed": len(results)}
```

### Pattern 4: Multi-Level Logging Strategy (Expert)

```python
class SmartLogger:
    """Logger that adapts based on operation success/failure"""
    
    def __init__(self, ctx):
        self.ctx = ctx
        self.operations = []
        self.errors = []
    
    async def track_operation(self, name: str, level: str = "debug", **data):
        """Track operation with context"""
        self.operations.append({
            "name": name,
            "level": level,
            "data": data,
            "timestamp": time.time()
        })
        
        # Log immediately based on level
        log_fn = getattr(self.ctx, level)
        await log_fn(name, extra=data)
    
    async def track_error(self, error: Exception, context: dict):
        """Track error with full context"""
        self.errors.append({
            "error": str(error),
            "type": type(error).__name__,
            "context": context
        })
        
        await self.ctx.error(f"Error: {str(error)}", extra={
            "error_type": type(error).__name__,
            **context
        })
    
    async def summarize(self):
        """Log summary at appropriate level"""
        total_ops = len(self.operations)
        total_errors = len(self.errors)
        
        summary_data = {
            "total_operations": total_ops,
            "successful": total_ops - total_errors,
            "failed": total_errors
        }
        
        if total_errors == 0:
            await self.ctx.info("Operation completed successfully", 
                              extra=summary_data)
        elif total_errors < total_ops * 0.1:  # <10% failure
            await self.ctx.warning("Operation completed with errors", 
                                 extra=summary_data)
        else:
            await self.ctx.error("Operation failed", extra=summary_data)

@server.call_tool()
async def complex_operation(data: dict, ctx) -> dict:
    """Use smart logger for adaptive logging"""
    
    logger = SmartLogger(ctx)
    
    await logger.track_operation("operation_started", "info", 
                                data_size=len(data))
    
    try:
        await logger.track_operation("validation", "debug")
        validate(data)
        
        await logger.track_operation("processing", "debug", 
                                    items=len(data))
        results = await process(data)
        
        await logger.track_operation("storage", "debug", 
                                    records=len(results))
        await store(results)
        
    except Exception as e:
        await logger.track_error(e, {"operation": "complex_operation"})
        raise
    finally:
        await logger.summarize()
    
    return results
```

</div>

---

## 💻 Client Implementation

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern 1: Basic Log Handler (Beginner)

```python
from mcp.client import Client, StdioServerParameters
import asyncio

async def main():
    """Connect and listen for logs"""
    
    async with Client(
        StdioServerParameters(
            command="python",
            args=["server.py"]
        )
    ) as client:
        
        # Set log level
        await client.set_logging_level("info")
        
        # Register log handler
        @client.on_log
        def handle_log(params):
            level = params.get("level", "info")
            logger = params.get("logger", "server")
            data = params.get("data", {})
            
            print(f"[{level.upper()}] [{logger}]", data)
        
        # Use the server
        result = await client.call_tool("fetch_weather", {"city": "Tokyo"})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 2: Colored Console Output (Intermediate)

```python
from colorama import Fore, Style, init

init(autoreset=True)

LEVEL_COLORS = {
    "debug": Fore.CYAN,
    "info": Fore.GREEN,
    "notice": Fore.BLUE,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "critical": Fore.MAGENTA,
    "alert": Fore.RED + Style.BRIGHT,
    "emergency": Fore.WHITE + Style.BRIGHT
}

LEVEL_ICONS = {
    "debug": "🐛",
    "info": "ℹ️ ",
    "notice": "📢",
    "warning": "⚠️ ",
    "error": "❌",
    "critical": "🔴",
    "alert": "🚨",
    "emergency": "💥"
}

async def create_pretty_client():
    """Client with beautiful log display"""
    
    async with Client(...) as client:
        
        await client.set_logging_level("debug")
        
        @client.on_log
        def handle_log(params):
            level = params.get("level", "info")
            logger = params.get("logger", "server")
            data = params.get("data", {})
            
            color = LEVEL_COLORS.get(level, Fore.WHITE)
            icon = LEVEL_ICONS.get(level, "  ")
            
            # Format main message
            main_msg = data.get("message", str(data))
            print(f"{color}{icon} [{level.upper():9}] [{logger}] {main_msg}")
            
            # Format additional data
            for key, value in data.items():
                if key != "message":
                    print(f"    {key}: {value}")
        
        # Use client...
```

### Pattern 3: Log Filtering and Routing (Advanced)

```python
from typing import Callable, Dict, List

class LogRouter:
    """Route logs to different handlers based on criteria"""
    
    def __init__(self):
        self.handlers: List[Callable] = []
        self.level_handlers: Dict[str, List[Callable]] = {}
        self.logger_handlers: Dict[str, List[Callable]] = {}
    
    def add_handler(self, handler: Callable, 
                   levels: list = None, 
                   loggers: list = None):
        """Add handler with optional filtering"""
        
        if levels is None and loggers is None:
            # Global handler
            self.handlers.append(handler)
        else:
            if levels:
                for level in levels:
                    if level not in self.level_handlers:
                        self.level_handlers[level] = []
                    self.level_handlers[level].append(handler)
            
            if loggers:
                for logger in loggers:
                    if logger not in self.logger_handlers:
                        self.logger_handlers[logger] = []
                    self.logger_handlers[logger].append(handler)
    
    def route(self, params: dict):
        """Route log message to appropriate handlers"""
        level = params.get("level", "info")
        logger = params.get("logger", "server")
        
        # Call global handlers
        for handler in self.handlers:
            handler(params)
        
        # Call level-specific handlers
        for handler in self.level_handlers.get(level, []):
            handler(params)
        
        # Call logger-specific handlers
        for handler in self.logger_handlers.get(logger, []):
            handler(params)

async def main():
    """Use log router for sophisticated handling"""
    
    router = LogRouter()
    
    # Console handler for all logs
    def console_handler(params):
        print(f"[{params['level']}] {params.get('data', {})}")
    
    # File handler for errors only
    def error_file_handler(params):
        with open("errors.log", "a") as f:
            f.write(f"{datetime.now()}: {params}\n")
    
    # Metrics handler for performance logs
    def metrics_handler(params):
        if "duration_seconds" in params.get("data", {}):
            record_metric("duration", params["data"]["duration_seconds"])
    
    # Register handlers
    router.add_handler(console_handler)  # All logs
    router.add_handler(error_file_handler, 
                      levels=["error", "critical", "alert", "emergency"])
    router.add_handler(metrics_handler, loggers=["perf"])
    
    # Connect client
    async with Client(...) as client:
        await client.set_logging_level("info")
        
        @client.on_log
        def handle_log(params):
            router.route(params)
        
        # Use client...
```

### Pattern 4: Real-Time Log Dashboard (Expert)

```python
import asyncio
from collections import deque
from datetime import datetime

class LogDashboard:
    """Real-time log monitoring dashboard"""
    
    def __init__(self, max_logs: int = 100):
        self.logs = deque(maxlen=max_logs)
        self.stats = {
            "debug": 0, "info": 0, "notice": 0, "warning": 0,
            "error": 0, "critical": 0, "alert": 0, "emergency": 0
        }
        self.logger_stats = {}
    
    def add_log(self, params: dict):
        """Add log and update statistics"""
        timestamp = datetime.now()
        level = params.get("level", "info")
        logger = params.get("logger", "server")
        
        self.logs.append({
            "timestamp": timestamp,
            "level": level,
            "logger": logger,
            "data": params.get("data", {})
        })
        
        # Update stats
        self.stats[level] = self.stats.get(level, 0) + 1
        self.logger_stats[logger] = self.logger_stats.get(logger, 0) + 1
    
    def display(self):
        """Display dashboard"""
        print("\n" + "="*60)
        print("LOG DASHBOARD")
        print("="*60)
        
        # Overall stats
        print("\nLevel Statistics:")
        for level, count in self.stats.items():
            if count > 0:
                print(f"  {level:10} : {count:4} messages")
        
        # Logger stats
        print("\nLogger Statistics:")
        for logger, count in self.logger_stats.items():
            print(f"  {logger:15} : {count:4} messages")
        
        # Recent logs
        print("\nRecent Logs:")
        for log in list(self.logs)[-10:]:
            ts = log["timestamp"].strftime("%H:%M:%S")
            print(f"  [{ts}] [{log['level']:7}] [{log['logger']}]")
    
    async def auto_refresh(self, interval: float = 2.0):
        """Auto-refresh dashboard"""
        while True:
            self.display()
            await asyncio.sleep(interval)

async def main():
    """Run client with live dashboard"""
    
    dashboard = LogDashboard()
    
    async with Client(...) as client:
        await client.set_logging_level("debug")
        
        @client.on_log
        def handle_log(params):
            dashboard.add_log(params)
        
        # Start auto-refresh in background
        refresh_task = asyncio.create_task(
            dashboard.auto_refresh(interval=2.0)
        )
        
        try:
            # Use client normally
            while True:
                await client.call_tool("some_operation", {})
                await asyncio.sleep(1)
        finally:
            refresh_task.cancel()
```

</div>

---

## 🎯 Log Level Decision Tree

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### When to Use Each Level

```
Is this message about normal operation?
│
├─ YES → Is it detailed internal info?
│   │
│   ├─ YES → 🐛 DEBUG
│   │         (Function entry/exit, variable values)
│   │
│   └─ NO → ℹ️  INFO
│             (Operation progress, successful completion)
│
└─ NO → Is something wrong or unusual?
    │
    ├─ SOMEWHAT → Is it significant but not problematic?
    │   │
    │   ├─ YES → 📢 NOTICE
    │   │         (Configuration changes, user actions)
    │   │
    │   └─ NO → ⚠️  WARNING
    │             (Deprecated usage, approaching limits)
    │
    └─ YES → Did an operation fail?
        │
        ├─ PARTIALLY → ❌ ERROR
        │               (Retryable errors, single request failures)
        │
        └─ SEVERELY → Is system functionality impaired?
            │
            ├─ COMPONENT → 🔴 CRITICAL
            │              (Service down, major feature broken)
            │
            └─ SYSTEM → Does it need immediate human action?
                │
                ├─ URGENT → 🚨 ALERT
                │           (Data corruption, security breach)
                │
                └─ CATASTROPHIC → 💥 EMERGENCY
                                  (Complete system failure)
```

</div>

---

## 🛡️ Best Practices & Anti-Patterns

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO (Server)

**Level Selection:**
- Use DEBUG for tracing execution flow
- Use INFO for notable successful operations
- Use WARNING for concerning but non-fatal issues
- Use ERROR only when operations fail
- Reserve CRITICAL+ for serious system issues

**Message Content:**
- Include relevant context in `data` field
- Use structured data, not formatted strings
- Add timestamps for time-sensitive events
- Include operation IDs for correlation
- Remove sensitive information

**Performance:**
- Rate-limit high-frequency logs
- Use DEBUG liberally during development
- Reduce DEBUG in production
- Buffer logs before sending
- Make logging async

**Code Example:**
```python
# Good: Structured, contextual, appropriate level
await ctx.info("User authenticated", extra={
    "user_id": "usr_123",
    "method": "oauth",
    "duration_ms": 245
})

# Good: Error with full context
await ctx.error("Payment processing failed", extra={
    "transaction_id": "txn_789",
    "amount": 99.99,
    "error_code": "INSUFFICIENT_FUNDS",
    "retry_possible": True
})

# Good: Performance tracking
start = time.time()
result = await expensive_operation()
duration = time.time() - start

if duration > 5.0:
    await ctx.warning("Slow operation", extra={
        "operation": "data_sync",
        "duration_seconds": duration,
        "threshold": 5.0
    })
```

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T (Server)

**Level Misuse:**
- Don't use ERROR for warnings
- Don't use INFO for debug traces
- Don't log everything at same level
- Don't use EMERGENCY for regular errors
- Don't overuse high-severity levels

**Message Anti-Patterns:**
- Don't log sensitive data (passwords, tokens)
- Don't use unstructured string formatting
- Don't log personal identifying information
- Don't include massive data dumps
- Don't make logs human-unreadable

**Performance Pitfalls:**
- Don't log synchronously in hot paths
- Don't log every loop iteration
- Don't create log message if below threshold
- Don't forget to rate-limit
- Don't block operations for logging

**Bad Code:**
```python
# Bad: Wrong level (should be warning)
await ctx.error("Cache miss")

# Bad: Unstructured message
await ctx.info(f"User {user_id} did {action} at {time}")

# Bad: Sensitive data exposure
await ctx.debug("Auth attempt", extra={
    "username": "john",
    "password": "secret123"  # NEVER LOG THIS!
})

# Bad: Too verbose
for item in items:  # Could be 10,000 items
    await ctx.debug(f"Processing {item}")

# Bad: Blocking operation
with open("log.txt", "a") as f:  # Don't do file I/O
    f.write(log_message)
```

</div>

</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO (Client)

**Configuration:**
- Set appropriate initial log level
- Allow users to change level dynamically
- Respect server's logging capability
- Handle missing log fields gracefully

**Display:**
- Use colors/icons for visual clarity
- Show timestamp for each message
- Group related messages
- Make logs searchable
- Support log export

**Performance:**
- Handle high-frequency logs efficiently
- Use async processing
- Buffer display updates
- Limit memory usage

**Code Example:**
```python
# Good: Graceful handling
@client.on_log
def handle_log(params):
    level = params.get("level", "info")
    logger = params.get("logger", "unknown")
    data = params.get("data", {})
    
    # Safe extraction
    message = data.get("message", "")
    
    display_log(level, logger, message, data)

# Good: User control
async def set_user_log_level(client, level: str):
    """Allow user to change log level"""
    valid_levels = [
        "debug", "info", "notice", "warning",
        "error", "critical", "alert", "emergency"
    ]
    
    if level not in valid_levels:
        print(f"Invalid level. Choose from: {valid_levels}")
        return
    
    await client.set_logging_level(level)
    print(f"Log level set to: {level}")
```

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T (Client)

**Configuration Issues:**
- Don't ignore logging capability check
- Don't assume all logs will arrive
- Don't hardcode log level
- Don't fail if logging unavailable

**Display Problems:**
- Don't block UI thread for logs
- Don't spam console uncontrollably
- Don't lose logs in production
- Don't make logs unreadable

**Performance Mistakes:**
- Don't process every log synchronously
- Don't store unlimited logs in memory
- Don't fetch logs you don't need

**Bad Code:**
```python
# Bad: Blocking UI
@client.on_log
def handle_log(params):
    time.sleep(0.1)  # NEVER block!
    print(params)

# Bad: No error handling
@client.on_log
def handle_log(params):
    level = params["level"]  # KeyError if missing
    print(params["data"]["message"])  # Crash!

# Bad: Memory leak
all_logs = []  # Unbounded list
@client.on_log
def handle_log(params):
    all_logs.append(params)  # Grows forever

# Bad: Wrong log level request
await client.set_logging_level("verbose")  # Invalid!
```

</div>

</div>

---

## 🔔 Error Handling

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Standard Error Responses

**Invalid Log Level (-32602):**
```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "detail": "Invalid log level: 'verbose'. Must be one of: debug, info, notice, warning, error, critical, alert, emergency"
    }
  }
}
```

**Server Error (-32603):**
```json
{
  "jsonrpc": "2.0",
  "id": "124",
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": {
      "detail": "Failed to configure logging subsystem"
    }
  }
}
```

### Server Error Handling

```python
from mcp.server import Server
from mcp.types import McpError

VALID_LEVELS = [
    "debug", "info", "notice", "warning",
    "error", "critical", "alert", "emergency"
]

@server.set_logging_level()
async def handle_set_level(level: str) -> None:
    """Handle log level changes with validation"""
    
    # Validate level
    if level not in VALID_LEVELS:
        raise McpError(
            code=-32602,
            message="Invalid params",
            data={
                "detail": f"Invalid log level: '{level}'",
                "valid_levels": VALID_LEVELS
            }
        )
    
    try:
        # Update internal log level
        server.log_level = level
        
        # Log the change itself
        await server.info(f"Log level changed to {level}", extra={
            "previous_level": getattr(server, "_prev_level", "info"),
            "new_level": level
        })
        
    except Exception as e:
        raise McpError(
            code=-32603,
            message="Internal error",
            data={"detail": str(e)}
        )
```

### Client Error Handling

```python
async def safe_set_log_level(client: Client, level: str):
    """Set log level with error handling"""
    
    try:
        await client.set_logging_level(level)
        print(f"Log level set to: {level}")
        
    except McpError as e:
        if e.code == -32602:
            print(f"Invalid log level: {level}")
            print(f"Valid levels: {e.data.get('valid_levels', [])}")
        else:
            print(f"Error setting log level: {e.message}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

@client.on_log
def safe_log_handler(params):
    """Log handler with error protection"""
    
    try:
        level = params.get("level", "info")
        logger = params.get("logger", "server")
        data = params.get("data", {})
        
        display_log(level, logger, data)
        
    except Exception as e:
        # Don't let log handling crash the client
        print(f"Error handling log message: {e}", file=sys.stderr)
```

</div>

---

## 🎓 Real-World Use Cases

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">

### Use Case 1: Database Query Tool

**Challenge:** Users need visibility into slow queries and connection issues.

```python
@server.call_tool()
async def query_database(sql: str, ctx) -> dict:
    """Execute database query with comprehensive logging"""
    
    query_id = generate_id()
    
    await ctx.info("Database query started", extra={
        "query_id": query_id,
        "query_length": len(sql)
    }, logger="database")
    
    try:
        # Connection phase
        await ctx.debug("Acquiring connection from pool", extra={
            "query_id": query_id,
            "pool_size": db_pool.size,
            "active_connections": db_pool.active
        }, logger="database")
        
        conn = await db_pool.acquire()
        
        # Execution phase
        start = time.time()
        await ctx.debug("Executing query", extra={
            "query_id": query_id
        }, logger="database")
        
        result = await conn.execute(sql)
        duration = time.time() - start
        
        # Performance warning
        if duration > 2.0:
            await ctx.warning("Slow query detected", extra={
                "query_id": query_id,
                "duration_seconds": round(duration, 2),
                "threshold": 2.0,
                "suggestion": "Consider adding indexes"
            }, logger="database")
        else:
            await ctx.info("Query completed", extra={
                "query_id": query_id,
                "duration_seconds": round(duration, 2),
                "rows_affected": len(result)
            }, logger="database")
        
        return {"rows": result, "count": len(result)}
        
    except ConnectionError as e:
        await ctx.error("Database connection failed", extra={
            "query_id": query_id,
            "error": str(e),
            "retry_recommended": True
        }, logger="database")
        raise
        
    except TimeoutError as e:
        await ctx.error("Query timeout", extra={
            "query_id": query_id,
            "timeout_seconds": 30,
            "suggestion": "Query may be too complex"
        }, logger="database")
        raise
        
    finally:
        if conn:
            await db_pool.release(conn)
            await ctx.debug("Connection returned to pool", extra={
                "query_id": query_id
            }, logger="database")
```

### Use Case 2: API Integration Tool

**Challenge:** Track external API calls, rate limits, and failures.

```python
@server.call_tool()
async def fetch_api_data(endpoint: str, ctx) -> dict:
    """Fetch data from external API with detailed logging"""
    
    request_id = generate_id()
    
    await ctx.info("API request initiated", extra={
        "request_id": request_id,
        "endpoint": endpoint
    }, logger="api")
    
    try:
        # Rate limit check
        remaining = await rate_limiter.get_remaining()
        
        if remaining < 10:
            await ctx.warning("API rate limit low", extra={
                "request_id": request_id,
                "remaining_calls": remaining,
                "reset_time": rate_limiter.reset_time
            }, logger="api")
        
        await ctx.debug("Making HTTP request", extra={
            "request_id": request_id,
            "method": "GET",
            "url": f"https://api.example.com{endpoint}"
        }, logger="api")
        
        # Make request
        start = time.time()
        response = await http_client.get(endpoint)
        duration = time.time() - start
        
        await ctx.info("API request successful", extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "response_size_bytes": len(response.content)
        }, logger="api")
        
        return response.json()
        
    except RateLimitError as e:
        await ctx.error("Rate limit exceeded", extra={
            "request_id": request_id,
            "retry_after": e.retry_after,
            "recommendation": "Wait before retrying"
        }, logger="api")
        raise
        
    except TimeoutError:
        await ctx.error("API timeout", extra={
            "request_id": request_id,
            "timeout_seconds": 10
        }, logger="api")
        raise
        
    except Exception as e:
        await ctx.critical("Unexpected API error", extra={
            "request_id": request_id,
            "error_type": type(e).__name__,
            "error_message": str(e)
        }, logger="api")
        raise
```

### Use Case 3: Batch Processing Tool

**Challenge:** Monitor progress of long-running batch operations.

```python
@server.call_tool()
async def process_batch(items: list, ctx) -> dict:
    """Process batch with progress logging"""
    
    batch_id = generate_id()
    total = len(items)
    
    await ctx.info("Batch processing started", extra={
        "batch_id": batch_id,
        "total_items": total
    }, logger="batch")
    
    results = {"success": 0, "failed": 0, "errors": []}
    
    for i, item in enumerate(items):
        try:
            await ctx.debug(f"Processing item {i+1}/{total}", extra={
                "batch_id": batch_id,
                "item_id": item.get("id"),
                "progress_percent": round((i / total) * 100, 1)
            }, logger="batch")
            
            await process_item(item)
            results["success"] += 1
            
            # Progress milestones
            if (i + 1) % 100 == 0:
                await ctx.info(f"Progress: {i+1}/{total} items", extra={
                    "batch_id": batch_id,
                    "processed": i + 1,
                    "remaining": total - i - 1,
                    "success_rate": round(results["success"] / (i + 1) * 100, 1)
                }, logger="batch")
            
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({
                "item_id": item.get("id"),
                "error": str(e)
            })
            
            await ctx.error(f"Item processing failed", extra={
                "batch_id": batch_id,
                "item_id": item.get("id"),
                "error": str(e)
            }, logger="batch")
    
    # Final summary
    success_rate = round(results["success"] / total * 100, 1)
    
    if results["failed"] == 0:
        await ctx.info("Batch completed successfully", extra={
            "batch_id": batch_id,
            "total": total,
            "success": results["success"],
            "success_rate": success_rate
        }, logger="batch")
    elif results["failed"] < total * 0.1:
        await ctx.warning("Batch completed with some failures", extra={
            "batch_id": batch_id,
            "total": total,
            "success": results["success"],
            "failed": results["failed"],
            "success_rate": success_rate
        }, logger="batch")
    else:
        await ctx.error("Batch completed with high failure rate", extra={
            "batch_id": batch_id,
            "total": total,
            "success": results["success"],
            "failed": results["failed"],
            "success_rate": success_rate
        }, logger="batch")
    
    return results
```

</div>

---

## 🚀 Complete Working Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Server Implementation (server.py)

```python
from mcp.server.fastmcp import FastMCP
import time
import asyncio

mcp = FastMCP("Logging Demo Server")

@mcp.tool()
async def fetch_weather(city: str, ctx) -> str:
    """Fetch weather data with comprehensive logging"""
    
    await ctx.info(f"Weather request received for {city}", extra={
        "city": city,
        "request_time": time.time()
    })
    
    # Simulate checking cache
    await ctx.debug("Checking weather cache", extra={
        "cache_key": f"weather_{city.lower()}"
    })
    
    await asyncio.sleep(0.5)
    
    # Simulate cache miss
    await ctx.debug("Cache miss, calling weather API", extra={
        "city": city
    })
    
    # Simulate API call
    await ctx.info("Calling weather API", extra={
        "endpoint": "api.weather.com/v2/current",
        "city": city
    })
    
    await asyncio.sleep(1.0)
    
    # Simulate API response
    await ctx.info("Weather data retrieved", extra={
        "city": city,
        "temperature": 72,
        "conditions": "Sunny",
        "api_response_time_ms": 1000
    })
    
    return f"{city}: 72°F, Sunny"

@mcp.tool()
async def process_data(data: dict, ctx) -> dict:
    """Process data with error simulation"""
    
    await ctx.info("Starting data processing", extra={
        "data_size": len(data)
    })
    
    try:
        # Simulate validation
        await ctx.debug("Validating input data")
        
        if not data:
            await ctx.error("Empty data provided", extra={
                "expected": "non-empty dictionary"
            })
            raise ValueError("Data cannot be empty")
        
        # Simulate slow operation
        await ctx.debug("Applying transformations")
        start = time.time()
        await asyncio.sleep(3.0)
        duration = time.time() - start
        
        if duration > 2.0:
            await ctx.warning("Processing took longer than expected", extra={
                "duration_seconds": round(duration, 2),
                "threshold": 2.0
            })
        
        await ctx.info("Processing completed successfully", extra={
            "duration_seconds": round(duration, 2)
        })
        
        return {"status": "success", "processed": len(data)}
        
    except Exception as e:
        await ctx.error("Processing failed", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        raise

if __name__ == "__main__":
    mcp.run()
```

### Client Implementation (client.py)

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ANSI color codes
COLORS = {
    "debug": "\033[36m",      # Cyan
    "info": "\033[32m",       # Green
    "notice": "\033[34m",     # Blue
    "warning": "\033[33m",    # Yellow
    "error": "\033[31m",      # Red
    "critical": "\033[35m",   # Magenta
    "alert": "\033[91m",      # Bright Red
    "emergency": "\033[97m"   # Bright White
}
RESET = "\033[0m"

ICONS = {
    "debug": "🐛",
    "info": "ℹ️ ",
    "notice": "📢",
    "warning": "⚠️ ",
    "error": "❌",
    "critical": "🔴",
    "alert": "🚨",
    "emergency": "💥"
}

async def main():
    """Run logging demo client"""
    
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize
            await session.initialize()
            
            print("🚀 MCP Logging Demo Started\n")
            print("=" * 60)
            
            # Set log level to debug to see everything
            print("\n📊 Setting log level to 'debug'\n")
            await session.set_logging_level("debug")
            
            # Test 1: Normal operation
            print("\n" + "=" * 60)
            print("TEST 1: Normal Weather Fetch")
            print("=" * 60 + "\n")
            
            result = await session.call_tool("fetch_weather", {"city": "Tokyo"})
            print(f"\n✅ Result: {result.content[0].text}\n")
            
            # Wait a bit
            await asyncio.sleep(2)
            
            # Test 2: Error scenario
            print("\n" + "=" * 60)
            print("TEST 2: Error Scenario (Empty Data)")
            print("=" * 60 + "\n")
            
            try:
                result = await session.call_tool("process_data", {"data": {}})
            except Exception as e:
                print(f"\n❌ Expected error: {e}\n")
            
            # Wait a bit
            await asyncio.sleep(2)
            
            # Test 3: Change log level
            print("\n" + "=" * 60)
            print("TEST 3: Changing Log Level to 'info'")
            print("=" * 60 + "\n")
            
            await session.set_logging_level("info")
            print("ℹ️  Debug messages will now be filtered\n")
            
            result = await session.call_tool("fetch_weather", {"city": "Paris"})
            print(f"\n✅ Result: {result.content[0].text}\n")
            
            print("\n" + "=" * 60)
            print("Demo Complete!")
            print("=" * 60)

# Register log handler before running
def handle_log(params):
    """Handle incoming log messages with pretty formatting"""
    level = params.get("level", "info")
    logger = params.get("logger", "server")
    data = params.get("data", {})
    
    color = COLORS.get(level, "")
    icon = ICONS.get(level, "  ")
    
    # Extract message
    if isinstance(data, dict):
        message = data.get("message", "")
        if not message and "error" in data:
            message = data["error"]
    else:
        message = str(data)
    
    # Print main log line
    print(f"{color}{icon} [{level.upper():9}] [{logger:10}] {message}{RESET}")
    
    # Print additional context
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in ["message", "error"]:
                print(f"    {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected Output

```
🚀 MCP Logging Demo Started

============================================================

📊 Setting log level to 'debug'

============================================================
TEST 1: Normal Weather Fetch
============================================================

🐛 [DEBUG    ] [server    ] Checking weather cache
    cache_key: weather_tokyo
🐛 [DEBUG    ] [server    ] Cache miss, calling weather API
    city: Tokyo
ℹ️  [INFO     ] [server    ] Calling weather API
    endpoint: api.weather.com/v2/current
    city: Tokyo
ℹ️  [INFO     ] [server    ] Weather data retrieved
    city: Tokyo
    temperature: 72
    conditions: Sunny
    api_response_time_ms: 1000

✅ Result: Tokyo: 72°F, Sunny

============================================================
TEST 2: Error Scenario (Empty Data)
============================================================

🐛 [DEBUG    ] [server    ] Validating input data
❌ [ERROR    ] [server    ] Empty data provided
    expected: non-empty dictionary
❌ [ERROR    ] [server    ] Processing failed
    error: Data cannot be empty
    error_type: ValueError

❌ Expected error: Data cannot be empty

============================================================
TEST 3: Changing Log Level to 'info'
============================================================

ℹ️  Debug messages will now be filtered

ℹ️  [INFO     ] [server    ] Calling weather API
    endpoint: api.weather.com/v2/current
    city: Paris
ℹ️  [INFO     ] [server    ] Weather data retrieved
    city: Paris
    temperature: 72
    conditions: Sunny
    api_response_time_ms: 1000

✅ Result: Paris: 72°F, Sunny

============================================================
Demo Complete!
============================================================
```

</div>

---

## 🎯 Quick Reference Card

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; border-radius: 15px; margin: 30px 0;">

### Server Checklist

- ✅ Declare logging capability in initialization
- ✅ Use appropriate severity levels for each message
- ✅ Include structured data in `extra` parameter
- ✅ Use logger names to categorize messages
- ✅ Remove sensitive information before logging
- ✅ Rate-limit high-frequency log messages
- ✅ Make logging async and non-blocking
- ✅ Validate log level in setLevel handler

### Client Checklist

- ✅ Check for logging capability before using
- ✅ Set initial log level via `set_logging_level()`
- ✅ Register log message handler
- ✅ Handle missing fields gracefully
- ✅ Display logs with visual hierarchy
- ✅ Allow users to change log level
- ✅ Don't block UI thread processing logs
- ✅ Consider buffering for high-frequency logs

### Level Selection Guide

- 🐛 **DEBUG**: Function traces, variable dumps
- ℹ️  **INFO**: Successful operations, progress
- 📢 **NOTICE**: Config changes, notable events
- ⚠️  **WARNING**: Deprecated features, limits
- ❌ **ERROR**: Failed operations, retryable
- 🔴 **CRITICAL**: Major component failures
- 🚨 **ALERT**: Security issues, data corruption
- 💥 **EMERGENCY**: Complete system failure

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Think of Logging as a Conversation

**Without Logging:**  
Silent partner—you have no idea what they're doing or thinking

**↓**

**With Logging:**  
Communicative partner—narrates actions, warnings, and problems

**↓**

**Log Levels = Tone of Voice:**  
Debug: Whisper (detailed minutiae)  
Info: Normal voice (regular updates)  
Warning: Raised voice (concern)  
Error: Shout (something went wrong!)  
Emergency: SCREAM (everything is on fire!)

**↓**

**Result:**  
Transparent operations, easy debugging, user confidence, operational intelligence

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"MCP logging enables servers to send structured diagnostic messages to clients using RFC 5424's 8 severity levels (debug through emergency), with clients controlling verbosity via logging/setLevel requests and servers sending notifications/message notifications containing level, optional logger name, and arbitrary JSON context data."*

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now master MCP logging from basic concepts to advanced implementation patterns.**  
Build transparent, debuggable MCP servers that communicate clearly with their clients! 📋✨

</div>
