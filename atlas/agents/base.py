import json
from typing import List, Dict, Any
from atlas.core.harness import AgentHarness
from atlas.core.identity import Identity
from atlas.engine.gemini import DefaultEngine

class SubAgent:
    """Base class for all Atlas subagents with tool-calling capabilities."""

    def __init__(self, persona_key: str, harness: AgentHarness):
        self.persona_key = persona_key
        self.harness = harness
        self.identity = Identity()
        self.system_prompt = self.identity.get_system_prompt(persona_key)
        self.engine = DefaultEngine

    def run(self, task: str) -> str:
        """Execute a task using the agent's persona and tools."""
        # 1. Gather context
        context = self.harness.get_context()
        context_str = json.dumps(context, indent=2)
        
        # 2. Construct prompt
        user_prompt = f"TASK: {task}\n\nENVIRONMENT CONTEXT:\n{context_str}\n\nPlan your actions and call tools if necessary."
        
        # 3. Call LLM
        response = self.engine.ask(self.system_prompt, user_prompt)
        
        # 4. Handle tool calls (Simple parsing for prototype)
        # In a real version, we'd use Structured Outputs or a specific tool-call syntax.
        return response
