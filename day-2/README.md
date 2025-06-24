Day 2: Advanced Agent Configuration & Model Mastery
===================================================

Welcome to Day 2 of your journey to mastering AI agents using Python and the OpenAI Agents framework with Gemini API integration. This repository builds on [Day 1](https://github.com/your-username/day1), focusing on advanced agent configuration, model settings (temperature, max_tokens), and dynamic instruction patterns. It contains all the code, setup instructions, and resources needed to complete the 6-hour curriculum for Day 2.

🎯 Goal
-------

Master agent configuration, model settings, and dynamic behaviors to create flexible, task-specific AI agents.

📚 Curriculum Overview
----------------------

-   **Setup Phase (30 minutes)**: Enhance the Day 1 project with new files and an advanced configuration system supporting temperature and max_tokens.
-   **Theory Session (1.5 hours)**: Learn about model parameters (temperature, max_tokens), model selection, and agent architecture.
-   **Code Practice Session (1.5 hours)**: Experiment with temperature settings and build dynamic agents that adapt to various tasks.
-   **Debug Session (45 minutes)**: Troubleshoot issues with model parameters, instructions, and async patterns.
-   **MCQ Test (15 minutes)**: Test your understanding with multiple-choice questions.
-   **Homework**: Create agents with varying temperatures, task-specific behaviors, and context-aware responses.

📂 Repository Structure
-----------------------

```
day2/
├── src/
│   ├── __init__.py
│   ├── setup.py
│   ├── enhanced_setup.py
│   ├── day1_basic_agent.py
│   ├── day1_personality_agents.py
│   ├── debug_api_key.py
│   ├── debug_test.py
│   ├── day2/
│   │   ├── __init__.py
│   │   ├── temperature_demo.py
│   │   ├── dynamic_instructions.py
│   │   ├── debug_guide.py
├── tests/
│   ├── __init__.py
├── examples/
│   ├── __init__.py
│   ├── day2/
│   │   ├── __init__.py
├── .env
├── README.md
├── pyproject.toml

```

-   **`src/`**: Contains all source code files.
    -   `setup.py`: Day 1 Gemini API configuration (kept for compatibility).
    -   `enhanced_setup.py`: Day 2 advanced configuration with temperature and max_tokens control.
    -   `day1_basic_agent.py`: Day 1 simple "Hello World" agent.
    -   `day1_personality_agents.py`: Day 1 multiple personality demo.
    -   `debug_api_key.py`: Day 1 API key debugging.
    -   `debug_test.py`: Day 1 setup verification.
    -   **`day2/`**:
        -   `temperature_demo.py`: Demonstrates temperature effects on agent responses.
        -   `dynamic_instructions.py`: Implements a flexible agent system with task-specific behaviors.
        -   `debug_guide.py`: Comprehensive debugging for Day 2 issues.
-   **`tests/`**: Placeholder for future unit tests.
-   **`examples/day2/`**: Placeholder for homework and example scripts.
-   **`.env`**: Stores environment variables (e.g., Gemini API key).
-   **`README.md`**: This file, providing project overview and instructions.
-   **`pyproject.toml`**: UV project configuration.

🚀 Setup Instructions
---------------------

1.  **Clone the Repository**:

    ```
    git clone https://github.com/your-username/day2.git
    cd day2

    ```

2.  **Install UV**:\
    Install UV, a fast Python project manager, following the [UV Documentation](https://docs.astral.sh/uv/).

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
    Execute the scripts to test your setup:

    ```
    uv run src/debug_test.py              # Verify Day 1 setup
    uv run src/day2/temperature_demo.py   # Temperature comparison
    uv run src/day2/dynamic_instructions.py # Dynamic agent demo
    uv run src/day2/debug_guide.py        # Day 2 debug guide

    ```

🧠 Key Concepts Learned
-----------------------

-   **Temperature**: Controls response creativity (0.0 = focused, 1.0 = creative).
-   **Max Tokens**: Limits response length (1 token ≈ 0.75 words).
-   **Dynamic Instructions**: Enable agents to adapt behavior based on task or context.
-   **Multiple Configurations**: Support creative, analytical, concise, and balanced use cases.
-   **Error Handling**: Validate parameters, handle async/await, and debug model settings.

💻 How to Run Each File
-----------------------

-   **`src/debug_test.py`**: Verifies Day 1 setup (configuration, agent creation, execution).

    ```
    uv run src/debug_test.py

    ```

-   **`src/day1_basic_agent.py`**: Runs Day 1's simple "Hello World" agent.

    ```
    uv run src/day1_basic_agent.py

    ```

-   **`src/day1_personality_agents.py`**: Demonstrates Day 1 agents with different personalities.

    ```
    uv run src/day1_personality_agents.py

    ```

-   **`src/debug_api_key.py`**: Debugs Day 1 API key issues.

    ```
    uv run src/debug_api_key.py

    ```

-   **`src/day2/temperature_demo.py`**: Compares agent responses with low (0.1) and high (0.9) temperatures.

    ```
    uv run src/day2/temperature_demo.py

    ```

-   **`src/day2/dynamic_instructions.py`**: Shows a dynamic agent system handling multiple tasks and evolving context.

    ```
    uv run src/day2/dynamic_instructions.py

    ```

-   **`src/day2/debug_guide.py`**: Runs debugging tests for model parameters, instructions, and async patterns.

    ```
    uv run src/day2/debug_guide.py

    ```

📝 Homework
-----------

Create three agents in new files under `examples/day2/`:

1.  **Temperature Test**: Create agents with temperatures 0.1, 0.5, and 0.9, asking the same creative question (e.g., "Write a story about a magical forest").
2.  **Task Specialist**: Build a dynamic agent switching between "teacher", "coder", and "writer" modes.
3.  **Context Builder**: Create an agent that adjusts responses based on user expertise (e.g., beginner, intermediate, expert).

Example starter code:

```
import asyncio
from agents import Agent, Runner
from enhanced_setup import create_gemini_config

async def temperature_test():
    configs = {
        'low': create_gemini_config(temperature=0.1)[0],
        'medium': create_gemini_config(temperature=0.5)[0],
        'high': create_gemini_config(temperature=0.9)[0]
    }
    agent = Agent(
        name="StoryTeller",
        instructions="Write a creative story.",
        model="gemini-2.0-flash"
    )
    question = "Write a story about a magical forest."
    for name, config in configs.items():
        result = await Runner.run(agent, question, run_config=config)
        print(f"{name.capitalize()} Temperature:\n{result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(temperature_test())

```

🔗 Resources
------------

-   [Gemini API Documentation](https://ai.google.dev/)
-   [OpenAI Agents Framework](https://platform.openai.com/docs/agents)
-   [UV Project Manager](https://docs.astral.sh/uv/)
-   [Python Asyncio Guide](https://docs.python.org/3/library/asyncio.html)
-   [Day 1 Repository](https://github.com/your-username/day1)

🚀 What's Next?
---------------

Day 3 will cover:

-   Tool integration (web search, calculators, file readers).
-   Custom tool creation.
-   Multi-step agent workflows.
-   Tool error handling.

📋 Day 2 Summary
----------------

-   **Achievements**: Enhanced configuration system, mastered temperature and max_tokens, built dynamic agents, and debugged advanced issues.
-   **New Files**: `enhanced_setup.py`, `temperature_demo.py`, `dynamic_instructions.py`, `debug_guide.py`.
-   **Key Insight**: The same AI model can behave differently based on configuration, enabling versatile agents.

* * * * *

*Created on June 24, 2025*
