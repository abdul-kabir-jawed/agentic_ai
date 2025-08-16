# Agents SDK: Complete Guide to LLM Provider Configuration

## Overview

The Agents SDK provides a flexible hierarchy for configuring Large Language Model (LLM) providers across your application. While the SDK defaults to OpenAI, it supports multiple providers including Google's Gemini, Anthropic's Claude, and any OpenAI-compatible API endpoints.

The configuration system follows a three-tier hierarchy that allows for maximum flexibility and control:

```
Agent Level (Highest Priority) → Run Level (Medium Priority) → Global Level (Lowest Priority)
```

This hierarchical approach ensures that more specific configurations override general ones, giving you granular control over which models your agents use.

---

## Configuration Hierarchy Explained

### Priority System
- **Agent Level**: Highest priority - overrides all other configurations
- **Run Level**: Medium priority - overrides global settings but not agent-specific ones  
- **Global Level**: Lowest priority - provides default fallback configuration

### When to Use Each Level

| Level | Best Use Cases | Benefits |
|-------|---------------|----------|
| **Agent** | Specialized agents requiring specific models | Maximum flexibility, model optimization per use case |
| **Run** | Temporary model switching, testing scenarios | Easy experimentation without changing global settings |
| **Global** | Standard application-wide model preferences | Simplified configuration, consistent behavior |

---

## 1. Agent-Level Configuration

Agent-level configuration provides the most granular control, allowing each agent to use the optimal model for its specific tasks.

### Key Features
- **Override Priority**: Supersedes both run and global configurations
- **Model Specialization**: Different agents can use different models optimized for their tasks
- **Independent Configuration**: Each agent maintains its own model settings
- **Custom Client Support**: Full control over API clients and parameters

### Implementation Example

```python
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# Configuration for Google Gemini via OpenAI-compatible API
gemini_api_key = "your_gemini_api_key_here"

# Create a custom client for Gemini
# Reference: https://ai.google.dev/gemini-api/docs/openai
gemini_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Disable tracing for cleaner output (optional)
set_tracing_disabled(disabled=True)

async def main():
    # Create an agent with specific model configuration
    haiku_agent = Agent(
        name="HaikuPoet",
        instructions="You are a creative assistant who responds only in traditional haiku format (5-7-5 syllable pattern).",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash", 
            openai_client=gemini_client
        ),
    )
    
    # Run the agent with its configured model
    result = await Runner.run(
        haiku_agent,
        "Explain the concept of recursion in computer programming.",
    )
    
    print("Agent Response:")
    print(result.final_output)
    print(f"\nModel Used: {haiku_agent.model}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Agent Configuration

```python
# Multiple agents with different models
async def multi_agent_example():
    # Agent 1: Gemini for creative tasks
    creative_agent = Agent(
        name="CreativeWriter",
        instructions="You are a creative writing assistant.",
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=gemini_client
        )
    )
    
    # Agent 2: OpenAI GPT-4 for analytical tasks
    analytical_agent = Agent(
        name="DataAnalyst", 
        instructions="You are a data analysis expert.",
        model=OpenAIChatCompletionsModel(model="gpt-4")
    )
    
    # Each agent uses its configured model automatically
    creative_result = await Runner.run(creative_agent, "Write a short story about AI")
    analytical_result = await Runner.run(analytical_agent, "Analyze this dataset trend")
```

---

## 2. Run-Level Configuration

Run-level configuration allows you to specify models for individual execution contexts without modifying agent definitions. This is ideal for experimentation and temporary model switching.

### Key Features
- **Execution Context**: Applies to specific run instances
- **Override Capability**: Overrides global settings while respecting agent-level configs
- **Flexible Testing**: Easy A/B testing between different models
- **Shared Configuration**: Multiple agents in the same run can share the same model config

### Implementation Example

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# External provider setup
gemini_api_key = "your_gemini_api_key_here"

# Configure external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Create model configuration
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure run-specific settings
run_configuration = RunConfig(
    model=gemini_model,
    model_provider=external_client,
    tracing_disabled=True,
    # Additional run-specific configurations can be added here
)

# Create agent without model specification
generic_agent = Agent(
    name="AssistantBot", 
    instructions="You are a helpful and knowledgeable assistant."
)

# Execute with run-level configuration
def demonstrate_run_config():
    result = Runner.run_sync(
        agent=generic_agent, 
        message="Explain quantum computing in simple terms.",
        run_config=run_configuration
    )
    
    print("Run-Level Configuration Result:")
    print(result.final_output)
    print(f"\nConfiguration Applied: {run_configuration.model}")

demonstrate_run_config()
```

### Advanced Run Configuration

