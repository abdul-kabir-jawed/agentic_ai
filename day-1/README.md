Day 1: OpenAI Agents Python Foundation
======================================

Welcome to Day 1 of your journey to mastering AI agents using Python and the OpenAI Agents framework with Gemini API integration. This repository contains all the code, setup instructions, and resources needed to complete the 6-hour curriculum for Day 1.

🎯 Goal
-------

Understand core AI agent concepts and create your first working agent.

📚 Curriculum Overview
----------------------

-   **Setup Phase (30 minutes)**: Configure your development environment using UV and set up the project structure.
-   **Theory Session (1.5 hours)**: Learn what AI agents are, their components, and how they differ from traditional chatbots.
-   **Code Practice Session (1.5 hours)**: Build your first agent and explore agents with different personalities.
-   **Debug Session (45 minutes)**: Troubleshoot common setup issues.
-   **MCQ Test (15 minutes)**: Test your understanding with multiple-choice questions.
-   **Homework**: Create agents with unique behaviors (cooking assistant, ELI5 explainer, Shakespearean style).

📂 Repository Structure
-----------------------

```
day1/
├── src/
│   ├── __init__.py
│   ├── setup.py
│   ├── day1_basic_agent.py
│   ├── day1_personality_agents.py
│   ├── debug_api_key.py
│   ├── debug_test.py
├── tests/
│   ├── __init__.py
├── examples/
│   ├── __init__.py
├── .env
├── README.md
├── pyproject.toml

```

-   **`src/`**: Contains all source code files.
    -   `setup.py`: Configures Gemini API with OpenAI Agents framework.
    -   `day1_basic_agent.py`: Implements a simple "Hello World" agent.
    -   `day1_personality_agents.py`: Demonstrates agents with different personalities.
    -   `debug_api_key.py`: Debugs API key setup.
    -   `debug_test.py`: Tests the full agent setup flow.
-   **`tests/`**: Placeholder for future unit tests.
-   **`examples/`**: Placeholder for example scripts.
-   **`.env`**: Stores environment variables (e.g., Gemini API key).
-   **`README.md`**: This file, providing project overview and instructions.
-   **`pyproject.toml`**: UV project configuration.

🚀 Setup Instructions
---------------------

1.  **Clone the Repository**:

    ```
    git clone https://github.com/your-username/day1.git
    cd day1

    ```

2.  **Install UV**:\
    Follow the instructions at [UV Documentation](https://docs.astral.sh/uv/) to install UV, a fast Python project manager.

3.  **Initialize the Project**:

    ```
    uv init
    uv add openai-agents-python python-dotenv

    ```

4.  **Create .env File**:\
    Create a `.env` file in the root directory and add your Gemini API key:

    ```
    GEMINI_API_KEY=your_gemini_api_key_here

    ```

5.  **Run the Code**:\
    Execute the scripts in the `src/` directory to test your setup:

    ```
    uv run src/debug_test.py
    uv run src/day1_basic_agent.py
    uv run src/day1_personality_agents.py

    ```

🧠 Key Concepts Learned
-----------------------

-   AI agents can think, plan, act, and remember, unlike traditional chatbots.
-   Core components: Instructions (behavior), Model (engine), Tools (actions), Context (memory).
-   Async/await is essential for agent operations.
-   Instructions shape agent personality and behavior.
-   RunConfig sets global settings for agent execution.

💻 How to Run Each File
-----------------------

-   **`src/debug_test.py`**: Verifies your entire setup (configuration, agent creation, execution).

    ```
    uv run src/debug_test.py

    ```

-   **`src/day1_basic_agent.py`**: Runs a simple "Hello World" agent.

    ```
    uv run src/day1_basic_agent.py

    ```

-   **`src/day1_personality_agents.py`**: Demonstrates agents with professional, casual, and technical personalities.

    ```
    uv run src/day1_personality_agents.py

    ```

-   **`src/debug_api_key.py`**: Debugs API key configuration issues.

    ```
    uv run src/debug_api_key.py

    ```

📝 Homework
-----------

Create three agents in new files under `examples/`:

1.  A cooking assistant that provides recipes.
2.  An explainer that describes concepts as if you're 5 years old.
3.  A Shakespearean-style agent that responds in Elizabethan English.

Example starter code:

```
from agents import Agent, Runner
from setup import create_gemini_config
import asyncio

async def cooking_agent():
    config, _, _ = create_gemini_config()
    agent = Agent(
        name="ChefBot",
        instructions="You are a cooking assistant. Provide clear recipes and tips.",
        model="gemini-2.0-flash"
    )
    result = await Runner.run(agent, "How do I make pasta?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(cooking_agent())

```

🔗 Resources
------------

-   [Gemini API Documentation](https://ai.google.dev/)
-   [OpenAI Agents Framework](https://platform.openai.com/docs/agents)
-   [UV Project Manager](https://docs.astral.sh/uv/)
-   [Python Asyncio Guide](https://docs.python.org/3/library/asyncio.html)

🚀 What's Next?
---------------

Day 2 will cover advanced agent configuration, model settings, dynamic instructions, context management, and complex behaviors. Stay tuned!

* * * * *

*Created on June 24, 2025*
