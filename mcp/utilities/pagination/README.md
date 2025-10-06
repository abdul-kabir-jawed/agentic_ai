# 📄 MCP Pagination Mastery Guide

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is MCP Pagination?

**Pagination** is MCP's mechanism for handling large result sets by breaking them into smaller, manageable chunks called **pages**. Instead of overwhelming clients with thousands of items at once, servers deliver data incrementally using an **opaque cursor-based system**.

> **Think of it like this:** Reading a book chapter by chapter with a bookmark, not trying to read all 1000 pages at once. The bookmark (cursor) remembers your position, and you can continue reading from where you left off.

</div>

---

## 🤔 The Problem Pagination Solves

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Scenario: Database Query Server

**User requests:** *"List all available resources"*

**Without Pagination:**
```
❌ Server loads 10,000 resources into memory
❌ Serializes massive 50MB JSON response
❌ Network timeout after 30 seconds
❌ Client crashes trying to parse huge payload
❌ User sees: "Request failed" 
```

**With Pagination:**
```
✅ Server sends first 100 resources (500KB)
✅ Response includes cursor: "eyJwYWdlIjoxfQ=="
✅ Client processes first page instantly
✅ User sees results immediately
✅ Client requests next page when needed
✅ Smooth, responsive experience
```

**The Magic:** Pagination transforms overwhelming data dumps into smooth, incremental loading—better performance, reliability, and user experience.

</div>

---

## 🎯 Core Concept: Cursor-Based Pagination

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🔖 Opaque Cursors
Position markers that track progress

*Client treats as black box*

</div>

<div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 📦 Dynamic Page Sizes
Server controls chunk size

*Not fixed, client adapts*

</div>

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### ♾️ Stateless Operation
Each request is independent

*No server-side session needed*

</div>

</div>

---

## 🏗️ Pagination Flow Structure

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Initial Request (No Cursor)

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "method": "resources/list",
  "params": {}
}
```

### Initial Response (With nextCursor)

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {
    "resources": [
      {"uri": "file:///doc1.txt", "name": "Document 1"},
      {"uri": "file:///doc2.txt", "name": "Document 2"},
      // ... 98 more items
    ],
    "nextCursor": "eyJwYWdlIjoxLCJvZmZzZXQiOjEwMH0="
  }
}
```

### Subsequent Request (With Cursor)

```json
{
  "jsonrpc": "2.0",
  "id": "124",
  "method": "resources/list",
  "params": {
    "cursor": "eyJwYWdlIjoxLCJvZmZzZXQiOjEwMH0="
  }
}
```

### Final Response (No nextCursor = End)

```json
{
  "jsonrpc": "2.0",
  "id": "125",
  "result": {
    "resources": [
      {"uri": "file:///doc201.txt", "name": "Document 201"}
    ]
  }
}
```

**Key:** Missing `nextCursor` signals no more pages!

</div>

---

## 🔄 The Complete Pagination Workflow

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #f093fb;">

### Step-by-Step Flow

```
1. 👤 Client requests list (no cursor)
        ↓
2. 🔧 Server queries first page from data source
        ↓
3. 🧮 Server calculates if more pages exist
        ↓
4. 🔖 Server generates cursor if more data available
        ↓
5. 📤 Server sends: page + nextCursor
        ↓
6. 💻 Client processes first page
        ↓
7. 🔄 Client requests next page with cursor
        ↓
8. 🔧 Server decodes cursor to find position
        ↓
9. 📊 Server fetches next page from that position
        ↓
10. 🔁 Repeat steps 3-9 until nextCursor is absent
        ↓
11. ✅ Client has all data, pagination complete
```

</div>

---

## 💡 Perfect Example: Document Library

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 15px; margin: 20px 0;">

### The Scenario

A document management server with 1,500 files needs to list resources.

**Challenge:** Sending all 1,500 at once would be slow and unreliable.

**Solution:** Paginate with 100 items per page.

### Page-by-Page Journey

**Page 1 Request:**
```json
{"method": "resources/list", "params": {}}
```

**Page 1 Response:**
```json
{
  "resources": [
    // 100 documents (items 1-100)
  ],
  "nextCursor": "eyJvZmZzZXQiOjEwMH0="
}
```

**Page 2 Request:**
```json
{
  "method": "resources/list",
  "params": {"cursor": "eyJvZmZzZXQiOjEwMH0="}
}
```

**Page 2 Response:**
```json
{
  "resources": [
    // 100 documents (items 101-200)
  ],
  "nextCursor": "eyJvZmZzZXQiOjIwMH0="
}
```

**... continues for 15 pages ...**

**Page 15 Request:**
```json
{
  "method": "resources/list",
  "params": {"cursor": "eyJvZmZzZXQiOjE0MDB9"}
}
```

**Page 15 Response (Final):**
```json
{
  "resources": [
    // 100 documents (items 1401-1500)
  ]
  // NO nextCursor = We're done!
}
```

