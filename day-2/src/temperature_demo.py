# src/day2/temperature_demo.py
import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

async def temperature_comparison():
    """
    Demonstrates how temperature affects agent responses
    
    What this teaches:
    - Temperature controls creativity/randomness
    - Same question, different creativity levels
    - How to choose right temperature for your use case
    """
    print("🌡️ Testing Temperature Effects...\n")
    
    # Create configs with different temperatures
    low_temp_config, _, _ = create_gemini_config(temperature=0.1)
    high_temp_config, _, _ = create_gemini_config(temperature=0.9)
    
    # Same agent instructions for fair comparison
    agent_instructions = """You are a creative writing assistant. 
    Write a short story opening about a mysterious door."""
    
    # Low temperature agent (focused, consistent)
    focused_agent = Agent(
        name="Focused Writer",
        instructions=agent_instructions,
        model="gemini-2.0-flash"
    )
    
    # High temperature agent (creative, varied)
    creative_agent = Agent(
        name="Creative Writer", 
        instructions=agent_instructions,
        model="gemini-2.0-flash"
    )
    
    prompt = "Write the opening paragraph of a story about finding a glowing door in an old library."

    print("📝 LOW TEMPERATURE (0.1) - Focused & Consistent:")
    print("-" * 50)
    result1 = await Runner.run(
        focused_agent, 
        prompt, 
        run_config=low_temp_config
    )
    print(result1.final_output)
    
    print("\n🎨 HIGH TEMPERATURE (0.9) - Creative & Varied:")
    print("-" * 50)
    result2 = await Runner.run(
        creative_agent, 
        prompt, 
        run_config=high_temp_config
    )
    print(result2.final_output)
    
    print("\n✅ Notice the difference in creativity and style!")

# Run multiple times to see consistency vs variation
async def run_consistency_test():
    """
    Run the same prompt multiple times to see consistency differences
    """
    print("\n🔄 Running consistency test...\n")
    
    low_temp_config, _, _ = create_gemini_config(temperature=0.1)
    
    agent = Agent(
        name="Test Agent",
        instructions="Answer this question briefly and clearly.",
        model="gemini-2.0-flash"
    )
    
    question = "What is the capital of France?"
    print("Running same question 3 times with LOW temperature:")
    for i in range(3):
        result = await Runner.run(agent, question, run_config=low_temp_config)
        print(f"Run {i+1}: {result.final_output}")
    
if __name__ == "__main__":
    asyncio.run(temperature_comparison())
    asyncio.run(run_consistency_test())
