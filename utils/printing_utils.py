import textwrap
import pprint

from pydantic_ai import CallToolsNode, ModelRequestNode
from pydantic_ai.messages import TextPart, ThinkingPart, ToolCallPart, SystemPromptPart, UserPromptPart, ToolReturnPart, RetryPromptPart

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[34m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    ORANGE = '\033[38;5;208m'
    MINT = '\033[38;5;121m'

def pretty_print(content, width=120, color=None):
    if color:
        content = f"{color}{content}{bcolors.ENDC}"
    if isinstance(content, str):
        print(textwrap.fill(content, width=width))
    else:
        pprint.pprint(content, width=width, ensure_ascii=False)

def print_agent_node(node):
    if isinstance(node, CallToolsNode):
        for part in node.model_response.parts:
            if isinstance(part, TextPart):
                pretty_print(part.content)
            elif isinstance(part, ToolCallPart):
                pretty_print(f"🔧 [Calling: {part.tool_name} tool] -> {part.args}", color=bcolors.ORANGE)
            elif(isinstance(part, ThinkingPart)):
                pretty_print("💭 [Thinking]", color=bcolors.OKGREEN)
                pretty_print(part.content, color=bcolors.OKGREEN)
            else:
                pretty_print(f"{bcolors.FAIL}DEVINFO: Unexpected part type (in CallToolsNode): {type(part)}", flush=True)
                pretty_print(part)
    elif(isinstance(node, ModelRequestNode)):
        for part in node.request.parts:
            if(isinstance(part, SystemPromptPart)):
                pretty_print(f"[SYSTEM PROMPT] {part.content}", color=bcolors.HEADER)
            elif(isinstance(part, UserPromptPart)):
                pretty_print(f"[USER PROMPT] {part.content}", color=bcolors.HEADER)
            elif(isinstance(part, ToolReturnPart)):
                pretty_print(f"📊 [Tool output] -> {part.content}", color=bcolors.MINT)
            elif(isinstance(part, RetryPromptPart)):
                pretty_print("Output Validation Failed, Retry info:")
                pretty_print(part.content)
            else:
                pretty_print(f"DEVINFO: Unexpected part type (in ModelRequestNode): {type(part)}")
                pretty_print(part)