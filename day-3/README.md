📅 Day 3: Introduction to LLMs and Basic OpenAI Agent 🤖
--------------------------------------------------------

**Goal**: Understand large language models (LLMs) and create a basic SDK agent with Gemini.

-   **🧠 Theory**:

    -   **Large Language Models (LLMs)**: Neural networks trained on vast text data to generate human-like responses. They process prompts and produce outputs based on patterns learned during training. 📖

        -   *Relevance*: The SDK uses LLMs (e.g., Gemini via LiteLLM) to power agent responses.

    -   **OpenAI Agents SDK Basics**: The SDK enables building AI agents with Agent and Runner classes. Agents have instructions, models, and optional tools for task execution. 🛠️

        -   *Example*: Agent(name="Assistant", instructions="Help user", model="litellm/gemini/gemini-1.5-flash").

-   **📚 Study**:

    -   **LLM Basics (30 min)**:

        -   Watch YouTube: "sentdex introduction to LLMs Python" or "freeCodeCamp AI language models" 📹.

        -   Concepts: Prompt engineering, API-based LLMs, Gemini via LiteLLM.

    -   **SDK Introduction (30 min)**:

        -   Read SDK Introduction 📖.

        -   Concepts: Agent, Runner.run_sync, model integration.

        -   Example:

            ```
            from agents import Agent, Runner
            agent = Agent(name="Assistant", instructions="You are helpful", model="litellm/gemini/gemini-1.5-flash")
            result = Runner.run_sync(agent, "Hello!")
            print(result.final_output)  # Output: Greeting response
            ```

-   **💻 Coding**:

    -   **Verify uv Setup (15 min)**:

        -   Ensure project:

            ```
            cd openai-agent
            source .venv/bin/activate
            uv sync
            ```

        -   Verify .env has GEMINI_API_KEY (mock if unavailable).

    -   **Build Basic Agent (45 min)**:

        -   Create basic_agent.py for a Q&A agent:

            ```
            from agents import Agent, Runner
            from dotenv import load_dotenv
            import os
            load_dotenv()
            # Mock response if no API key
            def mock_gemini(query: str) -> str:
                return f"Mock response: {query}"
            agent = Agent(
                name="Assistant",
                instructions="You are a helpful assistant",
                model="litellm/gemini/gemini-1.5-flash"
            )
            query = "Write a Python function to reverse a string"
            if not os.getenv("GEMINI_API_KEY"):
                result = mock_gemini(query)
            else:
                result = Runner.run_sync(agent, query).final_output
            print(result)  # Output: Function code or mock response
            ```

        -   Run:

            ```
            uv run python basic_agent.py
            ```

-   **🐞 Debugging**:

    -   **Error 1**: Missing GEMINI_API_KEY (expect AuthenticationError).

        -   Fix: Add key to .env or use mock:

            ```
            if not os.getenv("GEMINI_API_KEY"):
                print(mock_gemini(query))
            ```

    -   **Error 2**: Incorrect model name (expect ValueError).

        -   Fix: Use "litellm/gemini/gemini-1.5-flash".

    -   **Strategy**: Check .env, use print(os.getenv("GEMINI_API_KEY")), search X (#OpenAIAgentsSDK) for "AuthenticationError".
