import os
from typing import List, Dict, Any
from atlas.tools.file_system import FileSystem
from atlas.tools.shell_runner import ShellRunner

class AgentHarness:
    """The execution environment for Atlas subagents."""

    def __init__(self):
        self.tools = {
            "read_file": FileSystem.read_file,
            "replace": FileSystem.replace,
            "run_shell": ShellRunner.run
        }

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self.tools[tool_name](**kwargs)

    def get_context(self) -> Dict[str, Any]:
        """Gathers environmental context (cwd, git branch, etc.)"""
        context = {
            "cwd": os.getcwd(),
        }
        # Add git info if available
        git_info = ShellRunner.run("git branch --show-current")
        if git_info.get("exit_code") == 0:
            context["branch"] = git_info["stdout"].strip()
        return context
