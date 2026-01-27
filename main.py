from pydantic_ai import Agent, RunContext
import asyncio
import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from tools.bash_tool import create_bash_tool
from utils.agent_utils import run_agent

ollama_model = OpenAIChatModel(
    model_name='mistral:7b',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
)

tools = [
    create_bash_tool(runs_dir=os.getcwd(), 
                     timeout=60, 
                     max_retries=2) 
                     #conda_env_path needs to be set according to your local env 
    ]

agent = Agent(
    ollama_model,
    tools=tools,
    system_prompt="You are an sysadmin expert",
    deps_type=str
)

user_prompt = """Return me the list of files from the current directory in a human friendly way"""

async def main():
    await run_agent(
        agent = agent,
        user_prompt=user_prompt,
        max_steps=10,
        deps=None
    )

asyncio.run(main())