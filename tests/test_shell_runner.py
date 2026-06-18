import pytest
from atlas.tools.shell_runner import ShellRunner

def test_run_success():
    result = ShellRunner.run("echo 'Hello Atlas'")
    assert result["exit_code"] == 0
    assert "Hello Atlas" in result["stdout"]

def test_run_failure():
    result = ShellRunner.run("non_existent_command_12345")
    assert result["exit_code"] != 0
    assert result["stderr"] != ""

def test_run_timeout():
    # Use a command that sleeps longer than the default timeout in tests if possible, 
    # but here we'll just check if it handles it.
    result = ShellRunner.run("sleep 2", timeout=1)
    assert "timed out" in result["error"].lower()
