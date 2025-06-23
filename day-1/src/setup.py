import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents import RunConfig

# Load environment variables
load_dotenv()

def create_gemini_config():
    """
    Create configuration for using Gemini API with OpenAI Agents
    Why we do this:
    - OpenAI Agents framework expects OpenAI-compatible API
    - Gemini provides OpenAI-compatible endpoint
    - We create a custom client pointing to Gemini's endpoint
    - We disable tracing since we're not using OpenAI's tracing service
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    # Create external client pointing to Gemini's OpenAI-compatible endpoint
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Create model configuration using Gemini
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",  # Gemini's fast model
        openai_client=external_client
    )

    # Create run configuration
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True  # Disable OpenAI tracing
    )

    return config, external_client, model

# Test the setup
if __name__ == "__main__":
    try:
        config, client, model = create_gemini_config()
        print("✅ Setup successful! Gemini API configured.")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