**Result:** Client retrieved 1,500 items smoothly in 15 manageable chunks!

</div>

---

## 🎭 Operations Supporting Pagination

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### 📚 resources/list

**Purpose:** List available resources

**Example:**
```json
{
  "method": "resources/list",
  "params": {"cursor": "..."}
}
```

**Response:**
```json
{
  "resources": [...],
  "nextCursor": "..."
}
```

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### 📋 resources/templates/list

**Purpose:** List resource templates

**Example:**
```json
{
  "method": "resources/templates/list",
  "params": {"cursor": "..."}
}
```

**Response:**
```json
{
  "resourceTemplates": [...],
  "nextCursor": "..."
}
```

</div>

<div style="background: #e8f5e9; padding: 20px; border-radius: 10px;">

### 💬 prompts/list

**Purpose:** List available prompts

**Example:**
```json
{
  "method": "prompts/list",
  "params": {"cursor": "..."}
}
```

**Response:**
```json
{
  "prompts": [...],
  "nextCursor": "..."
}
```

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px;">

### 🔧 tools/list

**Purpose:** List available tools

**Example:**
```json
{
  "method": "tools/list",
  "params": {"cursor": "..."}
}
```

**Response:**
```json
{
  "tools": [...],
  "nextCursor": "..."
}
```

</div>

</div>

---

## 💻 Server Implementation Patterns

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern 1: Simple Offset-Based Pagination (Beginner)

```python
import base64
import json
from mcp.server import Server
from mcp.types import Resource, ListResourcesResult

# Sample dataset
ALL_RESOURCES = [
    Resource(uri=f"file:///doc{i}.txt", name=f"Document {i}")
    for i in range(1, 1501)  # 1500 resources
]

PAGE_SIZE = 100

def create_cursor(offset: int) -> str:
    """Create opaque cursor from offset"""
    cursor_data = {"offset": offset}
    return base64.b64encode(
        json.dumps(cursor_data).encode()
    ).decode()

def parse_cursor(cursor: str) -> int:
    """Extract offset from cursor"""
    cursor_data = json.loads(
        base64.b64decode(cursor.encode()).decode()
    )
    return cursor_data["offset"]

@server.list_resources()
async def handle_list_resources(cursor: str | None = None) -> ListResourcesResult:
    """Handle paginated resource listing"""
    
    # Determine starting position
    offset = 0 if cursor is None else parse_cursor(cursor)
    
    # Get current page
    page_resources = ALL_RESOURCES[offset:offset + PAGE_SIZE]
    
    # Calculate next cursor
    next_offset = offset + PAGE_SIZE
    next_cursor = None
    if next_offset < len(ALL_RESOURCES):
        next_cursor = create_cursor(next_offset)
    
    return ListResourcesResult(
        resources=page_resources,
        nextCursor=next_cursor
    )
```

### Pattern 2: Database Query Pagination (Intermediate)

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

@server.list_resources()
async def handle_list_resources(cursor: str | None = None) -> ListResourcesResult:
    """Paginate database results"""
    
    offset = 0 if cursor is None else parse_cursor(cursor)
    
    # Database query with limit/offset
    async with get_db_session() as session:
        stmt = (
            select(DocumentModel)
            .offset(offset)
            .limit(PAGE_SIZE + 1)  # +1 to check if more exist
        )
        results = await session.execute(stmt)
        documents = results.scalars().all()
    
    # Check if more pages exist
    has_more = len(documents) > PAGE_SIZE
    page_documents = documents[:PAGE_SIZE]
    
    # Convert to resources
    resources = [
        Resource(uri=doc.uri, name=doc.name)
        for doc in page_documents
    ]
    
    # Generate next cursor if needed
    next_cursor = None
    if has_more:
        next_cursor = create_cursor(offset + PAGE_SIZE)
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Pattern 3: Keyset-Based Pagination (Advanced)

