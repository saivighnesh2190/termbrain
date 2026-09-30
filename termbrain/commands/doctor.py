import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.markdown import Markdown
from termbrain.core.system import get_system_vitals
from termbrain.core.llm import stream_diagnostic

app = typer.Typer()
console = Console()


def _build_ai_prompt(vitals):
    """Build a beginner-friendly Manjaro health-check prompt."""
    return f"""Analyze these current system vitals from a Manjaro Linux machine:

- Logical CPU cores: {vitals['cpu_cores']}
- CPU load average (1, 5, and 15 minutes): {vitals['cpu_load']}
- Memory used: {vitals['memory']}
- Memory available: {vitals['memory_available']}
- Root disk used: {vitals['disk']} ({vitals['disk_percent']})

The user is still learning Linux. Explain the result in clear, beginner-friendly language without assuming prior knowledge.

Use this Markdown structure:
## Overall health
Give a direct one- or two-sentence verdict.

## CPU
Explain what the three load averages mean, compare them with the logical CPU core count, describe the recent trend, and say whether the load is healthy.

## Memory
Explain used versus available memory, mention that Linux uses RAM for cache, and say whether there is any concern.

## Disk
Explain the root disk usage percentage and say whether action is needed.

## Recommended next steps
Only include this section when a value is concerning or unknown. Suggest safe, read-only commands for investigating it and briefly explain each command. Never suggest destructive commands.

Do not invent causes, processes, temperatures, or hardware details that are not present in the data. Keep the response concise and actionable."""


@app.command(name="check")
def check(ai: bool = typer.Option(False, "--ai", help="Explain system health with local AI.")):
    """Perform a system health check."""
    vitals = get_system_vitals()
    
    table = Table(title="[bold blue]System Health Check[/bold blue]")
    table.add_column("Metric", style="cyan")
    table.add_column("Status", style="magenta")

    table.add_row("Logical CPU Cores", str(vitals["cpu_cores"]))
    table.add_row("CPU Load (1/5/15m)", vitals["cpu_load"])
    table.add_row("Memory Used", vitals["memory"])
    table.add_row("Memory Available", vitals["memory_available"])
    table.add_row("Disk Used (/)", f"{vitals['disk']} ({vitals['disk_percent']})")

    console.print(table)

    if ai:
        console.print("\n[bold yellow]Generating AI explanation...[/bold yellow]")
        prompt = _build_ai_prompt(vitals)

        full_response = ""
        with Live(Markdown(full_response), refresh_per_second=4, console=console) as live:
            for chunk in stream_diagnostic(prompt):
                full_response += chunk
                live.update(Markdown(full_response))

if __name__ == "__main__":
    app()
