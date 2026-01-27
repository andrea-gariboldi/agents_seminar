from pydantic_ai import Agent, RunContext
import asyncio
import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from tools.bash_tool import create_bash_tool
from utils.agent_utils import run_agent
from eval.evaluate_result import evaluate_clustering

ollama_model = OpenAIChatModel(
    model_name='mistral:7b',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
)

tools = [
    create_bash_tool(runs_dir=os.getcwd(), 
                     timeout=60, 
                     max_retries=2, conda_env_path="/home/agari01/miniconda3/envs/agents_env") 
                     #conda_env_path needs to be set according to your local env 
    ]

agent = Agent(
    ollama_model,
    tools=tools,
    system_prompt="You are an expert agent with bash scripting skills. Use the tools provided to answer the user's requests.",
    deps_type=str
)

user_prompt = """Your final deliverable is to cluster a datasets. The sumbmission file should contain the original columns: feat1, feat2, feat3, feat4 plus a new column cluster_id indicating the cluster assignment for each row.
            The original dataset is: /home/agari01/agents_seminar/dataset.csv. Save the file as submission.csv in the current working directory.            
            """

async def main():
    await run_agent(
        agent = agent,
        user_prompt=user_prompt,
        max_steps=10,
        deps=None
    )

    evaluate_clustering(submission_path="/home/agari01/agents_seminar/submission.csv")

asyncio.run(main())