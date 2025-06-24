# enhanced_setup.py
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.model_settings import ModelSettings
from agents import RunConfig

# Load environment variables
load_dotenv()

def create_gemini_config(temperature=0.7, max_tokens=1000):
    """
    Enhanced configuration with model parameters
    
    Why we add parameters:
    - temperature: Controls creativity (0.0 = very focused, 1.0 = very creative)
    - max_tokens: Limits response length
    - These help us fine-tune agent behavior
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Create external client pointing to Gemini's OpenAI-compatible endpoint
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    # Create model without parameters (they go in RunConfig)
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    )
    model_settings=ModelSettings(
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Create run configuration with model parameters
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,  # Still disable OpenAI tracing
        model_settings=model_settings
    )
    
    return config, external_client, model

def create_different_model_configs():
    """
    Create multiple configurations for different use cases
    
    Why multiple configs:
    - Different tasks need different settings
    - Creative tasks: high temperature
    - Analytical tasks: low temperature
    - Long responses vs short responses
    """
    return {
        'creative': create_gemini_config(temperature=0.9, max_tokens=1500),
        'analytical': create_gemini_config(temperature=0.2, max_tokens=800),
        'balanced': create_gemini_config(temperature=0.7, max_tokens=1000),
        'concise': create_gemini_config(temperature=0.5, max_tokens=200)
    }

# Test the enhanced setup
if __name__ == "__main__":
    try:
        # Test basic config
        config, client, model = create_gemini_config()
        print("✅ Basic setup successful!")
        
        # Test multiple configs
        configs = create_different_model_configs()
        print(f"✅ Created {len(configs)} different configurations!")
        
        for name, (cfg, _, _) in configs.items():
            print(f"  - {name.capitalize()} config ready")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
