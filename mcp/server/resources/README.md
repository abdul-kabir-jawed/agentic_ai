# Model Context Protocol (MCP) Resources - Complete Guide

## 🎯 What Are MCP Resources?

Resources in MCP provide **structured, read-only access** to information that AI applications can retrieve and use as context. Think of them as smart data endpoints that AI models can discover, explore, and consume seamlessly.

### 🔗 Analogy: Resources vs. Familiar Concepts

| **If you're familiar with...** | **MCP Resources are like...** | **Key advantage** |
|-------------------------------|--------------------------------|-------------------|
| **File Systems** | Files the AI can browse and read | Discoverable and structured for AI |
| **REST API GET endpoints** | Read-only API endpoints | Built-in metadata and categorization |
| **RAG (Retrieval Augmented Generation)** | Knowledge base for AI context | Standardized across all AI platforms |
| **Documentation Sites** | Docs the AI can navigate | Self-describing with rich metadata |
| **Database Views** | Queryable data collections | AI-friendly formatting and discovery |

---

## 🏗️ Core Architecture

### Resource Flow
```
AI Application → MCP Client → MCP Server → Data Source
     ↑                                          ↓
   Context ← Resource Content ← Processing ← Raw Data
```

### Key Characteristics
- **📖 Read-only**: Resources provide data, not actions
- **🔗 URI-based**: Accessed through specific URIs with optional parameters
- **📋 MIME-typed**: Support various content types (JSON, text, images, etc.)
- **🎮 App-controlled**: The application decides when to expose resources
- **⚡ Static or templated**: Can be direct resources or parameterized

---

## 🆔 Resource URIs

Resources are identified using URIs that follow this format:
```
[protocol]://[host]/[path]
```

### Examples:
- `file:///home/user/documents/report.pdf`
- `postgres://database/customers/schema`
- `screen://localhost/display1`
- `docs://documents` (custom protocol)
- `weather://forecast/{city}/{date}` (templated)

---

## 📊 Content Types

### 1. Text Resources 📝
- **Content**: UTF-8 encoded text data
- **Use cases**: Source code, configuration files, JSON/XML data, documentation
- **MIME types**: `text/plain`, `application/json`, `text/markdown`, etc.

### 2. Binary Resources 🗂️
- **Content**: Raw binary data encoded in base64
- **Use cases**: Images, PDFs, audio files, video files
- **MIME types**: `application/pdf`, `image/png`, `audio/mp3`, etc.

---

## 🔧 Types of Resources

### 1. Direct Resources (Static)
Fixed URIs that never change - perfect for operations that don't need parameters.

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    """Returns all available document IDs"""
    return list(docs.keys())
```

**Characteristics:**
- ✅ Static URI
- ✅ No parameters
- ✅ Immediate access
- ✅ Simple implementation

### 2. Templated Resources (Dynamic)
Include parameters in their URIs for flexible, dynamic queries.

```python
@mcp.resource(
    "docs://{doc_id}",
    mime_type="text/plain"
)
def get_doc(doc_id: str) -> str:
    """Returns content of a specific document"""
    return docs[doc_id]
```

**Characteristics:**
- ✅ Parameterized URI
- ✅ Dynamic content
- ✅ Parameter completion support
- ✅ Flexible queries

---

## 📨 Protocol Messages

### 1. Listing Resources

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resources": [
      {
        "uri": "file:///project/src/main.rs",
        "name": "main.rs",
        "title": "Rust Software Application Main File",
        "description": "Primary application entry point",
        "mimeType": "text/x-rust"
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### 2. Reading Resources

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///project/src/main.rs"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "contents": [
      {
        "uri": "file:///project/src/main.rs",
        "name": "main.rs",
        "title": "Rust Software Application Main File",
        "mimeType": "text/x-rust",
        "text": "fn main() {\n    println!(\"Hello world!\");\n}"
      }
    ]
  }
}
```

### 3. Resource Templates

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/templates/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "resourceTemplates": [
      {
        "uriTemplate": "weather://forecast/{city}/{date}",
        "name": "weather-forecast",
        "title": "Weather Forecast",
        "description": "Get weather forecast for any city and date",
        "mimeType": "application/json"
      }
    ]
  }
}
```

---

## 🛠️ Implementation Details

### Server-Side Resource Management

#### Resource Registration Decorator
```python
def resource(
    self,
    uri: str,
    *,
    name: str | None = None,
    title: str | None = None,
    description: str | None = None,
    mime_type: str | None = None,
) -> Callable[[AnyFunction], AnyFunction]:
```

**Parameters Explained:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `uri` | `str` | ✅ | Resource URI (e.g., `"docs://documents"` or `"docs://{doc_id}"`) |
| `name` | `str \| None` | ❌ | Short identifier for the resource |
| `title` | `str \| None` | ❌ | Human-readable title |
| `description` | `str \| None` | ❌ | Detailed description of what the resource provides |
| `mime_type` | `str \| None` | ❌ | MIME type hint for content (e.g., `"application/json"`) |

#### Resource Listing
```python
async def list_resources(self) -> list[MCPResource]:
    """List all available resources."""
    resources = self._resource_manager.list_resources()
    return [
        MCPResource(
            uri=resource.uri,
            name=resource.name or "",
            title=resource.title,
            description=resource.description,
            mimeType=resource.mime_type,
        )
        for resource in resources
    ]
```

#### Resource Reading
```python
async def read_resource(self, uri: AnyUrl | str) -> Iterable[ReadResourceContents]:
    """Read a resource by URI."""
    resource = await self._resource_manager.get_resource(uri)
    if not resource:
        raise ResourceError(f"Unknown resource: {uri}")
    
    try:
        content = await resource.read()
        return [ReadResourceContents(content=content, mime_type=resource.mime_type)]
    except Exception as e:
        logger.exception(f"Error reading resource {uri}")
        raise ResourceError(str(e))
