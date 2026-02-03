import textwrap
import pprint
import json

from pydantic_ai import CallToolsNode, ModelRequestNode
from pydantic_ai.messages import TextPart, ThinkingPart, ToolCallPart, SystemPromptPart, UserPromptPart, ToolReturnPart, RetryPromptPart
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalTrueColorFormatter as TF
from pygments.formatters import TerminalFormatter as TF

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[34m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    OKBLUE = '\033[94m'
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
                if part.tool_name == 'write_python_file':
                    pretty_print(f"🔧 [Calling: {part.tool_name}]", color=bcolors.ORANGE)
                    args_dict = json.loads(str(part.args))
                    pretty_print_code(args_dict.get('code'))
                else:
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
                content = part.content if part.content else "<no output>"
                pretty_print(f"📊 [Tool output] -> {content}", color=bcolors.MINT)
            elif(isinstance(part, RetryPromptPart)):
                pretty_print("Output Validation Failed, Retry info:")
                pretty_print(part.content)
            else:
                pretty_print(f"DEVINFO: Unexpected part type (in ModelRequestNode): {type(part)}")
                pretty_print(part)

def pretty_print_code(code):
    """
    Pretty print Python code with syntax highlighting and line numbers.
    args:
        code (str): The code string to pretty print.
    """
    if not code:
        return

    # normalize escapes and dedent
    code = code.replace('\\r\\n', '\n').replace('\\r', '\n')
    code = code.replace('\\t', '\t').replace('\\n', '\n')
    code = textwrap.dedent(code).strip('\n') + '\n'

    header = f"{bcolors.BOLD}{bcolors.OKCYAN}----- CODE START -----{bcolors.ENDC}"
    footer = f"{bcolors.BOLD}{bcolors.OKCYAN}-----  CODE END  -----{bcolors.ENDC}"
    print(header)

    try:
        # Try to use pygments for nice terminal highlighting
        # Prefer truecolor formatter if available, fall back to standard terminal formatter
        try:
            formatter = TF()
        except Exception:
            formatter = TF()

        highlighted = highlight(code, PythonLexer(), formatter)
        lines = highlighted.splitlines()
        width = len(str(len(lines)))
        for i, ln in enumerate(lines, 1):
            lineno = f"{bcolors.BOLD}{bcolors.OKBLUE}{str(i).rjust(width)}{bcolors.ENDC} "
            # ln already contains color codes from pygments
            print(f"{lineno}{ln}")
    except Exception:
        # Fallback: simple numbered output without external coloring
        lines = code.splitlines()
        width = len(str(len(lines)))
        for i, ln in enumerate(lines, 1):
            lineno = f"{bcolors.BOLD}{bcolors.OKBLUE}{str(i).rjust(width)}{bcolors.ENDC} "
            print(f"{lineno}{ln}")

    print(footer)

def print_eval_message(message: str, is_error: bool = False):
    if is_error:
        pretty_print(message, color=bcolors.FAIL)
    else:
        pretty_print(message, color=bcolors.BLUE)