```python
from datetime import datetime

def create_keyset_cursor(last_id: int, last_created: datetime) -> str:
    """Create cursor based on last item's unique identifiers"""
    cursor_data = {
        "last_id": last_id,
        "last_created": last_created.isoformat()
    }
    return base64.b64encode(json.dumps(cursor_data).encode()).decode()

def parse_keyset_cursor(cursor: str) -> tuple[int, datetime]:
    """Extract keyset from cursor"""
    data = json.loads(base64.b64decode(cursor.encode()).decode())
    return data["last_id"], datetime.fromisoformat(data["last_created"])

@server.list_resources()
async def handle_list_resources(cursor: str | None = None) -> ListResourcesResult:
    """Keyset pagination (better for large, changing datasets)"""
    
    async with get_db_session() as session:
        if cursor is None:
            # First page
            stmt = (
                select(DocumentModel)
                .order_by(DocumentModel.created_at, DocumentModel.id)
                .limit(PAGE_SIZE + 1)
            )
        else:
            # Subsequent pages
            last_id, last_created = parse_keyset_cursor(cursor)
            stmt = (
                select(DocumentModel)
                .where(
                    (DocumentModel.created_at > last_created) |
                    (
                        (DocumentModel.created_at == last_created) &
                        (DocumentModel.id > last_id)
                    )
                )
                .order_by(DocumentModel.created_at, DocumentModel.id)
                .limit(PAGE_SIZE + 1)
            )
        
        results = await session.execute(stmt)
        documents = results.scalars().all()
    
    # Check if more exist
    has_more = len(documents) > PAGE_SIZE
    page_documents = documents[:PAGE_SIZE]
    
    # Convert to resources
    resources = [
        Resource(uri=doc.uri, name=doc.name)
        for doc in page_documents
    ]
    
    # Generate next cursor
    next_cursor = None
    if has_more:
        last_doc = page_documents[-1]
        next_cursor = create_keyset_cursor(last_doc.id, last_doc.created_at)
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Pattern 4: API-Based Pagination (Expert)

```python
import httpx

@server.list_resources()
async def handle_list_resources(cursor: str | None = None) -> ListResourcesResult:
    """Paginate results from external API"""
    
    # External API uses its own pagination
    api_cursor = None if cursor is None else parse_cursor(cursor)
    
    async with httpx.AsyncClient() as client:
        params = {"limit": PAGE_SIZE}
        if api_cursor:
            params["cursor"] = api_cursor
        
        response = await client.get(
            "https://api.example.com/documents",
            params=params
        )
        data = response.json()
    
    # Convert API response to MCP resources
    resources = [
        Resource(uri=item["url"], name=item["title"])
        for item in data["items"]
    ]
    
    # Map API's next cursor to MCP cursor
    next_cursor = None
    if data.get("next_cursor"):
        next_cursor = create_cursor_from_api(data["next_cursor"])
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

</div>

---

## 💻 Client Implementation

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Basic Client Pattern

```python
from mcp.client import Client, StdioServerParameters

async def fetch_all_resources():
    """Fetch all resources using pagination"""
    
    async with Client(
        StdioServerParameters(command="python", args=["server.py"])
    ) as client:
        
        all_resources = []
        cursor = None
        page_num = 1
        
        while True:
            print(f"Fetching page {page_num}...")
            
            # Request page
            result = await client.list_resources(cursor=cursor)
            
            # Collect resources
            all_resources.extend(result.resources)
            print(f"  Got {len(result.resources)} resources")
            
            # Check if more pages exist
            if result.nextCursor is None:
                print("No more pages!")
                break
            
            # Continue to next page
            cursor = result.nextCursor
            page_num += 1
        
        print(f"\nTotal resources fetched: {len(all_resources)}")
        return all_resources
```

### Advanced Client with Progress Tracking

```python
from typing import AsyncIterator

async def paginate_resources(
    client: Client,
    on_progress: callable = None
) -> AsyncIterator[Resource]:
    """Generator that yields resources as they're fetched"""
    
    cursor = None
    total_fetched = 0
    
    while True:
        result = await client.list_resources(cursor=cursor)
        
        for resource in result.resources:
            total_fetched += 1
            if on_progress:
                on_progress(total_fetched, resource)
            yield resource
        
        if result.nextCursor is None:
            break
        
        cursor = result.nextCursor

# Usage
async def main():
    async with Client(...) as client:
        async for resource in paginate_resources(
            client,
            on_progress=lambda count, res: print(f"[{count}] {res.name}")
        ):
            # Process each resource as it arrives
            await process_resource(resource)
```

### Client with Concurrent Page Fetching

```python
import asyncio
from collections import deque

async def fetch_resources_parallel(client: Client, prefetch_pages: int = 3):
    """Fetch multiple pages concurrently for better performance"""
    
    all_resources = []
    pending_requests = deque()
    
    # Start with first page
    pending_requests.append(client.list_resources(cursor=None))
    
    while pending_requests:
        # Fetch next completed page
        result = await pending_requests.popleft()
        all_resources.extend(result.resources)
        
        # If more pages exist and we haven't reached prefetch limit
        if result.nextCursor and len(pending_requests) < prefetch_pages:
            # Queue next page request
            pending_requests.append(
                client.list_resources(cursor=result.nextCursor)
            )
    
    return all_resources
```

</div>

---

## 🎯 Cursor Design Strategies

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ Good Cursor Design

**Characteristics:**
- Opaque (base64-encoded)
- Contains position info
- Stateless
- Short-lived valid
- Version-aware

**Example:**
```python
# Encode meaningful data
cursor = {
    "version": 1,
    "offset": 100,
    "timestamp": "2025-01-15T10:00:00Z"
}
encoded = base64.b64encode(
    json.dumps(cursor).encode()
).decode()
```

