# 🧠 MCP Sampling Mastery Guide

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is Sampling?

**Sampling** enables servers to delegate AI reasoning tasks to the client's LLM, shifting cost and control while maintaining security. Instead of hardcoding intelligence or managing API keys, servers ask the client: *"Can you think about this for me?"*

> **Think of it like this:** A travel agent (server) gathering flight options, then asking you and your AI assistant (client) to analyze which is best, rather than making the decision themselves.

</div>

---

## 🤔 The Core Problem Sampling Solves

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Without Sampling (Traditional Approach)

**Server must:**
- Pay for LLM API calls
- Manage API keys and credentials
- Hardcode AI logic or responses
- Handle rate limits and costs
- Risk unlimited usage by random users

### With Sampling (MCP Approach)

**Server delegates:**
- Client pays for their own AI usage
- Client manages their LLM access
- Dynamic, flexible AI reasoning
- User maintains control and security
- No server-side API costs

**Result:** Publicly accessible AI-powered tools without the server paying for inference!

</div>

---

## 🔄 The Sampling Flow

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #667eea;">

```
1. 🖥️  Server completes its work (e.g., fetches 47 flight options)
        ↓
2. 🧠  Server creates a prompt asking for AI analysis
        ↓
3. 📤  Server sends sampling request to client
        ↓
4. 👤  User reviews and approves request (human-in-the-loop)
        ↓
5. 🤖  Client calls their LLM (Claude, GPT, etc.) with the prompt
        ↓
6. 👤  User reviews AI response before sending back
        ↓
7. 📥  Client returns generated text to server
        ↓
8. ✅  Server uses the AI analysis in its final response
```

**Critical Point:** Multiple human-in-the-loop checkpoints ensure security and control!

</div>

---

## 🎭 Traditional Tools vs Sampling-Enabled Tools

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #f8d7da; padding: 25px; border-radius: 10px; border: 2px solid #dc3545;">

### ❌ Option A: Server Calls LLM Directly

```python
def create_story(topic: str) -> str:
    # Server makes API call
    story = llm_api.generate(
        f"Story about {topic}"
    )
    return story
```

**Problems:**
- Server pays for every call
- Needs API keys
- Security risks
- Cost scales with users

</div>

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px; border: 2px solid #28a745;">

### ✅ Option B: Sampling (AI on Client)

```python
async def create_story(
    ctx: Context, 
    topic: str
) -> str:
    # Ask client's LLM
    prompt = f"Write story: {topic}"
    result = await ctx.sampling.create(
        messages=[...]
    )
    return result.content
```

**Benefits:**
- Client pays for their usage
- No server API keys needed
- User controls AI access
- Publicly scalable

</div>

</div>

---

## 🏗️ Architecture: Why Stateful HTTP?

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">

### Traditional HTTP (Stateless) ❌

```
Client → Tool Request → Server
Client ← Tool Response ← Server
```

**One-way communication only!**

---

### Sampling HTTP (Stateful) ✅

```
Client → Tool Request → Server
          ↓
Client ← Sampling Request ← Server  (Server asks client to think)
          ↓
Client → Sampling Response → Server
          ↓
Client ← Tool Response ← Server
```

**Bidirectional communication required!**

**Why?** The server must be able to send requests BACK to the client, which requires maintaining connection state throughout the operation.

</div>

---

## 📋 Sampling Request Anatomy

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```python
{
  messages: [
    {
      role: "user",
      content: "Analyze these 47 flight options and recommend best:\n" +
               "[Flight data: prices, times, airlines, layovers]\n" +
               "User preferences: morning departure, max 1 layover"
    }
  ],
  
  modelPreferences: {
    hints: [{ name: "claude-3-5-sonnet" }],  # Suggested model
    costPriority: 0.3,           # Less concerned about API cost
    speedPriority: 0.2,          # Can wait for analysis
    intelligencePriority: 0.9    # Need complex reasoning
  },
  
  systemPrompt: "You are a travel expert helping users find optimal flights",
  
  maxTokens: 1500
}
```

</div>

---

## 🎯 Key Components Explained

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### 📨 Messages
The actual prompt/conversation sent to the LLM

**Contains:** The analysis task, data, context, and user preferences

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### 🎛️ Model Preferences
Priority hints for model selection

**Three dimensions:**
- Cost (cheap vs expensive)
- Speed (fast vs thorough)
- Intelligence (simple vs complex)

</div>

<div style="background: #e8f5e9; padding: 20px; border-radius: 10px;">

### 📜 System Prompt
Sets the AI's role and behavior

**Purpose:** Defines expertise and response style

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px;">

### 🔢 Max Tokens
Limits response length

**Purpose:** Controls generation length and cost

</div>

</div>

---

## 💡 Perfect Example: Flight Analysis Tool

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">

### The Scenario

**User asks:** "Book me the best flight to Barcelona next month"

**Server's `findBestFlight` tool:**

1. 🔍 Queries airline APIs → Gets 47 flight options
2. 🧠 Creates sampling request: "Analyze these 47 flights considering user preferences"
3. 👤 User approves the analysis request
4. 🤖 Client's AI evaluates complex trade-offs:
   - Cheaper red-eye vs convenient morning flights
   - Direct vs 1-layover options
   - Price vs comfort balance
5. 📊 Returns top 3 recommendations with reasoning
6. ✅ Server presents analyzed results to user

