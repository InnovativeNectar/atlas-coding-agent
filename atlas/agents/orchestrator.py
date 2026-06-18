from typing import List
from atlas.agents.base import SubAgent
from atlas.core.harness import AgentHarness

class Orchestrator(SubAgent):
    """The central brain that coordinates specialized subagents."""

    def __init__(self, harness: AgentHarness):
        super().__init__("orchestrator", harness)
        self.investigator = SubAgent("investigator", harness)
        self.coder = SubAgent("coder", harness)

    def plan_and_execute(self, user_goal: str):
        """Standard delegation workflow."""
        # 1. Start with the Orchestrator's own thinking/planning
        plan = self.run(f"Create a high-level plan for: {user_goal}")
        
        # 2. Delegate to Investigator for research
        research = self.investigator.run(f"Based on this plan, research the requirements: {plan}")
        
        # 3. Delegate to Coder for implementation
        result = self.coder.run(f"Implement the changes using the research: {research}")
        
        return result
