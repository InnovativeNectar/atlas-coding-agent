import os
import re
from typing import Optional

class FileSystem:
    """Atomic file system operations for Atlas."""

    @staticmethod
    def read_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        start = (start_line - 1) if start_line else 0
        end = end_line if end_line else len(lines)
        return "".join(lines[start:end])

    @staticmethod
    def replace(file_path: str, old_string: str, new_string: str, allow_multiple: bool = False) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        count = content.count(old_string)
        if count == 0:
            raise ValueError(f"Target string not found in {file_path}")
        if count > 1 and not allow_multiple:
            raise ValueError(f"Ambiguous replacement: {count} occurrences found in {file_path}")
            
        new_content = content.replace(old_string, new_string)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return f"Successfully updated {file_path}"