```python
# Multiple run configurations for comparison
def compare_models():
    # Configuration for Gemini
    gemini_config = RunConfig(
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash", 
            openai_client=external_client
        ),
        tracing_disabled=True
    )
    
    # Configuration for GPT-4
    gpt4_config = RunConfig(
        model=OpenAIChatCompletionsModel(model="gpt-4"),
        tracing_disabled=True
    )
    
    agent = Agent(
        name="TestAgent",
        instructions="Provide concise, accurate responses."
    )
    
    query = "What are the benefits of renewable energy?"
    
    # Test with Gemini
    gemini_result = Runner.run_sync(agent, query, run_config=gemini_config)
    
    # Test with GPT-4
    gpt4_result = Runner.run_sync(agent, query, run_config=gpt4_config)
    
    print("Gemini Response:", gemini_result.final_output)
    print("\nGPT-4 Response:", gpt4_result.final_output)
```

---

## 3. Global-Level Configuration

Global configuration sets application-wide defaults that apply to all agents and runs unless explicitly overridden. This approach simplifies configuration management for consistent model usage.

### Key Features
- **Application Default**: Sets the baseline model for all operations
- **Simplified Management**: Single configuration point for the entire application
- **Fallback Behavior**: Provides defaults when no specific configuration is set
- **Easy Migration**: Allows quick switching of default providers

### Implementation Example

```python
from agents import (
    Agent, Runner, AsyncOpenAI, 
    set_default_openai_client, set_tracing_disabled, 
    set_default_openai_api
)

# Global configuration setup
gemini_api_key = "your_gemini_api_key_here"

# Configure global settings
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

# Create and set global client
global_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(global_client)

# Create agent using global configuration
def demonstrate_global_config():
    # Agent will automatically use global settings
    assistant_agent = Agent(
        name="GlobalAssistant", 
        instructions="You are a helpful assistant using the globally configured model.",
        model="gemini-2.0-flash"  # Model name only - client comes from global config
    )
    
    # Execute using global configuration
    result = Runner.run_sync(
        agent=assistant_agent, 
        message="Hello! Tell me about the benefits of using global configuration."
    )
    
    print("Global Configuration Result:")
    print(result.final_output)

demonstrate_global_config()
```

### Advanced Global Configuration

```python
# Environment-based global configuration
import os

def setup_environment_based_config():
    # Check environment for provider preference
    provider = os.getenv('LLM_PROVIDER', 'openai')
    
    if provider == 'gemini':
        client = AsyncOpenAI(
            api_key=os.getenv('GEMINI_API_KEY'),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        default_model = "gemini-2.0-flash"
    elif provider == 'anthropic':
        client = AsyncOpenAI(
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            base_url="https://api.anthropic.com/v1/openai/",
        )
        default_model = "claude-3-sonnet-20240229"
    else:
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        default_model = "gpt-4"
    
    # Apply global configuration
    set_default_openai_client(client)
    
    return default_model

# Use in application startup
default_model = setup_environment_based_config()
```

## Debugging and Development Tools

### Enable Verbose Logging

For development and debugging purposes, the SDK provides detailed logging capabilities:

```python
from agents import enable_verbose_stdout_logging

# Enable detailed logging
enable_verbose_stdout_logging()

# Now all agent operations will show detailed logs
def debug_agent_execution():
    agent = Agent(
        name="DebugAgent",
        instructions="You are a test agent for debugging."
    )
    
    # Detailed logs will show:
    # - Model selection process
    # - API calls and responses
    # - Configuration resolution
    # - Execution steps
    result = Runner.run_sync(agent, "Test debugging output")
    
    print("Result:", result.final_output)
```
---

## Best Practices and Recommendations

### Model Selection Guidelines

1. **Agent-Level Configuration**: Use for specialized agents requiring specific model capabilities
   - Creative tasks → Gemini 2.0 Flash
   - Code generation → GPT-4 or Claude
   - Analysis → GPT-4 Turbo

2. **Run-Level Configuration**: Use for experimentation and testing
   - A/B testing different models
   - Temporary provider switching
   - Cost optimization experiments

3. **Global Configuration**: Use for standardized applications
   - Consistent model across all agents
   - Simplified configuration management
   - Production environments with standard requirements


---

## Conclusion

The Agents SDK's three-tier configuration system provides maximum flexibility for LLM provider management. Choose the appropriate level based on your specific needs:

- **Start with Global** for simple, consistent applications
- **Add Run-Level** for experimentation and testing
- **Use Agent-Level** for specialized, optimized implementations

This hierarchical approach ensures your agents can leverage the best model for each task while maintaining clean, maintainable code architecture.
