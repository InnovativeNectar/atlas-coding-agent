import os
import pytest
from atlas.tools.file_system import FileSystem

def test_read_file(tmp_path):
    d = tmp_path / "testdir"
    d.mkdir()
    f = d / "hello.txt"
    content = "Line 1\nLine 2\nLine 3"
    f.write_text(content)
    
    # Test full read
    assert FileSystem.read_file(str(f)) == content
    
    # Test partial read
    assert FileSystem.read_file(str(f), start_line=1, end_line=1) == "Line 1\n"
    assert FileSystem.read_file(str(f), start_line=2) == "Line 2\nLine 3"

def test_replace(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Hello World")
    
    # Test successful replace
    FileSystem.replace(str(f), "World", "Atlas")
    assert f.read_text() == "Hello Atlas"
    
    # Test ambiguous replace
    f.write_text("Repeat Repeat")
    with pytest.raises(ValueError, match="Ambiguous replacement"):
        FileSystem.replace(str(f), "Repeat", "Single")
        
    # Test multiple replace
    FileSystem.replace(str(f), "Repeat", "Multiple", allow_multiple=True)
    assert f.read_text() == "Multiple Multiple"

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        FileSystem.read_file("non_existent_file.txt")
