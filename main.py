from pydantic_ai import Agent
import asyncio
import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from tools.bash_tool import create_bash_tool
from utils.agent_utils import run_agent
from eval.evaluate_result import evaluate_clustering

ollama_model = OpenAIChatModel(
    model_name='ministral-3:3b',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
)

tools = [
    create_bash_tool(runs_dir=f"{os.getcwd()}/agents_workspace/",
                     timeout=60,
                     max_retries=2
                     )
    ]

agent = Agent(
    ollama_model,
    tools=tools,
    system_prompt="You are an expert agent with bash scripting skills. Use the tools provided to answer the user's requests. Always create python files instead of defining and running them directly through bash tool.",
    deps_type=str
)

user_prompt = f"""Your final deliverable is to cluster a datasets. The sumbmission file should contain the original columns: feat1, feat2, feat3, feat4 plus a new column cluster_id indicating the cluster assignment for each row.
            The original dataset is in the directory: {os.getcwd()}/agents_workspace/data/. Save the file as submission.csv in the current working directory.            
            """

async def main():
    await run_agent(
        agent = agent,
        user_prompt=user_prompt,
        max_steps=10,
        deps=None
    )

    evaluate_clustering(submission_path=f"{os.cwd()}/submission.csv")

asyncio.run(main())