**Benefits:**
- Server remains stateless
- Client treats as opaque
- Easy to validate
- Can evolve over time

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ Poor Cursor Design

**Anti-Patterns:**
- Plain text offsets: `"page=2"`
- Transparent format: `"100"`
- Session-dependent: `"sess_abc_p2"`
- Long-lived: Never expires
- Unversioned: Can't evolve

**Example:**
```python
# Bad: Transparent, no encoding
cursor = "offset=100"

# Bad: Exposes internals
cursor = "SELECT * FROM docs LIMIT 100 OFFSET 100"
```

**Problems:**
- Clients might manipulate
- Hard to change format
- Security risks
- Coupling issues

</div>

</div>

---

## 🛡️ Best Practices & Patterns

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO (Server)

**Cursor Management:**
- Make cursors opaque (base64)
- Include version in cursor
- Validate cursor format
- Handle invalid cursors gracefully
- Set reasonable page sizes

**Performance:**
- Index database columns used in pagination
- Use efficient queries (keyset > offset for large sets)
- Cache expensive calculations
- Consider cursor expiration

**Code Example:**
```python
def create_cursor(offset: int) -> str:
    data = {
        "v": 1,  # Version
        "off": offset,
        "ts": time.time()  # Timestamp
    }
    return base64.b64encode(
        json.dumps(data).encode()
    ).decode()

def validate_cursor(cursor: str) -> bool:
    try:
        data = json.loads(
            base64.b64decode(cursor).decode()
        )
        # Check version
        if data.get("v") != 1:
            return False
        # Check expiration
        if time.time() - data.get("ts", 0) > 3600:
            return False
        return True
    except:
        return False
```

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T (Server)

**Cursor Anti-Patterns:**
- Use transparent cursors
- Store state server-side per cursor
- Make cursors never expire
- Allow client-controlled page sizes
- Expose internal query structure

**Performance Pitfalls:**
- Use offset pagination for huge datasets
- Forget to index sort columns
- Return too many items per page
- Make blocking I/O calls

**Bad Code:**
```python
# Bad: Transparent cursor
def create_cursor(page: int) -> str:
    return str(page)

# Bad: No validation
def parse_cursor(cursor: str) -> int:
    return int(cursor)  # Crashes on invalid input

# Bad: Client controls page size
def handle_list(cursor, limit):
    # What if limit=1000000?
    return items[:limit]
```

</div>

</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO (Client)

**Cursor Handling:**
- Treat cursor as opaque string
- Never parse or modify cursors
- Don't persist cursors across sessions
- Check for `nextCursor` absence

**User Experience:**
- Show loading indicators
- Allow user to stop pagination
- Display progress
- Handle errors gracefully

**Code Example:**
```python
async def fetch_all(client):
    resources = []
    cursor = None
    
    while True:
        try:
            result = await client.list_resources(
                cursor=cursor
            )
            resources.extend(result.resources)
            
            # Critical: Check nextCursor
            if result.nextCursor is None:
                break
            
            cursor = result.nextCursor
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    return resources
```

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T (Client)

**Cursor Misuse:**
- Parse cursor content
- Modify cursor values
- Cache cursors long-term
- Assume fixed page sizes
- Assume cursor format

**UX Anti-Patterns:**
- Block UI during pagination
- No way to cancel
- No progress feedback
- Crash on pagination errors

**Bad Code:**
```python
# Bad: Parsing cursor
cursor_data = json.loads(
    base64.b64decode(cursor)
)
cursor_data["offset"] += 50  # Manipulating!

# Bad: Assuming page size
total_pages = total_items / 100  # Wrong!

# Bad: Persisting cursors
save_to_file(cursor)  # May be invalid later

# Bad: No end check
while cursor:  # Wrong! Check nextCursor
    result = await client.list_resources(cursor)
    cursor = result.nextCursor  # Infinite loop if None!
```

</div>

</div>

---

## 🔔 Error Handling

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Standard Error Responses

**Invalid Cursor (-32602):**
```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "detail": "Invalid or expired cursor"
    }
  }
}
```

### Server Error Handling Pattern

```python
@server.list_resources()
async def handle_list_resources(cursor: str | None = None):
    """Handle pagination with proper error handling"""
    
    try:
        # Validate cursor if provided
        if cursor is not None:
            if not validate_cursor(cursor):
                raise ValueError("Invalid cursor format")
            
            offset = parse_cursor(cursor)
            
            # Check if cursor expired
            if is_cursor_expired(cursor):
                raise ValueError("Cursor has expired")
        else:
            offset = 0
        
        # Fetch data
        resources = await fetch_resources(offset, PAGE_SIZE)
        
        # Generate next cursor
        next_cursor = None
        if len(resources) == PAGE_SIZE:
            next_cursor = create_cursor(offset + PAGE_SIZE)
        
        return ListResourcesResult(
            resources=resources,
            nextCursor=next_cursor
        )
        
    except ValueError as e:
        # Invalid cursor
        raise MCPError(
            code=-32602,
            message="Invalid params",
            data={"detail": str(e)}
        )
    except Exception as e:
        # Internal error
        raise MCPError(
            code=-32603,
            message="Internal error",
            data={"detail": str(e)}
        )
```