```

### Client-Side Resource Access

```python
async def read_resource(self, uri: str) -> Any:
    """Read a resource and parse based on MIME type."""
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    
    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)
    
    return resource.text
```

---

## 🎯 Parameter Completion

Dynamic resources support intelligent parameter completion:

### Examples:
- Typing `"Par"` for `weather://forecast/{city}` → suggests `"Paris"` or `"Park City"`
- Typing `"JFK"` for `flights://search/{airport}` → suggests `"JFK - John F. Kennedy International"`

### Implementation:
```python
@mcp.resource("weather://forecast/{city}/{date}")
def get_weather_forecast(city: str, date: str) -> dict:
    """Get weather forecast with auto-completed parameters."""
    return {
        "city": city,
        "date": date,
        "forecast": fetch_weather_data(city, date)
    }
```

---

## 🎨 User Interaction Patterns

Applications can implement resource discovery through various UI patterns:

### 🌳 Tree/List Views
- Familiar folder-like structures
- Hierarchical browsing
- Nested resource organization

### 🔍 Search & Filter
- Finding specific resources
- Keyword-based discovery
- Category filtering

### 🤖 Smart Suggestions
- AI-powered resource selection
- Context-aware recommendations
- Automatic inclusion based on conversation

### 📋 Manual Selection
- Bulk resource selection
- Preview capabilities
- Integration with existing file browsers

---

## 💡 Best Practices

### 1. URI Design
- Use descriptive protocols: `docs://`, `api://`, `database://`
- Keep paths logical and hierarchical
- Include version information when needed: `api://v2/users/{id}`

### 2. MIME Type Selection
- Be specific: `application/json` vs `text/plain`
- Use standard types when possible
- Provide content type hints for binary data

### 3. Metadata Quality
- Write clear, descriptive titles
- Provide helpful descriptions
- Use consistent naming conventions

### 4. Parameter Validation
- Validate URI parameters match function parameters
- Handle missing or invalid parameters gracefully
- Provide meaningful error messages

### 5. Performance Considerations
- Cache frequently accessed resources
- Implement pagination for large datasets
- Use lazy loading for heavy resources

---

## 🔧 Practical Examples

### Document Management System
```python
# List all documents
@mcp.resource(
    "docs://list",
    name="document-list",
    title="All Documents",
    description="List of all available documents",
    mime_type="application/json"
)
def list_documents() -> list[dict]:
    return [
        {"id": doc_id, "title": doc["title"], "type": doc["type"]}
        for doc_id, doc in documents.items()
    ]

# Get specific document
@mcp.resource(
    "docs://document/{doc_id}",
    name="document-content",
    title="Document Content",
    description="Full content of a specific document",
    mime_type="text/markdown"
)
def get_document(doc_id: str) -> str:
    if doc_id not in documents:
        raise ValueError(f"Document {doc_id} not found")
    return documents[doc_id]["content"]
```

### Database Integration
```python
@mcp.resource(
    "db://users/{user_id}/profile",
    name="user-profile",
    title="User Profile",
    description="Complete user profile information",
    mime_type="application/json"
)
async def get_user_profile(user_id: str) -> dict:
    async with database.connection() as conn:
        user = await conn.fetch_user(user_id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "preferences": user.preferences
        }
```

---

## 🚀 Advanced Features

### Resource Subscriptions
Monitor resource changes in real-time:
```python
# Subscribe to resource changes
{
  "jsonrpc": "2.0",
  "method": "resources/subscribe",
  "params": {
    "uri": "docs://live-feed"
  }
}
```

### Binary Resource Handling
```python
@mcp.resource(
    "files://image/{image_id}",
    mime_type="image/png"
)
def get_image(image_id: str) -> bytes:
    """Return binary image data."""
    with open(f"images/{image_id}.png", "rb") as f:
        return f.read()
```

### Error Handling
```python
@mcp.resource("docs://secure/{doc_id}")
def get_secure_document(doc_id: str) -> str:
    if not user_has_permission(doc_id):
        raise ResourceError("Access denied")
    
    try:
        return load_document(doc_id)
    except FileNotFoundError:
        raise ResourceError(f"Document {doc_id} not found")
```

---

## 📈 Testing & Debugging

### 1. MCP Inspector
- Verify server resources are correctly implemented
- Test resource discovery and reading
- Debug URI template parameters

### 2. Direct API Testing
- Use tools like Postman for endpoint verification
- Test both direct and templated resources
- Validate MIME type handling

### 3. Client Integration Testing
- Test autocomplete functionality with "@" prefix
- Verify resource content inclusion in prompts
- Check error handling and fallbacks

---

## 🔗 Resources & References

- [MCP Resource Specification](https://modelcontextprotocol.io/specification/2025-06-18#resources)
- [MIME Types Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- [URI Design Best Practices](https://tools.ietf.org/html/rfc3986)

---

## 📝 Summary

MCP Resources provide a powerful, standardized way to expose data to AI applications. They offer:

- **🎯 Discoverability**: AI can find and explore available data
- **📋 Metadata**: Rich descriptions and type information
- **⚡ Flexibility**: Both static and dynamic resource patterns
- **🔧 Simplicity**: Easy implementation with decorators
- **🎨 UI Integration**: Support for various interaction patterns

By leveraging MCP Resources, you can create AI applications that seamlessly access and utilize structured information, making your AI interactions more contextual and powerful.
