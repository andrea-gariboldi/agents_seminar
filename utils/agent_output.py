from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    """
    Model representing the output of an agent's clustering task.
    """
    script_path: str = Field(
        description="The full path to the cluster.py script."
    )