from rich.console import Console
from rich.panel import Panel

console = Console()

def display_welcome():
    console.print(Panel("[bold green]TermBrain v0.1.0[/bold green] - Your privacy-first AI diagnostic assistant.", border_style="blue"))
