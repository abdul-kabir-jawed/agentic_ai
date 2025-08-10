# MCP - Model Context Protocol

![MCP Logo](https://github.com/modelcontextprotocol/specification/raw/main/docs/mcp-logo.png)

The **Model Context Protocol (MCP)** is an open standard that enables AI assistants to securely connect to external data sources and tools. MCP provides a universal way for AI models to interact with various services, databases, and APIs while maintaining security and standardization.

## 🎯 What is MCP?

MCP is a protocol designed to solve the challenge of connecting AI models to external resources in a secure, standardized way. Instead of each AI application needing custom integrations for every service, MCP provides:

- **Standardized communication** between AI models and external resources
- **Secure access control** and authentication mechanisms  
- **Extensible architecture** for adding new integrations
- **Consistent API** across different data sources and tools

## 🏗️ Architecture Overview

MCP follows a client-server architecture:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   AI Model  │◄──►│ MCP Client  │◄──►│ MCP Server  │
│  (Claude,   │    │             │    │             │
│   GPT, etc) │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ External Service│
                                    │ (Database, API, │
                                    │  File System)   │
                                    └─────────────────┘
```

### Components

- **MCP Client** - Integrated into AI applications, handles protocol communication
- **MCP Server** - Provides access to specific external resources or tools
- **Transport Layer** - Handles secure communication (HTTP, WebSocket, etc.)

## ✨ Key Features

### 🔒 Security First
- **Authentication & Authorization** - Secure access control mechanisms
- **Sandboxed Execution** - Isolated execution environments
- **Permission Management** - Granular control over resource access
- **Audit Logging** - Track all interactions for compliance

### 🔌 Extensible Design
- **Plugin Architecture** - Easy to add new integrations
- **Custom Tools** - Create domain-specific tools and functions
- **Protocol Extensions** - Extend functionality while maintaining compatibility
- **Language Agnostic** - Implementations available in multiple languages

### 📊 Resource Types
- **Data Sources** - Databases, APIs, file systems
- **Tools & Functions** - Custom business logic and operations
- **Knowledge Bases** - Documentation, FAQs, and reference materials
- **Real-time Services** - Streaming data and live information

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (for Python implementations)
- Node.js 16+ (for JavaScript implementations)
- Access to external resources you want to connect

### Installation

#### Python
```bash
# Install the MCP Python SDK
pip install mcp

# Or install from source
git clone https://github.com/modelcontextprotocol/python-sdk.git
cd python-sdk
pip install -e .
```

#### JavaScript/TypeScript
```bash
# Install the MCP JavaScript SDK
npm install @modelcontextprotocol/sdk

# Or with yarn
yarn add @modelcontextprotocol/sdk
```

### Basic Server Example

#### Python Server
```python
#!/usr/bin/env python3
import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent

# Create server instance
server = Server("example-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get weather information for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        location = arguments.get("location")
        # Your weather API logic here
        return [TextContent(
            type="text",
            text=f"Weather in {location}: Sunny, 22°C"
        )]

async def main():
    # Run the server
    async with server:
        await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

#### JavaScript Server
```javascript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  {
    name: 'example-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'get_weather',
        description: 'Get weather information for a location',
        inputSchema: {
          type: 'object',
          properties: {
            location: {
              type: 'string',
              description: 'City name',
            },
          },
          required: ['location'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_weather') {
    const location = request.params.arguments.location;
    return {
      content: [
        {
          type: 'text',
          text: `Weather in ${location}: Sunny, 22°C`,
        },
      ],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Client Configuration

Add your MCP server to your AI client configuration:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "python",
      "args": ["weather-server.py"],
      "env": {
        "API_KEY": "your-weather-api-key"
      }
    }
  }
}
```

## 🛠️ Common Use Cases

### Database Integration
```python
@server.list_tools()
async def database_tools():
    return [
        Tool(
            name="query_database",
            description="Execute SQL queries on the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "params": {"type": "array"}
                }
            }
        )
    ]
```

### File System Access
```python
@server.list_tools()
async def file_tools():
    return [
        Tool(
            name="read_file",
            description="Read contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                }
            }
        )
    ]
```

### API Integration
```python
@server.list_tools()
async def api_tools():
    return [
        Tool(
            name="call_api",
            description="Make HTTP requests to external APIs",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "method": {"type": "string"},
                    "headers": {"type": "object"},
                    "body": {"type": "object"}
                }
            }
        )
    ]
```

## 🔧 Advanced Features

### Resource Discovery
```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///path/to/document.txt",
            name="Important Document",
            description="Key business document",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    # Return resource content
    pass
```

### Streaming Support
```python
@server.call_tool()
async def streaming_tool(name: str, arguments: dict):
    async def generate_stream():
        for i in range(10):
            yield TextContent(
                type="text",
                text=f"Stream chunk {i}"
            )
            await asyncio.sleep(1)
    
    return generate_stream()
```

### Error Handling
```python
from mcp.types import McpError

@server.call_tool()
async def safe_tool_call(name: str, arguments: dict):
    try:
        # Tool logic here
        pass
    except ValueError as e:
        raise McpError(
            code="INVALID_PARAMS",
            message=f"Invalid parameters: {e}"
        )
```

## 📋 Available MCP Servers

### Official Servers
- **File System** - Access local files and directories
- **Git** - Git repository operations
- **SQLite** - SQLite database queries
- **HTTP** - Generic HTTP API client
- **Memory** - Persistent memory for conversations

### Community Servers
- **PostgreSQL** - PostgreSQL database integration
- **MongoDB** - MongoDB operations  
- **Redis** - Redis cache operations
- **Docker** - Container management
- **Kubernetes** - K8s cluster operations
- **AWS** - AWS service integrations
- **Google Cloud** - GCP service integrations

## 🔒 Security Best Practices

### Authentication
```python
# Server-side authentication
@server.initialize()
async def initialize(options: InitializationOptions):
    # Validate API keys, tokens, etc.
    if not validate_credentials(options.client_info):
        raise McpError("UNAUTHORIZED", "Invalid credentials")
```

### Input Validation
```python
@server.call_tool()
async def secure_tool(name: str, arguments: dict):
    # Validate and sanitize inputs
    validated_args = validate_input_schema(arguments)
    # Execute with validated data
    return execute_safely(validated_args)
```

### Resource Access Control
```python
def check_permissions(resource_uri: str, client_info: dict):
    # Implement your authorization logic
    allowed_paths = get_allowed_paths(client_info.get('user_id'))
    if not any(resource_uri.startswith(path) for path in allowed_paths):
        raise McpError("FORBIDDEN", "Access denied")
```

## 🧪 Testing

### Unit Testing
```python
import pytest
from mcp.server.models import CallToolRequest

@pytest.mark.asyncio
async def test_weather_tool():
    request = CallToolRequest(
        name="get_weather",
        arguments={"location": "New York"}
    )
    result = await call_tool(request.name, request.arguments)
    assert "New York" in result[0].text
```

### Integration Testing
```bash
# Test server startup
mcp-test-server --server ./my-server.py

# Test tool functionality
mcp-test-tool --server ./my-server.py --tool get_weather --args '{"location": "London"}'
```

## 📚 Resources & Documentation

### Official Documentation
- **Specification** - [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- **Python SDK** - [Python Implementation Guide](https://python-sdk.modelcontextprotocol.io/)
- **JavaScript SDK** - [TypeScript/JavaScript Guide](https://js-sdk.modelcontextprotocol.io/)

### Community Resources
- **GitHub Organization** - [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- **Examples Repository** - Sample implementations and tutorials
- **Discord Community** - Real-time community support
- **Stack Overflow** - Tag: `model-context-protocol`

### Tutorials & Guides
- **Getting Started Tutorial** - Step-by-step implementation guide
- **Security Best Practices** - Comprehensive security guidelines
- **Performance Optimization** - Tips for high-performance servers
- **Deployment Guide** - Production deployment strategies

## 🤝 Contributing

MCP is an open standard and welcomes contributions:

1. **Protocol Development** - Contribute to the specification
2. **SDK Improvements** - Enhance existing SDKs
3. **Server Implementations** - Create new MCP servers
4. **Documentation** - Improve guides and examples
5. **Testing** - Add test coverage and scenarios

### Development Setup
```bash
# Clone the repository
git clone https://github.com/modelcontextprotocol/python-sdk.git
cd python-sdk

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

## 📄 License

MCP is available under the MIT License, promoting open adoption and contribution.

---

**Ready to connect your AI to the world?** Start building with MCP today and unlock the full potential of context-aware AI applications!