### Client Error Handling Pattern

```python
async def fetch_all_with_retry(client: Client, max_retries: int = 3):
    """Fetch all resources with error handling and retry"""
    
    resources = []
    cursor = None
    retries = 0
    
    while True:
        try:
            result = await client.list_resources(cursor=cursor)
            resources.extend(result.resources)
            retries = 0  # Reset on success
            
            if result.nextCursor is None:
                break
            
            cursor = result.nextCursor
            
        except InvalidCursorError:
            print("Invalid cursor, restarting from beginning")
            cursor = None  # Restart pagination
            resources = []  # Clear partial results
            
        except TimeoutError:
            retries += 1
            if retries >= max_retries:
                print("Max retries reached")
                break
            print(f"Timeout, retrying... ({retries}/{max_retries})")
            await asyncio.sleep(2 ** retries)  # Exponential backoff
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    return resources
```

</div>

---

## 🎓 Real-World Use Cases

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">

### Use Case 1: GitHub Repository Browser

**Challenge:** List all repositories in an organization (could be 1000+)

**Implementation:**
```python
@server.list_resources()
async def list_github_repos(cursor: str | None = None):
    """Paginate through GitHub repositories"""
    
    # GitHub's API uses page numbers
    page = 1 if cursor is None else parse_cursor(cursor)
    
    # Fetch from GitHub API
    repos = await github_client.get_repos(
        org="myorg",
        page=page,
        per_page=100
    )
    
    # Convert to MCP resources
    resources = [
        Resource(
            uri=f"github://{repo.full_name}",
            name=repo.name,
            description=repo.description
        )
        for repo in repos
    ]
    
    # Check if more pages exist
    next_cursor = None
    if len(repos) == 100:  # Full page = more might exist
        next_cursor = create_cursor(page + 1)
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Use Case 2: Database Document Store

**Challenge:** List millions of documents efficiently

**Implementation:**
```python
@server.list_resources()
async def list_documents(cursor: str | None = None):
    """Keyset pagination for large document store"""
    
    async with get_db() as db:
        if cursor is None:
            # First page
            docs = await db.documents.find(
                {}, 
                limit=100,
                sort=[("_id", 1)]
            ).to_list()
        else:
            # Subsequent pages using last ID
            last_id = parse_cursor(cursor)
            docs = await db.documents.find(
                {"_id": {"$gt": last_id}},
                limit=100,
                sort=[("_id", 1)]
            ).to_list()
    
    resources = [
        Resource(uri=f"doc://{doc['_id']}", name=doc['title'])
        for doc in docs
    ]
    
    next_cursor = None
    if len(docs) == 100:
        next_cursor = create_cursor(docs[-1]['_id'])
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Use Case 3: Cloud Storage Browser

**Challenge:** Browse thousands of files in cloud storage

**Implementation:**
```python
@server.list_resources()
async def list_s3_objects(cursor: str | None = None):
    """Paginate through S3 objects"""
    
    import boto3
    s3 = boto3.client('s3')
    
    # S3 provides its own continuation token
    kwargs = {
        'Bucket': 'my-bucket',
        'MaxKeys': 100
    }
    
    if cursor is not None:
        # S3's token can be used directly
        s3_token = parse_cursor(cursor)
        kwargs['ContinuationToken'] = s3_token
    
    response = s3.list_objects_v2(**kwargs)
    
    resources = [
        Resource(
            uri=f"s3://my-bucket/{obj['Key']}",
            name=obj['Key'],
            mimeType=guess_mime_type(obj['Key'])
        )
        for obj in response.get('Contents', [])
    ]
    
    # Map S3's continuation token to MCP cursor
    next_cursor = None
    if response.get('IsTruncated'):
        next_cursor = create_cursor(response['NextContinuationToken'])
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

</div>

---

## 🧠 Advanced Patterns

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern: Filtered Pagination

```python
@server.list_resources()
async def list_resources_filtered(
    cursor: str | None = None,
    filter_type: str | None = None
):
    """Paginate with filters"""
    
    # Include filter in cursor
    if cursor is None:
        offset = 0
        filter_val = filter_type
    else:
        cursor_data = parse_cursor(cursor)
        offset = cursor_data['offset']
        filter_val = cursor_data.get('filter')
    
    # Query with filter
    query = {"type": filter_val} if filter_val else {}
    resources = await db.resources.find(
        query,
        skip=offset,
        limit=PAGE_SIZE
    ).to_list()
    
    # Preserve filter in next cursor
    next_cursor = None
    if len(resources) == PAGE_SIZE:
        next_cursor = create_cursor({
            'offset': offset + PAGE_SIZE,
            'filter': filter_val
        })
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Pattern: Stable Sorting