**Why Sampling Wins:** The server doesn't need to understand travel preferences or complex decision-making—it just gathers data and lets the client's AI do the reasoning!

</div>

---

## 🛡️ Security & Human-in-the-Loop

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Two Critical Approval Points

**1. Request Approval (Before AI Call)**
- User sees what the server wants to analyze
- Can approve, deny, or modify the request
- Prevents malicious or wasteful prompts

**2. Response Approval (After AI Call)**
- User reviews AI-generated content
- Can approve, modify, or reject response
- Prevents harmful content from reaching server

### User Controls

**Transparency:**
- See exact prompts sent to AI
- View model selection and token limits
- Review all AI responses

**Configuration:**
- Set trusted servers for auto-approval
- Require approval for everything
- Configure model preferences
- Redact sensitive information

**Security Features:**
- Rate limiting on sampling requests
- Content validation
- Sensitive data handling
- No blind server access to AI

</div>

---

## 💻 Implementation Deep Dive

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Client Declares Sampling Capability

```python
# Client announces it can handle sampling
capabilities = ClientCapabilities(
    sampling=SamplingCapability(
        models=["openai/gpt-4o-mini"]  # Supported models
    )
)
```

### Server Uses Sampling

```python
@mcp.tool()
async def create_story(ctx: Context, topic: str) -> str:
    # Construct the prompt
    prompt = f"Write a creative story about: {topic}"
    
    # Ask client's LLM to generate content
    result = await ctx.sampling.create(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=prompt
                )
            )
        ],
        max_tokens=500
    )
    
    return result.content
```

### Default Callback (If Sampling Not Supported)

```python
async def _default_sampling_callback(
    context: RequestContext,
    params: CreateMessageRequestParams,
) -> CreateMessageResult | ErrorData:
    return ErrorData(
        code=INVALID_REQUEST,
        message="Sampling not supported"
    )
```

</div>

---

## 🎯 When to Use Sampling

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px; border: 2px solid #28a745;">

### ✅ Perfect Use Cases

- **Public MCP servers** - Let users pay for their AI usage
- **Complex reasoning** - Analysis, recommendations, evaluation
- **Creative generation** - Stories, summaries, content
- **Data interpretation** - Making sense of large datasets
- **Contextual decisions** - Personalized recommendations
- **Cost-sensitive tools** - Avoid unlimited server expenses

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px; border: 2px solid #dc3545;">

### ❌ Poor Use Cases

- **Simple lookups** - Just return data directly
- **Deterministic operations** - No AI needed
- **Real-time requirements** - Human approval adds latency
- **Private internal tools** - Server can have its own AI
- **Minimal computation** - Overhead not worth it

</div>

</div>

---

## 🔑 Key Concepts Summary

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px;">

### 🔄 Sampling/Create
Server-to-client request for LLM inference

**Purpose:** Delegate AI reasoning to client

</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px;">

### 🤖 Agentic Tools
Tools that use AI reasoning in their workflow

**Purpose:** Flexible, adaptive functionality

</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px;">

### 🔌 Stateful Connections
Required for bidirectional communication

**Purpose:** Server can send requests to client

</div>

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 10px;">

### 🤝 Capability Negotiation
Client declares sampling support at init

**Purpose:** Server knows what client can do

</div>

</div>

---

## 🎓 Best Practices

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Server-Side

✅ **Construct clear, specific prompts** - The better your prompt, the better the AI response  
✅ **Handle sampling failures gracefully** - Client might not support sampling  
✅ **Set appropriate max_tokens** - Balance completeness and cost  
✅ **Provide system prompts** - Guide AI behavior and expertise  
✅ **Use model preferences wisely** - Match priority to task complexity

### Client-Side

✅ **Implement human-in-the-loop review** - Let users approve requests  
✅ **Display transparent information** - Show prompts, models, limits  
✅ **Rate limit sampling requests** - Prevent abuse  
✅ **Validate message content** - Security check all inputs  
✅ **Support multiple models** - Give users choice

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### The Fundamental Shift

**Traditional Tools:**  
Server contains all the logic and intelligence

**↓**

**Sampling-Enabled Tools:**  
Server defines the process, client provides the intelligence

**↓**

**Result:**  
Tools that can adapt, reason, and produce sophisticated outputs without server-side AI costs

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"Sampling lets servers delegate AI reasoning to clients, enabling publicly accessible AI-powered tools without server-side API costs or security risks, while maintaining user control through human-in-the-loop approval."*

</div>

---

## 🚀 Quick Start Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```python
# Complete story generation tool with sampling
@mcp.tool()
async def create_story(ctx: Context, topic: str) -> str:
    """Generate a creative story about any topic using AI."""
    
    # Construct the prompt
    prompt = f"Write a creative short story about: {topic}"
    
    try:
        # Request AI generation from client
        result = await ctx.sampling.create(
            messages=[
                SamplingMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=prompt
                    )
                )
            ],
            system_prompt="You are a creative storyteller",
            max_tokens=500,
            model_preferences={
                "intelligencePriority": 0.8,
                "costPriority": 0.5
            }
        )
        
        return result.content
        
    except SamplingNotSupported:
        return "Error: Client doesn't support AI sampling"
```

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now understand how to build intelligent tools that delegate reasoning to clients.**  
Create powerful, publicly accessible AI tools without managing API keys or costs! 🚀

</div>
