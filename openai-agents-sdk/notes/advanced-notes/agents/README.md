# OpenAI Agents SDK - Agent Class Complete Reference

## 🧠 What is the Agent Class?

The `Agent` class is the core component of the OpenAI Agents SDK that defines an autonomous AI entity. It wraps together:

- A model (GPT-4, Gemini, etc.)
- Instructions (system prompts)
- Tools for enhanced capabilities
- Guardrails for validation
- Handoffs for delegation to other agents

Think of it as a smart assistant with a brain, toolbox, boundaries, and teammates.

## 🏗️ Constructor Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | **Required** - Unique identifier for the agent |

### Essential Parameters (Strongly Recommended)

| Parameter | Type | Description |
|-----------|------|-------------|
| `instructions` | `str` or `callable` | System prompt defining agent behavior - technically optional but always recommended |
| `model` | `str` or `Model` | Model to use (defaults to GPT-4o if not specified) |

### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `Prompt` or function | Dynamic configuration via Prompt object (alternative to instructions) |
| `handoff_description` | `str` | Human-readable description for LLM handoffs |
| `handoffs` | `list[Agent or Handoff]` | Other agents this agent can delegate to |
| `model_settings` | `ModelSettings` | Temperature, top_p, etc. (auto-filled defaults) |
| `tools` | `list[Tool]` | Function tools for enhanced capabilities |
| `mcp_servers` | `list[MCPServer]` | External servers for Model Context Protocol tools |
| `mcp_config` | `MCPConfig` | Configuration for MCP servers |
| `input_guardrails` | `list[InputGuardrail]` | Validation before agent starts (first agent only) |
| `output_guardrails` | `list[OutputGuardrail]` | Validation after agent completes |
| `output_type` | `type` or `AgentOutputSchema` | Expected output format (str, dict, custom schema) |
| `hooks` | `AgentHooks` | Debugging, logging, or tracing events |
| `tool_use_behavior` | `Literal[...]` or function | Controls how tools are handled |
| `reset_tool_choice` | `bool` | Prevents infinite tool loops (default: True) |

## 🚀 Basic Usage Examples

### Minimal Agent

```python
from agents import Agent

agent = Agent(
    name="StudyBot",
    instructions="Help users understand Python with clear examples.",
    model="gpt-4o"
)
```

### Complete Agent with Tools

```python
from agents import Agent
from my_tools import search_tool, calculator_tool

agent = Agent(
    name="PythonHelper",
    instructions="Write Python functions with explanations and use tools when needed.",
    model="gpt-4o",
    tools=[search_tool, calculator_tool],
    output_type=str,
    tool_use_behavior="run_llm_again"
)
```

## ⚙️ Special Methods

### 1. `clone(**kwargs)`

**Purpose**: Creates a copy of an agent with modified fields

```python
new_agent = agent.clone(
    instructions="Now act like a teacher",
    model="gpt-4o-mini"
)
```

**Returns**: New `Agent` object with updated fields

### 2. `as_tool(tool_name, tool_description, custom_output_extractor=None)`

**Purpose**: Converts the agent into a tool that other agents can use

```python
tool_version = agent.as_tool(
    tool_name="code_writer",
    tool_description="Writes Python code on request"
)

# Use in another agent
assistant = Agent(
    name="DevHelper",
    instructions="Use tools to help with development",
    tools=[tool_version],
    model="gpt-4o"
)
```

**Returns**: `Tool` object usable by other agents

### 3. `get_system_prompt(run_context)`

**Purpose**: Returns the actual system prompt string that will be used

```python
system_prompt = await agent.get_system_prompt(run_context)
print(system_prompt)  # "Help users understand Python..."
```

**Returns**: `str` - the system prompt, or `None` if invalid

### 4. `get_prompt(run_context)`

**Purpose**: Converts dynamic prompts into model input format (only used when using `prompt=` instead of `instructions`)

```python
prompt_input = await agent.get_prompt(run_context)
```

**Returns**: `ResponsePromptParam` or `None`

### 5. `get_all_tools(run_context)`

**Purpose**: Returns all enabled tools (function tools + MCP tools) filtered by availability

```python
all_tools = await agent.get_all_tools(run_context)
for tool in all_tools:
    print(tool.name)  # Lists all usable tools
```

**Returns**: `list[Tool]` - all enabled and available tools

## 🔧 Tool Use Behavior Options

Control how the agent handles tool calls:

```python
# Default: Let LLM see tool result and continue
tool_use_behavior = "run_llm_again"

# Stop after first tool call and return tool result
tool_use_behavior = "stop_on_first_tool"

# Stop if specific tools are called
tool_use_behavior = ["search_docs", "get_weather"]

# Custom behavior function
tool_use_behavior = custom_function
```

## ⚠️ Common Errors and Fixes

### 1. Missing Required Name

```python
# ❌ Error
agent = Agent(instructions="Help users")

# ✅ Fix
agent = Agent(name="HelperBot", instructions="Help users")
```

### 2. Invalid Instructions Type

```python
# ❌ Error
agent = Agent(name="Bot", instructions=123)

# ✅ Fix
agent = Agent(name="Bot", instructions="Help with questions")
```

### 3. Missing Model

```python
# ❌ May cause issues
agent = Agent(name="Bot", instructions="Help")

# ✅ Better
agent = Agent(name="Bot", instructions="Help", model="gpt-4o")
```

### 4. Invalid Tools

```python
# ❌ Error
agent = Agent(name="Bot", tools=["invalid_tool"])

# ✅ Fix
from agents.tools import tool

@tool
def my_tool(query: str) -> str:
    return f"Result for {query}"

agent = Agent(name="Bot", tools=[my_tool])
```

### 5. Tool Output Not Used

```python
# ❌ Tool runs but result ignored
agent = Agent(name="Bot", tools=[my_tool])

# ✅ Use tool result as final output
agent = Agent(
    name="Bot", 
    tools=[my_tool],
    tool_use_behavior="stop_on_first_tool"
)
```

## 📝 Best Practices

1. **Always provide a descriptive `name`** - helps with debugging and logging
2. **Include clear `instructions`** - defines the agent's behavior and purpose
3. **Explicitly set the `model`** - don't rely on defaults for production
4. **Use `output_type`** when you need structured output
5. **Add `tools` gradually** - start simple, then enhance capabilities
6. **Test with `clone()`** - useful for A/B testing different configurations
7. **Use appropriate `tool_use_behavior`** based on your workflow needs
8. **Add `guardrails`** for production applications with validation requirements

## 🔗 Integration Points

- Use with `Runner.run()` to execute the agent
- Combine with other agents via `handoffs`
- Convert to tools with `as_tool()` for hierarchical workflows
- Extend with custom tools and MCP servers
- Monitor with `hooks` for debugging and analytics
