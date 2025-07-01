Day 2: Async Programming Basics
-------------------------------

**Goal**: Deepen async programming understanding, practice uv commands, and build an async calculator to prepare for SDK's async workflows.

-   **Theory (0.5 hours, 8:00--8:30 AM PKT)**:

    -   **Async Programming in Depth**:

        -   Async programming allows concurrent task execution without multithreading, using an event loop to manage coroutines.

        -   Coroutines (async def) are special functions that pause with await, allowing other tasks to run.

        -   Example: await asyncio.sleep(1) simulates an I/O-bound task (e.g., API call).

        -   Relevance: OpenAI Agents SDK uses async methods (e.g., Runner.run) for efficient agent interactions.

    -   **uv Workflow**:

        -   uv streamlines dependency management with pyproject.toml, ensuring reproducible environments.

        -   Key commands: uv sync updates dependencies; uv run executes scripts in the virtual environment.

        -   Relevance: Ensures clean SDK setup, avoiding conflicts when adding openai-agents or litellm.

-   **Study (1 hour, 8:30--9:30 AM PKT)**:

    -   **Async Programming Basics (40 minutes)**:

        -   Watch a YouTube video on async/await, focusing on coroutines and event loops.

        -   **YouTube Search Query**: "Tech With Tim Python async await tutorial" or "freeCodeCamp Python async basics".

        -   Key Concepts:

            -   asyncio.run executes async functions.

            -   await pauses coroutines for non-blocking tasks.

            -   Example:

                ```
                import asyncio
                async def task():
                    await asyncio.sleep(1)
                    return "Task done"
                print(asyncio.run(task()))  # Output: Task done
                ```

    -   **uv Commands Review (20 minutes)**:

        -   Review uv commands (https://docs.astral.sh/uv/).

        -   **YouTube Search Query**: "Python uv project manager tutorial".

        -   Key Concepts:

            -   uv sync: Updates dependencies.

            -   uv run: Runs scripts in the virtual environment.

-   **Coding (1 hour, 9:30--10:30 AM PKT)**:

    -   **Verify uv Setup (15 minutes)**:

        -   Ensure project is set up:

            ```
            cd openai-agent
            source .venv/bin/activate
            uv sync
            ```

    -   **Build an Async Calculator Class (45 minutes)**:

        -   Create a script to practice async programming with OOP, building on Day 1's calculator.

        -   File: async_calculator.py

            ```
            import asyncio
            class AsyncCalculator:
                def __init__(self, name: str):
                    self.name = name

                async def add(self, a: int, b: int) -> int:
                    """Add two numbers with delay."""
                    await asyncio.sleep(1)  # Simulate async work
                    return a + b

                async def multiply(self, a: int, b: int) -> int:
                    """Multiply two numbers with delay."""
                    await asyncio.sleep(1)
                    return a * b

                async def reverse_string(self, text: str) -> str:
                    """Reverse a string with delay."""
                    await asyncio.sleep(1)
                    return text[::-1]

            # Test the class
            async def main():
                calc = AsyncCalculator("AsyncCalc")
                add_result = await calc.add(5, 3)
                multiply_result = await calc.multiply(4, 2)
                reverse_result = await calc.reverse_string("hello")
                print(f"Add: {add_result}, Multiply: {multiply_result}, Reverse: {reverse_result}")
                # Output: Add: 8, Multiply: 8, Reverse: olleh
            asyncio.run(main())
            ```

        -   Run:

            ```
            uv run python async_calculator.py
            ```

-   **Debugging (0.5 hours, 10:30--11:00 AM PKT)**:

    -   **Simulate Error 1**: Call an async method without await:

        ```
        calc = AsyncCalculator("AsyncCalc")
        print(calc.add(5, 3))  # TypeError or coroutine object
        ```

        -   Fix: Use await in an async function:

            ```
            async def main():
                calc = AsyncCalculator("AsyncCalc")
                result = await calc.add(5, 3)
                print(result)  # Output: 8
            asyncio.run(main())
            ```

    -   **Simulate Error 2**: Pass incorrect types to add:

        ```
        await calc.add("5", 3)  # TypeError
        ```

        -   Fix: Convert types:

            ```
            await calc.add(int("5"), 3)
            ```

    -   **Strategy**:

        -   Check for coroutine object errors (missing await).

        -   Use print(f"a: {type(a)}, b: {type(b)}") to debug types.

        -   Search X (#PythonAsync) or Stack Overflow for "Python async TypeError coroutine" if needed.
