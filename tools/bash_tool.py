import subprocess
import re
import threading
import shlex    

from pydantic_ai import Tool

class BashProcess:
    def __init__(self, runs_dir, timeout=60):
        self.locked = threading.Lock()
        self.runs_dir = runs_dir
        self.timeout = timeout

    def run(self, command: str):
        with self.locked: #exclusive bash access
            try:
                run_kwargs = {
                    "shell": True,
                    "executable": "/bin/bash",
                    "timeout": self.timeout,
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.STDOUT,
                    "text": True,
                    "errors": "replace",  # handle invalid UTF-8 bytes
                    "cwd": f"{self.runs_dir}"
                }

                result = subprocess.run(
                    command,
                    **run_kwargs
                )
                output = result.stdout
                if result.stderr:
                    output += result.stderr

                if result.returncode != 0:
                    return f"Command failed with error code {result.returncode}:\n{output}"

                return self.process_output(output, command)
            except subprocess.TimeoutExpired as e:
                return f"Command timed out after {self.timeout} seconds: {e}"
    
    def process_output(self, output: str, command: str) -> str:
        """
        Uses regex to remove the command from the output.
        Return only first 5000 output characters.

        Args:
            output: a process' output string
            command: the executed command
        """
        pattern = re.escape(command) + r"\s*\n"
        output = re.sub(pattern, "", output, count=1)
        if(len(output) > 5000):
            output = output[:5000]+"\n ... (output truncated, too long)"
        return output.strip()

def create_bash_tool(runs_dir, timeout, max_retries, conda_env_path="/usr/local/envs/agents_env"):
        bash = BashProcess(
            timeout=timeout,
            runs_dir=runs_dir,
        )

        def _bash(command: str):
            """
            A persistent bash. 
            Use this to execute bash commands. 
            Input should be a valid bash command.
            Do not use sudo commands, as you don't have sudo access.

            Examples:
            \"ls\"
            \"cd /workspace\"
            \"mkdir test\"
            \"echo "hello world" > test.txt\"
            \"conda install conda-forge::scikit-learn -y\"
            \"df -h\"

            Args:
                command: A valid bash command.
            """  
            command_parsed = shlex.quote(command)
            command = f"conda run -p {conda_env_path} --no-capture-output bash -c {command_parsed}"
            out = bash.run(command)
            return out
    
        bash_tool = Tool(
            function=_bash,
            takes_ctx=False,
            max_retries=max_retries,
            # description=None, # Inferred from the function docstring
            require_parameter_descriptions=True,
            name="bash",
            sequential=True,
        )

        return bash_tool