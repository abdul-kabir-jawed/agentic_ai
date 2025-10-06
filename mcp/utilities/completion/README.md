# 📝 MCP Completions Mastery Guide

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is MCP Completion?

**Completion** is MCP's intelligent autocomplete system that provides context-aware suggestions for prompt arguments and resource template parameters. Think of it as **IDE-style autocomplete for AI agents**—making parameter entry intuitive, accurate, and delightful.

> **Think of it like this:** When you type in Google Search, it suggests completions. When you start typing a filename in VS Code, it shows matching files. MCP completions bring this same intelligent assistance to AI agent interactions.

</div>

---

## 🤔 The Problem Completions Solve

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Scenario: Code Review Tool

**User asks:** *"Review my code"*

**Without Completions:**
```
❌ System: "Enter programming language"
❌ User: "What languages do you support?"
❌ System: [No help provided]
❌ User tries: "javascript"
❌ System: "Invalid! Supported: python, typescript, rust, go..."
   (User wastes time guessing)
```

**With Completions:**
```
✅ System: "Enter programming language"
✅ User starts typing: "py"
✅ System shows: ["python", "pytorch", "pyspark"]
✅ User selects: "python" 
✅ System: "Perfect! Now analyzing Python code..."
   (Instant success, zero frustration)
```

**The Magic:** Completions transform guessing into guided discovery—users learn what's possible while entering values naturally.

</div>

---

## 🎯 Core Concept: What Completions Really Are

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🎯 Smart Suggestions
Real-time parameter value suggestions

*Context-aware & filtered*

</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🧠 Context Intelligence
Suggestions adapt to previous choices

*Hierarchical decision trees*

</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🚀 Enhanced UX
IDE-like autocomplete experience

*Discover as you type*

</div>

</div>

---

## 🏗️ Completion Request Structure

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```json
{
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "code_review"
    },
    "argument": {
      "name": "language",
      "value": "py"
    },
    "context": {
      "arguments": {
        "project_type": "web_app"
      }
    }
  }
}
```

### Key Components

**`ref`** - What you're completing for (prompt or resource template)

**`argument`** - Current parameter being typed (name + partial value)

**`context`** - Previously completed arguments that provide context

</div>

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">

### Response Structure

```json
{
  "completion": {
    "values": ["python", "pytorch", "pyspark"],
    "total": 3,
    "hasMore": false
  }
}
```

**`values`** - Array of suggestions (max 100)  
**`total`** - Optional: total number of matches  
**`hasMore`** - Boolean: more results available beyond 100?

</div>

---

## 💡 Perfect Example: GitHub Repository Navigator

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 15px; margin: 20px 0;">

### The Scenario

User navigates GitHub repositories using a resource template.

**Resource Template:**
```
github://repos/{owner}/{repo}/branches/{branch}
```

### Hierarchical Completion Flow

**Step 1: Complete Owner**
```python
# User types: "mod"
Request: {
  "ref": {"type": "ref/resource", "uri": "github://repos/{owner}/*"},
  "argument": {"name": "owner", "value": "mod"}
}

Response: {
  "values": ["modelcontextprotocol", "modular", "modernweb"]
}
```

**Step 2: Complete Repo (Context-Aware)**
```python
# User selected: owner="modelcontextprotocol"
# Now types: "ser"
Request: {
  "ref": {"type": "ref/resource", "uri": "github://repos/{owner}/{repo}/*"},
  "argument": {"name": "repo", "value": "ser"},
  "context": {"arguments": {"owner": "modelcontextprotocol"}}
}

Response: {
  "values": ["servers", "server-templates"]
}
# Only repos from modelcontextprotocol, not other owners!
```

**Step 3: Complete Branch (Context-Aware)**
```python
# User selected: repo="servers"
# Now types: "m"
Request: {
  "argument": {"name": "branch", "value": "m"},
  "context": {
    "arguments": {
      "owner": "modelcontextprotocol",
      "repo": "servers"
    }
  }
}

Response: {
  "values": ["main", "maintenance-branch"]
}
# Only branches from modelcontextprotocol/servers!
```

**The Power:** Each completion builds on previous context—intelligent, not random!

</div>

---

## 🔄 The Completion Workflow

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #667eea;">

### Complete Interactive Flow