```python
@server.list_resources()
async def list_resources_stable(cursor: str | None = None):
    """Ensure stable ordering across pagination"""
    
    if cursor is None:
        offset = 0
        sort_timestamp = datetime.now()
    else:
        cursor_data = parse_cursor(cursor)
        offset = cursor_data['offset']
        sort_timestamp = datetime.fromisoformat(cursor_data['ts'])
    
    # Get resources created BEFORE pagination started
    # This prevents new items from shifting results
    resources = await db.resources.find(
        {"created_at": {"$lte": sort_timestamp}},
        skip=offset,
        limit=PAGE_SIZE,
        sort=[("created_at", -1), ("_id", -1)]
    ).to_list()
    
    next_cursor = None
    if len(resources) == PAGE_SIZE:
        next_cursor = create_cursor({
            'offset': offset + PAGE_SIZE,
            'ts': sort_timestamp.isoformat()
        })
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

### Pattern: Parallel Pagination

```python
async def fetch_multiple_lists_parallel(client: Client):
    """Fetch multiple paginated lists concurrently"""
    
    async def fetch_all_resources():
        all_items = []
        cursor = None
        while True:
            result = await client.list_resources(cursor=cursor)
            all_items.extend(result.resources)
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return all_items
    
    async def fetch_all_tools():
        all_items = []
        cursor = None
        while True:
            result = await client.list_tools(cursor=cursor)
            all_items.extend(result.tools)
            if result.nextCursor is None:
                break
            cursor = result.nextCursor
        return all_items
    
    # Fetch both concurrently
    resources, tools = await asyncio.gather(
        fetch_all_resources(),
        fetch_all_tools()
    )
    
    return resources, tools
```

</div>

---

## 📊 Performance Considerations

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 25px; border-radius: 10px;">

### ⚡ Optimization Strategies

**Database Level:**
```sql
-- Create indexes for pagination queries
CREATE INDEX idx_documents_created 
ON documents(created_at, id);

-- Use covering indexes
CREATE INDEX idx_documents_list 
ON documents(created_at, id, title, uri);
```

**Application Level:**
```python
# Use connection pooling
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    "postgresql://...",
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10
)

# Batch operations
async def fetch_page(offset: int):
    # Fetch page
    resources = await fetch_resources(offset)
    
    # Prefetch related data in bulk
    resource_ids = [r.id for r in resources]
    metadata = await fetch_metadata_bulk(resource_ids)
    
    return resources
```

**Caching Strategy:**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_page_cache_key(cursor: str, filters: str) -> str:
    return hashlib.sha256(
        f"{cursor}:{filters}".encode()
    ).hexdigest()

async def cached_list_resources(cursor, filters):
    cache_key = get_page_cache_key(cursor, filters)
    
    # Check cache
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    result = await fetch_resources(cursor, filters)
    
    # Cache for 5 minutes
    await redis.setex(
        cache_key, 
        300, 
        json.dumps(result)
    )
    
    return result
```

</div>

<div style="background: #fff3cd; padding: 25px; border-radius: 10px;">

### 📏 Page Size Guidelines

**General Rules:**

| Data Type | Recommended Size | Reason |
|-----------|-----------------|---------|
| Small objects | 100-200 | Fast response |
| Medium objects | 50-100 | Balanced |
| Large objects | 20-50 | Avoid timeouts |
| With images | 10-20 | Network limits |

**Adaptive Page Sizing:**
```python
def calculate_page_size(avg_item_size: int) -> int:
    """Calculate optimal page size based on item size"""
    
    # Target: ~1MB per page
    target_size = 1024 * 1024  # 1MB
    
    # Calculate items per page
    items_per_page = target_size // avg_item_size
    
    # Clamp between min and max
    return max(10, min(items_per_page, 200))

@server.list_resources()
async def adaptive_pagination(cursor: str | None = None):
    # Calculate based on resource type
    avg_size = await get_avg_resource_size()
    page_size = calculate_page_size(avg_size)
    
    # Use calculated page size
    offset = 0 if cursor is None else parse_cursor(cursor)
    resources = await fetch_resources(offset, page_size)
    
    next_cursor = None
    if len(resources) == page_size:
        next_cursor = create_cursor(offset + page_size)
    
    return ListResourcesResult(
        resources=resources,
        nextCursor=next_cursor
    )
```

</div>

</div>

---

## 🎓 Testing Pagination

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Unit Test Suite

