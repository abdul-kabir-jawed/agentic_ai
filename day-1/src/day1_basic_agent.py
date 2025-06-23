import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

async def basic_agent_example():
    """
    Creates the simplest possible agent
    What this code does:
    1. Creates an agent with basic instructions
    2. Runs the agent with a simple question
    3. Prints the response
    """
    # Get our Gemini configuration
    config, _, _ = create_gemini_config()

    # Create a basic agent
    # Think of this like hiring an assistant and giving them job description
    basic_agent = Agent(
        name="HelloBot",  # Just a friendly name for identification
        instructions="You are a friendly assistant. Always greet users warmly and be helpful.",
        model="gemini-2.0-flash"  # Using Gemini model
    )

    print("🤖 Creating your first AI agent...")

    # Run the agent with a simple message
    # This is like talking to your assistant
    result = await Runner.run(
        agent=basic_agent,
        input="Hello! What can you help me with?",
        run_config=config  # Use our Gemini configuration
    )

    print("Agent Response:", result.final_output)
    print("✅ Success! Your first agent is working!")

# Run the example
if __name__ == "__main__":
    asyncio.run(basic_agent_example())