```
1. 👤 User invokes prompt/resource needing parameters
        ↓
2. 🖥️ Client shows input field for first parameter
        ↓
3. ⌨️ User starts typing partial value
        ↓
4. 📤 Client sends completion request with partial value
        ↓
5. 🔧 Server analyzes ref type, argument, and context
        ↓
6. 🧠 Server generates filtered, context-aware suggestions
        ↓
7. 📥 Client receives suggestions
        ↓
8. 🎯 Client displays dropdown/popup with suggestions
        ↓
9. ✅ User selects suggestion
        ↓
10. 🔄 Process repeats for next parameter (with context!)
```

</div>

---

## 🎭 Completion Reference Types

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 25px; border-radius: 10px;">

### 📋 Prompt Reference

**Use when:** Completing prompt arguments

```json
{
  "type": "ref/prompt",
  "name": "code_review"
}
```

**Example Prompt:**
```python
@mcp.prompt()
async def code_review(language: str, style: str):
    """Review code with specific style guide"""
    pass
```

**Completes:** `language`, `style` parameters

</div>

<div style="background: #f3e5f5; padding: 25px; border-radius: 10px;">

### 🔗 Resource Reference

**Use when:** Completing resource template parameters

```json
{
  "type": "ref/resource",
  "uri": "file:///{path}"
}
```

**Example Template:**
```python
@mcp.resource("github://repos/{owner}/{repo}")
async def github_repo(owner: str, repo: str):
    """Access GitHub repository"""
    pass
```

**Completes:** `owner`, `repo` parameters

</div>

</div>

---

## 💻 Server Implementation Patterns

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern 1: Static Completions (Beginner)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Code Reviewer")

@mcp.prompt()
async def review_code(language: str, code: str):
    """Review code in specified language"""
    return f"Reviewing {language} code..."

@mcp.completion()
async def handle_completion(ref, argument, context):
    """Provide static language completions"""
    if argument.name == "language":
        languages = ["python", "javascript", "typescript", "rust", "go"]
        return {"values": languages}
    return {"values": []}
```

### Pattern 2: Filtered Completions (Intermediate)

```python
@mcp.completion()
async def handle_completion(ref, argument, context):
    """Filter completions based on user input"""
    if argument.name == "language":
        all_languages = [
            "python", "javascript", "typescript", 
            "rust", "go", "java", "kotlin"
        ]
        typed = argument.value.lower() if argument.value else ""
        
        # Filter by what user typed
        filtered = [
            lang for lang in all_languages 
            if lang.startswith(typed)
        ]
        
        return {
            "values": filtered,
            "total": len(filtered),
            "hasMore": False
        }
    return {"values": []}
```

### Pattern 3: Context-Aware Completions (Advanced)

```python
@mcp.completion()
async def handle_completion(ref, argument, context):
    """Provide context-aware completions"""
    
    # Framework depends on language
    if argument.name == "framework":
        language = context.arguments.get("language") if context else None
        
        frameworks = {
            "python": ["fastapi", "flask", "django", "tornado"],
            "javascript": ["express", "fastify", "koa", "nest"],
            "rust": ["actix-web", "rocket", "warp", "axum"]
        }
        
        available = frameworks.get(language, [])
        typed = argument.value.lower() if argument.value else ""
        
        filtered = [fw for fw in available if fw.startswith(typed)]
        
        return {"values": filtered, "hasMore": False}
    
    return {"values": []}
```

### Pattern 4: Dynamic/API-Based Completions (Expert)

```python
@mcp.completion()
async def handle_completion(ref, argument, context):
    """Fetch completions from external API"""
    
    if argument.name == "repo":
        owner = context.arguments.get("owner") if context else None
        if not owner:
            return {"values": []}
        
        # Fetch from GitHub API
        repos = await fetch_github_repos(owner)
        typed = argument.value.lower() if argument.value else ""
        
        filtered = [
            repo for repo in repos 
            if typed in repo.lower()
        ]
        
        return {
            "values": filtered[:100],  # Max 100
            "total": len(repos),
            "hasMore": len(repos) > 100
        }
    
    return {"values": []}
```

</div>

---

## 💻 Client Implementation

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Basic Client Usage

```python
from mcp.client import Client, StdioServerParameters
from mcp.types import PromptReference, CompletionArgument

# Connect to server
async with Client(
    StdioServerParameters(
        command="python",
        args=["server.py"]
    )
) as client:
    
    # Request completions
    result = await client.complete(
        ref=PromptReference(
            type="ref/prompt",
            name="code_review"
        ),
        argument={
            "name": "language",
            "value": "py"
        }
    )
    
    # Display suggestions
    print("Suggestions:")
    for value in result.completion.values:
        print(f"  - {value}")