```python
import pytest
from mcp.types import ListResourcesResult

@pytest.mark.asyncio
async def test_first_page_no_cursor():
    """Test first page returns results and cursor"""
    result = await handle_list_resources(cursor=None)
    
    assert isinstance(result, ListResourcesResult)
    assert len(result.resources) > 0
    assert result.nextCursor is not None

@pytest.mark.asyncio
async def test_last_page_no_cursor():
    """Test last page has no nextCursor"""
    # Navigate to last page
    cursor = None
    while True:
        result = await handle_list_resources(cursor=cursor)
        if result.nextCursor is None:
            # This is the last page
            assert len(result.resources) <= PAGE_SIZE
            break
        cursor = result.nextCursor

@pytest.mark.asyncio
async def test_invalid_cursor():
    """Test invalid cursor returns error"""
    with pytest.raises(MCPError) as exc:
        await handle_list_resources(cursor="invalid_cursor")
    assert exc.value.code == -32602

@pytest.mark.asyncio
async def test_pagination_consistency():
    """Test pagination returns all items exactly once"""
    all_resources = []
    cursor = None
    seen_ids = set()
    
    while True:
        result = await handle_list_resources(cursor=cursor)
        
        # Check for duplicates
        for resource in result.resources:
            assert resource.uri not in seen_ids, "Duplicate found!"
            seen_ids.add(resource.uri)
        
        all_resources.extend(result.resources)
        
        if result.nextCursor is None:
            break
        cursor = result.nextCursor
    
    # Verify we got all resources
    total_count = await get_total_resource_count()
    assert len(all_resources) == total_count

@pytest.mark.asyncio
async def test_empty_result():
    """Test empty dataset returns empty list, no cursor"""
    # Clear all resources
    await clear_all_resources()
    
    result = await handle_list_resources(cursor=None)
    assert result.resources == []
    assert result.nextCursor is None

@pytest.mark.asyncio
async def test_single_page():
    """Test dataset smaller than page size"""
    # Add only 10 resources (page size is 100)
    await add_resources(count=10)
    
    result = await handle_list_resources(cursor=None)
    assert len(result.resources) == 10
    assert result.nextCursor is None

@pytest.mark.asyncio
async def test_exact_page_boundary():
    """Test dataset exactly equal to page size"""
    # Add exactly 100 resources
    await add_resources(count=100)
    
    # First page
    result = await handle_list_resources(cursor=None)
    assert len(result.resources) == 100
    
    # Should have no next cursor (all data retrieved)
    # OR should have next cursor with empty second page
    if result.nextCursor:
        second_result = await handle_list_resources(
            cursor=result.nextCursor
        )
        assert len(second_result.resources) == 0
        assert second_result.nextCursor is None
```

### Integration Test

```python
@pytest.mark.asyncio
async def test_client_server_pagination():
    """End-to-end pagination test"""
    
    # Setup server with known data
    test_resources = [
        Resource(uri=f"test://{i}", name=f"Resource {i}")
        for i in range(250)  # 3 pages at 100 per page
    ]
    await setup_test_resources(test_resources)
    
    # Start server
    async with start_test_server() as server:
        # Connect client
        async with create_test_client(server) as client:
            
            # Fetch all pages
            fetched = []
            cursor = None
            page_count = 0
            
            while True:
                result = await client.list_resources(cursor=cursor)
                fetched.extend(result.resources)
                page_count += 1
                
                if result.nextCursor is None:
                    break
                cursor = result.nextCursor
            
            # Verify results
            assert len(fetched) == 250
            assert page_count == 3  # 100, 100, 50
            
            # Verify order preserved
            for i, resource in enumerate(fetched):
                assert resource.uri == f"test://{i}"
```

</div>

---

## 🎯 Quick Reference Card

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 30px; border-radius: 15px; margin: 30px 0;">

### Server Checklist

- ✅ Declare no special capabilities (pagination built-in)
- ✅ Return `nextCursor` when more pages exist
- ✅ Omit `nextCursor` on last page
- ✅ Make cursors opaque (base64-encoded)
- ✅ Validate cursor format
- ✅ Handle invalid cursors with -32602 error
- ✅ Use consistent page sizes (server-controlled)
- ✅ Index database columns for pagination queries
- ✅ Consider keyset pagination for large datasets

### Client Checklist

- ✅ Start with `cursor=None` for first page
- ✅ Check `nextCursor` field for more pages
- ✅ Treat cursors as opaque strings
- ✅ Never parse or modify cursors
- ✅ Don't persist cursors across sessions
- ✅ Handle pagination errors gracefully
- ✅ Show progress to users
- ✅ Allow cancellation of pagination

### Cursor Design Checklist

- ✅ Use base64 encoding
- ✅ Include version number
- ✅ Store position information
- ✅ Consider expiration timestamp
- ✅ Keep cursors short
- ✅ Make format evolvable

</div>

---

## 🚀 Complete Working Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Server Implementation (server.py)

