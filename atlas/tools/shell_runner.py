import subprocess
from typing import Dict, Any

class ShellRunner:
    """Safe shell command execution for Atlas."""

    @staticmethod
    def run(command: str, timeout: int = 30) -> Dict[str, Any]:
        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"error": str(e)}
