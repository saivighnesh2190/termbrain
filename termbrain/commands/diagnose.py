import typer
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from termbrain.core.logs import get_recent_pacman_logs, get_recent_journal_logs
from termbrain.core.llm import stream_diagnostic

app = typer.Typer(help="Diagnose system components using local AI.")
console = Console()

@app.command()
def pacman():
    """Diagnose recent Pacman (package manager) activity."""
    console.print("[bold cyan]Reading /var/log/pacman.log...[/bold cyan]")
    logs = get_recent_pacman_logs()
    
    if logs.startswith("Error:"):
        console.print(f"[bold red]{logs}[/bold red]")
        return
    
    prompt = (
        f"Here are the recent Pacman logs from my Manjaro system:\n\n{logs}\n\n"
        "Analyze these logs. Were there any errors or failed transactions? "
        "Summarize recent activity and suggest fixes if anything looks broken."
    )

    full_response = ""
    with Live(Markdown(full_response), refresh_per_second=4, console=console) as live:
        for chunk in stream_diagnostic(prompt):
            full_response += chunk
            live.update(Markdown(full_response))

@app.command()
def journal():
    """Diagnose recent system journal (journalctl) errors."""
    console.print("[bold cyan]Reading system journal...[/bold cyan]")
    logs = get_recent_journal_logs()
    
    console.print("[bold yellow]Generating AI Diagnosis...[/bold yellow]\n")
    
    prompt = (
        f"Here are the recent system journal logs:\n\n{logs}\n\n"
        "Identify any critical errors or service failures. "
        "Explain what's happening and how to fix it."
    )

    full_response = ""
    with Live(Markdown(full_response), refresh_per_second=4, console=console) as live:
        for chunk in stream_diagnostic(prompt):
            full_response += chunk
            live.update(Markdown(full_response))
