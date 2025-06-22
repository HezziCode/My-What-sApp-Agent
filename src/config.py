from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunConfig    # type: ignore
from dotenv import load_dotenv
import os


load_dotenv()

gemini_api = os.getenv("GEMINI_API_KEY")
if not gemini_api:
    raise ValueError("Api key not set")



client = AsyncOpenAI(
    api_key=gemini_api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

