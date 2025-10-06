# 📁 MCP Roots Mastery Guide

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What are Roots?

**Roots** define filesystem boundaries for server operations—they're permission markers that tell servers *"You can work in these directories."* Think of them as **workspace boundaries** that guide servers to relevant files while maintaining security.

> **Think of it like this:** Giving someone keys to specific rooms in a building, not the entire building. Roots say "here's your workspace" without granting unlimited filesystem access.

</div>

---

## 🤔 The Problem Roots Solve

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Scenario: Video Conversion Tool

**User asks:** *"Convert biking.mp4 to MOV format"*

**Without Roots:**
```
❌ Claude receives: "biking.mp4"
❌ Where is this file? Unknown!
❌ Search entire filesystem? Security risk!
❌ Require full path? Poor user experience!
   User must type: /Users/john/Movies/vacation/biking.mp4
```

**With Roots:**
```
✅ Client exposes: file:///Users/john/Movies (root directory)
✅ Server searches within allowed roots
✅ Finds: /Users/john/Movies/vacation/biking.mp4
✅ User just says: "biking.mp4" - natural and easy!
```

**The Magic:** Roots provide automatic context discovery—servers know where to look without compromising security or user experience.

</div>

---

## 🎯 Core Concept: What Roots Really Are

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🗺️ Workspace Boundaries
Define where servers can operate

*Not permissions, but guidance*

</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 📂 Project Context
Help servers understand structure

*Which files belong to the project?*

</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🔒 Security Markers
Guide access without full control

*Client always has final say*

</div>

</div>

---

## 🏗️ Root Structure

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```json
{
  "uri": "file:///Users/agent/travel-planning",
  "name": "Travel Planning Workspace"
}
```

### Key Components

**`uri`** - File system path using `file://` scheme (ALWAYS filesystem, never HTTP)

**`name`** - Human-readable description of the workspace

</div>

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">

### Important Rules

✅ **Roots are ONLY filesystem paths** - Always use `file://` URI scheme  
✅ **Client controls actual access** - Roots are guidance, not permissions  
✅ **Dynamic updates** - Roots can change as users work  
✅ **Multiple roots allowed** - Different directories for different purposes

</div>

---

## 💡 Perfect Example: Travel Planning Workspace

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 15px; margin: 20px 0;">

### The Scenario

A travel agent manages multiple client trips with organized directories.

**Client provides these roots:**

```javascript
[
  {
    uri: "file:///Users/agent/travel-planning",
    name: "Main Workspace"
  },
  {
    uri: "file:///Users/agent/travel-templates", 
    name: "Reusable Templates"
  },
  {
    uri: "file:///Users/agent/client-documents",
    name: "Client Documents"
  }
]
```

### Server Operations Within Roots

**✅ Can access:**
- Read itineraries in `/travel-planning/barcelona-trip/`
- Copy templates from `/travel-templates/european-tour.md`
- Reference passport info in `/client-documents/smith-passport.pdf`

**❌ Cannot access:**
- Files outside these roots like `/Users/agent/personal-finances/`
- System directories
- Other users' files

**When agent opens archive:** `file:///Users/agent/archive/2023-trips`  
→ Client sends `roots/list_changed` notification  
→ Server updates its understanding of available directories

</div>

---

## 🔄 The Roots Workflow

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #11998e;">

### Complete Flow

```
1. 👤 User opens workspace/project
        ↓
2. 🖥️ Client automatically exposes directory as root
        ↓
3. 🔧 Server requests root list when needed
        ↓
4. 📋 Client returns available roots
        ↓
5. 🔍 Server searches within root boundaries
        ↓
6. 📁 Server finds and operates on files
        ↓
7. 🔔 User opens new folder → roots/list_changed notification
        ↓
8. 🔄 Server updates its understanding
```

</div>

---

## 💻 Implementation Patterns

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Server Requests Roots

