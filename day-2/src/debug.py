# src/day2/debug_guide.py
import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

async def debug_model_parameters():
    """
    Debug common issues with model parameters
    """
    print("🔧 Debugging Model Parameters...\n")
    
    # Issue 1: Invalid temperature values
    try:
        print("Testing invalid temperature (1.5)...")
        config, _, _ = create_gemini_config(temperature=1.0)  # Too high!
        print("❌ This should have failed but didn't - check your validation")
    except Exception as e:
        print(f"✅ Correctly caught invalid temperature: {e}")
    
    # Issue 2: Negative max_tokens
    try:
        print("\nTesting negative max_tokens...")
        config, _, _ = create_gemini_config(max_tokens=100)  # Invalid!
        print("❌ This should have failed but didn't")
    except Exception as e:
        print(f"✅ Correctly caught invalid max_tokens: {e}")
    
    # Issue 3: Testing valid ranges
    print("\nTesting valid parameter ranges...")
    valid_configs = [
        (0.1, 100),   # Minimum creativity, short responses
        (0.5, 500),   # Balanced
        (1.0, 2000),  # Maximum creativity, longer responses
    ]
    
    for temp, tokens in valid_configs:
        try:
            config, _, _ = create_gemini_config(temperature=temp, max_tokens=tokens)
            print(f"✅ Valid config: temp={temp}, max_tokens={tokens}")
        except Exception as e:
            print(f"❌ Unexpected error with temp={temp}, tokens={tokens}: {e}")

async def debug_agent_instructions():
    """
    Debug common issues with agent instructions
    """
    print("\n🎭 Debugging Agent Instructions...\n")
    
    config, _, _ = create_gemini_config()
    
    # Issue 1: Empty instructions
    try:
        print("Testing empty instructions...")
        agent = Agent(
            name="Empty Agent",
            instructions="greet the user",
            model="gemini-2.0-flash"
        )
        result = await Runner.run(agent, "Hello", run_config=config)
        print(f"Result with empty instructions: {result.final_output}")
    except Exception as e:
        print(f"Error with empty instructions: {e}")
    
    # Issue 2: Very long instructions
    try:
        print("\nTesting very long instructions...")
        long_instructions = "You are a helpful assistant. "  # Very long
        agent = Agent(
            name="Verbose Agent",
            instructions=long_instructions,
            model="gemini-2.0-flash"
        )
        result = await Runner.run(agent, "Hello", run_config=config)
        print("✅ Long instructions handled successfully")
    except Exception as e:
        print(f"❌ Error with long instructions: {e}")
    
    # Issue 3: Conflicting instructions
    print("\nTesting conflicting instructions...")
    conflicting_agent = Agent(
        name="Conflicted Agent",
        instructions="""You are both a formal business assistant.
        Always be professional.
        Give brief answers""",
        model="gemini-2.0-flash"
    )
    
    result = await Runner.run(
        conflicting_agent, 
        "Explain machine learning", 
        run_config=config
    )
    print(f"Result with conflicting instructions: {result.final_output[:200]}...")

async def debug_async_patterns():
    """
    Debug common async/await issues
    """
    print("\n⚡ Debugging Async Patterns...\n")
    
    config, _, _ = create_gemini_config()
    agent = Agent(
        name="Test Agent",
        instructions="Be helpful and brief.",
        model="gemini-2.0-flash"
    )
    
    # Issue 1: Forgetting await
    print("❌ Common mistake - forgetting await:")
    print("# This will NOT work:")
    print("# result = Runner.run(agent, 'Hello', run_config=config)")
    print("# print(result.final_output)  # Error: result is a coroutine!")
    
    print("\n✅ Correct way:")
    result = await Runner.run(agent, "Hello", run_config=config)
    print(f"Correct result: {result.final_output}")
    
    # Issue 2: Running multiple agents concurrently
    print("\n🚀 Running multiple agents concurrently:")
    
    agents = [
    Agent(
        name=f"Agent {i}",
        instructions="Be helpful",  # ✅ Fix: set explicitly
        model="gemini-2.0-flash"
    )
    for i in range(3)
]

    
    # Correct way to run multiple agents
    tasks = [
        Runner.run(agent, f"What is {2**i}?", run_config=config)
        for i, agent in enumerate(agents)
    ]
    
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"Agent {i} result: {result.final_output}")

def debug_common_errors():
    """
    Debug non-async common errors
    """
    print("\n🔍 Common Error Patterns...\n")
    
    # Issue 1: Module import errors
    print("1. Import Issues:")
    try:
        from agents import Agent, Runner
        print("✅ Correct imports working")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Solution: Make sure you installed openai-agents-python")
    
    # Issue 2: Environment variable issues
    print("\n2. Environment Variables:")
    import os
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        print("💡 Solution: Check your .env file")
    else:
        print(f"✅ API key found (length: {len(api_key)})")
    
    # Issue 3: Model name typos
    print("\n3. Model Name Issues:")
    valid_models = ["gemini-2.0-flash", "gemini-1.5-pro"]
    test_model = "gemini-2.0-flash"  # Common typo: "flash" vs "Flash"
    
    if test_model in valid_models:
        print(f"✅ Model name '{test_model}' is valid")
    else:
        print(f"❌ Model name '{test_model}' might be invalid")
        print("💡 Check documentation for correct model names")

async def comprehensive_debug_test():
    """
    Run all debug tests
    """
    print("🧪 Running Comprehensive Debug Test\n")
    print("=" * 60)
    
    # Run all debug functions
    debug_common_errors()
    await debug_model_parameters()
    await debug_agent_instructions()
    await debug_async_patterns()
    
    print("\n✅ All debug tests completed!")
    print("💡 If you see any errors above, review the solutions provided")

if __name__ == "__main__":
    asyncio.run(comprehensive_debug_test())
