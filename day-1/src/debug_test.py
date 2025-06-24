import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

async def debug_full_flow():
    """Complete test of our setup"""
    print("🧪 Running full debug test...\n")
    try:
        # Step 1: Test configuration
        print("1️⃣ Testing configuration...")
        config, _, _ = create_gemini_config()
        print("✅ Configuration OK\n")

        # Step 2: Test agent creation
        print("2️⃣ Testing agent creation...")
        test_agent = Agent(
            name="Debug Agent",
            instructions="You are a test agent. Just say 'Debug test successful!'",
            model="gemini-2.0-flash"
        )
        print("✅ Agent created OK\n")

        # Step 3: Test agent execution
        print("3️⃣ Testing agent execution...")
        result = await Runner.run(
            test_agent,
            "Please confirm the test is working",
            run_config=config
        )
        print(f"✅ Agent response: {result.final_output}\n")
        print("🎉 All tests passed! Your setup is working perfectly!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Check the error message above and fix the issue")

if __name__ == "__main__":
    asyncio.run(debug_full_flow())