```

### Context-Aware Client Usage

```python
# First completion: language
lang_result = await client.complete(
    ref=PromptReference(type="ref/prompt", name="setup_project"),
    argument={"name": "language", "value": "py"}
)
selected_language = lang_result.completion.values[0]  # "python"

# Second completion: framework (with context!)
framework_result = await client.complete(
    ref=PromptReference(type="ref/prompt", name="setup_project"),
    argument={"name": "framework", "value": "fast"},
    context_arguments={"language": selected_language}
)
# Returns ["fastapi"] not ["fastify"] because language="python"!
```

### Implementing Debouncing (Best Practice)

```python
import asyncio

class DebouncedCompleter:
    def __init__(self, client, delay=0.3):
        self.client = client
        self.delay = delay
        self.current_task = None
    
    async def complete(self, ref, argument, context_arguments=None):
        # Cancel previous request if still pending
        if self.current_task:
            self.current_task.cancel()
        
        # Wait before sending request
        await asyncio.sleep(self.delay)
        
        # Send completion request
        return await self.client.complete(
            ref=ref,
            argument=argument,
            context_arguments=context_arguments
        )

# Usage
completer = DebouncedCompleter(client)
result = await completer.complete(
    ref=PromptReference(type="ref/prompt", name="review_code"),
    argument={"name": "language", "value": "py"}
)
```

</div>

---

## 🎯 Completion Levels: Mastery Path

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 20px; border-radius: 10px;">

### Level 1️⃣: Static Lists

**What:** Fixed completion values

**Example:**
```python
if argument.name == "priority":
    return {"values": ["high", "medium", "low"]}
```

**When:** Values never change

</div>

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### Level 2️⃣: Filtered Completions

**What:** Filter based on user input

**Example:**
```python
options = ["python", "javascript", "typescript"]
typed = argument.value or ""
return {"values": [o for o in options if typed in o]}
```

**When:** Large static lists need filtering

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### Level 3️⃣: Context-Aware

**What:** Completions depend on previous choices

**Example:**
```python
language = context.arguments.get("language")
if language == "python":
    return {"values": ["fastapi", "django"]}
```

**When:** Parameters have dependencies

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px;">

### Level 4️⃣: Dynamic/API-Based

**What:** Fetch completions from external sources

**Example:**
```python
owner = context.arguments.get("owner")
repos = await github_api.list_repos(owner)
return {"values": repos}
```

**When:** Values come from databases/APIs

</div>

</div>

---

## 🎓 Real-World Use Cases

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">

### Use Case 1: Multi-Cloud Deployment Tool

**Prompts:** `deploy_app(cloud_provider, region, instance_type)`

**Completion Flow:**
1. **cloud_provider**: ["aws", "azure", "gcp"]
2. **region**: Context-aware based on provider
   - If aws: ["us-east-1", "eu-west-1", ...]
   - If azure: ["eastus", "westeurope", ...]
3. **instance_type**: Context-aware based on provider + region
   - If aws + us-east-1: ["t3.micro", "t3.small", ...]

**Value:** Prevents invalid combinations like "azure" + "us-east-1"

### Use Case 2: Database Query Builder

**Resource:** `db://{connection}/{schema}/{table}`

**Completion Flow:**
1. **connection**: ["prod", "staging", "dev"]
2. **schema**: API call to list schemas in selected connection
3. **table**: API call to list tables in selected schema

**Value:** Users discover available resources dynamically

### Use Case 3: Code Analysis Tool

**Prompts:** `analyze_code(language, framework, analysis_type)`

**Completion Flow:**
1. **language**: ["python", "javascript", "rust"]
2. **framework**: 
   - If python: ["fastapi", "django", "flask"]
   - If javascript: ["react", "vue", "angular"]
3. **analysis_type**:
   - If fastapi: ["security", "performance", "async-patterns"]
   - If django: ["security", "orm-optimization", "migrations"]

**Value:** Intelligent, targeted analysis suggestions

</div>

---

## 🛡️ Best Practices & Patterns

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO

**Performance:**
- Return max 100 values per response
- Implement server-side filtering
- Cache expensive lookups
- Use debouncing on client

**UX:**
- Sort by relevance
- Provide descriptions when helpful
- Implement fuzzy matching
- Return empty array if no matches

