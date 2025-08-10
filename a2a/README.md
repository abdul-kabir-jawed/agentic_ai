# 🤖 Agent2Agent (A2A) Protocol


*An open protocol enabling communication and interoperability between opaque agentic applications*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation](https://img.shields.io/badge/docs-a2a--protocol.org-brightgreen.svg)](https://a2a-protocol.org/latest/)
[![Python SDK](https://img.shields.io/pypi/v/a2a-sdk?label=Python%20SDK)](https://pypi.org/project/a2a-sdk/)
[![JS SDK](https://img.shields.io/npm/v/@a2a-js/sdk?label=JS%20SDK)](https://www.npmjs.com/package/@a2a-js/sdk)

[**📚 Documentation**](https://a2a-protocol.org/latest/) • [**📝 Specification**](https://a2aproject.github.io/A2A/specification/) • [**🎬 Samples**](https://github.com/a2aproject/a2a-samples) • [**💬 Discussions**](https://github.com/a2aproject/A2A/discussions)

</div>

---

## 🎯 What is A2A?

The Agent2Agent (A2A) protocol addresses a critical challenge in the AI landscape: enabling AI agents to communicate and collaborate across different platforms and frameworks, regardless of their underlying technologies. A2A provides a common language for agents, fostering a more interconnected, powerful, and innovative AI ecosystem.

### 🌟 Key Capabilities

With A2A, agents can:
- **🔍 Discover** each other's capabilities dynamically
- **🤝 Negotiate** interaction modalities (text, forms, media)
- **🔒 Securely collaborate** on long-running tasks
- **🛡️ Operate without exposing** their internal state, memory, or tools

---

## ✨ Why A2A Matters

| Challenge | A2A Solution |
|-----------|--------------|
| **🏗️ Break Down Silos** | Connect agents across different ecosystems and frameworks |
| **🔄 Enable Complex Collaboration** | Allow specialized agents to work together on multi-step tasks |
| **📐 Promote Open Standards** | Foster community-driven approach to agent communication |
| **🔐 Preserve Opacity** | Agents collaborate without sharing internal memory or proprietary logic |

---

## 🏛️ Core Architecture

A2A is built on existing standards including HTTP, SSE, and JSON-RPC, making it easier to integrate with existing IT stacks. The protocol features:

### 🔧 Technical Foundation
- **📡 Standardized Communication**: JSON-RPC 2.0 over HTTP(S)
- **🎯 Agent Discovery**: Via "Agent Cards" detailing capabilities and connection info
- **⚡ Flexible Interaction**: Supports synchronous request/response, streaming (SSE), and asynchronous push notifications
- **📊 Rich Data Exchange**: Handles text, files, and structured JSON data
- **🏢 Enterprise-Ready**: Built with enterprise-grade authentication and authorization, supporting OpenAPI's authentication schemes

### 🔒 Security Features
- HTTPS with modern TLS mandatory for production
- Each Agent Card specifies authentication method clients must use (API keys, OAuth, etc.)
- Server identity verification via standard TLS certificate validation
- Enterprise-grade authentication and authorization support

---

## 🤜🤛 A2A and MCP: Better Together

A2A and the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) are complementary standards:

| Protocol | Purpose | Role |
|----------|---------|------|
| **🔧 MCP** | Connects agents to tools, APIs, and resources | How agents access their capabilities |
| **🤖 A2A** | Facilitates communication between agents as peers | How agents collaborate and delegate tasks |

---

## 🚀 Quick Start

### Installation

**Python SDK:**
```bash
pip install a2a-sdk
```

**JavaScript SDK:**
```bash
npm install @a2a-js/sdk
```

### Basic Usage

**Python Example:**
```python
from a2a_sdk import A2AClient

# Initialize client
client = A2AClient(
    agent_card_url="https://example.com/agent-card",
    auth_token="your-token"
)

# Discover agent capabilities
capabilities = await client.get_capabilities()

# Start a task
task = await client.start_task(
    skill="data_analysis",
    parameters={"dataset": "sales_data.csv"}
)

# Get task status
status = await client.get_task_status(task.id)
```

**JavaScript Example:**
```javascript
import { A2AClient } from '@a2a-js/sdk';

// Initialize client
const client = new A2AClient({
  agentCardUrl: 'https://example.com/agent-card',
  authToken: 'your-token'
});

// Discover agent capabilities
const capabilities = await client.getCapabilities();

// Start a task
const task = await client.startTask({
  skill: 'data_analysis',
  parameters: { dataset: 'sales_data.csv' }
});

// Stream task updates
const stream = client.streamTask(task.id);
for await (const update of stream) {
  console.log('Task update:', update);
}
```

---

## 🔄 Task Lifecycle

A2A supports various interaction patterns:

### 🎯 Synchronous Tasks
Quick, immediate responses for simple operations.

### 📡 Streaming Tasks
Real-time feedback for long-running operations with Server-Sent Events (SSE).

### 🔔 Asynchronous Tasks
Support for very long-running tasks and human-in-the-loop interactions with push notifications.

---

## 🏗️ Framework Integrations

A2A works with popular agent frameworks:

| Framework | Integration | Status |
|-----------|-------------|---------|
| **🦾 CrewAI** | Native support | ✅ Available |
| **🕸️ LangGraph** | Official integration | ✅ Available |
| **⚙️ Vertex GenKit** | Google ADK support | ✅ Available |
| **🔧 Custom Solutions** | SDK-based integration | ✅ Supported |

---

## 📊 Use Cases

### 🏢 Enterprise Scenarios
- **📈 Multi-step Data Analysis**: Chain specialized agents for complex analytics workflows
- **📝 Document Processing**: Route documents through OCR, analysis, and summary agents
- **🔍 Research & Investigation**: Coordinate search, analysis, and synthesis agents

### 🌐 Cross-Platform Collaboration
- **☁️ Hybrid Cloud**: Agents running on different cloud providers working together
- **🏪 Vendor Ecosystems**: Integration between different AI service providers
- **🔧 Tool Orchestration**: Combine agents with different specialized capabilities

---

## 📚 Resources

### 📖 Documentation
- [**Complete Documentation**](https://a2a-protocol.org/latest/) - Full guides and tutorials
- [**Technical Specification**](https://a2aproject.github.io/A2A/specification/) - Detailed protocol definition
- [**Quickstart Tutorial**](https://a2a-protocol.org/latest/quickstart/) - Build your first A2A agent

### 🛠️ Development
- [**Code Samples**](https://github.com/a2aproject/a2a-samples) - Example implementations
- [**Python SDK**](https://github.com/a2aproject/a2a-python) - Full-featured Python client
- [**JavaScript SDK**](https://github.com/a2aproject/a2a-js) - Complete JS/TypeScript support

### 🎥 Learning
- [**Video Introduction**](https://a2a-protocol.org/latest/) - 8-minute overview
- [**Google Developers Blog**](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) - Announcement post
- [**Forbes Coverage**](https://www.forbes.com/sites/janakirammsv/2025/06/25/key-tech-firms-unite-as-google-donates-a2a-to-linux-foundation/) - Industry perspective

---

## 🤝 Contributing

We welcome community contributions to enhance and evolve the A2A protocol!

### 💬 Get Involved
- **Questions & Discussions**: Join our [GitHub Discussions](https://github.com/a2aproject/A2A/discussions)
- **Issues & Feedback**: Report issues via [GitHub Issues](https://github.com/a2aproject/A2A/issues)
- **Private Feedback**: Use our [Google Form](https://goo.gle/a2a-feedback)
- **Partner Program**: Google Cloud customers can join via [this form](https://goo.gle/a2a-partner)

### 🛠️ Development Setup
```bash
# Clone the repository
git clone https://github.com/a2aproject/A2A.git
cd A2A

# Follow the contribution guide
cat CONTRIBUTING.md
```

---

## 🛣️ Roadmap

### 🔍 Agent Discovery
- Formalize authorization schemes within Agent Cards
- Enhanced capability negotiation

### 🤖 Agent Collaboration  
- Dynamic skill querying with `QuerySkill()` method
- Improved multi-agent orchestration

### 🎨 Task Lifecycle & UX
- Dynamic UX negotiation within tasks
- Enhanced audio/video support

### 📡 Transport & Reliability
- Client-initiated method extensions
- Improved streaming and push notification reliability

---

## 📄 License

The A2A Protocol is an open-source project by Google LLC, licensed under the [Apache License 2.0](https://github.com/a2aproject/A2A/blob/main/LICENSE).

---

## 🌟 Linux Foundation Project

Google Cloud donated A2A to the Linux Foundation, ensuring community governance and open development for the future of agent interoperability.

---

<div align="center">

**🚀 Ready to build the future of agent collaboration?**

[**Get Started Now**](https://a2a-protocol.org/latest/quickstart/) • [**Join the Community**](https://github.com/a2aproject/A2A/discussions)

</div>
