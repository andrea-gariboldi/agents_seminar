import traceback

from pydantic_ai import Agent, capture_run_messages
from pydantic_ai.usage import UsageLimits
from pydantic_ai.exceptions import UsageLimitExceeded

from utils.printing_utils import print_agent_node as pretty_print_node

async def run_agent(agent: Agent, user_prompt: str, max_steps: int, deps=None):
    with capture_run_messages():
        try:
            async with agent.iter(
                user_prompt=user_prompt,
                usage_limits=UsageLimits(request_limit=max_steps),
                deps=deps,
            ) as agent_run:
                async for node in agent_run:
                    pretty_print_node(node)
                return agent_run.result.output

        except Exception as e:
            trace = traceback.format_exc()
            print('--------------- ERROR TRACEBACK ---------------')
            print('Agent run failed', trace)
            print('--------------- ERROR TRACEBACK ---------------')
        except UsageLimitExceeded as ule:
            print('---------------AGENT EXCEEDED CALLS LIMIT ---------------')
            print(f'Agent run stopped: {str(ule)}')
            print('---------------AGENT EXCEEDED CALLS LIMIT ---------------')