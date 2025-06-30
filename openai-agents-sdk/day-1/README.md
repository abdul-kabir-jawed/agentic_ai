Day 1  Learning Plan for OpenAI Agents SDK
===================================================

This document outlines detailed plans for **Day 1**  to start your journey toward mastering the OpenAI Agents SDK for Python, tailored for a beginner with basic Python skills (lists, dictionaries, functions, OOP). Each day includes 3 hours: 1 hour study (YouTube, documentation), 1 hour coding, 0.5 hours debugging, and 0.5 hours theory, using uv and a Gemini API key, all free. The schedule assumes 8:00--11:00 AM PKT (adjustable to 6:00--9:00 PM PKT). The goal is to build foundational skills for the SDK, with practical projects, debugging, and theoretical understanding to achieve mastery in 4 months (360 hours).

* * * * *

Day 1: Python OOP Review and uv Setup
-------------------------------------

**Goal**: Reinforce Python OOP skills, set up uv for OpenAI Agents SDK, and introduce async programming to prepare for SDK usage.

-   **Theory (0.5 hours, 8:00--8:30 AM PKT)**:

    -   **Object-Oriented Programming (OOP)**:
        -   OOP organizes code into objects, which are instances of classes combining data (attributes) and behavior (methods).
        -   Key principles: Encapsulation (bundling data/methods), Inheritance (reusing class functionality), Polymorphism (flexible method behavior).
        -   Relevance: The SDK uses OOP for agents (e.g., `Agent` class) and tools, leveraging your existing OOP skills.
    -   **uv Project Manager**:
        -   uv is a fast, Rust-based tool for managing Python virtual environments and dependencies, replacing `venv`/`pip`.
        -   Benefits: Faster dependency resolution, simplified project setup, critical for efficient SDK development.
    -   **Async Programming**:
        -   Async programming enables non-blocking operations, allowing tasks (e.g., API calls) to run concurrently.
        -   Uses `async def` for functions and `await` for pausing execution, managed by an event loop.
        -   Relevance: SDK's `Runner.run` supports async workflows for efficient agent execution.
-   **Study (1 hour, 8:30--9:30 AM PKT)**:

    -   **Python OOP Review (30 minutes)**:
        -   Watch a YouTube video to refresh OOP knowledge, focusing on classes, objects, and methods.
        -   **YouTube Search Query**: "Corey Schafer Python OOP tutorial" or "freeCodeCamp Python object oriented programming".
        -   Key Concepts:
            -   Define classes with `__init__` for initialization.

            -   Create methods to perform operations.

            -   Example:

                ```
                class Calculator:
                    def __init__(self, name: str):
                        self.name = name
                    def add(self, a: int, b: int) -> int:
                        return a + b
                calc = Calculator("Basic")
                print(calc.name, calc.add(2, 3))  # Output: Basic 5

                ```

    -   **uv Project Manager Introduction (30 minutes)**:
        -   Read the uv getting started guide (<https://docs.astral.sh/uv/getting-started/>).
        -   **YouTube Search Query**: "Python uv project manager tutorial" (look for Astral or Python community videos).
        -   Key Concepts:
            -   Commands: `uv init`, `uv venv`, `uv add`, `uv run`.
-   **Coding (1 hour, 9:30--10:30 AM PKT)**:

    -   **Install uv and Set Up Project (20 minutes)**:
        -   Install uv (requires Python 3.10+):

            ```
            pip install uv

            ```

        -   Create a project:

            ```
            uv init openai-agent && cd openai-agent
            uv venv
            source .venv/bin/activate  # Windows: .venv\Scripts\activate

            ```

        -   Add dependencies:

            ```
            uv add openai-agents python-dotenv litellm

            ```

        -   Create `.env` for Gemini API key (leave empty if no key yet):

            ```
            GEMINI_API_KEY=your-gemini-key

            ```

    -   **Build a Calculator Class (40 minutes)**:
        -   Create a Python script to practice OOP, aligning with your interest in calculator apps and string methods.

        -   File: `calculator.py`

            ```
            class Calculator:
                def __init__(self, name: str):
                    self.name = name

                def add(self, a: int, b: int) -> int:
                    """Add two numbers."""
                    return a + b

                def multiply(self, a: int, b: int) -> int:
                    """Multiply two numbers."""
                    return a * b

                def reverse_string(self, text: str) -> str:
                    """Reverse a string."""
                    return text[::-1]

            # Test the class
            calc = Calculator("MyCalc")
            print(calc.add(5, 3))  # Output: 8
            print(calc.multiply(4, 2))  # Output: 8
            print(calc.reverse_string("hello"))  # Output: olleh

            ```

        -   Run:

            ```
            uv run python calculator.py

            ```

-   **Debugging (0.5 hours, 10:30--11:00 AM PKT)**:

    -   **Simulate Error 1**: Run `uv add nonexistent-package` (expect `ResolutionError: Failed to resolve dependencies`).

        -   Fix: Correct to `uv add openai-agents; uv sync`.
    -   **Simulate Error 2**: Modify `calculator.py` to pass a string to `add`:

        ```
        print(calc.add("5", 3))  # TypeError: unsupported operand type(s)

        ```

        -   Fix: Ensure correct types:

            ```
            print(calc.add(int("5"), 3))  # Output: 8

            ```

    -   **Strategy**:

        -   Read error messages carefully.
        -   Use `print(f"a: {type(a)}, b: {type(b)}")` to inspect types.
        -   Search X (#Python) or Stack Overflow for "Python TypeError unsupported operand" if stuck.

* * * * *

### Tips for Success

-   **YouTube**: Use exact search queries (e.g., "Corey Schafer Python OOP tutorial") on channels like freeCodeCamp, Corey Schafer, or Tech With Tim.
-   **Environment**: Verify uv with `uv --version`. Run `uv sync` if dependencies fail.
-   **Gemini**: Days 1--2 focus on Python foundations; Gemini API will be used on Day 3 for a basic agent.
-   **Debugging**: Read error messages, use `print` for debugging, and check X (#Python, #OpenAIAgentsSDK).
-   **Schedule**: Stick to 8:00--11:00 AM PKT or adjust to 6:00--9:00 PM PKT.

