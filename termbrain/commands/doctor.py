import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.markdown import Markdown
from termbrain.core.system import get_system_vitals
from termbrain.core.llm import stream_diagnostic

app = typer.Typer()
console = Console()

@app.command(name="check")
def check(ai: bool = typer.Option(False, "--ai", help="Include AI-powered diagnostic advice.")):
    """Perform a system health check."""
    vitals = get_system_vitals()
    
    table = Table(title="[bold blue]System Health Check[/bold blue]")
    table.add_column("Metric", style="cyan")
    table.add_column("Status", style="magenta")

    table.add_row("CPU Load (1/5/15m)", vitals["cpu_load"])
    table.add_row("Memory Used", vitals["memory"])
    table.add_row("Disk Used (/)", vitals["disk"])

    console.print(table)

    if ai:
        console.print("\n[bold yellow]Generating AI Diagnostic...[/bold yellow]")
        
        prompt = (
            f"Here are the current system vitals for my Manjaro Linux machine:\n"
            f"- CPU Load: {vitals['cpu_load']}\n"
            f"- Memory Used: {vitals['memory']}\n"
            f"- Disk Space: {vitals['disk']}\n\n"
            "Based on these, is my system healthy? Give a one-sentence summary and highlight any concerns."
        )

        full_response = ""
        with Live(Markdown(full_response), refresh_per_second=4, console=console) as live:
            for chunk in stream_diagnostic(prompt):
                full_response += chunk
                live.update(Markdown(full_response))

if __name__ == "__main__":
    app()
