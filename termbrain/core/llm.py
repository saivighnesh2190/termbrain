import ollama
from typing import Generator

def stream_diagnostic(prompt: str, model: str = "llama3.2:3b") -> Generator[str, None, None]:
    """
    Sends a prompt to the local Ollama instance and yields tokens as they arrive.
    """
    system_prompt = (
        "You are TermBrain, a senior Linux systems engineer. "
        "Provide concise, technical, and actionable advice based on the provided system vitals. "
        "Use markdown formatting. Avoid fluff."
    )

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ],
            stream=True,
        )
        for chunk in response:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    except Exception as e:
        yield f"\n[bold red]Error connecting to Ollama:[/bold red] {str(e)}"