```python
import base64
import json
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, ListResourcesResult

mcp = FastMCP("Paginated Document Server")

# Generate 150 dummy resources
ALL_RESOURCES = [
    Resource(
        uri=f"file:///documents/doc_{i:03d}.txt",
        name=f"Document {i}",
        description=f"This is document number {i}",
        mimeType="text/plain"
    )
    for i in range(1, 151)
]

PAGE_SIZE = 20

def create_cursor(offset: int) -> str:
    """Create opaque cursor from offset"""
    cursor_data = {"v": 1, "offset": offset}
    return base64.b64encode(
        json.dumps(cursor_data).encode()
    ).decode()

def parse_cursor(cursor: str) -> int:
    """Parse cursor to extract offset"""
    try:
        cursor_data = json.loads(
            base64.b64decode(cursor.encode()).decode()
        )
        if cursor_data.get("v") != 1:
            raise ValueError("Invalid cursor version")
        return cursor_data["offset"]
    except Exception as e:
        raise ValueError(f"Invalid cursor: {e}")

@mcp.list_resources()
async def list_resources(cursor: str | None = None) -> ListResourcesResult:
    """Handle paginated resource listing"""
    
    # Determine starting position
    offset = 0 if cursor is None else parse_cursor(cursor)
    
    # Validate offset
    if offset < 0 or offset >= len(ALL_RESOURCES):
        if offset >= len(ALL_RESOURCES):
            # Past the end - return empty page
            return ListResourcesResult(resources=[])
        raise ValueError("Invalid offset in cursor")
    
    # Get current page
    page_end = min(offset + PAGE_SIZE, len(ALL_RESOURCES))
    page_resources = ALL_RESOURCES[offset:page_end]
    
    # Calculate next cursor
    next_cursor = None
    if page_end < len(ALL_RESOURCES):
        next_cursor = create_cursor(page_end)
    
    print(f"Page: offset={offset}, returned={len(page_resources)}, "
          f"hasMore={next_cursor is not None}")
    
    return ListResourcesResult(
        resources=page_resources,
        nextCursor=next_cursor
    )

if __name__ == "__main__":
    mcp.run()
```

### Client Implementation (client.py)

```python
import asyncio
from mcp.client import Client, StdioServerParameters

async def main():
    """Fetch all resources with pagination"""
    
    async with Client(
        StdioServerParameters(
            command="python",
            args=["server.py"]
        )
    ) as client:
        
        print("🚀 Starting pagination demo\n")
        
        all_resources = []
        cursor = None
        page_num = 1
        
        while True:
            print(f"📄 Fetching page {page_num}...")
            
            # Request page
            result = await client.list_resources(cursor=cursor)
            
            # Collect resources
            page_count = len(result.resources)
            all_resources.extend(result.resources)
            
            print(f"   ✓ Received {page_count} resources")
            print(f"   ✓ Total so far: {len(all_resources)}")
            
            # Check if more pages exist
            if result.nextCursor is None:
                print(f"\n✅ Pagination complete!")
                print(f"   Total resources: {len(all_resources)}")
                break
            
            # Continue to next page
            cursor = result.nextCursor
            page_num += 1
            print(f"   ⏭️  Next cursor: {cursor[:20]}...\n")
        
        # Display summary
        print(f"\n📊 Summary:")
        print(f"   Total pages: {page_num}")
        print(f"   Total resources: {len(all_resources)}")
        print(f"   First resource: {all_resources[0].name}")
        print(f"   Last resource: {all_resources[-1].name}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected Output

```
🚀 Starting pagination demo

📄 Fetching page 1...
   ✓ Received 20 resources
   ✓ Total so far: 20
   ⏭️  Next cursor: eyJ2IjogMSwgIm9mZnNldCI6IDIwfQ==...

📄 Fetching page 2...
   ✓ Received 20 resources
   ✓ Total so far: 40
   ⏭️  Next cursor: eyJ2IjogMSwgIm9mZnNldCI6IDQwfQ==...

... (continues for 8 pages total) ...

📄 Fetching page 8...
   ✓ Received 10 resources
   ✓ Total so far: 150

✅ Pagination complete!
   Total resources: 150

📊 Summary:
   Total pages: 8
   Total resources: 150
   First resource: Document 1
   Last resource: Document 150
```

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Think of Pagination as Reading a Book

**Without Pagination:**  
Try to read entire 1000-page book in one sitting—overwhelming, exhausting, impossible

**↓**

**With Pagination:**  
Read one chapter at a time, use bookmark to remember position

**↓**

**Cursor = Bookmark:**  
Opaque token that marks your position in the story

**↓**

**nextCursor = "Turn the Page":**  
When present: more chapters to read  
When absent: you've finished the book

**↓**

**Result:**  
Manageable reading experience, you can pause/resume anytime, never lose your place

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"MCP pagination uses opaque cursor tokens to break large result sets into server-controlled pages, enabling efficient, reliable data transfer where clients fetch pages sequentially until nextCursor is absent, signaling completion."*

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now master MCP pagination from basic concepts to advanced implementation patterns.**  
Build scalable servers that handle massive datasets effortlessly! 📚✨

</div>
