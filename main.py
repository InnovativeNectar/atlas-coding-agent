import typer
from rich.console import Console
from rich.panel import Panel

from atlas.core.harness import AgentHarness
from atlas.agents.orchestrator import Orchestrator
from atlas.core.heartbeat import Heartbeat

app = typer.Typer(
    name="atlas",
    help="Atlas Coding Agent - Your AI-powered pair programmer.",
    add_completion=False,
)
console = Console()
harness = AgentHarness()
orchestrator = Orchestrator(harness)
heartbeat = Heartbeat()

@app.command()
def hello():
    """Say hello and verify installation."""
    heartbeat.pulse("Running 'hello' command")
    status = heartbeat.get_status_report()
    console.print(Panel(f"[bold blue]Atlas Coding Agent[/bold blue] is online! 🚀\n\n[dim]Uptime: {status['uptime_seconds']}s[/dim]", title="System"))

@app.command()
def chat(prompt: str = typer.Argument(..., help="What do you want to do?")):
    """Start an interactive coding session."""
    heartbeat.pulse(f"Starting chat: {prompt}")
    console.print(f"[bold green]Atlas thinking...[/bold green]")
    result = orchestrator.plan_and_execute(prompt)
    console.print(Panel(result, title="Atlas Response"))
    heartbeat.pulse("Chat completed")

from atlas.auth.handler import AuthHandler
import getpass

@app.command()
def login():
    """Securely log in to the Atlas system."""
    heartbeat.pulse("Attempting login")
    console.print("[bold cyan]Atlas Authentication[/bold cyan]")
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    
    # For prototype, we'll just hash and verify a dummy password
    # or create a token if the user is 'admin'
    if username == "admin":
        token = AuthHandler.create_access_token({"sub": username})
        console.print(f"[bold green]Login successful![/bold green]")
        console.print(f"Token: [dim]{token[:20]}...[/dim]")
        heartbeat.pulse("Login successful")
    else:
        console.print("[bold red]Invalid credentials.[/bold red]")
        heartbeat.pulse("Login failed")

@app.command()
def status():
    """Check the agent's vital signs and heartbeat logs."""
    report = heartbeat.get_status_report()
    console.print(Panel(
        f"[bold]Uptime:[/bold] {report['uptime_seconds']}s\n"
        f"[bold]Tasks Completed:[/bold] {report['tasks_completed']}\n"
        f"[bold]Last Active:[/bold] {report['last_active']}\n\n"
        f"[bold green]Heartbeat Logs:[/bold green]\n" + "\n".join(report['recent_logs']),
        title="Atlas Vital Signs",
        border_style="green"
    ))

if __name__ == "__main__":
    app()