**Code Quality:**
```python
# Good: Descriptive values
{
    "value": "python",
    "description": "Python 3.11+"
}

# Good: Proper filtering
filtered = [
    v for v in values 
    if query.lower() in v.lower()
]
```

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T

**Performance:**
- Return unlimited results
- Skip filtering with large lists
- Make API calls on every keystroke
- Ignore rate limiting

**UX:**
- Return irrelevant matches
- Ignore user input for filtering
- Skip context when available
- Use vague value names

**Code Quality:**
```python
# Bad: No filtering
return {"values": all_10000_items}

# Bad: Ignoring context
def complete(ref, argument, context):
    # context is available but ignored
    return static_list

# Bad: No error handling
repos = fetch_api(owner)  # May fail!
```

</div>

</div>

---

## 🔔 Advanced Topics

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pagination for Large Result Sets

```python
@mcp.completion()
async def handle_completion(ref, argument, context):
    """Handle large completion lists"""
    all_results = await fetch_large_dataset()
    
    # Filter based on user input
    filtered = filter_results(all_results, argument.value)
    
    # Return paginated results
    return {
        "values": filtered[:100],  # First page only
        "total": len(filtered),
        "hasMore": len(filtered) > 100
    }
```

### Fuzzy Matching Implementation

```python
from difflib import SequenceMatcher

def fuzzy_match(query: str, options: list[str], threshold=0.6):
    """Return options matching query with fuzzy logic"""
    matches = []
    query_lower = query.lower()
    
    for option in options:
        ratio = SequenceMatcher(
            None, 
            query_lower, 
            option.lower()
        ).ratio()
        
        if ratio >= threshold:
            matches.append((option, ratio))
    
    # Sort by match quality
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches]

# Usage in completion
@mcp.completion()
async def handle_completion(ref, argument, context):
    options = ["python", "pytorch", "pyspark", "javascript"]
    typed = argument.value or ""
    
    matches = fuzzy_match(typed, options)
    return {"values": matches}
```

### Caching Strategy

```python
from functools import lru_cache
import asyncio

class CompletionCache:
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    async def get_or_fetch(self, key, fetch_func):
        """Get from cache or fetch fresh data"""
        now = asyncio.get_event_loop().time()
        
        if key in self.cache:
            data, timestamp = self.cache[key]
            if now - timestamp < self.ttl:
                return data
        
        # Cache miss or expired
        data = await fetch_func()
        self.cache[key] = (data, now)
        return data

# Usage
cache = CompletionCache()

@mcp.completion()
async def handle_completion(ref, argument, context):
    if argument.name == "repo":
        owner = context.arguments.get("owner")
        repos = await cache.get_or_fetch(
            f"repos:{owner}",
            lambda: fetch_github_repos(owner)
        )
        return {"values": repos}
```

</div>

---

## 🎯 Testing Your Completion Logic

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Unit Test Template

```python
import pytest
from mcp.types import PromptReference, CompletionArgument

@pytest.mark.asyncio
async def test_language_completion():
    """Test basic language completion"""
    result = await handle_completion(
        ref=PromptReference(type="ref/prompt", name="review_code"),
        argument=CompletionArgument(name="language", value="py"),
        context=None
    )
    
    assert "python" in result["values"]
    assert "pytorch" in result["values"]
    assert "javascript" not in result["values"]

@pytest.mark.asyncio
async def test_context_aware_completion():
    """Test framework completion depends on language"""
    from mcp.types import CompletionContext
    
    result = await handle_completion(
        ref=PromptReference(type="ref/prompt", name="setup_project"),
        argument=CompletionArgument(name="framework", value="fast"),
        context=CompletionContext(arguments={"language": "python"})
    )
    
    assert "fastapi" in result["values"]
    assert "fastify" not in result["values"]  # JavaScript framework

@pytest.mark.asyncio
async def test_empty_input_returns_all():
    """Test empty input returns all options"""
    result = await handle_completion(
        ref=PromptReference(type="ref/prompt", name="review_code"),
        argument=CompletionArgument(name="language", value=""),
        context=None
    )
    
    # Should return all languages when nothing typed
    assert len(result["values"]) > 0
```

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Think of Completions as a Smart Assistant

**Without Completions:**  
User navigates a dark room, guessing where things are

**↓**

**With Static Completions:**  
User has a list of items in the room

**↓**

**With Filtered Completions:**  
List updates as user describes what they want

