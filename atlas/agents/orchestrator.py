from typing import List
from atlas.agents.base import SubAgent
from atlas.core.harness import AgentHarness
from rich.console import Console

console = Console()

class Orchestrator(SubAgent):
    """The central brain that coordinates specialized subagents."""

    def __init__(self, harness: AgentHarness):
        super().__init__("orchestrator", harness)
        self.investigator = SubAgent("investigator", harness)
        self.coder = SubAgent("coder", harness)

    def plan_and_execute(self, user_goal: str):
        """Standard delegation workflow."""
        
        # 1. Start with the Orchestrator's own thinking/planning
        with console.status("[bold blue]Atlas Prime[/bold blue] is planning the mission...", spinner="bouncingBall"):
            plan = self.run(f"Create a high-level plan for: {user_goal}")
        console.print("[dim]→ Strategy formulated.[/dim]")
        
        # 2. Delegate to Investigator for research
        with console.status("[bold cyan]Atlas Deep[/bold cyan] is researching codebase requirements...", spinner="aesthetic"):
            research = self.investigator.run(f"Based on this plan, research the requirements: {plan}")
        console.print("[dim]→ Research phase complete.[/dim]")
        
        # 3. Delegate to Coder for implementation
        with console.status("[bold green]Atlas Craft[/bold green] is implementing the solution...", spinner="earth"):
            result = self.coder.run(f"Implement the changes using the research: {research}")
        console.print("[dim]→ Implementation finalized.[/dim]")
        
        return result
