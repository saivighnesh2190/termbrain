import typer
from rich.console import Console
from termbrain.ui.display import display_welcome
from termbrain.commands import doctor, diagnose

app = typer.Typer(help="TermBrain: Your local AI-powered Linux diagnostic tool.")

# Add command groups
app.add_typer(doctor.app, name="doctor", help="Check system vitals.")
app.add_typer(diagnose.app, name="diagnose", help="Diagnose specific logs (pacman, journal).")

console = Console()

@app.command()
def welcome():
    """Welcome to TermBrain."""
    display_welcome()

if __name__ == "__main__":
    app()
