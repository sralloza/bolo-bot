import re
from pathlib import Path

import typer

try:
    import pyperclip
except ImportError:
    typer.secho("You need to install pyperclip", fg="bright_red")
    raise typer.Abort()

app = typer.Typer(add_completion=False)


@app.command()
def copy_commands():
    commands_path = Path(__file__).parent.with_name("commands.md")
    commands_info = commands_path.read_text("utf8")

    filtered = []
    for line in commands_info.splitlines():
        if line.strip().startswith("-"):
            line = re.sub(r"- `\/([\w]+)`", r"\1", line)
            filtered.append(line)

    result = "\n".join(filtered)
    pyperclip.copy(result)
    typer.secho("Done", fg="bright_green")


if __name__ == "__main__":
    app()
