import ollama
from typing import Generator

def stream_diagnostic(prompt: str, model: str = "llama3.2:3b") -> Generator[str, None, None]:
    """
    Sends a prompt to the local Ollama instance and yields tokens as they arrive.
    Errors are yielded as Markdown (not Rich markup) because callers render
    the stream with rich.markdown.Markdown.
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
    except ollama.ResponseError as e:
        if e.status_code == 404:
            yield (
                f"\n\n**Model not found:** `{model}` is not available in Ollama.\n\n"
                f"Pull it first:\n\n```bash\nollama pull {model}\n```\n"
            )
        else:
            yield f"\n\n**Ollama returned an error:** {e.error}\n"
    except (ConnectionError, OSError) as e:
        yield (
            "\n\n**Could not connect to Ollama.** Is it running?\n\n"
            "Start it with:\n\n```bash\nollama serve\n```\n\n"
            f"Details: {e}\n"
        )
    except Exception as e:
        yield f"\n\n**Error connecting to Ollama:** {e}\n"
