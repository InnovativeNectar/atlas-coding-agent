import pytest
from atlas.core.harness import AgentHarness

def test_harness_tool_execution(tmp_path):
    harness = AgentHarness()
    f = tmp_path / "harness_test.txt"
    f.write_text("Initial Content")
    
    # Test read_file through harness
    content = harness.execute_tool("read_file", file_path=str(f))
    assert content == "Initial Content"
    
    # Test replace through harness
    harness.execute_tool("replace", file_path=str(f), old_string="Initial", new_string="Updated")
    assert f.read_text() == "Updated Content"

def test_harness_context():
    harness = AgentHarness()
    context = harness.get_context()
    assert "cwd" in context
    # branch might not be present if not in a git repo during test, but we check if it handles it
    assert isinstance(context["cwd"], str)

def test_unknown_tool():
    harness = AgentHarness()
    with pytest.raises(ValueError, match="Unknown tool"):
        harness.execute_tool("magic_tool")
