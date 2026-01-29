from pydantic_ai import Agent
import asyncio
import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from tools.bash_tool import create_bash_tool
from utils.agent_utils import run_agent
from utils.workspace_utils import cleanup_workspace
from eval.evaluate_result import evaluate_clustering
from utils.dataset_utils import get_columns_from_dataset

cleanup_workspace() # careful, this will delete all files produced by previous agent runs (except the dataset)

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
    system_prompt="You are an expert agent with bash scripting skills. Use the tools provided to answer the user's requests. Always create python files intead of running python scripts directly in bash." \
    "Do not assume the script will be run by the user, you should be the one running them",
    deps_type=str
)

user_prompt = f"""Your final deliverable is to cluster a dataset. The sumbmission file should contain the original columns: {get_columns_from_dataset("agents_workspace/data/ecoli.csv")} plus a new column cluster_id indicating the cluster assignment for each row.
            The original dataset is in the directory: {os.getcwd()}/agents_workspace/data/. Save the file as submission.csv in the current working directory.            
            """

async def main():
    await run_agent(
        agent = agent,
        user_prompt=user_prompt,
        max_steps=10,
        deps=None
    )

    evaluate_clustering(submission_path=f"{os.getcwd()}/agents_workspace/submission.csv")

asyncio.run(main())