**↓**

**With Context-Aware Completions:**  
Assistant remembers previous choices and suggests related items

**↓**

**Result:**  
User moves through decisions effortlessly, discovering capabilities naturally

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"Completions provide intelligent, context-aware autocomplete suggestions for prompt arguments and resource parameters, transforming parameter entry from frustrating guesswork into guided discovery with IDE-like user experience."*

</div>

---

## 🚀 Quick Start: Complete Working Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Server (server.py)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Project Setup Assistant")

# Define prompt with parameters
@mcp.prompt()
async def setup_project(
    language: str,
    framework: str,
    features: str
):
    """Setup a new project with specified stack"""
    return f"Setting up {language} project with {framework}..."

# Implement intelligent completions
@mcp.completion()
async def handle_completion(ref, argument, context):
    """Provide context-aware completions"""
    
    # Level 1: Static language list
    if argument.name == "language":
        languages = ["python", "javascript", "typescript", "rust"]
        typed = (argument.value or "").lower()
        matches = [l for l in languages if l.startswith(typed)]
        return {"values": matches, "hasMore": False}
    
    # Level 3: Context-aware framework
    if argument.name == "framework":
        language = context.arguments.get("language") if context else None
        
        frameworks = {
            "python": ["fastapi", "flask", "django"],
            "javascript": ["express", "nest", "fastify"],
            "typescript": ["nest", "trpc", "fastify"],
            "rust": ["actix-web", "rocket", "axum"]
        }
        
        available = frameworks.get(language, [])
        typed = (argument.value or "").lower()
        matches = [f for f in available if f.startswith(typed)]
        return {"values": matches, "hasMore": False}
    
    # Level 3: Context-aware features
    if argument.name == "features":
        framework = context.arguments.get("framework") if context else None
        
        features = {
            "fastapi": ["async", "websockets", "background-tasks"],
            "django": ["orm", "admin", "rest-framework"],
            "express": ["middleware", "routing", "static-files"],
        }
        
        available = features.get(framework, [])
        return {"values": available, "hasMore": False}
    
    return {"values": []}

if __name__ == "__main__":
    mcp.run()
```

### Client (client.py)

```python
import asyncio
from mcp.client import Client, StdioServerParameters
from mcp.types import PromptReference

async def interactive_setup():
    """Interactive project setup with completions"""
    
    async with Client(
        StdioServerParameters(command="python", args=["server.py"])
    ) as client:
        # Step 1: Complete language
        print("Enter language (type 'py' to see suggestions):")
        lang_result = await client.complete(
            ref=PromptReference(type="ref/prompt", name="setup_project"),
            argument={"name": "language", "value": "py"}
        )
        print("Suggestions:", lang_result.completion.values)
        language = "python"
        
        # Step 2: Complete framework (with context!)
        print(f"\nEnter framework for {language}:")
        fw_result = await client.complete(
            ref=PromptReference(type="ref/prompt", name="setup_project"),
            argument={"name": "framework", "value": "fast"},
            context_arguments={"language": language}
        )
        print("Suggestions:", fw_result.completion.values)
        framework = "fastapi"
        
        # Step 3: Complete features (with context!)
        print(f"\nAvailable features for {framework}:")
        feat_result = await client.complete(
            ref=PromptReference(type="ref/prompt", name="setup_project"),
            argument={"name": "features", "value": ""},
            context_arguments={
                "language": language,
                "framework": framework
            }
        )
        print("Suggestions:", feat_result.completion.values)

if __name__ == "__main__":
    asyncio.run(interactive_setup())
```

### Run It

```bash
# Terminal 1: Start server
python server.py

# Terminal 2: Run client
python client.py
```

**Output:**
```
Enter language (type 'py' to see suggestions):
Suggestions: ['python', 'pyspark']

Enter framework for python:
Suggestions: ['fastapi']

Available features for fastapi:
Suggestions: ['async', 'websockets', 'background-tasks']
```

</div>

---

## 📚 Capability Declaration

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">

### Server Must Declare Completions Support

```python
# FastMCP (automatic)
mcp = FastMCP("My Server")  # Completions enabled automatically

# Manual MCP Server
capabilities = {
    "completions": {}  # Declare support
}
```

**Important:** Clients will only send completion requests if server declares this capability!

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now understand MCP completions from basics to advanced patterns.**  
Build intelligent, context-aware autocomplete experiences that delight users! 🎯

</div>
