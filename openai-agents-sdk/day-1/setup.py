import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents import RunConfig

load_dotenv()

def create_gemini_setup():
    """
    Create configuration for using Gemini API with OpenAI Agents
    """
    
    gemini_api=os.getenv("GEMINI_API_KEY")
    
    if not gemini_api :
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    external_client=AsyncOpenAI(
        api_key=gemini_api,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config=RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    
    return config,model,external_client

if __name__=="__main__":
    print("setup check is Running")
    config,model,external_client=create_gemini_setup()
    print("The Setup is Successful")

else:
    print("Setup Failed")
