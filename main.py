import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.status import Status
from rich.theme import Theme
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from rich import box

from atlas.core.harness import AgentHarness
from atlas.agents.orchestrator import Orchestrator
from atlas.core.heartbeat import Heartbeat
from atlas.auth.handler import AuthHandler

# Custom Theme for Atlas
atlas_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "atlas": "bold blue",
    "dim": "grey50",
    "command": "bold magenta"
})

console = Console(theme=atlas_theme)
app = typer.Typer(
    name="atlas",
    help="Atlas Coding Agent - Your AI-powered pair programmer.",
    add_completion=False,
    no_args_is_help=True
)

harness = AgentHarness()
orchestrator = Orchestrator(harness)
heartbeat = Heartbeat()

def print_header():
    header_text = Text.assemble(
        (" 🌌 ", "atlas"),
        ("ATLAS CODING AGENT", "atlas"),
        (" v1.0.0 ", "dim")
    )
    console.print(Align.center(Panel(header_text, box=box.ROUNDED, border_style="atlas")))

@app.command()
def hello():
    """Say hello and verify installation."""
    print_header()
    heartbeat.pulse("Running 'hello' command")
    status = heartbeat.get_status_report()
    console.print(Align.center(f"[success]Atlas is online![/success] 🚀"))
    console.print(Align.center(f"[dim]Uptime: {status['uptime_seconds']}s[/dim]"))

@app.command()
def chat():
    """Start an interactive coding session."""
    print_header()
    
    prompt = questionary.text(
        "What do you want to do today?",
        instruction="Enter your coding task or 'exit' to quit."
    ).ask()
    
    if not prompt or prompt.lower() in ["exit", "quit"]:
        console.print("[info]Goodbye![/info]")
        return

    heartbeat.pulse(f"Starting chat: {prompt}")
    
    try:
        with console.status("[bold green]Atlas thinking...", spinner="dots"):
            result = orchestrator.plan_and_execute(prompt)
        
        console.print("\n")
        console.print(Panel(result, title="[success]Atlas Response[/success]", border_style="success", box=box.HEAVY))
        heartbeat.pulse("Chat completed")
    except Exception as e:
        console.print_exception(show_locals=True)
        heartbeat.pulse(f"Chat failed: {str(e)}")

@app.command()
def login():
    """Securely log in to the Atlas system."""
    print_header()
    heartbeat.pulse("Attempting login")
    
    console.print(Align.center("[info]Atlas Authentication[/info]"))
    
    username = questionary.text("Username:").ask()
    if not username:
        return
        
    password = questionary.password("Password:").ask()
    if not password:
        return
    
    with console.status("[info]Verifying credentials...", spinner="bouncingBar"):
        # Simulated delay for feedback
        import time
        time.sleep(1)
        
        if username == "admin":
            token = AuthHandler.create_access_token({"sub": username})
            console.print(f"\n[success]Login successful![/success]")
            console.print(Panel(f"Token: [dim]{token}[/dim]", title="Access Granted", border_style="success"))
            heartbeat.pulse("Login successful")
        else:
            console.print("\n[error]Invalid credentials.[/error]")
            heartbeat.pulse("Login failed")

@app.command()
def status():
    """Check the agent's vital signs and heartbeat logs."""
    print_header()
    report = heartbeat.get_status_report()
    
    # Dashboard Layout
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    layout["upper"].split_row(
        Layout(name="vitals"),
        Layout(name="telemetry")
    )
    
    # Vitals Panel
    vitals_table = Table(show_header=False, box=box.SIMPLE)
    vitals_table.add_row("[bold]Uptime[/bold]", f"{report['uptime_seconds']}s")
    vitals_table.add_row("[bold]Tasks Completed[/bold]", f"{report['tasks_completed']}")
    vitals_table.add_row("[bold]Errors[/bold]", f"[red]{report['errors_encountered']}[/red]")
    vitals_table.add_row("[bold]LLM Calls[/bold]", f"{report['llm_calls']}")
    
    layout["vitals"].update(Panel(vitals_table, title="Vitals", border_style="atlas"))
    
    # Telemetry Panel
    telemetry_text = f"[bold]Last Active:[/bold] {report['last_active']}\n"
    telemetry_text += f"[bold]Status:[/bold] [success]Operational[/success]\n"
    layout["telemetry"].update(Panel(telemetry_text, title="Telemetry", border_style="info"))
    
    # Logs Panel
    logs_table = Table(title="Recent Heartbeat Logs", expand=True, box=box.MINIMAL)
    logs_table.add_column("Timestamp", style="dim")
    logs_table.add_column("Event")
    
    for log in report['recent_logs']:
        if "]" in log:
            ts, msg = log.split("]", 1)
            logs_table.add_row(ts.replace("[", ""), msg.strip())
        else:
            logs_table.add_row("-", log)
            
    layout["lower"].update(Panel(logs_table, border_style="dim"))
    
    console.print(layout)

if __name__ == "__main__":
    try:
        app()
    except Exception:
        console.print_exception()
