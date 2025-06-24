import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

async def personality_agents_example():
    """
    Creates agents with different personalities to show how instructions work
    This demonstrates:
    - How instructions shape agent behavior
    - Running multiple agents with same input
    - Comparing different response styles
    """
    config, _, _ = create_gemini_config()

    # Agent 1: Professional and formal
    professional_agent = Agent(
        name="Professional Assistant",
        instructions="""You are a professional business assistant.
        Always be formal, use proper grammar, and provide structured responses.
        Address users as 'Sir' or 'Madam'.""",
        model="gemini-2.0-flash"
    )

    # Agent 2: Casual and friendly
    casual_agent = Agent(
        name="Buddy",
        instructions="""You are a casual, friendly helper.
        Use relaxed language, contractions, and be conversational.
        Think of yourself as talking to a good friend.""",
        model="gemini-2.0-flash"
    )

    # Agent 3: Technical expert
    technical_agent = Agent(
        name="Tech Expert",
        instructions="""You are a senior software engineer.
        Provide technical explanations with code examples when relevant.
        Use programming terminology and be precise.""",
        model="gemini-2.0-flash"
    )

    # Same question to all agents
    question = "How do I improve my coding skills?"

    print("🤖 Testing different agent personalities...\n")

    # Test professional agent
    print("👔 PROFESSIONAL AGENT:")
    result1 = await Runner.run(professional_agent, question, run_config=config)
    print(result1.final_output)
    print("\n" + "="*50 + "\n")

    # Test casual agent
    print("😊 CASUAL AGENT:")
    result2 = await Runner.run(casual_agent, question, run_config=config)
    print(result2.final_output)
    print("\n" + "="*50 + "\n")

    # Test technical agent
    print("💻 TECHNICAL AGENT:")
    result3 = await Runner.run(technical_agent, question, run_config=config)
    print(result3.final_output)
    print("\n✅ Notice how the same question gets different response styles!")

if __name__ == "__main__":
    asyncio.run(personality_agents_example())
