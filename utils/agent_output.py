from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    script_path: str = Field(
        description="The full path to the cluster.py script."
    )