```python
# Server asks: "What directories can I access?"
async def list_roots(self) -> types.ListRootsResult:
    """Request list of accessible roots from client."""
    return await self.send_request(
        types.ServerRequest(
            types.ListRootsRequest(
                method="roots/list"
            )
        ),
        types.ListRootsResult
    )
```

### Client Notifies of Changes

```python
# Client announces: "The workspace changed!"
async def send_roots_list_changed(self) -> None:
    """Notify server that roots have changed."""
    await self.send_notification(
        types.ClientNotification(
            types.RootsListChangedNotification(
                method="notifications/roots/list_changed"
            )
        )
    )
```

### Server Uses Roots

```python
# Server intelligently uses root context
async def find_file(filename: str):
    # Get available roots
    roots = await ctx.session.list_roots()
    
    # Search within root boundaries
    for root in roots.roots:
        # Search root directory
        files = await search_directory(root.uri, filename)
        if files:
            return files[0]  # Found it!
    
    return None  # Not found in accessible roots
```

</div>

---

## 🎭 Traditional vs Roots-Based Approach

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #f8d7da; padding: 25px; border-radius: 10px; border: 2px solid #dc3545;">

### ❌ Without Roots (Manual Config)

```python
# Hardcoded or configured
project_dir = "/path/to/project"

def analyze_code():
    file = f"{project_dir}/src/main.py"
    # Analyze file
```

**Problems:**
- Manual configuration required
- Hardcoded paths break
- No dynamic updates
- Poor user experience
- Security risks with full paths

</div>

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px; border: 2px solid #28a745;">

### ✅ With Roots (Automatic)

```python
# Automatic context discovery
async def analyze_code():
    roots = await ctx.session.list_roots()
    files = roots[0].list_files("**/*.py")
    # Analyze files
```

**Benefits:**
- Automatic context discovery
- Dynamic workspace updates
- Natural user commands
- Secure boundaries
- No manual configuration

</div>

</div>

---

## 🎯 Root Types & Use Cases

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### 📦 Project Roots

**Examples:**
- VS Code workspace folders
- PyCharm project directories
- Git repository roots

**Purpose:** Define project boundaries for development tools

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### 📄 Document Roots

**Examples:**
- Client document folders
- Template libraries
- Resource directories

**Purpose:** Organize access to related files

</div>

<div style="background: #e8f5e9; padding: 20px; border-radius: 10px;">

### 🗄️ Archive Roots

**Examples:**
- Historical project folders
- Backup directories
- Read-only archives

**Purpose:** Access to reference materials

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px;">

### 🔧 Resource Roots

**Examples:**
- Shared templates
- Common utilities
- Configuration folders

**Purpose:** Reusable resources across projects

</div>

</div>

---

## 🔔 Dynamic Root Updates

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">

### How Roots Change During Work

**Scenario:** User's workflow throughout the day

```
9:00 AM  → Opens /travel-planning
         ✓ Root added: file:///Users/agent/travel-planning

11:30 AM → Opens /templates folder
         ✓ Root added: file:///Users/agent/templates
         📢 roots/list_changed notification sent

2:00 PM  → Opens archived project
         ✓ Root added: file:///Users/agent/archive/2023
         📢 roots/list_changed notification sent

4:00 PM  → Closes templates folder
         ✗ Root removed: file:///Users/agent/templates
         📢 roots/list_changed notification sent
```

**Server Response:** Automatically adapts to current workspace context!

</div>

---

## 🛡️ Security Model

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Critical Understanding

**Roots are NOT permissions!** They're guidance markers.

**Client Always Controls:**
- ✅ Actual file access
- ✅ Read/write permissions
- ✅ Security policies
- ✅ User privacy

**Roots Provide:**
- 📍 Workspace boundaries
- 🗺️ Project context
- 🧭 Guidance for servers
- 📋 Directory organization

### Example

```
Root: file:///Users/agent/documents

Server requests: /Users/agent/documents/report.pdf
→ Client checks: Is this allowed? (Yes)
→ Client provides: File content

Server requests: /Users/agent/passwords.txt
→ Client checks: Is this allowed? (No - outside roots!)
→ Client denies: Access denied
```

**Bottom Line:** Roots guide servers to appropriate directories, but clients make the final access decisions.

</div>

---

## 🎓 User Interaction Models

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### 🤖 Automatic (Most Common)

**How it works:**
- User opens folder in IDE
- Client automatically exposes as root
- Server receives updated roots
- No user configuration needed

**Example:**
- Open VS Code workspace
- All workspace folders become roots
- Tools can access project files

</div>

<div style="background: #e3f2fd; padding: 25px; border-radius: 10px;">

### ⚙️ Manual (Advanced Users)

**How it works:**
- User configures roots in settings
- Explicitly add/remove directories
- Fine-grained control

**Example:**
```json
{
  "roots": [
    "/projects/myapp",
    "/templates",
    "/shared-resources"
  ]
}
```

</div>

</div>

---

## 💡 Common Patterns

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Pattern 1: File Discovery

```python
# Find a file across all roots
async def find_file(filename: str):
    roots = await session.list_roots()
    for root in roots.roots:
        file_path = await search_in_directory(root.uri, filename)
        if file_path:
            return file_path
    return None
```

### Pattern 2: Project Analysis

```python
# Analyze project structure
async def analyze_project():
    roots = await session.list_roots()
    analysis = {
        "python_files": 0,
        "javascript_files": 0,
        "config_files": 0
    }
    
    for root in roots.roots:
        files = await list_files(root.uri)
        for file in files:
            if file.endswith(".py"):
                analysis["python_files"] += 1
            elif file.endswith(".js"):
                analysis["javascript_files"] += 1
    
    return analysis
```

### Pattern 3: Template Access

```python
# Access shared templates from root
async def load_template(template_name: str):
    roots = await session.list_roots()
    template_root = find_root_by_name(roots, "Templates")
    return await read_file(f"{template_root.uri}/{template_name}")
```

</div>

---

## 🎯 Best Practices

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✅ DO

- Request roots when you need context
- Respect root boundaries
- Handle roots/list_changed notifications
- Search within roots intelligently
- Use relative paths from roots
- Cache root list appropriately
- Provide helpful root names

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ❌ DON'T

- Assume roots are permissions
- Try to access outside roots
- Ignore list_changed notifications
- Hardcode file paths
- Request roots unnecessarily
- Cache roots indefinitely
- Use generic root names

</div>

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Think of Roots as a Map

**Without Roots:**  
Server is lost in a massive city (filesystem) with no map

**↓**

**With Roots:**  
Server has a map showing neighborhoods (directories) it can explore

**↓**

**Result:**  
Server knows where to look, user gets natural experience, security is maintained

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"Roots define filesystem boundaries that guide servers to relevant directories, enabling automatic workspace discovery and natural user commands while the client maintains full security control."*

</div>

---

## 🚀 Quick Start Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```python
# Complete example: File finder with roots
@mcp.tool()
async def find_and_read_file(ctx: Context, filename: str) -> str:
    """Find a file in workspace roots and read its content."""
    
    # Get available roots
    roots_result = await ctx.session.list_roots()
    
    # Search through each root
    for root in roots_result.roots:
        # Search directory
        files = await search_directory(root.uri, filename)
        
        if files:
            # Found the file!
            file_path = files[0]
            content = await read_file(file_path)
            return f"Found in {root.name}:\n\n{content}"
    
    return f"File '{filename}' not found in any accessible workspace"
```

**User Experience:**
```
User: "Read the config.yaml file"
→ No full path needed!
→ Server searches roots automatically
→ Returns content from correct location
```

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now understand how roots provide workspace context to servers.**  
Build intelligent tools that know where to look without compromising security! 🗂️

</div>
